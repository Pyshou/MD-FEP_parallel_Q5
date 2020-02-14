#!/home/apps/bin/python2.7
import argparse
import datetime
import logging
import shutil
import sys
import textwrap
import os

import clustersettings as s
sys.path.append(s.BINDIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "http_settings")
import http_settings
from http_models import *

import complex
import gromacs
import membrane
import protein
import queue
import recipes
import clustersettings

from subprocess import call
import broker



class Run(object):
    #This is a dummy
    def __init__(self, dynamic_pk, *args, **kwargs):
        '''
        This is an specialized version of run.py, but it's able to interact
        with the remote DB to get the values without being explicitly provided

        A "Run()" of molecular dynamics MUST be provided with a "pdb"
        
        This class tries to initiate a full complex and send it to simulation. Given
        a bunch of molecules (protein, ligand, other ligand, waters, ...), 
        this class builds a full embedded-in-membrane complex.

        These complexes are stored in self.g (A "Gromacs" object), and thus
        can be 'runned' through g.recipe and g.run_recipe procedures. See
        gromacs.py for more information.

        Here, the queue system is also created for use in certain steps.'''

        self.dynamic = DynamicDynamic.objects.get(pk = dynamic_pk)
        if kwargs.get("broker_pk"):
            self.broker = broker.DjangoDB(pk=kwargs.get("broker_pk"))
        else:
            self.broker = broker.Printing()

        self.pdb = os.path.join(http_settings.CUELEBRE_ROOT,
            self.dynamic.pdb.file_path)

        user = str(self.dynamic.pdb.project.user_id.username)
        project = str(self.dynamic.pdb.project.name)
        id_ = str(self.dynamic.pk)
        self.own_dir = os.path.join(http_settings.CUELEBRE_ROOT,
            user, project, "dynamic", id_)

        if not (os.path.isdir(self.own_dir)):
            os.makedirs(self.own_dir)
            self.broker.dispatch(
                "Created working dir {0}".format(self.own_dir))

        os.chdir(self.own_dir)

        self.repo_dir = kwargs.get("repo_dir") or ""
        self.ligand = self.dynamic.ligand or ""
        self.alosteric = self.dynamic.alosteric or ""
        self.waters = self.dynamic.waters or ""
        self.ions = self.dynamic.ions or ""
        self.cho = self.dynamic.cholesterol or ""
        self.queue = kwargs.get("queue") or ""
        self.debug = kwargs.get("debug") or False

        # Configure all paths to all compounds in the mix
        self.make_mix()

        #And now start to set up the Complex before running.
        if self.pdb:
            self.pdb = protein.Monomer(pdb = self.pdb)

        self.membr = membrane.Membrane()

        prot_complex = protein.ProteinComplex(
            monomer = self.pdb,
            ligand = self.ligand or None,
            alosteric = self.alosteric or None,
            waters = self.waters or None,
            ions = self.ions or None,
            cho = self.cho or None)
        full_complex = complex.MembraneComplex()
        full_complex.complex = prot_complex
        full_complex.membrane = self.membr

        self.g = gromacs.Gromacs(membrane_complex = full_complex,
            broker=self.broker)

        # Note that if not provided in command line, self.queue is set in
        # settings.py
        if self.queue:
            if self.queue == "slurm":
                my_queue = queue.Slurm()
            elif self.queue == "pbs":
                my_queue = queue.PBS()
            elif self.queue == "pbs_ib":
                my_queue = queue.PBS_IB()
            elif self.queue == "svgd":
                my_queue = queue.Svgd()
        else:
            my_queue = queue.NoQueue()

        self.g.queue = my_queue

    def clean(self):
        '''Removes all previously generated files'''
        to_unlink = ["#index.ndx.1#", "#ligand_ha.ndx.1#", "#mdout.mdp.1#",
            "#mdout.mdp.2#", "#mdout.mdp.3#", "#mdout.mdp.4#", "#mdout.mdp.5#",
            "#mdout.mdp.6#", "#mdout.mdp.7#", "#mdout.mdp.8#", "#mdout.mdp.9#",
            "#output.pdb.1#", "#output.tpr.1#", "#popc.pdb.1#",
            "#posre.itp.1#", "#proteinopls.pdb.1#", "#proteinopls.pdb.2#",
            "#proteinopls.pdb.3#", "#proteinopls.pdb.4#","#protein.top.1#",
            "#protpopc.pdb.1#", "#protpopc.pdb.2#", "#tmp.pdb.1#",
            "#topol.top.1#", "#topol.top.2#", "#topol.top.3#",
            "#topol.tpr.1#", "#topol.tpr.2#", "#topol.tpr.3#",
            "#topol.tpr.4#", "#water.pdb.1#", "ener_EQ.edr", 
            "ffoplsaabon_mod.itp", "ffoplsaa_mod.itp", "ffoplsaanb_mod.itp",
            "genion.log", "hexagon.pdb", "index.ndx",
            "ligand_ha.ndx", "mdout.mdp", "min.pdb",
            "output.pdb", "output.tpr", "popc.pdb", "popc.itp", "posre.itp",
            "posre_lig.itp", "protein.itp", "protein.top",
            "protein_ca200.itp", "proteinopls.pdb", "proteinopls-ligand.pdb",
            "protpopc.pdb", "steep.mdp", "traj.xtc", "traj_EQ.xtc", "tmp.pdb",
            "topol.top", "topol.tpr", "tmp_proteinopls.pdb", "water.pdb"]

        dirs_to_unlink = ["Rmin", "eq", "eqCA"]

        for target in to_unlink:
            if os.path.isfile(target): os.unlink(target)

        for target in dirs_to_unlink:
            if os.path.isdir(target): shutil.rmtree(target)
    
        return True

    def make_mix(self):
        '''Explore all ingredients and set the file paths'''
        #TODO: to be added the Lipids
        sugars = {"ligand": "Ligand",
            "alosteric": "Alosteric",
            "waters": "CrystalWaters",
            "ions": "Ions",
            "cho": "Cholesterol"}

        for sugar_type, class_name in sugars.iteritems():
            if getattr(self, sugar_type):
                #Get the molecule to be added to the mix
                base_model = getattr(self, sugar_type)
                # Some molecules don't need itp nor ff (water and ions),
                # Their constructors fill in with default if not provided.
                # Here we check if the user provided the fields
                kwargs = {"pdb": None, "itp": None, "ff": None}
                for type, uploaded_file in kwargs.iteritems():
                    kwargs[type] = getattr(base_model, type, None)
                    #If there was a file uploaded, set the absolute path
                    if kwargs[type]:
                        kwargs[type] = os.path.join(
                            http_settings.CUELEBRE_ROOT, kwargs[type])

                # And now we set all these files to the compound Class
                # The constructor should complain it it need the file,
                # or fall back to the default files
                setattr(self, sugar_type,
                    getattr(protein, class_name)(**kwargs))
        return True

    def moldyn(self):
        '''Runs all the dynamics'''

        steps = ["Init", "Minimization", "Equilibration",
            "Relax", "CARelax", "CollectResults"]

        for step in steps:
            self.g.select_recipe(stage = step, debug = self.debug)
            self.g.run_recipe(debug = self.debug)

    def send_email(self):
        '''Send an email to the user who launched the dynamic'''
        from django.core.mail import send_mail
        email_addr = self.dynamic.pdb.project.user_id.email

        body_msg = ["You can check this dynamic at http://gpcr-modsim.org",
                    "/dynamic/{0}".format(self.dynamic.pk)]
        
        send_mail("GPCR-ModSim ended a Molecular Dynamics Run",
            "".join(body_msg),
            http_settings.EMAIL_HOST_USER, [email_addr])

    def set_file_path(self):
        '''If all the dynamic run fine, update the file_path in the DB'''
        self.dynamic.file_path = os.path.join(
            os.path.relpath(
                self.own_dir, http_settings.CUELEBRE_ROOT),
                "MD_output.tgz")
        self.dynamic.save()
        return True

def update_queue(queue_obj, status, timefield):
      '''Update a queue_obj (a DB Table) with current status (Started, Running,
      ...) in the timefield appropiate (started, ended)'''
      now = datetime.datetime.now()

      setattr(queue_obj, timefield, now)
      queue_obj.last_status = status
      if(timefield == "started"): queue_obj.ended = None
      queue_obj.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent('''\
    == This script runs a Molecular Dynamic with a Dynamic PK. ==
    '''))

    parser.add_argument('-r',
        dest = "repo_dir",
        help = "Path to templates of fixed files. If not \
            provided, take the value from settings.REPO_DIR.",
        default = clustersettings.REPO_DIR)
    parser.add_argument('-d',
        dest = "dynamic_pk",
        required = True,
        help = "PK of the Dynamic to retrieve from Database (mandatory)")
    parser.add_argument('-q',
        dest = "queue",
        help = "Queue system to use (slurm, pbs, pbs_ib and svgd supported)",
        default = clustersettings.QUEUE)
    parser.add_argument('--queue_pk',
        dest = "queue_pk",
        help = "Provide a queue pk to interface with a db",
        default = None)
    parser.add_argument('--debug',
        action="store_true")
    args = parser.parse_args()

    if args.queue_pk:
        queue_task = QueueTask.objects.get(pk = args.queue_pk)
        update_queue(queue_task, "Running", "started")

    run = Run(dynamic_pk = args.dynamic_pk,
        repo_dir = args.repo_dir,
        queue = args.queue,
        broker_pk = args.queue_pk,
        debug = args.debug)
    #run.clean()

    #Delete old GROMACS.log if this is a re-run
    f = open("GROMACS.log", "w")
    f.close()

    if args.debug:
        logging.basicConfig(filename='GROMACS.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='GROMACS.log',
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S',
            level=logging.DEBUG)
    #
    try:
        run.moldyn()
        if args.queue_pk:
            update_queue(queue_task, "Finished", "ended")
        run.set_file_path()
        run.send_email()
    except:
        if args.queue_pk:
            update_queue(queue_task, "Failed", "ended")
        run.send_email()
        raise

#!/usr/bin/env python2.7
import argparse
import datetime
import logging
import os
import shutil
import sys
import textwrap

import complex
import gromacs
import membrane
import protein
import queue
import recipes
import settings

class Run(object):
    def __init__(self, pdb, *args, **kwargs):
        '''
        A molecular dynamics "Run()"  MUST be given a "pdb"
        
        This class tries to initialize a full complex to send to simulation. Given
        a set of molecules (protein, ligand, other ligand, waters, ...), 
        this class would try to build a full embedded-in-membrane complex.

        The complex is stored in self.g (a "Gromacs" object), and thus
        can be 'runned' through g.recipe and g.run_recipe procedure. See
        gromacs.py for more information.

        The queueing system is also created here to be used in certain steps.'''

        self.pdb = pdb
        self.own_dir = kwargs.get("own_dir") or ""
        self.repo_dir = kwargs.get("repo_dir") or ""
        self.ligand = kwargs.get("ligand") or ""
        self.alosteric = kwargs.get("alosteric") or ""
        self.waters = kwargs.get("waters") or ""
        self.ions = kwargs.get("ions") or ""
        self.cho = kwargs.get("cho") or ""
        self.queue = kwargs.get("queue") or ""
        self.debug = kwargs.get("debug") or False

        if self.pdb:
            self.pdb = protein.Protein(pdb = self.pdb).check_number_of_chains()

        sugars = {"ligand": "Ligand",
            "alosteric": "Alosteric",
            "waters": "CrystalWaters",
            "ions": "Ions",
            "cho": "Cholesterol"}

        for sugar_type, class_name in sugars.iteritems():
            if getattr(self, sugar_type):
                base_name = getattr(self, sugar_type)
                setattr(self,
                    sugar_type,
                    getattr(protein, class_name)(
                        pdb = base_name + ".pdb",
                        itp = base_name + ".itp",
                        ff = base_name + ".ff"))
        
        self.membr = membrane.Membrane()

        prot_complex = protein.ProteinComplex(
            monomer = self.pdb,
            ligand = self.ligand or None,
            alosteric = self.alosteric or None,
            waters = self.waters or None,
            ions = self.ions or None,
            cho = self.cho or None)
        full_complex = complex.MembraneComplex()
        if self.pdb.__class__.__name__ == "Dimer":
            '''The box for the dimers is slightly bigger'''
            full_complex.box_height = 3.5
            full_complex.box_width = 1.2
        full_complex.complex = prot_complex
        full_complex.membrane = self.membr

        self.g = gromacs.Gromacs(membrane_complex = full_complex)

        # NOTE: If it's not provided in command line, self.queue is set in
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

    def moldyn(self):
        '''Runs all the dynamics'''

        steps = ["Init", "Minimization", "Equilibration", "Relax", "CARelax",
            "CollectResults"]

        for step in steps:
            self.g.select_recipe(stage = step, debug = self.debug)
            self.g.run_recipe(debug = self.debug)

    def light_moldyn(self):
        '''This is a function to debug a run in steps'''
#        steps = ["Init", "Minimization", "Equilibration", "Relax", "CARelax"]
        steps = ["Equilibration","Relax"]        
#        steps = ["CollectResults"]
        for step in steps:
            self.g.select_recipe(stage = step, debug = self.debug)
            self.g.run_recipe(debug = self.debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent('''\
    == Setup Molecular Dynamics for Membrane Proteins given a PDB. ==
    '''))

    parser.add_argument('-b',
        dest = "own_dir",
        help = "Working dir if different from actual dir",
        default = os.getcwd())
    parser.add_argument('-r',
        dest = "repo_dir",
        help = "Path to templates of fixed files. If not \
            provided, take the value from settings.REPO_DIR.",
        default = settings.REPO_DIR)
    parser.add_argument('-p',
        dest = "pdb",
        required = True,
        help = "Name of the pdb to insert into MD (mandatory)")
    parser.add_argument('--lig',
        dest = "ligand",
        help = "Name of the ligand, without extension. Three files must be \
            present along with the molecule pdb: the ligand, its itp and \
            its force field.")
    parser.add_argument("--alo",
        dest = "alosteric",
        help = "Name of the alosteric interaction, without extension. Three \
            files must be present along with the molecule pdb: the alosteric, \
            its itp and its force field.")
    parser.add_argument('--waters',
        dest="waters",
        help = "Crystalized water molecules. File name without extension.")
    parser.add_argument('--ions',
        dest="ions",
        help = "Crystalized ions file name without extension.")
    parser.add_argument('--cho',
        dest="cho",
        help = "Crystalized cholesterol molecules file name\
            without extension.")
    parser.add_argument('-q',
        dest = "queue",
        help = "Queueing system to use (slurm, pbs, pbs_ib and svgd supported)",
        default = settings.QUEUE)
    parser.add_argument('--debug',
        action="store_true")
#    parser.add_argument('--clean',
#                        )
    
    args = parser.parse_args()

    if not (os.path.isdir(args.own_dir)):
        os.makedirs(args.own_dir)
        print "Created working dir {0}".format(args.own_dir)
    os.chdir(args.own_dir)

    run = Run(own_dir = args.own_dir,
        repo_dir = args.repo_dir,
        pdb = args.pdb,
        ligand = args.ligand,
        alosteric = args.alosteric,
        waters = args.waters,
        ions = args.ions,
        cho = args.cho,
        queue = args.queue,
        debug = args.debug)
    run.clean()

    #Delete old GROMACS.log if this is a re-run
    f = open("GROMACS.log", "w")
    f.close()

    if args.debug:
        logging.basicConfig(filename='GROMACS_debug.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='GROMACS.log',
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S',
            level=logging.DEBUG)
    #
    run.moldyn()
#    run.light_moldyn()

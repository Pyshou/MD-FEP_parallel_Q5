import os
import settings

class Queue(object):
    def __init__(self, *args, **kwargs):
        #Default number of processors to be used
        self.num_proc = getattr(settings, "QUEUE_NUM_PROCS") or 8
        self.max_time = getattr(settings, "QUEUE_MAX_TIME") or "50:00:00"
        self.sh = "./mdrun.sh"

    def set_mdrun(self, value):
        '''Set the md_run command'''
        self._mdrun = value
    def get_mdrun(self):
        return self._mdrun
    mdrun = property(get_mdrun, set_mdrun)

class NoQueue(Queue):
    '''Dummy queue when no queue is selected'''
    def __init__(self, *args, **kwargs):
        super(NoQueue, self).__init__(self, *args, **kwargs)
        self.command = [self.sh]

        self._mdrun = os.path.join(settings.GROMACS_PATH, "mdrun")

    def make_script(self, workdir, options):
        '''binary is the executable
        options is a list with all the options'''
        sh = open(self.sh, "w")
        sh.write("#!/bin/bash\n")
        sh.write("cd %s\n" % workdir)
        sh.write("%s %s\n" % (self.mdrun, " ".join(options)))
        sh.close()
        os.chmod(self.sh, 0755)

        return True

class Slurm(Queue):
    def __init__(self, *args, **kwargs):
        super(Slurm, self).__init__(self, *args, **kwargs)
        self.command = ["srun",
#            "-n", str(self.num_proc),
            "-c", str(self.num_proc),
            "-t", self.max_time,
            self.sh]

#        self._mdrun = os.path.join(settings.GROMACS_PATH, "mdrun_slurm") #FOR CUELEBRE
        self._mdrun = os.path.join(settings.GROMACS_PATH, "mdrun") # FOR CSB

    def make_script(self, workdir, options):
        '''binary is the executable
        options is a list with all the options'''
        sh = open(self.sh, "w")
        sh.write("#!/bin/bash\n")
#        sh.write("source /home/apps/gromacs-4.6.5/bin/GMXRC\n")
#        sh.write("source /home/apps/bin/apps.sh\n")
#        sh.write("module load openmpi-x86_64\n")
        sh.write("cd %s\n" % workdir)
        sh.write("%s -ntmpi 16 -ntomp 1  %s -v&> mdrun.log\n" % (self.mdrun, " ".join(options)))
        sh.close()
        os.chmod(self.sh, 0755)

        return True

class PBS(Queue):
    '''Queue for the PBS system'''
    def __init__(self, *args, **kwargs):
        super(PBS, self).__init__(self, *args, **kwargs)
        '''Setting the command to run mdrun in pbs queue with mpi'''
        # These values are here for reference, doesn't do NOTHING      #
        # Calling file run.sh should resemble this lines               #
        self.num_nodes = 5                                             #
        self.proc_per_node = 8                                         #
        self.max_time = getattr(settings, "QUEUE_MAX_TIME") or "36:00:00"#
        self.max_cpu_time = "1440:00:00"                               #
        self.max_mem = "12gb"                                          #
        self.command = ["qsub",                                        #
            "-nodes=%d:ppn=%d" % (self.num_nodes, self.proc_per_node), #
            "-walltime=%s" % self.max_time,                            #
            "-cput=%s" % self.max_cpu_time,                            #
            "-mem=%s" % self.max_mem,                                  #
            self.sh]                                                   #
                                                                       #
        # XXX ##########################################################

        self._mdrun=os.path.join(settings.GROMACS_PATH, "mdrun_mpi")
        self.command = [self.sh]

    def make_script(self, workdir, options):
        '''PBS must load some modules in each node by shell scripts
        options is a list with all the options'''
        sh = open(self.sh, "w")
        sh.write("#!/bin/bash\n")
        sh.write("cd %s\n" % os.path.join(os.getcwd(), workdir))
        sh.write("module load gromacs/4.0.5-gige\n")
        sh.write("mpirun %s %s -v &>mdrun.log\n" \
            % (self.mdrun, " ".join(options)))
        sh.close()
        os.chmod(self.sh, 0755)

        return True

class PBS_IB(Queue):
    def __init__(self, *args, **kwargs):
        super(PBS, self).__init__(self, *args, **kwargs)
        # USELESS, see class PBS for explanation                            #
        self.num_nodes = 10                                                 #
        self.proc_per_node = 4                                              #
        self.max_time = getattr(settings, "QUEUE_MAX_TIME") or "08:00:00"   #
        self.max_cpu_time = "320:00:00"                                     #
        self.max_mem = "12gb"                                               #
                                                                            #
        self.command = [                                                    #
            "qsub",                                                         #
            "-l nodes=%d:ppn=%d:ib" % (self.num_nodes, self.proc_per_node), #
            "-l walltime=%s" % self.max_time,                               #
            "-l cput=%s" % self.max_cpu_time,                               #
            "-l mem=%s" % self.max_mem,                                     #
            self.sh]                                                        #
        #####################################################################

        self._mdrun=os.path.join(settings.GROMACS_PATH, "mdrun_mpi")
        self.command = [self.sh]

    def make_script(self, workdir, options):
        '''PBS must load some modules in each node by shell scripts
        options is a list with all the options'''
        sh = open(self.sh, "w")
        sh.write("#!/bin/bash\n")
        sh.write("cd %s\n" % os.path.join(os.getcwd(), workdir))
        sh.write("module load gromacs\n")
        sh.write("mpirun %s %s -v &>mdrun.log\n" \
            % (self.mdrun, " ".join(options)))
        sh.close()
        os.chmod(self.sh, 0755)

        return True

class Svgd(Queue):
    '''Queue for the PBS system at svgd.cesga.es'''
    def __init__(self, *args, **kwargs):
        super(Svgd, self).__init__(self, *args, **kwargs)
        '''Setting the command to run mdrun in pbs queue with mpi'''
        self._mdrun=os.path.join(settings.GROMACS_PATH, "mdrun")
        self.command = [self.sh]

    def make_script(self, workdir, options):
        '''PBS must load some modules in each node by shell scripts
        options is a list with all the options'''
        sh = open(self.sh, "w")
        sh.write("#!/bin/bash\n")
        sh.write("cd %s\n" % os.path.join(os.getcwd(), workdir))
        # Somehow impi is loaded, and conflicts with the (see down) tricky way
        # of SVGD of dealing with parallel runnings of mdrun through mpich2
        sh.write("module unload impi\n")
        sh.write("module load mpich2\n")
        sh.write("module load gromacs/4.0.7\n")
        # CESGA SVGD has its own tweaks. The mdrun binary "jumps" to mpiexec,
        # and call back mdrun with as much nslots (~cores) as reserved in the
        # command line calling the whole pipeline, this way:
        #  qsub -l num_proc=1,s_rt=01:00:00,s_vmem=1G,h_fsize=1G,arch=amd \
        #    -pe mpi 4 run.sh
        # That "-pe mpi 4" tells the queue system to allocate 4 cores to run.sh
        # and it's responsability of run.sh (aka the next line) to pass $NSLOTS
        # Note that this SVGD uses THE SAME queue system than PBS and PBS_IB,
        # but lacks of mpirun executable. Always a pleasure to adjust a queue.
        sh.write("%s -np $NSLOTS %s -v &>mdrun.log\n" \
            % (self.mdrun, " ".join(options)))
        sh.close()
        os.chmod(self.sh, 0755)

        return True

class Other(Queue):
    def __init__(self):
        pass

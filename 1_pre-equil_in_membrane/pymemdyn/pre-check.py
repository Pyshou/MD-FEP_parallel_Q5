import os
import queue
import settings

def gromacs_check():
    '''Verify the gromacs paths'''
    if not os.path.isdir(settings.GROMACS_PATH):
        print "Invalid GROMACS_PATH: '%s'" % settings.GROMACS_PATH
        return False

    return True

def queue_check():
    '''Verify the usability of the queue'''
    queues = {"": "NoQueue",
              "slurm": "Slurm",
              "pbs": "PBS",
              "pbs_ib": "PBS_IB",
              "svgd": "Svgd"}

    if settings.QUEUE in queues.keys():
        if hasattr(queue, queues[settings.QUEUE]):
            #Get the binary path from the queue
            mdrun = getattr(queue, queues[settings.QUEUE])().mdrun
            #And check if it exists
            if not os.path.isfile(mdrun_mpi):
                print "Queue doesn't match with Gromacs path: '%s'" % mdrun
                return False
        else:
            print "Bad defined queue: '%s'" % settings.QUEUE
            return False
    else:
        print "Bad defined queue: '%s'" % settings.QUEUE
        return False

    return True

def repo_dir():
    '''Verify the validity of the repo dir defined'''

    repo_files = ["eqCA.mdp", "ffoplsaa_mod.itp", "popc.itp", "topol.top",
        "eqDEBUG.mdp", "ffoplsaanb_base.itp", "prod.mdp", "x4bilayer.pdb",
        "eq.mdp", "ffoplsaanb_cho.itp", "steepDEBUG.mdp",
        "ffoplsaabon_mod.itp", "ffoplsaanb_lip.itp", "steep.mdp"]

    if not os.path.isdir(settings.REPO_DIR):
        print "Invalid REPO_DIR: '%s'" % settings.REPO_DIR
        return False

    current_files = os.listdir(settings.REPO_DIR)
    for f in repo_files:
        if f not in current_files:
            print "'%s' expected to be in %s" % (f, settings.REPO_DIR)
            return False

    return True

if __name__ == "__main__":
    if repo_dir() and gromacs_check() and queue_check():
        print 'All checks passed OK!'

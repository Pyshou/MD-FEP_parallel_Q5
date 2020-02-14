#import pymoldyn
import os

#SCRIPT_DIR = os.path.dirname(os.path.realpath(pymoldyn.__file__))

# This is the dir where pymoldyn git repo has been deployed,
# or to be more specific, this file settings.py is located
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

#This dir now has to be the absolute path to the source of templates
# You can refer it relatively like this:
REPO_DIR = os.path.join(ROOT_DIR, "templates")
# Or absolutely like this:
# REPO_DIR = "/path/to/your/templates"
# But this WILL FAIL: * REPO_DIR = "templates" *


# Choose a path to the gromacs binaries.
#GROMACS_PATH = "/opt/applications/gromacs/4.0.5/gnu/ib/bin/"
#GROMACS_PATH = "/opt/applications/gromacs/4.0.5/gnu/gige/bin/"
#GROMACS_PATH = "/opt/cesga/gromacs-4.0.7/bin/"
#GROMACS_PATH = "/opt/gromacs405/bin/"                               #cuelebre.inv.usc.es
#GROMACS_PATH = "/home/apps/gromacs-4.6.5/bin/"                      #csb.bmc.uu.se
GROMACS_PATH = "/software/apps/gromacs/4.6.3/g472/bin/"             #Triolith
#GROMACS_PATH = "/sw/bin/"                                           #Standalone in Mac Fink
#GROMACS_PATH = "/Users/esguerra/software/gromacs-4.6.5/bin/"        #Standalone in Mac
#GROMACS_PATH = "/c3se/apps/Glenn/gromacs/4.6.3-p20130821-gcc48/bin" #Glenn at Chalmers
#GROMACS_PATH = "/sw/apps/gromacs/4.6.3/tintin/bin"                  #Tintin
#GROMACS_PATH = "/lap/gromacs/4.6.5/bin"                             #Abisko

# Choose which queuing system to use. Look inside queue.py.
QUEUE = ""
#QUEUE = "slurm"
#QUEUE = "pbs"
#QUEUE = "pbs_ib"
#QUEUE = "svgd"


# Choose how many tasks
QUEUE_NUM_TASK = 16

# Choose how many nodes to use in parallel
QUEUE_NUM_NODES = 1

# Choose how many processor to use in parallel
QUEUE_NUM_PROCS = 16

#Choose the project number
PROJECT_NUM="snic2014-11-37"

# Choose the maximum alloted time for your run.
QUEUE_MAX_TIME = "47:59:00"


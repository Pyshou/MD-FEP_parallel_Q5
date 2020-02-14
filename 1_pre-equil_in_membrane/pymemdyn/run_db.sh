#!/bin/bash
source /home/apps/gromacs-4.6.5/bin/GMXRC.bash
source /home/apps/bin/apps.sh
/home/gpcruser/gpcr_modsim/pymemdyn/run_db.py $*


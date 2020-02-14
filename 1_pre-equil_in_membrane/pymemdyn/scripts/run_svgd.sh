#!/bin/bash
#
# This is a helper/wrapper script to use with the SVGD queues
# 
# Edit as needed
#
module load python/2.7.3
module load gromacs/4.0.7
python run.py -p a2a.pdb --debug 

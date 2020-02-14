#!/bin/bash
#
# This is a helper/wrapper script to use with the PBS queues, that doesn't 
# admit the pass of commands to the childs (or I don't figure how to pass'em)
# 
# Edit as needed
#
#PBS -l nodes=5:ppn=8
#PBS -l walltime=36:00:00
#PBS -l cput=1440:00:00
#PBS -l mem=12gb

cd $PBS_O_WORKDIR
python run.py -p a2a.pdb --debug

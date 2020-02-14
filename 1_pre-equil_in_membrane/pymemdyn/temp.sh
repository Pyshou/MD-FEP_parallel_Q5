#!/bin/bash -l
module load gromacs/4.6.3
module load python/2.7.6
~/software/pymemdyn/pymemdyn -p rec_aligned.pdb -q slurm


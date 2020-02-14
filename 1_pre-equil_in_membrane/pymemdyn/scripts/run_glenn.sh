#!/bin/bash
echo "#!/bin/bash -l
module load python/py27/2.7.6
module load gcc/4.8/4.8.1
module load intel-mpi/4.1.1.036
module load gromacs/4.6.3-gcc48
run.py -p a2b_filter.pdb
" > temp.sh
chmod +x temp.sh
sbatch -A snic2013-26-1 --exclusive -t 48:00:00 -J pymemdyn temp.sh

#!/bin/bash
echo "#!/bin/bash -l
module load gromacs/4.6.5
#module load python/2.7.6
run.py -p a2b_filter.pdb
" > temp.sh
chmod +x temp.sh
sbatch -A snic2013-26-1 --exclusive -n 16 -t 48:00:00 -J pymemdyn temp.sh

#!/bin/bash
echo "#!/bin/bash -l
module load gromacs/4.6.3
module load python/2.7.6
pymemdyn -p a2a_ag.pdb
" > temp.sh
chmod +x temp.sh
sbatch -A snic2014-1-262 -n 32 --exclusive -t 20:00:00 -J pymemdyn temp.sh

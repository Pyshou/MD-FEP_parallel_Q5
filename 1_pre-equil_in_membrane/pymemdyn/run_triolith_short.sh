#!/bin/bash
echo "#!/bin/bash
module load gromacs/4.6.3
module load python/2.7.6
~/software/pymemdyn/pymemdyn -p rec_aligned.pdb -q slurm
" > temp.sh
chmod +x temp.sh
sbatch -A snic2017-12-43 -n 1 --reservation=devel --exclusive -t 00:00:30 -J pymemdyn temp.sh

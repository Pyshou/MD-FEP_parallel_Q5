#!/bin/bash
echo "#!/bin/bash -l
source /home/apps/gromacs-4.6.5/bin/GMXRC.bash
source /home/apps/bin/apps.sh
pymemdyn -p a2a_ag.pdb --lig lig  --cho cho
" > temp.sh
chmod +x temp.sh
sbatch -c 8 -t 47:59:00 -J pymemdyn temp.sh

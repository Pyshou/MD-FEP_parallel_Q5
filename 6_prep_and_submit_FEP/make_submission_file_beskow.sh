#!/bin/bash # Generation submission scripts to run mutliple Q job on beskow 
#Change Qdyn path
# /!\ Executable has to be on /cfs partition (scratch) as /afs is not accessible from nodes
qdyn_exec=/cfs/klemming/nobackup/p/pierrema/software/Q5_Mauricio/bin/qdyn5_r8

#Determine of many core and node we need (32 cores/node)
core_by_node=32 #Modify according to your cluster configuration
njob=$(wc -l dirlist | cut -d " " -f 1)
nbnode=$(perl -w -e "use POSIX; print ceil($njob/$core_by_node), qq{\n}")

walltime="23:59:59"
if [ $(basename $PWD) == 'WAT' ]; then
    walltime="09:59:59"
fi

#Create scripts launching FEP calculations
cat <<EOF > run_fep.sh
#!/bin/bash

function RUN_Q (){
wdir=\$1
echo Run Q5 in directory \$wdir

cd \$wdir

export qdyn=$qdyn_exec
dc=\$(basename \$wdir)

# Data production, 1 core for each job
\$qdyn eq0.inp > eq0.log
\$qdyn eq1.inp > eq1.log
\$qdyn eq2.inp > eq2.log
\$qdyn eq3.inp > eq3.log
\$qdyn eq4.inp matricon@csb.bmc.uu.se:> eq4.log
\$qdyn eq5.inp > eq5.log
\$qdyn eq6.inp > eq6.log
# Data production, 1 core for each job
\$qdyn \$dc.inp > \$dc.log

}

export -f RUN_Q

#Read the smile list and run q in parallel
dirlist=\$1
cat \$dirlist | xargs -n 1 -I {} -P $core_by_node bash -c 'RUN_Q "{}"' 
EOF

#Make script executable
chmod 774 run_fep.sh

#Create sumission script for SLURM
cat <<EOF > run_fep.com
#!/bin/bash
#SBATCH -A 2019-2-16
#SBATCH -J FEP_LIG
#SBATCH -C Haswell
#SBATCH --ntasks $core_by_node
#SBATCH --nodes 1 
#SBATCH -t $walltime

#Must be divided by two as SLURM takes hyperthreading into account
cpu=\$(bc <<< "\$SLURM_CPUS_ON_NODE/2")

#Run script mastering FEP calculation
i=\$(printf "%02d\n" \$SLURM_ARRAY_TASK_ID) 
#aprun -n 1 -d \$cpu -cc none ./run_fep.sh dirlist\$i
srun --ntasks=1 ./run_fep.sh dirlist\$i
EOF

#Split dirlist in smaller files and submit array
split -a 2 -d -l $core_by_node dirlist dirlist
lastid=$(bc <<< "$nbnode-1")
sbatch --array=0-$lastid run_fep.com

#!/bin/sh
#SBATCH -N 1
#SBATCH -t 23:59:59
#SBATCH -J Gaussian
#SBATCH --exclusive
#SBATCH -A snic2018-2-22

job=LIG
WRKDIR=$(pwd)

#Trap SIGTERM and copy the chk file if the job hits the walltime limit 
trap 'if [ -f ${job}.chk ]; then cp ${job}.chk ${WRKDIR}; else echo "No named chk file"; fi; echo "SIGTERM was traped"' SIGTERM

#Load the relevant Gaussian module
module load Gaussian/16.B.01-avx2-nsc1-bdist

cd $GAUSS_SCRDIR

if [ -f ${WRKDIR}/${job}.chk ]
then
    cp ${WRKDIR}/${job}.chk .
fi

(time g16 < ${WRKDIR}/${job}.com) > ${WRKDIR}/${job}.out &
wait

g_exit_status=$?

if [ -f ${job}.chk ]
then
    cp ${job}.chk ${WRKDIR}
fi

exit $g_exit_status
#END OF SCRIPT


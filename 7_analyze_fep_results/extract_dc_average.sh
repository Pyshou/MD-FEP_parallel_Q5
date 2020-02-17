#!/bin/bash
# By Pierre Matricon, 2015


# Variables to change

ff_folder=$2
qprep_path='/home/matricon/software/Q5_Mauricio/bin/qprep5'

if [ ! -d $ff_folder ]; then
        echo "WARNING: $ff_folder does not exist. Please, change ff_folder at the beginning of the script if you want to generate a topology !"
        exit
fi

if [ ! -f $qprep_path ]; then
        echo "WARNING: $qprep_path does not exist. Please, change qprep_path at the beginning of the script (Qprep location) !"
        exit
fi


# Input

if [ $# -eq 0 ]; then
	echo "ERROR: You need to provide what you want to extract (i.e. dc1) as an argument. Also make sure that you are in an md_rsx folder !"
	exit
else
	if [ $# -ge 3 ]; then
		echo "ERROR: Too many arguments ! You only need to provide what you want to extract (i.e. dc1) as an argument. Also make sure that you are in an md_rsx folder !"
		exit
	else
		if [ ! -d $1 ]; then
			echo "ERROR: $1 is not a folder. Are you in an md_rsx folder or do you have the restart file $1.re in the $1 folder ?"
			exit
		fi
	fi
fi

if [ ! -f $1"/"$1".re" ]; then
        echo "WARNING: $1/$1.re does not exist"
        exit
fi


# Writting Qprep input file

echo "rl "$ff_folder"Forcefield/Qoplsaa.lib" > ".get_"$1"_av.in"
echo "rl "$ff_folder"Forcefield/popc_hugo.lib" >> ".get_"$1"_av.in"
echo "rl "$ff_folder"Forcefield/WAS.lib" >> ".get_"$1"_av.in"
echo "rl "$ff_folder"Forcefield/LIG.lib" >> ".get_"$1"_av.in"
echo "rt "$1"/topology.top" >> ".get_"$1"_av.in"
echo "mask none" >> ".get_"$1"_av.in"
echo "mask not excluded" >> ".get_"$1"_av.in"
echo "av" >> ".get_"$1"_av.in"
echo $1"/"$1.dcd >> ".get_"$1"_av.in"
echo "y" >> ".get_"$1"_av.in"
echo "n" >> ".get_"$1"_av.in"
echo $1"_av.pdb" >> ".get_"$1"_av.in"
echo "y" >> ".get_"$1"_av.in"
echo "q" >> ".get_"$1"_av.in"

# Running Qprep and writting output file

$qprep_path < ".get_"$1"_av.in" > ".get_"$1"_av.log"

echo "
Done, check "$1"_av.pdb or .get_"$1"_av.log !"
echo "PS: Do not care about Fortran, it just worked ! If you are not convinced, you can do it again by typing the content of .get_"$1"_av.in on your own using Qprep5, and compare the files with the diff command (there is no bug this way) ;-)"

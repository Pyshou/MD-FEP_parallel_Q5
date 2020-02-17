#!/bin/bash
# By Pierre Matricon, 2015


# ff_forlder to change and checking if folder exists

ff_folder=$2
qprep_path='/home/matricon/software/Q5_Mauricio/bin/qprep5'

if [ ! -f $1/eq6.re ]; then
        echo "WARNING: $1/eq6.re does not exist. Is your last (6th) equilibration step finished in your $1 folder ?" 
        exit
fi

if [ ! -d $ff_folder ]; then
        echo "WARNING: $ff_folder does not exist. Please, change ff_folder at the beginning of the script if you want to generate a topology !"
        exit
fi

if [ ! -f $qprep_path ]; then
        echo "WARNING: $qprep_path does not exist. Please, change qprep_path at the beginning of the script (Qprep location) !"
        exit
fi


# Writting Qprep input file

echo "rl "$ff_folder"Forcefield/Qoplsaa.lib" > .get_eq6.in
echo "rl "$ff_folder"Forcefield/popc_hugo.lib" >> .get_eq6.in
echo "rl "$ff_folder"Forcefield/LIG.lib" >> .get_eq6.in
echo "rt $ff_folder/topology.top" >> .get_eq6.in
echo "mask none" >> .get_eq6.in
echo "mask not excluded" >> .get_eq6.in
echo "rx $1/eq6.re" >> .get_eq6.in
echo "wp "$1"_eq6.pdb n" >> .get_eq6.in
echo "quit" >> .get_eq6.in


# Running Qprep and writting output file

$qprep_path < .get_eq6.in > .get_eq6.log

echo "Done, check eq6.pdb or .get_eq6.log !"

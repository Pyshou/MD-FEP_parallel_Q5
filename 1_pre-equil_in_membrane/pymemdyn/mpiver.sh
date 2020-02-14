#!/bin/bash
# Sorry about this patchy way of getting thing done.
# This should later disappear and a new section, probably in settings.py
# be added to define as variables all of the executables in the gromacs
# binaries folder so it's easier to modify them when a new cluster facility
# decides to change to non-standard gromacs names.
# NOTICE that these are not the only changes in recipes.py. Others like
# make_ndx also have to be changed to make_ndx_mpi. In addition to this
# settings.py, gromacs.py, and queue.py also need to be changed.
# Mauricio Esguerra: April 24, 2015
cp recipes.py recipesmpi.py
sed -i '' 's/"gromacs": "pdb2gmx"/"gromacs": "pdb2gmx_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "editconf"/"gromacs": "editconf_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "grompp"/"gromacs": "grompp_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "trjconv"/"gromacs": "trjconv_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "make_ndx"/"gromacs": "make_ndx_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "genrestr"/"gromacs": "genrestr_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "g_energy"/"gromacs": "g_energy_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "eneconv"/"gromacs": "eneconv_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "genbox"/"gromacs": "genbox_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "genion"/"gromacs": "genion_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "g_rms"/"gromacs": "g_rms_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "trjcat"/"gromacs": "trjcat_mpi"/g' recipesmpi.py
sed -i '' 's/"gromacs": "mdrun"/"gromacs": "mdrun_mpi"/g' recipesmpi.py







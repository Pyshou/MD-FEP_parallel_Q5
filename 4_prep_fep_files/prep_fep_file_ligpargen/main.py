#! /usr/bin/env python
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2017


import sys, re, os, json
import prep_fep_files as pf

### Running the program ###

data=pf.parse_args() # Parsing arguments once
lig1_lib=data[0]
lig2_lib=data[1]
mapping=json.loads(str(data[2].readlines()[0])[:-1])

if os.path.exists('lig_step0.fep')==True or os.path.exists('lig_step1_1.fep')\
==True: # Ensuring new file
	os.system('rm lig_step*.fep')

# Editing lig_step0.fep and detecting if using softcore
fep_data=pf.get_lig_param_diffs(lig1_lib, lig2_lib, mapping)
softcore_on=fep_data[0]
atom_nb=fep_data[1] 
charges_state2=fep_data[2]
atom_types2=fep_data[3]

# Editing lig_step1_1.fep
lig1_prm=data[3]
pf.edit_step1_1(lig1_prm, softcore_on, atom_nb, charges_state2, atom_types2)

print "Alirght! Check generated .fep files, update softcore and atoms in \
step1_2 and use compare_bonffparams_Qoplsaa.py to check for bonded changes"

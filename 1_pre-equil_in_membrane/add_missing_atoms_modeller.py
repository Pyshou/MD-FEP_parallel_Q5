#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2016


# Checking arguments


import sys, os

if len(sys.argv) == 2: # If one argument
	if str(sys.argv[1]) == "-h" : # Help
		sys.exit("Usage : ./add_missing_atoms_modeller.py <input.pdb>\noptions:\n-h : Usage")
	elif os.path.exists(sys.argv[1]):
		if ".pdb" in str(sys.argv[1]):
			input_PDB=str(sys.argv[1])
		else:
			sys.exit("ERROR: I do not see a '.pdb' in your file. Make sure there is! Use the [-h] option for help!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" does not exist!")
else:
	sys.exit("ERROR: You need to provide an input PDB file! Use the [-h] option for help!")


# Running the program


from modeller import *              # Load standard Modeller classes
from modeller.scripts import complete_pdb
from modeller.optimizers import conjugate_gradients

log.verbose()
env = environ()
env.io.atom_files_directory = ['.']
env.libs.topology.read('$(LIB)/top_heav.lib')
env.libs.parameters.read('$(LIB)/par.lib')

mdl = complete_pdb(env, input_PDB, transfer_res_num=True)
rsr = mdl.restraints


allat = selection(mdl) #Atom selection
cg = conjugate_gradients()
cg.optimize(allat, max_iterations=100, output='REPORT')
mdl.write(file=str(input_PDB)[:-4]+"_full.pdb")

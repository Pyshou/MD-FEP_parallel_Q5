#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015


# Parameters

output = "rec_noH.pdb"

# Importing necessary modules


import sys, os


# Defining and checking options and arguments


if len(sys.argv) == 2: # If 1 argument
	if str(sys.argv[1]) == "-h" : # Help
		sys.exit("\nUsage : make_sphere.py <input_file>>\n\nOptions:\n-h : Usage\n")
	else:
		if not ".pdb" in str(sys.argv[1]):
			sys.exit("ERROR: Your first argument has to be a PDB file")
		else:
			if os.path.exists(str(sys.argv[1])):
				fin=open(str(sys.argv[1]), 'r')
			else: 
				 sys.exit("ERROR: "+str(sys.argv[1])+", No such file")
else:
	sys.exit('ERROR: You should specifiy an input PDB file')



# Defining useful functions


def writing_output():
	fout  = open(str(output), 'w') # Output file
	for line in fin.readlines():
		if ('ATOM' or 'HETATM') in line:
			if str(line[13]) != 'H':
				fout.write(line)
		elif ('GAP' or 'TER') in line:
			fout.write('GAP\n')
	fout.close()
	return 0


# Running the program

writing_output()

print "\nAlright, check "+str(output)

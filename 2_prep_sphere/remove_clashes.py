#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015


# Sets the environment and parameters

import math, os, sys

def distance(x1,x2,y1,y2,z1,z2):
	dist = float(math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
	return dist

treshold = 2.5  # Default distance between atom centers to consider then as clashes


# Defining and checking options and arguments


confirmation = 1

if len(sys.argv) < 3 and "-h" not in sys.argv: # If missing arguments
        sys.exit("ERROR: You need to specify at least the residue name you suspect to make clashes (default treshold = 2.5 A), plus the path to your PDB file ! use the [-h] option for help.")
elif "-h" in sys.argv:
	sys.exit("Usage : remove_clashes.py [resname] <option> [PDB file]\n-s [resname2] : if you want to remove clashes with a specific residue\n-t [distance treshold in angstroms for clashes]\n-h : Usage")
elif len(sys.argv) == 3 or len(sys.argv) == 5 or len(sys.argv) == 7 : # If more arguments
        if len(str(sys.argv[1])) == 3:
		resn = str(sys.argv[1])
	else: # Wrong argument case
		sys.exit("ERROR: Wrong argument, you need to specify a residue you suspect to make clashes with others (by 3 its letters name in your PDB file), and also the PDB file to analyze! Use the [-h] option for help.")
	if len(sys.argv) == 5 or len(sys.argv) == 7: # -s or/and -t option used
		counter = 1
		for i in range(1, len(sys.argv)):
			if sys.argv[i] == "-s" and i < len(sys.argv)-2:
				if len(str(sys.argv[i+1])) == 3:
					resn2 = str(sys.argv[i+1])
					(counter, confirmation) = (0, 0)
				else:
					sys.exit("ERROR: The specific residue to analyse in terms of clashes with the suspected one should be a 3-letter residue name!")
			elif sys.argv[i] == "-t" and i < len(sys.argv)-2:
				treshold = float(sys.argv[i+1])
		if counter == 1:
			sys.exit("ERROR: You used an option without argument. Use the -h option for help.")
elif len(sys.argv) == 6 or len(sys.argv) == 4 or len(sys.argv) > 7: # Too many arguments
	sys.exit("ERROR: Too many arguments or option(s) provided without argument! Use the -h option for help.")
if ".pdb" in sys.argv[len(sys.argv)-1]:
	if os.path.exists(str(sys.argv[len(sys.argv)-1])):
		pdb_file = str(sys.argv[len(sys.argv)-1])
	else:
		sys.exit("ERROR: " + str(sys.argv[len(sys.argv)-1]) + " does not exist !")
else:
	sys.exit("ERROR: You did not specify a PDB file for analysis (no .pdb extension detected)! Use the [-h] option for help.")



# Defining useful functions


def get_coordinates(): # Reads and saves coordinates of interest
	filin = open(pdb_file, 'r')
	coordinates = {}
	resn_coordinates = {}
	(confirmer1, confirmer2, resname) = (1, 1, '0')
	for line in filin.readlines():
		if str(line[0:4]) == "ATOM" or str(line[0:6]) == "HETATM":
			atom_name = str(line[12:16])
			if str(line[17:20]) + str(int(line[22:26])) != resname: # If new residue
				(confirm1, confirm2, confirm3) = (1, 1, 1)
				resnb = str(int(line[22:26]))
				resname = str(line[17:20]) + resnb
			if resn in resname : # If target residue found
				if confirm1 == 1: # Initialise
					resn_coordinates[resname] = {}
					(confirm1, confirmer1) = (0, 0)
				resn_coordinates[resname][atom_name] = []
				resn_coordinates[resname][atom_name].append(float(line[30:38]))
				resn_coordinates[resname][atom_name].append(float(line[38:46]))
				resn_coordinates[resname][atom_name].append(float(line[46:54]))
				confirm = 0
			elif resn not in resname:
				if confirmation == 0:
					if resn2 in resname: # Target residue 2
						if confirm2 == 1:
							coordinates[resname] = {}
							(confirm2, confirmer2) = (0, 0)
						coordinates[resname][atom_name] = []
						coordinates[resname][atom_name].append(float(line[30:38]))
						coordinates[resname][atom_name].append(float(line[38:46]))
						coordinates[resname][atom_name].append(float(line[46:54]))
				elif confirmation == 1 and resn not in resname: # Other residues if no target residue 2 (no use of -s)
					if confirm3 == 1:
						coordinates[resname] = {}
						confirm3 = 0
					coordinates[resname][atom_name] = []
					coordinates[resname][atom_name].append(float(line[30:38]))
					coordinates[resname][atom_name].append(float(line[38:46]))
					coordinates[resname][atom_name].append(float(line[46:54]))
	filin.close()
	if confirmer1 == 1:
		sys.exit("ERROR: " + resn + " not found in PDB file!")
	elif confirmation == 0:
		if confirmer2 == 1:
			sys.exit("ERROR: " + resn2 + " not found in PDB file!")
	return coordinates, resn_coordinates



def compute_distances(): # Analyses which residues clash between target residue 1 and other residues (or target 2 if -s is used)
	toremove = []
	data = get_coordinates()
	coordinates = data[0]
	resn_coordinates = data[1]
	for key1 in resn_coordinates:
		for atom1 in resn_coordinates[key1]:
			for key2 in coordinates:
				for atom2 in coordinates[key2]:
					if key2 not in toremove:
						x1 = resn_coordinates[key1][atom1][0]
						x2 = coordinates[key2][atom2][0]
						y1 = resn_coordinates[key1][atom1][1]
						y2 = coordinates[key2][atom2][1]
						z1 = resn_coordinates[key1][atom1][2]
						z2 = coordinates[key2][atom2][2]	
#						if abs(x1-x2) < treshold:
#							if abs(y1-y2) < treshold:
#								if abs(z1-x2) < treshold:
						if distance(x1, x2, y1, y2, z1, z2) <= treshold:
							toremove.append(key2)
	return toremove


def write_new_structure(): # Writes a new PDB file without residues that clash with the specified one ("target 1")
	filin = open(pdb_file, 'r')
	filout = open(pdb_file[:-4] + "_noclash.pdb", 'w')
	toremove = compute_distances()

	resname = '0'
	for line in filin.readlines():
		if ("GAP" or "TER" or "END") in line:
			filout.write("GAP\n")
		elif str(line[0:4]) == "ATOM" or str(line[0:6]) == "HETATM":
			if str(line[17:20]) + str(int(line[22:26])) != resname: # If new residue
				resnb = str(int(line[22:26]))
				resname = str(line[17:20]) + resnb
			if resname not in toremove:
				filout.write(line[:54]+"\n")
	filin.close()
	filout.close()
	return 0 


# Running the script


write_new_structure()

print "Alright, check " + pdb_file[:-4] + "_noclash.pdb" + " !"

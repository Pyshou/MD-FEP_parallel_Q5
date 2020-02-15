#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2020


# Sets the environment and parameters

import math, os, re, sys

def distance(x1,x2,y1,y2,z1,z2):
	dist = float(math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
	return dist


# Defining and checking options and arguments


confirmation = 1

if len(sys.argv) < 4 and "-h" not in sys.argv: # If missing arguments
        sys.exit("ERROR: You need to specify a path to your PDB file, the atom name of your 'LIG' residue chosen as sphere center and a sphere radius in Angstroms! use the [-h] option for help.")
elif "-h" in sys.argv:
	sys.exit("Usage : remove_waters_outside_sphere.py [input_PDB] [LIGatom-name_sphere-center] [Sphere_radius(A)]\n-h : Usage")
elif len(sys.argv) == 4: # If three arguments
	if os.path.exists(sys.argv[1]):
		if str(sys.argv[1])[-4:]=='.pdb':
			fin=open(str(sys.argv[1]), 'r')
		else:
			sys.exit("ERROR: " + str(sys.argv[1]) +" is not a PDB file!")
	else:
		sys.exit("ERROR: " + str(sys.argv[1]) + " does not exist !")
	sphere_center=str(sys.argv[2])
	sphere_radius=float(sys.argv[3])
else:
	sys.exit("ERROR: You need to specify a path to your PDB file, the atom name of your 'LIG' residue chosen as sphere center and a sphere radius in Angstroms! Use the [-h] option for help.")



# Defining useful functions


def get_coordinates(): # Reads and saves coordinates of interest
	center_coordinates = []
	HOH_coordinates = {}
	for line in fin.readlines():
		if str(line[0:4]) == "ATOM" or str(line[0:6]) == "HETATM":
			atom_name = re.findall('[A-Z-0-9]+', str(line[12:16]))[0]
			resnb = str(int(line[22:26]))
			resname = str(line[17:20]) + resnb
			if str(line[17:20])=='LIG' and atom_name==sphere_center: # Sphere center found
				center_coordinates.append(float(line[30:38]))
				center_coordinates.append(float(line[38:46]))
				center_coordinates.append(float(line[46:54]))
			elif str(line[17:20])=='HOH': # Water residue found
				HOH_coordinates[resname] = {}
				HOH_coordinates[resname][atom_name] = []
				HOH_coordinates[resname][atom_name].append(float(line[30:38]))
				HOH_coordinates[resname][atom_name].append(float(line[38:46]))
				HOH_coordinates[resname][atom_name].append(float(line[46:54]))
	fin.seek(0)
	if len(center_coordinates)==0:
		fin.close()
		sys.exit('ERROR: Sphere center not found!')
	elif len(HOH_coordinates)==0:
		fin.close()
		sys.exit('ERROR: No HOH residue found. Check the formatting of your input PDB!!')
	return center_coordinates, HOH_coordinates



def compute_distances(): # Analyses which residues clash between target residue 1 and other residues (or target 2 if -s is used)
	toremove = []
	data = get_coordinates()
	center = data[0]
	HOH_coordinates = data[1]
	for key in HOH_coordinates:
		for atom in HOH_coordinates[key]:
			x1 = HOH_coordinates[key][atom][0]
			y1 = HOH_coordinates[key][atom][1]
			z1 = HOH_coordinates[key][atom][2]
			if distance(x1, center[0], y1, center[1], z1, center[2]) > sphere_radius-0.5:
				toremove.append(key)
	return toremove


def write_new_structure(): # Writes a new PDB file without residues that clash with the specified one ("target 1")
	fout = open(str(sys.argv[1])[:-4] + "_sphered.pdb", 'w')
	toremove = compute_distances()
	resname = '0'
	for line in fin.readlines():
		if ("GAP" or "TER" or "END") in line:
			fout.write("GAP\n")
		elif str(line[0:4]) == "ATOM" or str(line[0:6]) == "HETATM":
			resnb = str(int(line[22:26]))
			resname = str(line[17:20]) + resnb
			if resname not in toremove:
				fout.write(line[:54]+"\n")
	fin.close()
	fout.close()
	return 0 


# Running the script


write_new_structure()

print "Alright, check " + str(sys.argv[1])[:-4] + "_sphered.pdb" + " !"

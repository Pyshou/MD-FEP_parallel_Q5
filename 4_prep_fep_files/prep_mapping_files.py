#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2017


# Importing necessary modules ###

import sys, re, os, math


### Defining and checking options and arguments ###

def distance(x1,x2,y1,y2,z1,z2):
        dist = float(math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
        return dist


# Parsing arguments

if len(sys.argv)==2:# One argument
	if str(sys.argv[1])=="-h":
		sys.exit("\nUsage: ./prep_mapping_files.py <LIGA_top.pdb> <LIGB_top.pdb> <dist_treshold>\n")
	else:
		 sys.exit("ERROR: You need to provide the PDB topology files of ligands A and B as respective arguments, and a distance mapping treshold (in A) as third argument.")
elif len(sys.argv)<4:# Not enough arguments
	sys.exit("ERROR: You need to provide the PDB topology files of ligands A and B as respective arguments, and a distance mapping treshold (in A) as third argument.")
elif len(sys.argv)==4:# Three arguments
	if os.path.exists(sys.argv[1]):
		if os.path.exists(sys.argv[2]):
			if str(sys.argv[1])[-4:]==".pdb":
				if str(sys.argv[2])[-4:]==".pdb":
					pdbAin=open(str(sys.argv[1]), 'r')
					LIGAname=re.split("\.", re.split("/", str(sys.argv[1]))[-2])[-1]
					pdbBin=open(str(sys.argv[2]), 'r')
					LIGBname=re.split("\.", re.split("/", str(sys.argv[2]))[-2])[-1]
					treshold=float(sys.argv[3])
				else:
					sys.exit("ERROR: "+sys.argv[2]+" is no a PDB file according to the extension!")
			else:
				sys.exit("ERROR: "+sys.argv[1]+" is not a PDB file according to the extension!")
		else:
			sys.exit("ERROR: "+str(sys.argv[2])+" does not exist!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" does not exist!")
else:# Too many arguments
	sys.exit("ERROR: Too many arguments. Use the -h option for help.")



# Parsing the stuff

LIGA=0
fout=open('mapping_'+LIGAname+'_to_'+LIGBname+'.txt', 'w')
LIGA_coords={}
data={}
for line in pdbAin.readlines():
	if "ATOM" in line or "HETATM" in line:
		if "LIG" in line:
			LIGA=1
			atom_name=re.findall("[A-Z-a-z-0-9]+", line[13:17])[0]
			data[atom_name]="?"
			LIGA_coords[atom_name]=[float(str(line[30:38])),float(str(line[38:46])),float(str(line[46:54]))]
if LIGA==0:
	sys.exit("ERROR: I did not find a 'LIG' residue in "+sys.argv[1]+"!")
pdbAin.close()


for atom in LIGA_coords:
	pdbBin.seek(0)
	counter=0
	for line in pdbBin.readlines():
		if "ATOM" in line or "HETATM" in line:
			if "LIG" in line:
				dist=distance(float(line[30:38]),LIGA_coords[atom][0],float(line[38:46]),LIGA_coords[atom][1],float(line[46:54]),LIGA_coords[atom][2])
				if counter==0:
					counter=1
					atom_name=re.findall("[A-Z-a-z-0-9]+", line[13:17])[0]
					old_dist=dist
				elif counter==1:
					if old_dist > dist:
						old_dist=dist
						atom_name=re.findall("[A-Z-a-z-0-9]+", line[13:17])[0]
	if old_dist == 0.0:
		data[atom]=atom_name
	elif old_dist <= treshold:
		data[atom]=atom_name
	elif old_dist > treshold:
		data[atom]=atom_name+'?'
pdbBin.close()
data2=''
for char in str(data):
	if char=="'":
		data2+='"'
	else:
		data2+=char
fout.write(str(data2))
fout.close()
print "Arlight, check mapping_"+LIGAname+"_to_"+LIGBname+".txt and remove the extra comma at the end of the dictionnary!"

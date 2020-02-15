#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2019


# Importing necessary modules ###

import sys, re, os, math, json


### Defining and checking options and arguments ###

def distance(x1,x2,y1,y2,z1,z2):
        dist = float(math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
        return dist


# Parsing arguments

if len(sys.argv)==2:# One argument
	if str(sys.argv[1])=="-h":
		sys.exit("\nUsage: ./ligpargen2Q_charges.py <LIGref_lib> <LIGpargen.lib> <Burried_atom_name_for_neutralizing_cpd>\n")
	else:
		 sys.exit("ERROR: You need to provide the libdary files of original Q stuff and LiParGen and then a burried atom name  as respective arguments.")
elif len(sys.argv)<4:# Not enough arguments
	sys.exit("ERROR: You need to provide the libdary files of original Q stuff and LiParGen and then a burried atom name as respective arguments")
elif len(sys.argv)==4:# Three arguments
	if os.path.exists(sys.argv[1]):
		if os.path.exists(sys.argv[2]):
			if str(sys.argv[1])[-4:]==".lib":
				if str(sys.argv[2])[-4:]==".lib":
					libAin=open(str(sys.argv[1]), 'r')
					libBin=open(str(sys.argv[2]), 'r')
					burriedatom=str(sys.argv[3])
					if os.path.exists('mapping_ligpargen2Q.txt'):
						mappingf=open('mapping_ligpargen2Q.txt', 'r')
						mapping=json.loads(str(mappingf.readlines()[0]))
					else:
						sys.exit('ERROR: mapping_ligpargen2Q.txt does not exist. Please run prep_mapping_files_ligpargen2Q.py to generate it and correct it if there is any mistake!')
				else:
					sys.exit("ERROR: "+sys.argv[2]+" is no a .lib file according to the extension!")
			else:
				sys.exit("ERROR: "+sys.argv[1]+" is not a .lib file according to the extension!")
		else:
			sys.exit("ERROR: "+str(sys.argv[2])+" does not exist!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" does not exist!")
else:# Too many arguments
	sys.exit("ERROR: Too many arguments. Use the -h option for help.")



# Parsing the stuff

data={}
counter=0
atoms=[]
for line in libAin.readlines():
	if "[atoms]" in line:
		counter=1
	elif counter==1:
		if line=='\n' or '[bonds]' in line:
			break
		else:
			atom_name=re.findall("[A-Z-a-z-0-9]+", line)[1]
			atoms.append(atom_name)
			data[atom_name]={}
libAin.seek(0)

if burriedatom not in atoms:
	sys.exit("ERROR: Specified burried atom "+burriedatom+" not found in reference library file!")

counter=0
charges={}
for line in libBin.readlines():
	if "[atoms]" in line:
		counter=1
	elif counter==1:
		if line=='\n' or '[bonds]' in line:
			break
		else:
			atom_name=re.findall("[A-Z-a-z-0-9]+", line)[1]
			matches=0
			for atom in data:
				if mapping[atom]==atom_name:
					matches=1
					newcharge=re.findall(r"[-+]?\d*\.\d+|\d+", line)[-1]
					data[atom]=newcharge # New charge
					charges[atom]=newcharge
			if matches==0:
				sys.exit("ERROR: "+atom_name+" not matched to atoms of the reference dictionnary in mapping file!")
			
libBin.close()

# Checking residual charge and neutralizing specified burried atom

somme=0
for atom in charges:
	somme+=float(charges[atom])
if somme!=0:
	print "Neutralizing the residue by offsetting the charge of "+burriedatom+" by "+str(-round(somme, 6))
	data[burriedatom]=str(float(data[burriedatom])-round(somme, 6))

somme=0 # Double checking
for atom in data:
	somme+=float(data[atom])
if somme!=0:
	if somme>0.1 or somme<-0.1:
		print "WARNING: Residual charge is now "+str(round(somme, 6))
	else:
		print "Residual charge is now "+str(round(somme, 6))


# Now writting new .lib file

fout=open('LIG_new.lib', 'w')
counter=0
for line in libAin.readlines():
	if counter==0 and '[atoms]' not in line:
		fout.write(line)
	if '[atoms]' in line:
		counter=1
		fout.write(line)
	elif counter==1 and line!='\n' and '[bonds]' not in line:
		charge=data[re.findall("[A-Z-a-z-0-9]+", line)[1]]
		elements=re.split('[ \t]+', line[:-1])
		if len(elements)!=5:
			sys.exit("ERROR: Did not manage to split libary atom #/name/type/charge line into 4 elements in reference LIG.lib file. Maybe the spacing is no a 't character? If so, ask Pierre to ajust this script")
		else:
			if charge[0]!='-':
				fout.write(elements[1]+'\t'+elements[2]+'\t'+elements[3]+'\t'+' '+str(format(float(charge), '.6f'))+'\n')
			else:
				fout.write(elements[1]+'\t'+elements[2]+'\t'+elements[3]+'\t'+str(format(float(charge), '.6f'))+'\n')
	elif counter==1 and (line=='\n' or '[bonds]' in line):
		counter=2
		fout.write(line)
	elif counter==2:
		 fout.write(line)

libAin.close()
fout.close()

print "Arlight, check the newly generated LIG_new.lib file and replace the Forcefild/LIG.lib file with this one!"

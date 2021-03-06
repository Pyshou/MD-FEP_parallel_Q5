#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2017


# Importing necessary modules ###

import sys, re, os, json


### Defining and checking options and arguments ###


# Function for parsing arguments
def parse_args():
	counter=0
	if len(sys.argv) == 4: # If three arguments
		if "-h" in sys.argv[1:] : # Help
			sys.exit('\nUsage : prep_ligfep_file_steps0and1.py \
<LIG1.lib> <LIG2.lib> <mapping_file.txt>\n\nContent of mapping file:\n\
{"atomname1":"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"\
}\nNote: an atom becoming a dummy atom should be named DU for the end state\n')
		else: # Checking if input files exist and if argument 3 is dico
			for file in sys.argv[1:4]:
				if os.path.exists(file) == False: # Not existing
					error_msg = "'ERROR: " + file + ", \
No such file in the specified path'"
					sys.exit(error_msg)
				elif '.lib' not in file and file in \
sys.argv[1:3]:
					sys.exit("ERROR: This tool only deals \
with LIG.lib files, I need a .lib extension")
				else: # If okay
					if counter == 0:
						lig1_lib=open(str(file), 'r')
						lig1_prm=\
open(str(file)[:-7]+"Qoplsaa.prm", 'r')
						counter+=1
					elif counter == 1:
						lig2_lib=open(str(file), 'r')
						counter+=1
					elif counter == 2:
						mappingf=open(str(file), 'r')
						if len(mappingf.readlines())>1:
							sys.exit('ERROR: The \
mapping file should only contain one line as a dictionary!')
						else:
							mappingf.seek(0)
	elif "-h" in sys.argv[1:] : # Help
		sys.exit('\nUsage : prep_ligfep_file_steps0and1.py <LIG1.lib> \
<LIG2.lib> <mapping_file.txt>\n\nContent of mapping file:\n{"atomname1":\
"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"}\nNote: an \
atom becoming a dummy atom should be named DU for the end state\n')
	elif len(sys.argv) == 1 : # If no arguments
		sys.exit("ERROR: No arguments or input files, use the [-h] \
option for help.")
	elif len(sys.argv) == 2 or len(sys.argv) == 3 : # If one arguments
		sys.exit("ERROR: You need to provide 3 arguments, use the [-h] \
option for help.")
	elif len(sys.argv) > 4 : # If too much arguments
		sys.exit("ERROR: Too many arguments, use the [-h] option for \
help.")
	return lig1_lib, lig2_lib, mappingf, lig1_prm


# Function for writing lig.fep file
def write_fep_file(counter, line_elements, line2_elements, atom_nb, output, \
softcore_on, atom_types, parameters, charges_state2, atom_types2, lig1_lib, lig1_prm):
	fout=open(output, 'a')
	if counter==0 or counter==3: # Writting header
		if counter==0 or (counter==3 and softcore_on==0):
			fout.write("!LIG1-2, electrostatics\n\n[FEP]\nstates 2\n\
offset_residue 1\n\n")
		elif counter==3 and softcore_on==1:
			fout.write("!LIG1-2, electrostatics\n\n[FEP]\nstates 2\n\
offset_residue 1\nsoftcore_use_max_potential on\n\n")
		fout.write("[atoms]\n")
		for atom in range(1, atom_nb+1):
			fout.write("%-2s %-2s\n"%(atom, atom))
		fout.write("\n[change_charges]\n")
	elif counter==1: # Writting charge transformation to dummy
		fout.write("%-2s   %9s %9s\n"%(line_elements[0], \
line_elements[3], '0.0000'))
	elif counter==2: # Writting charge transformation to atom in LIG2
		fout.write("%-2s   %9s %9s\n"\
%(line_elements[0], line_elements[3], line2_elements[3]))
	elif counter==4 or counter==5: # Output for step1_1/2
		for i in range(0, len(charges_state2)): # Updating charges
			fout.write("%-2s   %9s %9s\n"%(i+1, \
str(charges_state2[i]), str(charges_state2[i])))
		fout.write('\n[atom_types]\n')
		lig1_lib.seek(0)
		countlig=0
		match=0
		atom_names_ordered=[]
		atomtypes=[]
		for line in lig1_lib.readlines():
			if (str(line)=="\n" or "[bonds]" in line) and countlig==1:
				break
			elif countlig==1:
				atom_names_ordered.append(str(re.findall("[A-Z-a-z-0-9]+", line)[2])) # This will help later!
				lig1_prm.seek(0)
				countprm=0
				for line2 in lig1_prm.readlines():
					if (str(line2)=="\n" or "[bonds]" in line2) and countprm==1:
						break
					elif countprm==1:
						if str(re.findall("[A-Z-a-z-0-9]+", line2)[0])==str(re.findall("[A-Z-a-z-0-9]+", line)[2]):
							for atom in parameters: # Writting nbon parameter list
								if len(atomtypes)==0 and parameters[atom][0]==str(re.findall(r"[-+]?\d*\.\d+|\d+", line2)[1]):
									match=1
									fout.write("%-4s    %-9s %-7s    %-4s   %-4s   %-8s \
%-7s   %-6s\n"%(atom, parameters[atom][0], parameters[atom][2], 0.00, 0.00, \
parameters[atom][3], parameters[atom][4], parameters[atom][5]))
									atomtypes.append(atom)
									break
								elif atom not in atomtypes and parameters[atom][0]==str(re.findall(r"[-+]?\d*\.\d+|\d+", line2)[1]):
									match=1
									fout.write("%-4s    %-9s %-7s    %-4s   %-4s   %-8s \
%-7s   %-6s\n"%(atom, parameters[atom][0], parameters[atom][2], 0.00, 0.00, \
parameters[atom][3], parameters[atom][4], parameters[atom][5])) 
									atomtypes.append(atom)
									break
					elif "NONBONDED LIG PARAMETERS" in line2:
						countprm=1
				if match==0:
					 sys.exit("ERROR: Did not find "+str(atom)+" in first .lib file while it has been read in the corresponding .prm file! The script probably needs fixing with your format. Ask pierre.matricon@gmail.com")
			elif "[atoms]" in line or "[ atoms ]" in line:
				 countlig=1
		tocount=0
		atoms={}
		lig1_prm.seek(0)
		for line in lig1_prm.readlines():
			if (line=="\n" in line or "[bonds]" in line) and tocount==1:
				tocount=0
				break
			if tocount==1:
				atoms[str(re.findall("[A-Z-a-z-0-9]+", line)[0])]=str(re.findall("[0-9]+.[0-9]+", line)[1])
			if "NONBONDED LIG PARAMETERS" in line:
				tocount=1
		if softcore_on==1:
			fout.write("DU      0.0000    0.0000     0.0    0.0    0.0000   0.0000    1.0079\n")
		fout.write("\n[change_atoms]\n")
		if counter==4: # If step1_1
			zerocounter=-1
			for atom in atom_names_ordered:# Writting atomtypes in the order of the LIG file (can differ with ffld_server)!
				zerocounter+=1
				for param in parameters:
					for notordered in atoms:
						if notordered==atom and atoms[notordered]==parameters[param][0]:
							fout.write("%-2s  %-4s  %-4s\n"%(zerocounter+1, \
param, param))
		elif counter==5: # If step1_2 / step2
			zerocounter=-1
			for atom in atom_names_ordered:# Writting atomtypes the same way
				zerocounter+=1
				for param in parameters:
					for notordered in atoms:
						if atom_types2[zerocounter]=="DU?" and atoms[notordered]==parameters[param][0] and notordered==atom:
							fout.write("%-2s  %-4s  %-4s\n"%(zerocounter+1, param, atom_types2[zerocounter]))
						elif atoms[notordered]==parameters[param][0] and notordered==atom:
							fout.write("%-2s  %-4s  %-4s\n"%(zerocounter+1, \
param, param+"?"))
		if softcore_on==1: # If using softcore
			fout.write("\n[softcore]\n")
			count=0
			for charge in charges_state2: # Writting softcore \
#section 
				count+=1
				if float(charge)==0.0 and counter==4:\
# Softcored atom
					fout.write("%-2s   %-2s   %-2s\n"%(\
count, 0, 20))
				elif float(charge)==0.0 and counter==5:
					fout.write("%-2s   %-2s   %-2s\n"%(\
count, 20, "XX"))
				else: # Other atom
					fout.write("%-2s   %-2s   %-2s\n"%(\
count, 0, 0))
	fout.close()
	return 0


# Function counter atoms from .lib file of LIG1
def count_atoms(lig1_lib):
	counter=0
	atom_nb=0
	for line in lig1_lib.readlines():
		if (str(line)=="\n" or "[bonds]" in line) and counter==1:
			break
		elif counter==1:
			atom_nb+=1
		elif "[atoms]" in line or "[ atoms ]" in line:
			counter=1
	return atom_nb


# Function parsing charges and calling function for output editing
def get_lig_param_diffs(lig1_lib, lig2_lib, mapping, lig1_prm):
	softcore_on=0 # Will take value 1 if line to be added for
#			lig_step1_1.fep
	charges=[]
	atom_nb = count_atoms(lig1_lib)
	atom_types2=[]
	write_fep_file(0, 0, 0, atom_nb, 'lig_step0.fep', softcore_on, 0, 0, 0\
, 0, lig1_lib, lig1_prm) # Editing header
	counter=0
	lig1_lib.seek(0)
	for line in lig1_lib.readlines(): # Scanning .lib file of first LIG
		if (str(line)=="\n" or "[bonds]" in line) and counter==1:
			break
		elif counter==1: # Line with atom partial charge
			lig2_lib.seek(0)
			line_elements=re.findall("[A-Z-a-z-0-9]+", line)[0:3]+[re.findall(r"[-+]?\d*\.\d+|\d+", line)[-1]]
			counter2=0
			if mapping[re.findall("[A-Z-a-z-0-9]+", line)[1]]=="DU": # Dummy
				softcore_on=1 # Softcore will be used
				write_fep_file(1, line_elements, 0, atom_nb, \
'lig_step0.fep', softcore_on, 0, 0, 0, 0, lig1_lib, lig1_prm)
				charges.append('0.0000')
				atom_types2.append("DU?")
			else: # Searching for charge in LIG2.lib file
				atom_types2.append("CHK")
				for line2 in lig2_lib.readlines():
					if (str(line2)=="\n" or "[bonds]" in line2) and counter2==1:
						break
					elif counter2==1:
						line2_elements=re.findall("[A-Z-a-z-0-9]+", line2)[0:3]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[-1]]
						if str(line2_elements[1])==\
mapping[str(re.findall("[A-Z-a-z-0-9]+", line)[1])]:
							write_fep_file(2, \
line_elements, line2_elements, atom_nb, "lig_step0.fep", softcore_on, 0, 0, 0\
, 0, lig1_lib, lig1_prm) # Writting in .fep file
							charges.append(\
line2_elements[3])
							break
					elif "[atoms]"in line2 or "[ atoms ]" in line2:
						counter2=1
		elif "[atoms]" in line or "[ atoms ]" in line: # Reaching atom lines
			counter=1
	return softcore_on, atom_nb, charges, atom_types2


# Function parsing non_bonded parameters to edit step1_1.fep file
def edit_step1_1(lig1_prm, softcore_on, atom_nb, charges_state2, atom_types2, lig1_lib):
	write_fep_file(3, 0, 0, atom_nb, 'lig_step1_1.fep', softcore_on, 0, 0,\
0, 0, lig1_lib, lig1_prm)# Header
	write_fep_file(3, 0, 0, atom_nb, 'lig_step1_2.fep', softcore_on, 0, 0,\
0, 0, lig1_lib, lig1_prm)
	parameters={}
	counter=0
	atom_types = []
	for line in lig1_prm.readlines():
		if "! NONBONDED LIG PARAMETERS" in line: # Nnbon data
			counter=1
		elif (line=='\n' in line or "[bonds]" in line) and counter==1: # End of nbon params read
			break
		elif counter==1: # nbon params line
			line_elements=[re.findall("[A-Z-a-z-0-9]+", line)[0]]+re.findall(r"[-+]?\d*\.\d+|\d+", line)[1:7]
			atomtype=re.findall('[a-z-A-Z-0-9]+', line)[0]
			new=[0]
			if len(parameters)>0:
				for atom in parameters:
					if line_elements[1] == parameters[atom][0]:
						new.append(1)
						break
			if (1 not in new) or len(parameters)==0: # If new atom type
				if atomtype in parameters:
					count=0
					newatomtype=atomtype
					while newatomtype in parameters: # But if duplicated name
						count+=1
						newatomtype=atomtype+str(count)
					atomtype=newatomtype # Create new name with index
				if re.split("\.", line_elements[1])[0]=="944":
					parameters["CT"]=line_elements[1:7]
					atom_types.append("CT")
				elif re.split("\.", line_elements[1])[0]=="1802":
					parameters["CAM"]=line_elements[1:7]
					atom_types.append("CAM")
				elif re.split("\.", line_elements[1])[0]=="1026":
					parameters["NA2"]=line_elements[1:7]
					atom_types.append("NA2")
				elif re.split("\.", line_elements[1])[0]=="1064":
					parameters["NH"]=line_elements[1:7]
					atom_types.append("NH")
				elif re.split("\.", line_elements[1])[0]=="616":
					parameters["OAM"]=line_elements[1:7]
					atom_types.append("OAM")
				elif re.split("\.", line_elements[1])[0]=="971":
					parameters["NA1"]=line_elements[1:7]
					atom_types.append("NA1")
				elif re.split("\.", line_elements[1])[0]=="760":
					parameters["OH"]=line_elements[1:7]
					atom_types.append("OH")
				elif re.split("\.", line_elements[1])[0]=="445":
					parameters["OT"]=line_elements[1:7]
					atom_types.append("OT")
				elif re.split("\.", line_elements[1])[0]=="69":
					parameters["HA1"]=line_elements[1:7]
					atom_types.append("HA1")
				elif re.split("\.", line_elements[1])[0]=="109":
					parameters["HA2"]=line_elements[1:7]
					atom_types.append("HA2")
				elif re.split("\.", line_elements[1])[0]=="84":
					parameters["HC"]=line_elements[1:7]
					atom_types.append("HC")
				elif re.split("\.", line_elements[1])[0]=="1059":
					parameters["CA1"]=line_elements[1:7]
					atom_types.append("CA1")
				elif re.split("\.", line_elements[1])[0]=="1039":
					parameters["CA2"]=line_elements[1:7]
					atom_types.append("CA2")
				elif line_elements[1]=="0.0054" or line_elements[1]=="0.01":
					parameters["HO"]=line_elements[1:7]
					atom_types.append("HO")
				elif line_elements[1]=="0.0" or line_elements[1]=="0.0000":
					parameters["HDU"]=line_elements[1:7]
					atom_types.append("HDU")
				elif re.split("\.", line_elements[1])[0]=="2558":
					parameters["SA"]=line_elements[1:7]
					atom_types.append("SA")
				else:#New type
					parameters[atomtype]=line_elements[1:7]
					atom_types.append(atomtype)
			else: # Already defined atomtype
				for atom in parameters:
					if line_elements[1] == parameters[atom][0]:
						atomtype=atom
				atom_types.append(atomtype)
	write_fep_file(4, line_elements, 0, atom_nb, "lig_step1_1.fep", \
softcore_on, atom_types, parameters, charges_state2, atom_types2, lig1_lib, lig1_prm)\
# Writting in .fep file
	write_fep_file(5, line_elements, 0, atom_nb, "lig_step1_2.fep", \
softcore_on, atom_types, parameters, charges_state2, atom_types2, lig1_lib, lig1_prm)\
# Writting in .fep file
	return 0

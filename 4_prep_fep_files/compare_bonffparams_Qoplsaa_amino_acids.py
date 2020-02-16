#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2017


# Importing necessary modules


import sys, re, os, json


# Preparing variables
outlines={}
outlines["[bond_types]"]=[]
outlines["[change_bonds]"]=[]
outlines["[angle_types]"]=[]
outlines["[change_angles]"]=[]
outlines["[torsion_types]"]=[]
outlines["[change_torsions]"]=[]

# Defining and checking options and arguments


counter=0
if len(sys.argv) == 4: # If three arguments
	if "-h" in sys.argv[1:] : # Help
		sys.exit('\nUsage : compare_bonffparams_Qoplsaa_amino_acids.py <RES1.lib> <RES2.lib> <mapping_file.txt>\n\nContent of mapping file:\n{"atomname1":"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"}\nNote: an atom becoming a dummy atom should be named DU for the end state\n')
	else: # Checking if input files exist and if argument 3 is a dictionary
		for file in sys.argv[1:4]:
			if os.path.exists(file) == False: # Doesn't exist
				error_msg = "'ERROR: " + file + ", No such file in the specified path'"
				sys.exit(error_msg)
			elif '.lib' not in file and file in sys.argv[1:3]:
				sys.exit("ERROR: This tool only deals with library files, I need a .lib extension")
			else: # If okay
				if counter == 0:
					if os.path.exists("Forcefield/Qoplsaa.prm"):
						topol_prm=open("Forcefield/Qoplsaa.prm", 'r')
					else:
						sys.exit("ERROR: Forcefield/Qoplsaa.prm does not exist. I need it!")
					lig1_lib=open(str(file), 'r')
					counter+=1
				elif counter == 1:
					lig2_lib=open(str(file), 'r')
					counter+=1
				elif counter == 2:
					mappingf=open(str(file), 'r')
					if len(mappingf.readlines())>1:
						sys.exit('ERROR: The mapping file should only contain one line as a dictionary!')
					else:
						mappingf.seek(0)
elif "-h" in sys.argv[1:] : # Help
	sys.exit('\nUsage : compare_bonffparams_Qoplsaa.py <RES1.lib> <RES2.lib> <mapping_file.txt>\n\nContent of mapping file:\n{"atomname1":"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"}\nNote: an atom becoming a dummy atom should be named DU for the end state\n')
elif len(sys.argv) == 1 : # If no arguments
	sys.exit("ERROR: No arguments or input files, use the [-h] option for help.")
elif len(sys.argv) == 2 or len(sys.argv) == 3 : # If one arguments
	sys.exit("ERROR: You need to provide 3 arguments, use the [-h] option for help.")
elif len(sys.argv) > 4 : # If too much arguments
	sys.exit("ERROR: Too many arguments, use the [-h] option for help.")



# Enumerating non bonded parameters of both states

mapping=json.loads(str(mappingf.readlines()[0])[:-1])

print "\nProcessing non_bonded parameter for "+str(len(mapping))+" atoms (exluding removals for dummy atoms)...\n"


def get_param_list(liglib):
	counter=0
	atom_list={}
	bond_list={}
	angle_list={}
	torsion_list={}
	atom_nb=0
	for line in liglib.readlines():
		if counter==1 and "[" not in line: # Establishing atom name/type correspondance from [atoms] section
			atom_nb+=1
			atom_list[re.findall("[A-Z-0-9]+", line)[1]]=[re.findall("[A-Z-0-9]+", line)[2],str(atom_nb)]
		elif counter==2 and "[" not in line: # Enumerating bonds, getting correspondance with atomtypes plus atom indices
			bond_list[re.findall("[A-Z-0-9]+", line)[0]+' '+re.findall("[A-Z-0-9]+", line)[1]]=[atom_list[re.findall("[A-Z-0-9]+", line)[0]][0],atom_list[re.findall("[A-Z-0-9]+", line)[1]][0],atom_list[re.findall("[A-Z-0-9]+", line)[0]][1],atom_list[re.findall("[A-Z-0-9]+", line)[1]][1]]
		elif "[atoms]" in line:
			counter=1
		elif "[bonds]" in line:
			counter=2
		elif "[" in line and counter==2:
			counter=0
			break
	for atm1 in atom_list: # Enumerating angles
		atom1=atom_list[atm1][0]
		for atm2 in atom_list:
			atom2=atom_list[atm2][0]
			for atm3 in atom_list:
				atom3=atom_list[atm3][0]
				if (atm1+' '+atm2 in bond_list or atm2+' '+atm1 in bond_list) and (atm2+' '+atm3 in bond_list or atm3+' '+atm2 in bond_list) and atm1!=atm3:
					angle_list[atm1+' '+atm2+' '+atm3]=[atom1, atom2, atom3]+[atom_list[atm1][1],atom_list[atm2][1],atom_list[atm3][1]]
	for atm1 in atom_list: # Enumerating torsions
		atom1=atom_list[atm1][0]
		for atm2 in atom_list:
			atom2=atom_list[atm2][0]
			for atm3 in atom_list:
				atom3=atom_list[atm3][0]
				for atm4 in atom_list:
					atom4=atom_list[atm4][0]
					if (atm1+' '+atm2 in bond_list or atm2+' '+atm1 in bond_list) and (atm2+' '+atm3 in bond_list or atm3+' '+atm2 in bond_list) and (atm3+' '+atm4 in bond_list or atm4+' '+atm3 in bond_list) and atm1!=atm3 and atm1!=atm4 and atm2!=atm4:
						torsion_list[atm1+' '+atm2+' '+atm3+' '+atm4]=[atom1, atom2, atom3, atom4]+[atom_list[atm1][1],atom_list[atm2][1],atom_list[atm3][1],atom_list[atm4][1]]
	return bond_list, angle_list, torsion_list


lig1_params=get_param_list(lig1_lib)[0:3]
lig2_params=get_param_list(lig2_lib)[0:3]



# Enumerating changed bond lengths


print "\nBOND LENGTHS\n"

bond_nb=0
for bond1 in lig1_params[0]: # Bonds data for state 1
	for bond2 in lig2_params[0]: # Bonds data for state 2
		if (mapping[re.findall('[A-Z-0-9]+', bond1)[0]] == re.findall('[A-Z-0-9]+', bond2)[0] and mapping[re.findall('[A-Z-0-9]+', bond1)[1]] == re.findall('[A-Z-0-9]+', bond2)[1]) or (mapping[re.findall('[A-Z-0-9]+', bond1)[1]] == re.findall('[A-Z-0-9]+', bond2)[0] and mapping[re.findall('[A-Z-0-9]+', bond1)[0]] == re.findall('[A-Z-0-9]+', bond2)[1]): # Matched bonds
			topol_prm.seek(0)
			counter=0
			match_count=0
			for line in topol_prm.readlines(): # Searching for corresponding parameters
				if match_count==2:# Already found bond data for both states
					break
				if "[bonds]" in line:
					counter=1
				elif counter==1 and "*" not in line and line[0]!="!" and line!="\n" and "LIG" not in line: # Bond section
					line_elements=re.findall("[A-Z-0-9]+", line)[0:2]+re.findall("[0-9]+\.[0-9]+", line)[0:2]
					if (line_elements[0]==lig1_params[0][bond1][0] and line_elements[1]==lig1_params[0][bond1][1]) or (line_elements[0]==lig1_params[0][bond1][1] and line_elements[1]==lig1_params[0][bond1][0]): # Matching Qoplsaa.prm line with bond of state A
						bond1_data=line_elements
						match_count+=1
					if (line_elements[0]==lig2_params[0][bond2][0] and line_elements[1]==lig2_params[0][bond2][1]) or (line_elements[0]==lig2_params[0][bond2][1] and line_elements[1]==lig2_params[0][bond2][0]): # Matching Qoplsaa.prm line with bond of state B
						bond2_data=line_elements
						match_count+=1
			if match_count==2: # Found data for both states
				if bond1_data[2:4]!=bond2_data[2:4]: # Bond has changed
					bond_nb+=2
					print re.findall("[A-Z-0-9]+", bond1)[0]+'\t'+re.findall("[A-Z-0-9]+", bond1)[1]+'\n   '+bond1_data[2]+' '+bond1_data[3]+'\n-> '+bond2_data[2]+'\t'+bond2_data[3]+'\n---------------------'
					outlines["[bond_types]"].append(str(bond_nb-1)+' '+bond1_data[2]+' '+bond1_data[3]+'\n')
					outlines["[bond_types]"].append(str(bond_nb)+' '+bond2_data[2]+' '+bond2_data[3]+'\n')
					outlines["[change_bonds]"].append(lig1_params[0][bond1][2]+' '+lig1_params[0][bond1][3]+' '+str(bond_nb-1)+' '+str(bond_nb)+'\n')



# Enumerating changed angles

print "\n\nANGLES\n"

angle_nb=0
already_angles=[]
for angle1 in lig1_params[1]: # Angles data for state 1
	for angle2 in lig2_params[1]: # Angles data for state 2
		if (mapping[re.findall('[A-Z-0-9]+', angle1)[0]] == re.findall('[A-Z-0-9]+', angle2)[0] and mapping[re.findall('[A-Z-0-9]+', angle1)[1]] == re.findall('[A-Z-0-9]+', angle2)[1] and mapping[re.findall('[A-Z-0-9]+', angle1)[2]] == re.findall('[A-Z-0-9]+', angle2)[2]) or (mapping[re.findall('[A-Z-0-9]+', angle1)[2]] == re.findall('[A-Z-0-9]+', angle2)[0] and mapping[re.findall('[A-Z-0-9]+', angle1)[1]] == re.findall('[A-Z-0-9]+', angle2)[1] and mapping[re.findall('[A-Z-0-9]+', angle1)[0]] == re.findall('[A-Z-0-9]+', angle2)[2]): # Matched angles
			topol_prm.seek(0)
			counter=0
			match_count=0
			for line in topol_prm.readlines(): # Searching for corresponding parameters
				if match_count==2:# Already found angle data for both states
					break
				if "[angles]" in line:
					counter=1
				elif counter==1 and "*" not in line and line[0]!="!" and line!="\n" and "LIG" not in line: # Angle section
					line_elements=re.findall("[A-Z-0-9]+", line)[0:3]+re.findall("[0-9]+\.[0-9]+", line)[0:2]
					if (line_elements[0]==lig1_params[1][angle1][0] and line_elements[1]==lig1_params[1][angle1][1] and line_elements[2]==lig1_params[1][angle1][2]) or (line_elements[0]==lig1_params[1][angle1][2] and line_elements[1]==lig1_params[1][angle1][1] and line_elements[2]==lig1_params[1][angle1][0]): # Matching Qoplsaa.prm line with angle of state A
						angle1_data=line_elements
						match_count+=1
					if (line_elements[0]==lig2_params[1][angle2][0] and line_elements[1]==lig2_params[1][angle2][1] and line_elements[2]==lig2_params[1][angle2][2]) or (line_elements[0]==lig2_params[1][angle2][2] and line_elements[1]==lig2_params[1][angle2][1] and line_elements[2]==lig2_params[1][angle2][0]): # Matching Qoplsaa.prm line with angle of state B
						angle2_data=line_elements
						match_count+=1
			if match_count==2: # Found data for both states
				if angle1_data[3:5]!=angle2_data[3:5]: # Angle has changed
					if lig1_params[1][angle1][3]+' '+lig1_params[1][angle1][4]+' '+lig1_params[1][angle1][5] not in already_angles:
						angle_nb+=2
						already_angles.append(lig1_params[1][angle1][3]+' '+lig1_params[1][angle1][4]+' '+lig1_params[1][angle1][5])
						print re.findall("[A-Z-0-9]+", angle1)[0]+'\t'+re.findall("[A-Z-0-9]+", angle1)[1]+'\t'+re.findall("[A-Z-0-9]+", angle1)[2]+'\n   '+angle1_data[3]+' '+angle1_data[4]+'\n-> '+angle2_data[3]+' '+angle2_data[4]+'\n---------------------'
						outlines["[angle_types]"].append(str(angle_nb-1)+' '+angle1_data[3]+' '+angle1_data[4]+'\n')
						outlines["[angle_types]"].append(str(angle_nb)+' '+angle2_data[3]+' '+angle2_data[4]+'\n')
						outlines["[change_angles]"].append(lig1_params[1][angle1][3]+' '+lig1_params[1][angle1][4]+' '+lig1_params[1][angle1][5]+' '+str(angle_nb-1)+' '+str(angle_nb)+'\n')


# Enumerating changed torsions

print "\n\nTORSIONS"

torsion_nb=0
already_torsions=[]
for torsion1 in lig1_params[2]: # Torsions data for state 1
	for torsion2 in lig2_params[2]: # Torsions data for state 2
		if (mapping[re.findall('[A-Z-0-9]+', torsion1)[0]] == re.findall('[A-Z-0-9]+', torsion2)[0] and mapping[re.findall('[A-Z-0-9]+', torsion1)[1]] == re.findall('[A-Z-0-9]+', torsion2)[1] and mapping[re.findall('[A-Z-0-9]+', torsion1)[2]] == re.findall('[A-Z-0-9]+', torsion2)[2] and mapping[re.findall('[A-Z-0-9]+', torsion1)[3]] == re.findall('[A-Z-0-9]+', torsion2)[3]) or (mapping[re.findall('[A-Z-0-9]+', torsion1)[3]]== re.findall('[A-Z-0-9]+', torsion2)[0] and mapping[re.findall('[A-Z-0-9]+', torsion1)[2]] == re.findall('[A-Z-0-9]+', torsion2)[1] and mapping[re.findall('[A-Z-0-9]+', torsion1)[1]] == re.findall('[A-Z-0-9]+', torsion2)[2] and mapping[re.findall('[A-Z-0-9]+', torsion1)[0]] == re.findall('[A-Z-0-9]+', torsion2)[3]): # Matched torsions
			topol_prm.seek(0)
			counter=0
			term_count1=0
			term_count2=0
			match_count=0
			torsion1_data=[]
			torsion2_data=[]
			for line in topol_prm.readlines(): # Searching for corresponding parameters
				if "[impropers]" in line:# Already found torsion data for both states
					break
				if "[torsions]" in line:
					counter=1
				elif counter==1 and "*" not in line and line[0]!="!" and line!="\n" and "LIG" not in line: # Torsion section
					line_elements=re.findall("[A-Z-0-9]+", line)[0:4]+re.findall(r"[-+]?\d*\.\d+|\d+", line)[4:7]
					if (line_elements[0]==lig1_params[2][torsion1][0] and line_elements[1]==lig1_params[2][torsion1][1] and line_elements[2]==lig1_params[2][torsion1][2] and line_elements[3]==lig1_params[2][torsion1][3]) or (line_elements[0]==lig1_params[2][torsion1][3] and line_elements[1]==lig1_params[2][torsion1][2] and line_elements[2]==lig1_params[2][torsion1][1] and line_elements[3]==lig1_params[2][torsion1][0]): # Matching Qoplsaa.prm line with torsion of state A
						if term_count1==0:
							torsion1_data=[]
						if line_elements not in torsion1_data:
							torsion1_data.append(line_elements)
							term_count1+=1
					if (line_elements[0]==lig2_params[2][torsion2][0] and line_elements[1]==lig2_params[2][torsion2][1] and line_elements[2]==lig2_params[2][torsion2][2] and line_elements[3]==lig2_params[2][torsion2][3]) or (line_elements[0]==lig2_params[2][torsion2][3] and line_elements[1]==lig2_params[2][torsion2][2] and line_elements[2]==lig2_params[2][torsion2][1] and line_elements[3]==lig2_params[2][torsion2][0]): # Matching Qoplsaa.prm line with torsion of state B
						if term_count2==0:
							torsion2_data=[]
						if line_elements not in torsion2_data:
							torsion2_data.append(line_elements)
							term_count2+=1
			for tors1 in torsion1_data:
				for tors2 in torsion2_data:
					if tors1[4] == tors2[4] and tors1[6] == tors2[6]:
						match_count+=1
			if len(tors1)!=len(tors2) or match_count!=len(torsion1_data): # Different torsions
				if torsion1 not in already_torsions:
					already_torsions.append(torsion1)
					print "\n"+re.findall("[A-Z-0-9]+", torsion1)[0]+'\t'+re.findall("[A-Z-0-9]+", torsion1)[1]+'\t'+re.findall("[A-Z-0-9]+",torsion1)[2]+'\t'+re.findall("[A-Z-0-9]+",torsion1)[3]
					count_terms1=0
					for term1 in torsion1_data:
						count_terms1+=1
						torsion_nb+=1
						print '   Term'+str(count_terms1)+': '+term1[4]+' '+term1[5]+' '+term1[6]
						outlines["[torsion_types]"].append(str(torsion_nb)+' '+term1[4]+' '+term1[5]+' '+term1[6]+'\n')
						outlines["[change_torsions]"].append(lig1_params[2][torsion1][4]+' '+lig1_params[2][torsion1][5]+' '+lig1_params[2][torsion1][6]+' '+lig1_params[2][torsion1][7]+' '+str(torsion_nb)+' 0\n')
					count_terms2=0
					for term2 in torsion2_data:
						count_terms2+=1
						torsion_nb+=1
						print '-> Term'+str(count_terms2)+': '+term2[4]+' '+term2[5]+' '+term2[6]
						outlines["[torsion_types]"].append(str(torsion_nb)+' '+term2[4]+' '+term2[5]+' '+term2[6]+'\n')
						outlines["[change_torsions]"].append(lig1_params[2][torsion1][4]+' '+lig1_params[2][torsion1][5]+' '+lig1_params[2][torsion1][6]+' '+lig1_params[2][torsion1][7]+' 0 '+str(torsion_nb)+'\n')
					print "\n------------------------------"


# Writting output

fout=open("changes.fep", 'w')
fout.write("[bond_types]\n")
for bond_types in outlines["[bond_types]"]:
	fout.write(bond_types)
fout.write("\n[change_bonds]\n")
for change_bonds in outlines["[change_bonds]"]:
	fout.write(change_bonds)
fout.write("\n[angle_types]\n")
for angle_types in outlines["[angle_types]"]:
	fout.write(angle_types)
fout.write("\n[change_angles]\n")
for change_angles in outlines["[change_angles]"]:
	fout.write(change_angles)
fout.write("\n[torsion_types]\n")
for torsion_types in outlines["[torsion_types]"]:
	fout.write(torsion_types)
fout.write("\n[change_torsions]\n")
for change_torsions in outlines["[change_torsions]"]:
	fout.write(change_torsions)
fout.write("\n")
fout.close()

print "\nAlright! Check changes.fep and also check improper torsions manually!"

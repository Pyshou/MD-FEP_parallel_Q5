#! /usr/bin/env python
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2017


# Importing necessary modules


import sys, re, os, json


# Defining and checking options and arguments


counter=0
if len(sys.argv) == 4: # If three arguments
	if "-h" in sys.argv[1:] : # Help
		sys.exit('\nUsage : compare_bonffparams_Qoplsaa.py <Qoplsaa_topol.prm> <Qoplsaa_end_state.prm> <mapping_file.txt>\n\nContent of mapping file:\n{"atomname1":"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"}\nNote: an atom becoming a dummy atom should be named DU for the end state\n')
	else: # Checking if input files exist and if argument 3 is a dictionary
		for file in sys.argv[1:4]:
			if os.path.exists(file) == False: # Doesn't exist
				error_msg = "'ERROR: " + file + ", No such file in the specified path'"
				sys.exit(error_msg)
			elif '.prm' not in file and file in sys.argv[1:3]:
				sys.exit("ERROR: This tool only deals with Qoplaa.prm files, I need a .prm extension")
			else: # If okay
				if counter == 0:
					topol_prm=open(str(file), 'r')
					lig1_lib=open(str(file)[:-11]+"LIG.lib", 'r')
					counter+=1
				elif counter == 1:
					end_prm=open(str(file), 'r')
					lig2_lib=open(str(file)[:-11]+"LIG.lib", 'r')
					counter+=1
				elif counter == 2:
					mappingf=open(str(file), 'r')
					if len(mappingf.readlines())>1:
						sys.exit('ERROR: The mapping file should only contain one line as a dictionary!')
					else:
						mappingf.seek(0)
elif "-h" in sys.argv[1:] : # Help
	sys.exit('\nUsage : compare_bonffparams_Qoplsaa.py <Qoplsaa_topol.prm> <Qoplsaa_end_state.prm> <mapping_file.txt>\n\nContent of mapping file:\n{"atomname1":"atomname1b","atomname2":"atomname2b",...,"atomnamen":"atomnamenb"}\nNote: an atom becoming a dummy atom should be named DU for the end state\n')
elif len(sys.argv) == 1 : # If no arguments
	sys.exit("ERROR: No arguments or input files, use the [-h] option for help.")
elif len(sys.argv) == 2 or len(sys.argv) == 3 : # If one arguments
	sys.exit("ERROR: You need to provide 3 arguments, use the [-h] option for help.")
elif len(sys.argv) > 4 : # If too much arguments
	sys.exit("ERROR: Too many arguments, use the [-h] option for help.")



# Running the programm 

mapping=json.loads(str(mappingf.readlines()[0])[:-1])

print "\nProcessing non_bonded parameter for "+str(len(mapping))+" atoms (exluding removals for dummy atoms)...\n"

term_data1={}
term_data2={}
(counter,counter2)=(0,0)
outlines={}
bond_nb=0
angle_nb=0
outlines["[bond_types]"]=[]
outlines["[change_bonds]"]=[]
outlines["[angle_types]"]=[]
outlines["[change_angles]"]=[]
outlines["[torsion_types]"]=[]
outlines["[change_torsions]"]=[]
isfile=0
for line in topol_prm.readlines():
	if str(line)=="\n" or line[0]=="!" or "WILD CARD" in line:
		counter=0
	if counter==1:#Bond section
		end_prm.seek(0)
		line_elements=re.split('[\t\n]', re.split("[ ]+", line)[0])
		if len(line_elements)==1:
			line_elements=re.findall('[A-Z0-9]+', line)[0:2]+re.findall(r"[-+]?\d*\.\d+|\d+", line)[2:4]
			strike=0
			lig1_lib.seek(0)
			atom_data1={}
			atom_nb=0
			for linelib1 in lig1_lib.readlines():
				if "[bonds]" in linelib1:
					strike=0
					break
				elif "[atoms]" in linelib1 or "[ atoms ]" in linelib1:
					strike=1
				elif strike==1:
					atom_nb+=1
					if line_elements[0]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1]=atom_nb
					elif line_elements[1]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1b=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1b]=atom_nb
		for line2 in end_prm.readlines():
			if str(line2)=="\n" or line2[0]=="!" or "WILD CARD" in line2:
				counter2=0
			elif counter2==1:
				line2_elements=re.split('[\t\n]', re.split("[ ]+", line2)[0])
				if len(line2_elements)==1:
					isfile=1
					line2_elements=re.findall('[A-Z0-9]+', line2)[0:2]+re.findall(r"[-+]?\d*\.\d+|\d+", line2)[2:4]
					lig2_lib.seek(0)
					strike2=0
					for linelib2 in lig2_lib.readlines():
						if "[bonds]" in linelib2:
							strike2=0
							break
						elif "[atoms]" in linelib2 or "[ atoms ]" in linelib2:
							strike2=1
						elif strike2==1:
							if line2_elements[0]==re.findall('[A-Z0-9]+', linelib2)[2]:
								atom2=re.findall('[A-Z0-9]+', linelib2)[1]
							elif line2_elements[1]==re.findall('[A-Z0-9]+', linelib2)[2]:
								atom2b=re.findall('[A-Z0-9]+', linelib2)[1]
					if (atom2==mapping[atom1] and atom2b==mapping[atom1b]) or (atom2==mapping[atom1b] and atom2b==mapping[atom1]):
						if line_elements[2]!=line2_elements[2] or line_elements[3]!=line2_elements[3]:
							bond_nb+=2
							outlines["[change_bonds]"].append(str(atom_data1[atom1])+' '+str(atom_data1[atom1b])+' '+str(bond_nb-1)+' '+str(bond_nb)+'\n')
							outlines["[bond_types]"].append(str(bond_nb-1)+' '+line_elements[2]+' '+line_elements[3]+'\n')
							outlines["[bond_types]"].append(str(bond_nb)+' ' +line2_elements[2]+' '+line2_elements[3]+'\n')
							print ''+atom1+'\t'+atom1b+'\n   '+line_elements[2]+'\t'+line_elements[3]+'\n-> '+line2_elements[2],'\t'+line2_elements[3]+'\n'+'---------------------'
							counter2=0
							end_prm.seek(0)
							break
				elif (str(line2_elements[0])[1:]==mapping[str(line_elements[0])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[1])[1:]]) or (str(line2_elements[0])[1:]==mapping[str(line_elements[1])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[0])[1:]]):
					if line_elements[2]!=line2_elements[2] or line_elements[3]!=line2_elements[3]:
						print ''+line_elements[0]+'\t'+line_elements[1]+'\n   '+line_elements[2]+'\t'+line_elements[3]+'\n-> '+line2_elements[2],'\t'+line2_elements[3]+'\n'+'---------------------'
					counter2=0
					end_prm.seek(0)
					break
			elif "BOND LIG PARAMETERS" in line2:
				counter2=1
	if counter==2:#Angle section
		end_prm.seek(0)
		line_elements=re.split('[\t]', re.split("[\n]+", line)[0])
		if len(line_elements)==1:
			atom_data1={}
			line_elements=re.findall('[A-Z0-9]+', line)[0:3]+re.findall(r"[-+]?\d*\.\d+|\d+", line)[3:5]
			lig1_lib.seek(0)
			strike1=0
			atom_nb=0
			for linelib1 in lig1_lib.readlines():
				if "[bonds]" in linelib1:
					strike1=0
					break
				elif "[atoms]" in linelib1 or "[ atoms ]" in linelib1:
					strike1=1
				elif strike1==1:
					atom_nb+=1
					if line_elements[0]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1]=atom_nb
					elif line_elements[1]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1b=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1b]=atom_nb
					elif line_elements[2]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1c=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1c]=atom_nb
		for line2 in end_prm.readlines():
			if str(line2)=="\n" or "!  X" in str(line2) or "WILD CARD" in line2:
				counter2=0
			elif counter2==2:
				line2_elements=re.split('[\t]', re.split("[\n]+", line2)[0])
				if len(line2_elements)==1:
					line2_elements=re.findall('[A-Z0-9]+', line2)[0:3]+re.findall(r"[-+]?\d*\.\d+|\d+", line2)[3:5]
					lig2_lib.seek(0)
					strike2=0
					for linelib2 in lig2_lib.readlines():
						if "[bonds]" in linelib2:
							strike2=0
							break
						elif "[atoms]" in linelib2 or "[ atoms ]" in linelib2:
							strike2=1
						elif strike2==1:
							if line2_elements[0]==re.findall('[A-Z0-9]+', linelib2)[2]:
								atom2=re.findall('[A-Z0-9]+', linelib2)[1]
							elif line2_elements[1]==re.findall('[A-Z0-9]+', linelib2)[2]:
								atom2b=re.findall('[A-Z0-9]+', linelib2)[1]
							elif line2_elements[2]==re.findall('[A-Z0-9]+', linelib2)[2]:
								atom2c=re.findall('[A-Z0-9]+', linelib2)[1]
					if (atom2==mapping[atom1] and atom2b==mapping[atom1b] and atom2c==mapping[atom1c]) or (atom2==mapping[atom1c] and atom2b==mapping[atom1b] and atom2c==mapping[atom1]):
						if line_elements[3]!=line2_elements[3] or line_elements[4]!=line2_elements[4]:
							angle_nb+=2
							outlines["[change_angles]"].append(str(atom_data1[atom1])+' '+str(atom_data1[atom1b])+' '+str(atom_data1[atom1c])+' '+str(angle_nb-1)+' '+str(angle_nb)+'\n')
							outlines["[angle_types]"].append(str(angle_nb-1)+' '+line_elements[3]+' '+line_elements[4]+'\n')
							outlines["[angle_types]"].append(str(angle_nb)+' ' +line2_elements[3]+' '+line2_elements[4]+'\n')
							print '   '+atom1+'\t'+atom1b+'\t'+atom1c+'\n   '+line_elements[3]+'\t'+line_elements[4]+'\n-> '+line2_elements[3]+'\t'+line2_elements[4]+'\n'+'-----------------------'
							counter2=0
							end_prm.seek(0)
							break
				elif (str(line2_elements[0])[1:]==mapping[str(line_elements[0])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[1])[1:]] and str(line2_elements[2])[1:]==mapping[str(line_elements[2])[1:]]) or (str(line2_elements[0])[1:]==mapping[str(line_elements[2])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[1])[1:]] and str(line2_elements[2])[1:]==mapping[str(line_elements[0])[1:]]):
					if line_elements[3]!=line2_elements[3] or line_elements[4]!=line2_elements[4]:
						print '   '+line_elements[0]+'\t'+line_elements[1]+'\t'+line_elements[2]+'\n   '+line_elements[3]+'\t'+line_elements[4]+'\n-> '+line2_elements[3]+'\t'+line2_elements[4]+'\n'+'-----------------------'
					counter2=0
					end_prm.seek(0)
					break
			elif "ANGLE LIG PARAMETERS" in line2:
				counter2=2
	if counter==3:# Torsion section
		end_prm.seek(0)
		line_elements=re.split('[\t]', re.split("[\n]+", line)[0])
		if len(line_elements)==1:
			atom_data1={}
			line_elements=re.findall('[A-Z0-9]+', line)[0:4]+[re.findall(r"[-+]?\d*\.\d+|\d+", line)[4]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line)[5]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line)[6]]
			lig1_lib.seek(0)
			strike1=0
			atom_nb=0
			for linelib1 in lig1_lib.readlines():
				if "[bonds]" in linelib1:
					strike1=0
					break
				elif "[atoms]" in linelib1 or "[ atoms ]" in linelib1:
					strike1=1
				elif strike1==1:
					atom_nb+=1
					if line_elements[0]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1]=atom_nb
					elif line_elements[1]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1b=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1b]=atom_nb
					elif line_elements[2]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1c=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1c]=atom_nb
					elif line_elements[3]==re.findall('[A-Z0-9]+', linelib1)[2]:
						atom1d=re.findall('[A-Z0-9]+', linelib1)[1]
						atom_data1[atom1d]=atom_nb
			if atom1+' '+atom1b+' '+atom1c+' '+atom1d not in term_data1:
				redundancy=0
				term1_count=1
				term_data1[atom1+' '+atom1b+' '+atom1c+' '+atom1d]={}
				term_data1[atom1+' '+atom1b+' '+atom1c+' '+atom1d][str(term1_count)]=[line_elements[4], line_elements[5], line_elements[6],str(atom_data1[atom1]),str(atom_data1[atom1b]),str(atom_data1[atom1c]),str(atom_data1[atom1d])]
			else:
				term1_count+=1
				term_data1[atom1+' '+atom1b+' '+atom1c+' '+atom1d][str(term1_count)]=[line_elements[4], line_elements[5], line_elements[6],str(atom_data1[atom1]),str(atom_data1[atom1b]),str(atom_data1[atom1c]),str(atom_data1[atom1d])]
				redundancy=1
			end_prm.seek(0)
			for line2 in end_prm.readlines():
				if str(line2)=="\n" or line2[0]=="!" or "WILD CARD" in line2:
					counter2=0
				elif counter2==3 and redundancy==0:
					line2_elements=re.split('[\t]', re.split("[\n]+", line2)[0])
					if len(line2_elements)==1:
						line2_elements=re.findall('[A-Z0-9]+', line2)[0:4]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[4]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[5]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[6]]
						lig2_lib.seek(0)
						strike2=0
						for linelib2 in lig2_lib.readlines():
							if "[bonds]" in linelib2:
								strike2=0
								break
							elif "[atoms]" in linelib2 or "[ atoms ]" in linelib2:
								strike2=1
							elif strike2==1:
								if line2_elements[0]==re.findall('[A-Z0-9]+', linelib2)[2]:
									atom2=re.findall('[A-Z0-9]+', linelib2)[1]
								elif line2_elements[1]==re.findall('[A-Z0-9]+', linelib2)[2]:
									atom2b=re.findall('[A-Z0-9]+', linelib2)[1]
								elif line2_elements[2]==re.findall('[A-Z0-9]+', linelib2)[2]:
									atom2c=re.findall('[A-Z0-9]+', linelib2)[1]
								elif line2_elements[3]==re.findall('[A-Z0-9]+', linelib2)[2]:
									atom2d=re.findall('[A-Z0-9]+', linelib2)[1]
					if (atom2==mapping[atom1] and atom2b==mapping[atom1b] and atom2c==mapping[atom1c] and atom2d==mapping[atom1d]) or (atom2==mapping[atom1d] and atom2b==mapping[atom1c] and atom2c==mapping[atom1b] and atom2d==mapping[atom1]):
						if atom1+' '+atom1b+' '+atom1c+' '+atom1d not in term_data2:
							term2_count=1
							term_data2[atom1+' '+atom1b+' '+atom1c+' '+atom1d]={}
							term_data2[atom1+' '+atom1b+' '+atom1c+' '+atom1d][str(term2_count)]=[line2_elements[4], line2_elements[5], line2_elements[6]]
						else:
							term2_count+=1
							term_data2[atom1+' '+atom1b+' '+atom1c+' '+atom1d][str(term2_count)]=[line2_elements[4], line2_elements[5], line2_elements[6]]
				elif " PROPER TORSION LIG PARAMETERS" in line2:
					counter2=3
		elif line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:] not in term_data1:
			redundancy=0
			term1_count=1
			term_data1[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]]={}
			term_data1[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]][str(term1_count)]=[line_elements[4], line_elements[5], line_elements[6]]
		else:
			term1_count+=1
			term_data1[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]][str(term1_count)]=[line_elements[4], line_elements[5], line_elements[6]]
			redundancy=1
		end_prm.seek(0)
		for line2 in end_prm.readlines():
			if str(line2)=="\n" or line2[0]=="!" or "WILD CARD" in line2:
				counter2=0
			elif counter2==3 and redundancy==0:
				line2_elements=re.split('[\t]', re.split("[\n]+", line2)[0])
				if len(line2_elements)==1:
					line2_elements=re.findall('[A-Z0-9]+', line2)[0:4]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[4]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[5]]+[re.findall(r"[-+]?\d*\.\d+|\d+", line2)[6]]
					lig2_lib.seek(0)
					strike2=0
				elif (str(line2_elements[0])[1:]==mapping[str(line_elements[0])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[1])[1:]] and str(line2_elements[2])[1:]==mapping[str(line_elements[2])[1:]] and str(line2_elements[3])[1:]==mapping[str(line_elements[3])[1:]]) or (str(line2_elements[0])[1:]==mapping[str(line_elements[3])[1:]] and str(line2_elements[1])[1:]==mapping[str(line_elements[2])[1:]] and str(line2_elements[2])[1:]==mapping[str(line_elements[1])[1:]] and str(line2_elements[3])[1:]==mapping[str(line_elements[0])[1:]]):
					if line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:] not in term_data2:
						term2_count=1
						term_data2[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]]={}
						term_data2[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]][str(term2_count)]=[line2_elements[4], line2_elements[5], line2_elements[6]]
					else:
						term2_count+=1
						term_data2[line_elements[0][1:]+' '+line_elements[1][1:]+' '+line_elements[2][1:]+' '+line_elements[3][1:]][str(term2_count)]=[line2_elements[4], line2_elements[5], line2_elements[6]]
			elif " PROPER TORSION LIG PARAMETERS" in line2:
				counter2=3
				
	if "BOND LIG PARAMETERS" in line:
		counter=1
		print "BOND LENGTHS\n"
	if "ANGLE LIG PARAMETERS" in line:
		counter=2
		print "\n\nANGLES\n"
	if " PROPER TORSION LIG PARAMETERS" in line:
		counter=3
		print "\n\nTORSIONS\n"
	if "improper type definitions" in str(line) or "[impropers]" in str(line):
		torsion='0'
		counter=0
		tors_nb=0
		for ele in term_data1:# Print previous data (we now have the number of terms, etc..)
			somestuff={}
			somestuff[ele]={}
			for stuff in term_data1[ele]:
				somestuff[ele][stuff]=term_data1[ele][stuff][0:3]
			if ele in term_data2 and somestuff[ele]!=term_data2[ele]: # Data differs
				if re.split("[ ]", ele)[0]+'\t'+re.split("[ ]", ele)[1]+'\t'+re.split("[ ]", ele)[2]+'\t'+re.split("[ ]", ele)[3]!=torsion:# New torsion
					torsion=re.split("[ ]", ele)[0]+'\t'+re.split("[ ]", ele)[1]+'\t'+re.split("[ ]", ele)[2]+'\t'+re.split("[ ]", ele)[3]
					print '   '+torsion
					term_index=0
					for term in term_data1[ele]:
						tors_nb+=1
						term_index+=1
						print '   Term'+str(term_index)+': '+term_data1[ele][term][0]+' '+term_data1[ele][term][1]+' '+term_data1[ele][term][2]
						outlines["[torsion_types]"].append(str(tors_nb)+' '+term_data1[ele][term][0]+' '+term_data1[ele][term][1]+' '+term_data1[ele][term][2]+'\n')
						outlines["[change_torsions]"].append(term_data1[ele][term][3]+' '+term_data1[ele][term][4]+' '+term_data1[ele][term][5]+' '+term_data1[ele][term][6]+' '+str(tors_nb)+' '+'0\n')
					term_index2=0
					for term2 in term_data2[ele]:
						tors_nb+=1
						term_index2+=1
						print '-> Term'+str(term_index2)+': '+term_data2[ele][term2][0]+' '+term_data2[ele][term2][1]+' '+term_data2[ele][term2][2]
						outlines["[torsion_types]"].append(str(tors_nb)+' '+term_data2[ele][term2][0]+' '+term_data2[ele][term2][1]+' '+term_data2[ele][term2][2]+'\n')
						outlines["[change_torsions]"].append(term_data1[ele][term][3]+' '+term_data1[ele][term][4]+' '+term_data1[ele][term][5]+' '+term_data1[ele][term][6]+' 0 '+str(tors_nb)+'\n')
					print "----------------------------"




if isfile==1:
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
	print "Now also check edited changes.fep file!"

print "\nNote: Check improper torsions if needed (when opening, closing or changing a ring size or groups such as amides)!"

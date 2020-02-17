#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2016


# Importing necessary modules

import sys, os, re, operator

# Maximum deltaG you wish to have between your intermediate states

gap_treshold = 0.6


# Defining and checking options and arguments


if len(sys.argv) == 2: # If one argument
        if str(sys.argv[1]) == "-h" : # Help
                sys.exit("Usage : ./FEP_converger.py \noptions:\n-h : Usage\n\nYou can change gap_treshold at the beginning of the script, in order to chose the maximum deltaG you wish between your intermediate states")
elif len(sys.argv) == 1: # No argument
	qfep_files=[]
	for folder in re.split('\n', os.popen('ls -d md_rs*').read())[:-1]:
		qfep_files.append(folder+'/qfep.out')
		if os.path.exists(folder+'/qfep.out') == False:
			sys.exit("ERROR: "+folder+'/qfep.out'+" doesn't exist ! Use the -h option for help")
else: # Too many arguments
	sys.exit("ERROR: Too many arguments. Check the -h option for syntax.")



# Running the program

convergence_data={}

def convergence_collector(qfep_file):
	counter = 0
	qfepin = open(qfep_file, 'r')
	for line in qfepin.readlines():
		if "Calculation for full system" in line:
			counter=1
		elif counter == 1 and "#" not in line and len(str(line)) > 4:
				convergence_data[(str(line)[3:11])] = []
				convergence_data[(str(line)[3:11])].append(float(str(line)[23:31]))
				convergence_data[(str(line)[3:11])].append(float(str(line)[43:51]))
		elif counter==1 and len(str(line)) < 4:
			break
	qfepin.close()
	return sorted(convergence_data.items(), key=operator.itemgetter(0))[::-1]


def lambda_designer():
	fout=open('lambdas.txt', 'w')
	data={}
	for qfep_file in qfep_files:
		data[qfep_file] = convergence_collector(qfep_file)
	for i in range(1,len(data[qfep_file])):
		gaps=[]
		for qfep_file in qfep_files:
			energy1=float(data[qfep_file][i-1][1][1])
			energy2=float(data[qfep_file][i][1][1])
			energy3=float(data[qfep_file][i][1][0])
			energy4=float(data[qfep_file][i-1][1][0])
			gaps.append(max(abs(energy2-energy1), abs(energy4-energy3)))
		gap=max(gaps)
		if gap > abs(float(gap_treshold)):
			number_of_new_lambdas=int(round((gap/0.6),0))
			if number_of_new_lambdas > 1:
				for j in range(1, number_of_new_lambdas):
					fout.write(str(format(float(data[qfep_files[0]][i][0])-j*(float(data[qfep_files[0]][i][0])-float(data[qfep_files[0]][i-1][0]))/number_of_new_lambdas, '2f'))+'\n')
			elif number_of_new_lambdas == 1:
				fout.write(str(format(float(data[qfep_files[0]][i][0])-(float(data[qfep_files[0]][i][0])-float(data[qfep_files[0]][i-1][0]))/2., '2f'))+'\n')
	fout.close()
	os.system('mv lambdas.txt temp; sort -r -u temp > lambdas.txt; rm temp')
	return 0

lambda_designer()

print "Alright, that should be done! Check 'lambdas.txt'! Use the same lambdas for each random seed so that you can combine them! You can use combine_FEP_files.py for that. Note that you can change gap_treshold at the beginning of the script, in order to chose the maximum deltaG you wish between your intermediate states"

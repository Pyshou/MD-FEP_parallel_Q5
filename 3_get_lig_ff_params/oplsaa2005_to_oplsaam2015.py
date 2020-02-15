#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2019


# Importing necessary modules ###

import sys, re, os


### Defining and checking options and arguments ###


# Parsing arguments

if len(sys.argv)==2:# One argument
	if str(sys.argv[1])!="h":
		sys.exit("\nUsage: ./oplsaa2005_to_oplsaam2015.py <Qoplsaa.prm> <LIG.prm>\n")
	else:
		 sys.exit("ERROR: You need to provide the Qoplsaa.prm and LIG.prm file paths as respective arguments.")
elif len(sys.argv)<3:# Not enough arguments
	sys.exit("ERROR: You need to provide the Qoplsaa.prm and LIG.prm file paths as respective arguments.")
elif len(sys.argv)==3:# Two arguments
	if os.path.exists(sys.argv[1]):
		if os.path.exists(sys.argv[2]):
			if len(open(str(sys.argv[1]), 'r').readlines()) <= len(open(str(sys.argv[2]), 'r').readlines()):
				sys.exit("ERROR: The first file should be the full opls one and second the ligand's. The number of lines contradict this!")
			else:
				LIGin=open(str(sys.argv[2]), 'r')
				prmin=open(str(sys.argv[1]), 'r')
		else:
			sys.exit("ERROR: "+str(sys.argv[2])+" does not exist!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" does not exist!")
else:# Too many arguments
	sys.exit("ERROR: Too many arguments. Use the -h option for help.")



# Parsing the stuff

fout=open('Qoplsaa_2.prm', 'w')
counter=0
counter2=0
(counter1b,counter2b,counter3b,counter4b,counter5b)=(0,0,0,0,0)
for line in prmin.readlines():
	if counter==0:
		fout.write(line)
		if "Avdw1" in line:
			counter=1#VdW section
		elif "dist" in line:
			counter=2#Bond section
			fout.write("*------------------------------------------------\n")
		elif "angle0" in line:
			counter=3#Angle section
			fout.write("*------------------------------------------------------------\n")
		elif "paths" in line:
			counter=4#Torsion section
			fout.write("*-----------------------------------------------------------------\n")
		elif "[impropers]" in line:
			counter=6#Special instance
	elif counter==6:
		fout.write(line)
		counter=5#Improper section
	elif counter==1:
		if str(line)!="\n":
			fout.write(line)
		else:
			for line2 in LIGin.readlines():
				if "! NONBONDED LIG PARAMETERS" in line2:
					fout.write(line2)
					counter2=1# VdW LIG section
				elif counter2==1:
					if str(line2)=="\n":
						fout.write(line2)
						counter2=0
						counter=0
						break
					else:
						fout.write(line2)
	elif counter==2:
		if str(line)!="\n":
			fout.write(line)
		else:
			LIGin.seek(0)
			for line2 in LIGin.readlines():
				if "! BOND LIG PARAMETERS" in line2:
					fout.write(line2)
					counter2=1# Bond LIG section
				elif counter2==1:
					if str(line2)=="\n":
						fout.write(line2)
						counter2=0
						counter=0
						break
					else:
						fout.write(line2)
	elif counter==3:
		if str(line)!="\n":
			fout.write(line)
		else:
			LIGin.seek(0)
			for line2 in LIGin.readlines():
				if "! ANGLE LIG PARAMETERS" in line2:
					fout.write(line2)
					counter2=1# Angle LIG section
				elif counter2==1:
					if str(line2)=="\n":
						fout.write(line2)
						counter2=0
						counter=0
						break
					else:
						fout.write(line2)
	elif counter==4:
		if str(line)!="\n":
			fout.write(line)
		else:
			LIGin.seek(0)
			for line2 in LIGin.readlines():
				if "! PROPER TORSION LIG PARAMETERS" in line2:
					fout.write(line2)
					counter2=1# Torsion LIG section
				elif counter2==1:
					if str(line2)=="\n":
						fout.write(line2)
						counter2=0
						counter=0
						break
					else:
						fout.write(line2)
	elif counter==5:
		if str(line)!="\n":
			fout.write(line)
		else:
			LIGin.seek(0)
			for line2 in LIGin.readlines():
				if "! IMPROPER TORSION LIG PARAMETERS" in line2:
					fout.write(line2)
					counter2=1# Improper LIG section
				elif counter2==1:
					if str(line2)=="\n":
						fout.write(line2)
						counter2=0
						counter=0
						break
					else:
						fout.write(line2)

print "Alright, check Qoplsaa_2.prm!"

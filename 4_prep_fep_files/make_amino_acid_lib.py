#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2018


# Importing necessary modules ###

import sys, re, os


# Parsing arguments

if len(sys.argv)==2:# One argument
	if str(sys.argv[1])=="-h":
		sys.exit("\nUsage: ./make_amino_acid_lib.py <Qoplsaa.lib> <resname>\n")
	else:
		 sys.exit("ERROR: You need to provide a path to an amino acid library file (i.e. Qoplsaa.lib), and a residue number (3-letter code) as respective arguments.")
elif len(sys.argv)<3:# Not enough arguments
	sys.exit("ERROR: You need to provide a path to an amino acid library file (i.e. Qoplsaa.lib), and     a residue number (3-letter code) as respective arguments.")
elif len(sys.argv)==3:# Three arguments
	if os.path.exists(sys.argv[1]):
		if len(str(sys.argv[2]))==3:
			if str(sys.argv[1])[-4:]==".lib":
				libin=open(str(sys.argv[1]), 'r')
				resname=str(sys.argv[2])
			else:
				sys.exit("ERROR: "+sys.argv[1]+" is not a library file according to the extension!")
		else:
			sys.exit("ERROR: "+str(sys.argv[2])+" should be a 3-letter amino acid code!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" does not exist!")
else:# Too many arguments
	sys.exit("ERROR: Too many arguments. Use the -h option for help.")



# Parsing the stuff

foutname=resname+".lib"
fout=open(foutname, 'w')
counter=0
for line in libin.readlines():
	if "{"+resname+"}"in line:
		counter=1
		fout.write(line)
	elif counter==1 and "*-" in line:
		counter=0
		break
	elif counter==1 and "*-" not in line:
		fout.write(line)

libin.close()
fout.close()

print "Arlight, check "+foutname+"!"

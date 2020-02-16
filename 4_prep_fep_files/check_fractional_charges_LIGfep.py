#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015



# Importing necessary modules


import sys, os, re


# Parsing arguments

if len(sys.argv)==1:
	sys.exit("ERROR: You need to provide a .fep file as argument!")
elif len(sys.argv)==2:
	if os.path.exists(str(sys.argv[1])):
		if ".fep" in str(sys.argv[1]):
			fin=open(str(sys.argv[1]), 'r')
		else:
			sys.exit("ERROR: "+str(sys.argv[1])+" is not a .fep file!")
	else:
		sys.exit("ERROR: "+str(sys.argv[1])+" doesn't exist!")
else:
	sys.exit("ERROR: Too many arguments. You only need to provide a .fep file as argument!")

counter=0
(charges1, charges2)=([],[])
for line in fin.readlines():
	if "[change_charges]" in line:
		counter=1
	elif line=="\n" or "[atom_types]" in line:
		counter=0
	elif counter==1:
		charges1.append(float(line[5:14]))
		charges2.append(float(line[15:24]))

fin.close()
total_charge1=float(sum(charges1))
total_charge2=float(sum(charges2))

if total_charge1==0. and total_charge2==0.:
	print "Good, you have a neutral residue!"
elif total_charge1>0. or total_charge1<0. or total_charge2>0. or total_charge2<0.:
	print "WARNING: The total charge of the residue is\n"+str(round(total_charge1, 6))+" for state A\n"+str(round(total_charge2, 6))+" for state B"
else:
	print "ERROR: I have no charge there.."

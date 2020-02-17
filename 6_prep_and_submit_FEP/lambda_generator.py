#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015


# Importing necessary modules


import sys
from numpy import arange


# Defining and checking options and arguments

if len(sys.argv) == 1: # If no arguments
	sys.exit("ERROR: You need to specify at least the starting and final lambda values as arguments, use the [-h] option for help.")
elif len(sys.argv) == 2: # If one argument
	if str(sys.argv[1]) == "-h" : # Help
		sys.exit("Usage : lambda_generator.py <from> <to> <step_size> [option]\n-h : Usage")
	else : # Wrong argument case
		sys.exit("ERROR: Wrong argument, use the [-h] option for help.")
elif "-h" in sys.argv : # Help
	sys.exit("Usage : lambda_generator.py <from> <to> <step_size> [option]\n-h : Usage")
elif len(sys.argv) == 3: # Step size is 1 (as not specified)
	start = sys.argv[1]
	to = sys.argv[2]
	step_size = 1
elif len(sys.argv) == 4: # With specified step size
	start = sys.argv[1]
	to = sys.argv[2]
	if float(sys.argv[3]) < 0:
		sys.exit("ERROR: The specified step size must be positive ! You can inverse the starting and final values for getting the inversed list !")
	else:
		step_size = sys.argv[3]
elif len(sys.argv) > 4 : # If too many arguments
	sys.exit("ERROR: Too many arguments, use the [-h] option for help.")



# Defining useful functions


def lambda_listing(start, to, step_size) : # Generating the desired list of lambda values
	lambdas = []
	if float(to) > float(start):
		for l in arange(float(start),float(to)+float(step_size)-0.0001,float(step_size)):
			lambdas.append(round(l, 5))
	else:
		for l in arange(float(start),float(to),-float(step_size)):
			lambdas.append(round(l, 5))
		lambdas.append(0.0)
	return lambdas


# Running the program

fout=open('FEP.in', 'w')
for lambda_val in lambda_listing(start, to, step_size):
	print(lambda_val)
	fout.write(str(lambda_val)+'\n')

fout.close()

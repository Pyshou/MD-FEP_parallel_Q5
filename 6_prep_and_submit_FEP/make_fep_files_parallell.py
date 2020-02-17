#!/usr/bin/python2
# Jens & Anirudh 2012
# Make FEP input files

import string
import sys
from optparse import OptionParser

# Option parser
description = "Make FEP files for parallell run."
usage = "%prog [options]"
version = "%prog: version 2012 - created by Jens & Anirudh"
parser = OptionParser(usage=usage, description=description,version=version)
parser.add_option("-i", dest="filename",help='FEP lambda values')
(options,args) = parser.parse_args()

if options.filename == None:
	print "make_fep_files.py -h"
	exit(1)

# Read file with residue numbers
dc0 = open("dc0","r")
tmp = dc0.read()
dcfile = tmp.rstrip('\n')


# Read FEP steps
lambdas = []
FEPfile = open(options.filename,"r")
for line in FEPfile.readlines():
	lambdas.append(line.rstrip('\n'))

print lambdas

# Loop over all lambdas and make file
k = 1
for l in lambdas:
	FILE = open("dc"+str(k)+".inp","w")
	FILE.write(dcfile)
	FILE.write("\ntrajectory     dc"+str(k)+".dcd\n")
	FILE.write("restart        eq6.re\n")
	FILE.write("energy         dc"+str(k)+".en\n")
        FILE.write("final          dc"+str(k)+".re\n\n")
        
        FILE.write("[trajectory_atoms]\n")
        FILE.write("not excluded\n\n")	
        FILE.write("[lambdas]\n")
	i = 1-float(l)
	FILE.write(l+" "+str(i)+"\n")
	FILE.close()
	k = k+1

#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015


import sys, os
if len(sys.argv) != 2:
	sys.exit("ERROR: You must provide an input structure file as a unique argument!")
else:
	if os.path.exists(sys.argv[1])==False:
		sys.exit("ERROR: " + str(sys.argv[1]) + ", No such file!")

fin=open(sys.argv[1], 'r')
fout=open('output.pdb', 'w')

count=0
counter=1
resnb=1
for line in fin.readlines():
	if "HETATM" in line or "ATOM" in line:
		if count==0:
			res=line[17:20]+line[23:26]
			count+=1
		else:
			if res!=line[17:20]+line[23:26]:
				resnb+=1
				res=line[17:20]+line[23:26]
		if resnb < 10:
			fout.write(line[0:23]+'  '+str(resnb)+line[26:54]+'\n')
		elif resnb >= 10 and resnb < 100:
			fout.write(line[0:23]+' '+str(resnb)+line[26:54]+'\n')
		elif resnb >= 100 and resnb < 1000:
			fout.write(line[0:23]+str(resnb)+line[26:54]+'\n')
		elif resnb >= 1000 and resnb < 10000:
			fout.write(line[0:23]+str(resnb)+line[27:54]+'\n')
		elif resnb >= 10000 and resnb < 100000:
			fout.write(line[0:23]+str(resnb)+line[28:54]+'\n')
		elif resnb >= 100000 and resnb < 1000000:
			fout.write(line[0:23]+str(resnb)+line[29:54]+'\n')
	elif "GAP" in line or "TER" in line:
		fout.write("GAP\n")

print("Done, check 'output.pdb'!")

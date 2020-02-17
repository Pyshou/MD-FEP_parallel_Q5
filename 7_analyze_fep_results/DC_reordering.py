#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015



# Importing necessary modules


import sys, os, re
from math import *
from operator import itemgetter


# Checking stuff


if len(os.popen("ls dc*/dc*en*").read().split("\n")[:-1]) == 0:
	sys.exit("ERROR: There is no dc*/dc*en* file. Make sure you are in an appropriate folder!")


# Setting necessary variables and checking folders


def analyse_lambdas(): # Getting all lambda values in order
	data = {}
	lambdas=[]
	if os.path.isdir("New_lambdas"):
		tmp = os.popen('for file in $(ls dc*/dc*.inp New_lambdas/dc*/dc*inp); do echo $file; done').read()
	else:
		tmp = os.popen('for file in $(ls dc*/dc*.inp); do echo $file; done').read()
	files = tmp.split('\n')[:-1]
	for l in files:
		fin = open(str(l), 'r')
		a = 0
		for line in fin.readlines():
			if a == 1:
				data[str(float(re.split(' ', line)[0]))]=str(l)
				lambdas.append(str(float(re.split(' ', line)[0])))
			elif "[lambdas]" in line:
				a = 1
		fin.close()
	return data, sorted(lambdas)[::-1]

def reorder(): # re-ordering*
	os.system('mv input_files/FEP.in input_files/old_FEP.in')
	fout=open('input_files/FEP.in','w')
	os.system('mkdir TEMP')
	data = analyse_lambdas()[0]
	lambdas=analyse_lambdas()[1]
	count=0
	for lambda_value in lambdas:
		if lambda_value==lambdas[-1]:
			fout.write(str(float(lambda_value)))
		else:
			fout.write(str(float(lambda_value))+'\n')
		count+=1
		if "New_lambdas" in str(data[str(lambda_value)]):
			dc_file="New_lambdas/"+re.split(".inp", re.split("/", str(data[str(lambda_value)]))[-1])[-2]
		else:	
			dc_file=re.split(".inp", re.split("/", str(data[str(lambda_value)]))[-1])[-2]
		os.system('cp -r '+dc_file+' TEMP/dc'+str(count))
	if os.path.exists("New_lambdas/input_files/FEP.in"):
		os.system('cp New_lambdas/input_files/FEP.in input_files/FEP_new.in')
	if os.path.exists('qfep.out'):
		os.system('mv qfep.out qfep_unconverged.out')
	os.system('rm -Rf New_lambdas dc*; mv TEMP/* .; rmdir TEMP')
	os.system('for i in {1..'+str(len(lambdas))+'}; do mv dc$i/dc*inp dc$i/dc$i.inp; done')
	if len(os.popen("ls dc*/dc*en").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.en $folder/$folder.en; done')
	if len(os.popen("ls dc1/dc*en.gz").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.en.gz $folder/$folder.en.gz; done')
	if len(os.popen("ls dc*/dc*log").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.log $folder/$folder.log; done')
	if len(os.popen("ls dc1/dc*log.gz").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.log.gz $folder/$folder.log.gz; done')
	if len(os.popen("ls dc*/dc*re").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.re $folder/$folder.re; done')
	if len(os.popen("ls dc*/dc*dcd").read().split("\n")[:-1]) > 0:
		os.system('for folder in $(ls -d dc*); do mv $folder/dc*.dcd $folder/$folder.dcd; done')
	os.system('rm input_files/dc*inp; cp dc*/dc*inp input_files/')
	fout.close()
	return 0


# Running the program

reorder()

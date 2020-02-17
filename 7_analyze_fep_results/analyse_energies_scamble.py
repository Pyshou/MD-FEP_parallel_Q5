#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015



# Importing necessary modules


import sys, os, re, random
from math import *


# Setting necessary variables and checking folders


def_folder='/home/matricon/input_files/'
qfep_path='/home/matricon/software/Q5_Mauricio/bin/qfep5'

temp_temp = os.popen('pwd').read()
if len(re.findall('[0-9]+K', temp_temp)) >= 1:
	temp = re.findall('[0-9]+K', temp_temp)[0]
	inp_folder = str(def_folder) + str(temp) + '/'
else:
	inp_folder = str(def_folder) 

if os.path.exists(qfep_path) == False: # Checking the Qfep path
        sys.exit('ERROR: ' + qfep_path + ' does not exist ! You need to change qfep_path at the beginning of the script. It should be the location of your Qfep binary.')

if os.path.exists('md_step0/md_rs1/dc1') == False: # Checking whether in appropriate folder, folder tree and whether simulations are done (otherwise it would't work).
	sys.exit('ERROR: Are you running this script in an appropriate folder ? you should have md_step* folders in it, and md_rs* sub_folders containing energy files (dc*.en) in dc* folders')


# Defining useful functions


def prepare_energy_files() : # Doing the operations that are usually done by hand 
	steps_tmp = os.popen('for file in md_step*; do echo $file; done').read()
	steps = steps_tmp.split('\n')[:-1]
	step_data={}
	for step in steps: # Getting intermediate step data for each step and replica
		if step not in step_data:
			step_data[step]={}
		rs_tmp = os.popen('cd ' + step + '; for rs in md_rs*; do echo $rs; done').read()
		rss = rs_tmp.split('\n')[:-1]
		dcs=[]
		step_data[step]['dc']=[]
		for i in range(1, len(rs_tmp.split('\n')[:-1])+1):
			dcs.append(str(os.popen('ls ' + step + '/md_rs'+str(i)+'/dc*/dc*inp | wc -l').read().split('\n')[0]))
			step_data[step]['dc'].append(dcs)
	samples={}
	lambdas={}
	lambda_to_dc={}
	for step in steps: # Getting lambda values
		if step not in lambdas:
			lambdas[step]=[]
			lambda_to_dc[step]={}
		if step not in samples:
			samples[step]={}
		for rs in range(1, len(step_data[step]['dc'])+1):
			if str(rs) not in samples[step]:
				samples[step][str(rs)]=[]
				lambda_to_dc[step][str(rs)]={}
			for dc in range(1, int(step_data[step]['dc'][rs-1][0])+1):
				samples[step][str(rs)].append(re.findall('\d*\.?\d+', str(os.popen('grep -A1 "lambda" '+step+'/md_rs'+str(rs)+'/dc'+str(dc)+'/dc*.inp | tail -n 1 | awk "{print $1}"').read().split('\n')[0]))[0])
				lambda_to_dc[step][str(rs)][re.findall('\d*\.?\d+', str(os.popen('grep -A1 "lambda" '+step+'/md_rs'+str(rs)+'/dc'+str(dc)+'/dc*.inp | tail -n 1 | awk "{print $1}"').read().split('\n')[0]))[0]]=str(dc)
				if re.findall('\d*\.?\d+', str(os.popen('grep -A1 "lambda" '+step+'/md_rs'+str(rs)+'/dc'+str(dc)+'/dc*.inp | tail -n 1 | awk "{print $1}"').read().split('\n')[0]))[0] not in lambdas[step]:
					lambdas[step].append(re.findall('\d*\.?\d+', str(os.popen('grep -A1 "lambda" '+step+'/md_rs'+str(rs)+'/dc'+str(dc)+'/dc*.inp | tail -n 1 | awk "{print $1}"').read().split('\n')[0]))[0])
					lambdas[step]=sorted(lambdas[step])[::-1]
	i=0
	sampling={}
	while i<=1000: # Chosing samples
		i+=1
		sampling[str(i)]={}
		for step in steps:
			sampling[str(i)][step]={}
			for lambda_value in lambdas[step]:
				data=[]
				for rs in samples[step]:
					if lambda_value in samples[step][rs]:
						data.append(str(rs))
				sampling[str(i)][step][str(lambda_value)]=data[random.randint(0,len(data)-1)]
	i=1
	print "Analysing random sample of 1000 combinations of energy files:"
	dGs=[]
	while i<=1000:
		print "sample "+str(i)
		os.system('mkdir temp')
		for step in steps:
			os.system('mkdir temp/'+step)
			for lambda_value in lambdas[step]:
				os.system('cp '+step+'/md_rs'+sampling[str(i)][step][str(lambda_value)]+'/dc'+lambda_to_dc[step][str(rs)][lambda_value]+'/dc'+lambda_to_dc[step][str(rs)][lambda_value]+'.en temp/'+step)
			os.system('cd temp/'+step+'; '+qfep_path+' < '+inp_folder+'qfep'+str(len(sampling[str(i)][step]))+'.in > qfep.out')
		dGs.append(analyse_energies(steps))
		os.system('rm -Rf temp')
		i+=1
	mean=sum(dGs)/float(len(dGs))
	rss=[]
	for dG in dGs:
		rss.append((dG-mean)**2)
	std=sqrt((sum(rss))/(len(dGs)))
	fout=open('scramble_summary.csv', 'w')
	fout.write('mean,std\n')
	fout.write(str(round(mean,2))+','+str(round(std,2)))
	fout.close()
	fout=open('scramble_data.csv', 'w')
	fout.write(str(dGs))
	fout.close()
	print 'mean='+str(round(mean,2))+' +/- '+str(round(std, 2))+' kcal/mol'
	


def analyse_energies(steps):
#	energies = {}
	themean=0
	for step in steps:
#		energies[step] = {}
		qfepout=open('temp/'+step+'/qfep.out', 'r')
		a = 0
		for line in qfepout.readlines():
			if 'Free energy perturbation summary' in line:
				a = 1
			if a == 1:
#				if '1.000000' in line[3:11]:
#					reverse = float(re.findall('[-+]?\d*\.\d+', line)[4])
				if '0.000000' in line[3:11]:		
					mean = float(re.findall('[-+]?\d*\.\d+', line)[5])
#					forward = float(re.findall('[-+]?\d*\.\d+', line)[2])
					a = 0
					break
#		energies[step] = []
#		energies[step].append(mean)
#		energies[step].append(forward)
#		energies[step].append(reverse)
		themean+=mean
	return themean


# Running the program

prepare_energy_files()

print "Alright, this should be done ! You can now use analyse_scambled_data.py in the FEP folders, but make sure you modify the header for RECS! Works for 2 by default"

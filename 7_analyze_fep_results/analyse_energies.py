#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2015



# Importing necessary modules


import sys, os, re
from math import *


# Setting necessary variables and checking folders


Qfep_inp_folder='/home/matricon/input_files/'
qfep_path='/home/matricon/software/Q5_Mauricio/bin/qfep5'

temp_temp = os.popen('pwd').read()
if len(re.findall('[0-9]+K', temp_temp)) >= 1:
	temp = re.findall('[0-9]+K', temp_temp)[0]
	inp_folder = str(Qfep_inp_folder) +  str(temp) + '/'
else:
	inp_folder = str(Qfep_inp_folder) 

if os.path.exists(qfep_path) == False: # Checking the Qfep path
        sys.exit('ERROR: ' + qfep_path + ' does not exist ! You need to change qfep_path at the beginning of the script. It should be the location of your Qfep binary.')

if os.path.exists('md_step0/md_rs1/dc1') == False: # Checking whether in appropriate folder, folder tree and whether simulations are done (otherwise it would't work).
	sys.exit('ERROR: Are you running this script in an appropriate folder ? you should have md_step* folders in it, and md_rs* sub_folders containing energy files (dc*.en) in dc* folders')


# Defining useful functions


def prepare_energy_files() : # Doing the operations that are usually done by hand 
	steps_tmp = os.popen('for file in md_step*; do echo $file; done').read()
	steps = steps_tmp.split('\n')[:-1]
	for step in steps:
		rs_tmp = os.popen('cd ' + step + '; for rs in md_rs*; do echo $rs; done').read()
		dcs1 = os.popen('ls -d ' + step + '/md_rs1/dc*/ | wc -l').read()
		DCs1 = str(dcs1.split('\n')[0])
		dcs2 = os.popen('ls -d ' + step + '/md_rs2/dc*/ | wc -l').read()
		DCs2 = str(dcs2.split('\n')[0])
		dcs3 = os.popen('ls -d ' + step + '/md_rs3/dc*/ | wc -l').read()
		DCs3 = str(dcs3.split('\n')[0])
		rss = rs_tmp.split('\n')[:-1]
		if len(rss)>9:
			print "WARNING: If you have converged replicas independently, please update this script as it does not consider more than 3 otherwise!"
		counter = 0
		while counter < len(rss):# rs in rss:
			os.popen('cp ' + step + '/' + rss[counter] + '/dc*/dc*.en ' + step + '/' + rss[counter] + '/')
			if counter==0:
				if os.path.exists(inp_folder + 'qfep' + str(DCs1) + '.in'):
					command1 = 'cd ' + step + '/' + rss[counter] + '; ' + qfep_path + ' < ' + inp_folder + 'qfep' + str(DCs1) + '.in > qfep.out; rm dc*en; cd ../..'
				else:
					sys.exit("ERROR: "+inp_folder + "qfep" + str(DCs1) + ".in does not exist. Please edit it so that I can run Qfep with that number of steps!")
			elif counter==1:
				if os.path.exists(inp_folder + 'qfep' + str(DCs2) + '.in'):
					command1 = 'cd ' + step + '/' + rss[counter] + '; ' + qfep_path + ' < ' + inp_folder + 'qfep' + str(DCs2) + '.in > qfep.out; rm dc*en; cd ../..'
				else:
					sys.exit("ERROR: "+inp_folder + "qfep" + str(DCs2) + ".in does not exist. Please edit it so that I can run Qfep with that number of steps!")
			elif counter==2:
				if os.path.exists(inp_folder + 'qfep' + str(DCs3) + '.in'):
					command1 = 'cd ' + step + '/' + rss[counter] + '; ' + qfep_path + ' < ' + inp_folder + 'qfep' + str(DCs3) + '.in > qfep.out; rm dc*en; cd ../..'
				else:
					sys.exit("ERROR: "+inp_folder + "qfep" + str(DCs3) + ".in does not exist. Please edit it so that I can run Qfep with that number of steps!")
			else:
				command1 = 'cd ' + step + '/' + rss[counter] + '; ' + qfep_path + ' < ' + inp_folder + 'qfep' + str(DCs1) + '.in > qfep.out; rm dc*en; cd ../..'
			os.popen(command1)
			counter += 1
	return 0

def analyse_energies():
	energies = {}
	fout = open('FEP_analysis.csv', 'w')
	fout_full = open('full_data.csv', 'w')
	fout_full.write(',forward,reverse,mean,RS1,RS2,RS3,RS4,RS5,RS6\n')
	steps_tmp = os.popen('for file in md_step*; do echo $file; done').read()
	steps = steps_tmp.split('\n')[:-1]
	for step in steps:
		energies[step] = {}
		rs_tmp = os.popen('cd ' + step + '; for rs in md_rs*; do echo $rs; done').read()
		rss = rs_tmp.split('\n')[:-1]
		(reversel, meanl, forwardl) = ([], [], [])
		counter = 0
		while counter < len(rss):# rs in rss:
			fin_rss = open(step + '/' + rss[counter] + '/qfep.out', 'r')
			a = 0
			for line in fin_rss.readlines():
				if 'Free energy perturbation summary' in line:
					a = 1
				if a == 1:
					if '1.000000' in line[3:11]:
						reverse = float(re.findall('[-+]?\d*\.\d+', line)[4])
					elif '0.000000' in line[3:11]:
						
						mean = float(re.findall('[-+]?\d*\.\d+', line)[5])
						forward = float(re.findall('[-+]?\d*\.\d+', line)[2])
						a = 0
			fin_rss.close()
			energies[step][rss[counter]] = []
			energies[step][rss[counter]].append(mean)
			energies[step][rss[counter]].append(forward)
			energies[step][rss[counter]].append(reverse)
			counter += 1
	(delG, forward_delG, reverse_delG, rs1delG, rs2delG, rs3delG, rs4delG, rs5delG, rs6delG, rs7delG, rs8delG, rs9delG) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
	step_list=[]
	for step in energies:
		rs1delG += energies[step]['md_rs1'][0]
		counter2=0
		(delGX, forward_delGX, reverse_delGX)=(0,0,0)
		for replica in energies[step]:
			counter2+=1
			delGX += energies[step][replica][0]
			forward_delGX += energies[step][replica][1]
			reverse_delGX += energies[step][replica][2]
			if counter2==len(energies[step]):
				delG += delGX/float(counter2)
				forward_delG += forward_delGX/float(counter2)
				reverse_delG += reverse_delGX/float(counter2)
				step_list.append(str(step)[3:]+','+str(round(forward_delGX/float(counter2), 3))+','+str(round(reverse_delGX/float(counter2), 3))+','+str(round(delGX/float(counter2), 3))+',')
				for theRS in range(1,counter2+1):
					if theRS==counter2:
						step_list[-1]+=(str(round(energies[step]['md_rs'+str(theRS)][0], 3))+'\n')
					else:
						step_list[-1]+=(str(round(energies[step]['md_rs'+str(theRS)][0], 3))+',')
		if ('md_rs9') in energies[step]:
			rs2delG += energies[step]['md_rs2'][0]
			rs3delG += energies[step]['md_rs3'][0]
			rs4delG += energies[step]['md_rs4'][0]
			rs5delG += energies[step]['md_rs5'][0]
			rs6delG += energies[step]['md_rs6'][0]
			rs7delG += energies[step]['md_rs7'][0]
			rs8delG += energies[step]['md_rs8'][0]
			rs9delG += energies[step]['md_rs9'][0]
		elif 'md_rs6' in energies[step]:
			rs2delG += energies[step]['md_rs2'][0]
			rs3delG += energies[step]['md_rs3'][0]
			rs4delG += energies[step]['md_rs4'][0]
			rs5delG += energies[step]['md_rs5'][0]
			rs6delG += energies[step]['md_rs6'][0]
			rs7delG += energies[step]['md_rs6'][0]
			rs8delG += energies[step]['md_rs6'][0]
			rs9delG += energies[step]['md_rs6'][0]
		elif ('md_rs3') in energies[step] and ('md_rs6' and 'md_rs5' and
 'md_rs4') not in energies[step]:
			rs2delG += energies[step]['md_rs1'][0]
			rs3delG += energies[step]['md_rs1'][0]
			rs4delG += energies[step]['md_rs2'][0]
			rs5delG += energies[step]['md_rs2'][0]
			rs6delG += energies[step]['md_rs2'][0]
			rs7delG += energies[step]['md_rs3'][0]
			rs8delG += energies[step]['md_rs3'][0]
			rs9delG += energies[step]['md_rs3'][0]
		elif ('md_rs5') in energies[step] and ('md_rs6') not in energies[step]:
			rs2delG += energies[step]['md_rs2'][0]
			rs3delG += energies[step]['md_rs3'][0]
			rs4delG += energies[step]['md_rs4'][0]
			rs5delG += energies[step]['md_rs5'][0]
			rs6delG += energies[step]['md_rs5'][0]
			rs7delG += energies[step]['md_rs5'][0]
			rs8delG += energies[step]['md_rs5'][0]
			rs9delG += energies[step]['md_rs5'][0]
		elif ('md_rs4') in energies[step] and ('md_rs6' and 'md_rs5') not in energies[step]:
			rs2delG += energies[step]['md_rs2'][0]
			rs3delG += energies[step]['md_rs3'][0]
			rs4delG += energies[step]['md_rs4'][0]
			rs5delG += energies[step]['md_rs4'][0]
			rs6delG += energies[step]['md_rs4'][0]
			rs7delG += energies[step]['md_rs4'][0]
			rs8delG += energies[step]['md_rs4'][0]
			rs9delG += energies[step]['md_rs4'][0]
		elif ('md_rs2') in energies[step] and ('md_rs3') not in energies[step]:
			rs2delG += energies[step]['md_rs2'][0]
			rs3delG += energies[step]['md_rs2'][0]
			rs4delG += energies[step]['md_rs2'][0]
			rs5delG += energies[step]['md_rs2'][0]
			rs6delG += energies[step]['md_rs2'][0]
			rs7delG += energies[step]['md_rs2'][0]
			rs8delG += energies[step]['md_rs2'][0]
			rs9delG += energies[step]['md_rs2'][0]
		else:
			rs2delG += energies[step]['md_rs1'][0]
			rs3delG += energies[step]['md_rs1'][0]
			rs4delG += energies[step]['md_rs1'][0]
			rs5delG += energies[step]['md_rs1'][0]
			rs6delG += energies[step]['md_rs1'][0]
			rs7delG += energies[step]['md_rs1'][0]
			rs8delG += energies[step]['md_rs1'][0]
			rs9delG += energies[step]['md_rs1'][0]
	fout.write('delG (kcal.mol-1),Forward (kcal.mol-1),Reverse (kcal.mol-1),rs1delG (kcal.mol-1),rs2delG (kcal.mol-1),rs3delG (kcal.mol-1),rs4delG (kcal.mol-1),rs5delG (kcal.mol-1),rs6delG (kcal.mol-1),rs7delG (kcal.mol-1),rs8delG (kcal.mol-1),rs9delG (kcal.mol-1)\n' + str(round(delG, 2)) + ',' + str(round(forward_delG, 2)) + ',' + str(round(reverse_delG, 2)) + ',' + str(round(rs1delG, 2)) + ',' + str(round(rs2delG, 2)) + ',' + str(round(rs3delG, 2)) + ',' + str(round(rs4delG, 2)) + ',' + str(round(rs5delG, 2)) + ',' + str(round(rs6delG, 2)) + ',' + str(round(rs7delG, 2)) + ',' + str(round(rs8delG, 2)) + ',' + str(round(rs9delG, 2)) + '\n\n')
	for content in sorted(step_list):
		fout_full.write(content)
	fout.close()
	fout_full.close()
	return 0


# Running the program

prepare_energy_files()
analyse_energies()

print "Alright, this should be done !"

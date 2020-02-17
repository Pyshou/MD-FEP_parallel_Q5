#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By Pierre Matricon, 2018
import re
from math import *

fin1=open('REC/scramble_data.csv', 'r')
#fin2=open('REC_HID/scramble_data.csv', 'r')
finwat=open('WAT/scramble_data.csv', 'r')

data1=[]
#forwards1=[]
#reverses1=[]
for ele in re.split(',', str(fin1.readlines()[0])):
	data1.append(re.findall(r'-?\d+\.?\d*', ele)[0])
#	forwards1.append(float(re.findall(r'-?\d+\.?\d*', ele)[1]))
#	reverses1.append(float(re.findall(r'-?\d+\.?\d*', ele)[2]))
	
#data2=[]
#forwards2=[]
#reverses2=[]
#for ele in re.split(',', str(fin2.readlines()[0])):
#	data2.append(re.findall(r'-?\d+\.?\d*', ele)[0])
#       forwards2.append(float(re.findall(r'-?\d+\.?\d*', ele)[1]))
#       reverses2.append(float(re.findall(r'-?\d+\.?\d*', ele)[2]))

datawat=[]
#forwardswat=[]
#reverseswat=[]
for ele in re.split(',', str(finwat.readlines()[0])):
	datawat.append(re.findall(r'-?\d+\.?\d*', ele)[0])
#	forwardswat.append(float(re.findall(r'-?\d+\.?\d*', ele)[1]))
#	reverseswat.append(float(re.findall(r'-?\d+\.?\d*', ele)[2]))

dGs1=[]
#HYSs1=[]
for i in range (0,1000):
	dGs1.append(float(data1[i])-float(datawat[i]))
#	HYSs1.append((forwards1[i]+reverses1[i]-forwardswat[i]-reverseswat[i])/2.)

mean1=sum(dGs1)/float(len(dGs1))
#meanHYS1=sum(HYSs1)/float(len(HYSs1))

rss=0
for i in range(0,1000):
	rss+=(dGs1[i]-mean1)**2

std1=sqrt(rss/1000.)
#spread1=(max(dGs1)-min(dGs1))/2.

#dGs2=[]
#HYSs2=[]
#for i in range (0,1000):
#	dGs2.append(float(data2[i])-float(datawat[i]))
#       HYSs2.append((forwards2[i]+reverses2[i]-forwardswat[i]-reverseswat[i])/2.)

#mean2=sum(dGs2)/float(len(dGs2))
#meanHYS2=sum(HYSs2)/float(len(HYSs2))

#rss=0
#for i in range(0,1000):
#	rss+=(dGs2[i]-mean2)**2

#std2=sqrt(rss/1000.)
#spread2=(max(dGs2)-min(dGs2))/2.

print "ddG +/- std / meanHYS / mindGs - maxdGs:"
print "ddG = "+str(round(mean1, 2))+" +/- "+str(round(std1, 2))#+" / "+str(round(meanHYS1, 2))+" / "+str(round(min(dGs1), 2))+" - "+str(round(max(dGs1), 2))
#print "ddG(HID) = "+str(round(mean2, 2))+" +/- "+str(round(std2, 2))#+" / "+str(round(meanHYS2, 2))+" / "+str(round(min(dGs2), 2))+" - "+str(round(max(dGs2), 2))

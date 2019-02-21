#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:46:51 2017

@author: gbonnet
"""
from CyTOF_preprocessing import GateOnLiveSingletCells
import os
import numpy as np
import pickle


path= ###file path here
os.chdir(path)
temp=os.listdir(path)
ListOfFolders=[]
ListOfFiles=[]


for x in temp:
    if (x.find('.fcs')>0)|(x.find('.FCS')>0):
        ListOfFiles.append(x)

               
NumberOfFiles=np.shape(ListOfFiles)[0]
AllData={}

for fcsfilename in ListOfFiles:
   
    AllData[ListOfFiles.index(fcsfilename)]=GateOnLiveSingletCells(fcsfilename)

    
    
pickle.dump(AllData,open('AllData.pkl','wb'))
pickle.dump(ListOfFiles,open('ListOfFiles.pkl','wb'))

#%% Sanity check: all markers are identical across samples

marker=AllData[0].columns
Flag='False'
for df in AllData:
    if np.sum(AllData[df].columns==marker)<np.shape(marker)[0]:
        print('THESE FILES HAVE MISMATCHED LISTS OF MARKERS !')
        Flag='True'
        break


       

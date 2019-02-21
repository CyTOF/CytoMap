#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:09:56 2019

@author: jsanjak
"""
import pandas as pd
import subprocess
import re
import os
import sys



datasets = pd.read_csv("rnaseq-datasets.txt",header=None)
geo_ftp_base='ftp://ftp.ncbi.nlm.nih.gov/geo/samples/'

main_dir = os.getcwd()

if os.path.isdir("data/scRNAseq"):
    os.chdir("data/scRNAseq")
else:
    os.mkdir("data/scRNAseq")
    os.chdir("data/scRNAseq")

for index, ds in datasets.iterrows():
    
    if ds[0] == "scRNAseq":
        ds_ftp_url = geo_ftp_base + ds[1][:(len(ds[1])-3)]+'nnn/'+ ds[1] + '/' 
        
        #Make the data directories
        if os.path.isdir(ds[1]):
            os.chdir(ds[1])
        else:
            os.mkdir(ds[1])
            os.chdir(ds[1])
            
        args = ['wget', '--recursive','--no-parent', '--no-directories', ds_ftp_url]
        subprocess.call(args)
        os.chdir("..")



        
os.chdir(main_dir)
    




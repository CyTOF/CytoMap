#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:09:56 2019

@author: jsanjak
"""
import pandas as pd
import subprocess
import os


datasets = pd.read_csv("rnaseq-datasets.csv",header=None)

#All GEO data ftp links start with this base
geo_ftp_base='ftp://ftp.ncbi.nlm.nih.gov/geo/samples/'

#Useful to return home
main_dir = os.getcwd()

#Make the rna-seq directory
if not os.path.isdir("data/scRNAseq"):
    os.mkdir("data/scRNAseq")
os.chdir("data/scRNAseq")

#loop over datasets
for index, ds in datasets.iterrows():
    
    #GEO data ftp links go GSM##nnn/GSM#####/*
    ds_ftp_url = geo_ftp_base + ds[1][:(len(ds[1])-3)]+'nnn/'+ ds[1] + '/' 
    
    #Make the data directories based on how data are labeled in the input file
    if not os.path.isdir(ds[0]):
        os.mkdir(ds[0])
    os.chdir(ds[0])
    
    #if not os.path.isdir(ds[1]):
    #    os.mkdir(ds[1])
    #os.chdir(ds[1])
    
    #Use wget to obtain all data files under that GEO accession
    args = ['wget', '--recursive','--no-parent', '--no-directories', ds_ftp_url]
    subprocess.call(args)
    os.chdir("../")

#Return home
os.chdir(main_dir)
    




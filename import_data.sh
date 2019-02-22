#!/usr/bin/bash

#scRNA datasets from GEO
python import_geo_data.py

#CyTOF datasets from flow repo
Rscript import_flowrepo_data.R

#Tabula Muris data -- hard coded as this is unlikely to change
mkdir -p data/scRNAseq/TabulaMuris/facs
mkdir -p data/scRNAseq/TabulaMuris/droplet

curl https://ndownloader.figshare.com/articles/5829687/versions/4 > data/scRNAseq/TabulaMuris/facs/00_facs_raw_data.zip
curl https://ndownloader.figshare.com/articles/5968960/versions/1 > data/scRNAseq/TabulaMuris/droplet/01_droplet_raw_data.zip

unzip data/scRNAseq/TabulaMuris/facs/00_facs_raw_data.zip -d data/scRNAseq/TabulaMuris/facs/
unzip data/scRNAseq/TabulaMuris/facs/FACS.zip -d data/scRNAseq/TabulaMuris/facs/

unzip data/scRNAseq/TabulaMuris/droplet/01_droplet_raw_data.zip -d data/scRNAseq/TabulaMuris/droplet/
unzip data/scRNAseq/TabulaMuris/droplet/droplet.zip -d data/scRNAseq/TabulaMuris/droplet/

#Leave or remove zip files
#rm data/scRNAseq/TabulaMuris/facs/00_facs_raw_data.zip
#rm data/scRNAseq/TabulaMuris/droplet/01_droplet_raw_data.zip


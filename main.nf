#!/usr/bin/env nextflow

/*
========================================================================================
                  A U T O I M M U N O P H E N O T Y E  C Y T O F
========================================================================================
 CyTOF automated phenotyping pipeline. NIH February Hackathon 2019.
 #### Homepage / Documentation
 https://github.com/NCBI-Hackathons/Automatic-classification-of-CyTOF-measurements-to-generate-biomarkers-of-human-immunodeficiencies
 @#### Authors
 Brian Capaldo <brian.capaldo@gmail.com>
 Ratnadeep Mukherjee <ratnadeep.mukherjee@gmail.com>
 Wanhu Tang <tangw2@niaid.nih.gov>
 James Anibal <james.anibal@nih.gov>
 Gege Gui <gege.gui@nih.gov>
 Jaleal Sanjak <jsanjak@gryphonscientific.com>
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
Pipeline overview:
 - 1:   Data preprocessing 
 - 2:   Runs HAL-x on single cell data
 - 3:   Infer network of features
 - 4:   Maps HAL-x clusters from cytometry to scRNA seq
 - 5:   Assign immunophenotypes to cytomery data
 - 6:   Compare differences between experimental groups
 ----------------------------------------------------------------------------------------
*/

def helpMessage() {
    log.info"""
    =========================================
     NCBI-Hackathons/cytomaton : ChIP-Seq Best Practice v${params.version}
    =========================================
    Usage:
    The typical command for running the pipeline is as follows:
    nextflow run NCBI-Hackathon/cytomaton --cytof 'data/cytof' --scrna 'data/scRNAseq' -profile docker

    Mandatory arguments:
      --cytof                       Path to cytof data (must be surrounded with quotes).
      --scrna                       Path to scrna data
      --expconfig                   Configuration file that explains the experimental design 
      -profile                      Hardware config to use. uppmax / uppmax_modules / docker / aws

    """.stripIndent()
}

process prepare_cytof {

  input:

  output:
  
  script:


}

process prepare_scrna {

}

process halx_cytof {

}

process halx_scrna {
  
}

process infer_feature_bucket {

}

process map_cyto_scrna {

}

process assign_immunophenotype {

}

process experimental_analysis {

}
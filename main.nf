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
    nextflow run NCBI-Hackathon/cytomaton --cytof 'data/cytof/mice' --scrna 'data/scRNAseq/mice' -profile docker

    Mandatory arguments:
      --cytof                       Path to cytof data (must be surrounded with quotes).
      --scrna                       Path to scrna data
      --expconfig                   Configuration file that explains the experimental design 
      -profile                      Hardware config to use. uppmax / uppmax_modules / docker / aws

    """.stripIndent()
}

cytof_raw = Channel.fromPath( params.cytof + "/*" )
scrna_raw = Channel.fromPath( params.scrna + "/*")


process prepare_cytof {

  input:
    file cytof_file from cytof_raw

  output:
    file '*.proc' into cytof_proc

  script:
    """
    touch '${cytof_file}.proc'
    """


}

process prepare_scrna {


  input:
    file scrna_file from scrna_raw

  output:
    file '*.proc' into scrna_proc

  script:
    """
    touch '${scrna_file}.proc'
    """

}

process halx_cytof {

  input:
    file cytof_all_proc from cytof_proc.collect()

  output:
    file "cytof.halx" into cytof_halx

  script:
    """
    touch cytof.halx
    """

}

process halx_scrna {
  
  input:
    file scrna_all_proc from scrna_proc.collect()

  output:
    file "scrna.halx" into scrna_halx

  script:
    """
    touch scrna.halx
    """
}

process infer_feature_bucket {

  input:
    file scrna_halx
    file cytof_halx
  
  output:
    file "cluster_features.txt" into feature_bucket

  script:
    """
    touch cluster_features.txt
    """
}

process map_cyto_scrna {

  input:
    file scrna_halx
    file cytof_halx
    file feature_bucket

  output:
    file "cyto_rna_map.txt" into cyto_rna_map

  script:     
    """
    touch cyto_rna_map.txt
    """
}

process assign_immunophenotype {

"""
echo "assign immunophenotype"
"""

}

process experimental_analysis {
"""
echo "experimental analysis"
"""
}
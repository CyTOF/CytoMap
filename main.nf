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
 - 3:   Differential Abundance and Expression analysis
 - 4:   Construct feature buckets
 - 5:   Map feature buckets
 - 6:   Visualize results
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

scrna_all_proc = scrna_proc.collect()
cytof_all_proc = cytof_proc.collect()

process halx_cytof {

  input:
    file cytof_all from cytof_all_proc

  output:
    file "cytof.halx" into cytof_halx

  script:
    """
    touch cytof.halx
    """

}

process halx_scrna {
  
  input:
    file scrna_all from scrna_all_proc

  output:
    file "scrna.halx" into scrna_halx

  script:
    """
    touch scrna.halx
    """
}

process diff_AE_scrna {
  
  input:
    file scrna_all from scrna_all_proc

  output:
    file "scrna.diff" into scrna_diff_AE

  script:
    """
    touch scrna.diff
    """
}

process diff_AE_cytof {
  
  input:
    file ctyof_all from cytof_all_proc

  output:
    file "cytof.diff" into cytof_diff_AE

  script:
    """
    touch cytof.diff
    """
}



process scrna_feature_bucket {

  input:
    file scrna_halx
    file scrna_diff_AE
  
  output:
    file "scrna_bucket.txt" into scrna_bucket

  script:
    """
    touch scrna_bucket.txt
    """
}

process cytof_feature_bucket {

  input:
    file cytof_halx
    file cytof_diff_AE
  
  output:
    file "cytof_bucket.txt" into cytof_bucket

  script:
    """
    touch cytof_bucket.txt
    """
}

process map_cytof_scrna {

  input:
    file cytof_bucket
    file scrna_bucket

  output:
    file "cytof_rna_map.txt" into cytof_rna_map

  script:     
    """
    touch cytof_rna_map.txt
    """
}

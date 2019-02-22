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
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
Pipeline overview:
 - 1:   Runs HAL-x on single cell data
 - 2:   Maps HAL-x clusters from cytometry to scRNA seq
 - 3:   Compare differences between experimental groups
 ----------------------------------------------------------------------------------------
*/

def helpMessage() {
    log.info"""
    =========================================
     nf-core/chipseq : ChIP-Seq Best Practice v${params.version}
    =========================================
    Usage:
    The typical command for running the pipeline is as follows:
    nextflow run nf-core/chipseq --reads '*_R{1,2}.fastq.gz' --genome GRCh37 --macsconfig 'macssetup.config' -profile uppmax
    Mandatory arguments:
      --reads                       Path to input data (must be surrounded with quotes).
      --genome                      Name of iGenomes reference
      --macsconfig                  Configuration file for peaking calling using MACS. Format: ChIPSampleID,CtrlSampleID,AnalysisID
      -profile                      Hardware config to use. uppmax / uppmax_modules / docker / aws
    Options:
      --singleEnd                   Specifies that the input is single end reads
      --allow_multi_align           Secondary alignments and unmapped reads are also reported in addition to primary alignments
      --saturation                  Run saturation analysis by peak calling with subsets of reads
      --broad                       Run MACS with the --broad flag
      --blacklist_filtering         Filter ENCODE blacklisted regions from ChIP-seq peaks. It only works when --genome is set as GRCh37 or GRCm38
    Presets:
      --extendReadsLen [int]        Number of base pairs to extend the reads for the deepTools analysis. Default: 100
    References
      --fasta                       Path to Fasta reference
      --bwa_index                   Path to BWA index
      --gtf                         Path to GTF file (Ensembl format)
      --blacklist                   Path to blacklist regions (.BED format), used for filtering out called peaks. Note that --blacklist_filtering is required
      --saveReference               Save the generated reference files in the Results directory.
      --saveAlignedIntermediates    Save the intermediate BAM files from the Alignment step  - not done by default
    Trimming options
      --notrim                      Specifying --notrim will skip the adapter trimming step.
      --saveTrimmed                 Save the trimmed Fastq files in the the Results directory.
      --clip_r1 [int]               Instructs Trim Galore to remove bp from the 5' end of read 1 (or single-end reads)
      --clip_r2 [int]               Instructs Trim Galore to remove bp from the 5' end of read 2 (paired-end reads only)
      --three_prime_clip_r1 [int]   Instructs Trim Galore to remove bp from the 3' end of read 1 AFTER adapter/quality trimming has been performed
      --three_prime_clip_r2 [int]   Instructs Trim Galore to re move bp from the 3' end of read 2 AFTER adapter/quality trimming has been performed
    Other options:
      --outdir                      The output directory where the results will be saved
      --email                       Set this parameter to your e-mail address to get a summary e-mail with details of the run sent to you when the workflow exits
      --rlocation                   Location to save R-libraries used in the pipeline. Default value is ~/R/nxtflow_libs/
      --clusterOptions              Extra SLURM options, used in conjunction with Uppmax.config
      -name                         Name for the pipeline run. If not specified, Nextflow will automatically generate a random mnemonic
    """.stripIndent()
}
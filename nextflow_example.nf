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
 - 1:   Runs HAL-x on single cell data
 - 2:   Maps HAL-x clusters from cytometry to scRNA seq
 - 3:   Assign immunophenotypes to cytomery data
 - 4:   Compare differences between experimental groups
 ----------------------------------------------------------------------------------------
*/

def helpMessage() {
    log.info"""
    =========================================
     NCBI-Hackathons/cytomaton : ChIP-Seq Best Practice v${params.version}
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


process bwa {
    tag "$prefix"
    publishDir path: { params.saveAlignedIntermediates ? "${params.outdir}/bwa" : params.outdir }, mode: 'copy',
               saveAs: {filename -> params.saveAlignedIntermediates ? filename : null }

    input:
    file reads from trimmed_reads
    file index from bwa_index.first()

    output:
    file '*.bam' into bwa_bam

    script:
    prefix = reads[0].toString() - ~/(.R1)?(_1)?(_R1)?(_trimmed)?(_val_1)?(\.fq)?(\.fastq)?(\.gz)?$/
    filtering = params.allow_multi_align ? '' : "| samtools view -b -q 1 -F 4 -F 256"
    """
    bwa mem -M ${index}/genome.fa $reads | samtools view -bT $index - $filtering > ${prefix}.bam
    """
}

process picard {
    tag "$prefix"
    publishDir "${params.outdir}/picard", mode: 'copy'

    input:
    file bam from bam_picard

    output:
    file '*.dedup.sorted.bam' into bam_dedup_spp, bam_dedup_ngsplot, bam_dedup_deepTools, bam_dedup_macs, bam_dedup_saturation
    file '*.dedup.sorted.bam.bai' into bai_dedup_deepTools, bai_dedup_ngsplot, bai_dedup_macs, bai_dedup_saturation
    file '*.dedup.sorted.bed' into bed_dedup
    file '*.picardDupMetrics.txt' into picard_reports

    script:
    prefix = bam[0].toString() - ~/(\.sorted)?(\.bam)?$/

    """
        java -Xmx10g -XX:ParallelGCThreads=5 -jar \$PICARDJARPATH/picard.jar MarkDuplicates \\
        INPUT=$bam \\
        OUTPUT=${prefix}.dedup.bam \\
        ASSUME_SORTED=true \\
        REMOVE_DUPLICATES=true \\
        METRICS_FILE=${prefix}.picardDupMetrics.txt \\
        VALIDATION_STRINGENCY=LENIENT \\
        PROGRAM_RECORD_ID='null'
    samtools sort ${prefix}.dedup.bam -o ${prefix}.dedup.sorted.bam
    samtools index ${prefix}.dedup.sorted.bam
    bedtools bamtobed -i ${prefix}.dedup.sorted.bam | sort -k 1,1 -k 2,2n -k 3,3n -k 6,6 > ${prefix}.dedup.sorted.bed
    """
}

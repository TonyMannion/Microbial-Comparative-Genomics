# Microbial-Comparative-Genomics
Python 2.7 scripts for analyzing and comparing microbial genomes.

full_genome_analysis.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes.  This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously.
The workflow and outputs are the following:
1) upload sequencing reads (fastq files) --> data store in PATRIC account 
2) perform quality control of raw reads --> outputs FASTQC analysis
3) perform de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4) perform DIAMOND analysis for virulence factor genes and antibiotic resistance genes --> outputs annotation table with hits

pan-genome-tree.py

This script creates pan-genome phylogenetic trees using IQ-TREE (http://www.iqtree.org/) based on a binary matrix of Global protein family (cross-genus, called PGfam) determined by PATRIC (https://www.patricbrc.org/).



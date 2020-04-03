# Microbial-Comparative-Genomics
Python 2.7 scripts for analyzing and comparing microbial genomes.

full_genome_analysis.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes.  This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously.
The workflow and outputs are the following:
1) upload sequencing reads (fastq files) --> data store in PATRIC account 
2) perform quality control of raw reads --> outputs FASTQC analysis
3) perform de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4) perform DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

pan-genome-tree.py

This script creates pan-genome phylogenetic trees using IQ-TREE (http://www.iqtree.org/) based on a binary matrix of Global protein family (ie PGfam) determined by PATRIC (https://www.patricbrc.org/).

The workflow and outputs are the following:
1) via PATRIC (https://www.patricbrc.org/), compile list of genome ids desired for pan-genome phylogenetic tree
2) acuqires Global protein family (ie PGfam) from genomes 
3) creates binary matrix of PGfam in PHYLIP format 
4) executes IQ-TREE to analyze to pan-genome phylogenetic tree --> outputs .treefile files, which can be viewed in FigTree (http://tree.bio.ed.ac.uk/software/figtree/) or similar programs

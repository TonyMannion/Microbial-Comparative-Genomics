# Microbial-Comparative-Genomics
Python 2.7 scripts for analyzing and comparing microbial genomes.

full_genome_analysis.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes AND/OR microbial genomes that are already assembled as contigs.  This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously.
The workflow and outputs are the following:
1) upload sequencing reads (fastq files) AND/OR assembled genome contigs (fasta files) --> data stored in PATRIC account 
2) perform quality control of raw reads --> outputs FASTQC analysis
3) perform de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4) perform DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

full_genome_analysis_reads.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes.  This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously.
The workflow and outputs are the following:
1) upload sequencing reads (fastq files) --> data store in PATRIC account 
2) perform quality control of raw reads --> outputs FASTQC analysis
3) perform de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4) perform DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

full_genome_analysis_contigs.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes that are already assembled as contigs.  This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously.
The workflow and outputs are the following:
1) upload assembled genome contig (fasta files) --> data store in PATRIC account 
2) perform annotation --> outputs summary statistics for annotated genomes as well as fasta files for contigs and annotated gene sequences
3) perform DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits


pan-genome-tree.py

This script creates pan-genome phylogenetic trees using IQ-TREE (http://www.iqtree.org/) based on a binary matrix of Global protein family (ie PGfam) determined by PATRIC (https://www.patricbrc.org/).

The workflow and outputs are the following:
1) via PATRIC (https://www.patricbrc.org/), compile list of genome ids desired for pan-genome phylogenetic tree
2) acquires Global protein family (ie PGfam) from genomes 
3) creates binary matrix of PGfam in PHYLIP format 
4) executes IQ-TREE to analyze to pan-genome phylogenetic tree --> outputs .treefile files, which can be viewed in FigTree (http://tree.bio.ed.ac.uk/software/figtree/) or similar programs

pgfam_median_counter.py

This script calculates the median number PGfam genes for a set of genomes in order to facilitate the identification of unique and core genes as well as over/under abundant gene copies.  This script may enable identitication of PGfam genes that differentiate species/strains from each other based on output of pan-genome-tree.py script (above). 

The workflow and outputs are the following:
1) merges annotations data outputted by full_genome_analysis.py scripts (above) from genomes of interest
2) performs groupby operation to calculate number of PGfam genes per genome
3) calculates median PGfam genes from all genomes of interest
4) per genome, outputs annotation data indicating number of PGfam genes and if PGfams genes are equal to, greater than, or less than median

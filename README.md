# Microbial-Comparative-Genomics

## Overview
These are series of Python 2.7 scripts aimed to facilitate and improve the comparative analysis of bacterial genomes.
These scripts enable genome assembly and gene annotation from raw sequencing reads followed by comparative analyses to understand the similarities and difference between a group of bacterial genomes of interest.
These scripts take advantage of the curated database of publicly accessible bacterial genomes and services hosted by [Pathosystems Resource Integration Center (PATRIC)](https://www.patricbrc.org/).  
Users of these scripts will require a [PATRIC](https://www.patricbrc.org/) account to take advantage of their features.

Often, researchers require assembly and annotation of more than one genome for their projects.
There are many steps involved from processing raw reads of adaptor sequences or low quality base pairs, assembling reads into contigs, and finally gene annotation.
Thus, processing each genome one-by-one can be cumbersome, time consuming, and error prone.
The **genome_assembly_annotate.py** script overcomes these challenges employing the [Comprehensive Genome Analysis Service](https://docs.patricbrc.org/user_guides/services/comprehensive_genome_analysis_service.html) hosted by [PATRIC](https://www.patricbrc.org/) in order to automate the assembly and annotation workflow, thereby increasing throughput when numerous genomes must be processed.
Additionally, the **genome_assembly_annotate.py** accepts pair-end reads (fastq) or pre-assembled contigs (fasta), which provides flexibility.
Pair-end reads (fastq) or pre-assembled contigs (fasta) data for numerous genomes can be piped into **genome_assembly_annotate.py** by including the appropriate metadata.
The output of **genome_assembly_annotate.py** is a full-genome report summarizing the genome assemlby and annotation characteristics, assemlbed genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata.

Furthermore, the **patric_genome_dl.py** script provided in this library allows researchers to access and downlaod bacterial genomes maintained in the PATRIC database.  Specifically, **patric_genome_dl.py** allows reserachers to acquires dassemlbed genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata from numerous genomes quickly.

Comparative genomics involves the identification of genetic factors, namely genes, that are shared or differ between bacteria genra, species, and/or strains.
The **genome_analysis.py** script facilitates the identification of genes and gene families that differentiate bacterial genomes.  This script execute six analysis workflows, which are summarized below.

## *genome_assembly_annotate.py*

The **genome_assembly_annotate.py** script allows the assembley and anntoation from raw sequenicng reads and/or pre-assembled contigs of multiple genomes simultanesouly.

## *patric_genomes_dl.py*

For genomes that have already been deposited in PATRIC, the **patric_genomes_dl.py** enables rapid acqusition of genomic data from multiple genomes.

## *genome_analysis.py*

The **genome_analysis.py** script performs six different analyses that faciliate the identicaiton comparision of genomes.


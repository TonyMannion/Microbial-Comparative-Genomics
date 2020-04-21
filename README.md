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

Comparative genomics involves the identification of genetic factors, namely genes, that are shared or differ between bacteria genra, species, and/or strains.
The scripts included in this compendium facilitate the identification of genes and gene families that differentiate bacterial genomes.


## *genome_assembly_annotate.py*
![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/genome_assembly_annotate_outline.png)

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes AND/OR microbial genomes that are already assembled as contigs. This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously. The workflow and outputs are the following:
1.	Uploads sequencing reads (fastq files) AND/OR assembled genome contigs (fasta files) --> data stored in PATRIC account
2.	Performs quality control of raw reads --> outputs FASTQC analysis
3.	Performs de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4.	Performs DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

### pan-genome-tree.py

This script creates pan-genome phylogenetic trees using IQ-TREE (http://www.iqtree.org/) based on a binary matrix of Global protein family (ie PGfam) determined by PATRIC (https://www.patricbrc.org/).
The workflow and outputs are the following:
1.	Via PATRIC (https://www.patricbrc.org/), compile list of genome ids desired for pan-genome phylogenetic tree
2.	Acquires Global protein family (ie PGfam) from genomes
3.	Creates binary matrix of PGfam in PHYLIP format
4.	Executes IQ-TREE to analyze to pan-genome phylogenetic tree --> outputs .treefile files, which can be viewed in FigTree (http://tree.bio.ed.ac.uk/software/figtree/) or similar programs

gene_family_analysis.py

This script calculates which gene families (eg PGfam) in a genome are equal, overly, or under abundant based on the median number of genes present in gene families within a set of genomes. This script also generates a clustermap (ie heatmap with cluster analysis) of the abundance and relationship of gene familes within the set of genomes.  When used in conjunction with the pan-genome-tree.py (above), the analysis by this script enables identification of gene families that differentiate species/strains from each other, such as core and accessory genes from the pangenome.
The workflow and outputs are the following:
1.	Input annotation data from a group of genomes of interest. Annotation data can be obtained by: 
i) the annotation.txt output by the full_genome_analysis.py scripts (above); 
ii) the gene family feature output downloaded from PATRIC by the pan-genome-tree.py script (above); and 
iii) the gene family feature output downloaded from PATRIC by this script (ie gene_family_analysis.py)
2.	Calculates the median genes per gene family in the set of genomes, the number of genes per gene family (eg PGfam) for each genome, and if the number of genes per gene family for each genomes is equal to, greater than, or less than median
3.	Output gene counts are merged to annotation metadata** (eg gene name, location on contig, sequence etc).
4.  Output clustermap (ie heatmap with cluster analysis) of gene familes within the set of genomes
5.  Output associated clustermap dataframe with genomes and gene families reordered per hierarchical clustering

**Note: Annotation metadata is more comprehensive when annotation.txt data (obtained using the full_genome_analysis.py scripts) are used as the input versus gene family feature data (obtained using gene_family_analysis.py or pan-genome-tree.py script). 

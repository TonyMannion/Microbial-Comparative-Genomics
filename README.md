# Microbial-Comparative-Genomics
Python 2.7 scripts for analyzing and comparing microbial genomes.

full_genome_analysis.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes AND/OR microbial genomes that are already assembled as contigs. This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously. The workflow and outputs are the following:
1.	Uploads sequencing reads (fastq files) AND/OR assembled genome contigs (fasta files) --> data stored in PATRIC account
2.	Performs quality control of raw reads --> outputs FASTQC analysis
3.	Performs de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4.	Performs DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

full_genome_analysis_reads.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes from raw sequencing data to assembled and annotated genomes. This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously. The workflow and outputs are the following:
1.	Uploads sequencing reads (fastq files) --> data store in PATRIC account
2.	Performs quality control of raw reads --> outputs FASTQC analysis
3.	Performs de novo assembly and annotation --> outputs summary statistics for assembled and annotated genomes as well as fasta files for contigs and annotated gene sequences
4.	Performs DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

full_genome_analysis_contigs.py

This script utilizes services hosted by PATRIC (https://www.patricbrc.org/) to process microbial genomes that are already assembled as contigs. This script enables batch genome processing and useful for users desiring to efficiently process and analyze multiple genomes simultaneously. The workflow and outputs are the following:
1.	Uploads assembled genome contig (fasta files) --> data store in PATRIC account
2.	Performs annotation --> outputs summary statistics for annotated genomes as well as fasta files for contigs and annotated gene sequences
3.	Performs DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download) --> outputs annotation table with hits

pan-genome-tree.py

This script creates pan-genome phylogenetic trees using IQ-TREE (http://www.iqtree.org/) based on a binary matrix of Global protein family (ie PGfam) determined by PATRIC (https://www.patricbrc.org/).
The workflow and outputs are the following:
1.	Via PATRIC (https://www.patricbrc.org/), compile list of genome ids desired for pan-genome phylogenetic tree
2.	Acquires Global protein family (ie PGfam) from genomes
3.	Creates binary matrix of PGfam in PHYLIP format
4.	Executes IQ-TREE to analyze to pan-genome phylogenetic tree --> outputs .treefile files, which can be viewed in FigTree (http://tree.bio.ed.ac.uk/software/figtree/) or similar programs

gene_family_count_analysis.py

This script calculates which gene families (eg PGfam) in a genome are equal, overly, or under abundant based on the median number of genes present in gene families within a set of genomes. This script also generates a clustermap (ie heatmap with cluster analysis) of the abundance and relationship of gene familes within the set of genomes.  When used in conjunction with the pan-genome-tree.py (above), the analysis by this script enables identification of gene families that differentiate species/strains from each other, such as core and accessory genes from the pangenome.
The workflow and outputs are the following:
1.	Input annotation data from a group of genomes of interest. Annotation data can be obtained by: i) the annotation.txt output by the full_genome_analysis.py scripts (above) ii) the gene family feature output downloaded from PATRIC by the pan-genome-tree.py script (above) iii) the gene family feature output downloaded from PATRIC by this script (ie gene_family_count_analysis.py)
2.	Calculates the median genes per gene family in the set of genomes, the number of genes per gene family (eg PGfam) for each genome, and if the number of genes per gene family for each genomes is equal to, greater than, or less than median
3.	Output gene counts are merged to annotation metadata** (eg gene name, location on contig, sequence etc).
4.  Output clustermap (ie heatmap with cluster analysis) of gene familes within the set of genomes 

**Note: Annotation metadata is more comprehensive when annotation.txt data (obtained using the full_genome_analysis.py scripts) are used as the input versus gene family feature data (obtained using gene_family_count_analysis.py or pan-genome-tree.py script). 

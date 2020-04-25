# Microbial-Comparative-Genomics

## Overview
These are series of Python 2.7 scripts aimed to facilitate and improve the comparative analysis of bacterial genomes.
These scripts enable genome assembly and gene annotation from raw sequencing reads followed by comparative analyses to understand the similarities and difference between a group of bacterial genomes of interest.
These scripts take advantage of the curated database of publicly accessible bacterial genomes and services hosted by [Pathosystems Resource Integration Center (PATRIC)](https://www.patricbrc.org/). Users of these scripts will require a [PATRIC](https://www.patricbrc.org/) account and must use the [PATRIC Command Line Interface](https://docs.patricbrc.org/cli_tutorial/).

Often, researchers require assembly and annotation of more than one genome for their projects.
There are many steps involved from processing raw reads of adaptor sequences or low quality base pairs, assembling reads into contigs, and finally gene annotation.
Thus, processing each genome one-by-one can be cumbersome, time consuming, and error prone.
The **get_genome_data.py** script overcomes these challenges employing the [Comprehensive Genome Analysis Service](https://docs.patricbrc.org/user_guides/services/comprehensive_genome_analysis_service.html) hosted by [PATRIC](https://www.patricbrc.org/) in order to automate the assembly and annotation workflow, thereby increasing throughput when numerous genomes must be processed.
Additionally, the **get_genome_data.py** accepts pair-end reads (fastq) or pre-assembled contigs (fasta), which provides flexibility.
Pair-end reads (fastq) or pre-assembled contigs (fasta) data for numerous genomes can be piped into **get_genome_data.py** by including the appropriate metadata.
The output of **get_genome_data.py** is a full-genome report summarizing the genome assemlby and annotation characteristics, assemlbed genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata.

Furthermore, the **get_genome_data.py** script provided in this library allows researchers to access and download bacterial genomes maintained in the PATRIC database.  Specifically, **get_genome_data.py** allows reserachers to acquire assemlbed genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata from numerous genomes quickly.

Comparative genomics involves the identification of genetic factors, namely genes, that are shared or differ between bacteria genra, species, and/or strains.
The **genome_analysis.py** script facilitates the identification of genes and gene families that differentiate bacterial genomes.  This script execute six analysis workflows, which are summarized below.

**Overview of Workflow**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/overview.PNG)

## *get_genome_data.py*

**Workflow of *get_genome_data.py***

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/get_genome_data_1.PNG)

The **genome_assembly_annotate.py** script allows the assembley and anntoation from raw sequenicng reads and/or pre-assembled contigs of multiple genomes simultanesouly.

**flags**
|	Flag	|	Flag (verbose)	|	Description	|
|	-----	|	-----	|	-----	|
|	 -h	|	 --help            	|	Show all flags and descriptions	|
|	 -u	|	 --username	|	Provide username for PATRIC account. Prompt to enter password will appear.	|
|	 -m	|	 --metadata_file	|	Specify metadata file.	|
|	 -f	|	 --file_upload	|	Upload read and/or contig files? Enter "yes" or "no". Default is "yes". If file with same name has already been uploaded to PATRIC, it will be overwritten by the newly uploaded file.	|
|	 -a	|	 --assembly_annotate	|	Execute assembly and annotate pipeline? Enter "yes" or "no". Default is "yes".	|
|	 -c	|	 --check_job	|	Check status of assembly/annotation job? Enter "yes" or "no". Default is "yes".  When job is complete, genome reports, contigs, and annotations data will be downloaded to output folder.	|
|	 -d	|	 --download_data	|	Download genome reports, contigs, and annotations data for assembled/annotated genomes from previously completed jobs to output folder? Enter "yes" or "no". Default is "no".	|
|	 -p	|	 --patric_download	|	Download genome reports, contigs, and annotations data from PATRIC genomes.	|
|	 -o	|	 --output_folder	|	Specify output folder for downloaded data.	|

## Output
**FullGenomeReport.html** - Summarizes genome assembly and gene annotation results.  See below for excerpt data from FullGenomeReport.html output of *Escherichia coli* str. K-12 substr. MG1655 (genome id: 511145.12) pre-assembled contigs annotated using this script.

**Summary of genome assembly and annotation results from FullGenomeReport.html for *E. coli* K12.**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/FullGenomeReport_K12_assembly_annotation.png)

**Circular chromosome showing gene annotations and subsystems from FullGenomeReport.html for *E. coli* K12.**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/FullGenomeReport_K12_chromosome_and_subsystems.png)

## *genome_analysis.py*

**Workflow of *genome_analysis.py***
![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/genome_analysis_1.png)

The **genome_analysis.py** script performs six different analyses that faciliate the identicaiton comparision of genomes.


**flags**
|	Flag	|	Flag (verbose)	|	Description	|
|	-----	|	-----	|	-----	|
|	 -h	|	 --help            	|	Show all flags and descriptions	|
|	 -i	|	 --input_folder	|	Specify folder with annotation data.	|
|	 -o	|	 --output_folder	|	Specify name for output folder.	|
|	 -m	|	 --metadata_file	|	Specify metadata file.	|
|	 -make_tree	|	 --make_tree	|	Generate binary matrix of protein families in PHYLIP format for pan-genome phylogenetic tree? Enter "yes" or "no". Default is "yes".	|
|	 -make_clustermap	|	 --make_clustermap	|	Create hierarchically-clustered heatmap (ie clustermap) of protein families in pan-genome? Enter "yes" or "no". Default is "yes".	|
|	 -core_unique_genes	|	 --core_unique_genes	|	Determine core and unique protein family genes for genome group? Enter "yes" or "no". Default is "yes".	|
|	 -median_analysis	|	 --median_analysis	|	Calculate median protein family gene copy number in genome group and if protein family genes for individual genomes are equal to, greater than, or less than median? Enter "yes" or "no". Default is "yes".	|
|	 -subgroup_genes	|	 --subgroup_genes	|	Determine unique protein family genes for genome subgroup within the larger genome group? Enter "yes" or "no". Default is "yes".	|
|	 -VF_blast	|	 --VF_blast	|	Perform DIAMOND blast analysis for virulence factor genes? Enter "yes" or "no". Default is "yes".	|
|	 -res_blast	|	 --res_blast	|	Perform DIAMOND blast analysis for antibiotic resistence genes? Enter "yes" or "no". Default is "yes".	|
|	 -custom_blast	|	 --custom_blast	|	Perform DIAMOND blast analysis for custom gene database? Enter "yes" or "no". Default is "no".	|
|	 -custom_fasta	|	 --custom_fasta	|	Provide custom gene database as multi-sequence fasta file using amino acids.	|


# Example 

*E. coli* commensal intestinal bacterial found in many species including humans and other mammalian species.  Some *E. coli* strains encode virulence factor genes that allow make them pathogenic.  One virulence factor gene expressed by some *E. coli* strains is colibactin, a genotoxin produced by *pks* gene island, and these strains are associated with UTI, meningitis, and colon cancer in humans and animal models.  In this example, the *get_genome_data.py* and *genome_analysis.py* scripts are used to compare genomes of human and rodent *E. coli* strains that do and do not encode the *pks* gene island.

Here, *get_genome_data.py* will be used to assembly and annotate six user genomes.  Pre-assembled contigs from five *E. coli* strains isolated from lab mice ([Mannion A. et al. *Genome Announc.* 2016.](https://mra.asm.org/content/4/5/e01082-16)) and Illumina MiSeq 2x250 bp reads from one *E. coli* strain isolated from pet rat ([Fabian NJ. et al. *Vet Microbiol.* 2020.]( https://www.sciencedirect.com/science/article/pii/S0378113519303669?via%3Dihub)).  The sequencing reads (fastq files) and pre-assembled contigs (fasta files) along with their corresponding genome names are recorded in the metadata table shown below.

To complement our genome group, data from four reference *E. coli* genomes will be acquired from PATRIC using *get_genome_data.py*.  These genomes will include: 
- *E. coli* K12: non-pathogenic lab strain
- *E. coli* NC101: *pks*+ strain isolated from mouse and associated with colon cancer
- *E. coli* IHE3034: *pks*+ strain from human meningitis
- *E. coli* UTI89:  *pks*+ strain from human urinary tract infection

[PATRIC]( https://www.patricbrc.org/) is browsed to find these four genomes, and their corresponding genome names and genome ids are recorded in the metadata table shown below.

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/get_genome_data_2.png)

Since we are curious about the similarities and differences between human versus rodent *E. coli* strains as well as genomes that do and do not encode the *pks* gene island, we use *genome_analysis.py* to identify genes that are unique to these subgroups compared to the larger genome group.  The subgroups of interested are 1) all rodent genomes, 2) the novel rodent genomes, and 3) all *pks*+ genomes. These subgroups are recorded in the metadata table shown below.  

**metadata_table.txt file**
|	genome_name	|	genome_ids_patric	|	genome_name_patric	|	contigs	|	genome_name_contigs	|	R1	|	R2	|	genome_name_reads	|	subgroup	|	include_all_rodents	|	exclude_all_rodents	|	include_novel_rodents	|	exclude_novel_rodents	|	include_all_pks	|	exclude_all_pks	|
|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|
|	Escherichia coli IHE3034	|	714962.3	|	Escherichia coli IHE3034	|		|		|		|		|		|	all_rodents	|		|	Escherichia coli IHE3034	|		|	Escherichia coli IHE3034	|	Escherichia coli IHE3034	|		|
|	Escherichia coli NC101	|	753642.3	|	Escherichia coli NC101	|		|		|		|		|		|	novel_rodents	|	Escherichia coli NC101	|		|		|	Escherichia coli NC101	|	Escherichia coli NC101	|		|
|	Escherichia coli str. K-12 substr. MG1655	|	511145.12	|	Escherichia coli str. K-12 substr. MG1655	|		|		|		|		|		|	all_pks	|		|	Escherichia coli str. K-12 substr. MG1655	|		|	Escherichia coli str. K-12 substr. MG1655	|		|	Escherichia coli str. K-12 substr. MG1655	|
|	Escherichia coli UTI89	|	364106.8	|	Escherichia coli UTI89	|		|		|		|		|		|		|		|	Escherichia coli UTI89	|		|	Escherichia coli UTI89	|	Escherichia coli UTI89	|		|
|	Escherichia coli strain 1408270010	|		|		|	Escherichia_coli_strain_1408270010_contigs.fasta	|	Escherichia coli strain 1408270010	|		|		|		|		|	Escherichia coli strain 1408270010	|		|	Escherichia coli strain 1408270010	|		|	Escherichia coli strain 1408270010	|		|
|	Escherichia coli strain 1409150006	|		|		|	Escherichia_coli_strain_1409150006_contigs.fasta	|	Escherichia coli strain 1409150006	|		|		|		|		|	Escherichia coli strain 1409150006	|		|	Escherichia coli strain 1409150006	|		|	Escherichia coli strain 1409150006	|		|
|	Escherichia coli strain 1409160003	|		|		|	Escherichia_coli_strain_1409160003_contigs.fasta	|	Escherichia coli strain 1409160003	|		|		|		|		|	Escherichia coli strain 1409160003	|		|	Escherichia coli strain 1409160003	|		|		|	Escherichia coli strain 1409160003	|
|	Escherichia coli strain 1512290008	|		|		|	Escherichia_coli_strain_1512290008_contigs.fasta	|	Escherichia coli strain 1512290008	|		|		|		|		|	Escherichia coli strain 1512290008	|		|	Escherichia coli strain 1512290008	|		|	Escherichia coli strain 1512290008	|		|
|	Escherichia coli strain 1512290026	|		|		|	Escherichia_coli_strain_1512290026_contigs.fasta	|	Escherichia coli strain 1512290026	|		|		|		|		|	Escherichia coli strain 1512290026	|		|	Escherichia coli strain 1512290026	|		|	Escherichia coli strain 1512290026	|		|
|	Escherichia coli strain 20170221001	|		|		|		|		|	20170221001_R1.fastq	|	20170221001_R2.fastq	|	Escherichia coli strain 20170221001	|		|	Escherichia coli strain 20170221001	|		|	Escherichia coli strain 20170221001	|		|	Escherichia coli strain 20170221001	|		|

## Outputs

### Pan-genome Phylogentic Tree
The pan-genome-tree_out.txt file is a matrix of binary presence and absence of core and accessory genes that is in PHYLIP format.
A phylogenetic tree can be created using analyzed by [RAxML](https://cme.h-its.org/exelixis/web/software/raxml/index.html),  [IQ-TREE](http://www.iqtree.org/), or similar program.  Here, we will download [IQ-TREE](http://www.iqtree.org/) and then use this program create the phylogenetic tree with the command below.

`directory\to\bin\iqtree -s directory\to\pan-genome-tree_out.txt -bb 1000` 

The output of IQ-TREE, pan-genome-tree_out.txt.tree file, is loaded into [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) or similar tool to visualize the phylogenetic tree. In the image below, [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) was used.  It appears from the pan-genome phylogenetic tree that the genomes of *E. coli* strains isolated from rodent hosts are more similar to each other than to the strians from human hosts.

**Pan-genome phylogenetic Tree**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/pan-genome-tree.png)

**Clustermap**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/clustermap.png)

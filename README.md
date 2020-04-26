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
|	 -merge_all_annotations	|	 --merge_all_annotations	|	Merge all annotation metadata files in output folder? Enter "yes" or "no". Default is "yes".	|

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

**Hierarchically-clustered heatmap (ie clustermap) of protein families in pan-genome**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/clustermap.png)

**gene_family_clustermap_out.txt**
Below is an excerpt of the dataframe associated with the hierarchically-clustered heatmap (ie clustermap) shown above. (Note: Only the first 10 rows are shown in the exceprt.)

|	pgfam	|	Escherichia_coli_str._K-12_substr._MG1655	|	Escherichia_coli_strain_1408270010	|	Escherichia_coli_strain_1409150006	|	Escherichia_coli_strain_1512290008	|	Escherichia_coli_strain_1409160003	|	Escherichia_coli_strain_20170221001	|	Escherichia_coli_NC101	|	Escherichia_coli_strain_1512290026	|	Escherichia_coli_IHE3034	|	Escherichia_coli_UTI89	|
|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|	-----	|
|	PGF_08225224	|	50	|	156	|	167	|	161	|	116	|	123	|	139	|	118	|	95	|	120	|
|	PGF_01000105	|	1	|	40	|	42	|	47	|	31	|	14	|	21	|	12	|	9	|	29	|
|	PGF_03024018	|	18	|	0	|	0	|	0	|	0	|	0	|	7	|	0	|	6	|	6	|
|	PGF_05075091	|	1	|	13	|	1	|	1	|	1	|	1	|	1	|	1	|	1	|	1	|
|	PGF_00047661	|	0	|	6	|	5	|	6	|	4	|	0	|	1	|	1	|	0	|	2	|
|	PGF_06366833	|	4	|	1	|	1	|	1	|	1	|	2	|	2	|	1	|	6	|	4	|
|	PGF_07937889	|	2	|	1	|	1	|	1	|	0	|	2	|	1	|	1	|	5	|	3	|
|	PGF_10529284	|	3	|	1	|	1	|	1	|	2	|	1	|	1	|	1	|	4	|	3	|
|	PGF_10443983	|	0	|	1	|	1	|	1	|	0	|	1	|	3	|	1	|	2	|	2	|
|	PGF_00369678	|	1	|	1	|	1	|	1	|	1	|	0	|	2	|	1	|	4	|	2	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|

**core_unqiue_genes.txt**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing which genes are core or unique to this genome.  For genes that are neither core nor unique (ie shared between some but not all genomes in the group), the row is left blank.  The relationship of these genes within the genome group can be found by comparing subgroups, which is shown next.
(Note: In the excerpt below, some columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	start	|	stop	|	strand	|	function	|	pgfam	|	core_unique_gene	|
|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.1	|	CDS	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.2	|	CDS	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.3	|	CDS	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.4	|	CDS	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.5	|	CDS	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.6	|	CDS	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.7	|	CDS	|	5975	|	5214	|	-	|	Transcriptional regulator YdeO, AraC family	|	PGF_00058697	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.8	|	CDS	|	6284	|	6051	|	-	|	Two-component-system connector protein SafA	|	PGF_00063151	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.13	|	CDS	|	13799	|	11148	|	-	|	Outer membrane usher protein FimD	|	PGF_00028437	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.15	|	CDS	|	15476	|	14913	|	-	|	Type-1 fimbrial protein, A chain	|	PGF_02911992	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.16	|	CDS	|	16126	|	16004	|	-	|	hypothetical protein	|	PGF_08225224	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.339	|	CDS	|	329558	|	329445	|	-	|	hypothetical protein	|	PGF_01651140	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.354	|	CDS	|	343234	|	343055	|	-	|	hypothetical protein	|	PGF_01650528	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.450	|	CDS	|	425232	|	425080	|	-	|	hypothetical protein	|	PGF_01632236	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.464	|	CDS	|	438546	|	437446	|	-	|	hypothetical protein	|	PGF_00281105	|	unique_Escherichia_coli_strain_20170221001	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|


**Subgroup analysis**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing which genes are unqiue to paricular subgroups.  The subgroups of interest were defined based on the metadata table (shown above).  To recap, we were interested in which genes are unique to 1) all genomes that encode *pks* gene island, 2) all genomes that were isolated from rodent hosts, and 3) the genomes from the six novel *E. coli* isolates from lab mice and a pet rat. For genes not found in these subgroups (ie could be a core, unique gene to this genome, or unique to subgroup not analyzed), the row is left blank.  From this output, we can see which genes are shared between these subgroups and not found in the other genome in the larger group.
(Note: In the excerpt below, some columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	start	|	stop	|	strand	|	function	|	pgfam	|	subgroup_gene	|
|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.1	|	CDS	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.2	|	CDS	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.3	|	CDS	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.4	|	CDS	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.5	|	CDS	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.6	|	CDS	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.14	|	CDS	|	14551	|	13841	|	-	|	chaperone FimC	|	PGF_02911703	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.108	|	CDS	|	109072	|	109272	|	+	|	hypothetical protein	|	PGF_00250457	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.123	|	CDS	|	122706	|	122467	|	-	|	Uncharacterized protein YdhL	|	PGF_02720073	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.412	|	CDS	|	394531	|	393980	|	-	|	UPF0098 protein ybcL precursor	|	PGF_04249868	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.459	|	CDS	|	433910	|	432447	|	-	|	PilV-like protein	|	PGF_00034309	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.460	|	CDS	|	434520	|	433963	|	-	|	IncI1 plasmid conjugative transfer prepilin PilS	|	PGF_00013956	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.461	|	CDS	|	435223	|	434918	|	-	|	hypothetical protein	|	PGF_05161694	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.468	|	CDS	|	439859	|	439584	|	-	|	hypothetical protein	|	PGF_04171970	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.494	|	CDS	|	460587	|	460297	|	-	|	hypothetical protein	|	PGF_00219209	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.559	|	CDS	|	536811	|	536089	|	-	|	Thioesterase	|	PGF_00056580	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.560	|	CDS	|	538309	|	536804	|	-	|	Polyketide synthase modules and related proteins	|	PGF_00402183	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.561	|	CDS	|	540790	|	538331	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.562	|	CDS	|	545188	|	540821	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.898	|	CDS	|	929878	|	930042	|	+	|	hypothetical protein	|	PGF_01087026	|	novel_rodents	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|

**Median Analysis**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing how many genes are present and how they compare to the median copy number in the genome group (ie equal to, greater than, or less than the median).  Sometimes a gene may not be present in a genome while other genomes have this gene.  In these cases, the gene is *less than the median*.  Accordinlgy, the annotation metadata output will still show these genes are absent; however, since these gene are not present in the genome, there will be no addition annotation metadata in the output.  (Note: In the excerpt below, some columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	start	|	stop	|	strand	|	function	|	pgfam	|	gene_count	|	median	|	gene_count-median	|	vs_median
|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.1	|	CDS	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|	3	|	3	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.2	|	CDS	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|	1	|	1	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.3	|	CDS	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|	1	|	0	|	1	|	greater than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.4	|	CDS	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|	1	|	1	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.5	|	CDS	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|	1	|	1	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.6	|	CDS	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|	1	|	1	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.16	|	CDS	|	16126	|	16004	|	-	|	hypothetical protein	|	PGF_08225224	|	123	|	121.5	|	1.5	|	greater than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.19	|	CDS	|	19186	|	18482	|	-	|	Toxin HigB / Protein kinase domain of HipA	|	PGF_00011753	|	3	|	2	|	1	|	greater than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.20	|	CDS	|	19608	|	19315	|	-	|	Toxin HigB / Protein kinase domain of HipA	|	PGF_00011753	|	3	|	2	|	1	|	greater than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.89	|	CDS	|	89721	|	88456	|	-	|	Glucuronide transport facilitator UidC	|	PGF_00008042	|	1	|	1.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.178	|	CDS	|	180659	|	181705	|	+	|	2-keto-3-deoxy-D-arabino-heptulosonate-7-phosphate synthase I alpha (EC 2.5.1.54)	|	PGF_00070354	|	5	|	3	|	2	|	greater than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.256	|	CDS	|	255363	|	254617	|	-	|	MltA-interacting protein MipA	|	PGF_00040822	|	1	|	1.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.358	|	CDS	|	348666	|	347518	|	-	|	Flagellar biosynthesis protein FlhB	|	PGF_02186693	|	1	|	1.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.370	|	CDS	|	358246	|	357359	|	-	|	Flagellar motor rotation protein MotA	|	PGF_06889881	|	1	|	1.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.400	|	CDS	|	382121	|	381402	|	-	|	RNA polymerase sigma factor for flagellar operon	|	PGF_00046377	|	1	|	1.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|		|		|		|		|		|		|		|	PGF_00000241	|	0	|	0	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|		|		|		|		|		|		|		|	PGF_00000473	|	0	|	0	|	0	|	equal to median
|	Escherichia_coli_strain_20170221001	|		|		|		|		|		|		|		|	PGF_00002312	|	0	|	0.5	|	-0.5	|	less than median
|	Escherichia_coli_strain_20170221001	|		|		|		|		|		|		|		|	PGF_00002325	|	0	|	1	|	-1	|	less than median
|	Escherichia_coli_strain_20170221001	|		|		|		|		|		|		|		|	PGF_00002569	|	0	|	0	|	0	|	equal to median
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…

**DIAMOND Blast**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing the DIAMOND blast results against the virulence factor database.  In the excerpt, we see this strain encodes the *pks* genes. (Note: In the excerpt below, some columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	start	|	stop	|	strand	|	function	|	pgfam	|	qseqid_VF	|	qlen_VF	|	VF_ID	|	slen_VF	|	evalue_VF	|	bitscore_VF	|	pident_VF	|	qcovhsp_VF	|
|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.559	|	CDS	|	536811	|	536089	|	-	|	Thioesterase	|	PGF_00056580	|	fig|2.7989.peg.559	|	240	|	VFG043678(gi:112292703) (clbQ) putative thioesterase [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	240	|	4.00E-143	|	504.6	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.560	|	CDS	|	538309	|	536804	|	-	|	Polyketide synthase modules and related proteins	|	PGF_00402183	|	fig|2.7989.peg.560	|	501	|	VFG049162(gb-YP 006635488.1) (clbP) precolibactin peptidase ClbP [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	501	|	1.60E-290	|	995.3	|	99.8	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.561	|	CDS	|	540790	|	538331	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.561	|	819	|	VFG049161(gb-YP 006635487.1) (clbO) colibactin polyketide synthase ClbO [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	819	|	0.00E+00	|	1642.5	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.562	|	CDS	|	545188	|	540821	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.562	|	1455	|	VFG049160(gb-YP 006635486.1) (clbN) colibactin non-ribosomal peptide synthetase ClbN [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	1455	|	0.00E+00	|	2972.2	|	99.9	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.563	|	CDS	|	546624	|	545185	|	-	|	Na+-driven multidrug efflux pump	|	PGF_00025248	|	fig|2.7989.peg.563	|	479	|	VFG043682(gi:112292707) (clbM) putative drug/sodium antiporter [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	479	|	2.40E-256	|	881.7	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.564	|	CDS	|	548149	|	546686	|	-	|	Putative amidase	|	PGF_00040134	|	fig|2.7989.peg.564	|	487	|	VFG049158(gb-YP 006635484.1) (clbL) colibactin biosynthesis amidase ClbL [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	487	|	9.30E-288	|	986.1	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.566	|	CDS	|	558540	|	555508	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.566	|	1010	|	VFG049155(gb-YP 006635481.1) (clbI) colibactin polyketide synthase ClbI [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	1010	|	0.00E+00	|	1973	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.567	|	CDS	|	563386	|	558590	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.567	|	1598	|	VFG049154(gb-YP 006635480.1) (clbH) colibactin non-ribosomal peptide synthetase ClbH [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	1598	|	0.00E+00	|	3172.9	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.568	|	CDS	|	564702	|	563434	|	-	|	Malonyl CoA-acyl carrier protein transacylase (EC 2.3.1.39) in polyketide synthesis	|	PGF_02943429	|	fig|2.7989.peg.568	|	422	|	VFG043688(gi:112292713) (clbG) putative malonyl-CoA transacylase [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	422	|	2.10E-240	|	828.6	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.569	|	CDS	|	565829	|	564699	|	-	|	Acyl-CoA dehydrogenase	|	PGF_10428547	|	fig|2.7989.peg.569	|	376	|	VFG043689(gi:112292714) (clbF) putative acyl-CoA dehydrogenase [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	376	|	3.30E-216	|	748	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.570	|	CDS	|	566081	|	565833	|	-	|	hypothetical protein	|	PGF_00279040	|	fig|2.7989.peg.570	|	82	|	VFG049151(gb-YP 006635477.1) (clbE) colibactin biosynthesis aminomalonyl-acyl carrier protein ClbE [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	82	|	2.10E-38	|	155.2	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.571	|	CDS	|	566977	|	566111	|	-	|	3-hydroxyacyl-CoA dehydrogenase (EC 1.1.1.35)	|	PGF_07756589	|	fig|2.7989.peg.571	|	288	|	VFG049150(gb-YP 006635476.1) (clbD) colibactin biosynthesis dehydrogenase ClbD [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	289	|	4.20E-163	|	571.2	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.572	|	CDS	|	569590	|	566990	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.572	|	866	|	VFG043692(gi:112292717) (clbC) putative polyketide synthase [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	866	|	0.00E+00	|	1780.8	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.573	|	CDS	|	579251	|	569631	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	fig|2.7989.peg.573	|	3206	|	VFG043693(gi:112292718) (clbB) putative hybrid polyketide-non-ribosomal peptide synthetase [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	3206	|	0.00E+00	|	6393.5	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.574	|	CDS	|	579661	|	579873	|	+	|	hypothetical protein	|	PGF_01631935	|	fig|2.7989.peg.574	|	70	|	VFG043694(gi:112292719) (clbR) putative regulatory protein [colibactin (TX033)] [Escherichia coli O18:K1:H7 str. IHE3034]	|	70	|	2.90E-33	|	137.9	|	100	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.575	|	CDS	|	579874	|	580608	|	+	|	hypothetical protein	|	PGF_00292201	|	fig|2.7989.peg.575	|	244	|	VFG049147(gb-YP 006635473.1) (clbA) colibactin biosynthesis phosphopantetheinyl transferase ClbA [Colibactin (VF0573)] [Klebsiella pneumoniae subsp. pneumoniae 1084]	|	244	|	4.10E-143	|	504.6	|	100	|	100	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|

**merged annotation metadata from above analyses**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing the DIAMOND blast results against the virulence factor database.  In the excerpt, we see this strain encodes the *pks* genes. (Note: In the excerpt below, some columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	start	|	stop	|	strand	|	function	|	pgfam	|	core_unique_gene	|	gene_count	|	median	|	gene_count-median	|	vs_median	|	subgroup_gene	|	qlen_VF	|	VF_ID	|	slen_VF	|	evalue_VF	|	bitscore_VF	|	pident_VF	|	qcovhsp_VF	|
|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|	 -----	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.1	|	CDS	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|	core	|	3	|	3	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.2	|	CDS	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|		|	1	|	1	|	0	|	equal to median	|	all_rodents	|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.3	|	CDS	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|	unique_Escherichia_coli_strain_20170221001	|	1	|	0	|	1	|	greater than median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.4	|	CDS	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|	core	|	1	|	1	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.5	|	CDS	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|		|	1	|	1	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.6	|	CDS	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|		|	1	|	1	|	0	|	equal to median	|		|	560	|	VFG001444(gb-AAG10151) (aslA) putative arylsulfatase [AslA (VF0238)] [Escherichia coli O18:K1:H7 str. RS218]	|	475	|	6.70E-32	|	136.3	|	26.1	|	71.6	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.7	|	CDS	|	5975	|	5214	|	-	|	Transcriptional regulator YdeO, AraC family	|	PGF_00058697	|		|	1	|	1	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.8	|	CDS	|	6284	|	6051	|	-	|	Two-component-system connector protein SafA	|	PGF_00063151	|		|	1	|	1	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.9	|	CDS	|	8775	|	6496	|	-	|	Putative formate dehydrogenase oxidoreductase protein	|	PGF_06030909	|		|	1	|	1	|	0	|	equal to median	|		|		|		|		|		|		|		|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.10	|	CDS	|	10028	|	9114	|	-	|	mannose-specific adhesin FimH	|	PGF_00401044	|		|	1	|	1	|	0	|	equal to median	|		|	304	|	VFG042718(gi:15801636) (Z2206) putative adhesin; FimH protein [F9 fimbriae (AI090)] [Escherichia coli O157:H7 str. EDL933]	|	304	|	5.80E-171	|	597.4	|	98	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.11	|	CDS	|	10591	|	10088	|	-	|	Type 1 fimbrae adaptor subunit FimG	|	PGF_00063158	|		|	1	|	1	|	0	|	equal to median	|		|	167	|	VFG033335(gi:410482685) (fimG) fimbrial-like adhesin protein [Type I fimbriae (CVF426)] [Escherichia coli O104:H4 str. 2009EL-2050]	|	167	|	6.80E-89	|	323.9	|	98.2	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.12	|	CDS	|	11134	|	10604	|	-	|	Uncharacterized fimbrial-like protein YdeS	|	PGF_00064710	|		|	1	|	1	|	0	|	equal to median	|		|	176	|	VFG033311(gi:387607090) (fimF) fimbrial protein [Type I fimbriae (CVF426)] [Escherichia coli O44:H18 042]	|	176	|	1.80E-95	|	345.9	|	98.9	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.13	|	CDS	|	13799	|	11148	|	-	|	Outer membrane usher protein FimD	|	PGF_00028437	|	core	|	3	|	3	|	0	|	equal to median	|		|	883	|	VFG033284(gi:387607091) (fimD) fimbrial outer membrane usher protein [Type I fimbriae (CVF426)] [Escherichia coli O44:H18 042]	|	883	|	0	|	1721.1	|	96.8	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.14	|	CDS	|	14551	|	13841	|	-	|	chaperone FimC	|	PGF_02911703	|		|	1	|	1	|	0	|	equal to median	|	all_pks	|	236	|	VFG042714(gi:15801632) (Z2201) putative fimbrial chaperone protein [F9 fimbriae (AI090)] [Escherichia coli O157:H7 str. EDL933]	|	239	|	3.90E-130	|	461.5	|	97.9	|	100	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.15	|	CDS	|	15476	|	14913	|	-	|	Type-1 fimbrial protein, A chain	|	PGF_02911992	|	core	|	3	|	3	|	0	|	equal to median	|		|	187	|	VFG042713(gi:15801631) (Z2200) putative major fimbrial subunit [F9 fimbriae (AI090)] [Escherichia coli O157:H7 str. EDL933]	|	187	|	1.90E-95	|	345.9	|	99.5	|	100	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|



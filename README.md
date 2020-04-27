# Microbial-Comparative-Genomics

## Overview
These are series of Python 2.7 scripts aimed to facilitate and improve the comparative analysis of bacterial genomes.
These scripts enable genome assembly and gene annotation from raw sequencing reads followed by comparative analyses to understand the similarities and difference within a group of bacterial genomes of interest.
These scripts take advantage of the curated database of publicly accessible bacterial genomes and services hosted by [Pathosystems Resource Integration Center (PATRIC)](https://www.patricbrc.org/).  Users of these scripts will require a [PATRIC](https://www.patricbrc.org/) account and must use the [PATRIC Command Line Interface](https://docs.patricbrc.org/cli_tutorial/).

Often, researchers require assembly and annotation of more than one genome for their projects.
There are many steps involved from processing raw reads of adaptor sequences or low quality base pairs, assembling reads into contigs, and finally gene annotation.
Thus, processing each genome one-by-one can be cumbersome, time consuming, and error prone.
The **get_genome_data.py** script overcomes these challenges employing the [Comprehensive Genome Analysis Service](https://docs.patricbrc.org/user_guides/services/comprehensive_genome_analysis_service.html) hosted by [PATRIC](https://www.patricbrc.org/) in order to automate the assembly and annotation workflow, thereby increasing throughput when numerous genomes must be processed.
Additionally, the **get_genome_data.py** accepts pair-end reads (fastq) or pre-assembled contigs (fasta), which provides flexibility.
Pair-end reads (fastq) or pre-assembled contigs (fasta) data for numerous genomes can be piped into **get_genome_data.py** by including the appropriate metadata.
The output of **get_genome_data.py** is a full-genome report summarizing the genome assembly and annotation characteristics, assembled genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata.

Furthermore, the **get_genome_data.py** script provided in this library allows researchers to access and download bacterial genomes maintained in the PATRIC database.  Specifically, **get_genome_data.py** allows researchers to acquire assembled genome sequences (contigs fasta files), gene annotation sequences (DNA and protein fasta files), and annotation metadata from numerous genomes quickly.

Comparative genomics involves the identification of genetic factors, namely genes, which are shared or differ between bacteria genera, species, and/or strains.
The **genome_analysis.py** script facilitates the identification of genes and gene families that differentiate bacterial genomes.  This script executes six analysis workflows, which are summarized below.

**Overview of Workflow**

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/overview.PNG)

## *get_genome_data.py*

**Workflow of *get_genome_data.py***

![](https://github.com/TonyMannion/Microbial-Comparative-Genomics/blob/master/images/get_genome_data_1.PNG)

The **genome_assembly_annotate.py** script allows the assembly and annotation from raw sequencing reads and/or pre-assembled contigs of multiple genomes simultaneously.

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

The **genome_analysis.py** script performs six different analyses that facilitate the comparison of genomes.  [Global protein families (i.e., PGfams)]( https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4744870/) determined by PATRIC are used as the basis for determining relationships in the pan-genome. 

**1.	Pan-genome phylogenetic tree**

  Creates PHYLIP formatted matrix of binary presence and absence of PGfams in the pan-genome of the genome group.  The output file is * pan-genome-tree_out.txt * and can be used to make a phylogenetic tree in other programs such as [RAxML](https://cme.h-its.org/exelixis/web/software/raxml/index.html),  [IQ-TREE](http://www.iqtree.org/), or similar program.  Here, we will download [IQ-TREE](http://www.iqtree.org/).

**2.	Pan-genome hierarchically-clustered heatmap**

  A hierarchically-clustered heatmap (i.e., clustermap) of PGfams in the pan-genome is created using the [Seaborn clustermap function](https://seaborn.pydata.org/generated/seaborn.clustermap.html).  Cluster analysis is performed using the “Euclidean” distance metric and the “average” linkage method on both axis (i.e., genomes and PGfams).  The output is an image of the clustermap (i.e., clustermap.png), which shows the abundance of the genes per genome and their clustering relationships.  (Please note that the depiction of the dendrogram for the PGfam relationships is excluded in clustermap.png image because its dendrogram is too busy.)  The DataFrame corresponding to the clustermap is generated (i.e., gene_family_clustermap_out.txt), which can be analyzed if desired. 

**3.	Core and unique genes in pan-genome**

  The core (i.e., present in all genomes) and unique (i.e., present in only a single genomes) PGfams in the pan-genome are determined and merged into the annotation metadata per genome.

**4.	Unique genes in genome subgroups**

  PGfams unique to subgroups of genomes within the larger group are identified and merged into the annotation metadata for each genome.  The subgroups are indicated in the metadata table.  Sometimes subgroups of interest may be known *a priori* or may be realized following analysis of the pan-genome phylogenetic tree* and/or *pan-genome hierarchically-clustered heatmap* results.

**5.	Gene copies versus median gene copy number in genome group**

  The median copy number for each PGfams in the genome group is calculated and then compared per genome.  The resulting analysis yields how many PGfams are present in a genome and if the number PGfams is equal to, greater than, or equal to the median.  Results are merged into the annotation metadata for each genome

**6.	Diamond BLAST for virulence factors, antibiotic resistance, and other genes**

  [DIAMOND blast](http://www.diamondsearch.org/index.php) is used to determine if genes are homologous to known virulence factor or antibiotic resistance genes.  Virulence factor genes are derived from the [Virulence Factor DataBase (VFDB)](http://www.mgc.ac.cn/VFs/download.htm), and antibiotic resistance genes are derived from [Comprehensive Antibiotic Resistance Database (CARD)]( https://card.mcmaster.ca/download).  Users can also search against a custom database by providing a multiple sequence protein fasta file.  The best match hits per gene are merged into the annotation metadata for each genome.

For each genome, the above analyses are also merged into a single annotation metadata file, thereby allowing all results to be viewed simultaneously.  
	
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

More specifically, we would like to know:

-	Are *E. coli* strains from human and rodents phylogenetically distinct?
-	What genes are found in all *pks*+ *E. coli* genomes?
-	What genes are found only in genomes of *E. coli* strains isolated from all rodents?
-	What genes are found only in novel genomes of *E. coli* strains isolated from the rodent?
-	What genes are unique to novel genome of *E. coli* strains isolated from a rat compared to mice?


Here, *get_genome_data.py* will be used to assembly and annotate six user genomes.  Pre-assembled contigs from five *E. coli* strains isolated from lab mice ([Mannion A. et al. *Genome Announc.* 2016.](https://mra.asm.org/content/4/5/e01082-16)) and Illumina MiSeq 2x250 bp reads from one *E. coli* strain isolated from pet rat ([Fabian NJ. et al. *Vet Microbiol.* 2020.]( https://www.sciencedirect.com/science/article/pii/S0378113519303669?via%3Dihub)).  The sequencing reads (fastq files) and pre-assembled contigs (fasta files) along with their corresponding genome names are recorded in the metadata table shown below.  All of these isolates, except one, were experimentally shown to encode the *pks* gene island.

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
Below is an excerpt of the dataframe associated with the hierarchically-clustered heatmap (ie clustermap) shown above. (Note: Only the first 10 rows are shown in the excerpt.)

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

**Annotation metadata with gene analysis**

After each individual comparative analysis step is performed, the results are added to the annotation metadata table for each genome.  To facilitate analyzing this data, the results from previous analyses are also merged into a single file, per genome.  This makes it easy to examine the datasets and answer the questions we posed above.  Below is an excerpt of the merged annotation metadata table for *E. coli* strain 20170221001.  (Note: In the excerpt below, some columns were excluded to optimize viewing.)

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

## Analysis

How similar are human vs rodent genomes?

- phylogentic tree and clustermap

What genes are found in all pks+ genomes?

- 61 pgfams
- Includes full pks gene island 
- 14 other VF genes (>=90% identity and coverage), including S_fimbriae, Salmochelin siderophore and (ibeA) invasion protein IbeA gene

What genes are found only in all rodent genomes?

- 39 pgfams
- Including 19 genes annotated with Propanediol uptake and metabolism 
- In our example, we see a propanediol utilization pathway is present only in the seven *E. coli* strains isolated from rodents (all_rodents subgroup), suggesting these strains could use different carbon and energy sources compared to human strains.

What gene are found only in the novel rodent genomes?

- 15 pgfams
- Mainly hypothetical protein annotations
- No homology with vf or antibiotic resistence genes

What genes are unique to the rat isolate?

- Based on clustermap, there is large block of genes that are unique to this isolate
- 234 pgfams
- Mainly hypothetical protein annotations
- 36 are annotations relating to phage, 28 of these on the same contig, possible phage insert in its genome

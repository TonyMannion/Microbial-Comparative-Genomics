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
(Note: In the excerpt below, the columans aliases, plfam, figfam, evidence_codes, nucleotide_sequence, and aa_sequence columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	location	|	start	|	stop	|	strand	|	function	|	pgfam	|	core_unique_gene	|
|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.1	|	CDS	|	assembly_contig_1_291-291	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.2	|	CDS	|	assembly_contig_1_445-144	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.3	|	CDS	|	assembly_contig_1_472+144	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.4	|	CDS	|	assembly_contig_1_1663-1011	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.5	|	CDS	|	assembly_contig_1_3078-1158	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.6	|	CDS	|	assembly_contig_1_4812-1683	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.7	|	CDS	|	assembly_contig_1_5975-762	|	5975	|	5214	|	-	|	Transcriptional regulator YdeO, AraC family	|	PGF_00058697	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.8	|	CDS	|	assembly_contig_1_6284-234	|	6284	|	6051	|	-	|	Two-component-system connector protein SafA	|	PGF_00063151	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.13	|	CDS	|	assembly_contig_1_13799-2652	|	13799	|	11148	|	-	|	Outer membrane usher protein FimD	|	PGF_00028437	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.15	|	CDS	|	assembly_contig_1_15476-564	|	15476	|	14913	|	-	|	Type-1 fimbrial protein, A chain	|	PGF_02911992	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.16	|	CDS	|	assembly_contig_1_16126-123	|	16126	|	16004	|	-	|	hypothetical protein	|	PGF_08225224	|	core	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.339	|	CDS	|	assembly_contig_1_329558-114	|	329558	|	329445	|	-	|	hypothetical protein	|	PGF_01651140	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.354	|	CDS	|	assembly_contig_1_343234-180	|	343234	|	343055	|	-	|	hypothetical protein	|	PGF_01650528	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.450	|	CDS	|	assembly_contig_1_425232-153	|	425232	|	425080	|	-	|	hypothetical protein	|	PGF_01632236	|	unique_Escherichia_coli_strain_20170221001	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig-2.7989.peg.464	|	CDS	|	assembly_contig_1_438546-1101	|	438546	|	437446	|	-	|	hypothetical protein	|	PGF_00281105	|	unique_Escherichia_coli_strain_20170221001	|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|

**Subgroup analysis**

Below is an excerpt of the annotation metadata table for *E. coli* strain 20170221001 showing which genes are unqiue to paricular subgroups.  The subgroups of interest were defined based on the metadata table (shown above).  To recap, we were interested in which genes are unique to 1) all genomes that encode *pks* gene island, 2) all genomes that were isolated from rodent hosts, and 3) the genomes from the six novel *E. coli* isolates from lab mice and a pet rat. For genes not found in these subgroups (ie could be a core, unique gene to this genome, or unique to subgroup not analyzed), the row is left blank.  From this output, we can see which genes are shared between these subgroups and not found in the other genome in the larger group.
(Note: In the excerpt below, the columans aliases, plfam, figfam, evidence_codes, nucleotide_sequence, and aa_sequence columns were excluded to optomize viewing.)

|	genome_name	|	contig_id	|	feature_id	|	type	|	location	|	start	|	stop	|	strand	|	function	|	pgfam	|	subgroup_gene	|
|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|	 ------	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.14	|	CDS	|	assembly_contig_1_14551-711	|	14551	|	13841	|	-	|	chaperone FimC	|	PGF_02911703	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.559	|	CDS	|	assembly_contig_1_536811-723	|	536811	|	536089	|	-	|	Thioesterase	|	PGF_00056580	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.560	|	CDS	|	assembly_contig_1_538309-1506	|	538309	|	536804	|	-	|	Polyketide synthase modules and related proteins	|	PGF_00402183	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.561	|	CDS	|	assembly_contig_1_540790-2460	|	540790	|	538331	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.562	|	CDS	|	assembly_contig_1_545188-4368	|	545188	|	540821	|	-	|	Polyketide synthase modules and related proteins	|	PGF_10503453	|	all_pks	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.2	|	CDS	|	assembly_contig_1_445-144	|	445	|	302	|	-	|	hypothetical protein	|	PGF_02969562	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.123	|	CDS	|	assembly_contig_1_122706-240	|	122706	|	122467	|	-	|	Uncharacterized protein YdhL	|	PGF_02720073	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.459	|	CDS	|	assembly_contig_1_433910-1464	|	433910	|	432447	|	-	|	PilV-like protein	|	PGF_00034309	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.460	|	CDS	|	assembly_contig_1_434520-558	|	434520	|	433963	|	-	|	IncI1 plasmid conjugative transfer prepilin PilS	|	PGF_00013956	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.461	|	CDS	|	assembly_contig_1_435223-306	|	435223	|	434918	|	-	|	hypothetical protein	|	PGF_05161694	|	all_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.108	|	CDS	|	assembly_contig_1_109072+201	|	109072	|	109272	|	+	|	hypothetical protein	|	PGF_00250457	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.412	|	CDS	|	assembly_contig_1_394531-552	|	394531	|	393980	|	-	|	UPF0098 protein ybcL precursor	|	PGF_04249868	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.468	|	CDS	|	assembly_contig_1_439859-276	|	439859	|	439584	|	-	|	hypothetical protein	|	PGF_04171970	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.494	|	CDS	|	assembly_contig_1_460587-291	|	460587	|	460297	|	-	|	hypothetical protein	|	PGF_00219209	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.898	|	CDS	|	assembly_contig_1_929878+165	|	929878	|	930042	|	+	|	hypothetical protein	|	PGF_01087026	|	novel_rodents	|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.1	|	CDS	|	assembly_contig_1_291-291	|	291	|	1	|	-	|	Glutamate decarboxylase (EC 4.1.1.15)	|	PGF_00008094	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.3	|	CDS	|	assembly_contig_1_472+144	|	472	|	615	|	+	|	hypothetical protein	|	PGF_10512988	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.4	|	CDS	|	assembly_contig_1_1663-1011	|	1663	|	653	|	-	|	Probable zinc protease pqqL (EC 3.4.99.-)	|	PGF_09337443	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.5	|	CDS	|	assembly_contig_1_3078-1158	|	3078	|	1921	|	-	|	GALNS arylsulfatase regulator (Fe-S oxidoreductase)	|	PGF_00006721	|		|
|	Escherichia_coli_strain_20170221001	|	assembly_contig_1	|	fig|2.7989.peg.6	|	CDS	|	assembly_contig_1_4812-1683	|	4812	|	3130	|	-	|	N-acetylgalactosamine 6-sulfate sulfatase (GALNS)	|	PGF_00023745	|		|
|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|	…	|

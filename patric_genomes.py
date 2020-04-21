import os
from os import path
import argparse
import sys
import pandas as pd
import numpy as np

parser=argparse.ArgumentParser()

parser.add_argument('-u', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')
parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file. If using annotation metadata files, provide genome names of interest with under the header "genome_names". If downloading features from PATRIC, provide genome ids of interest under the header "genome_ids".')
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify folder with annotations. If downloading annotations from PATRIC, this will create folder for files.')

args=parser.parse_args()


print 'Logging into PATRIC...'
os.system('p3-login ' + str(args.username))
df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_ids','genome_name'])
genome_ids_list = df_genome_names['genome_ids'].dropna().tolist()
genome_name_list = df_genome_names['genome_name'].dropna().tolist()
zip(genome_ids_list,genome_name_list)
for genome_id, genome_name in zip(genome_ids_list,genome_name_list): 
	print 'Downloading features for ' + str(genome_id)+ ' ' + str(genome_name) + ' from PATRIC...'
	#make input folder if not already present
	if not os.path.exists(str(args.output_folder)):
		os.mkdir(str(args.output_folder))
	os.system('p3-echo -t genome_id ' + str(genome_id) + ' | p3-get-genome-features --in feature_type,CDS,rna --attr genome_name --attr sequence_id --attr patric_id --attr start --attr end --attr strand --attr product --attr pgfam_id --attr na_sequence --attr aa_sequence  > ' + str(args.output_folder) +'/'+str(genome_name) +'_annotation.txt')
	df_genome = pd.read_csv(str(args.output_folder) +'/'+str(genome_name) +'_annotation.txt', sep='\t')
	df_genome2=df_genome.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'})
	df_genome2.to_csv(str(args.output_folder) +'/'+str(genome_name) +'_annotation.txt', sep='\t', index=False)
	os.system('p3-genome-fasta --contig ' + str(genome_id) + ' > ' + str(args.output_folder) +'/'+str(genome_name) +'_contigs.fasta')
	os.system('p3-genome-fasta --protein ' + str(genome_id) + ' > ' + str(args.output_folder) +'/'+str(genome_name) +'_protein.fasta')
	os.system('p3-genome-fasta --feature ' + str(genome_id) + ' > ' + str(args.output_folder) +'/'+str(genome_name) +'_DNA.fasta')

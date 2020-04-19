import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_folder', dest='input_folder', help='Specify folder with protein fasta files and annotation meta file')
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify output folder.')
parser.add_argument('-m', '--metadata_table', dest='metadata_table', default = 'metadata_table.txt', help='Metadata tab-delimited file for read files, contig files, and genome names. Default is metadata_table.txt')
parser.add_argument('-v', '--VF_blast', dest='VF_blast', help='Execute blast for virulence factor (VF)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')
parser.add_argument('-r', '--res_blast', dest='res_blast', help='Execute blast for virulence factor (VF) and antibiotic resistance genes (Res)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')
parser.add_argument('-c', '--custom_blast', dest='custom_blast', help='Execute blast for virulence factor (VF) and antibiotic resistance genes (Res)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')
parser.add_argument('-f', '--custom_fasta', dest='custom_fasta', help='Execute blast for virulence factor (VF) and antibiotic resistance genes (Res)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')

args = parser.parse_args()

#make output folder
output_folder = 'blast_' + str(args.output_folder)
os.mkdir(output_folder)

def baster(type, database_file): #type = VF, RES, or custom
	df_genome_names = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['genome_name'])
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	for genome_name in genome_name_list:
		os.system('diamond blastp --db '+ str(database_file) + ' --query' + ' ' + str(args.input_folder) +'/'+ str(genome_name) + '_protein.fasta' + ' ' + '--out' + ' ' + output_folder +'/'+ str(genome_name) + '_' + str(type) + '_blast_out.txt' + ' ' + '--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df1 = pd.read_csv(str(args.input_folder) +'/'+str(genome_name) + '_annotation.txt', sep='\t', dtype=str)
		df2 = pd.read_csv(output_folder +'/'+ str(genome_name) + '_' + str(type) + '_blast_out.txt', sep='\t',  names=['qseqid' + '_' + str(type), 'qlen' + '_' + str(type), str(type) + '_'+'ID', 'slen' + '_' + str(type), 'qseq' + '_' + str(type), 'sseq' + '_' + str(type), 'evalue' + '_' + str(type), 'bitscore' + '_' + str(type), 'pident' + '_' + str(type), 'qcovhsp' + '_' + str(type)], dtype=str)
		df_merge = pd.merge(df1,df2, left_on='feature_id', right_on='qseqid' + '_' + str(type), how="left").to_csv(output_folder +'/'+str(genome_name) + '_annotation.txt', sep='\t', index=False)
		os.remove(output_folder +'/'+ str(genome_name) + '_' + str(type) + '_blast_out.txt')

#VF 
if str(args.VF_blast) == 'yes':
	baster('VF', 'VFDB_setB_pro.dmnd')
#Res
if str(args.res_blast) == 'yes':
	baster('RES', 'db card_protein.dmnd')
#custom
if str(args.custom_blast) == 'yes':
	os.system('diamond makedb --in ' + str(args.custom_fasta) + ' -d custom_database')
	baster('custom', 'custom_database.dmnd')
	os.remove('custom_database.dmnd')

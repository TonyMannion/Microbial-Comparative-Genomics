import pandas as pd
import numpy as np
import os
import argparse

parser.add_argument('-v', '--VF_blast', dest='VF_blast', default = 'yes', help='Execute blast for virulence factor (VF)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')
parser.add_argument('-r', '--res_blast', dest='res_blast', default = 'yes', help='Execute blast for virulence factor (VF) and antibiotic resistance genes (Res)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed')
parser.add_argument('-m', '--metadata_table', dest='metadata_table', default = 'metadata_table.txt', help='Metadata tab-delimited file for read files, contig files, and genome names. Default is metadata_table.txt')

parser = argparse.ArgumentParser()

df_genome_names = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['genome_name'])
genome_name_list = df_genome_names['genome_name'].dropna().tolist()

#VF
if str(args.VF_blast) == 'yes':
	for genome_name in genome_name_list:
		os.system('diamond blastp --db VFDB_setB_pro.dmnd --query' + ' ' + str(genome_name) + '_protein.fasta' + ' ' + '--out' + ' ' + str(genome_name) + '_VFDB_blast_out.txt' + ' ' + '--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df_an = pd.read_csv(str(genome_name) + '_annotation.txt', sep='\t', dtype=str)
		df_VF = pd.read_csv(str(genome_name) + '_VFDB_blast_out.txt', sep='\t',  names=['qseqid_VF', 'qlen_VF', 'VF_ID', 'slen_VF', 'qseq_VF', 'sseq_VF', 'evalue_VF', 'bitscore_VF', 'pident_VF', 'qcovhsp_VF'], dtype=str) 
		df_merge = pd.merge(df1,df2, left_on='feature_id', right_on='qseqid_VF', how="left").to_csv(str(genome_name) + '_annotation.txt', sep='\t')
#Res
if str(args.res_blast) == 'yes':
	for genome_name in genome_name_list:
		os.system('diamond blastp --db card_protein.dmnd --query' + ' ' + str(genome_name) + '_protein.fasta' + ' ' + '--out' + ' ' + str(genome_name) + '_Res_blast_out.txt' + ' ' + '--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df_an = pd.read_csv(str(genome_name) + '_annotation.txt', sep='\t', dtype=str)
		df_res = pd.read_csv(str(genome_name) + '_Res_blast_out.txt', sep='\t',  names=['qseqid_Res', 'qlen_Res', 'Res_ID', 'slen_Res', 'qseq_Res', 'sseq_Res', 'evalue_Res', 'bitscore_Res', 'pident_Res', 'qcovhsp_Res'], dtype=str) 
		df6 = pd.merge(df_an,df_res, left_on='feature_id', right_on='qseqid_Res', how="left").to_csv(str(genome_name) + '_annotation.txt', sep='\t')

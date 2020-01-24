import pandas as pd
import numpy as np
import os
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--reads_table', dest='reads_table', default = 'reads_table.txt', help='Metadata tab-delimited file for read file names and genome names. Default is reads_table.txt')
parser.add_argument('-u', '--upload_reads', dest='upload_reads', default = 'yes', help='Upload read files? Enter yes or no. Default is yes')
parser.add_argument('-a', '--assembly_annotate', dest='assembly_annotate', default = 'yes', help='Execute assembly and annotate pipeline? Enter yes or no. Default is yes', )
parser.add_argument('-d', '--download_reports', dest='download_reports', default = 'yes', help='Download genome reports, contigs, and annotations data.  Note: cannot execute blast unless assembly and annotate pipeline has been previously performed', )
parser.add_argument('-b', '--blast', dest='blast', default = 'yes', help='Execute blast for virulence factor (VF) and antibiotic resistance genes (Res)? Enter yes or no. Default is yes. Note: cannot execute blast unless assembly and annotate pipeline has been previously performed', )
args = parser.parse_args()

print 'Logging into PATRIC...'
os.system('p3-login manniona@mit.edu')

df = pd.read_csv(str(args.reads_table), sep='\t')
R1_list = df['R1'].tolist()
R2_list = df['R2'].tolist()
genome_name_list = df['genome_name'].tolist()

if str(args.upload_reads) == 'yes':
	for R1 in R1_list:
		print 'Uploading ' + str(R1)
		os.system('p3-cp ' + str(R1) + ' ws:/anthonymannion@patricbrc.org/home/AssemblyJob')
	for R2 in R2_list:
		print 'Uploading ' + str(R2)
		os.system('p3-cp ' + str(R2) + ' ws:/anthonymannion@patricbrc.org/home/AssemblyJob')

if str(args.assembly_annotate) == 'yes':
	zip(R1_list,R2_list,genome_name_list)
	for R1, R2, genome_name in zip(R1_list,R2_list,genome_name_list):
		in_file = open('params.json', "rb")
		out_file = open('params_out.json', "wb")
		reader = in_file.read()
		repls1= (('R1', str(R1)),('R2', str(R2)),('Genome_name', str(genome_name)))
		writer1 = reduce(lambda a, kv: a.replace(*kv), repls1, reader)
		writer2 = out_file.write(writer1)
		in_file.close()
		out_file.close()
		os.system('appserv-start-app ComprehensiveGenomeAnalysis params_out.json \"parrello@patricbrc.org/home/\"'+ ' > ' + str(genome_name) + '_job_ID.txt')
		job_id = open(str(genome_name) + '_job_ID.txt', "rb").readline().replace('Started task ', '').rstrip()
		print "Comprehensive Genome Analysis job sent for " + str(genome_name) + ' as job id ' + job_id
	for genome_name in genome_name_list:
		job_id2 = open(str(genome_name) + '_job_ID.txt', "rb").readline().replace('Started task ', '').rstrip()
		print job_id2
		while True:
			os.system('p3-job-status' + ' ' + job_id2 + ' > ' + str(genome_name) + '_job_status.txt')
			job_id_status = open(str(genome_name) + '_job_status.txt', "rb").readline().rstrip()
			print 'Checking status of ' + str(genome_name) + ' as job id ' + job_id_status
			if job_id_status == job_id2 + ': completed':
				break
			time.sleep(300) #check status of first jobs every 300 seconds (ie 5 minutes)
		print 'Comprehensive Genome Analysis done for ' + str(genome_name)
if str(args.download_reports) == 'yes':
	zip(R1_list,R2_list,genome_name_list)
	for R1, R2, genome_name in zip(R1_list,R2_list,genome_name_list):
		os.system('p3-cp ws:\"/anthonymannion@patricbrc.org/home/AssemblyJob/' + str(genome_name) + '/.' + str(genome_name) + '/FullGenomeReport.html\"' + ' ' + str(genome_name) + '_FullGenomeReport.html')
		os.system('p3-cp ws:\"/anthonymannion@patricbrc.org/home/AssemblyJob/' + str(genome_name) + '/.' + str(genome_name) + '/.annotation/annotation.txt\"' + ' ' + str(genome_name) + '_annotation.txt')
		os.system('p3-cp ws:\"/anthonymannion@patricbrc.org/home/AssemblyJob/' + str(genome_name) + '/.' + str(genome_name) + '/.annotation/annotation.feature_protein.fasta\"' + ' ' + str(genome_name) + '_protein.fasta')
if str(args.blast) == 'yes':
	zip(R1_list,R2_list,genome_name_list)
	for R1, R2, genome_name in zip(R1_list,R2_list,genome_name_list):
		os.system('diamond blastp --db VFDB_setB_pro.dmnd --query' + ' ' + str(genome_name) + '_protein.fasta' + ' ' + '--out' + ' ' + str(genome_name) + '_VFDB_blast_out.txt' + ' ' + '--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df1 = pd.read_csv(str(genome_name) + '_annotation.txt', sep='\t', dtype=str)
		df2 = pd.read_csv(str(genome_name) + '_VFDB_blast_out.txt', sep='\t',  names=['qseqid_VF', 'qlen_VF', 'VF_ID', 'slen_VF', 'qseq_VF', 'sseq_VF', 'evalue_VF', 'bitscore_VF', 'pident_VF', 'qcovhsp_VF'], dtype=str) 
		df3 = pd.merge(df1,df2, left_on='feature_id', right_on='qseqid_VF', how="left").to_csv(str(genome_name) + '_annotation_out.txt', sep='\t')
		os.system('diamond blastp --db card_protein.dmnd --query' + ' ' + str(genome_name) + '_protein.fasta' + ' ' + '--out' + ' ' + str(genome_name) + '_Res_blast_out.txt' + ' ' + '--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df4 = pd.read_csv(str(genome_name) + '_annotation_out.txt', sep='\t', dtype=str)
		df5 = pd.read_csv(str(genome_name) + '_Res_blast_out.txt', sep='\t',  names=['qseqid_Res', 'qlen_Res', 'Res_ID', 'slen_Res', 'qseq_Res', 'sseq_Res', 'evalue_Res', 'bitscore_Res', 'pident_Res', 'qcovhsp_Res'], dtype=str) 
		df6 = pd.merge(df4,df5, left_on='feature_id', right_on='qseqid_Res', how="left").to_csv(str(genome_name) + '_annotation_out.txt', sep='\t')
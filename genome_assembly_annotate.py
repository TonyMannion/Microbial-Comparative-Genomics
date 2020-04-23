#Dependancies
#1) download and install PATRIC command line (https://github.com/PATRIC3/PATRIC-distribution/releases)
#2) create PATRIC account (https://www.patricbrc.org/)
#3) create new folder in workspace of PATRIC account called "AssemblyJob"
#4) DIAMOND analysis (https://github.com/bbuchfink/diamond/releases/) for virulence factor genes (http://www.mgc.ac.cn/VFs/download.htm) and antibiotic resistance genes (https://card.mcmaster.ca/download).  will need to make reference database of virulence factor and antibiotic resistance genes databases using DIAMOND
import os
import time
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', dest='username', help='Enter PATRIC login username')
parser.add_argument('-m', '--metadata_table', dest='metadata_table', default = 'metadata_table.txt', help='Metadata tab-delimited file for read files, contig files, and genome names. Default is metadata_table.txt')
parser.add_argument('-i', '--input_files', dest='input_files', default = 'yes', help='Upload read and/or contig files? Enter yes or no. Default is yes')
parser.add_argument('-a', '--assembly_annotate', dest='assembly_annotate', default = 'yes', help='Execute assembly and annotate pipeline? Enter yes or no. Default is yes', )
parser.add_argument('-d', '--download_reports', dest='download_reports', default = 'yes', help='Download genome reports, contigs, and annotations data.  Note: cannot execute blast unless assembly and annotate pipeline has been previously performed', )
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify output folder for downloaded data.')
args=parser.parse_args()
#login
print 'Enter password to log into PATRIC...'
os.system('p3-login ' + str(args.username) + ' > patric_domain.txt')
patric_domain = open('patric_domain.txt', "rb").readlines()[1].replace('Logged in with username ', '').rstrip()
#metadata lists
df_reads = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['R1','R2','genome_name_reads'])
R1_list = df_reads['R1'].dropna().tolist()
R2_list = df_reads['R2'].dropna().tolist()
genome_name_list_reads = df_reads['genome_name_reads'].dropna().tolist()
df_contigs = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['contigs','genome_name_contigs'])
contigs_list = df_contigs['contigs'].dropna().tolist()
genome_name_list_contigs = df_contigs['genome_name_contigs'].dropna().tolist()

#upload data
if str(args.input_files) == 'yes':
	for R1 in R1_list:
		print 'Uploading ' + str(R1)
		os.system('p3-cp ' + str(R1) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
	for R2 in R2_list:
		print 'Uploading ' + str(R2)
		os.system('p3-cp ' + str(R2) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
	for contigs in contigs_list:
		print 'Uploading ' + str(contigs)
		os.system('p3-cp ' + str(contigs) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
#assembly annotate
if str(args.assembly_annotate) == 'yes': #do not need to specify if reads or contigs or both.  PATRIC will not execute job if not data.
#reads
	df_reads = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['R1','R2','genome_name_reads']).replace(' ','_', regex=True)
	R1_list = df_reads['R1'].dropna().tolist()
	R2_list = df_reads['R2'].dropna().tolist()
	zip(R1_list,R2_list,genome_name_list_reads)
	for R1, R2, genome_name in zip(R1_list,R2_list,genome_name_list_reads):
		in_file = open('params_reads.json', "rb")
		out_file = open('params_reads_out.json', "wb")
		reader = in_file.read()
		repls1= (('R1', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(R1)),('R2', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(R2)),('Genome_name_path', '/' + str(patric_domain) + '/home/AssemblyJob'),('Genome_name',str(genome_name)),)
		writer1 = reduce(lambda a, kv: a.replace(*kv), repls1, reader)
		writer2 = out_file.write(writer1)
		in_file.close()
		out_file.close()
		os.system('appserv-start-app ComprehensiveGenomeAnalysis params_reads_out.json \"parrello@patricbrc.org/home/\"'+ ' > ' + str(genome_name) + '_job_ID.txt')
		job_id = open(str(genome_name) + '_job_ID.txt', "rb").readline().replace('Started task ', '').rstrip()
		print "Comprehensive Genome Analysis job sent for " + str(genome_name) + ' as job id ' + job_id
#contigs
	df_contigs = pd.read_csv(str(args.metadata_table), sep='\t', usecols=['contigs','genome_name_contigs']).replace(' ','_', regex=True)
	contigs_list = df_contigs['contigs'].dropna().tolist()
	genome_name_list_contigs = df_contigs['genome_name_contigs'].dropna().tolist()
	zip(contigs_list,genome_name_list_contigs)
	for contigs, genome_name in zip(contigs_list,genome_name_list_contigs):
		in_file = open('params_contigs.json', "rb")
		out_file = open('params_contigs_out.json', "wb")
		reader = in_file.read()
		repls1= (('contigs_path', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(contigs)),('out_path', '/' + str(patric_domain) + '/home/AssemblyJob'),('Genome_name',str(genome_name)))
		writer1 = reduce(lambda a, kv: a.replace(*kv), repls1, reader)
		writer2 = out_file.write(writer1)
		in_file.close()
		out_file.close()
		os.system('appserv-start-app ComprehensiveGenomeAnalysis params_contigs_out.json \"parrello@patricbrc.org/home/\"'+ ' > ' + str(genome_name) + '_job_ID.txt')
		job_id = open(str(genome_name) + '_job_ID.txt', "rb").readline().replace('Started task ', '').rstrip()
		print "Comprehensive Genome Analysis job sent for " + str(genome_name) + ' as job id ' + job_id
#check job
	genome_name_list = genome_name_list_reads + genome_name_list_contigs
	for genome_name in genome_name_list:
		job_id2 = open(str(genome_name) + '_job_ID.txt', "rb").readline().replace('Started task ', '').rstrip()
		print job_id2
		while True:
			os.system('p3-job-status' + ' ' + job_id2 + ' > ' + str(genome_name) + '_job_status.txt')
			job_id_status = open(str(genome_name) + '_job_status.txt', "rb").readline().rstrip()
			print 'Checking status of ' + str(genome_name) + ' as job id ' + job_id_status
			t = time.localtime()
			current_time = time.strftime('%H:%M:%S', t)
			print current_time
			if job_id_status == job_id2 + ': completed':
				break
			time.sleep(300) #check status of first jobs every 300 seconds (ie 5 minutes)
		print 'Comprehensive Genome Analysis done for ' + str(genome_name)
#download data
if str(args.download_reports) == 'yes':
	for genome_name in genome_name_list:
		if not os.path.exists(str(args.output_folder)):
			os.mkdir(str(args.output_folder))
		os.system('p3-cp ws:\"/' + str(patric_domain) + '/home/AssemblyJob/.' + str(genome_name) + '/FullGenomeReport.html\"' + ' ' + str(args.output_folder) +'/'+str(genome_name) + '_FullGenomeReport.html')
		os.system('p3-cp ws:\"/' + str(patric_domain) + '/home/AssemblyJob/.' + str(genome_name) + '/.annotation/annotation.contigs.fasta\"' + ' ' + str(args.output_folder) +'/'+str(genome_name) + '_contigs.fasta')
		os.system('p3-cp ws:\"/' + str(patric_domain) + '/home/AssemblyJob/.' + str(genome_name) + '/.annotation/annotation.txt\"' + ' ' + str(args.output_folder) +'/'+str(genome_name) + '_annotation.txt')
		os.system('p3-cp ws:\"/' + str(patric_domain) + '/home/AssemblyJob/.' + str(genome_name) + '/.annotation/annotation.feature_protein.fasta\"' + ' ' + str(args.output_folder) +'/'+str(genome_name) + '_protein.fasta')
		os.system('p3-cp ws:\"/' + str(patric_domain) + '/home/AssemblyJob/.' + str(genome_name) + '/.annotation/annotation.feature_dna.fasta\"' + ' ' + str(args.output_folder) +'/'+str(genome_name) + '_DNA.fasta')
		#add column with genome name
		df = pd.read_csv(str(args.output_folder) +'/'+str(genome_name) + '_annotation.txt', sep='\t')
		df['genome_name']=str(genome_name)
		column_order = ['genome_name','contig_id','feature_id','type','location','start','stop','strand','function','aliases','plfam','pgfam','figfam','evidence_codes','nucleotide_sequence','aa_sequence']
		df[column_order].to_csv(str(args.output_folder) +'/'+str(genome_name) + '_annotation.txt', sep='\t', index=False)

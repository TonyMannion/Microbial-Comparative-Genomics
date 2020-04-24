import os
import time
import glob
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', dest='username', help='Provide username for PATRIC account. Prompt to enter password will appear.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
parser.add_argument('-f', '--upload_files', dest='upload_files', default = 'yes', help='Upload read and/or contig files? Enter "yes" or "no". Default is "yes". If file with same name has already been upload to PATRIC, it will be overwritten by file upload here.')
parser.add_argument('-a', '--assembly_annotate', dest='assembly_annotate', default = 'yes', help='Execute assembly and annotate pipeline? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-c', '--check_job', dest='check_job', default = 'yes', help='Check status of assemlby/annotation job? Enter "yes" or "no". Default is "yes".  When job is complete, genome reports, contigs, and annotations data will be downloaded to output folder.')
parser.add_argument('-d', '--download_reports', dest='download_reports', default = 'yes', help='Download genome reports, contigs, and annotations data for assembled/annotated genomes? Enter "yes" or "no". Default is "no". Use this flag to download data from previously completed jobs.')
parser.add_argument('-p', '--patric_download', dest='patric_dl', default = 'yes', help='Download genome reports, contigs, and annotations data from PATRIC genomes.')
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify output folder for downloaded data.')
args=parser.parse_args()

#login
print 'Enter password to log into PATRIC...'
os.system('p3-login ' + str(args.username) + ' > patric_domain_temp_genome_assemlby_annotation.txt')
patric_domain = open('patric_domain_temp_genome_assemlby_annotation.txt', "rb").readlines()[1].replace('Logged in with username ', '').rstrip()
#download from patric
if str(args.patric_dl) == 'yes':
	df_genome_names = pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_ids_patric','genome_name_patric']).replace(' ','_', regex=True)
	genome_ids_list = df_genome_names['genome_ids_patric'].dropna().tolist()
	genome_name_list = df_genome_names['genome_name_patric'].dropna().tolist()
	zip(genome_ids_list,genome_name_list)
	for genome_id,genome_name in zip(genome_ids_list,genome_name_list): 
		print 'Downloading data for '+str(genome_id)+' '+str(genome_name)+' from PATRIC...'
		if not os.path.exists(str(args.output_folder)):
			os.mkdir(str(args.output_folder))
		os.system('p3-echo -t genome_id '+str(genome_id)+' | p3-get-genome-features --in feature_type,CDS,rna --attr genome_name --attr sequence_id --attr patric_id --attr start --attr end --attr strand --attr product --attr pgfam_id --attr na_sequence --attr aa_sequence > '+str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt')
		df_genome = pd.read_csv(str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t')
		df_genome2=df_genome.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam','feature.patric_id':'feature_id'})
		df_genome2['genome_name'].replace(' ','_', regex=True, inplace=True)
		df_genome2.to_csv(str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t',index=False)
		os.system('p3-genome-fasta --contig '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_contigs.fasta')
		os.system('p3-genome-fasta --protein '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_protein.fasta')
		os.system('p3-genome-fasta --feature '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_DNA.fasta')
#upload data
if str(args.upload_files) == 'yes':
	df_reads = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['R1','R2','genome_name_reads'])
	R1_list = df_reads['R1'].dropna().tolist()
	R2_list = df_reads['R2'].dropna().tolist()
	df_contigs = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['contigs','genome_name_contigs'])
	contigs_list = df_contigs['contigs'].dropna().tolist()
	for R1 in R1_list:
		print 'Uploading ' + str(R1) + ' to PATRIC...'
		os.system('p3-cp ' + str(R1) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
	for R2 in R2_list:
		print 'Uploading ' + str(R2) + ' to PATRIC...'
		os.system('p3-cp ' + str(R2) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
	for contigs in contigs_list:
		print 'Uploading ' + str(contigs) + ' to PATRIC...'
		os.system('p3-cp ' + str(contigs) + ' ws:/' + str(patric_domain) + '/home/AssemblyJob -f')
#assembly annotate
if str(args.assembly_annotate) == 'yes':
#reads
	df_reads = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['R1','R2','genome_name_reads']).replace(' ','_', regex=True)
	R1_list = df_reads['R1'].dropna().tolist()
	R2_list = df_reads['R2'].dropna().tolist()
	genome_name_list_reads = df_reads['genome_name_reads'].dropna().tolist()
	zip(R1_list,R2_list,genome_name_list_reads)
	for R1, R2, genome_name in zip(R1_list,R2_list,genome_name_list_reads):
		in_file = open('params_reads.json', "rb")
		out_file = open('params_reads_out_temp_genome_assemlby_annotation.json', "wb")
		reader = in_file.read()
		repls1= (('R1', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(R1)),('R2', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(R2)),('Genome_name_path', '/' + str(patric_domain) + '/home/AssemblyJob'),('Genome_name',str(genome_name)),)
		writer1 = reduce(lambda a, kv: a.replace(*kv), repls1, reader)
		writer2 = out_file.write(writer1)
		in_file.close()
		out_file.close()
		os.system('appserv-start-app ComprehensiveGenomeAnalysis params_reads_out_temp_genome_assemlby_annotation.json \"parrello@patricbrc.org/home/\"'+ ' > ' + str(genome_name) + '_job_ID_temp_genome_assemlby_annotation.txt')
		job_id = open(str(genome_name) + '_job_ID_temp_genome_assemlby_annotation.txt', "rb").readline().replace('Started task ', '').rstrip()
		print "Comprehensive Genome Analysis job sent for " + str(genome_name) + ' as job id ' + job_id
#contigs
	df_contigs = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['contigs','genome_name_contigs']).replace(' ','_', regex=True)
	contigs_list = df_contigs['contigs'].dropna().tolist()
	genome_name_list_contigs = df_contigs['genome_name_contigs'].dropna().tolist()
	zip(contigs_list,genome_name_list_contigs)
	for contigs, genome_name in zip(contigs_list,genome_name_list_contigs):
		in_file = open('params_contigs.json', "rb")
		out_file = open('params_contigs_out_temp_genome_assemlby_annotation.json', "wb")
		reader = in_file.read()
		repls1= (('contigs_path', '/' + str(patric_domain) + '/home/AssemblyJob/' + str(contigs)),('out_path', '/' + str(patric_domain) + '/home/AssemblyJob'),('Genome_name',str(genome_name)))
		writer1 = reduce(lambda a, kv: a.replace(*kv), repls1, reader)
		writer2 = out_file.write(writer1)
		in_file.close()
		out_file.close()
		os.system('appserv-start-app ComprehensiveGenomeAnalysis params_contigs_out_temp_genome_assemlby_annotation.json \"parrello@patricbrc.org/home/\"'+ ' > ' + str(genome_name) + '_job_ID_temp_genome_assemlby_annotation.txt')
		job_id = open(str(genome_name) + '_job_ID_temp_genome_assemlby_annotation.txt', "rb").readline().replace('Started task ', '').rstrip()
		print "Comprehensive Genome Analysis job sent for " + str(genome_name) + ' as job id ' + job_id
#check job
if str(args.check_job) == 'yes':
	df_reads = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['R1','R2','genome_name_reads']).replace(' ','_', regex=True)
	genome_name_list_reads = df_reads['genome_name_reads'].dropna().tolist()
	df_contigs = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['contigs','genome_name_contigs']).replace(' ','_', regex=True)
	genome_name_list_contigs = df_contigs['genome_name_contigs'].dropna().tolist()
	genome_name_list = genome_name_list_reads + genome_name_list_contigs
	for genome_name in genome_name_list:
		job_id2 = open(str(genome_name) + '_job_ID_temp_genome_assemlby_annotation.txt', "rb").readline().replace('Started task ', '').rstrip()
		while True:
			os.system('p3-job-status' + ' ' + job_id2 + ' > ' + str(genome_name) + '_job_status_temp_genome_assemlby_annotation.txt')
			job_id_status = open(str(genome_name) + '_job_status_temp_genome_assemlby_annotation.txt', "rb").readline().rstrip()
			print 'Checking status of ' + str(genome_name) + ' as job id ' + job_id_status
			t = time.localtime()
			current_time = time.strftime('%H:%M:%S', t)
			print 'Current time: ' + current_time
			if job_id_status == job_id2 + ': completed':
				break
			time.sleep(300) #check status of first jobs every 300 seconds (ie 5 minutes)
		print 'Comprehensive Genome Analysis done for ' + str(genome_name)
		#download data
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
#download data
if str(args.download_reports) == 'yes':
	df_reads = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['R1','R2','genome_name_reads']).replace(' ','_', regex=True)
	genome_name_list_reads = df_reads['genome_name_reads'].dropna().tolist()
	df_contigs = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['contigs','genome_name_contigs']).replace(' ','_', regex=True)
	genome_name_list_contigs = df_contigs['genome_name_contigs'].dropna().tolist()
	genome_name_list = genome_name_list_reads + genome_name_list_contigs
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
#delete temp files
temp_filter_files=glob.glob('*_temp_genome_assemlby_annotation.txt')
for temp_file in temp_filter_files:
	os.remove(str(temp_file))

import pandas as pd
import numpy as np
import sys 
import os
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file. If using annotation metadata files, provide genome names of interest with under the header "genome_names". If downloading features from PATRIC, provide genome ids of interest under the header "genome_ids".')
parser.add_argument('-a', '--annotations', dest='annotations', default = 'yes', help='Peform median gene count analysis on annotations files? Enter "yes" or "no". Requires annotations files obtained from "full_genome_analysis.py" script.')
parser.add_argument('-d', '--downlaod_patric_features', dest='downlaod_patric_features', default = 'no', help='Download features from PATRIC? Enter "yes" or "no". Default is "yes". If features have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-username', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')

#download features
args=parser.parse_args()

#gene analysis function
def median_analysis(input_file):
	#input concatenated dataframe with gene families
	df_concat = pd.read_csv(str(input_file),sep='\t')
	df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
	#groupby
	df_concat2['count']=1
	df_groupby = df_concat2.groupby(['genome_name', 'pgfam'], as_index=False).sum().pivot(columns = 'genome_name', index = 'pgfam', values = 'count').fillna(0).to_csv('gene_family_groupby_out.txt', sep='\t') 
	print 'Output gene family groupby dataframe...'
	df_groupby2=pd.read_csv('gene_family_groupby_out.txt', sep='\t')
	#median cacluations
	for col in df_groupby2.columns[1:]:
		df_temp=pd.DataFrame()
		df_temp['pgfam']=df_groupby2['pgfam']
		df_temp['genome_name']= str(col)
		df_temp['genome_name_pgfam']=df_temp['genome_name'] + '_' + df_temp['pgfam']
		df_temp['gene_count']=df_groupby2[col]
		df_temp['median']=df_groupby2.median(axis=1)
		df_temp['gene_count-median']=df_groupby2[col]-df_temp['median']
		conditions=[(df_temp['gene_count']==df_temp['median']),(df_temp['gene_count'] > df_temp['median']), (df_temp['gene_count'] < df_temp['median'])]
		choices=['equal to median', 'greater than median', 'less than median']
		df_temp['vs_median']=np.select(conditions, choices, default='unknown')
		#merge median calculations with annotation metadata
		df_concat2['genome_name_pgfam']=df_concat2['genome_name'] + '_' + df_concat2['pgfam']
		#annotation metadata
		df_merged=pd.merge(df_temp, df_concat2, left_on='genome_name_pgfam', right_on='genome_name_pgfam', how="left").rename(columns={'genome_name_y': 'genome_name', 'pgfam_x':'pgfam'}).drop(['pgfam_y', 'genome_name_x','genome_name_pgfam','count'], axis=1)
		cols = list(df_merged.columns)
		cols = cols[5:] + cols[0:5]#rearranges first 4 cols to end
		df_merged2 = df_merged[cols].to_csv(str(col)+'_annotation.txt', sep='\t', index=False)
		print "Output gene counts merged to annotation metadata for " + str(col) +'...'

#download features from PATRIC
if str(args.downlaod_patric_features) == 'yes':
	print 'Logging into PATRIC...'
	os.system('p3-login ' + str(args.username))
	df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_ids','genome_name'])
	genome_ids_list = df_genome_names['genome_ids'].dropna().tolist()
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	zip(genome_ids_list,genome_name_list)
	for genome_id, genome_name in zip(genome_ids_list,genome_name_list): 
		print 'Downloading features for ' + str(genome_id)+ ' ' + str(genome_name) + ' from PATRIC...'
		os.system('p3-echo -t genome_id ' + str(genome_id) + ' | p3-get-genome-features --in feature_type,CDS,rna --attr genome_name --attr sequence_id --attr patric_id --attr start --attr end --attr strand --attr product --attr pgfam_id --attr na_sequence --attr aa_sequence  > ' + str(genome_name) +'_annotation.txt')
	df_concat = pd.concat([pd.read_csv(str(genome_name) + '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
	df_concat2.to_csv('concatenated_annotations.txt',  sep='\t', index=False)

#cluster map from annotation metadata
if str(args.annotations) == 'yes':
	print "Performing gene analysis..." 
	if os.path.isfile('concatenated_annotations.txt'):
		print 'file already found'
		median_analysis('concatenated_annotations.txt')
	else:
		print 'making file'
		df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_name'])
		genome_name_list = df_genome_names['genome_name'].dropna().tolist()
		df_concat = pd.concat([pd.read_csv(str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
		df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
		df_concat2.to_csv('concatenated_annotations.txt',  sep='\t', index=False)
		median_analysis('concatenated_annotations.txt')

os.remove('concatenated_annotations.txt')
os.remove('gene_family_groupby_out.txt')

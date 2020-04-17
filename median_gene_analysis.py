import pandas as pd
import numpy as np
import sys 
import os
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('-a', '--annotations', dest='annotations', default='no', help='Peform median gene count analysis on annotations files? Enter "yes" or "no". Requires annotations files obtained from "full_genome_analysis.py" script.')
parser.add_argument('-p', '--PATRIC_features', dest='PATRIC_features', default='no', help='Peform median gene count analysis on PATRIC features? Enter "yes" or "no". Requires features file for genomes of interest downloaded from PATRIC from "downlaod_patric_features" argument above.')
parser.add_argument('-d', '--downlaod_patric_features', dest='downlaod_patric_features', default='no', help='Download features from PATRIC? Enter "yes" or "no". Default is "yes". If features have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-username', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')
parser.add_argument('-f', '--features_file', dest='features_file', default='features.txt', help='If features will be or have been downloaded PATRIC, specify the desired the features file name.')
parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file containing PATRIC genome ids of interest or file names for annotations files. Header is "Genomes" and each genome id is on different row.')

#download features
args=parser.parse_args()

#gene analysis function
def median_analysis(input_file, genome_name, feature_type):
	#input dataframe with gene families
	df_concat=pd.read_csv(str(input_file),  sep='\t')
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby([str(genome_name), str(feature_type)], as_index=False).sum().pivot(columns=str(genome_name), index=str(feature_type), values='count').fillna(0).to_csv('gene_family_groupby_out.txt', sep='\t') 
	print 'Output gene family groupby dataframe...'
	df_groupby2=pd.read_csv('gene_family_groupby_out.txt', sep='\t')
	#median cacluations
	for col in df_groupby2.columns[1:]:
		df_temp=pd.DataFrame()
		df_temp['pgfam_id']=df_groupby2[str(feature_type)]
		df_temp['genome_name']= str(col)
		df_temp['genome_name_pgfam']=df_temp['genome_name'] + '_' + df_temp['pgfam_id']
		df_temp['gene_count']=df_groupby2[col]
		df_temp['median']=df_groupby2.median(axis=1)
		df_temp['gene_count-median']=df_groupby2[col]-df_temp['median']
		conditions=[(df_temp['gene_count']==df_temp['median']),(df_temp['gene_count'] > df_temp['median']), (df_temp['gene_count'] < df_temp['median'])]
		choices=['equal to median', 'greater than median', 'less than median']
		df_temp['vs_median']=np.select(conditions, choices, default='unknown')
		#merge median calculations with annotation metadata
		df_concat['genome_name_pgfam']=df_concat[str(genome_name)] + '_' + df_concat[str(feature_type)]
		#annotation metadata
		if  str(args.annotations)=='yes':
			df_merged=pd.merge(df_temp, df_concat, left_on='genome_name_pgfam', right_on='genome_name_pgfam', how="left").rename(columns={'genome_name_x': 'genome_name'})
			column_order=['genome_name','contig_id','feature_id','type','location','start','stop','strand','function','aliases','plfam','pgfam','figfam','evidence_codes','nucleotide_sequence','aa_sequence','gene_count','median','gene_count-median','vs_median']
			df_merged[column_order].to_csv(str(col)+'_annotation.txt', sep='\t', index=False)
			print "Output gene counts merged to annotation metadata for " + str(col) +'...'
		#PATRIC features
		elif str(args.PATRIC_features)=='yes':
			df_merged=pd.merge(df_temp, df_concat, left_on='genome_name_pgfam', right_on='genome_name_pgfam', how="left").rename(columns={'pgfam_id': 'pgfam'})
			column_order=['genome_name','feature.patric_id','feature.gene_id','pgfam','feature.product','gene_count','median','gene_count-median','vs_median']
			df_merged[column_order].to_csv(str(col)+'_annotation.txt', sep='\t', index=False)
			print "Output gene counts merged to annotation metadata for " + str(col) +'...'

#median analysis from annotation metadata
if str(args.annotations) == 'yes':
	print "Performing gene analysis..." 
	#concatenate
	df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_name'])
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	df_concat = pd.concat([pd.read_csv(str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat.to_csv('concatenated_annotations.txt',  sep='\t', index=False)
	#Execute gene analysis function
	median_analysis('concatenated_annotations.txt', 'genome_name', 'pgfam')

#download features from PATRIC
if str(args.downlaod_patric_features) == 'yes':
	print 'Logging into PATRIC...'
	os.system('p3-login ' + str(args.username))
	print 'Downloading features from PATRIC...'
	os.system('p3-get-genome-features --input ' + str(args.metadata_file) + ' --attr genome_name --attr patric_id --attr gene_id --attr pgfam_id --attr product > ' + str(args.features_file))

#median analysis from PATRIC features
if str(args.PATRIC_features) == 'yes':
	#Execute gene analysis function
	print "Performing gene analysis..."
	median_analysis(args.features_file, 'feature.genome_name', 'feature.pgfam_id')

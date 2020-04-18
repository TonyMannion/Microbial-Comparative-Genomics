import os
from os import path
import argparse
import sys
import glob
import pandas as pd
import numpy as np

parser=argparse.ArgumentParser()

parser.add_argument('-i', '--input_folder', dest='input_folder', help='Specify folder with annotations. If downloading annotations from PATRIC, this will create folder for files.')
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify output folder.')
parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file. If using annotation metadata files, provide genome names of interest with under the header "genome_names". If downloading features from PATRIC, provide genome ids of interest under the header "genome_ids".')
parser.add_argument('-d', '--downlaod_patric_features', dest='downlaod_patric_features', default = 'no', help='Download annotations from PATRIC? Enter "yes" or "no". Default is "yes". If annotations have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-username', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')

args=parser.parse_args()

#subgroup genes filter function
def subgroup_genes(input_file):
	#input concatenated dataframe with gene families
	df_concat = pd.read_csv(output_folder +'/'+ str(input_file),sep='\t')
	df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
	#groupby
	df_concat2['count']=1
	df_groupby = df_concat2.groupby(['genome_name', 'pgfam'], as_index=False).sum().pivot(columns = 'genome_name', index = 'pgfam', values = 'count').fillna(0).to_csv(output_folder +'/'+ 'gene_family_groupby_out.txt', sep='\t') 
	print 'Output gene family groupby dataframe...'
	#make lists from metadata
	df_metadata = pd.read_csv(str(args.metadata_file), sep='\t')
	subgroup_list=df_metadata['subgroup'].dropna().tolist()
	genome_name_list=df_metadata['genome_name'].dropna().tolist()
	#subgroups
	for subgroup in subgroup_list:
		genome_list_include = df_metadata['include_' + str(subgroup)].dropna().tolist()
		genome_list_exclude = df_metadata['exclude_' + str(subgroup)].dropna().tolist()
		df = pd.read_csv(output_folder +'/'+ 'gene_family_groupby_out.txt', sep='\t')
		for genome in genome_list_include:
			df=df[df[str(genome)]>0]
		for genome in genome_list_exclude:
			df= df[df[str(genome)]<=0]
		df['subgroup_gene']=str(subgroup)
		df2 = df.iloc[:,[0,-1]].to_csv(output_folder +'/'+ 'temp_' + str(subgroup) + '_filter_out.txt', sep='\t',index=False)
	#concat
	temp_filter_files = glob.glob(output_folder +'/'+ 'temp_' + '*_filter_out.txt')
	df_concat = pd.concat([pd.read_csv(temp_file,sep='\t') for temp_file in temp_filter_files])
	#delete temp files
	for temp_file in temp_filter_files:
		os.remove(str(temp_file))
	#merge
	for genome in genome_name_list:
		df_an = pd.read_csv(str(args.input_folder) +'/'+ str(genome)+'_annotation.txt', sep='\t')
		df_merged = pd.merge(df_an, df_concat, left_on='pgfam', right_on='pgfam', how="left").to_csv(output_folder +'/'+str(genome)+'_annotation.txt',  sep='\t', index=False)
		print 'Done with '+ str(genome)

#make output folder
output_folder = 'subgroup_gene_analysis_' + str(args.output_folder)
os.mkdir(output_folder)

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
		#make input folder if not already present
		if not os.path.exists(str(args.input_folder)):
			os.mkdir(str(args.input_folder))
		os.system('p3-echo -t genome_id ' + str(genome_id) + ' | p3-get-genome-features --in feature_type,CDS,rna --attr genome_name --attr sequence_id --attr patric_id --attr start --attr end --attr strand --attr product --attr pgfam_id --attr na_sequence --attr aa_sequence  > ' + str(args.input_folder) +'/'+str(genome_name) +'_annotation.txt')
		df_genome = pd.read_csv(str(args.input_folder) +'/'+str(genome_name) +'_annotation.txt', sep='\t')
		df_genome2=df_genome.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'})
		df_genome2.to_csv(str(args.input_folder) +'/'+str(genome_name) +'_annotation.txt', sep='\t', index=False)
	df_concat = pd.concat([pd.read_csv(str(args.input_folder) +'/'+str(genome_name) + '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
	df_concat2.to_csv(output_folder +'/'+'concatenated_annotations.txt',  sep='\t', index=False)

#subgroup gene analysis
print "Performing gene analysis..." 
if os.path.isfile(output_folder +'/'+ 'concatenated_annotations.txt'):
	print 'file already found'
	subgroup_genes('concatenated_annotations.txt')
else:
	print 'making file'
	df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_name'])
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	df_concat = pd.concat([pd.read_csv(str(args.input_folder) +'/'+ str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat2 = df_concat.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam'}) #clean up headers
	df_concat2.to_csv(output_folder +'/'+ 'concatenated_annotations.txt',  sep='\t', index=False)
	subgroup_genes('concatenated_annotations.txt')
#remove intermediate files
os.remove(output_folder +'/'+ 'concatenated_annotations.txt')
os.remove(output_folder +'/'+ 'gene_family_groupby_out.txt')

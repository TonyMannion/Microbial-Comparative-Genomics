import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import sys 
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--annotations', dest='annotations', default = 'no', help='Peform median gene count analysis on annotations files? Enter "yes" or "no". Requires annotations files obtained from "full_genome_analysis.py" script.')
parser.add_argument('-p', '--PATRIC_features', dest='PATRIC_features', default = 'no', help='Peform median gene count analysis on PATRIC features? Enter "yes" or "no". Requires features file for genomes of interest downloaded from PATRIC from "downlaod_patric_features" argument above.')
parser.add_argument('-d', '--downlaod_patric_features', dest='downlaod_patric_features', default = 'no', help='Download features from PATRIC? Enter "yes" or "no". Default is "yes". If features have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-username', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')
parser.add_argument('-f', '--features_file', dest='features_file', default = 'features.txt', help='If features will be or have been downloaded PATRIC, specify the desired the features file name.')
parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file. If using annotation metadata files, provide genome names of interest with under the header "genome_names". If downloading features from PATRIC, provide genome ids of interest under the header "genome_ids".')

args = parser.parse_args()

#gene analysis function
def make_clustermap(input_file, genome_name, feature_type):
	#input concatenated dataframe with gene families
	df_concat = pd.read_csv(str(input_file),  sep='\t')
	#groupby
	df_concat['count']=1
	df_concat2 = df_concat.rename(columns={str(feature_type): 'pgfam'})
	df_groupby = df_concat2.groupby([str(genome_name), 'pgfam'], as_index=False).sum().pivot(columns = str(genome_name), index = 'pgfam', values = 'count').fillna(0)
	print 'Output gene family groupby dataframe...'
	df_cm = df_groupby.transpose()
	print "Generating clustermap..."
	sys.setrecursionlimit(10**6) 
	df_cm = df_cm.rename_axis('', axis='rows')
	#11 hex codes for colors: off-white, red, orange, yellow, green, blue, purple, pink, gray, brown, black
	custom_cmap = ['#fdf8ef', '#ff7f7f', '#ffa500', '#ffff66', '#008000', '#0000ff', '#814ca7', '#ee82ee', '#808080', '#a5682a', '#000000']
	sns.set_palette(custom_cmap)
	cm = sns.clustermap(df_cm, cmap=custom_cmap, vmin=0, vmax=10, xticklabels=False, figsize=(25,10), cbar_kws={"ticks":[0,1,2,3,4,5,6,7,8,9,10], "label":('0 to 10+ genes per gene family')})
	cm.ax_col_dendrogram.set_visible(False)
	plt.savefig('clustermap.png', dpi=300)
	plt.clf()
	#save clustermap dataframe
	print "Output clustermap dataframe..."
	df_cm2 = pd.DataFrame(cm.data2d).transpose()
	df_cm2.to_csv('gene_family_clustermap_out.txt', sep='\t')

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
	df_concat = pd.concat([pd.read_csv(str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat.to_csv('concatenated_annotations.txt',  sep='\t', index=False)

#cluster map from PATRIC features
if str(args.PATRIC_features) == 'yes':
	#Execute gene analysis function
	print "Performing gene analysis..."
	make_clustermap('concatenated_annotations.txt', 'feature.genome_name', 'feature.pgfam_id')

#cluster map from annotation metadata
if str(args.annotations) == 'yes':
	print "Performing gene analysis..." 
	#concatenate
	df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_name'])
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	df_concat = pd.concat([pd.read_csv(str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat.to_csv('concatenated_annotations.txt',  sep='\t', index=False)
	#Execute gene analysis function
	make_clustermap('concatenated_annotations.txt', 'genome_name', 'pgfam')

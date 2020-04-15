import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import sys 
import os
import argparse
import glob

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--annotations', dest='annotations', default = 'no', help='Peform median gene count analysis on annotations files? Enter "yes" or "no". Requires annotations files obtained from "full_genome_analysis.py" script.')
parser.add_argument('-p', '--PATRIC_features', dest='PATRIC_features', default = 'no', help='Peform median gene count analysis on PATRIC features? Enter "yes" or "no". Requires features file for genomes of interest downloaded from PATRIC from "downlaod_patric_features" argument above.')
parser.add_argument('-d', '--downlaod_patric_features', dest='downlaod_patric_features', default = 'no', help='Download features from PATRIC? Enter "yes" or "no". Default is "yes". If features have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-username', '--username', dest='username', help='If downloading from PATRIC, enter PATRIC login username.')
parser.add_argument('-o', '--features_file', dest='features_file', default = 'features.txt', help='If features will be or have been downloaded PATRIC, specify the desired the features file name.')
parser.add_argument('-m', '--metadata_file', dest='metadata_file', help='Specify metadata file containing PATRIC genome ids of interest or file names for annotations files. Header is "Genomes" and each genome id is on different row.')
parser.add_argument('-f', '--feature_type', dest='feature_type', default = 'feature.pgfam_id', help='Specificy count column for gene family from feature file.  Choose "pgfam" for global protein family (cross-genus, called PGfam) or "plfam" for local protein family (genus-specific, called PLfam).  Default is "feature.pgfam_id" for global protein family (cross-genus, called PGfam).')
parser.add_argument('-cm', '--clustermap', dest='clustermap', default = 'yes', help='Generate clustermap of gene families. Enter "yes" or "no". Default is "yes".')

#download features
args = parser.parse_args()

if str(args.downlaod_patric_features) == 'yes':
	print 'Logging into PATRIC...'
	os.system('p3-login ' + str(args.username))
	print 'Downloading features from PATRIC...'
	os.system('p3-get-genome-features --input ' + str(args.metadata_file) + ' --attr genome_name --attr patric_id --attr gene_id --attr plfam_id --attr pgfam_id --attr product > ' + str(args.features_file))

#gene analysis function
def gene_analysis(input_file, genome_name, feature_type):
	#input dataframe with gene families
	df_merged = pd.read_csv(str(input_file),  sep='\t')
	#groupby
	df_merged['count']=1
	df_groupby = df_merged.groupby([str(genome_name), str(feature_type)], as_index=False).sum().pivot(columns = str(genome_name), index = str(feature_type), values = 'count').fillna(0).to_csv('gene_family_groupby_out.txt', sep='\t') 
	print 'Output gene family groupby dataframe...'
	df_groupby2 = pd.read_csv('gene_family_groupby_out.txt', sep='\t')
	#median
	for col in df_groupby2.columns[1:]:
		df_temp = pd.DataFrame()
		df_temp['pgfam_id']=df_groupby2[str(feature_type)]
		df_temp['genome']= str(col)
		df_temp['genome_name_pgfam']=df_temp['genome'] + '_' + df_temp['pgfam_id']
		df_temp['gene_count']=df_groupby2[col]
		df_temp['median']=df_groupby2.median(axis=1)
		df_temp['gene_count-median']=df_groupby2[col]-df_temp['median']
		conditions = [(df_temp['gene_count'] == df_temp['median']),(df_temp['gene_count'] > df_temp['median']), (df_temp['gene_count'] < df_temp['median'])]
		choices = ['equal to median', 'greater than median', 'less than median']
		df_temp['category'] = np.select(conditions, choices, default='unknown')
	#merge median calculations with annotations
		df_merged['genome_name_pgfam']=df_merged[str(genome_name)] + '_' + df_merged[str(feature_type)]
		df_merged2 = pd.merge(df_temp, df_merged, left_on='genome_name_pgfam', right_on='genome_name_pgfam', how="left")
		if str(args.PATRIC_features) == 'yes':
			column_order = ['genome', 'Genome ID','feature.patric_id','feature.gene_id','feature.plfam_id','pgfam_id','feature.product','gene_count','median','gene_count-median','category']
			df_merged2[column_order].to_csv(str(col)+'_median_gene_analysis.txt', sep='\t', index=False)
			print "Output gene counts merged to annotation metadata for " + str(col) +'...'
		elif str(args.annotations) == 'yes':
			column_order = ['genome','contig_id','feature_id','type','location','start','stop','strand','function','aliases','plfam','pgfam_id','figfam','evidence_codes','nucleotide_sequence','aa_sequence','gene_count','median','gene_count-median','category']
			df_merged2[column_order].to_csv(str(col)+'_median_gene_analysis.txt', sep='\t', index=False)
			print "Output gene counts merged to annotation metadata for " + str(col) +'...'
	#clustermap figure
	if str(args.clustermap) == 'yes':
		print "Generating clustermap..."
		sys.setrecursionlimit(10**6) 
		df_cm = pd.read_csv('gene_family_groupby_out.txt', sep='\t', index_col=0).transpose()
		df_cm = df_cm.rename_axis("Gene Family", axis="columns")
		#11 hex codes for colors: off-white, red, orange, yellow, green, blue, purple, pink, gray, brown, black
		custom_cmap = ['#fdf8ef', '#ff7f7f', '#ffa500', '#ffff66', '#008000', '#0000ff', '#814ca7', '#ee82ee', '#808080', '#a5682a', '#000000']
		sns.set_palette(custom_cmap)
		cm = sns.clustermap(df_cm, cmap=custom_cmap, vmin=0, vmax=10, xticklabels=False, figsize=(25,10), cbar_kws={"ticks":[0,1,2,3,4,5,6,7,8,9,10], "label":('0 to 10+ genes per gene family')})
		cm.ax_col_dendrogram.set_visible(False)
		plt.savefig('clustermap.png', dpi=300)
		plt.clf()
		#save clustermap dataframe
		print "Output clustermap dataframe..."
		df_cm2 = pd.DataFrame(cm.data2d)
		df_cm2.to_csv('gene_family_clustermap_out.txt', sep='\t')

if str(args.PATRIC_features) == 'yes':
	#Execute gene analysis function
	print "Performing gene analysis..."
	gene_analysis(args.features_file, 'feature.genome_name', args.feature_type)

if str(args.annotations) == 'yes':
	print "Performing gene analysis..."
	#add genome name and rename file
	df_annotation_files = pd.read_csv(str(args.metadata_file), sep='\t')
	df2_annotation_files = df_annotation_files.dropna()
	annotation_files_list = df2_annotation_files['genome_name'].tolist() #metadata file name header must be 'genome_name'
	for file in annotation_files_list:
		df = pd.read_csv(str(file), sep='\t')
		df['genome_name']=str(file).replace('_annotation.txt','')
		df2 = df
		df2.to_csv('temp_renamed_' + str(file), sep='\t', index=False)
	#concatenate
	all_filenames = glob.glob('temp_renamed*annotation.txt')
	df_merged = pd.concat([pd.read_csv(f,sep='\t') for f in all_filenames])
	df_merged.to_csv('merged_annotations.txt',  sep='\t', index=False)
	#delete temp files
	for f in all_filenames:
		os.remove(str(f))
	#Execute gene analysis function
	gene_analysis('merged_annotations.txt', 'genome_name', args.feature_type)

import pandas as pd
import numpy as np
import glob
import os

df_metadata = pd.read_csv('list_metadata.txt', sep='\t')
lists = df_metadata['list_name'].dropna().tolist()
genome_list = df_metadata['genomes'].dropna().tolist()

#core
df = pd.read_csv('gene_family_groupby_out.txt', sep='\t')
for genome in genome_list:
	df=df[df[str(genome)]>0]
df['gene_category']='core'
df2 = df.iloc[:,[0,-1]].to_csv(str(genome) +'_core_filter_out.txt', sep='\t',index=False)

#unique
for genome in genome_list:
	genome_list.remove(str(genome))
	df = pd.read_csv('gene_family_groupby_out.txt', sep='\t')
	df=df[df[str(genome)]>0]
	for genome_ex in genome_list:
		df= df[df[str(genome_ex)]<=0]
	df['gene_category']='unique_'+str(genome)
	df2 = df.iloc[:,[0,-1]].to_csv(str(genome) + '_unique_filter_out.txt', sep='\t',index=False)

#subgroups
for list in lists:
	genome_list_include = df_metadata['include_' + str(list)].dropna().tolist()
	genome_list_exclude = df_metadata['exclude_' + str(list)].dropna().tolist()
	df = pd.read_csv('gene_family_groupby_out.txt', sep='\t')
	for genome in genome_list_include:
		df=df[df[str(genome)]>0]
	for genome in genome_list_exclude:
		df= df[df[str(genome)]<=0]
	df['gene_category']=str(list)
	df2 = df.iloc[:,[0,-1]].to_csv(str(list) + '_filter_out.txt', sep='\t',index=False)

#concat
all_filenames = glob.glob('*_filter_out.txt')
df_merged = pd.concat([pd.read_csv(f,sep='\t') for f in all_filenames])
df_merged.to_csv('concat_filter.txt',  sep='\t', index=False)
	#delete temp files
for f in all_filenames:
	os.remove(str(f))

#merge
genome_list = df_metadata['genomes'].dropna().tolist()
for genome in genome_list:
	df_con = pd.read_csv('concat_filter.txt',  sep='\t')
	df_an = pd.read_csv(str(genome)+'_median_gene_analysis.txt', sep='\t')
	df_merged = pd.merge(df_an, df_con, left_on='pgfam_id', right_on='pgfam', how="left").to_csv(str(genome)+'_annotations_filter.txt',  sep='\t', index=False)


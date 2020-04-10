import os
import glob
import pandas as pd
import numpy as np

#rename
for file in glob.glob('*annotation.txt'):
	df = pd.read_csv(str(file), sep='\t')
	df['genome_name']=str(file).replace('_annotation.txt','')
	df2 = df
	df2.to_csv('renamed_' + str(file), sep='\t', index=False)

#merge renamed
all_filenames = glob.glob('renamed*annotation.txt')
df_merged = pd.concat([pd.read_csv(f,sep='\t') for f in all_filenames])
df_merged.to_csv('merged_annotations.txt',  sep='\t', index=False)
for f in all_filenames:
	os.remove(str(f))

#groupby
df_merged['count']=1 #adds new column called count at end and put number 1 in each cell
df_groupby = df_merged.groupby(['genome_name', 'pgfam'], as_index=False).sum().pivot(columns= 'genome_name', index = 'pgfam', values = 'count').fillna(0).to_csv('pgfam_groupby.txt', sep='\t') 
df_groupby2 = pd.read_csv('pgfam_groupby.txt', sep='\t')

#median
for col in df_groupby2.columns[1:]:
	df_temp = pd.DataFrame()
	df_temp['pgfam']=df_groupby2['pgfam']
	df_temp['gene_count']=df_groupby2[col]
	df_temp['median']=df_groupby2.median(axis=1)
	df_temp['gene_count-median']=df_groupby2[col]-df_temp['median']
	conditions = [(df_temp['gene_count'] == df_temp['median']),(df_temp['gene_count'] > df_temp['median']), (df_temp['gene_count'] < df_temp['median'])]
	choices = ['equal to median', 'greater than median', 'less than median']
	df_temp['category'] = np.select(conditions, choices, default='unknown')
	df_an = pd.read_csv(str(col)+'_annotation.txt', sep='\t')
	df_merged2 = pd.merge(df_an,df_temp, left_on='pgfam', right_on='pgfam', how="left").to_csv(str(col) + 'annotation_median_out.txt', sep='\t', index=False)

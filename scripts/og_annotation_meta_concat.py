import os
import sys
import glob
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input_folder',dest='input_folder',help='Specify folder with annotation data.')
parser.add_argument('-o','--output_folder',dest='output_folder',help='Specify name for output folder.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')

args=parser.parse_args()

#make output folder 
output_folder=str(args.output_folder)
os.mkdir(output_folder)


def tidy_spliter(df, column, sep=',', keep=False):
	indexes = list()
	new_values = list()
	df = df.dropna(subset=[column])
	for i, presplit in enumerate(df[column].astype(str)):
		values = presplit.split(sep)
		if keep and len(values) > 1:
			indexes.append(i)
			new_values.append(presplit)
		for value in values:
			indexes.append(i)
			new_values.append(value)
	new_df = df.iloc[indexes, :].copy()
	new_df[column] = new_values
	return new_df

#concat OGs files
orthogroup_files=glob.glob('Orthogroup*.tsv')
df_orthogroup=pd.concat([pd.read_csv(orthogroup_file,sep='\t', index_col= 0, dtype={"feature_id": object}, low_memory=False) for orthogroup_file in orthogroup_files])
#split OGS files
for col in df_orthogroup: 
	df_orthogroup2 = tidy_spliter(df_orthogroup, col, sep=', ').to_csv(output_folder+'/'+col + '_temp.txt', sep = '\t', columns = [col])
	df_orthogroup3 = pd.read_csv(output_folder+'/'+col + '_temp.txt', sep = '\t').rename(columns={str(col):'feature_id'}).to_csv(output_folder+'/'+col + '_temp.txt', sep = '\t',index=False)
#concat temp OGS files
temp_filter_files=glob.glob(output_folder+'/'+'*_temp.txt')
df_concat=pd.concat([pd.read_csv(temp_file,sep='\t') for temp_file in temp_filter_files], ignore_index=True).to_csv(output_folder+'/'+'concat_OGs.txt', sep = '\t',index=False)
#delete temp files
for temp_file in temp_filter_files:
	os.remove(str(temp_file))

#read metadata
df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'], dtype=object).replace(' ','_', regex=True)
genome_name_list=df_genome_names['genome_name'].dropna().tolist()
#merge OGs with annotation metadata
for genome_name in genome_name_list:
	print 'Merging annotation metadata with orthogroup id for '+str(genome_name)+'...'
	annotation_meta = pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t')
	df_orthogroup = pd.read_csv(output_folder+'/'+'concat_OGs.txt', sep = '\t')
	df_merged = pd.merge(annotation_meta,df_orthogroup, left_on='feature_id', right_on='feature_id', how="left").to_csv(output_folder+'/'+str(genome_name)+'_OG_annotation.txt',sep='\t',index=False)
#make df with unique OG and annotations functions to merge with median later
#	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_OG_annotation.txt',sep='\t',usecols=['Orthogroups','function']) for genome_name in genome_name_list]).drop_duplicates(inplace=True)
#	df_concat.to_csv(output_folder+'/'+'unique_OG_function.txt',sep='\t',index=False)
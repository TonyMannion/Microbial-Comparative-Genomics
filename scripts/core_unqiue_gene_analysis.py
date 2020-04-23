import os
import glob
import argparse
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input_folder',dest='input_folder',help='Specify folder with annotation data.')
parser.add_argument('-o','--output_folder',dest='output_folder',help='Specify name for output folder.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
args=parser.parse_args()

#core unique genes filter function
def core_unique_genes():
	#make output folder
	output_folder='core_unqiue_gene_analysis_'+str(args.output_folder)
	os.mkdir(output_folder)
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0).to_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t') 
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()	
	#core
	df=pd.read_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
	for col in df.columns[1:]:
		df=df[df[str(col)]>0]
	df['core_unique_gene']='core'
	df2=df.iloc[:,[0,-1]].to_csv(output_folder+'/'+'temp_core_filter_out.txt',sep='\t',index=False)
	for genome in genome_name_list:
		exclude_genome_list=df_genome_names['genome_name'].dropna().tolist()
		exclude_genome_list.remove(str(genome))
		df=pd.read_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
		df=df[df[str(genome)]>0]
		for excluded_genome in exclude_genome_list:
			df=df[df[str(excluded_genome)]<=0]
		df['core_unique_gene']='unique_'+str(genome)
		df2=df.iloc[:,[0,-1]].to_csv(output_folder+'/'+'temp_'+str(genome)+'_unique_filter_out.txt',sep='\t',index=False)
	#concat
	temp_filter_files=glob.glob(output_folder+'/'+'temp_'+'*_filter_out.txt')
	df_concat=pd.concat([pd.read_csv(temp_file,sep='\t') for temp_file in temp_filter_files])
	#delete temp files
	for temp_file in temp_filter_files:
		os.remove(str(temp_file))
	#merge
	for genome in genome_name_list:
		df_an=pd.read_csv(str(args.input_folder)+'/'+str(genome)+'_annotation.txt',sep='\t')
		df_merged=pd.merge(df_an,df_concat,left_on='pgfam',right_on='pgfam',how="left").to_csv(output_folder+'/'+str(genome)+'_annotation.txt',sep='\t',index=False)
		print 'Core and unique genes done for '+str(genome)
	#remove intermediate files
	os.remove(output_folder+'/'+'gene_family_groupby_out.txt')

if __name__=="__main__":
	core_unique_genes()

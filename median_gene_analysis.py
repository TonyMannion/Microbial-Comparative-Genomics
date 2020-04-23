import os
import argparse
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input_folder',dest='input_folder',help='Specify folder with annotation data.')
parser.add_argument('-o','--output_folder',dest='output_folder',help='Specify name for output folder.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
args=parser.parse_args()

#gene analysis function
def median_analysis():
	#make output folder
	output_folder='median_gene_analysis_'+str(args.output_folder)
	os.mkdir(output_folder)
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0).to_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
	df_groupby2=pd.read_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
	#median cacluations
	for col in df_groupby2.columns[1:]:
		df_temp=pd.DataFrame()
		df_temp['pgfam']=df_groupby2['pgfam']
		df_temp['genome_name']=str(col)
		df_temp['genome_name_pgfam']=df_temp['genome_name']+'_'+df_temp['pgfam']
		df_temp['gene_count']=df_groupby2[col]
		df_temp['median']=df_groupby2.median(axis=1)
		df_temp['gene_count-median']=df_groupby2[col]-df_temp['median']
		conditions=[(df_temp['gene_count']==df_temp['median']),(df_temp['gene_count'] > df_temp['median']),(df_temp['gene_count'] < df_temp['median'])]
		choices=['equal to median','greater than median','less than median']
		df_temp['vs_median']=np.select(conditions,choices,default='unknown')
		#merge median calculations with annotation metadata
		df_concat['genome_name_pgfam']=df_concat['genome_name']+'_'+df_concat['pgfam']
		#annotation metadata
		df_merged=pd.merge(df_temp,df_concat,left_on='genome_name_pgfam',right_on='genome_name_pgfam',how="left").rename(columns={'genome_name_y': 'genome_name','pgfam_x':'pgfam'}).drop(['pgfam_y','genome_name_x','genome_name_pgfam','count'],axis=1)
		cols=list(df_merged.columns)
		cols=cols[5:]+cols[0:5]#rearranges cols
		df_merged2=df_merged[cols].to_csv(output_folder+'/'+str(col)+'_annotation.txt',sep='\t',index=False)
		print "Median gene analysis done for "+str(col)+'...'
	#remove intermediate files
	os.remove(output_folder+'/'+'gene_family_groupby_out.txt')

if __name__=="__main__":
	median_analysis()

import os
import argparse
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input_folder',dest='input_folder',help='Specify folder with annotation data.')
parser.add_argument('-o','--output_folder',dest='output_folder',help='Specify name for output folder.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
args=parser.parse_args()

def make_tree():
	#make output folder
	output_folder='pangenome_tree_'+str(args.output_folder)
	os.mkdir(output_folder) 
	print 'Creating binary matrix of protein families in PHYLIP format for pan-genome phylogentic tree...'
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.replace(' ','_',regex=True).groupby(['genome_name','pgfam'],as_index=False).sum().pivot(index='genome_name',columns='pgfam',values='count').fillna(0).astype(int)
	for col in df_groupby:
		#If value is greater than 0,replace with 1,otherwise replace with 0.
		#Necessary because genome may have more than one count for protein family.
		df_groupby[col]=np.where(df_groupby[col] > 0,1,0) 
	total_rows=len(df_groupby.axes[0])
	total_cols=len(df_groupby.axes[1])
	df_groupby.to_csv(output_folder+'/'+'pan-genome-tree_out.txt',sep='\t') 
	with open(output_folder+'/'+'pan-genome-tree_out.txt',"rb") as f:
		lines=f.readlines()
	lines[0]=str(total_rows)+" "+str(total_cols)+"\n"
	with open(output_folder+'/'+'pan-genome-tree_out.txt',"w") as f:
		f.writelines(lines)

if __name__=="__main__":
	make_tree()

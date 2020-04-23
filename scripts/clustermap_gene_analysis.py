import os
import sys
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

#gene analysis function
def make_clustermap():
	#make output folder
	output_folder='clustermap_'+str(args.output_folder)
	os.mkdir(output_folder)
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0)
	df_cm=df_groupby.transpose()
	#clustermap
	print "Generating clustermap..."
	sys.setrecursionlimit(10**6) 
	df_cm=df_cm.rename_axis('',axis='rows')
	#11 hex codes for colors: off-white,red,orange,yellow,green,blue,purple,pink,gray,brown,black
	custom_cmap=['#fdf8ef','#ff7f7f','#ffa500','#ffff66','#008000','#0000ff','#814ca7','#ee82ee','#808080','#a5682a','#000000']
	sns.set_palette(custom_cmap)
	cm=sns.clustermap(df_cm,cmap=custom_cmap,vmin=0,vmax=10,xticklabels=False,figsize=(25,10),cbar_kws={"ticks":[0,1,2,3,4,5,6,7,8,9,10],"label":('0 to 10+genes per gene family')})
	cm.ax_col_dendrogram.set_visible(False)
	plt.savefig(output_folder+'/'+'clustermap.png',dpi=300)
	plt.clf()
	#save clustermap dataframe
	print "Output clustermap dataframe..."
	df_cm2=pd.DataFrame(cm.data2d).transpose()
	df_cm2.to_csv(output_folder+'/'+'gene_family_clustermap_out.txt',sep='\t')

if __name__=="__main__":
	make_clustermap()

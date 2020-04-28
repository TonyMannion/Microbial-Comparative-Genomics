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
parser.add_argument('-make_tree','--make_tree',dest='exe_make_tree',default='yes',help='Generate binary matrix of protein families in PHYLIP format for pan-genome phylogenetic tree? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-make_clustermap','--make_clustermap',dest='exe_make_clustermap',default='yes',help='Create hierarchically-clustered heatmap (ie clustermap) of protein families in pan-genome? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-core_unique_genes','--core_unique_genes',dest='exe_core_unique_genes',default='yes',help='Determine core and unique protein family genes for genome group? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-median_analysis','--median_analysis',dest='exe_median_analysis',default='yes',help='Calculate median protein family gene copy number in genome group and if protein family genes for individual genomes are equal to, greater than, or less than median? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-subgroup_genes','--subgroup_genes',dest='exe_subgroup_genes',default='yes',help='Determine unique protein family genes for genome subgroup within the larger genome group? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-VF_blast','--VF_blast',dest='exe_VF_blast',default='yes',help='Perform DIAMOND blast analysis for virulence factor genes? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-res_blast','--res_blast',dest='exe_res_blast',default='yes',help='Perform DIAMOND blast analysis for antibiotic resistence genes? Enter "yes" or "no". Default is "yes".')
parser.add_argument('-custom_blast','--custom_blast',dest='exe_custom_blast',default='no',help='Perform DIAMOND blast analysis for custom gene database? Enter "yes" or "no". Default is "no".')
parser.add_argument('-custom_fasta','--custom_fasta',dest='custom_fasta',help='Provide custom gene database as multi-sequence fasta file using amino acids.')
parser.add_argument('-merge_all_annotations','--merge_all_annotations',dest='exe_merge_all_annotations',default='yes',help='Merge all annotation metadata files in output folder? Enter "yes" or "no". Default is "yes".')
args=parser.parse_args()

#make output folder 
output_folder=str(args.output_folder)
os.mkdir(output_folder)

def make_tree():
	print 'Creating binary matrix of protein families in PHYLIP format for pan-genome phylogenetic tree...'
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
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

def make_clustermap():
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0)
	df_cm=df_groupby.transpose()
	#clustermap
	print "Creating hierarchically-clustered heatmap (ie clustermap) of protein families in pan-genome..."
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
	df_cm2.to_csv(output_folder+'/'+'PGfam_clustermap_dataframe.txt',sep='\t')

def core_unique_genes():
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0).to_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t') 
	#core
	df=pd.read_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
	for col in df.columns[1:]:
		df=df[df[str(col)]>0]
	df['core_unique_gene']='core'
	df2=df.iloc[:,[0,-1]].to_csv(output_folder+'/'+'temp_core_filter_out.txt',sep='\t',index=False)
	#unique
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
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
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	for genome in genome_name_list:
		df_an=pd.read_csv(str(args.input_folder)+'/'+str(genome)+'_annotation.txt',sep='\t')
		df_merged=pd.merge(df_an,df_concat,left_on='pgfam',right_on='pgfam',how="left").to_csv(output_folder+'/'+str(genome)+'_annotation_core_unique_genes.txt',sep='\t',index=False)
		print 'Core and unique genes determined for '+str(genome)
	#remove intermediate files
	os.remove(output_folder+'/'+'gene_family_groupby_out.txt')

def median_analysis():
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
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
		col_order=['genome_name','contig_id','feature_id','type','location','start','stop','strand','function','aliases','plfam','pgfam','figfam','evidence_codes','nucleotide_sequence','aa_sequence','gene_count','median','gene_count-median','vs_median']
		df_merged2=df_merged[col_order].to_csv(output_folder+'/'+str(col)+'_annotation_median_analysis.txt',sep='\t',index=False)
		print "Median gene analysis done for "+str(col)+'...'
	#remove intermediate files
	os.remove(output_folder+'/'+'gene_family_groupby_out.txt')

def subgroup_genes():
	#concat
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	df_concat=pd.concat([pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t') for genome_name in genome_name_list])
	#groupby
	df_concat['count']=1
	df_groupby=df_concat.groupby(['genome_name','pgfam'],as_index=False).sum().pivot(columns='genome_name',index='pgfam',values='count').fillna(0).to_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t') 
	#make lists from metadata
	df_metadata=pd.read_csv(str(args.metadata_file),sep='\t').replace(' ','_', regex=True)
	subgroup_list=df_metadata['subgroup'].dropna().tolist()
	genome_name_list=df_metadata['genome_name'].dropna().tolist()
	#subgroups
	for subgroup in subgroup_list:
		genome_list_include=df_metadata['include_'+str(subgroup)].dropna().tolist()
		genome_list_exclude=df_metadata['exclude_'+str(subgroup)].dropna().tolist()
		df=pd.read_csv(output_folder+'/'+'gene_family_groupby_out.txt',sep='\t')
		for genome in genome_list_include:
			df=df[df[str(genome)]>0]
		for genome in genome_list_exclude:
			df=df[df[str(genome)]<=0]
		df['subgroup_gene']=str(subgroup)
		df2=df.iloc[:,[0,-1]].to_csv(output_folder+'/'+'temp_'+str(subgroup)+'_filter_out.txt',sep='\t',index=False)
	#concat
	temp_filter_files=glob.glob(output_folder+'/'+'temp_'+'*_filter_out.txt')
	df_concat=pd.concat([pd.read_csv(temp_file,sep='\t') for temp_file in temp_filter_files])
	#delete temp files
	for temp_file in temp_filter_files:
		os.remove(str(temp_file))
	#merge
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	for genome in genome_name_list:
		df_an=pd.read_csv(str(args.input_folder)+'/'+str(genome)+'_annotation.txt',sep='\t')
		df_merged=pd.merge(df_an,df_concat,left_on='pgfam',right_on='pgfam',how="left").to_csv(output_folder+'/'+str(genome)+'_annotation_subgroup_genes.txt',sep='\t',index=False)
		print 'Subgroup gene analysis done for '+str(genome)
	#remove intermediate files
	os.remove(output_folder+'/'+'gene_family_groupby_out.txt')

def blaster(type,database_file): #type=VF,RES,or custom
	#read metadata
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	#blast
	for genome_name in genome_name_list:
		print 'DIAMOND blast for '+str(type)+' database for '+str(genome_name)+'...'
		os.system('diamond blastp --db '+str(database_file)+' --query'+' '+str(args.input_folder)+'/'+str(genome_name)+'_protein.fasta'+' '+'--out'+' '+output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt'+' '+'--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df1=pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t',dtype=str)
		df2=pd.read_csv(output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt',sep='\t',names=['qseqid'+'_'+str(type),'qlen'+'_'+str(type),str(type)+'_'+'ID','slen'+'_'+str(type),'qseq'+'_'+str(type),'sseq'+'_'+str(type),'evalue'+'_'+str(type),'bitscore'+'_'+str(type),'pident'+'_'+str(type),'qcovhsp'+'_'+str(type)],dtype=str)
		df_merge=pd.merge(df1,df2,left_on='feature_id',right_on='qseqid'+'_'+str(type),how="left").to_csv(output_folder+'/'+str(genome_name)+'_annotation_'+str(type)+'.txt',sep='\t',index=False)
		os.remove(output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt')

def merge_all_annotations():
	
	#read metadata
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name']).replace(' ','_', regex=True)
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	for genome_name in genome_name_list:
		print 'Merging all annotation metadata for '+str(genome_name)+'...'
		annotation_files = glob.glob(output_folder+'/'+str(genome_name)+'*'+'_annotation_'+'*'+'.txt')
		annotation_dfs = [pd.read_csv(file,sep='\t') for file in annotation_files]
		df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['feature_id'], how='outer', suffixes=('', '_drop')), annotation_dfs)
		df_merged.drop(list(df_merged.filter(regex='_drop$')), axis=1, inplace=True)
		df_merged.to_csv(output_folder+'/'+str(genome_name)+'_annotation_all_merged.txt',sep='\t',index=False)

if str(args.exe_make_tree)=='yes':
	make_tree()
if str(args.exe_make_clustermap)=='yes':
	make_clustermap()
if str(args.exe_core_unique_genes)=='yes':
	core_unique_genes()
if str(args.exe_median_analysis)=='yes':
	median_analysis()
if str(args.exe_subgroup_genes)=='yes':
	subgroup_genes()
if str(args.exe_VF_blast)=='yes':
	blaster('VF','VFDB_setB_pro.dmnd')
if str(args.exe_res_blast)=='yes':
	blaster('RES','card_protein.dmnd')
if str(args.exe_custom_blast)=='yes':
	os.system('diamond makedb --in '+str(args.custom_fasta)+' -d custom_database')
	blaster('custom','custom_database.dmnd')
	os.remove('custom_database.dmnd')
if str(args.exe_merge_all_annotations)=='yes':
	merge_all_annotations()

	print '\nDONE!!'

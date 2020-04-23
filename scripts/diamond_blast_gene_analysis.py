import os
import argparse
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input_folder',dest='input_folder',help='Specify folder with annotation data.')
parser.add_argument('-o','--output_folder',dest='output_folder',help='Specify name for output folder.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
parser.add_argument('-VF_blast','--VF_blast',dest='exe_VF_blast',default='yes',help='Execute function?')
parser.add_argument('-res_blast','--res_blast',dest='exe_res_blast',default='yes',help='Execute function?')
parser.add_argument('-custom_blast','--custom_blast',dest='exe_custom_blast',default='no',help='Execute function?')
parser.add_argument('-custom_fasta','--custom_fasta',dest='custom_fasta',help='Provide protein fasta file')
args=parser.parse_args()

def blaster(type,database_file): #type=VF,RES,or custom
	#make output folder
	output_folder='blast_'+str(type)+'_'+str(args.output_folder)
	os.mkdir(output_folder)
	#read metadata
	df_genome_names=pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_name'])
	genome_name_list=df_genome_names['genome_name'].dropna().tolist()
	#blast
	for genome_name in genome_name_list:
		print 'DIAMOND blast for '+str(type)+' database for '+str(genome_name)+'...'
		os.system('diamond blastp --db '+str(database_file)+' --query'+' '+str(args.input_folder)+'/'+str(genome_name)+'_protein.fasta'+' '+'--out'+' '+output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt'+' '+'--outfmt 6 qseqid qlen sseqid slen qseq sseq evalue bitscore pident qcovhsp -k 1')
		df1=pd.read_csv(str(args.input_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t',dtype=str)
		df2=pd.read_csv(output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt',sep='\t',names=['qseqid'+'_'+str(type),'qlen'+'_'+str(type),str(type)+'_'+'ID','slen'+'_'+str(type),'qseq'+'_'+str(type),'sseq'+'_'+str(type),'evalue'+'_'+str(type),'bitscore'+'_'+str(type),'pident'+'_'+str(type),'qcovhsp'+'_'+str(type)],dtype=str)
		df_merge=pd.merge(df1,df2,left_on='feature_id',right_on='qseqid'+'_'+str(type),how="left").to_csv(output_folder+'/'+str(genome_name)+'_annotation.txt',sep='\t',index=False)
		os.remove(output_folder+'/'+str(genome_name)+'_'+str(type)+'_blast_out.txt')

if __name__=="__main__":
	blaster()

if str(args.exe_VF_blast)=='yes':
	blaster('VF','VFDB_setB_pro.dmnd')
if str(args.exe_res_blast)=='yes':
	blaster('RES','card_protein.dmnd')
if str(args.exe_custom_blast)=='yes':
	os.system('diamond makedb --in '+str(args.custom_fasta)+' -d custom_database')
	blaster('custom','custom_database.dmnd')
	os.remove('custom_database.dmnd')

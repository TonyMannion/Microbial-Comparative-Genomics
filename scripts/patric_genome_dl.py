import os
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', dest='username', help='Provide username for PATRIC account. Prompt to enter password will appear.')
parser.add_argument('-m','--metadata_file',dest='metadata_file',help='Specify metadata file.')
parser.add_argument('-o', '--output_folder', dest='output_folder', help='Specify output folder for downloaded data.')
args=parser.parse_args()

#login
print 'Enter password to log into PATRIC...'
os.system('p3-login ' + str(args.username) + ' > patric_domain_temp_genome_assemlby_annotation.txt')
patric_domain = open('patric_domain_temp_genome_assemlby_annotation.txt', "rb").readlines()[1].replace('Logged in with username ', '').rstrip()
#download from patric
df_genome_names = pd.read_csv(str(args.metadata_file),sep='\t',usecols=['genome_ids','genome_name']).replace(' ','_', regex=True)
genome_ids_list = df_genome_names['genome_ids'].dropna().tolist()
genome_name_list = df_genome_names['genome_name'].dropna().tolist()
zip(genome_ids_list,genome_name_list)
for genome_id,genome_name in zip(genome_ids_list,genome_name_list): 
  print 'Downloading data for '+str(genome_id)+' '+str(genome_name)+' from PATRIC...'
  if not os.path.exists(str(args.output_folder)):
    os.mkdir(str(args.output_folder))
  os.system('p3-echo -t genome_id '+str(genome_id)+' | p3-get-genome-features --in feature_type,CDS,rna --attr genome_name --attr sequence_id --attr patric_id --attr start --attr end --attr strand --attr product --attr pgfam_id --attr na_sequence --attr aa_sequence > '+str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt')
  df_genome = pd.read_csv(str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t')
  df_genome2=df_genome.rename(columns={'feature.genome_name': 'genome_name','feature.pgfam_id': 'pgfam','feature.patric_id':'feature_id'})
  df_genome2['genome_name'].replace(' ','_', regex=True, inplace=True)
  df_genome2.to_csv(str(args.output_folder)+'/'+str(genome_name)+'_annotation.txt',sep='\t',index=False)
  os.system('p3-genome-fasta --contig '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_contigs.fasta')
  os.system('p3-genome-fasta --protein '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_protein.fasta')
  os.system('p3-genome-fasta --feature '+str(genome_id)+' > '+str(args.output_folder)+'/'+str(genome_name)+'_DNA.fasta')

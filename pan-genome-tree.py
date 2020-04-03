import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-username', '--username', dest='username', help='Enter PATRIC login username')

parser.add_argument('-p', '--patric_features_dl', dest='patric_features_dl', default = 'yes', help='Download features from PATRIC? Enter "yes" or "no". Default is "yes". If features have already been downloaded, enter "no" to bypass this step.')
parser.add_argument('-g', '--genome_id_file', dest='genome_ids', default = 'genome_ids.txt', help='Specify file containing PATRIC genome ids of interest. Header is "Genomes" and each genome id is on different row. Default is genome_ids.txt')
parser.add_argument('-i', '--features_file', dest='features_file', help='Input desired name for features file for genomes of interest downloaded from PATRIC.  Use a tab-delimited file')
parser.add_argument('-a', '--index_column', dest='index_column', default = 'feature.genome_name', help='Specificy index column for genomes from feature file.  For example, use "genome_name" or "patric_id".  Default is "feature.genome_name".')
parser.add_argument('-b', '--count_column', dest='count_column', default = 'feature.pgfam_id', help='Specificy count column for gene family from feature file.  Choose "plfam_id" for local protein family (genus-specific, called PLfam) or "pgfam_id" for global protein family (cross-genus, called PGfam).  Default is "feature.pgfam_id" for global protein family (cross-genus, called PGfam).')
parser.add_argument('-o', '--output', dest='output', default = 'pan-genome-tree_out.txt', help='Specificy name for output file.  Default is pan-genome-tree_out.txt')

args = parser.parse_args()

if str(args.patric_features_dl) == 'yes':
	print 'Logging into PATRIC...'
	os.system('p3-login ' + str(args.username))
	os.system('p3-get-genome-features --input ' + str(args.genome_ids) + ' --attr genome_name --attr patric_id --attr gene_id --attr plfam_id --attr pgfam_id --attr product > ' + str(args.index_column))

def groupby(index_column, count_column, output_file):  
	df1['count']=1
	df2 = df1.replace(' ', '_', regex=True).groupby([index_column, count_column], as_index=False).sum()  
	df3 = df2.pivot(index = index_column, columns = count_column, values = 'count').fillna(0)
	df4=df3.astype(int)
	for col in df4:
		df4[col] = np.where(df4[col] > 0, 1, 0) # If value is greater than 0, replace with 1, otherwise replace with 0.  Necessary because genome may have more than one count for protein family.
	total_rows=len(df4.axes[0])
	total_cols=len(df4.axes[1])
	df4.to_csv(output_file, sep='\t') 
	with open(output_file, "rb") as f:
		lines = f.readlines()
	lines[0] = str(total_rows) + " " + str(total_cols) + "\n"
	with open(output_file, "w") as f:
		f.writelines(lines)

df1 = pd.read_csv(str(args.features_file), sep='\t', usecols=[str(args.index_column),str(args.count_column)])
groupby(str(args.index_column), str(args.count_column), str(args.output))

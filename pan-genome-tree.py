import pandas as pd
import numpy as np
from sys import argv

script, argv1, argv2, argv3 = argv
#will change to flags

def groupby(index_column, count_column):  
	df1['count']=1 #adds new column called count at end and put number 1 in each cell
	df2 = df1.replace(' ', '_', regex=True).groupby([index_column, count_column], as_index=False).sum()  
	df3 = df2.pivot(index = index_column, columns = count_column, values = 'count').fillna(0)
	df4=df3.astype(int)
	for col in df4:
		df4[col] = np.where(df4[col] > 0, 1, 0)
	total_rows=len(df4.axes[0])
	total_cols=len(df4.axes[1])
	print total_rows
	print total_cols
	df4.to_csv("out_groupby.txt", sep='\t') 
	with open("out_groupby.txt", "rb") as f:
		lines = f.readlines()
	lines[0] = str(total_rows) + " " + str(total_cols) + "\n"
	with open("out_groupby.txt", "w") as f:
		f.writelines(lines)

df1 = pd.read_csv(str(argv1) +'.txt', sep='\t')
groupby(str(argv2), str(argv3))

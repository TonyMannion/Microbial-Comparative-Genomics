
	df_concat2 = df_concat.rename(columns={str(feature_type): 'pgfam'})
	df_groupby = df_concat2.groupby([str(genome_name), 'pgfam'], as_index=False).sum().pivot(columns = str(genome_name), index = 'pgfam', values = 'count').fillna(0)
	print 'Output gene family groupby dataframe...'
	df_cm = df_groupby.transpose()
	print "Generating clustermap..."
	sys.setrecursionlimit(10**6) 
	df_cm = df_cm.rename_axis('', axis='rows')
	#11 hex codes for colors: off-white, red, orange, yellow, green, blue, purple, pink, gray, brown, black
	custom_cmap = ['#fdf8ef', '#ff7f7f', '#ffa500', '#ffff66', '#008000', '#0000ff', '#814ca7', '#ee82ee', '#808080', '#a5682a', '#000000']
	sns.set_palette(custom_cmap)
	cm = sns.clustermap(df_cm, cmap=custom_cmap, vmin=0, vmax=10, xticklabels=False, figsize=(25,10), cbar_kws={"ticks":[0,1,2,3,4,5,6,7,8,9,10], "label":('0 to 10+ genes per gene family')})
	cm.ax_col_dendrogram.set_visible(False)
	plt.savefig('clustermap.png', dpi=300)
	plt.clf()
	#save clustermap dataframe
	print "Output clustermap dataframe..."
	df_cm2 = pd.DataFrame(cm.data2d).transpose()
	df_cm2.to_csv('gene_family_clustermap_out.txt', sep='\t')

#download features from PATRIC
if str(args.downlaod_patric_features) == 'yes':
	print 'Logging into PATRIC...'
	os.system('p3-login ' + str(args.username))
	print 'Downloading features from PATRIC...'
	os.system('p3-get-genome-features --input ' + str(args.metadata_file) + ' --attr genome_name --attr patric_id --attr gene_id --attr pgfam_id --attr product > ' + str(args.features_file))

#cluster map from PATRIC features
if str(args.PATRIC_features) == 'yes':
	#Execute gene analysis function
	print "Performing gene analysis..."
	make_clustermap(args.features_file, 'feature.genome_name', 'feature.pgfam_id')

#cluster map from annotation metadata
if str(args.annotations) == 'yes':
	print "Performing gene analysis..." 
	#concatenate
	df_genome_names = pd.read_csv(str(args.metadata_file), sep='\t', usecols=['genome_name'])
	genome_name_list = df_genome_names['genome_name'].dropna().tolist()
	df_concat = pd.concat([pd.read_csv(str(genome_name)+ '_annotation.txt',sep='\t') for genome_name in genome_name_list])
	df_concat.to_csv('concatenated_annotations.txt',  sep='\t', index=False)
	#Execute gene analysis function
	make_clustermap('concatenated_annotations.txt', 'genome_name', 'pgfam')

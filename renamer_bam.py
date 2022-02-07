#! /bin/python3.9.5

import sys
import os
import pandas as pd

## Script developed for renaming CPTAC SJ files and log files within

if len(sys.argv) < 3 :
	print('Usage: RenamerByMap.py /path/to/Sample/Folders/ SampleSheet.tsv CohortSheet.xlsx')
	sys.exit()
else :
	filepath=sys.argv[1]
	namemap=open(sys.argv[2], 'r')
	cohort=open(sys.argv[3], 'r')

## make pandas df with infiles
namemap=pd.read_csv(namemap, sep='\t', index_col=0)
cohort=pd.read_csv(cohort, index_col=0, header=0)

for folder in os.listdir(os.path.join(filepath)) :
	for file in os.listdir(os.path.join(filepath, folder)) :
		if os.path.isdir(os.path.join(filepath, folder, file)) == True :
			for file2 in os.listdir(os.path.join(filepath, folder, file)) :
				ext=file2.split('.')[1:]
				ext='.'.join(ext)
				#ext='rna_seq.star_SJ.tsv.gz'
				newID=namemap.at[folder,'Case ID']
				if ',' in newID :
					newID=newID.split(',')[0]
				#if namemap.at[folder,'File Name'].split('.')[2] == 'chimeric' :
				#	cog='Chim'
				#elif namemap.at[folder,'File Name'].split('.')[2] == 'genomic' :
				#	cog='Gen'
				if namemap.at[folder,'Sample Type'] ==  'Primary Tumor' or namemap.at[folder,'Sample Type'] ==  'Primary Tumor, Primary Tumor':
					lines=cohort.loc[cohort.index==newID,]
					tline=lines.loc[lines['Type']=='Tumor','Experiment (TMT10plex)']
					tmt=tline.iloc[0]
					stype='T'
				elif namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal' or namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal, Solid Tissue Normal':
					lines=cohort.loc[cohort.index==newID,]
					tline=lines.loc[lines['Type']=='Normal','Experiment (TMT10plex)']
					tmt=tline.iloc[0]
					stype='N'
				src=os.path.join(filepath, folder, file, file2)
				dst=os.path.join(filepath, folder, file, newID+'_'+str(tmt)+stype+'.'+str(ext))
				if os.path.exists(dst) == True :
					j=2
					dst=os.path.join(filepath, folder, file, newID+'_'+str(tmt)+stype	+str(j)+'.'+str(ext))
					j=j+1
				os.rename(src,dst)
		else:
			if 'annotation' in file : #dont change annotation file name
				continue
			else :
				ext=file.split('.')[1:]
				ext='.'.join(ext)
				#ext='rna_seq.star_SJ.tsv.gz'
				newID=namemap.at[folder,'Case ID']
				if ',' in newID :
					newID=newID.split(',')[0]
				#if namemap.at[folder,'File Name'].split('.')[2] == 'chimeric' :
				#	cog='Chim'
				#elif namemap.at[folder,'File Name'].split('.')[2] == 'genomic' :
				#	cog='Gen'
				if namemap.at[folder,'Sample Type'] ==  'Primary Tumor' or namemap.at[folder,'Sample Type'] ==  'Primary Tumor, Primary Tumor':
					lines=cohort.loc[cohort.index==newID,]
					tline=lines.loc[lines['Type']=='Tumor','Experiment (TMT10plex)']
					tmt=tline.iloc[0]
					stype='T'
				elif namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal' or namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal, Solid Tissue Normal':
					lines=cohort.loc[cohort.index==newID,]
					tline=lines.loc[lines['Type']=='Normal','Experiment (TMT10plex)']
					tmt=tline.iloc[0]
					stype='N'
				src=os.path.join(filepath, folder, file)
				dst=os.path.join(filepath, folder, newID+'_'+str(tmt)+stype+'.'+str(ext))
				if os.path.exists(dst) == True : #check if duplicate, add int if so
					j=2
					dst=os.path.join(filepath, folder, file, newID+'_'+str(tmt)+stype+str(j)+'.'+str(ext))
					j=j+1
				os.rename(src,dst)
	newID=namemap.at[folder,'Case ID']
	if ',' in newID :
		newID=newID.split(',')[0]
	if namemap.at[folder,'File Name'].split('.')[2] == 'chimeric' :
		cog='Chim'
	elif namemap.at[folder,'File Name'].split('.')[2] == 'genomic' :
		cog='Gen'
	if namemap.at[folder,'Sample Type'] ==  'Primary Tumor' or namemap.at[folder,'Sample Type'] ==  'Primary Tumor, Primary Tumor':
		lines=cohort.loc[cohort.index==newID,]
		tline=lines.loc[lines['Type']=='Tumor','Experiment (TMT10plex)']
		tmt=tline.iloc[0]
		stype='T'
	elif namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal' or namemap.at[folder,'Sample Type'] ==  'Solid Tissue Normal, Solid Tissue Normal':
		lines=cohort.loc[cohort.index==newID,]
		tline=lines.loc[lines['Type']=='Normal','Experiment (TMT10plex)']
		tmt=tline.iloc[0]
		stype='N'
	src=os.path.join(filepath, folder)
	dst=os.path.join(filepath, newID+'_'+str(tmt)+stype+'_'+cog)
	if os.path.exists(dst) == True : #check if duplicate, add int if so
		j=2
		dst=os.path.join(filepath, newID+'_'+str(tmt)+stype+'_'+cog+str(j))
		j=j+1
	os.rename(src, dst)
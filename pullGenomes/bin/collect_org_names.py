#!/usr/bin/env python
import os
import sys
import re

# Given a directory, loop over the sub-directories, collecting their org_names
# Also loop through those subdirectories, find the genomic file, and extract the
# organism name from the header line

# Most importantly get the absolute path to the file
# using os.path.realpath(content2)

# If this doesn't work aka len(ncbi) =/= len(org_list)
# Most likely reason is the org_exp regex.

# Issue where nextflow doesn't like entries having the same name, so I need
# to use os.mv or something to rename the entries with scaff or unplaced
# whatever to the directory name.

rootDataDir = sys.argv[1]

ncbi_accession = []
organism_list = []
genome_file_list = []
absolute_file_path = []

ncbi2org = {}

fastaExt = ['.fa', '.fna', '.faa', '.fasta']

for filename in os.listdir(rootDataDir): # Loop over passed directory
    content = os.path.join(rootDataDir, filename)

    if os.path.isdir(content): # If it is a directory
        ncbi_accession.append(filename)

        for filename2 in os.listdir(content): # Loop over the files inside
            content2 = os.path.join(content, filename2)

            if (filename in filename2) and (os.path.splitext(filename2)[1] in fastaExt): # if they are the proper genome file
                with open(content2) as file:
                    handle = file.readlines()

                    for line in handle: # loop over genome file lines
                        if line[0] == '>': # if it is the header line
                            org_exp = '\s.+[,|\n]' # Start with a space, end on a , or a newline
                            organism_name = re.search( org_exp, line )
                            #print(filename, organism_name)
                            ncbi2org[filename] = organism_name.group()[1:-1]
                            genome_file_list.append( filename2 )
                            absolute_file_path.append( os.path.realpath(content2) )
                            try:
                                organism_list.append( organism_name.group()[1:-1] )
                            except AttributeError:
                                organism_list.append( 'No_Name' )
                            break
                break
            elif (('unplaced' in filename2) or ('chr' in filename2)) and  (os.path.splitext(filename2)[1] in fastaExt): # if they are weirdly named
                fullPath = os.path.dirname(os.path.realpath(content2))
                newFileName = filename+"_strange"+os.path.splitext(filename2)[1]

                newFileDest = os.path.join(fullPath, newFileName)
                oldFileDest = os.path.realpath(content2)

                os.rename( oldFileDest, newFileDest )
                content2 = newFileDest
                
                with open(content2) as file:
                    handle = file.readlines()

                    for line in handle: # loop over genome file lines
                        if line[0] == '>': # if it is the header line
                            org_exp = '\s.+[,|\n]' # Start with a space, end on a , or a newline
                            organism_name = re.search( org_exp, line )
                            #print(filename, organism_name)
                            ncbi2org[filename] = organism_name.group()[1:-1]
                            genome_file_list.append( filename2 )
                            absolute_file_path.append( os.path.realpath(content2) )
                            try:
                                organism_list.append( organism_name.group()[1:-1] )
                            except AttributeError:
                                organism_list.append( 'No_Name' )
                            break
                break

            #else:
                #print(filename, filename2, os.path.splitext(filename2)[1], ( (filename in filename2) or ('unplaced' in filename2) ))

#print( f'{len(ncbi_accession)} directories\n{len(organism_list)} Human names\n{len(ncbi2org)} Both' )

# Write accession, organism name, file of interest, path to file of interest
with open('relations.tsv', 'w') as file:
    for i in range(len(ncbi_accession)-1):
        file.write(f'{ncbi_accession[i]}\t{organism_list[i]}\t{genome_file_list[i]}\t{absolute_file_path[i]}\n')

    finalIndex = len(ncbi_accession) - 1
    file.write(f'{ncbi_accession[finalIndex]}\t{organism_list[finalIndex]}\t{genome_file_list[finalIndex]}\t{absolute_file_path[finalIndex]}\n')
    """
    for key, value in ncbi2org.items():
        file.write(f'{key}\t{value}\n')
    """

#!/usr/bin/env python
import os
import sys
import re

# Given a directory, loop over the sub-directories, collecting their org_names
# Also loop through those subdirectories, find the genomic file, and extract the
# name from the header line
rootDataDir = sys.argv[1]

ncbi_accession = []
organism_list = []
ncbi2org = {}

fastaExt = ['.fa', '.fna', '.faa', '.fasta']

for filename in os.listdir(rootDataDir): # Loop over passed directory
    content = os.path.join(rootDataDir, filename)

    if os.path.isdir(content): # If it is a directory
        ncbi_accession.append(filename)

        for filename2 in os.listdir(content): # Loop over the files inside
            content2 = os.path.join(content, filename2)

            if ( (filename in filename2) or ('unplaced' in filename2) or ('chr' in filename2) ) and (os.path.splitext(filename2)[1] in fastaExt): # if they are the genome file
                with open(content2) as file:
                    handle = file.readlines()

                    for line in handle: # loop over genome file lines
                        if line[0] == '>': # if it is the header line
                            org_exp = '\s.+[,|\n]' # Start wit ha space, end on a , or a newline
                            organism_name = re.search( org_exp, line )
                            #print(filename, organism_name)
                            ncbi2org[filename] = organism_name.group()[1:-1]
                            try:
                                organism_list.append( organism_name.group()[1:-1] )
                            except AttributeError:
                                organism_list.append( 'No_Name' )
                            break
                break

            #else:
                #print(filename, filename2, os.path.splitext(filename2)[1], ( (filename in filename2) or ('unplaced' in filename2) ))

#print( f'{len(ncbi_accession)} directories\n{len(organism_list)} Human names\n{len(ncbi2org)} Both' )

with open('relations.txt', 'w') as file:
    """
    for i in range(len(ncbi_accession)-1):
        file.write(f'{ncbi_accession[i]}\t{organism_list[i]}\n')

    finalIndex = len(ncbi_accession) - 1
    file.write(f'{ncbi_accession[finalIndex]}\t{organism_list[finalIndex]}')
    """
    for key, value in ncbi2org.items():
        file.write(f'{key}\t{value}\n')

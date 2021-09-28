#!/usr/bin/env python
import os
import sys
import pandas as pd
import re

# Inputs:
    # tRNASCAN .ss file path

# Outputs:
    # appends to a preexisting csv file

# Usage:

# Purpose:
#   Parse tRNAscan's ss output file and collect
# * Filename
#   * Accession #
# * File contents
#   * Accession # : 1st line
#   * tRNA #      : 1st line
#   * begin genome: 1st line
#   * end genome  : 1st line
#   * length      : 1st line
#   * Isotype     : 2nd line
#   * Anticodon   : 2nd line
#   * Score       : 2nd line
#   * Seq         : 3rd line
#   * SS structure: 4th line


tRNAinfo = {'accession': [],
            'tRNA_num':  [],
            'begin':     [],
            'end':       [],
            'length':    [],
            'isotype':   [],
            'anticodon': [],
            'score':     [],
            'sequence':  [],
            'ss':  []
}
"""
rootDataDir = sys.argv[1]
for filename in os.listdir(rootDataDir): # Loop over passed directory
    content = os.path.join(rootDataDir, filename)
    fileNameAccession=os.path.splitext(filename)[0]
"""
content = sys.argv[1]
outputFile = f'{os.path.basename( os.path.splitext(content)[0])}.csv'

with open(content, 'a') as ssFile: #The way I parse the file requires a newline on the end
    ssFile.write("\n")

with open(content) as ssFile:
    chunk = []
    for n, line in enumerate(ssFile.readlines()):
        if len(chunk) == 6:
            # First line information
            accession_tnum_re = r'^.+\.trna\d+\s'# Looks for 'NC_000913.3.trna1 '
            accession_tnum_name = re.search( accession_tnum_re, chunk[0] )
            if accession_tnum_name:
                accession_tnum_name = accession_tnum_name.group()[0:-1]
            else:
                print(chunk)
                break
            accession = '.'.join( accession_tnum_name.split('.')[0:-1] )
            tnum = accession_tnum_name.split('.')[-1]
            #print(tnum)
            range_re = r'\(\d+-\d+\)'# Looks for (225381-225457)
            range_name = re.search( range_re, chunk[0] ).group()[1:-1]
            begin, end = range_name.split('-')

            length = chunk[0].split('\t')[1].split(' ')[1] # Looks for "NC_000913.3.trna1 (225381-225457)\tLength: 77 bp"

            # Second line information
            isotype = chunk[1].split('\t')[0].split(' ')[1] # Looks for "Type: Ile\tAnticodon: GAT at 35-37 (225415-225417)\tScore: 75.8"
            anticodon = chunk[1].split('\t')[1].split(' ')[1] # Looks for "Type: Ile\tAnticodon: GAT at 35-37 (225415-225417)\tScore: 75.8"
            score = chunk[1].split('\t')[2].split(' ')[1]

            # Third line information
            sequence = chunk[3].split(' ')[1]

            # Fourth line information
            ss = chunk[4].split(' ')[1]

            # Filling the dictionary
            tRNAinfo['accession'].append(accession)
            tRNAinfo['tRNA_num'].append(tnum)
            tRNAinfo['begin'].append(int(begin))
            tRNAinfo['end'].append(int(end))
            tRNAinfo['length'].append(int(length))
            tRNAinfo['isotype'].append(isotype)
            tRNAinfo['anticodon'].append(anticodon)
            tRNAinfo['score'].append(float(score))
            tRNAinfo['sequence'].append(sequence)
            tRNAinfo['ss'].append(ss)

            chunk = []
        if "Possible truncation" not in line:
            chunk.append(line.strip())

pd.DataFrame.from_dict(tRNAinfo).to_csv(outputFile, index=False)

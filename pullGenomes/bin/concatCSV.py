import pandas as pd
import sys
import os

outputFile = "organism_tRNAs.csv"

for file in sys.argv[1:]:
    df = pd.read_csv(file)
    df.to_csv(outputFile, index=False, mode='a', header=False)

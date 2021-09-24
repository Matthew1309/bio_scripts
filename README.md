# bio_scripts
The purpose of this is to compile my little useful scripts into
a nice central repository. 

*WARNING* this might get messy until I learn how to organize :P

====================================================================

## pullGenomes
Currently this repository has a tool to pull down a specified taxon's
reference genomes from ncbi_datasets.

Usage: nextflow run main.nf
Notes: Edit the nextflow.config file to change what taxon is pulled. 
	Can be as generic as typing Enterobacterales to pull 403 ref
	ecoli relatives :)

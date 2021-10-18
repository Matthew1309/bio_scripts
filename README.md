# bio_scripts
The purpose of this is to compile my little useful scripts into
a nice central repository. 

*WARNING* this might get messy until I learn how to organize :P

---

## pullGenomes
Currently this repository has a tool to pull down a specified taxon's
reference genomes from ncbi_datasets.

> **Usage**: nextflow run main.nf

> **Notes**: Edit the nextflow.config file to change what taxon is pulled. 
	Can be as generic as typing Enterobacterales to pull 403 ref
	ecoli relatives :)
---
## notes_parser
The project is supposed to help parse my new note format. 

On a google doc or in a text document if you do this format that I will paste
below


```
***Body

Title: title: Link
Summary/thoughts/insights

========================================================================
Asides:
========================================================================

Vocab: WORD: definition;;;
```

The parse should be able to put this all into convenient dictionaries/look up 
tables. At least that is the hope :)

Future goals:
* Get all the vocab into one place, with pointers to the papers it came from.
* Get all my asides into one place, with dates of when I wrote them down.
* Get a nice format to write this into, and have it add onto it.
* Get it to nicely and automatically pull from a google doc?

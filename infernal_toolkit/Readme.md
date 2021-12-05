# Purpose
Infernal covariance models are a pretty great tool, but fuck me they are picky! They need a multiple alignment stockholm formatted file, that no other tool can automatically generate! It kind of sucks. So I made a fasta to stockholm converting script that takes 
1. multiple sequence alignment fasta file output
2. multiple sequence alignment predicted secondary structure from RNAalifold

and returns to me something that can instantly be input into ```cmbuild```.

# Usage
1. ```conda env create -f "infernal.yml"```
2. ```sed -i 's/ /_/g' input.txt``` this replaces the spaces in the title (they can cause issues)
3. ```clustalo --in=hisps.fa --out=hisps_msa.fa --force```
4. ```RNAalifold --input-format=S hisps_msa.sto > hisps_ss.alifold```
5. Run the contents of file_for_cmbuild.ipynb
6. ```cmbuild hisps.cm hisps_msa.sto```


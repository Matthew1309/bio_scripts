# Well this is a nice little nasty bit of code, but it works
# Usage:
#    python seq_domesticator.py <paste raw seq here>

# If you want different enzymes add them to the bank and
# change the enzymes_of_interest. Also the frame_of_gene
# is a vestige, I don't think I'll be putting genes in that
# don't start from frame one.

# This code will help domesticate sequences
# for use in golden gate.

# Given a list of recognition sites and the frame
# of the sequence (or maybe even using  my old orf
# finder code) find all recognition sites, and
# eliminate them with equivalent substitution of codons
import sys
import random

try:
    inputSequence = sys.argv[1]#"GCAAGAATCCTCCTTCCACTCTACTTGATGTTTT"#
    old_inputSequence = inputSequence
except:
    pass


# User changes this
enzymes_of_interest = ["BpiI", "BsaI"]
frame_of_gene = 1
verbose = False

# Useful dictionaries
###############################################
complement_db = {"A":"T", "T":"A",
                "G":"C", "C":"G"}

res_recog_db = { "BpiI": 'GAAGAC',
                    "BsaI": 'GGTCTC'}
DNA_Codons_db = {
    # 'M' - START, '_' - STOP
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TGT": "C", "TGC": "C",
    "GAT": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "TTT": "F", "TTC": "F",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAT": "H", "CAC": "H",
    "ATA": "I", "ATT": "I", "ATC": "I",
    "AAA": "K", "AAG": "K",
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATG": "M",
    "AAT": "N", "AAC": "N",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TGG": "W",
    "TAT": "Y", "TAC": "Y",
    "TAA": "_", "TAG": "_", "TGA": "_"
}
AMINO_Codons_db = dict()
for key, value in DNA_Codons_db.items():
    AMINO_Codons_db.setdefault(value, list()).append(key)
###############################################

def findEnzymeSites(enzymes_of_interest, inputSequence):
    # Finding the recoginition sites from input
    results = {enzyme:{'occurences':0, 'start_loc_forward':[], 'start_loc_backward':[]} for enzyme in enzymes_of_interest}
    for enzyme in enzymes_of_interest:
        recog_sequence = res_recog_db[enzyme]
        rev_comp_recog_sequence = "".join([complement_db[i] for i in recog_sequence])[::-1]

        results[enzyme]['occurences'] = inputSequence.count(recog_sequence) + inputSequence.count(rev_comp_recog_sequence)
        results[enzyme]['start_loc_forward'] = [i for i in range(len(inputSequence)) if inputSequence.startswith(recog_sequence, i)]
        results[enzyme]['start_loc_backward'] = [i for i in range(len(inputSequence)) if inputSequence.startswith(rev_comp_recog_sequence, i)]

    return results
# I need to get the position (from my dict), check what frame
# the site is in (%), and starting in frame with the first
# letter, see if there are any equivalent substitutions!

# Actual loop that alters the inputSequence
def alterSequence(enzymes_of_interest, results, inputSequence):
    # Helper function to make the necessary substitution
    def break_recognition_site(recog_seq, frame):
        # Frames should be 0,1,2
        # Based on what frame the site is in
        # start at a different spot

        if frame == 1:
            startPoint = 2
        elif frame == 2:
            startPoint = 1
        else:
            startPoint = 0

        # Loop through the recognition site
        replacementSeq = None
        for i in range(startPoint, len(recog_seq), 3):
            currentSeq = recog_seq[i:i+3]
            amino = DNA_Codons_db[currentSeq]

            # If this spot has redundant codons,
            # pick one! Also make sure that this is
            # indeed a list and not just a single codon
            if len(AMINO_Codons_db[amino]) > 1 and type(AMINO_Codons_db[amino]) == list:
                llist = [i for i in AMINO_Codons_db[amino] if i != currentSeq]
                replacementSeq = random.choice(llist)
                # Make the replacement sequence
                recog_seq = recog_seq[:i] + replacementSeq + recog_seq[i+3:]
                break

        return recog_seq
    for enzyme in enzymes_of_interest:
        enz_len = len(res_recog_db[enzyme])
        if verbose:
            print(f'Length of rec site: {enz_len}')
        recog_sequence = res_recog_db[enzyme]
        rev_comp_recog_sequence = "".join([complement_db[i] for i in recog_sequence])[::-1]
        # Replace forward occurences
        for for_occ in results[enzyme]['start_loc_forward']:
            frame = for_occ % 3
            if verbose:
                print(f'For {enzyme}-{recog_sequence} at {for_occ} in frame {frame}: replacement is {break_recognition_site(recog_sequence, frame)}')
            inputSequence = inputSequence[:for_occ] + break_recognition_site(recog_sequence, frame) + inputSequence[for_occ+enz_len:]
        # Replace backward occurences
        for back_occ in results[enzyme]['start_loc_backward']:
            frame = back_occ % 3
            if verbose:
                print(f'For rev {enzyme}-{rev_comp_recog_sequence} at {back_occ} in frame {frame}: replacement is {break_recognition_site(rev_comp_recog_sequence, frame)}')
            inputSequence = inputSequence[:back_occ] + break_recognition_site(rev_comp_recog_sequence, frame) + inputSequence[back_occ+enz_len:]

    return inputSequence

# I have the functions in a loop, because sometimes
# the first round through creates another cut by accident
# and I don't feel like being clever about it, so here
# is the brute force lel
for n in range(3):
    results = findEnzymeSites(enzymes_of_interest, inputSequence)
    inputSequence = alterSequence(enzymes_of_interest, results, inputSequence)

print('writing to output_file.txt')
with open(f'output_file.txt', 'w') as file:
    file.write(inputSequence)

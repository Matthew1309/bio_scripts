# Given a gene, generate 2 primers for the
# type 2 restriction enzyme of choice

# This problem is a bit tougher than expected.
# To generate primers, I also need to generate
# a codon optimized gene. But mostly I need to
# implement a temperature dissociation calculation

# This involves an energy of formation calculation
# and melting temp. which I found here: https://en.wikipedia.org/wiki/Nucleic_acid_thermodynamics
import sys
import random

try:
    inputSequence = "GCAAGAATCCTCCTTCCACTCTACTTGATGTTTT"#sys.argv[1]#
    old_inputSequence = inputSequence
except:
    pass

# User changes this
enzyme_of_interest = "BpiI"
#                       5'        3'
overhangs_of_interest = ['CTCA', 'CGAG']
frame_of_gene = 1
verbose = False

# Useful dictionaries
###############################################
complement_db = {"A":"T", "T":"A",
                "G":"C", "C":"G"}

res_recog_db = { "BpiI": 'GAAGACNN',
                    "BsaI": 'GGTCTCN'}
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

# ATCG
nearest_neighbor_params = {    #     H              S         G37
    #                                kJ/mol, J/(mol*K), kJ/mol
                            "AA": [-33.1, -92.9, -4.26],
                            "AT":[-30.1, -85.4, -3.67],
                            "AC":[-35.6, -95.0, -6.12],
                            "AG":[-34.3, -92.9, -5.51],
                            "TA":[-30.1, -89.1, -2.50],
                            "TC":[-32.6, -87.9, -5.4],
                            "TG":[-35.1, -93.7, -6.09],
                            "CA":[-35.6, -95.0, -6.12],
                            "GT":[-35.1, -93.7, -6.09],
                            "CT":[-32.6, -87.9, -5.4],
                            "GA":[-34.3, -92.9, -5.51],
                            "CG":[-44.4, -113.8, -9.07],
                            "GC":[-41.0, -102.1, -9.36],
                            "GG":[-33.5, -83.3, -7.66],
                            "TT": [-33.1, -92.9, -4.26],
                            "CC": [-33.5, -83.3, -7.66],
                            "A":[9.6, 17.2, 4.31],
                            "T":[9.6, 17.2, 4.31],
                            "G":[0.4, -11.7, 4.05],
                            "C":[0.4, -11.7, 4.05]
                        }


# Helper functions
###############################################
def K(C):
 return C+273.15
def C(K):
    return K-273.15
def calculate_melting_temp(sequence):
    pass

def generate_complement(seq):
    comp = []
    for thing in seq:
        comp.append(complement_db[thing])
    return "".join(comp)
def generate_rev_complement(seq):
    comp = []
    seq = reversed(seq)
    for thing in seq:
        comp.append(complement_db[thing])
    return "".join(comp)

###############################################

#print(complement_db.keys())
primer_1 = f"tt-{''.join([x.lower() if x != 'N' else random.choice(list(complement_db.keys())).lower() for x in res_recog_db['BpiI']])}-{''.join([complement_db[x] for x in overhangs_of_interest[0]])}-end"

sequence_content = [inputSequence[0], inputSequence[-1]]
sequence_content.extend([inputSequence[pos:pos+2] for pos in range(0,len(inputSequence)-1)])
print(sequence_content)

H = [nearest_neighbor_params[x][0] for x in sequence_content]
S = [nearest_neighbor_params[x][1] for x in sequence_content]

melt_temp = (sum(H)/sum(S))*1000
print(C(melt_temp))
print(f'length of sequence: {len(inputSequence)}')
print( nearest_neighbor_params['AT'][0],
        K(37),
        nearest_neighbor_params['AT'][1]*1000,
        (nearest_neighbor_params['AT'][0]*1000)  - (K(37)*nearest_neighbor_params['AT'][1]))

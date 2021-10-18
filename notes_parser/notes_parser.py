import sys
import re
import os
import pandas as pd

try:
    notesFile = sys.argv[1]
except IndexError:
    notesFile = "data/Immune system background.txt"

try:
    outDir = sys.argv[2]
except IndexError:
    outDir = "./data/"

sectionDict = {'title': [],
               'link': [],
               'asides':[],
               'vocab':[]
               }

asideDict = {'title':[]}

vocabDict = {'type':[],
             'word':[],
             'definition':[]
             }

titleIndicator = "* Title:"
asideIndicator = r"Aside:.+"
vocabIndicator = r".+: [A-Z]+:.+;;;"

# Title line extraction
titleExtractor = r":.+?:"# The first of a title line to have this pattern (watch out for colons in link)
linkExtractor = r"http.+"

# Vocab line extraction
typeExtractor = r'.+?:'
wordExtractor = r':.+?:'
definitionExtractor = r';;;.+?:' # backwards regex

def getAttribute(regex, line):
    try:
        att = re.search(regex, line).group()
    except AttributeError:
        att = None

    return att

with open(notesFile) as notesFile:
    line = notesFile.readline()
    while "***Body" not in line: # Find the beginning of the body
        line = notesFile.readline()

    for line in notesFile.readlines():
        if titleIndicator in line: # extracts relevant title information
            titleTitle = getAttribute(titleExtractor,line)
            titleLink = getAttribute(linkExtractor, line)

            sectionDict['title'].append(titleTitle)
            sectionDict['link'].append(titleLink)

            if len(sectionDict['title']) == 1:
                pass
            else:
                sectionDict['asides'].append(asideDict)
                sectionDict['vocab'].append(vocabDict)

            asideDict = {'title':[]}

            vocabDict = {'type':[],
                         'word':[],
                         'definition':[]
                        }

        if re.search(vocabIndicator, line):
            vocabType = getAttribute(typeExtractor, line)
            vocabWord = getAttribute(wordExtractor, line)
            vocabDef = getAttribute(definitionExtractor, line[::-1])[::-1]

            vocabDict['type'].append(vocabType)
            vocabDict['word'].append(vocabWord)
            vocabDict['definition'].append(vocabDef)

        if re.search(asideIndicator, line):
            asideTitle = ":".join(line.split(':')[1:])

            asideDict['title'].append(asideTitle)


    sectionDict['asides'].append(asideDict)
    sectionDict['vocab'].append(vocabDict)


#pd.DataFrame.from_dict(sectionDict).to_csv('test.csv', index=False)
#pd.DataFrame.from_dict(sectionDict['vocab'][0]).to_csv('test2.csv', index=False)

# Future work: Have all the vocabs go into a global dataframe, with another column of what title it corresponds too
# Future work: Have this save all my writing as well

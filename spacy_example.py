import spacy
from spacy.matcher import Matcher
import re

names = []

# pattern
prime_minister_pattern = [{'LOWER':'prime'},
          {'LOWER':'minister'},
          {'POS':'ADP','OP':'?'},
          {'POS':'PROPN'}]

# load english language model
nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

# text = "The children love cream biscuits."
text = "The Prime Minister of India prevented catastrophe. No ministers were here. " \
       "The one near the door was prime minister of Russia"

# create spacy
doc = nlp(text)

# Matcher class object
matcher = Matcher(nlp.vocab)
matcher.add("names", None, prime_minister_pattern)

matches = matcher(doc)

# finding patterns in the text
for i in range(0, len(matches)):
    # match: id, start, end
    token = doc[matches[i][1]:matches[i][2]]
    # append token to list
    names.append(str(token))

print(names)

# Only keep sentences containing Indian PMs
for name in names:
    if (name.split()[2] == 'of') and (name.split()[3] != "India"):
        names.remove(name)

print(names)

for token in doc:
    # print(token.text, '->', token.pos_)
    # extract subject
    if token.dep_ == 'nsubj':
        print('subject ', token.text)
    # extract object
    elif token.dep_ == 'dobj':
        print('object ', token.text)

# spacy.displacy.serve(doc, style='dep')

# to extract initiatives using pattern matching
def all_schemes(text, check):
    schemes = []

    doc = nlp(text)

    # initiatives
    prog_list = ['programme', 'scheme',
                 'initiative', 'campaign',
                 'agreement', 'conference',
                 'alliance', 'plan']

    # pattern to match initiatives names
    pattern = [{'POS': 'DET'},
               {'POS': 'PROPN', 'DEP': 'compound'},
               {'POS': 'PROPN', 'DEP': 'compound'},
               {'POS': 'PROPN', 'OP': '?'},
               {'POS': 'PROPN', 'OP': '?'},
               {'POS': 'PROPN', 'OP': '?'},
               {'LOWER': {'IN': prog_list}, 'OP': '+'}
               ]

    if check == 0:
        # return blank list
        return schemes

    # Matcher class object
    matcher = Matcher(nlp.vocab)
    matcher.add("matching", None, pattern)
    matches = matcher(doc)

    for i in range(0, len(matches)):

        # match: id, start, end
        start, end = matches[i][1], matches[i][2]

        if doc[start].pos_ == 'DET':
            start = start + 1

        # matched string
        span = str(doc[start:end])

        if (len(schemes) != 0) and (schemes[-1] in span):
            schemes[-1] = span
        else:
            schemes.append(span)

    return schemes


# rule to extract initiative name
def sent_subtree(text):
    # pattern match for schemes or initiatives
    patterns = [r'\b(?i)' + 'plan' + r'\b',
                r'\b(?i)' + 'programme' + r'\b',
                r'\b(?i)' + 'scheme' + r'\b',
                r'\b(?i)' + 'campaign' + r'\b',
                r'\b(?i)' + 'initiative' + r'\b',
                r'\b(?i)' + 'conference' + r'\b',
                r'\b(?i)' + 'agreement' + r'\b',
                r'\b(?i)' + 'alliance' + r'\b']

    schemes = []
    doc = nlp(text)
    flag = 0
    # if no initiative present in sentence
    for pat in patterns:

        if re.search(pat, text) != None:
            flag = 1
            break

    if flag == 0:
        return schemes

    # iterating over sentence tokens
    for token in doc:

        for pat in patterns:

            # if we get a pattern match
            if re.search(pat, token.text) != None:

                word = ''
                # iterating over token subtree
                for node in token.subtree:
                    # only extract the proper nouns
                    if (node.pos_ == 'PROPN'):
                        word += node.text + ' '

                if len(word) != 0:
                    schemes.append(word)

    return schemes


import spacy


# кажется тут не учитываются пассивный залог и отрицания
# function for rule 1: noun(subject), verb, noun(object)
def rule1(text):
    doc = nlp(text)

    sent = []

    for token in doc:

        # if the token is a verb
        if (token.pos_ == 'VERB'):

            phrase = ''

            # only extract noun or pronoun subjects
            for sub_tok in token.lefts:

                if (sub_tok.dep_ in ['nsubj', 'nsubjpass']) and (sub_tok.pos_ in ['NOUN', 'PROPN', 'PRON']):

                    # add subject to the phrase
                    phrase += sub_tok.text

                    # save the root of the verb in phrase
                    phrase += ' ' + token.lemma_

                    # check for noun or pronoun direct objects
                    for sub_tok in token.rights:
                        # save the object in the phrase
                        if (sub_tok.dep_ in ['dobj']) and (sub_tok.pos_ in ['NOUN', 'PROPN']):
                            phrase += ' ' + sub_tok.text
                            sent.append(phrase)

    return sent


def rule2(text):
    doc = nlp(text)

    pat = []

    # iterate over tokens
    for token in doc:
        phrase = ''
        # if the word is a subject noun or an object noun
        if (token.pos_ == 'NOUN') \
                and (token.dep_ in ['dobj', 'pobj', 'nsubj', 'nsubjpass']):

            # iterate over the children nodes
            for subtoken in token.children:
                # if word is an adjective or has a compound dependency
                if (subtoken.pos_ == 'ADJ') or (subtoken.dep_ == 'compound'):
                    phrase += subtoken.text + ' '

            if len(phrase) != 0:
                phrase += token.text

        if len(phrase) != 0:
            pat.append(phrase)

    return pat


def rule2_mod(text, index):
    doc = nlp(text)

    phrase = ''

    for token in doc:

        if token.i == index:

            for subtoken in token.children:
                if subtoken.pos_ == 'ADJ' or subtoken.dep_ == 'compound':
                    phrase += ' ' + subtoken.text
            break

    return phrase


# rule 1 modified function
def rule1_mod(text):
    doc = nlp(text)

    sent = []

    for token in doc:
        # root word
        if (token.pos_ == 'VERB'):

            phrase = ''

            # only extract noun or pronoun subjects
            for sub_tok in token.lefts:

                if (sub_tok.dep_ in ['nsubj', 'nsubjpass']) and (sub_tok.pos_ in ['NOUN', 'PROPN', 'PRON']):

                    # look for subject modifier
                    adj = rule2_mod(text, sub_tok.i)

                    phrase += adj + ' ' + sub_tok.text

                    # save the root word of the word
                    phrase += ' ' + token.lemma_

                    # check for noun or pronoun direct objects
                    for sub_tok in token.rights:
                        if (sub_tok.dep_ in ['dobj']) and (sub_tok.pos_ in ['NOUN', 'PROPN']):
                            # look for object modifier
                            adj = rule2_mod(text, sub_tok.i)

                            phrase += adj + ' ' + sub_tok.text
                            sent.append(phrase)
    return sent


# rule 3 function
def rule3(text):
    doc = nlp(text)

    sent = []

    for token in doc:

        # look for prepositions
        if token.pos_ == 'ADP':

            phrase = ''

            # if its head word is a noun
            if token.head.pos_ == 'NOUN':

                # append noun and preposition to phrase
                phrase += token.head.text
                phrase += ' ' + token.text

                # check the nodes to the right of the preposition
                for right_tok in token.rights:
                    # append if it is a noun or proper noun
                    if (right_tok.pos_ in ['NOUN', 'PROPN']):
                        phrase += ' ' + right_tok.text

                if len(phrase) > 2:
                    sent.append(phrase)

    return sent


# rule 0
def rule0(text, index):
    doc = nlp(text)

    token = doc[index]

    entity = ''

    for sub_tok in token.children:
        if (sub_tok.dep_ in ['compound', 'amod']):
            entity += sub_tok.text + ' '

    entity += token.text

    return entity


# rule 3 function
def rule3_mod(text):
    doc = nlp(text)

    sent = []

    for token in doc:

        if token.pos_ == 'ADP':

            phrase = ''
            if token.head.pos_ == 'NOUN':

                # appended rule
                append = rule0(text, token.head.i)
                if len(append) != 0:
                    phrase += append
                else:
                    phrase += token.head.text
                phrase += ' ' + token.text

                for right_tok in token.rights:
                    if (right_tok.pos_ in ['NOUN', 'PROPN']):

                        right_phrase = ''
                        # appended rule
                        append = rule0(text, right_tok.i)
                        if len(append) != 0:
                            right_phrase += ' ' + append
                        else:
                            right_phrase += ' ' + right_tok.text

                        phrase += right_phrase

                if len(phrase) > 2:
                    sent.append(phrase)

    return sent


nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
text1 = 'As Bezos began his opening remarks, his image was expanded to take up the whole TV screen, but it appeared that the Cisco Webex videoconferencing service only showed a blank screen.'
text2 = 'The people of India believe in the principles of the United Nations'
text3 = 'Tech titans face video glitches in congressional testimony'
text = text3
print(rule1(text))
print(rule2(text))
print(rule1_mod(text))
print(rule3(text))
print(rule3_mod(text))

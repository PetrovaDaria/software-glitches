# import stanza
#
# stanza.download('en', processors='tokenize,ner')
# nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
import main


def fill_duration(text):
    doc = main.nlp(text)
    entities = doc.ents
    times = []
    for ent in entities:
        if ent.type == 'TIME' or ent.type == 'DATE':
            times.append(ent.text)
    return times

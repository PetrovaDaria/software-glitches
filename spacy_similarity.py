import spacy
from spacy import displacy

# load english language model
nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
sentence = 'A tech failure at the Bank of England that hit wholesale transactions has been fixed'
sentence2 = 'British supermarket chain Tesco Plc said on Tuesday a computer glitch had resulted in the cancellation of many home deliveries'
doc = nlp(sentence)
doc2 = nlp(sentence2)
#displacy.serve(doc, style='dep')
displacy.serve(doc2, style='dep')

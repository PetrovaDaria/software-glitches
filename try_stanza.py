import stanza
import nltk

stanza.download('en', processors='tokenize,ner')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
doc = nlp("Chris Manning teaches at Stanford University. "
          "He lives in the Bay Area. It costs 1 million dollars. "
          "It happened at 20.11.2020. There were 3 cats. "
          "Also it was at eleventh of Novemver. At 11th of April."
          "Two thousand rubles. Ural Federal University. Fastdev startup. Tochka bank. Petrova Daria. Twitter, Vkontakte, iCloud")
print(doc.ents)
doc2 = nlp('Nothing here')
print(doc2.ents)
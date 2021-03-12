import flair
import stanza
from parse_org import get_orgs
from wikidata.wikidata_sparql import is_software_company

text = '''
A tech failure at the Bank of England that hit wholesale transactions has been fixed, although Threadneedle Street warned that the glitch will result in delays.
The Bank admitted on Thursday evening that its IT system was suffering “intermittent technology communication problems” following a “regular internal update”.
The problem impaired the central bank’s ability to process a limited number of transactions for wholesale counterparties, leading it to implement “workarounds” to enable the Bank to operate as normal.
However, on Friday morning, the Bank said that the issue had been fixed overnight, but said that wholesale counterparty transactions may be delayed as it plays catch up.
A statement read: “Technology communications problems reported by the Bank yesterday have been fixed overnight.
“Systems are now working normally, although there is some catch-up work to complete.
“We expect to be able to process business as normal today, but in order to catch up from yesterday, wholesale counterparty transactions may be dealt with somewhat later in the day than usual.”
The governor of the Bank of England Mark Carney (PA)
The real-time gross settlement (RTGS) service and the Chaps system, which retail banking customers rely on, were not affected so the general public will see “no impact on any of their banking services”, the Bank added.
In 2014, the Bank suffered an IT outage that did affect Chaps and RTGS, impacting thousands of transactions such as home sales.
Following the debacle, Governor Mark Carney ordered a “thorough, independent review” of the payments system.
'''

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
sentences = text.split('.')
sentences = [sentence.replace('\n', '') for sentence in sentences]
sentences = list(filter(lambda x: len(x) > 0, sentences))
negative_sentences_with_sent_score = []
for sentence in sentences:
    flair_sentence = flair.data.Sentence(sentence)
    flair_sentiment.predict(flair_sentence)
    tone = flair_sentence.labels[0].value
    score = flair_sentence.labels[0].score
    if tone == 'NEGATIVE':
        negative_sentences_with_sent_score.append({
            'sentence': sentence,
            # 'tone': tone,
            'score': score
        })
# sorted_sentences = sorted(negative_sentences_with_sent_score, key = lambda x: (x['tone'], -x['score']))
sorted_negative_sentences_with_sent_score = sorted(negative_sentences_with_sent_score, key=lambda x: -x['score'])
print(sorted_negative_sentences_with_sent_score)
sorted_negative_sentences = [item['sentence'] for item in sorted_negative_sentences_with_sent_score]

stanza.download('en', processors='tokenize,ner')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
for sentence in sorted_negative_sentences:
    doc = nlp(sentence)
    orgs = get_orgs(doc)

import stanza
from textblob import TextBlob
import flair

stanza.download('en', processors='tokenize,sentiment,ner')
nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment,ner')


text = '''
YouBike offline due to system glitch. Staff writer, with CNA The public bike rental service YouBike was 
temporarily suspended in six cities and counties in northern and central Taiwan yesterday morning due to 
software damage during a system update, but the service was expected to resume normal operations within two days, 
YouBike spokesperson Liu Li-chu (劉麗珠) said. Liu said that the system went down at 1:30am when an update of 
the remote-control system of the parking slots failed. The system breakdown has resulted in the malfunction of 
17,317 parking slots in Taipei, New Taipei City, Hsinchu, Taoyuan, Taichung and Changhua, and affected 140,000 people,
including 100,000 to 110,000 users in the greater Taipei area, Liu said. Liu said that the company has informed 
the public transportation departments of the cities and counties and sent engineers to YouBike parking lots around
the nation to repair the control system. The service in Taichung and Changhua is expected to resume sooner than 
others, Liu added. The glitch is estimated to have caused at least NT$1 million (US$31,530) in financial 
losses in Taipei and New Taipei City. Soon after the system went down, the company’s management urged users to 
take other forms of transportation to get to their destinations. The large-scale breakdown is unprecedented in 
the history of the public bike rental system, which was formally launched in Taipei in November 2012 and was 
expanded to New Taipei City at the end of 2013, to Taichung and Changhua in 2014 and then to Taoyuan and 
Hsinchu this year.'''

doc2 = nlp(text)
for i, sentence in enumerate(doc2.sentences):
    print(sentence.text)
    print('stanze sentiment ', sentence.sentiment)
    print(TextBlob(sentence.text).sentiment)
    if sentence.sentiment == 0:
        print(sentence.ents)


flair_sentiment = flair.models.TextClassifier.load('en-sentiment')


text = '''
3BB back to normal after major technical issues on Saturday.
A technical issue with Thai internet provider 3BB meant that customers were unable 
to access Google services on Saturday (May 6). 
The problem began on Saturday morning when customers throughout 
Thailand took to the Thaivisa forum to complain they were unable to 
access Google websites including YouTube, Gmail and Google News.
Even the 3BB website was offline, as for a time, was its 1530 call centre number.'''


def is_negative_sentence(sentence):
    '''
    Проверить, имеет ли предложение негативный оттенок
    :param sentence: предложение
    :return: True - если негативное, иначе False
    '''
    flair_sentence = flair.data.Sentence(sentence)
    flair_sentiment.predict(flair_sentence)
    return flair_sentence.labels[0] == 'NEGATIVE'

import flair
from text_utils import text_to_sentences


def get_sorted_negative_sentences(text):
    '''
    По тексту получить список негативно окрашенных предложений, отсортированный в порядке убывания негатива
    :param text: текст
    :return: список предложений
    '''
    sentences = text_to_sentences(text)
    negative_sentences_with_sent_score = []

    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    for sentence in sentences:
        flair_sentence = flair.data.Sentence(sentence)
        flair_sentiment.predict(flair_sentence)
        tone = flair_sentence.labels[0].value
        score = flair_sentence.labels[0].score
        if tone == 'NEGATIVE':
            negative_sentences_with_sent_score.append({
                'sentence': sentence,
                'score': score
            })
    sorted_negative_sentences_with_sent_score = sorted(negative_sentences_with_sent_score, key=lambda x: -x['score'])
    return [item['sentence'] for item in sorted_negative_sentences_with_sent_score]

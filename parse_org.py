import pandas as pd
import stanza
import flair


def get_orgs(doc):
    '''
    Получение организаций из текста
    :param doc: документ, предобрабатанный stanza
    :return: словарь: ключ - название организации, значение - количество раз в тексте
    '''
    entities = doc.ents
    orgs = {}
    for ent in entities:
        if ent.type == 'ORG':
            if ent.text not in orgs.keys():
                orgs[ent.text] = 0
            orgs[ent.text] += 1
    orgs = dict(sorted(orgs.items(), key=lambda item: item[1], reverse=True))
    return orgs


def get_negative_text(text, flair_sentiment):
    sentences = list(filter(lambda x: len(x) > 0, text.split('.')))
    negative_sentences = []
    for sentence in sentences:
        flair_sentence = flair.data.Sentence(sentence)
        flair_sentiment.predict(flair_sentence)
        is_negative = flair_sentence.labels[0].value == 'NEGATIVE'
        if is_negative:
            negative_sentences.append(sentence)
    negative_text = '.'.join(negative_sentences)
    return negative_text


def get_money(doc):
    entities = doc.ents
    moneys = []
    for ent in entities:
        if ent.type == 'MONEY':
            moneys.append(ent.text)
    print(moneys)


def main():
    stanza.download('en', processors='tokenize,ner')
    nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    initial_csv = pd.read_csv('twenty-good-news-with-dicts.csv', sep='\t')
    csv_with_parsed_org = pd.DataFrame(
        columns=[
            'id',
            'url',
            'archive_name',
            'date',
            'title',
            'text',
            'manual_entities',
            'predicted_entities'
        ]
    )
    rows_count = initial_csv.shape[0]
    for i in range(rows_count):
        current_row = initial_csv.loc[i]
        title_and_text = current_row.title + ' ' + current_row.text
        doc1 = nlp(title_and_text)
        get_orgs(doc1)
        negative_text = get_negative_text(title_and_text, flair_sentiment)
        doc2 = nlp(negative_text)
        get_orgs(doc2)
        get_money(doc1)
        get_money(doc2)
    #     csv_with_parsed_org.loc[i] = [
    #         current_row.id,
    #         current_row.url,
    #         current_row.archive_name,
    #         current_row.date,
    #         current_row.title,
    #         current_row.text,
    #         current_row.manual_entities,
    #         current_row.predicted_entities
    #     ]
    # csv_with_parsed_org.to_csv('twenty-good-news-with-dicts.csv', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()

# import stanza
#
# stanza.download('en', processors='tokenize,ner')
# nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
import main


def fill_money_from_stanza_doc(doc):
    '''
    Получение списка денег из документа, полученного из stanza
    :param doc: stanza-документ
    :return: список денег
    '''
    entities = doc.ents
    moneys = []
    for ent in entities:
        if ent.type == 'MONEY':
            moneys.append(ent.text)
    return moneys


def fill_money(text):
    '''
    Получение списка денег из текста
    :param text: текст
    :return: список денег
    '''
    doc = main.nlp(text)
    return fill_money_from_stanza_doc(doc)



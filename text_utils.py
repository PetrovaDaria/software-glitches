from words_lists.words_lists import bug_words

def text_to_sentences(text):
    '''
    Текст в список предложений
    :param text: текст
    :return: список предложений
    '''
    sentences = text.split('.')
    sentences = [sentence.replace('\n', '') for sentence in sentences]
    sentences = list(filter(lambda x: len(x) > 0, sentences))
    return sentences


def get_text_with_glitch_words(text):
    '''
    Оставить в тексте только предложения, содержащие слова, означающие сбои/проблемы
    :param text: текст
    :return: текст, состоящий только из предложений со словами-сбоями
    '''
    sentences = text_to_sentences(text)
    sentences_with_glitch = []
    for sentence in sentences:
        for bug_word in bug_words:
            if bug_word in sentence:
                sentences_with_glitch.append(sentence + '.')
    return ' '.join(sentences_with_glitch)

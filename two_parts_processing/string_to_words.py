import re
import string

punctuation = '[{}\n\t]+'.format(string.punctuation)


def delete_tags(text):
    return re.sub('<.*?>', ' ', text)


def delete_punctuation(text):
    return re.sub(punctuation, '', text)


# \n, \s, \t, \\
def delete_spaces(text):
    return re.sub(r'(\\+[snt]?)+', ' ', text)


def delete_sixteen_symbols(text):
    return re.sub(r'[^\x00-\x7f]', ' ', text)


def delete_empty_words(words):
    return list(filter(lambda x: x != '', words))


def get_words_simply(record):
    record = delete_tags(record)
    record = delete_punctuation(record)
    record = delete_spaces(record)
    record = delete_sixteen_symbols(record)
    parts = record.split(' ')
    parts = delete_empty_words(parts)
    return parts
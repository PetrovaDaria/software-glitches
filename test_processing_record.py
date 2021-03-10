import re
import string
from newspaper import Article
from words_lists import software_words, bug_words
import time
import pandas as pd
from warcio.archiveiterator import ArchiveIterator


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


def get_words_with_newspaper(record):
    article = Article(url='test')
    article.download(input_html=record)
    article.parse()
    text = article.title.lower() + article.text.lower()
    text = delete_punctuation(text)
    text = delete_sixteen_symbols(text)
    parts = text.split(' ')
    parts = delete_empty_words(parts)
    return parts


def get_words_simply(record):
    record = delete_tags(record)
    record = delete_punctuation(record)
    record = delete_spaces(record)
    record = delete_sixteen_symbols(record)
    parts = record.split(' ')
    parts = delete_empty_words(parts)
    return parts


def get_words_stat(dict_words, text_words):
    stat = {}
    for dict_word in dict_words:
        word_count = text_words.count(dict_word)
        if word_count > 0:
            stat[dict_word] = word_count
    return stat


def get_software_news_stat(words):
    return get_words_stat(software_words, words)


def get_bug_words_stat(words):
    return get_words_stat(bug_words, words)


def is_software_bug_news(software_stat, bug_stat):
    return len(software_stat.keys()) > 0 and len(bug_stat.keys()) > 0


def process_approach(get_words_func, record):
    finding_words_start_time = time.time()
    words = get_words_func(record)
    current_time = time.time()
    words_count = len(words)
    finding_words_time = current_time - finding_words_start_time
    print('Finding array of words: %s seconds' % finding_words_time)
    getting_stat_start_time = time.time()
    software_stat = get_software_news_stat(words)
    bug_stat = get_bug_words_stat(words)
    current_time = time.time()
    getting_stat_time = current_time - getting_stat_start_time
    print('Getting stat: %s seconds' % getting_stat_time)
    print('software stat ', software_stat)
    print('bug stat ', bug_stat)
    is_news = is_software_bug_news(software_stat, bug_stat)
    print('is news ', is_news)
    return finding_words_time, words_count, getting_stat_time, software_stat, bug_stat, is_news


# with open('one_record.txt', 'r') as f:
#     record = f.read()
#     print('simply')
#     process_approach(get_words_simply, record)
#     print('with newspaper')
#     process_approach(get_words_with_newspaper, record)


def test_processing(web_archive_path, out_csv_filename):
    df = pd.DataFrame(
        columns=['id', 'url', 'parse_record_time', 'simply_get_words_time', 'simply_words_count', 'simply_get_stat_time', 'simply_software_stat',
                 'simply_bug_stat', 'simply_is_news', 'newspaper_get_words_time', 'newspaper_words_count',
                 'newspaper_get_stat_time', 'newspaper_software_stat', 'newspaper_bug_stat', 'newspaper_is_news'])

    with open(web_archive_path, 'rb') as stream:
        i = 0
        for record in ArchiveIterator(stream):
            url = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response':
                parse_record_start_time = time.time()
                try:
                    text = record.content_stream().read().decode('utf-8')
                    current_time = time.time()
                    parse_record_time = current_time - parse_record_start_time
                    print('Parse record: %s seconds' % parse_record_time)
                    print('simply')
                    simply_finding_words_time, simply_words_count, simply_getting_stat_time, \
                    simply_software_stat, simply_bug_stat, simply_is_news = \
                        process_approach(get_words_simply, text)
                    print('with newspaper')
                    newspaper_finding_words_time, newspaper_words_count, newspaper_getting_stat_time, \
                    newspaper_software_stat, newspaper_bug_stat, newspaper_is_news = \
                        process_approach(get_words_with_newspaper, text)
                    df.loc[i] = [
                        i,
                        url,
                        parse_record_time,
                        simply_finding_words_time,
                        simply_words_count,
                        simply_getting_stat_time,
                        simply_software_stat,
                        simply_bug_stat,
                        simply_is_news,
                        newspaper_finding_words_time,
                        newspaper_words_count,
                        newspaper_getting_stat_time,
                        newspaper_software_stat,
                        newspaper_bug_stat,
                        newspaper_is_news
                    ]
                except Exception as e:
                    print('Record ', i, ' ', e)
            i += 1
    df.to_csv(out_csv_filename, sep='\t', encoding='utf-8')


def get_csv_stat(csv_filename):
    df = pd.read_csv(csv_filename, delimiter='\t')
    sum_simply_get_words_time = df['simply_get_words_time'].sum()
    sum_newspaper_get_words_time = df['newspaper_get_words_time'].sum()
    median_simply_get_words_time = df['simply_get_words_time'].median()
    max_simply_get_words_time = df['simply_get_words_time'].max()
    print('median_simply_get_words_time', median_simply_get_words_time)
    print('max_simply_get_words_time', max_simply_get_words_time)
    median_newspaper_get_words_time = df['newspaper_get_words_time'].median()
    max_newspaper_get_words_time = df['newspaper_get_words_time'].max()
    print('median_newspaper_get_words_time', median_newspaper_get_words_time)
    print('max_newspaper_get_words_time', max_newspaper_get_words_time)
    sum_simply_get_stat_time = df['simply_get_stat_time'].sum()
    sum_newspaper_get_stat_time = df['newspaper_get_stat_time'].sum()
    simply_faster_newspaper_getting_words = (df['newspaper_get_words_time'] - df['simply_get_words_time'])\
        .apply(lambda diff: diff > 0)\
        .value_counts()\
        .to_dict()
    print(simply_faster_newspaper_getting_words)
    diff_get_words = (abs(df['newspaper_get_words_time'] - df['simply_get_words_time'])).mean()
    print(diff_get_words)
    print(sum_simply_get_words_time)
    print(sum_newspaper_get_words_time)
    print(sum_simply_get_stat_time)
    print(sum_newspaper_get_stat_time)
    simply_is_news_count = df['simply_is_news'].value_counts().to_dict()
    print(simply_is_news_count)
    newspaper_is_news_count = df['newspaper_is_news'].value_counts().to_dict()
    print(newspaper_is_news_count)
    newspaper_is_news_indices = df[df['newspaper_is_news'] == True]['id'].tolist()
    print(newspaper_is_news_indices)


def main():
    # web_archive_path = 'news.warc.gz'
    out_csv_filename = 'test_processing_record.csv'
    # test_processing(web_archive_path, out_csv_filename)
    get_csv_stat(out_csv_filename)


if __name__ == '__main__':
    main()

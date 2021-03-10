from warcio.archiveiterator import ArchiveIterator
import pandas as pd
from two_parts_processing.string_to_words import get_words_simply
from two_parts_processing.get_words_stat import get_software_news_stat, get_bug_words_stat, is_software_bug_news, get_collocations


def simply_process_record(record):
    words = get_words_simply(record)
    words_count = len(words)
    software_stat = get_software_news_stat(words)
    bug_stat = get_bug_words_stat(words)
    collocations = get_collocations(words, 3)
    is_news = is_software_bug_news(software_stat, bug_stat)
    return words_count, software_stat, bug_stat, collocations, is_news


def simply_process_archive(web_archive_path, out_csv_filename):
    df = pd.DataFrame(
        columns=['id', 'url', 'simply_words_count', 'simply_software_stat',
                 'simply_bug_stat', 'simply_collocations', 'simply_is_news',
                 'text'
                 ])

    with open(web_archive_path, 'rb') as stream:
        i = 0
        news_i = 0
        for record in ArchiveIterator(stream):
            url = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response':
                try:
                    text = record.content_stream().read().decode('utf-8')
                    words_count, software_stat, bug_stat, collocations, is_news = simply_process_record(text)
                    # тут точно будут и новости с collocations
                    more_than_one_for_each_category = \
                        is_news and \
                        sum(software_stat.values()) > 1 and \
                        sum(bug_stat.values()) > 1
                    if more_than_one_for_each_category:
                        df.loc[news_i] = [
                            i,
                            url,
                            words_count,
                            software_stat,
                            bug_stat,
                            collocations,
                            is_news,
                            text
                        ]
                        news_i += 1
                except Exception as e:
                    print('Record ', i, ' ', e)
            i += 1
    df.to_csv(out_csv_filename, sep='\t', encoding='utf-8')


def simply_process_archive_with_logger(web_archive_path, out_csv_filename, logger):
    df = pd.DataFrame(
        columns=['id', 'url', 'simply_words_count', 'simply_software_stat',
                 'simply_bug_stat', 'simply_collocations', 'simply_is_news',
                 'text'
                 ])

    with open(web_archive_path, 'rb') as stream:
        i = 0
        news_i = 0
        for record in ArchiveIterator(stream):
            if i % 100 == 0:
                logger.info('Archive {}. {} records were processed'.format(web_archive_path, i))
            url = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response':
                try:
                    text = record.content_stream().read().decode('utf-8')
                    words_count, software_stat, bug_stat, collocations, is_news = simply_process_record(text)
                    # тут точно будут и новости с collocations
                    more_than_one_for_each_category = \
                        is_news and \
                        sum(software_stat.values()) > 1 and \
                        sum(bug_stat.values()) > 1
                    if more_than_one_for_each_category:
                        df.loc[news_i] = [
                            i,
                            url,
                            words_count,
                            software_stat,
                            bug_stat,
                            collocations,
                            is_news,
                            text
                        ]
                        news_i += 1
                except Exception as e:
                    logger.info('Archive {}. Record {} has error: {}'.format(web_archive_path, i, e))
                    print('Record ', i, ' ', e)
            i += 1
    df.to_csv(out_csv_filename, sep='\t', encoding='utf-8')
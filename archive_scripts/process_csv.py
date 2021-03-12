import pandas as pd
from two_parts_processing.process_archive_simply import simply_process_record
import os


def second_time_process(initial_csv_file_name, new_csv_file_name):
    initial_df = pd.read_csv(initial_csv_file_name, sep='\t')
    rows_count = initial_df.shape[0]
    news_i = 0
    new_df = pd.DataFrame(
            columns=['id', 'url', 'words_count', 'software_stat',
                     'bug_stat', 'collocations', 'is_news',
                     'title ', 'text'
                     ])
    for i in range(rows_count):
        current_row = initial_df.loc[i]
        text = current_row.title + ' ' + current_row.text
        words_count, software_stat, bug_stat, collocations, is_news = simply_process_record(text)
        more_than_one_for_each_category = \
            is_news and \
            sum(software_stat.values()) > 1 and \
            sum(bug_stat.values()) > 1
        if more_than_one_for_each_category:
            new_df.loc[news_i] = [
                i,
                current_row.url,
                words_count,
                software_stat,
                bug_stat,
                collocations,
                is_news,
                current_row.title,
                current_row.text
            ]
            news_i += 1
    new_df.to_csv(new_csv_file_name, sep='\t', encoding='utf-8')


# second_time_process('example.csv', 'new.csv')
print(os.listdir('dire/subdire'))
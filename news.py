from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
import json
import pandas as pd


url_header = 'WARC-Target-URI'
response_record_type = 'response'

# столбцы таблицы
# название архива
# id записи в архиве
# url
# название
# основной текст
# встретившиеся словосочетания


def main():
    with open('news.warc.gz', 'rb') as stream:
        i = 0
        for record in ArchiveIterator(stream):
            url = record.rec_headers.get_header(url_header)
            if record.rec_type == response_record_type:
                text = record.content_stream().read()
                article = Article(url='test')
                article.download(input_html=text)
                article.parse()
                # проверить, есть ли подходящие словосочетания в названии
                # проверить, есть ли подходящее словосочетания в тексте
            i += 1


if __name__ == '__main__':
    main()

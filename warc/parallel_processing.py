import subprocess
import time
import json
import logging
from multiprocessing import Process
from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
from warc.parse_warc \
    import get_software_and_bug_words_from_news, \
    is_possible_software_and_bug_news, \
    form_news, \
    is_software_and_bug_news


download_path = "https://cloudstor.aarnet.edu.au/plus/s/M8BvXxe6faLZ4uE/download?path=%2Fwarc&files={}"


def process_archive(archive_name, logger):
    possible_software_bug_news = []
    software_bug_news = []
    possible_news_json_name = "news/possible_news_{}".format(archive_name)
    news_json_name = "news/news_{}".format(archive_name)

    try:
        with open(archive_name, 'rb') as stream:
            i = 0
            for record in ArchiveIterator(stream):
                if i % 100 == 0:
                    logger.info("Archive {}. {} records were processed already".format(archive_name, i))
                url = record.rec_headers.get_header('WARC-Target-URI')
                if record.rec_type == 'response':
                    text = record.content_stream().read()
                    article = Article(url='test')
                    article.download(input_html=text)
                    article.parse()
                    software_words_dict, bug_words_dict, title_collocations, text_collocations = \
                        get_software_and_bug_words_from_news(article.title, article.text)
                    is_possible_news = is_possible_software_and_bug_news(software_words_dict, bug_words_dict)
                    if is_possible_news:
                        news = form_news(i, article, url, software_words_dict, bug_words_dict,
                                         title_collocations, text_collocations)
                        possible_software_bug_news.append(news)
                        is_needed_news = is_software_and_bug_news(title_collocations, text_collocations)
                        if is_needed_news:
                            software_bug_news.append(news)
                i += 1
            logger.info("Archive {}. {} records".format(archive_name, i))
        with open(possible_news_json_name, 'w') as f:
            json.dump(possible_software_bug_news, f, indent=2)
        with open(news_json_name, 'w') as f:
            json.dump(software_bug_news, f, indent=2)
    except Exception as ex:
        logger.error("Archive {}. ERROR {}".format(archive_name, ex))
    logger.info("Archive {}. Possible news count: {}. News count: {}.".format(
        archive_name,
        len(possible_software_bug_news),
        len(software_bug_news)
    ))


def process_web_archive(archive_names, logger):
    for archive_name in archive_names:
        # download web-archive
        subprocess.run(["wget",
                        "-O",
                        archive_name,
                        download_path.format(archive_name)
                        ])
        logger.info('Archive {}. Downloaded.'.format(archive_name))

        # recompress archive
        new_archive_name = "./recompressed_{}".format(archive_name)
        subprocess.run([
            "warcio",
            "recompress",
            "./{}".format(archive_name),
            new_archive_name
        ])
        logger.info("Archive {}. Recompressed.".format(archive_name))

        # processing
        process_archive(new_archive_name, logger)

        # delete web-archive
        subprocess.run(["rm",
                        archive_name])
        subprocess.run(["rm",
                        new_archive_name])
        logger.info('Archive {}. Deleted.'.format(archive_name))


def get_indices(arr_len, parts_count):
    indices = []
    for i in range(parts_count):
        indices.append(arr_len * i // parts_count)
    indices.append(arr_len)
    return indices


def get_arr_parts(arr, indices):
    arr_parts = []
    for i in range(1, len(indices)):
        print(i)
        arr_parts.append(arr[indices[i - 1]:indices[i]])
    return arr_parts


if __name__ == '__main__':
    parts_count = 4
    logging.basicConfig(filename="logs/{}.log".format(time.ctime(time.time())))
    loggers = []
    for name in ['first', 'second', 'third', 'fourth']:
        logger = logging.getLogger(name)
        loggers.append(logger)

    with open("warcs_list.txt", 'r') as f:
        names = f.readlines()
        indices = get_indices(len(names), parts_count)
        names_parts = get_arr_parts(names, indices)

        processes = []
        i = 0
        for name_part in names_parts:
            proc = Process(target=process_web_archive, args=(name_part, loggers[i]))
            processes.append(proc)
            proc.start()
            i += 1

        for proc in processes:
            proc.join()

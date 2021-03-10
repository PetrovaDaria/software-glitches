import subprocess
import time
import json
import logging
from multiprocessing import Process
from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
from parse_warc \
    import get_software_and_bug_words_from_news, \
    is_possible_software_and_bug_news, \
    form_news, \
    is_software_and_bug_news
from two_parts_processing.process_archive_simply import simply_process_archive_with_logger


download_path = "https://cloudstor.aarnet.edu.au/plus/s/M8BvXxe6faLZ4uE/download?path=%2Fwarc&files={}"
processes_number = 8


def process_web_archive(archive_names, logger):
    i = 1
    for archive_name in archive_names:
        archive_name = archive_name.rstrip('\n')
        out_csv_filename = './two_parts_processing/csvs/{}.csv'.format(archive_name)
        # download web-archive
        logger.info("Archive {}. Started downloading.".format(archive_name))
        try:
            subprocess.run(["wget",
                            "-O",
                            archive_name,
                            download_path.format(archive_name)
                            ])
            logger.info('Archive {}. Downloaded.'.format(archive_name))
        except Exception as ex:
            logger.error("Archive {}. ERROR in downloading: {}".format(archive_name, ex))

        # recompress archive
        new_archive_name = "./recompressed_{}".format(archive_name)
        logger.info("Archive {}. Started recompressing.".format(archive_name))
        try:
            subprocess.run([
                "warcio",
                "recompress",
                "./{}".format(archive_name),
                new_archive_name
            ])
            logger.info("Archive {}. Recompressed.".format(archive_name))
        except Exception as ex:
            logger.error("Archive {}. ERROR in recompressing {}".format(archive_name, ex))

        # processing
        simply_process_archive_with_logger(new_archive_name, out_csv_filename, logger)

        # delete web-archive
        try:
            subprocess.run(["rm",
                            archive_name])
            subprocess.run(["rm",
                            new_archive_name])
            logger.info('Archive {}. Deleted.'.format(archive_name))
        except Exception as ex:
            logger.error("Archive {}. ERROR in recompressing: {}.".format(archive_name, ex))

        logger.info("Archive {}. Finished.".format(archive_name))
        logger.info("{} archives were finished.".format(i))
        i += 1


def get_indices(arr_len, parts_count):
    indices = []
    for i in range(parts_count):
        indices.append(arr_len * i // parts_count)
    indices.append(arr_len)
    return indices


def get_arr_parts(arr, indices):
    arr_parts = []
    for i in range(1, len(indices)):
        arr_parts.append(arr[indices[i - 1]:indices[i]])
    return arr_parts


if __name__ == '__main__':
    current_time = time.time()
    readable_current_time = time.ctime(current_time)
    subprocess.run([
        "mkdir",
        ".two_parts_processing/logs/{}".format(current_time)
    ])
    logging.basicConfig(level=logging.INFO)
    loggers = []
    for name in range(processes_number):
        logger = logging.getLogger(str(name))
        log_name = "logs/{}/{}-{}.log".format(current_time, readable_current_time, name)
        open(log_name, 'w').close()
        fh = logging.FileHandler(log_name)
        logger.addHandler(fh)
        loggers.append(logger)

    with open("warcs_list.txt", 'r') as f:
        names = f.readlines()
        indices = get_indices(len(names), processes_number)
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

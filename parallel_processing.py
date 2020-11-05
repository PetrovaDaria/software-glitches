import subprocess
import logging
import time
from multiprocessing import Process

logging.basicConfig(filename='log1.txt', level=logging.INFO)
download_path = "https://cloudstor.aarnet.edu.au/plus/s/M8BvXxe6faLZ4uE/download?path=%2Fwarc&files={}"


def process_web_archive(archive_names):
    for archive_name in archive_names:
        # download web-archive
        subprocess.run(["wget",
                        "-O",
                        archive_name,
                        download_path.format(archive_name)
                        ])
        logging.info('downloaded file {}'.format(archive_name))

        # processing
        # ...

        # delete web-archive
        subprocess.run(["rm",
                        archive_name])
        logging.info('deleted file {}'.format(archive_name))


def get_indices(arr_len, parts_count):
    indices = []
    for i in range(parts_count):
        indices.append(arr_len * i // parts_count)
    return indices


def get_arr_parts(arr, indices):
    arr_parts = []
    for i in range(1, len(indices)):
        arr_parts.append(arr[indices[i - 1], indices[i]])
    return arr_parts


if __name__ == '__main__':
    start_time = time.time()
    parts_count = 4
    names = ["CC-NEWS-20170202093341-00045_ENG.warc.gz", "CC-NEWS-20161222115112-00000_ENG.warc.gz"]
    indices = get_indices(len(names), parts_count)

    names_parts = get_arr_parts(names, indices)
    processes = []
    for name_part in names_parts:
        proc = Process(target=process_web_archive, args=(name_part,))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    print("--- %s seconds ---" % (time.time() - start_time))


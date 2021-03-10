from two_parts_processing.two_parts_processing import two_parts_processing
import time


def main():
    # web_archive_path = 'news.warc.gz'
    # out_csv_filename = 'two_parts_processing/csvs/simple_processing.csv'
    web_archive_path = 'news.warc.gz'
    out_csv_filename = 'two_parts_processing/csvs/simple_processing.csv'
    start_time = time.time()
    two_parts_processing(web_archive_path, out_csv_filename)
    end_time = time.time()
    print('%s seconds' % (end_time - start_time))


if __name__ == '__main__':
    main()
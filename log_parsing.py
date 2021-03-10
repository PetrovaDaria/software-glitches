import re
import json


def get_seconds(line):
    result = re.search(r'took ([\d.]+) seconds', line)
    return float(result.group(1))


def get_archive_name(line):
    result = re.search(r'Archive (.*).warc', line)
    return result.group(1)


def get_recomressed_archive_name(line):
    result = re.search(r'./recompressed_(.*).warc', line)
    return result.group(1)


def get_logs_stats(log_file_name, out_stats_file_name):
    downloading_time = 0
    recompressing_time = 0
    processing_time = 0
    total_records_count = 0
    possible_news_count = 0
    with_collocations_count = 0
    archives_count = 0

    logs_stats = {}
    with open(log_file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'Downloading took' in line:
                current_downloading_time = get_seconds(line)
                downloading_time += current_downloading_time
                archive_name = get_archive_name(line)
                logs_stats[archive_name] = {}
                logs_stats[archive_name]['downloading_time'] = current_downloading_time
                archives_count += 1
            if 'Recompressing took' in line:
                current_recompressing_time = get_seconds(line)
                recompressing_time += current_recompressing_time
                archive_name = get_archive_name(line)
                logs_stats[archive_name]['recompressing_time'] = current_recompressing_time
            if 'Processing took' in line:
                current_processing_time = get_seconds(line)
                processing_time += current_processing_time
                archive_name = get_archive_name(line)
                logs_stats[archive_name]['processing_time'] = current_processing_time
            if 'Total' in line:
                result = re.search(r'Total (\d+) records', line)
                current_total_records_count = int(result.group(1))
                total_records_count += current_total_records_count
                archive_name = get_recomressed_archive_name(line)
                logs_stats[archive_name]['total_records_count'] = current_total_records_count
            if 'Possible news' in line:
                result = re.search(r'news (\d+)', line)
                current_possible_news_count = int(result.group(1))
                archive_name = get_recomressed_archive_name(line)
                possible_news_count += current_possible_news_count
                logs_stats[archive_name]['possible_news_count'] = current_possible_news_count
            if 'with collocations' in line:
                result = re.search(r'collocations (\d+)', line)
                current_with_collocations_count = int(result.group(1))
                with_collocations_count += current_with_collocations_count
                archive_name = get_recomressed_archive_name(line)
                logs_stats[archive_name]['with_collocations_count'] = with_collocations_count

    print('Log file ', log_file_name)
    print('Archives count ', archives_count)
    print('Downloading time ', downloading_time)
    print('Recompressing time ', recompressing_time)
    print('Processing time ', processing_time)
    print('Total records count ', total_records_count)
    print('Possible news count ', possible_news_count)
    print('With collocations count ', with_collocations_count)

    with open(out_stats_file_name, 'w') as f:
        json.dump(logs_stats, f, indent=2)


get_logs_stats('example.log', 'logs_stats.json')

downloading_time = 0
recompressing_time = 0
processing_time = 0
total_records_count = 0
possible_news_count = 0
with_collocations_count = 0

with open('example.log', 'r') as f:
    lines = f.readlines()
    downloading_lines = list(filter(lambda x: 'Downloading took' in x, lines))
    recompressing_lines = list(filter(lambda x: 'Recompressing took' in x, lines))
    processing_lines = list(filter(lambda x: 'Processing took' in x, lines))
    total_records_lines = list(filter(lambda x: 'Total' in x, lines))
    possible_news_lines = list(filter(lambda x: 'Possible news' in x, lines))
    with_collocations_lines = list(filter(lambda x: 'with collocations' in x, lines))
    for downloading_line in downloading_lines:
        downloading_time += get_seconds(downloading_line)
    for recompressing_line in recompressing_lines:
        recompressing_time += get_seconds(recompressing_line)
    for processing_line in processing_lines:
        processing_time += get_seconds(processing_line)
    for total_records_line in total_records_lines:
        result = re.search(r'Total (\d+) records', total_records_line)
        records_count = int(result.group(1))
        total_records_count += records_count
    for possible_news_line in possible_news_lines:
        result = re.search(r'news (\d+)', possible_news_line)
        records_count = int(result.group(1))
        possible_news_count += records_count
    for with_collocations_line in with_collocations_lines:
        result = re.search(r'collocations (\d+)', with_collocations_line)
        records_count = int(result.group(1))
        with_collocations_count += records_count

print('Downloading time ', downloading_time)
print('Recompressing time ', recompressing_time)
print('Processing time ', processing_time)
print('Total records count ', total_records_count)
print('Possible news count ', possible_news_count)
print('With collocations count ', with_collocations_count)

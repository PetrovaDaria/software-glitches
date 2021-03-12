from cloudstor import cloudstor

warcs_url = 'https://cloudstor.aarnet.edu.au/plus/s/M8BvXxe6faLZ4uE'
warcs_password = ''
warc_names_path = 'warcs_list.txt'

warcs_dir = cloudstor(url=warcs_url, password=warcs_password)
warc_list = warcs_dir.list('warc')
with open(warc_names_path, 'w') as f:
    for name in warc_list:
        if name.startswith('CC-NEWS'):
            f.write('{}\n'.format(name))



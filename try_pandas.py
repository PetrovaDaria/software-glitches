import pandas as pd

trial_data = [
    {
        'archive': '20160901',
        'id': '5',
        'url': 'https://lalala.com/very-important-news',
        'title': 'Software glitch was found in Microsoft',
        'text': 'Errors in software are everywhere, even in Windows 2020.',
        'collocations': ['software glitch', 'errors in software'],
        'words': {
            'software': 2,
            'glitch': 1,
            'error': 1
        }
    }
]
df = pd.DataFrame(trial_data)
df.to_csv('news.csv', sep='\t', encoding='utf-8', index=False)

df = pd.read_csv('news.csv', delimiter='\t')
trial_data2 = [
    {
        'archive': '20160902',
        'id': '10',
        'url': 'https://lalala.com/very-important-news2',
        'title': 'Software glitch was found in Google',
        'text': 'Errors in software are everywhere, even in Google Chrome',
        'collocations': ['software glitch', 'errors in software'],
        'words': {
            'software': 2,
            'glitch': 1,
            'error': 1
        }
    }
]
current_df = pd.DataFrame(trial_data2)
result_df = pd.concat([df, current_df])
result_df.to_csv('news.csv', sep='\t', encoding='utf-8', index=False)

df = pd.read_csv('news.csv', delimiter='\t')
print(df.head())

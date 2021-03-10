import pandas as pd

entities_dict = {
    # hardware/software/network
    'glitch_type': [],
    # company-victim
    'victim': [],
    # company-maker of glitched software
    'manufacturer': [],
    # duration of glitch
    'duration': [],
    'severity_scale': [],
    'money_loss': [],
    'other_loss': [],
    'reason': []
}
initial_csv = pd.read_csv('twenty-good-news.csv', sep='\t')
csv_with_dicts = pd.DataFrame(
    columns=[
        'id',
        'url',
        'archive_name',
        'date',
        'title',
        'text',
        'manual_entities',
        'predicted_entities'
    ]
)
rows_count = initial_csv.shape[0]
for i in range(rows_count):
    current_row = initial_csv.loc[i]
    csv_with_dicts.loc[i] = [
        current_row.id,
        current_row.url,
        current_row.archive_name,
        current_row.date,
        current_row.title,
        current_row.text,
        entities_dict,
        entities_dict
    ]
csv_with_dicts.to_csv('twenty-good-news-with-dicts.csv', sep='\t', encoding='utf-8')

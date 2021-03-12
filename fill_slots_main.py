from fill_slots import fill_slots_configurations
import pandas as pd


def fill_slots_main():
    initial_csv = pd.read_csv('./twenty-good-news-with-dicts.csv', sep='\t')
    rows_count = initial_csv.shape[0]
    new_csv = pd.DataFrame(
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
    for i in range(rows_count):
        text = initial_csv.loc[i].title + ' ' + initial_csv.loc[i].text
        filled_slots = fill_slots_configurations.basic_fill_slots(text)
        print(filled_slots)
        current_row = initial_csv.loc[i]
        new_csv.loc[i] = [
            current_row.id,
            current_row.url,
            current_row.archive_name,
            current_row.date,
            current_row.title,
            current_row.text,
            current_row.manual_entities,
            filled_slots
        ]
    new_csv.to_csv('predicted_dicts.csv', sep='\t', encoding='utf-8', index=False)


if __name__ == '__main__':
    fill_slots_main()

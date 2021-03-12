import stanza
import json
import fill_slots_main

stanza.download('en', processors='tokenize,ner')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

is_software_company_cache_path = 'is_software_company_cache.json'
is_software_company_cache = {}
with open(is_software_company_cache_path, 'r') as f:
    is_software_company_cache = json.load(f)


def main():
    fill_slots_main.fill_slots_main()
    print('cache ', is_software_company_cache)
    with open(is_software_company_cache_path, 'w') as f:
        json.dump(is_software_company_cache, f)


if __name__ == '__main__':
    main()

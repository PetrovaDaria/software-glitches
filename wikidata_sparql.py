import re

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql_url = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper(sparql_url)

search_query_template = '''
SELECT distinct ?item ?itemLabel ?itemDescription WHERE{{  
  ?item ?label "{}"@en.  
  ?article schema:about ?item .
  ?article schema:inLanguage "en" .
  ?article schema:isPartOf <https://en.wikipedia.org/>.	
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}    
}}
'''

instanceof_query_template = '''
SELECT ?item ?itemLabel
WHERE
{{
    wd:{} wdt:P31 ?item .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
'''

produced_product_query_template = '''
SELECT ?item ?itemLabel
WHERE
{{
    wd:{} wdt:P1056 ?item .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
'''

industry_query_template = '''
SELECT ?item ?itemLabel
WHERE
{{
    wd:{} wdt:P452 ?item .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
'''

all_subclasses_query_template = '''
SELECT ?item ?itemLabel
WHERE
{{
    wd:{} wdt:P279+ ?item.
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
'''

instance_of_subclasses_query_template = '''
SELECT ?item ?itemLabel
WHERE
{{
    wd:{} wdt:P31/wdt:P279+ ?item.
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
'''

# Q1668024 - service on internet
# Q7397 - software
# Q17155032 - software category
# Q21198 - computer science
software_products = ['Q1668024', 'Q7397', 'Q17155032', 'Q21198']

# Q18388277 - technology company
# Q2401749 - telecommunication company
technology_companies = ['Q18388277', 'Q2401749']

# Q880371 - software industry
# Q11661 - information technology
# Q75 - Internet
industries = ['Q880371', 'Q11661', 'Q75']

def get_entity_id(url):
    result = re.search(r'http://www.wikidata.org/entity/(Q\d+)', url)
    return result.group(1)


def execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    return results_df


def print_results(results_df):
    if 'item.value' in results_df and 'itemLabel.value' in results_df:
        print(results_df[['item.value', 'itemLabel.value']])
    else:
        print('no such property')


def get_product_ids(entity_id):
    produced_product_query = produced_product_query_template.format(entity_id)
    results_df = execute_query(produced_product_query)
    if results_df.empty:
        return []
    else:
        urls = list(results_df['item.value'])
        return [get_entity_id(url) for url in urls]


def get_instance_subclasses_ids(entity_id):
    instance_of_subclasses_query = instance_of_subclasses_query_template.format(entity_id)
    results_df = execute_query(instance_of_subclasses_query)
    if results_df.empty:
        return []
    else:
        urls = list(results_df['item.value'])
        return [get_entity_id(url) for url in urls]


def get_instances_ids(entity_id):
    all_subclasses_query = all_subclasses_query_template.format(entity_id)
    results_df = execute_query(all_subclasses_query)
    if results_df.empty:
        return []
    else:
        urls = list(results_df['item.value'])
        return [get_entity_id(url) for url in urls]


def has_software_products(entity_id):
    product_ids = get_product_ids(entity_id)
    all_instances_ids = product_ids.copy()
    for product_id in product_ids:
        instances_ids = get_instances_ids(product_id)
        all_instances_ids += instances_ids
    for software_product in software_products:
        if software_product in all_instances_ids:
            return True
    return False


def is_technology_company(entity_id):
    instances_ids = get_instance_subclasses_ids(entity_id)
    for technology_company_id in technology_companies:
        if technology_company_id in instances_ids:
            return True
    return False


def get_industries_ids(entity_id):
    industry_query = industry_query_template.format(entity_id)
    results_df = execute_query(industry_query)
    if results_df.empty:
        return []
    else:
        urls = list(results_df['item.value'])
        return [get_entity_id(url) for url in urls]


def is_it_industry(entity_id):
    industries_ids = get_industries_ids(entity_id)
    all_instances_ids = industries_ids.copy()
    for industry_id in industries_ids:
        instances_ids = get_instances_ids(industry_id)
        all_instances_ids += instances_ids
    for industry in industries:
        if industry in all_instances_ids:
            return True
    return False


def is_software_company(word):
    search_query = search_query_template.format(word)
    results_df = execute_query(search_query)
    if results_df.empty:
        print('not existed word')
        return False
    else:
        urls = list(results_df['item.value'])
        searched_entity_ids = [get_entity_id(url) for url in urls]
        for searched_entity_id in searched_entity_ids:
            if is_technology_company(searched_entity_id):
                return True
            if is_it_industry(searched_entity_id):
                return True
            if has_software_products(searched_entity_id):
                return True
        return False


def main():
    print(is_software_company('Bank of England'))


if __name__ == '__main__':
    main()
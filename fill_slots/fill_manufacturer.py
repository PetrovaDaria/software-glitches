from wikidata.wikidata_sparql import is_software_company
from parse_org import get_orgs
from text_utils import get_text_with_glitch_words
# import stanza
#
# stanza.download('en', processors='tokenize,ner')
# nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

import main


def fill_manufacturer(text):
    text_with_glitch_words = get_text_with_glitch_words(text)
    doc = main.nlp(text_with_glitch_words)
    orgs = get_orgs(doc)
    software_companies = []
    for org in orgs:
        if org in main.is_software_company_cache.keys():
            if main.is_software_company_cache[org]:
                software_companies.append(org)
        else:
            if is_software_company(org):
                software_companies.append(org)
                main.is_software_company_cache[org] = True
            else:
                main.is_software_company_cache[org] = False
    return software_companies


def get_coefficients(count):
    coefficients = []
    current_coeff = 1
    for i in range(count - 1):
        current_coeff /= 2
        coefficients.append(current_coeff)
    coefficients.append(current_coeff)
    if count > 1:
        last_diff = coefficients[-1] * 0.3
        coefficients[-1] -= last_diff
        coefficients[-2] += last_diff
    print(coefficients)
    return coefficients

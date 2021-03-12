import main
from parse_org import get_orgs
from text_utils import get_text_with_glitch_words
from wikidata.wikidata_sparql import is_software_company


def fill_victim(text):
    text_with_glitch_words = get_text_with_glitch_words(text)
    doc = main.nlp(text_with_glitch_words)
    orgs = get_orgs(doc)
    for org in orgs:
        if org in main.is_software_company_cache.keys():
            if not main.is_software_company_cache[org]:
                return [org]
        else:
            if is_software_company(org):
                main.is_software_company_cache[org] = True
            else:
                main.is_software_company_cache[org] = False
                return [org]
    return []

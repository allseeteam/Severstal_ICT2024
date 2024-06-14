import xml.etree.ElementTree as ET
import requests
from io import StringIO


def parse_doc(doc, position):
    passages = []
    passages_obj = doc.find('passages')
    if passages_obj:
        for passage in passages_obj:
            passage = ''.join(list(passage.itertext()))
            if passage:
                passages.append(passage)
    return {
        'url': doc.find('url').text,
        'domain': doc.find('domain').text,
        'title': doc.find('title').text,
        'size': int(doc.find('size').text),
        'passages': passages,
        'position': position
    }


def ya_search(query, api_key):
    url = f'https://yandex.ru/search/xml?query={query}&folderid=b1gjpg4fsjcau2oceikv&l10n=ru&sortby=rlv&maxpassages=1'
    headers = {
        'Authorization': f'Api-Key {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(
            f'Search API status code {response.status_code}\n\nContent: {response.content}')
    return get_serp_from_xml(StringIO(response.content.decode('utf-8')))


def get_serp_from_xml(content):
    tree = ET.parse(content)
    root = tree.getroot().find('response')
    serp = []
    position = 1
    for group in root.find('results').find('grouping'):
        if group.tag == 'group':
            doc = group.find('doc')
            serp.append(parse_doc(doc, position))
            position += 1
    return serp

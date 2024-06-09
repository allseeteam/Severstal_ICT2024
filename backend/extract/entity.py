from extract.html import get_tables_from_raw_html
from extract.process_df import (
    get_entities_from_html_df,
    deduplicate_entities,
    calculate_ratios,
    find_header,
    filter_entities
)
import json
import pandas as pd


def prepare_raw_data(df):
    """
    сюда передаем вот эту csv
    $ python manage.py model2csv accounts.WebPage > pages.csv
    """
    print('parsing html...')
    entities = get_entities_from_html_df(df)
    print('deduplicating tables...')
    deduplicated_entities = deduplicate_entities(entities)
    print('calculating statistics...')
    entities = calculate_ratios(deduplicated_entities)
    entities = filter_entities(entities)
    entities = apply_to_data(entities, find_header)
    return entities


def apply_to_data(entities, func):
    for entity in entities:
        entity['frame'] = func(entity['frame'])
    return entities


def jsonify_df(df):
    return df.to_json()


def save_entities(entities, path):
    jsonified_entities = apply_to_data(entities, jsonify_df)
    with open(path, 'w') as f:
        f.write(json.dumps(jsonified_entities))


def read_entities(path):
    with open(path) as f:
        entities = json.loads(f.read())
    entities = apply_to_data(entities, read_entity_from_json)
    return entities


def read_entity_from_json(df_in_json):
    return pd.read_json(df_in_json)

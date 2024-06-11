from io import StringIO
from extract.process_df import (
    get_entities_from_html_df,
    get_entities_from_html,
    deduplicate_entities,
    calculate_ratios,
    find_header,
    filter_entities,
)
from extract.utils import jsonify_df, dictify_df
import json
import pandas as pd


def prepary_entities(raw_html, url):
    """
    не-векторизованная версия prepare_raw_data

    также хранит данные (поле frame) как строку (для записи в json поле)
    """
    print(raw_html)
    print()
    print()
    print()
    entities = get_entities_from_html(raw_html, url)
    entities = deduplicate_entities(entities)
    entities = calculate_ratios(entities)
    # entities = filter_entities(entities)
    # entities = apply_to_data(entities, find_header)
    entities = apply_to_data(entities, dictify_df)
    print(entities)
    return entities


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


def apply_to_data(entities, func, key='frame'):
    for entity in entities:
        entity[key] = func(entity[key])
    return entities


def save_entities(entities, path):
    jsonified_entities = apply_to_data(entities, jsonify_df)
    with open(path, 'w') as f:
        f.write(json.dumps(jsonified_entities))


def read_entities(path):
    with open(path) as f:
        entities = json.loads(f.read())
    entities = apply_to_data(entities, read_entity_from_json)
    return entities


def read_entities_dict(path):
    with open(path) as f:
        entities = json.loads(f.read())
    return entities


def read_entity_from_json(df_in_json):
    return pd.read_json(StringIO(df_in_json))

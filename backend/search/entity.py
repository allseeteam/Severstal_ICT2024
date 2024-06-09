import pandas as pd
from search.text import normalize_string


def normalize_entity(entity):
    content = normalize_string(entity['meta'])
    df_content = normalize_string(get_text_from_df(entity['frame']))
    return content + '\n' + df_content


def hash_df(df):
    return pd.util.hash_pandas_object(df, index=True).sum()


def get_entity_id(entity):
    return f'{entity["url"]}@{hash_df(entity["frame"])}'


def get_url_from_entity_id(entity_id):
    return '@'.join(entity_id.split('@')[:-1])


def get_text_from_df(df):
    return normalize_string(df.to_string())

import pandas as pd
from search.text import normalize_string


def normalize_entity(entity):
    content = normalize_string(entity['meta'])
    df_content = normalize_string(get_text_from_df(entity['frame']))
    return content + '\n' + df_content


def get_text_from_df(df):
    return normalize_string(df.to_string())

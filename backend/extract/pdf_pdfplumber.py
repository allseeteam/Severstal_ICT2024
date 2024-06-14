import pdfplumber
import numpy as np
import pandas as pd
import tqdm
from extract.utils import get_float_values_ratio


def parse_tables_with_pdfplumber(path):
    pdf = read_pdf_pdfplumber(path)
    parsed_dfs = _parse_tables_pdfplumber(pdf)
    return parsed_dfs


def _parse_tables_pdfplumber(pdf):
    parsed_dfs = []
    for i, page in enumerate(tqdm.tqdm(pdf.pages)):
        df, text = search_best_table(page)
        if df is not None:
            parsed_dfs.append({'page': i, 'df': df, 'text': text})
    return parsed_dfs


def preprocess_df(df):
    to_replace = ['X', 'Х', '', '-', '—']
    df = df.replace(to_replace, None).dropna(
        axis=0, how='all').dropna(axis=1, how='all')
    df['_row_float_ratio'] = df.apply(get_float_values_ratio, axis=1)
    df = df[df['_row_float_ratio'] > 0.2]
    df = df.drop('_row_float_ratio', axis=1)
    return df


def read_pdf_pdfplumber(path):
    return pdfplumber.open(path)


def get_settings_variants():
    variants = []
    for vertical in ['text', 'lines']:
        for horizontal in ['text', 'lines']:
            for snap_y_tolerange in [3]:
                for intersection_x_tolerance in [10]:
                    variants.append({
                        "vertical_strategy": vertical,
                        "horizontal_strategy": horizontal,
                        "snap_y_tolerance": snap_y_tolerange,
                        "intersection_x_tolerance": intersection_x_tolerance,
                    })
    return variants


def get_df_from_page(page, settings):
    table = page.extract_table(settings)
    if table:
        return pd.DataFrame(table)


def search_best_table(page):
    text = page.extract_text()
    base_df = page.extract_table()
    if base_df:
        return pd.DataFrame(base_df), text
    dfs = []
    for variant in get_settings_variants():
        df = get_df_from_page(page, variant)

        if df is not None:
            # проверяем, стал ли отличаться датафрейм от предыдущего
            if len(dfs) == 0 or not df.equals(dfs[-1]):
                dfs.append(df)
    # определяем, что лучший датафрейм - тот, где больше всего не-null значений
    # (наивная эвристика)
    best_df_idx = np.argmax(map(lambda x: x.shape[0] * x.shape[1], dfs))
    best_df = dfs[best_df_idx]
    if get_float_values_ratio(best_df) > 0:
        return best_df, text
    return None

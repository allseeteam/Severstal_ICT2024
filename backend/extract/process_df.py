from collections import Counter

from tqdm import tqdm
from extract.html import get_tables_from_raw_html
from extract.utils import calc_type_distribution


def get_entities_from_html_df(df):
    all_entities = []
    for _, row in tqdm(df.iterrows()):
        entities = get_entities_from_html(row.content, row.url)
        for entity in entities:
            all_entities.append(entity)
    return all_entities


def get_entities_from_html(content, url):
    entities = []
    dataframes = get_tables_from_raw_html(content, only_df=False)
    for frame in dataframes:
        entities.append(
            {'url': url, 'frame': frame['data'],
                'meta': {'title': frame['meta']}}
        )
    return entities


def filter_entities(entities, float_threshold=0.5, datetime_threshold=0.5):
    def check(x):
        return x['float_per_row'] > float_threshold and x['datetime_per_row'] > datetime_threshold
    usefull_entities = list(filter(check, entities))
    return usefull_entities


def deduplicate_entities(tables):
    deduplicated = []
    for i in tqdm(range(len(tables))):
        is_duplicate = False
        for j in range(len(deduplicated)):
            if tables[i]['frame'].equals(deduplicated[j]['frame']):
                is_duplicate = True
                break
        if not is_duplicate:
            deduplicated.append(tables[i])
    return deduplicated


def calculate_ratios(tables):
    for row in tables:
        type_distr = calc_type_distribution(row['frame'])
        row.update(type_distr)
    return tables


def find_header(df):
    # проходимся по каждой колонке
    # определяем ее тип (float, datetime, str)
    # для флота и дейттайма пытаемся жадно подобрать header_size
    # делаем шаг и проверяем, стало ли больше похоже на правду
    # дальше проводим majority vote по колонкам и ставим хединг
    if len(df) <= 2:
        return df

    header_sizes = []
    for col in df.columns:
        col_value = df[col]
        distr_raw = calc_type_distribution(col_value)
        if distr_raw['str_per_row'] >= 0.5:
            col_dtype = 'str'
            continue
        elif distr_raw['float_val_count'] >= distr_raw['datetime_val_count']:
            col_dtype = 'float'
            col_type = 'float_per_row'
        elif distr_raw['datetime_val_count'] > distr_raw['float_val_count']:
            col_dtype = 'datetime'
            col_type = 'datetime_per_row'
        else:
            continue

        if distr_raw[col_type] == 1:
            header_sizes.append(0)
            continue

        val_per_row = distr_raw[col_type]
        prev_val_per_row = val_per_row
        for i in range(1, 4):
            distr_i_row_header = calc_type_distribution(col_value.iloc[i:])
            if distr_i_row_header[col_type] <= prev_val_per_row:
                header_sizes.append(i - 1)
                break
            else:
                prev_val_per_row = distr_i_row_header[col_type]

    header_size = Counter(header_sizes).most_common(1)  # [0][0]
    if header_size:
        header_size = header_size[0][0]
    else:
        header_size = 0

    if header_size > 0:
        df.columns = [df.iloc[i, :] for i in range(header_size)]
        df = df.iloc[header_size:]
    return df

import pandas as pd


def hash_df(df):
    return pd.util.hash_pandas_object(df, index=True).sum()


def get_entity_id(entity):
    return f'{entity["url"]}@{hash_df(entity["frame"])}'


def get_url_from_entity_id(entity_id):
    return '@'.join(entity_id.split('@')[:-1])


def get_float_values_ratio(df):
    distr = calc_type_distribution(df)
    float_ratio = distr['float_val_count'] / distr['total_count']
    return float_ratio


def calc_type_distribution(df, prefix=''):
    if df is None:
        return
    if len(df.shape) == 1:
        rows_total = df.shape[0]
        cols_total = 0
    elif len(df.shape) == 2:
        rows_total, cols_total = df.shape
    na_val_count = 0
    float_val_count = 0
    datetime_val_count = 0
    str_val_count = 0
    total_count = 0
    for val in df.values.flatten().tolist():
        val_type = get_type(val)
        if val_type == 'na':
            na_val_count += 1
        elif val_type == 'datetime':
            datetime_val_count += 1
        elif val_type == 'float':
            float_val_count += 1
        else:
            str_val_count += 1
        total_count += 1

    if total_count == 0:
        na_ratio = 1
        datetime_per_row = 0
        float_per_row = 0
        str_per_row = 0
    else:
        na_ratio = na_val_count / total_count
        datetime_per_row = datetime_val_count / rows_total
        float_per_row = float_val_count / rows_total
        str_per_row = str_val_count / rows_total

    return {
        prefix + 'float_val_count': float_val_count,
        prefix + 'datetime_val_count': datetime_val_count,
        prefix + 'na_val_count': na_val_count,
        prefix + 'str_val_count': str_val_count,
        prefix + 'total_count': total_count,

        prefix + 'rows_total': rows_total,
        prefix + 'cols_total': cols_total,

        prefix + 'na_ratio': na_ratio,
        prefix + 'datetime_per_row': datetime_per_row,
        prefix + 'float_per_row': float_per_row,
        prefix + 'str_per_row': str_per_row,
    }


def get_type(x):
    if is_na(x):
        return 'na'
    elif is_datetime(x):
        return 'datetime'
    elif is_float(x):
        return 'float'
    return 'str'


def is_datetime(x):
    return is_type(x, lambda x: pd.to_datetime(x, infer_datetime_format=True))


def is_float(x):
    return is_type(x, convert_to_float)


def is_na(x):
    return x is None or x == ''


units = ['₽', 'р.', '$']


def convert_to_float(x):
    x = str(x)
    if x.startswith('0'):
        raise ValueError("it's not a float")
    x = x.replace(',', '.')
    for unit in units:
        x = x.replace(unit, '')
    return float(x)


def is_type(x, type):
    try:
        type(x)
        return True
    except ValueError:
        pass
    except TypeError:
        pass
    except OverflowError:
        # print('Overflow error:', x)
        pass
    return False
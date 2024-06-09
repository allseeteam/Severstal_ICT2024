import numpy as np


def rank(candidates):
    ranked = sorted(candidates, key=lambda x: x[8])
    ranked = [(doc[1], doc[8]) for doc in ranked]
    return ranked


def calc_factors(query, doc):
    static_factors = calc_static_factors(doc)
    dynamic_factors = calc_dynamic_factors(query, doc)

    factors = static_factors | dynamic_factors
    return factors


def factors_to_list(query, url, factors):
    ordered_factors = sorted(factors.items(), key=lambda x: x[0])
    factor_values = list(map(lambda x: x[1], ordered_factors))
    return [query, url] + factor_values


def calc_static_factors(entity):
    return {
        'is_cbr': calc_is_cbr(entity),
        'is_wiki': calc_is_wiki(entity),
        'is_html_table': calc_is_html_table(entity),
        'is_pdf_table': calc_is_pdf_table(entity),
        'is_series': calc_is_series(entity),
        'float_ratio': calc_float_ratio(entity),
        'datetime_ratio': calc_datetime_ratio(entity),
        'str_ratio': calc_str_ratio(entity),
    }


def calc_dynamic_factors(words, entity):
    return {
        'bm25': calc_bm25(words, entity),
        'idf_sum': calc_idf_sum(words, entity),
        'bm25sy': calc_bm25sy(words, entity),
        'bm25tr': calc_bm25tr(words, entity),
        'log_word_count': calc_log_word_count(words, entity),
        'is_report': calc_is_report(words, entity),
    }


def calc_is_cbr(entity):
    return 1


def calc_is_wiki(entity):
    return 1


def calc_is_html_table(entity):
    return 1


def calc_is_pdf_table(entity):
    return 1


def calc_is_series(entity):
    return 1


def calc_float_ratio(entity):
    return entity.get('float_per_row', 0)


def calc_datetime_ratio(entity):
    return entity.get('datetime_per_row', 0)


def calc_str_ratio(entity):
    return entity.get('str_per_row', 0)


def calc_bm25(words, entity):
    return 0


def calc_idf_sum(words, entity):
    return 0


def calc_bm25sy(words, entity):
    return 0


def calc_bm25tr(words, entity):
    """bm25 translated"""
    return 0


def calc_log_word_count(words, entity):
    return np.log(len(words))


def calc_is_report(words, entity):
    return 0

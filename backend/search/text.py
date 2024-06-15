import re


def normalize_whitespace(s):
    s = re.sub("\s+", " ", s)
    return s.strip()


def normalize_whitespace_v2(s):
    return ' '.join(s.split())


def normalize_punctuation(input_string: str) -> str:
    return re.sub(r"[^\w\s]+", ' ', input_string)


def normalize_case(s):
    return s.lower()


def normalize_string(s):
    pipeline = [
        normalize_case,
        normalize_whitespace,
        normalize_whitespace_v2,
        normalize_punctuation,
    ]
    for op in pipeline:
        s = op(s)
    return s


def remove_newlines(s):
    return s.replace('\\n', ' ').replace('\\t', ' ')


def normalize_string_repr(s):
    if not isinstance(s, str):
        s = str(s)
    pipeline = [
        remove_newlines,
        normalize_whitespace_v2,
    ]
    for op in pipeline:
        s = op(s)
    return s

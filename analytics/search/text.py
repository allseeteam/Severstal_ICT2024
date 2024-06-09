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

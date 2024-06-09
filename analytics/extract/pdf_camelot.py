import camelot


def parse_pdf_with_camelot(path):
    tables = camelot.read_pdf(path)
    dfs = []
    for table in tables:
        dfs.append(table.df)
    return dfs

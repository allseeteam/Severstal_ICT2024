import bs4
import pandas as pd
import numpy as np
import tqdm


import xml.etree.ElementTree as et


def read_html_file(path):
    with open(path) as file:
        content = file.read()
    return content


def get_tables_from_raw_html(content: str, only_df=True) -> list[dict]:
    """
    Парсит строку content с HTML.
    Возвращает список таблиц в формате
    [{'data': df, 'meta': caption}]
    """
    tree = bs4.BeautifulSoup(content, features="html.parser")

    tables = []
    for table in tree.find_all('table'):
        caption, table_list = html2list(str(table))
        if caption == '':
            caption = tree.find('title').text
        df = pd.DataFrame(table_list)
        if only_df:
            tables.append(df)
        else:
            tables.append({'data': df, 'meta': caption})
    return tables


def html2list(table):
    """Функция со stackoverflow для парсинга таблиц из html"""
    if isinstance(table, str):
        table = et.fromstring(table)

    # parse caption
    caption = table.find("caption")
    caption = caption.text if caption is not None else ''

    # parse table
    content = []
    rowspans = {}
    contents = {}

    for elem in table.iter(tag="tr"):
        row = []
        cell_index = 0

        for cell in list(elem):
            cell_text = ''.join(cell.itertext()).strip()

            rowspan = cell.get("rowspan")
            if rowspan:
                rowspan = rowspan.replace(';', '')
            rowspans[cell_index] = int(rowspan) if rowspan else (
                rowspans.get(cell_index, 0))
            if rowspan is not None:
                contents[cell_index] = cell_text

            if rowspan is None and rowspans[cell_index] > 0:
                row.append(contents[cell_index])
                rowspans[cell_index] -= 1

            colspan = cell.get("colspan")
            if colspan:
                colspan = colspan.replace(';', '')
            colspan = int(colspan) if colspan else 1
            row.extend([''.join(cell_text)] * colspan)

            cell_index += colspan
        content.append(row)

    return caption, content

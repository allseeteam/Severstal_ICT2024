import pickle
import click
import pandas as pd
from extract import prepare_raw_data
from search import SearchEngine


@click.command()
@click.option('--path', help='Путь до csv файла')
@click.option('--output', default='search.pkl', help='Путь до csv файла')
def main(path, output):
    """
    1) Читаем csv файл (path) с html документами
    2) Забираем оттуда таблички
    3) Кладем в инвертированный индекс в структуре SearchEngine
    4) Пиклим в output
    """
    print(f'Reading {path}')
    df = pd.read_csv(path)
    print(f'Read table with {len(df)} rows')
    entities = prepare_raw_data(df)
    se = SearchEngine()
    se.bulk_index_entities(entities)
    print(f'Saving search engine to {output}')
    pickle.dump(se, open(output, 'wb'))


if __name__ == '__main__':
    main()

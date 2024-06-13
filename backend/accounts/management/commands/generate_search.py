import json
import pickle

import pandas as pd

from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

from extract import read_html
from search import SearchEngine
from accounts import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('output', default='search.pkl',
                            type=str, help='Output file')

    def handle(self, output, *args, **options):
        """
        1) Читаем из базы энтити
        2) Кладем в инвертированный индекс в структуре SearchEngine
        3) Пиклим в output
        """
        entities = models.Data.objects.all()
        print(f'Read {len(entities)} entities')
        entities = [model_to_dict(r) for r in entities]
        for entity in entities:
            # print(entity['index_id'], entity['page'])
            entity['frame'] = read_html(entity['data'])
            entity['meta'] = entity['meta_data']['title']
            # break
        se = SearchEngine()
        se.bulk_index_entities(entities)
        print(f'Saving search engine to {output}')
        pickle.dump(se, open(output, 'wb'))

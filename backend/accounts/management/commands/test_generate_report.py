import csv
import sys

from django.core.management.base import BaseCommand
from accounts import models
from django.forms.models import model_to_dict
from extract import preprocess_entities, get_one_figure_by_entity


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, id, *args, **kwargs):
        print(models.Data.objects.all()[0].id)
        data = models.Data.objects.filter(id=id).first()
        entity = model_to_dict(data)
        entity['frame'] = entity['data']
        entity['meta'] = entity['meta_data']  # ['title']
        entity = preprocess_entities([entity])[0]
        result = get_one_figure_by_entity(entity)
        print(entity)
        # print(entity['page'])
        # print(entity['frame'].iloc[:10].to_html())
        # print(result)
        # print(data)
        # print()

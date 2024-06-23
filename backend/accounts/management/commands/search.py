from django.core.management.base import BaseCommand

from accounts.handlers import DataParser
from accounts.models import Data
import pickle
from analyst.settings import BASE_DIR, YANDEX_SEARCH_API_TOKEN

search_engine = None
try:
    search_engine = pickle.load(open(f'{BASE_DIR}/search.pkl', 'rb'))
except FileNotFoundError:
    print('No search.pkl file found')


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = search_engine.search('северсталь')
        ids = [id for id, rel in res]
        data_items = Data.objects.filter(id__in=ids).all()
        for data in data_items:
            print(data.data_type)
            print(data.data)

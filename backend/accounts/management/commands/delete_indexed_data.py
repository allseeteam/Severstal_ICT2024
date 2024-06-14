from django.core.management.base import BaseCommand

from accounts.handlers import DataParser
from accounts.models import Data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--id', default=None, type=int)
        parser.add_argument('--url', default=None, type=str)
        parser.add_argument('--delete_all', default=None, type=str)

    def handle(self, id, delete_all, url, *args, **options):
        if delete_all:
            Data.objects.all().delete()
            print('deleted all data')
        # elif url:
        #     o = Data.objects.filter(url=url).first()
        #     if o:
        #         print(f'deleting obj with url {o.url}')
        #         o.delete()
        #     else:
        #         print(f'no obj with id={id}')
        elif id:
            o = Data.objects.filter(id=id).first()
            if o:
                print(f'deleting obj with id {o.id}')
                o.delete()
            else:
                print(f'no obj with id={id}')

        # print(f'Already exists: {len(exists_pages)}')
        # DataParser.bulk_page_content_to_data(
        #     exists_pages
        # )

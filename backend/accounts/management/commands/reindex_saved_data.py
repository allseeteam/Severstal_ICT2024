from django.core.management.base import BaseCommand

from accounts.handlers import DataParser
from accounts.models import WebPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        exists_pages = WebPage.objects.all()

        print(f'Already exists: {len(exists_pages)}')
        DataParser.bulk_page_content_to_data(
            exists_pages
        )

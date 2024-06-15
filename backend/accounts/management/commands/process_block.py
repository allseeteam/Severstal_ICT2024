from django.forms import model_to_dict

from accounts import models
from search import ya_search
from extract.reports import get_one_figure_by_entity
from accounts.handlers import SiteParser
from analyst.settings import YANDEX_SEARCH_API_TOKEN
from accounts.tasks import process_block

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_block_id', type=int,
                            help='report block id')
        parser.add_argument('meta_block_id', type=int, help='meta block id')

    def handle(self, report_block_id: int, meta_block_id: int, *args, **options):
        process_block(report_block_id, meta_block_id)

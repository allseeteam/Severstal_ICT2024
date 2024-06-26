from django.core.management.base import BaseCommand, CommandError

from accounts.handlers import SiteParser
from .start_urls import START_URLS

class Command(BaseCommand):
    def handle(self, *args, **options):
        SiteParser().parse_sites(start_urls=START_URLS)

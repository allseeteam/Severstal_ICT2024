from django.core.management.base import BaseCommand

from accounts.handlers import FedStatParser
from .start_urls import START_URLS

class Command(BaseCommand):
    def handle(self, *args, **options):
        FedStatParser.parse()
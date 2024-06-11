from tqdm import tqdm
import pandas as pd

from django.core.management.base import BaseCommand

from accounts.handlers import DataParser
from accounts.models import WebPage

from bs4 import BeautifulSoup


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('input', type=str, help='Input csv')

    def handle(self, input, *args, **options):
        df = pd.read_csv(input)
        print(f"Total: {len(df)}")

        urls = df['url'].values.tolist()
        exists_pages = WebPage.objects.filter(url__in=urls)

        print(f'Already exists: {len(exists_pages)}')
        # DataParser.bulk_page_content_to_data(
        #     exists_pages
        # )

        exists_urls = set([page.url for page in exists_pages])
        not_exists_urls = set(urls).difference(exists_urls)
        df = df[df['url'].isin(not_exists_urls)]
        print(f'To index: {len(df)}')
        pages = []
        for i, row in tqdm(df.iterrows()):
            url = row.url
            content = row.content
            if 'title' in row:
                title = row.title
            else:
                soup = BeautifulSoup(content)
                title = ''
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.string
                if not title:
                    title = url

            update_date = row.update_date
            page = WebPage(
                title=title,
                url=url,
                content=content,
                update_date=update_date
            )
            page.save()
            pages.append(page)

        DataParser.bulk_page_content_to_data(
            pages
        )

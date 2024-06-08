from queue import Queue
import time
from typing import Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.utils import timezone
from langchain_community.document_loaders import AsyncChromiumLoader

from . import models


# sudo apt-get install libwoff1 libwebpdemux2 libenchant-2-2  libsecret-1-0  libhyphen0 libegl1 lib evdev2 libgles2 
# pip install -q langchain-openai langchain playwright beautifulsoup4
# playwright install

PARSER_TIMEOUT = 3

class DataParser:
    @classmethod
    def page_content_to_data(cls, content: str) -> models.Data:
        return
        return models.Data.objects.create(
            type=models.Data.WEB_PAGE,


        )

    @classmethod
    def pdf_to_data(cls, content: str) -> models.Data:
        return
        return models.Data.objects.create(
            type=models.Data.FILE,
            

        )

    @classmethod
    def video_to_data(cls, content: str) -> models.Data:
        return
        return models.Data.objects.create(
            type=models.Data.VIDEO,
            

        )

class SiteParser:
    def __init__(self, start_urls: List[str]) -> None:
        self.queues: Dict[Queue] = {}
        for url in start_urls:
            self.add_url_to_queue(url)

    def add_url_to_queue(self, url):
        site = self.get_url_site(url)
        if not self.queues.get(site):
            queue = Queue()
            queue.put(url)
            site = self.get_url_site(url)
            self.queues[site] = queue
        else:
            self.queues[site].put(url)

    def parse(self):
        while True:
            time.sleep(PARSER_TIMEOUT)
            urls: List[str] = [
                queue.get()
                for queue in self.queues.values()
                if not queue.empty()
            ]

            if len(urls) == 0:
                return
            
            urls_content = AsyncChromiumLoader(urls).load()

            now = timezone.now()
            web_pages: List[models.WebPage] = []
            for url, content in zip(urls, urls_content):
                if content.page_content.startswith('Error:'):
                    continue
                web_pages.append(
                    models.WebPage(
                        url=url,
                        content=content.page_content,
                        update_date=now
                    )
                )

            # Пока механизм обновления уже скаченных не предусмотрен
            web_pages = models.WebPage.objects.bulk_create(
                objs=web_pages, batch_size=700, ignore_conflicts=True
            )

            # Тут надо запускать преобразование в Data
            for page in web_pages:
                print(f'Скачана ссылка: {page.url}')

                DataParser.page_content_to_data(content=page.content)

                urls = self.extract_urls_from_page(page)
                existing_urls = models.WebPage.objects.filter(
                    url__in=urls
                ).values_list('url', flat=True)
    
                [
                    self.add_url_to_queue(url)
                    for url in urls
                    if url not in existing_urls
                ]


    def extract_urls_from_page(self, page: models.WebPage):
        site = self.get_url_site(page.url)
        soup = BeautifulSoup(page.content)
        urls = set()
        for a in soup.find_all('a'):
            href = a.attrs.get('href')
            if href:
                if href.startswith(site):
                    return href
                elif not href.startswith(
                    ('http', 'tel:', '/tel:', '/#', '#', 'mailto:', '/mailto:')
                ):
                    if href[0] == '/':
                        urls.add(f'{site}{href[1:]}')
                    elif href[0] != '.':
                        urls.add(f'{site}{href}')
        return urls
    
    def get_url_site(self, url: str) -> str:
        parsed_url = urlparse(url)
        return f'{parsed_url.scheme}://{parsed_url.netloc}/'


class AccountHandler:
    def update_data_from_search(self, search_query: models.SearchQuery):
        """
        Метод для парсинга и сохранения в бд всей информации
        по аналитическому отчету
        """
        search_urls = self.get_search_urls(search_query)

        search_web_pages = models.WebPage.objects.bulk_create(
            objs=[
                models.WebPage(
                    url=url,
                )
                for url in search_urls
            ],
            ignore_conflicts=True # пока обновление информации не предусмотрено.
        )

        urls = [page.url for page in search_web_pages]
        
        urls_content = AsyncChromiumLoader(urls).load()
        for page, content in zip(search_web_pages, urls_content):
            page.content = content.page_content

        models.WebPage.objects.bulk_update(
            objs=search_web_pages, fields=('content',)
        )


    def get_search_urls(self, search_query: models.SearchQuery) -> List[str]:
        """
        Метод для получения ссылок из Yandex Search Api на основании 
        запроса пользователя.
        """
        return [
            'https://www.metalinfo.ru/ru/magazine/rate/2023/2023_1',
            'https://gostmetal.ru/dinamika/',
            'https://dzen.ru/a/ZYf-4u3htX0pnGwC'
        ]


account_handler = AccountHandler()

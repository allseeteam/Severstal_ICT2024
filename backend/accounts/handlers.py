from queue import Queue
import time
from typing import Dict, List, Tuple
from urllib.parse import urlparse
from datetime import datetime
import uuid

from bs4 import BeautifulSoup
from django.utils import timezone
from search.yagpt import make_prompt_by_html, ask_yagpt
from langchain_community.document_loaders import AsyncChromiumLoader
import requests

from analyst.settings import BASE_DIR, YANDEX_SEARCH_API_TOKEN

from extract.utils import get_entity_id
from extract import prepare_entities, is_valid_entity, preprocess_entities, htmlify_df, prepare_pdf_entities
from extract.pdf import get_tables_from_raw_pdf
from search import video_inference
from tqdm import tqdm

from . import models


# sudo apt-get install libwoff1 libwebpdemux2 libenchant-2-2  libsecret-1-0  libhyphen0 libegl1 lib evdev2 libgles2
# pip install -q langchain-openai langchain playwright beautifulsoup4
# playwright install

PARSER_TIMEOUT = 5


class FedStatParser:
    DOMAIN = 'https://www.fedstat.ru'

    @classmethod
    def parse(cls):
        main_page = requests.get(f'{cls.DOMAIN}/opendata')
        soup = BeautifulSoup(main_page.content, 'html.parser')

        data_pasport_links = soup.find_all(attrs={'class': 'lnk lnk_txt'})
        for link in data_pasport_links:
            try:
                url = link.attrs.get('href')
                data_id = url.split('/')[2]
                data_passport = requests.get(f'{cls.DOMAIN}{url}')
                soup = BeautifulSoup(data_passport.content)
                for a in soup.find_all('a'):
                    url: str = a.attrs.get('href')
                    if url.startswith(f'{data_id}/data'):
                        print(url)
                        with open(f'{BASE_DIR.parent}/data/{data_id}.xml', 'wb') as f:
                            f.write(requests.get(
                                f'{cls.DOMAIN}/opendata/{url}').content)
                    if url.startswith(f'{data_id}/structure'):
                        print(url)
                        with open(f'{BASE_DIR.parent}/data/structure-{data_id}.xsd', 'wb') as f:
                            f.write(requests.get(
                                f'{cls.DOMAIN}/opendata/{url}').content)
            except Exception as e:
                print(e)


class DataParser:
    @classmethod
    def summarize_video(cls, query, model_id='yandexgpt'):
        try:
            video_result = video_inference(
                query, YANDEX_SEARCH_API_TOKEN, model_id)
        except Exception as e:
            print(f'Ошибка в поиске по видео: {e}')
            return
        if not video_result:
            return
        url = video_result['url']
        text = video_result['text']
        title = video_result['title']
        transcription = video_result['raw_transcription']
        video_page = models.WebPage.objects.filter(url=url).first()
        if not video_page:
            video_page = models.WebPage(
                url=url,
                title=title,
                content=transcription,
            )
            video_page.save()
        data = models.Data(
            index_id=f'{url}@{hash(text)}',
            type=models.Data.VIDEO,
            data_type=models.Data.TEXT,
            page=video_page,
            data=text,
            meta_data={},
            date=datetime.today(),
            version=0,
        )
        data.save()
        return data

    @classmethod
    def summarize_urls_from_search(cls, urls: list[str], model_id='yandexgpt'):
        data = None
        for url in urls:
            try:
                data_row = cls.summarize_url(url, model_id)
                if 'сменим тему' in data_row.data or len(data_row.data) < 50:
                    continue
                data = data_row
            except Exception:
                pass
        if not data:
            return
        data = [data]
        return data

    @classmethod
    def summarize_url(cls, url: str, model_id='yandexgpt'):
        page = models.WebPage.objects.filter(url=url).first()
        yagpt_response = ask_yagpt(make_prompt_by_html(
            page.content), YANDEX_SEARCH_API_TOKEN, model_id)
        data = models.Data(
            index_id=f'{url}@{hash(yagpt_response)}',
            type=models.Data.WEB_PAGE,
            data_type=models.Data.TEXT,
            page=page,
            data=yagpt_response,
            meta_data={},
            date=datetime.today(),
            version=0,
        )
        data.save()
        return data

    @classmethod
    def page_content_to_data(cls, page: models.WebPage, save: bool = True) -> List[models.Data]:
        # try:
        entities = prepare_entities(page.content, page.url)
        objs = []
        try:
            entities = prepare_entities(
                page.content, page.url, return_dicts=False)
            entities = preprocess_entities(entities)
            print(f'len of entities before filter {len(entities)}')
            entities = list(
                filter(lambda entity: is_valid_entity(entity), entities))
            print(f'len of entities after filter {len(entities)}')
        except TypeError:
            return []
        for entity in entities:
            objs.append(
                models.Data(
                    index_id=get_entity_id(entity),
                    type=models.Data.WEB_PAGE,
                    data_type=models.Data.PLOTLY,
                    page=page,
                    data=htmlify_df(entity['frame']),
                    meta_data=entity['meta'],
                    date=datetime.today(),
                    version=0,
                )
            )

        if save:
            return models.Data.objects.bulk_create(objs=objs, ignore_conflicts=True)
        return objs
        # except:
        #     return []

    @classmethod
    def bulk_page_content_to_data(cls, pages: list[models.WebPage]) -> list[models.Data]:
        objs = []
        print(f'To index {len(pages)} pages')
        for page in tqdm(pages):
            objs += cls.page_content_to_data(page=page, save=False)

        print(f'Saving {len(objs)} objects')
        return models.Data.objects.bulk_create(objs=objs, ignore_conflicts=True, batch_size=700)

    @classmethod
    def pdf_to_data(cls, file: models.Files, path: str) -> List[models.Data]:
        entities = get_tables_from_raw_pdf(path)
        try:
            entities = prepare_pdf_entities(entities, return_dicts=False)
            entities = preprocess_entities(entities)
            entities = list(
                filter(lambda entity: is_valid_entity(entity), entities))
        except TypeError:
            return []
        objs = []
        for entity in entities:
            objs.append(
                models.Data(
                    index_id=get_entity_id(entity),
                    type=models.Data.FILE,
                    data_type=models.Data.PLOTLY,
                    file=file,
                    data=htmlify_df(entity['frame']),
                    meta_data=entity['meta'],
                    date=datetime.today(),
                    version=0,
                )
            )
        return models.Data.objects.bulk_create(objs=objs, ignore_conflicts=True, batch_size=700)

    @classmethod
    def video_to_data(cls, content: str) -> List[models.Data]:
        pass


class SiteParser:
    FILE_FORMATS = (
        '.pdf',
        '.xlsx',
        '.xls',
        '.zip',
        '.rar',
        '.gz',
        '.gzip',
        '.doc',
        '.docx'
    )

    def add_url_to_queue(self, url):
        site = self.get_url_site(url)
        if not self.queues.get(site):
            queue = Queue()
            queue.put(url)
            site = self.get_url_site(url)
            self.queues[site] = queue
        else:
            self.queues[site].put(url)

    def parse_pages(
        self, urls: List[str],
        parse_page_urls: bool = False,
        download_files: bool = False,
    ) -> List[models.Data]:
        data: List[models.Data] = []
        print(urls)

        urls_to_files: List[str] = [
            url
            for url in urls
            if url.endswith(self.FILE_FORMATS)
        ]

        urls: List[str] = [
            url
            for url in urls
            if not url.endswith(self.FILE_FORMATS)
        ]

        if len(urls) == 0 and len(urls_to_files) == 0:
            return

        now = timezone.now()
        web_pages: List[models.WebPage] = []

        if download_files:
            for url in urls_to_files:
                try:
                    filename = url.split('/')[-1]
                    print(f'Файл: {filename}')
                    # Может дублироваться, но если сразу сохранять информациюв бд и не сохранять файл, то не страшно
                    with open(f'{BASE_DIR.parent}/data/{filename}', 'wb') as f:
                        f.write(requests.get(url).content)
                    print(f'Скачан файл{filename}')
                    page = models.WebPage(
                        url=url,
                        # content=content.page_content,
                        update_date=now
                    )
                    page.save()
                    web_pages.append(
                        page
                    )
                except Exception as e:
                    print(f'Ошибка при сохранении {e}')
                    continue

        urls_content = AsyncChromiumLoader(urls).load()
        for url, content in zip(urls, urls_content):
            print(url)
            if content.page_content.startswith('Error:'):
                print('Error')
                continue

            # исключаем страницы без ссылок, потому что
            # большая вероятность, что сработала защита от парсинга
            # или ddos.
            title, urls = self.extract_urls_and_title_from_url_and_content(
                url, content.page_content
            )
            if len(urls) == 0:
                continue

            print(f'Скачана ссылка: {url}')

            existing_urls = models.WebPage.objects.filter(
                url__in=urls
            ).values_list('url', flat=True)

            if parse_page_urls:
                [
                    self.add_url_to_queue(url)
                    for url in urls
                    if url not in existing_urls
                ]

            if not models.WebPage.objects.filter(
                url=url
            ).exists():
                page = models.WebPage.objects.create(
                    title=title,
                    url=url,
                    content=content.page_content,
                    update_date=now
                )

                data += DataParser.page_content_to_data(
                    page
                )
            else:
                data += list(models.WebPage.objects.get(url=url).data.all())

        # Пока механизм обновления уже скаченных не предусмотрен
        models.WebPage.objects.bulk_create(
            objs=web_pages, batch_size=700, ignore_conflicts=True
        )

        models.Data.objects.bulk_create(
            objs=data, batch_size=700, ignore_conflicts=True
        )

        return data

    def parse_sites(self, start_urls: List[str]):
        self.queues: Dict[Queue] = {}
        for url in start_urls:
            self.add_url_to_queue(url)

        while True:
            time.sleep(PARSER_TIMEOUT)

            urls: List[str] = [
                queue.get()
                for queue in self.queues.values()
                if not queue.empty()
            ]

            if len(urls) == 0:
                break

            self.parse_pages(urls=urls, parse_page_urls=True)

    def extract_urls_and_title_from_url_and_content(
        self, url: str, content: str
    ) -> Tuple[str, List[str]]:
        site = self.get_url_site(url)
        soup = BeautifulSoup(content, 'html.parser')
        title = ''
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.string

        urls = set()
        for a in soup.find_all('a'):
            href = a.attrs.get('href')
            if href:
                if href.startswith(site):
                    urls.add(href)
                elif not href.startswith(
                    ('http', 'tel:', '/tel:', '/#', '#', 'mailto:', '/mailto:')
                ):
                    if href[0] == '/':
                        urls.add(f'{site}{href[1:]}')
                    elif href[0] != '.':
                        urls.add(f'{site}{href}')
        return title, urls

    def get_url_site(self, url: str) -> str:
        parsed_url = urlparse(url)
        return f'{parsed_url.scheme}://{parsed_url.netloc}/'

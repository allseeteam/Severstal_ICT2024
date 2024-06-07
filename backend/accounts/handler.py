import asyncio
from typing import List

import aiohttp
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_core.documents import Document


from . import models
from common import async_db


# sudo apt-get install libwoff1 libwebpdemux2 libenchant-2-2  libsecret-1-0  libhyphen0 libegl1 lib evdev2 libgles2 
# pip install -q langchain-openai langchain playwright beautifulsoup4
# playwright install


class CustomAsyncChromiumLoader(AsyncChromiumLoader):
    async def load(self) -> List[Document]:
        """
        Load and return all Documents from the provided URLs.

        Returns:
            List[Document]: A list of Document objects
            containing the scraped content from each URL.

        """
        return [doc async for doc in self.alazy_load()]


class AccountHandler:
    async def parse_account_data(self, account: models.Account):
        """
        Метод для парсинга и сохранения в бд всей информации
        по аналитическому отчету
        """
        search_urls = await self.get_search_urls(account)

        search_web_pages = await models.WebPage.objects.abulk_create(
            objs=[
                models.WebPage(
                    url=url,
                )
                for url in search_urls
            ]
        )

        await account.pages.aadd(*search_web_pages)

        pages = [page async for page in account.pages.all()]
        urls = [page.url for page in pages]
        
        urls_content = await CustomAsyncChromiumLoader(urls).load()
        for page, content in zip(pages, urls_content):
            page.content = content.page_content

        await models.WebPage.objects.abulk_update(
            objs=pages, fields=('content',)
        )



        # async for page in account.pages.all():
        #     await self.parse_web_page(page)



    async def get_search_urls(self, account: models.Account) -> List[str]:
        return [
            'https://www.metalinfo.ru/ru/magazine/rate/2023/2023_1',
            'https://gostmetal.ru/dinamika/',
            'https://dzen.ru/a/ZYf-4u3htX0pnGwC'
        ]
        pass

    async def parse_web_page(self, web_page: models.WebPage):
        async with aiohttp.ClientSession() as session:
            async with session.get(web_page.url) as response:
                if response.status != 200:
                    return
                
                response_text = await response.text()
                web_page.content = response_text
                
                await web_page.asave()



account_handler = AccountHandler()

# asyncio.run(account_handler.parse_account_data(account))
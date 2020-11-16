# -*- encoding:utf-8 -*-
'''
苦瓜网盘
url:https://kgbook.com/
'''
import aiohttp
from yarl import URL
from bs4 import BeautifulSoup
import re
import asyncio


class kgBook:


    def __init__(self):
        self.domain = 'https://kgbook.com'
        self.search_url = f'{self.domain}/e/search/index.php'
        self.session = None
        self.search_dict_list = []

    def get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_result_page_by_keyword(self, keyword):
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {
            "keyboard": keyword,
            "show": "title,booksay,bookwriter",
            "tbname": "download",
            "tempid": 1,
            "submit": "搜索"
        }
        try:
            session = self.get_session()
            async with session.post(self.search_url, data=payload) as resp:
                if resp.url == URL(self.domain):
                    return None
                content = await resp.text()
                return self.get_detail_page_by_content(content)
        except Exception as e:
            print(f'get_result_page_by_keyword:{e}')
            return []


    def get_detail_page_by_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        span_list = soup.find_all('span', class_='url')
        a_list = [span.find('a') for span in span_list]
        return [a.attrs['href'] for a in a_list if a.attrs['href'] is not None]

    async def get_download_url_by_detail_url(self, page_url):
        try:
            session = self.get_session()
            async with session.get(page_url) as resp:
                content = await resp.text()
                return await self.get_download_url_by_content(content)
        except Exception as e:
            print(f'get_download_url_by_detail_url:{e}')
            return {}


    async def get_download_url_by_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('h1', class_='news_title')
        a = soup.find(href=re.compile('GetDown'), class_='button')
        session = self.get_session()
        try:
            async with session.get(a.attrs['href'].strip()) as resp:
                if resp.url != URL(a.attrs['href'].strip()):
                    real_url = str(resp.url)
                    ext = real_url.split(".")[-1]
                    download_dict = {
                            f'{title.text}.{ext}':{
                                "download":str(resp.url),
                                "size":"未知",
                                "speed":"很快"
                            }
                        }
                self.search_dict_list.append(download_dict)                
        except Exception as e:
            print(f'get_download_url_by_detail_url:{e}')
            return {}        


    async def search(self, keyword):
        detail_url_list = await self.get_result_page_by_keyword(keyword)
        tasks = [asyncio.ensure_future(self.get_download_url_by_detail_url(
            url)) for url in detail_url_list]
        return await asyncio.gather(*tasks)
    
    async def close_session(self):
        if self.session:
            await self.session.close()        


if __name__ == '__main__':
    book = kgBook()
    loop = asyncio.new_event_loop()
    tasks = book.search('三体')
    results = loop.run_until_complete(tasks)
    loop.close()

    loop = asyncio.new_event_loop()
    tasks = book.close_session()
    results = loop.run_until_complete(tasks)
    loop.close()

    print(book.search_dict_list)

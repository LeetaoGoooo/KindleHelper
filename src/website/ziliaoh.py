
# -*- encoding:utf-8 -*-
'''
图书网
url:http://www.ziliaoh.com/mobi.html
'''

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import os
from cryptography.fernet import Fernet
import ast
from common import store_path


class ziliaoH:

    def __init__(self):
        self.domain = 'http://www.ziliaoh.com/mobi.html'
        self.timeout = aiohttp.ClientTimeout(total=600)
        self.search_dict = {}
        os.makedirs(store_path, exist_ok=True)
        self.local_store = os.path.join(store_path, 'ziliaoH.db')

    async def get_book_url(self, url):
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as rep:
                    html = await rep.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    div = soup.find('div', class_='single-content')
                    p_list = div.find_all('p')
                    for p in p_list:
                        a = p.find('a')
                        if a:
                            self.search_dict[p.get_text(
                            ).strip()] = a.attrs['href']
        except Exception as e:
            print(f'获取异常，Exception:{e}')

    async def get_pan_url_by_url(self, book_name, url):
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as rep:
                    html = await rep.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    div = soup.find('div', class_='alert-url')
                    if div:
                        self.search_dict[book_name] = div.get_text().strip()
                    else:
                        del self.search_dict[book_name]
                        print(f'{book_name}--链接:{url}失效')
        except Exception as e:
            print(f'获取异常，Exception:{e}')

    async def prepare_search(self):
        url_list = [f'{self.domain}/{i}' for i in range(1, 11)]
        tasks = [self.get_book_url(url) for url in url_list]
        await asyncio.gather(*tasks)
        tasks = [self.get_pan_url_by_url(
            key, self.search_dict.get(key)) for key in self.search_dict]
        await asyncio.gather(*tasks)

        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open(self.local_store, 'w', encoding='utf-8') as f:
            txt = fernet.encrypt(str(self.search_dict).encode('utf-8'))
            f.writelines([str(key, encoding='utf-8'),
                          "\n", str(txt, encoding='utf-8')])

    async def search(self, keyword):
        search_results_list = []

        if not os.path.exists(self.local_store):
            await self.prepare_search()

        with open(self.local_store, 'r', encoding='utf-8') as f:
            key = f.readline()
            txt = f.readline()
            fernet = Fernet(bytes(key.strip(), encoding='utf-8'))
            bytes_txt = bytes(txt, encoding='utf-8')
            self.search_dict = ast.literal_eval(
                str(fernet.decrypt(bytes_txt), encoding='utf-8'))
            keys = self.search_dict.keys()
            match_key = [key for key in keys if keyword in key]
            for key in match_key:
                search_results_dict = {}
                search_results_dict[key] = {}
                search_results_dict[key]["百度网盘"] = self.search_dict[key]
                search_results_list.append(search_results_dict)
        return search_results_list


if __name__ == "__main__":
    book = ziliaoH()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(book.prepare_search())
    loop.close()
    print(book.search_dict)

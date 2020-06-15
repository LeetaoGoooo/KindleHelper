# -*- encoding:utf-8 -*-
'''
云海免费电子图书馆
url:http://www.pdfbook.cn/
'''

import aiohttp
from bs4 import BeautifulSoup
import asyncio
import time
import random
import json


class PdfHome:

    def __init__(self):
        self.search_url = 'http://www.pdfbook.cn/'
        self.file_info_url = 'https://webapi.400gb.com/getfile.php'
        self.file_download_url = 'https://webapi.400gb.com/get_file_url.php'
        self.file_url_list = [] # 城通网盘
        self.file_direct_url_list = [] # 其他
        self.keyword = None
        self.timeout = aiohttp.ClientTimeout(total=120)

    async def search(self, keyword):
        try:
            self.keyword = keyword
            book_url_list = await self.get_book_url_list(keyword)
            for book_url in book_url_list:
                await self.get_download_page_url_by_book_url(book_url)

            file_info_list = []
            for file_url in self.file_url_list:
                file_info_url_list = await self.get_file_info_by_url(file_url)
                if file_info_url_list:
                    file_info_list += file_info_url_list

            tasks = [self.get_download_url(uid,fid,file_chk,file_name,file_size,speed) for uid,fid,file_chk,file_name,file_size,speed in file_info_list]
            return await asyncio.gather(*tasks)
        except Exception as e:
            print(f'异常...{e}')
            return []

    def search_results(self, async_results):
        for index,value in enumerate(self.file_direct_url_list):
            async_results.append({
                f'{self.keyword}-{index}':{
                    "download":value,
                    "size":"未知",
                    "speed":"很快"
                }
            })
        return async_results

    async def get_download_page_url(self, keyword):
        book_url_list = await self.get_book_url_list(keyword)
        tasks = [asyncio.ensure_future(self.get_download_page_url_by_book_url(book_url)) for book_url in book_url_list]
        return await asyncio.gather(*tasks)     
    
    async def get_download_file_url(self, file_url_list):
        tasks = [asyncio.ensure_future(self.get_file_info_by_url(file_url)) for file_url in file_url_list]
        return await asyncio.gather(*tasks)

    async def get_download_url_dict(self, file_info_list):
        tasks = [self.get_download_url(uid,fid,file_chk,file_name,file_size,speed) for uid,fid,file_chk,file_name,file_size,speed in file_info_list]
        return await asyncio.gather(*tasks)          

    async def get_book_url_list(self, keyword):
        data = {
            "s": keyword
        }
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(self.search_url,data=data) as rep:
                content = await rep.text()
                return await self.get_book_page_by_content(content)

    async def get_book_page_by_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        a_list = soup.find_all('a', class_='out')
        book_url_list = [a.attrs["href"] for a in a_list]
        return book_url_list

    async def get_download_page_url_by_book_url(self, url):
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as rep:
                    html = await rep.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    a_list = soup.select('span > a')
                    url_list = set([a.attrs['href'] for a in a_list if not a.attrs['href'].startswith("http://7xpqk5.com1.z0.glb.clouddn.com/")])
                    for url in url_list:
                        if url.startswith('https://n459.com/'):
                            self.file_url_list.append(url)
                        else:
                            self.file_direct_url_list.append(url)
        except Exception as e:
            print(f'获取异常，Exception:{e}')


    async def get_file_info_by_url(self, url):
        uid_fid = url.strip().split("/")[-1]
        file_info_url = f'{self.file_info_url}?f={uid_fid}&passcode=&ref={url}'
        async with aiohttp.ClientSession(timeout=self.timeout) as session:            
            async with session.get(file_info_url, headers={"Accept":"application/json","Origin":"http://kankan.yyupload.com","Referer":f'http://kankan.yyupload.com/file/{uid_fid}'}) as rep:
                if rep.status == 200:
                    file_info_text = await rep.text()
                    try:
                        file_info_json = json.loads(file_info_text)
                    except Exception as e:
                        print(f'获取下载文件信息异常,返回信息:{file_info_text}')
                        return []
                    if file_info_json['code'] == 200:
                        uid, fid, file_chk, file_name, file_size,speed = file_info_json['userid'], file_info_json[
                            'file_id'], file_info_json['file_chk'], file_info_json['file_name'], file_info_json['file_size'], file_info_json['free_speed']
                        return [(uid,fid, file_chk, file_name, file_size,speed)]
                else:
                    print(f'请求异常，状态码:{rep.status}')


    async def get_download_url(self, uid, fid, file_chk, file_name, file_size, file_speed):
        params = [("uid", uid), ("fid", fid), ("folder_id", 0), ("file_chk", file_chk),
                  ("mb", 0), ("app", 0), ("acheck", 1), ("verifycode", ''), ("rd", str(random.random()))]
        async with aiohttp.ClientSession(timeout=self.timeout) as session:            
            async with session.get(self.file_download_url, params=params) as rep:
                rep_text = await rep.text()
                rep_json = json.loads(rep_text)
                if rep_json['code'] == 200:
                    url = rep_json['downurl']
                    return {
                        file_name:{
                            "download":url,
                            "size": file_size,
                            "speed": file_speed
                        }
                    }

if __name__ == '__main__':
    kankan = PdfHome()
    # loop = asyncio.get_event_loop()
    # begin = time.time()
    # tasks = kankan.search('三体')
    # results = loop.run_until_complete(tasks)
    # end = time.time()
    # print(f'{end-begin} s 检索到 {len(results)}')

    # 
    file_info_list = []
    loop = asyncio.new_event_loop()
    begin = time.time()
    tasks = kankan.get_download_page_url('与孩子一起学编程')
    results = loop.run_until_complete(tasks)
    loop.close()

    loop = asyncio.new_event_loop()
    tasks = kankan.get_download_file_url(kankan.file_url_list)
    results = loop.run_until_complete(tasks)

    for result in results:
        if result:
            file_info_list += result
    loop.close()

    loop = asyncio.new_event_loop()
    tasks = kankan.get_download_url_dict(file_info_list)
    results = loop.run_until_complete(tasks)
    end = time.time()
    loop.close()
    print(results)
    print(f'{end-begin} s 检索到 {len(results)}')
    print(f'{kankan.file_direct_url_list}')
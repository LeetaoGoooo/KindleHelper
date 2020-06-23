# -*- encoding:utf-8 -*-

'''
异步断点续传工具
'''
import requests
import asyncio
import os
import aiohttp
from tools.fake_user_agent import useragent_random
import requests
import time
from contextlib import closing
import hashlib
from common import root_path

root = root_path



class Download:
    def __init__(self):
        self.file_size = 0
        self.down_nums = 4
        self.max_retry = 10
        self.download_dir = os.path.join(root,'downloads')
        self.check_dir()

    def set_down_nums(self, size):
        self.down_nums = size
    
    def check_dir(self):
        if not os.path.exists(self.download_dir):
            try:
                print(f'开始创建目录{self.download_dir}')
                os.makedirs(self.download_dir,exist_ok=True)
            except Exception as e:
                print(f'创建文件夹失败,失败原因:{e}')
                raise Exception(f'创建文件夹失败,失败原因:{e}')

    async def download_file(self, url, file_name, trigger=None):

        if not os.path.exists(file_name):
            with open(f'{file_name}', 'w', encoding='utf-8') as f:
                f.close()

        print(f'开始获取文件...')
        download_response = requests.head(url)
        self.file_size = int(download_response.headers['Content-Length'])
        print(f'当前文件大小:{self.file_size}')
        remainder = self.file_size % self.down_nums
        self.part_file_size = self.file_size // self.down_nums
        if remainder:
            self.down_nums += 1
        tasks = [asyncio.ensure_future(self.download_part(
            part_num, url, file_name)) for part_num in range(1, self.down_nums+1)]
        return await asyncio.gather(*tasks)
    
    def single_download(self, url, file_name, trigger=None):
        start_time = time.time()
        with closing(requests.get(url,stream=True)) as response:
            chunk_size = 50
            content_size = int(response.headers['content-length'])
            print(f'start....content_size:{content_size}')
            data_count = 0
            with open(f'{self.download_dir}/{file_name}','wb') as f:
                print(f'begin write...')
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    data_count = data_count + len(data)
                    now_progress = (data_count/content_size)*100
                    speed = data_count / 1024 / (time.time()-start_time)
                    if not trigger: 
                        print(f'\r 文件下载进度:{int(now_progress)}% 文件下载速度:{int(speed)} kb/s')
                    else:
                        trigger.emit({"progress":int(now_progress),"speed":int(speed),"id":hashlib.md5(url.encode('utf-8')).hexdigest()})
        print('end...')
        return True

    async def download_part(self, part_num, url, file_name):
        print(f'{part_num} 开始下载文件...')
        start_pos = (part_num-1)*self.part_file_size
        end_pos = part_num * self.part_file_size

        if start_pos:
            start_pos += 1

        if end_pos > self.file_size:
            end_pos = self.file_size

        print(f'文件下载范围:{start_pos}-{end_pos}')
        headers = {"Range": "bytes=%s-%s" %
                   (start_pos, end_pos), "User-Agent": useragent_random()}
        async with aiohttp.ClientSession() as session:
            retry = self.max_retry
            content = await self.fetch(session, url, headers)
            while not content and retry:
                retry -= 1
                content = await self.fetch(session, url, headers)
            if not content:
                raise Exception('文件下载失败,请重新下载，或者换个连接!')
            await self.write_to_file(file_name, start_pos, content)
            print(f'{part_num}写入完成!')

    async def fetch(self, session, url, headers):
        async with session.get(url, headers=headers) as rep:
            if rep.status == 206:
                return await rep.read()
            else:
                return False

    async def write_to_file(self, file_name, start_pos, content):
        with open(f'{self.download_dir}/{file_name}', 'rb+') as f:
            f.seek(start_pos)
            f.write(content)

    def cancle(self):
        pass

    def recover(self):
        pass


if __name__ == '__main__':
    download = Download()
    url = 'http://file.lanjuhua.com/file/8975458ea18d6ffdf880f5af12400c3d/%E4%B8%89%E4%BD%93%E5%85%A8%E9%9B%86.mobi?ctt=1570247893&ctk=2iY-Y91eL6WiAugOz5xH4w&chk=6d183fe5c15557fc811e5a1e782203e1-3170213'
    download.single_download(url,'三体.mobi')
    # loop = asyncio.get_event_loop()
    # tasks = download.download_file(url, "三体.mobi")
    # results = loop.run_until_complete(tasks)

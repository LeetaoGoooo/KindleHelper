# -*- encoding:utf-8 -*-

'''
蓝菊花搜索引擎
'''
import requests
import time
from bs4 import BeautifulSoup
import re
import threading

from exceptions import NecessaryElementNotFoundException, NetWorkException


class LanJuHua:

    def __init__(self):
        self.domain_url = 'http://www.lanjuhua.com/'
        self.search_url = 'http://www.lanjuhua.com/do.php'
        self.ajax_url = 'http://www.lanjuhua.com/iajax.php'
        self.detail_url = 'http://www.lanjuhua.com/get_file_info.php'
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
        self.session.headers.update({'Connection':'Keep-Alive'})
        self.form_id = '206459435515'
        self.load_cookies()
        self.download_url = []
        self.search_results_list = []
        self.search_json = []

    @staticmethod
    def sort_by_speed(item):
        key = list(item.keys())[0]
        download_item = item.get(key)
        if download_item['speed'].endswith('秒'):
            return int(download_item['speed'][:-2].strip())
        elif download_item['speed'].endswith('分钟'):
            return int(download_item['speed'][:-2].strip())*60
        else:
            return int(download_item['speed'][:-2].strip())*3600

    def get_form_id(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        input_ele = soup.find(name="input", attrs={"name": "id"})
        if not input_ele:
            raise NecessaryElementNotFoundException("form id input")
        self.form_id = input_ele.attrs['value']

    def load_cookies(self):
        index_response = self.session.get(self.domain_url)
        if index_response.status_code != 200:
            NetWorkException(
                'load_cookies', index_response.status_code, index_response.text)
        self.get_form_id(index_response.text)

    def search(self, keyword):
        k, keword_id = self.get_encoded_k_and_id(keyword)
        total_pages = self.get_total_page(k, keword_id)

        search_threads = []

        for page_num in range(total_pages):
            t = threading.Thread(target=self.get_search_json,
                                 args=(k, keword_id, page_num))
            t.start()
            search_threads.append(t)

        for thread in search_threads:
            thread.join()

        validate_threads = []
        for search_json_item in self.search_json:
            t = threading.Thread(target=self.validate_url,
                                 args=(search_json_item, keword_id))
            t.start()
            validate_threads.append(t)

        for thread in validate_threads:
            thread.join()
        return sorted(self.search_results_list, key=lambda item: LanJuHua.sort_by_speed(item))

    def get_fs_id(self, ele_html):
        match_group = re.search(r'/fs/(.+)?">(.+)?<\/a>', ele_html)
        if match_group:
            return match_group.group(1), match_group.group(2)
        return None, None

    def get_total_page(self, k, book_id):
        payload = {
            "item": "search",
            "action": "search_file_list",
            "k": k,
            "id": book_id,
            "sEcho": 1,
            "iColumns": 2,
            "sColumns": "",
            "iDisplayStart": 0,
            "iDisplayLength": 25,
            "mDataProp_0": 0,
            "mDataProp_1": 1,
            "_": int(time.time())
        }
        search_response = self.session.get(self.ajax_url, params=payload)
        if search_response.status_code == 200:
            search_response_json = search_response.json()
            total_pages = min(int(search_response_json['iTotalRecords']), int(
                search_response_json['iTotalDisplayRecords']))//25
            return total_pages if total_pages else 1
        raise Exception(f'获取搜索结果异常!')

    def get_search_json(self, k, book_id,  page_num=1):
        payload = {
            "item": "search",
            "action": "search_file_list",
            "k": k,
            "id": book_id,
            "sEcho": page_num,
            "iColumns": 2,
            "sColumns": "",
            "iDisplayStart": (page_num-1)*25,
            "iDisplayLength": 25,
            "mDataProp_0": 0,
            "mDataProp_1": 1,
            "_": int(time.time())
        }
        search_response = self.session.get(self.ajax_url, params=payload)
        if search_response.status_code == 200:
            try:
                search_response_json = search_response.json()
                self.search_json += search_response_json['aaData']
            except Exception as e:
                print(f'返回结果:{search_response}')

    def get_encoded_k_and_id(self, book_name):
        url = f'{self.search_url}'
        form_data = {
            "id": self.form_id,
            "k": book_name
        }
        search_response = self.session.post(url, data=form_data)
        if search_response.status_code in [302, 200]:
            url_split_list = search_response.url.split("/")
            k, book_id = url_split_list[4], url_split_list[-1]
            return k, book_id
        raise NetWorkException(
            'search_book', search_response.status_code, search_response.text)

    def validate_url(self, search_item, keyword_id):
        fs_id, source_name = self.get_fs_id(search_item[0])
        if not fs_id and not source_name:
            return
        payload = {
            "id": keyword_id,
            "fid": fs_id
        }
        index_response = self.session.get(self.detail_url, params=payload)
        if index_response.status_code == 200:
            index_response_json = index_response.json()
            # 移除 vip 下载资源
            if index_response_json.get("code") == 200 and index_response_json['downurl'].strip():
                if index_response_json['downurl'] not in self.download_url:
                    self.download_url.append(index_response_json['downurl'])
                    self.search_results_list.append({source_name: {"download": index_response_json['downurl'], "size": search_item[1], "speed": index_response_json['free_speed']}})

# -*- encoding:utf-8 -*-
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import asyncio
import traceback

from website import LanJuHua, PdfHome, ziliaoH, kgBook


class SearchWorker(QThread):
    trigger = pyqtSignal(dict)

    def __init__(self, keyword):
        super(SearchWorker, self).__init__()
        self.lanjuhua = LanJuHua()
        self.ziliaoh = ziliaoH()
        self.pdfHome = PdfHome()
        self.kg = kgBook()
        self.keyword = keyword

    def pdfHome_search(self):
        loop = asyncio.new_event_loop()
        tasks = self.pdfHome.get_download_page_url(self.keyword)
        results = loop.run_until_complete(tasks)
        loop.close()

        loop = asyncio.new_event_loop()
        file_info_list = []
        tasks = self.pdfHome.get_download_file_url(self.pdfHome.file_url_list)
        results = loop.run_until_complete(tasks)
        results = [result for result in results if bool(result)]
        for result in results:
            if result:
                file_info_list += result
        loop.close()

        loop = asyncio.new_event_loop()
        tasks = self.pdfHome.get_download_url_dict(file_info_list)
        results = loop.run_until_complete(tasks)
        loop.close()

        return results

    def lanjuhua_search(self):
        return self.lanjuhua.search(self.keyword)

    def ziliaoh_search(self):
        loop = asyncio.new_event_loop()
        tasks = self.ziliaoh.search(self.keyword)
        results = loop.run_until_complete(tasks)
        loop.close()
        return results
    
    def kg_search(self):
        loop = asyncio.new_event_loop()
        tasks = self.kg.search(self.keyword)
        results = loop.run_until_complete(tasks)
        loop.close()

        loop = asyncio.new_event_loop()
        tasks = self.kg.close_session()
        results = loop.run_until_complete(tasks)
        loop.close()

        return self.kg.search_dict_list        

    def run(self):
        net_download_dict_list = []
        direct_download_dict_list = []

        try:
            direct_download_dict_list += self.pdfHome_search()
        except Exception as e:
            print(f'pdfHome搜索异常')

        try:
            direct_download_dict_list += self.lanjuhua_search()
        except Exception as e:
            traceback.print_exc()
            print(f'蓝菊花搜索异常:{e}')

        try:
            direct_download_dict_list += self.kg_search()
        except Exception as e:
            traceback.print_exc()
            print(f'苦瓜搜索异常:{e}')

        try:
            net_download_dict_list = self.ziliaoh_search()
        except Exception as e:
            print(f'搜索异常:{e}')

        self.trigger.emit({"direct":direct_download_dict_list,"net":net_download_dict_list})

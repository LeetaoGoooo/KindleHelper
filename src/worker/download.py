from PyQt5.QtCore import Qt, QThread, pyqtSignal
from tools import Download
import asyncio


class DownloadWorker(QThread):
    trigger = pyqtSignal(list) # 推送下载结果
    download_trigger = pyqtSignal(dict) # 实时推送下载进度

    def __init__(self, download_dict):
        super(DownloadWorker, self).__init__()
        self.download = Download()
        self.download_dict = download_dict
        self.download_url = download_dict['url']
        self.file_name = download_dict['file_name']
        self.download_file_id = download_dict['id']

    def download_file(self):
        print(self.download_url)
        if self.download_url.find("lanjuhua"):
            return self.single_download()
        else:
            return self.muti_download()

    def single_download(self):
        try:
            if self.download.single_download(self.download_url, self.file_name, self.download_trigger):
                return [True, self.download_dict]
        except Exception as e:
            print(e)
        return [False, self.download_dict]

    def muti_download(self):
        try:
            loop = asyncio.new_event_loop()
            tasks = self.download.download_file(
                self.download_url, self.file_name, self.download_trigger)
            results = loop.run_until_complete(tasks)
        except Exception as e:
            print(e)
            return [False, self.download_dict]
        return [True, self.download_dict]

    def run(self):
        self.trigger.emit(self.download_file())

    def terminate(self):
        super(DownloadWorker, self).terminate()
        self.trigger.emit([None,None])


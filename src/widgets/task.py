
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal

import os
import re

class TaskPage(QWidget):
    new_task_trigger = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(TaskPage, self).__init__(parent)
        self.download_tasks_textEdit = QTextEdit(self)
        self.download_btn = QPushButton(self)
        self.init_ui()
        self.init_event()

    def init_ui(self):
        self.download_tasks_textEdit.setEnabled(True)
        self.download_tasks_textEdit.setGeometry(QRect(0, 40, 1011, 791))
        self.download_tasks_textEdit.setStyleSheet("QTextEdit{ border:none;}")
        self.download_tasks_textEdit.setObjectName("download_tasks_textEdit")
        self.download_tasks_textEdit.setPlaceholderText("添加多个链接的时，请确保每行只有一个链接")

        self.download_btn.setEnabled(False)
        self.download_btn.setGeometry(QRect(820, 840, 120, 26))
        self.download_btn.setMaximumSize(QSize(160, 30))
        self.download_btn.setSizeIncrement(QSize(15, 15))
        self.download_btn.setBaseSize(QSize(15, 15))
        self.download_btn.setAutoFillBackground(False)
        self.download_btn.setStyleSheet(
            "QPushButton#download_btn::enabled{background-color:rgb(49, 194, 124);color:white;}QPushButton#download_btn{background-color:#ddd;border-radius:4px 4px 0 0;}")
        self.download_btn.setIconSize(QSize(15, 15))
        self.download_btn.setCheckable(False)
        self.download_btn.setAutoDefault(False)
        self.download_btn.setDefault(False)
        self.download_btn.setFlat(False)
        self.download_btn.setObjectName("download_btn")
        self.download_btn.setText("立即下载")

    def init_event(self):
        self.download_tasks_textEdit.textChanged.connect(self.text_change)
        self.download_btn.clicked.connect(self.send_download_task)
    
    def text_change(self):
        download_urls = self.download_tasks_textEdit.toPlainText().strip()
        if download_urls and download_urls.startswith("http"):
            self.download_btn.setEnabled(True)
        else:
            self.download_btn.setEnabled(False)
    
    def send_download_task(self):
        download_urls = self.download_tasks_textEdit.toPlainText().strip()
        download_urls = download_urls.replace('\r',"").replace('\n',' ')
        download_urls = re.sub(' +',' ',download_urls)
        download_url_list = download_urls.split(" ")
        print(download_url_list)
    

class TaskDialog(QWidget):

    def __init__(self,download_url_list):
        super(TaskDialog).__init__()
        self.download_url_list = download_url_list

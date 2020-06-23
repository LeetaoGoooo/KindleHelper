from widgets import ProgressBar
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidgetItem, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QRect, Qt

import os
import json
import hashlib

from common import data_path,assets_path


class DownloadingPage(QWidget):
    def __init__(self, parent=None):
        super(DownloadingPage, self).__init__(parent)
        self.download_worker_dict = {}
        self.data_path = os.path.join(data_path, 'downloading.json')
        self.downloaing_list_widget = QListWidget(self)
        self.downloaing_list_widget.setStyleSheet("QListWidget{border:none;}")
        self.downloaing_list_widget.setSpacing(2)
        self.downloaing_list_widget.setGeometry(QRect(10, 20, 950, 800))
        self.init_ui()
    
    def check_download(self, downloading_dict):
        downloading_dict_list = self.load_downloading_dict_list()
        if not downloading_dict_list:
            return True
        for downloading_dict in downloading_dict_list:
            if downloading_dict['url'].find("lanjuhua"):
                return False


    def init_ui(self):
        downloading_dict_list = self.load_downloading_dict_list()
        if not downloading_dict_list:
            return
        for downloading_dict in downloading_dict_list:
            self.add_downloading_item_to_widget(downloading_dict)

    def add_downloading_item(self, downloading_dict, worker=None):
        self.download_worker_dict[downloading_dict['id']] = worker
        self.add_downloading_item_to_widget(downloading_dict)
        self.add_downloading_item_to_data(downloading_dict)


    def add_downloading_item_to_widget(self, downloading_dict):
        item = QListWidgetItem()
        item.setText(downloading_dict['id'])
        item.setSizeHint(QSize(608, 86))
        self.downloaing_list_widget.addItem(item)
        self.downloaing_list_widget.setItemWidget(
            item, self.create_downloading_item(downloading_dict))

    def add_downloading_item_to_data(self, downloading_dict):
        downloading_dict_list = self.load_downloading_dict_list()
        downloading_dict_list.append(downloading_dict)
        self.write_data(downloading_dict_list)


    def load_downloading_dict_list(self):
        if not os.path.exists(self.data_path):
            os.makedirs(data_path, exist_ok=True)
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            downloading_dict_list = json.load(f)
            return downloading_dict_list

    def create_downloading_item(self, downloading_dict):
        book_name = downloading_dict['file_name']
        item_widget = QWidget()
        item_widget.setObjectName(f'{downloading_dict["id"]}')
        hbox_layout = QHBoxLayout()

        item_label = QLabel()
        item_label.setPixmap(QPixmap(os.path.join(assets_path, 'book.png')))
        hbox_layout.addWidget(item_label)

        vlayout = QVBoxLayout()
        file_name_label = QLabel(book_name)
        download_progress = ProgressBar(
            minimum=0, maximum=100, textVisible=False, objectName=f'{downloading_dict["id"]}_progress_bar')
        style_sheet = f'''
            #{downloading_dict["id"]}_progress_bar {{
                min-height: 6px;
                max-height: 6px;
                border-radius: 6px;
            }}
            #{downloading_dict["id"]}_progress_bar::chunk {{
                border-radius: 6px;
                width:12px;
                background-color: #D20A0A;
            }}        
        '''
        download_progress.setStyleSheet(style_sheet)
        vlayout.addWidget(file_name_label)
        vlayout.addWidget(download_progress)

        h_in_v_item_layout = QHBoxLayout()
        h_in_v_item_layout.addWidget(
            QLabel(downloading_dict['size']), Qt.AlignLeft)

        percent_label = QLabel()
        percent_label.setObjectName(f'{downloading_dict["id"]}_percent')
        percent_label.setText(f'已经下载:0%')
        h_in_v_item_layout.addWidget(percent_label, Qt.AlignHCenter)

        speed_label = QLabel()
        speed_label.setObjectName(f'{downloading_dict["id"]}_speed')
        speed_label.setText("0 kb/s")
        h_in_v_item_layout.addWidget(speed_label, Qt.AlignRight)

        vlayout.addLayout(h_in_v_item_layout)
        hbox_layout.addLayout(vlayout)

        del_btn = QPushButton()
        del_btn.setIcon(QIcon(os.path.join(assets_path, 'delete.png')))
        del_btn.setStyleSheet("QPushButton{border:none}")
        del_btn.clicked.connect(
            lambda: self.remove_task(downloading_dict["id"]))
        hbox_layout.addWidget(del_btn)

        item_widget.setLayout(hbox_layout)
        item_widget_style_sheet = f'#{downloading_dict["id"]}{{background-color:rgb(241,231,230);color:rgb(210,10,10)}}'
        item_widget.setStyleSheet(item_widget_style_sheet)
        return item_widget

    def downloading_callback(self, downloading_dict):
        downloading_dict = list(downloading_dict)

    def remove_task(self, id):
        print(f'remove_task {id}...')
        self.remove_task_form_list_widget(id)
        self.remove_task_from_data(id)

    def remove_task_from_data(self, id):
        downloading_dict_list = self.load_downloading_dict_list()
        for downloading_dict in downloading_dict_list:
            if id in downloading_dict['id']:
                if id in self.download_worker_dict:
                    eval(str(self.download_worker_dict[id]()))
                downloading_dict_list.remove(downloading_dict)
        self.write_data(downloading_dict_list)

    def write_data(self, downloading_dict_list):
        with open(self.data_path, 'w') as f:
            json.dump(downloading_dict_list, f)

    def remove_task_form_list_widget(self, id):
        item = self.downloaing_list_widget.findItems(id, Qt.MatchExactly)[0]
        self.downloaing_list_widget.takeItem(
            self.downloaing_list_widget.row(item))

    def update_progress(self, progress_dict):
        percent_label = self.downloaing_list_widget.findChild(
            QLabel, f'{progress_dict["id"]}_percent')
        if percent_label:
            percent_label.setText(f'已经下载:{progress_dict["progress"]}%')

            speed_label = self.downloaing_list_widget.findChild(
                QLabel, f'{progress_dict["id"]}_speed')
            speed_label.setText(f'{progress_dict["speed"]} kb/s')

            progress_bar = self.downloaing_list_widget.findChild(
                ProgressBar, f'{progress_dict["id"]}_progress_bar')
            progress_bar.setValue(progress_dict["progress"])

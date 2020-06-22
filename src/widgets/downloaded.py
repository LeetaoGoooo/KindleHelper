from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidgetItem, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal

import os
import json
import hashlib
import copy
import time

from worker import SendWorker
from common import check_send_config, ConfigDialog

root = os.getcwd()
data = os.path.join(root, 'src', 'data')
assets = os.path.join(root, 'src', 'assets')


class DownloadedPage(QWidget):
    send_trigger = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(DownloadedPage, self).__init__(parent)
        self.data_path = os.path.join(data, 'downloaded.json')
        self.rm_file_check = True
        self.downloaded_list_widget = QListWidget(self)
        self.downloaded_list_widget.setStyleSheet("QListWidget{border:none;}")
        self.downloaded_list_widget.setSpacing(2)
        self.downloaded_list_widget.setGeometry(QRect(10, 20, 950, 800))
        self.init_ui()

    def init_ui(self):
        downloaded_dict_list = self.load_downloaded_dict_list()
        if not downloaded_dict_list:
            return
        for downloaded_dict in downloaded_dict_list:
            self.add_downloaded_item_to_widget(downloaded_dict)

    def add_downloaded_item(self, downloaded_dict):
        downloaded_dict['date'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.add_downloaded_item_to_widget(downloaded_dict)
        self.add_downloaded_item_to_data(downloaded_dict)

    def add_downloaded_item_to_widget(self, downloaded_dict):
        item = QListWidgetItem()
        item.setText(downloaded_dict['id'])
        item.setSizeHint(QSize(608, 86))
        self.downloaded_list_widget.addItem(item)
        self.downloaded_list_widget.setItemWidget(
            item, self.create_downloaded_item(downloaded_dict))

    def add_downloaded_item_to_data(self, downloaded_dict):
        downloaded_dict_list = self.load_downloaded_dict_list()
        downloaded_dict_list.append(downloaded_dict)
        self.write_data(downloaded_dict_list)

    def load_downloaded_dict_list(self):
        if not os.path.exists(self.data_path):
            os.makedirs(data, exist_ok=True)
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            downloaded_dict_list = json.load(f)
            return downloaded_dict_list

    def create_downloaded_item(self, downloaded_dict):
        book_name = downloaded_dict['file_name']
        item_widget = QWidget()
        item_widget.setObjectName(f'{downloaded_dict["id"]}')
        hbox_layout = QHBoxLayout()

        item_label = QLabel()
        pixmap, push = self.get_icon_by_file_type(book_name)
        item_label.setPixmap(pixmap)
        hbox_layout.addWidget(item_label)

        vlayout = QVBoxLayout()
        file_name_label = QLabel(book_name)
        vlayout.addWidget(file_name_label)

        h_in_v_item_layout = QHBoxLayout()
        h_in_v_item_layout.addWidget(
            QLabel(downloaded_dict['size']), Qt.AlignRight)

        downloaded_date_label = QLabel()
        downloaded_date_label.setObjectName(f'{downloaded_dict["id"]}_date')
        downloaded_date_label.setText(f'{downloaded_dict["date"]}')
        h_in_v_item_layout.addWidget(downloaded_date_label, Qt.AlignRight)

        vlayout.addLayout(h_in_v_item_layout)
        hbox_layout.addLayout(vlayout)

        file_path = os.path.join(root, 'downloads', f'{book_name}')

        if os.path.exists(file_path):
            del_btn = QPushButton()
            del_btn.setIcon(QIcon(os.path.join(assets, 'delete.png')))
            del_btn.setStyleSheet("QPushButton{border:none}")
            del_btn.clicked.connect(lambda: self.remove_task(
                downloaded_dict["id"], file_path))

            if push:
                send_btn = QPushButton()
                send_btn.setIcon(QIcon(os.path.join(assets, 'send.png')))
                send_btn.setStyleSheet("QPushButton{border:none}")
                downloaded_dict['file_path'] = file_path
                send_btn.clicked.connect(
                    lambda: self.send_to_kindle(downloaded_dict))
                hbox_layout.addWidget(send_btn)

            hbox_layout.addWidget(del_btn)
        else:
            download_btn = QPushButton()
            download_btn.setIcon(
                QIcon(os.path.join(assets, 'download_btn.png')))
            download_btn.setStyleSheet("QPushButton{border:none}")
            download_btn.clicked.connect(
                lambda: self.regain(downloaded_dict))
            hbox_layout.addWidget(download_btn)

        item_widget.setLayout(hbox_layout)
        item_widget_style_sheet = f'#{downloaded_dict["id"]}{{background-color:rgb(241,231,230);color:rgb(210,10,10)}}'
        item_widget.setStyleSheet(item_widget_style_sheet)
        return item_widget

    def remove_task(self, id, file_path):
        if self.remove_file_or_not():
            if self.rm_file_check:
                self.remove_file(file_path)
            self.remove_task_from_list_widget(id)
            self.remove_task_from_data(id)

    def remove_file_or_not(self):
        rm_file_checkbox = QCheckBox('同时删除源文件')
        rm_file_checkbox.setChecked(True)
        rm_file_checkbox.stateChanged.connect(self.checkbox_check)
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText("您确定要删除此任务吗?")
        sure = message_box.addButton('确定', QMessageBox.AcceptRole)
        cancel = message_box.addButton('取消', QMessageBox.RejectRole)
        message_box.setDefaultButton(sure)
        message_box.setCheckBox(rm_file_checkbox)
        reply = message_box.exec()
        if reply == QMessageBox.AcceptRole:
            return True
        return False

    def checkbox_check(self, state):
        check = self.sender()
        if state == Qt.Unchecked:
            self.rm_file_check = False
        else:
            self.rm_file_check = True

    def remove_task_from_data(self, id):
        downloaded_dict_list = self.load_downloaded_dict_list()
        for downloaded_dict in downloaded_dict_list:
            if id in downloaded_dict['id']:
                downloaded_dict_list.remove(downloaded_dict)
        self.write_data(downloaded_dict_list)

    def write_data(self, downloaded_dict_list):
        with open(self.data_path, 'w') as f:
            json.dump(downloaded_dict_list, f)

    def remove_task_from_list_widget(self, id):
        item = self.downloaded_list_widget.findItems(id, Qt.MatchExactly)[0]
        self.downloaded_list_widget.takeItem(
            self.downloaded_list_widget.row(item))

    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def send_to_kindle(self, downloaded_dict):
        if not check_send_config():
            reply = QMessageBox.question(
                self, '配置提示', '推送配置未完成，不能推送书籍，需要现在配置吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                config_dialog = ConfigDialog(self)
                config_dialog.show()
            return
        downloaded_dict['status'] = "0"
        self.send_trigger.emit(downloaded_dict)
        QMessageBox.information(self, '推送通知', '正在推送...')
        self.send_work = SendWorker(downloaded_dict)
        self.send_work.send_trigger.connect(self.call_back_send)
        self.send_work.start()

    def regain(self, downloaded_dict):
        pass

    def get_file_extension(self, file_name):
        return file_name.strip().split(".")[-1]

    def get_icon_by_file_type(self, file_name):
        extension = self.get_file_extension(file_name)
        if extension in ['rar', 'zip', '7z']:
            return QPixmap(os.path.join(assets, 'zip.png')), False
        elif extension == 'mobi':
            return QPixmap(os.path.join(assets, 'book.png')), True
        elif extension == 'pdf':
            return QPixmap(os.path.join(assets, 'pdf.png')), True
        else:
            return QPixmap(os.path.join(assets, 'file.png')), False

    def get_status_msg(self, status_code):
        status_dict = {"1": "推送成功", "-1": "推送失败", "0": "正在推送"}
        if str(status_code) in status_dict:
            return status_dict[str(status_code)]
        else:
            return '未知状态'

    def call_back_send(self, send_dict):
        QMessageBox.information(
            self, '推送完成', self.get_status_msg(send_dict['status']))
        self.send_trigger.emit(send_dict)

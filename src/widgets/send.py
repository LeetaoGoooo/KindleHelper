from PyQt5.QtWidgets import QWidget, QListWidget,QTableWidgetItem, QPushButton, QTableWidget, QAbstractItemView, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal

import os
import json
import hashlib
import copy
import time

from worker import SendWorker
from common import check_send_config, ConfigDialog, data_path, assets_path


class SendedPage(QWidget):

    def __init__(self, parent=None):
        super(SendedPage, self).__init__(parent)
        self.data_path = os.path.join(data_path,'sended.json')
        self.file_push_btn = PushButton(self)
        self.push_table = QTableWidget(self)
        self.init_ui()

    def init_ui(self):

        self.init_upload_btn()
        self.init_push_table()

        load_sended_dict_list = self.load_sended_dict_list()
        if not load_sended_dict_list:
            return
        for sended_dict in load_sended_dict_list:
            self.add_sended_item_to_widget(sended_dict)

    def init_upload_btn(self):
        self.file_push_btn.setEnabled(True)
        self.file_push_btn.setGeometry(QRect(210, 20, 570, 120))
        self.file_push_btn.setStyleSheet("QPushButton#file_push_btn{background-color:white;color:white;border:none}")
        self.file_push_btn.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(assets_path,"upload.png")), QIcon.Normal, QIcon.Off)
        self.file_push_btn.setIcon(icon)
        self.file_push_btn.setIconSize(QSize(64, 64))
        self.file_push_btn.setAutoDefault(False)
        self.file_push_btn.setDefault(False)
        self.file_push_btn.setFlat(False)
        self.file_push_btn.setObjectName("file_push_btn")
        self.file_push_btn.setToolTip('由推送窗口主动推送的文件，将不会记录到推送历史记录中')

    def init_push_table(self):
        self.push_table.setGeometry(QRect(10, 160, 950, 700))
        self.push_table.setStyleSheet("QTableView#push_table{border:none;}")
        self.push_table.setColumnCount(4)
        self.push_table.setObjectName("push_table")
        self.push_table.setRowCount(0)
        self.push_table.horizontalHeader().setStretchLastSection(True)
        self.push_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.push_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.push_table.setHorizontalHeaderLabels(["推送文件名称","推送时间","推送状态","文件id"])
        self.push_table.setColumnWidth(0, 300)
        self.push_table.setColumnWidth(1, 300)
        self.push_table.setColumnWidth(2, 300)
        self.push_table.setColumnHidden(3,True)
        self.push_table.horizontalHeader().setSectionsClickable(False)
        self.push_table.setEditTriggers(QAbstractItemView.NoEditTriggers)               

    def add_sended_item(self, sended_dict):
        self.add_sended_item_to_widget(sended_dict)
        self.add_sended_item_to_data(sended_dict)

    def add_sended_item_to_widget(self, sended_dict):
        book_name = sended_dict['file_name']
        send_time = sended_dict['date']
        send_status_msg = self.get_status_msg(sended_dict['status'])
        
        row_count = self.push_table.rowCount()
        self.push_table.insertRow(row_count)
        self.push_table.setRowHeight(row_count, 60)        
        self.push_table.setItem(row_count, 0, QTableWidgetItem(book_name))
        self.push_table.setItem(row_count, 1, QTableWidgetItem(send_time))
        self.push_table.setItem(row_count,2, QTableWidgetItem(send_status_msg))
        self.push_table.setItem(row_count,3,QTableWidgetItem(sended_dict['id']))

    def get_status_msg(self, status_code):
        status_dict = {"1":"推送成功","-1":"推送失败","0":"正在推送"}
        if str(status_code) in status_dict:
            return status_dict[str(status_code)]
        else:
            return '未知状态'

    def add_sended_item_to_data(self, sended_dict):
        sended_dict_list = self.load_sended_dict_list()
        sended_dict_list.append(sended_dict)
        self.write_data(sended_dict_list)

    def load_sended_dict_list(self):
        if not os.path.exists(self.data_path):
            os.makedirs(data_path,exist_ok=True)
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            sended_dict_list = json.load(f)
            return sended_dict_list
 
    def write_data(self, sended_dict_list):
        with open(self.data_path, 'w') as f:
            json.dump(sended_dict_list, f)

    def update_sended_item(self, sended_dict):
        self.update_sended_item_to_data(sended_dict)
        self.update_sended_item_to_widget(sended_dict)
    
    def update_sended_item_to_widget(self, sended_dict):
        items = self.push_table.findItems(sended_dict['id'],Qt.MatchExactly)
        if items:
            row = items[0].row()
            status = self.get_status_msg(sended_dict['status'])
            self.push_table.item(row,3).setText(status)

    
    def update_sended_item_to_data(self, sended_dict):
        sended_dict_list = self.load_sended_dict_list()
        for sended_dict_item in sended_dict_list:
            if sended_dict_item['id'] == sended_dict['id']:
                sended_dict_item['status'] = sended_dict['status']
        self.write_data(sended_dict_list)        


class PushButton(QPushButton):                              
    def __init__(self, parent):
        super(PushButton, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        file_path = e.mimeData().text().strip().replace('file:///','')
        print(file_path)
        file_name = os.path.basename(file_path)
        extension = self.get_file_extension(file_name)
        if not check_send_config():
            reply = QMessageBox.question(self,'配置提示','推送配置未完成，不能推送书籍，需要现在配置吗?',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                config_dialog = ConfigDialog(self)
                config_dialog.show()
            return
        if self.can_push(extension):
            reply =  QMessageBox.question(self,'推送确认',f'确认推送{file_name}(该条推送将不会记录到推送历史数据中))')
            if reply == QMessageBox.Yes:
                self.sender_work = SendWorker({"file_path":file_path})
                self.sender_work.send_trigger.connect(self.call_back)
                self.sender_work.start()
        else:
            QMessageBox.warning(self,'格式不支持',f'不支持{extension}的文件的推送')
    
    def can_push(self, extension):
        return (extension.lower() in ['mobi','pdf','txt','azw','epub'])

    def get_file_extension(self, file_name):
        return file_name.strip().split(".")[-1]
    
    def call_back(self, sended_dict):
        QMessageBox.information(self,'推送结果',self.get_status_msg(sended_dict['status']))


    def get_status_msg(self, status_code):
        status_dict = {"1":"推送成功","-1":"推送失败","0":"正在推送"}
        if str(status_code) in status_dict:
            return status_dict[str(status_code)]
        else:
            return '未知状态'
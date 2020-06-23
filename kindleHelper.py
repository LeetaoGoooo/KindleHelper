# -*- encoding:utf-8 -*-

import sys
import hashlib
from datetime import datetime
# 打包的时候使用
# import fix_qt_import_error 

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QFrame, QAbstractItemView, QHBoxLayout, QPushButton, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QIcon, QPixmap

from ui import KindleHelperUI
from widgets import ProgressBar, SysTray

from worker import SearchWorker, DownloadWorker


class KindleHelper(KindleHelperUI, QMainWindow):

    def __init__(self, parent=None):
        super(KindleHelper, self).__init__(parent)
        self.setWindowTitle("Kindle助手")
        self.setWindowIcon(QIcon('kindle.icns'))
        self.expire = False
        self.setupUi(self)
        self.clipboard = QApplication.clipboard()
        self.init_ui()

    def expire_or_not(self):
        end_date_str = '2019-11-18 00:00:00'
        now = datetime.now()
        format_pattern = '%Y-%m-%d %H:%M:%S'
        difference = datetime.strptime(end_date_str, format_pattern) - now
        if difference.days <= 0:
            return True
        return False


    def init_ui(self):
        self.init_sider_btn_groups()
        self.init_search_page()
        self.init_direct_tab()
        self.init_net_pan_tab()
        self.init_progressbar()
        self.init_systray()
        self.init_trigger()

    def init_trigger(self):
        self.downloaded_widget.send_trigger.connect(self.sended_page.add_sended_item)
        self.task_widget.new_task_trigger.connect(self.download)

    def init_systray(self):
        self.tray = SysTray(self)
        self.tray.trigger.connect(self.systray_trigger_callback)
        self.tray.show()

    def systray_trigger_callback(self, action_dict):
        if action_dict['visible']:
            # self.setVisible(True)
            self.show()
        if action_dict['quit']:
            # self.setVisible(False)
            self.hide()
            sys.exit()

    def init_search_page(self):
        if not self.expire:
            self.search_book_lineEdit.returnPressed.connect(self.input_search)
        else:
            self.search_book_lineEdit.setDisabled(True)


    def init_progressbar(self):
        self.progressbar = ProgressBar(
            self, minimum=0, maximum=0, textVisible=False, objectName="RedProgressBar")
        self.progressbar.setGeometry(QRect(-10, 0, 1230, 3))
        self.progressbar.setMaximumSize(16777215, 3)
        self.progressbar.setMinimumSize(0, 2)
        self.progressbar.start()
        self.progressbar.setTextVisible(False)
        self.progressbar.setHidden(True)

    def init_sider_btn_groups(self):
        self.sider_page_dict = {
            "search_btn": 0,
            "new_task_btn": 1,
            "downloading_btn": 2,
            "done_btn": 3,
            "send_btn": 4,
            "about_btn": 5
        }
        self.search_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.search_btn))
        self.new_task_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.new_task_btn))
        self.downloading_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.downloading_btn))
        self.done_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.done_btn))
        self.send_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.send_btn))
        self.about_btn.clicked.connect(
            lambda: self.sider_btn_checked(self.about_btn))

    def sider_btn_checked(self, btn):
        self.search_btn.setChecked(False)
        self.new_task_btn.setChecked(False)
        self.downloading_btn.setChecked(False)
        self.done_btn.setChecked(False)
        self.send_btn.setChecked(False)
        self.about_btn.setChecked(False)
        self.stackedWidget.setCurrentIndex(
            self.sider_page_dict[btn.objectName()])
        btn.setChecked(True)

    def input_search(self):
        search_keyword = self.search_book_lineEdit.text().strip()
        self.search_book_lineEdit.setDisabled(True)
        if search_keyword == "":
            QMessageBox.warning(self, "KindleHelper", "搜索书籍名称不能为空!")
            self.search_book_lineEdit.setDisabled(False)
            return
        self.progressbar.setHidden(False)
        self.start_work_thread(search_keyword)

    def start_work_thread(self, keyword):
        self.search_worker = SearchWorker(keyword)
        self.search_worker.trigger.connect(self.callback_search)
        self.search_worker.start()

    def callback_search(self, download_dict):
        self.search_book_lineEdit.setDisabled(False)
        self.progressbar.setHidden(True)
        self.callback_search_direct_tab(download_dict['direct'])
        self.callback_search_net_tab(download_dict['net'])

    def callback_search_direct_tab(self, direct_download_dict_list):
        self.direct_tab.setRowCount(0)
        row_count = 0
        for direct_download_dict in direct_download_dict_list:
            if direct_download_dict:
                key = list(direct_download_dict.keys())[0]
                self.direct_tab.insertRow(row_count)
                self.direct_tab.setRowHeight(row_count, 60)
                book_name = key
                book_size = direct_download_dict[key]['size']
                speed = direct_download_dict[key]['speed']
                download_url = direct_download_dict[key]['download']
                download_dict = {
                    "id": hashlib.md5(download_url.encode('utf-8')).hexdigest(),
                    "file_name": book_name,
                    "url": download_url,
                    "size": book_size
                }
                download_btn = self.create_download_btn(download_dict)
                self.direct_tab.setItem(
                    row_count, 0, QTableWidgetItem(book_name))
                self.direct_tab.setItem(
                    row_count, 1, QTableWidgetItem(book_size))
                self.direct_tab.setItem(row_count,2, QTableWidgetItem(speed))
                self.direct_tab.setCellWidget(row_count, 3, download_btn)
                row_count += 1
    
    def callback_search_net_tab(self, net_download_dict_list):
        self.net_pan_tab.setRowCount(0)
        row_count = 0
        for net_download_dict in net_download_dict_list:
            if net_download_dict:
                key = list(net_download_dict.keys())[0]
                self.net_pan_tab.insertRow(row_count)
                self.net_pan_tab.setRowHeight(row_count, 60)
                book_name = key
                self.net_pan_tab.setItem(
                    row_count, 0, QTableWidgetItem(book_name))
                btn_groups_dict = self.create_net_pan_btn_groups_dict(net_download_dict)
                for key in btn_groups_dict:
                    self.net_pan_tab.setCellWidget(row_count, key, btn_groups_dict[key])
                row_count += 1
    
    def create_net_pan_btn_groups_dict(self, net_pan_dict):
        btn_dict = {}
        pan_dict = net_pan_dict[list(net_pan_dict.keys())[0]]
        for key in pan_dict:
            widget = QWidget()
            widget.setObjectName(f'{hashlib.md5(key.encode("utf-8")).hexdigest()}_widget')
            btn = QPushButton()
            btn.setStyleSheet("QPushButton{border:none}")
            btn.setToolTip('打开浏览器下载文件')     
            hbox_layout = QHBoxLayout()
            hbox_layout.addWidget(btn, Qt.AlignHCenter)
            widget.setLayout(hbox_layout)    
            if '百度网盘' in key:
                btn.setIcon(QIcon('baidu.png'))
                btn.setObjectName(f'{key}-{pan_dict[key]}')
                btn.clicked.connect(self.copy_download_url)
                btn_dict[1] = widget
            elif '腾讯微云' == key:
                btn.setIcon(QIcon('tengxun.png'))
                btn.setObjectName(f'{pan_dict[key]}')
                btn.clicked.connect(self.copy_download_url)
                btn_dict[2] = widget
            else:             
                btn.setIcon(QIcon('chengtong.png'))
                btn.setObjectName(f'{pan_dict[key]}')
                btn.clicked.connect(self.copy_download_url)
                btn_dict[3] = widget
        return btn_dict

    def copy_download_url(self):
        print(self.sender().objectName())
        self.clipboard.setText(self.sender().objectName())
        QMessageBox.information(self,None,'下载地址成功复制到剪贴板!')

    def create_download_btn(self, download_dict):
        widget = QWidget()
        download_btn = QPushButton()
        download_btn.setIcon(QIcon('download_btn.png'))
        download_btn.setObjectName("item_download_btn")
        download_btn.setStyleSheet("QPushButton#item_download_btn{\n"
                                   " border:none;}")
        download_btn.clicked.connect(
            lambda: self.download_book(download_btn, download_dict))
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(download_btn, Qt.AlignHCenter)
        widget.setLayout(hbox_layout)
        return widget

    def init_direct_tab(self):
        self.direct_tab = QTableWidget()
        self.direct_tab.setFrameShape(QFrame.NoFrame)
        self.direct_tab.setColumnCount(4)
        self.direct_tab.horizontalHeader().setStretchLastSection(True)
        self.direct_tab.setSelectionMode(QAbstractItemView.SingleSelection)
        self.direct_tab.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.direct_tab.setHorizontalHeaderLabels(['文件名称', '文件大小','下载时间','操作'])
        self.direct_tab.horizontalHeader().setSectionsClickable(False)
        self.direct_tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.direct_tab.setColumnWidth(0, 600)
        self.direct_tab.setColumnWidth(1, 100)
        self.direct_tab.setColumnWidth(2, 100)
        self.direct_tab.setColumnWidth(3, 40)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.direct_tab)
        self.direct_download.setLayout(hbox_layout)
    
    def init_net_pan_tab(self):
        self.net_pan_tab = QTableWidget()
        self.net_pan_tab.setFrameShape(QFrame.NoFrame)
        self.net_pan_tab.setColumnCount(4)
        self.net_pan_tab.horizontalHeader().setStretchLastSection(True)
        self.net_pan_tab.setSelectionMode(QAbstractItemView.SingleSelection)
        self.net_pan_tab.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.net_pan_tab.setHorizontalHeaderLabels(['文件名称', '百度网盘','腾讯微云','城通网盘'])
        self.net_pan_tab.horizontalHeader().setSectionsClickable(False)
        self.net_pan_tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.net_pan_tab.setColumnWidth(0, 480)
        self.net_pan_tab.setColumnWidth(1, 120)
        self.net_pan_tab.setColumnWidth(2, 120)
        self.net_pan_tab.setColumnWidth(3, 120)
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.net_pan_tab)
        self.netpan.setLayout(hbox_layout)

    def download_book(self, button, download_dict):
        row = self.direct_tab.indexAt(button.pos()).row()
        self.direct_tab.removeRow(row)
        QMessageBox.about(self, None, '开始下载')
        self.download(download_dict)

    def download(self, download_dict):
        self.download_worker = DownloadWorker(download_dict)
        self.downloading_widget.add_downloading_item(download_dict)
        self.download_worker.trigger.connect(self.callback_download)
        self.download_worker.download_trigger.connect(self.callback_download_progress)
        self.download_worker.start()

    def callback_download(self, download_return_list):
        finish_or_not, download_dict = download_return_list
        msg = f'{download_dict["file_name"]}下载失败!'
        if finish_or_not:
            msg = f'{download_dict["file_name"]}下载完成!'
            self.downloading_widget.remove_task(download_dict['id'])
            self.downloaded_widget.add_downloaded_item(download_dict)
        QMessageBox.information(self,None,msg)
    
    def callback_download_progress(self, download_progress_dict):
        self.downloading_widget.update_progress(download_progress_dict)

    def closeEvent(self, event):
        quit_flag = QMessageBox.question(
            self, '退出确认', '确认退出应用程序?', QMessageBox.Yes | QMessageBox.No)
        event.ignore()
        if quit_flag == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            # self.setVisible(False)
            self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = KindleHelper()
    myWin.show()
    sys.exit(app.exec_())

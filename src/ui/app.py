# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/app2.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from widgets import DownloadingPage, DownloadedPage, SendedPage, TaskPage, AboutPage

import os

from common import assets_path

class Ui_KindleHelper(object):
    def setupUi(self, KindleHelper):
        KindleHelper.setObjectName("KindleHelper")
        KindleHelper.resize(1218, 900)
        KindleHelper.setMaximumSize(QtCore.QSize(1218, 900))
        KindleHelper.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(KindleHelper)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(250, 0, 971, 881))
        self.stackedWidget.setStyleSheet("QStackedWidget{\n"
"    background-color:rgb(255,255,255);\n"
"}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.search_page = QtWidgets.QWidget()
        self.search_page.setObjectName("search_page")
        self.search_book_lineEdit = QtWidgets.QLineEdit(self.search_page)
        self.search_book_lineEdit.setGeometry(QtCore.QRect(170, 20, 641, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 248, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.search_book_lineEdit.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.search_book_lineEdit.setFont(font)
        self.search_book_lineEdit.setAutoFillBackground(False)
        self.search_book_lineEdit.setStyleSheet("QLineEdit {\n"
"        border-radius: 10px;\n"
"    background-color: rgb(247,248,250);\n"
"}\n"
"QLineEdit::focus {\n"
"    background-color:rgb(247,248,250)\n"
"}")
        self.search_book_lineEdit.setPlaceholderText("")
        self.search_book_lineEdit.setObjectName("search_book_lineEdit")
        self.downloadTab = QtWidgets.QTabWidget(self.search_page)
        self.downloadTab.setGeometry(QtCore.QRect(10, 140, 951, 731))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.downloadTab.setFont(font)
        self.downloadTab.setStyleSheet("QTableWidget::downloadTab{\n"
"  border:none;\n"
"}")
        self.downloadTab.setTabPosition(QtWidgets.QTabWidget.North)
        self.downloadTab.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.downloadTab.setObjectName("downloadTab")
        self.direct_download = QtWidgets.QWidget()
        self.direct_download.setObjectName("direct_download")
        self.downloadTab.addTab(self.direct_download, "")
        self.netpan = QtWidgets.QWidget()
        self.netpan.setObjectName("netpan")
        self.downloadTab.addTab(self.netpan, "")
        self.stackedWidget.addWidget(self.search_page)
        self.task_page = QtWidgets.QWidget()
        self.task_page.setObjectName("task_page")
        self.task_widget = TaskPage(self.task_page)
        self.stackedWidget.addWidget(self.task_page)
        self.downloading_page = QtWidgets.QWidget()
        self.downloading_page.setObjectName("downloading_page")

        self.downloading_widget = DownloadingPage(self.downloading_page)
        self.downloading_widget.setGeometry(QtCore.QRect(0, 21, 1011, 861))

        self.stackedWidget.addWidget(self.downloading_page)
        self.downloaded_page = QtWidgets.QWidget()
        self.downloaded_page.setObjectName("downloaded_page")
        #self.open_download_dir_btn = QtWidgets.QPushButton(self.downloaded_page)
        #self.open_download_dir_btn.setEnabled(True)
        #self.open_download_dir_btn.setGeometry(QtCore.QRect(820, 836, 120, 26))
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(15)
#         sizePolicy.setVerticalStretch(15)
#         sizePolicy.setHeightForWidth(self.open_download_dir_btn.sizePolicy().hasHeightForWidth())
#         self.open_download_dir_btn.setSizePolicy(sizePolicy)
#         self.open_download_dir_btn.setMaximumSize(QtCore.QSize(160, 30))
#         self.open_download_dir_btn.setSizeIncrement(QtCore.QSize(15, 15))
#         self.open_download_dir_btn.setBaseSize(QtCore.QSize(15, 15))
#         font = QtGui.QFont()
#         font.setFamily("Agency FB")
#         font.setPointSize(6)
#         self.open_download_dir_btn.setFont(font)
#         self.open_download_dir_btn.setAutoFillBackground(False)
#         self.open_download_dir_btn.setStyleSheet("\n"
# "QPushButton#open_download_dir_btn{\n"
# "    background-color:#ddd;\n"
# "    border-radius:4px 4px 0 0;\n"
# "    background-color:rgb(242, 58, 58);\n"
# "    color:white;    \n"
# "\n"
# "}\n"
# "\n"
# "")
#         self.open_download_dir_btn.setIconSize(QtCore.QSize(15, 15))
#         self.open_download_dir_btn.setCheckable(False)
#         self.open_download_dir_btn.setAutoDefault(False)
#         self.open_download_dir_btn.setDefault(False)
#         self.open_download_dir_btn.setFlat(False)
#         self.open_download_dir_btn.setObjectName("open_download_dir_btn")
        self.downloaded_widget = DownloadedPage(self.downloaded_page)
        self.downloaded_widget.setGeometry(QtCore.QRect(0, 20, 1011, 811))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.downloaded_widget.setFont(font)
        self.downloaded_widget.setStyleSheet("QListView#downloaded_files_list{\n"
"   border:none\n"
"}")
        self.downloaded_widget.setObjectName("downloaded_files_list")
        self.stackedWidget.addWidget(self.downloaded_page)
        self.push_page = QtWidgets.QWidget()
        self.push_page.setObjectName("push_page")
        self.sended_page = SendedPage(self.push_page)
        self.stackedWidget.addWidget(self.push_page)

        self.about_page = QtWidgets.QWidget()
        self.about_page.setObjectName("about_page")
        self.about_widget = AboutPage(self.about_page)

        self.stackedWidget.addWidget(self.about_page)
        self.sidebar_widget = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_widget.setEnabled(True)
        self.sidebar_widget.setGeometry(QtCore.QRect(10, -20, 231, 891))
        self.sidebar_widget.setAutoFillBackground(False)
        self.sidebar_widget.setStyleSheet("QWidget{\n"
"    background-color:rgb(242,242,241);\n"
"}")
        self.sidebar_widget.setObjectName("sidebar_widget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.sidebar_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 70, 231, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.sidebar_gridlayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.sidebar_gridlayout.setContentsMargins(0, 0, 0, 6)
        self.sidebar_gridlayout.setHorizontalSpacing(4)
        self.sidebar_gridlayout.setVerticalSpacing(0)
        self.sidebar_gridlayout.setObjectName("sidebar_gridlayout")
        self.send_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.send_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);padding: 10px 15px;}\n"
" QPushButton#send_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"\n"
"    QPushButton#send_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10)\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"send.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"send_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.send_btn.setIcon(icon1)
        self.send_btn.setIconSize(QtCore.QSize(15, 15))
        self.send_btn.setCheckable(True)
        self.send_btn.setObjectName("send_btn")
        self.sidebar_gridlayout.addWidget(self.send_btn, 4, 0, 1, 1)
        self.done_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.done_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);\n"
"padding: 10px 15px;}\n"
"    QPushButton#done_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"    QPushButton#done_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10)\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"done.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"done_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.done_btn.setIcon(icon2)
        self.done_btn.setIconSize(QtCore.QSize(15, 15))
        self.done_btn.setCheckable(True)
        self.done_btn.setObjectName("done_btn")
        self.sidebar_gridlayout.addWidget(self.done_btn, 3, 0, 1, 1)
        self.about_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.about_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);padding: 10px 15px;}\n"
" QPushButton#about_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"    QPushButton#about_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10)\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"about_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.about_btn.setIcon(icon3)
        self.about_btn.setIconSize(QtCore.QSize(16, 16))
        self.about_btn.setCheckable(True)
        self.about_btn.setObjectName("about_btn")
        self.sidebar_gridlayout.addWidget(self.about_btn, 5, 0, 1, 1)
        self.downloading_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.downloading_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);\n"
"padding: 10px 15px;}\n"
"    QPushButton#downloading_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"    QPushButton#downloading_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10)\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"download.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"download_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.downloading_btn.setIcon(icon4)
        self.downloading_btn.setIconSize(QtCore.QSize(15, 15))
        self.downloading_btn.setCheckable(True)
        self.downloading_btn.setObjectName("downloading_btn")
        self.sidebar_gridlayout.addWidget(self.downloading_btn, 2, 0, 1, 1)
        self.new_task_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.new_task_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);\n"
"padding: 10px 15px;}\n"
"    QPushButton#new_task_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"    QPushButton#new_task_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10)\n"
"}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"add_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.new_task_btn.setIcon(icon5)
        self.new_task_btn.setIconSize(QtCore.QSize(15, 15))
        self.new_task_btn.setCheckable(True)
        self.new_task_btn.setObjectName("new_task_btn")
        self.new_task_btn.setHidden(True)
        # TODO v1.0.0 不添加直接下载功能
        #self.sidebar_gridlayout.addWidget(self.new_task_btn, 1, 0, 1, 1)
        self.search_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.search_btn.setStyleSheet("    QPushButton{border:none;background-color:rgb(242,242,241);color:rgb(102,102,102);\n"
"padding: 10px 15px;}\n"
"    QPushButton#search_btn:hover{border-left:4px solid red;font-weight:700;}\n"
"    QPushButton#search_btn:checked {background-color:rgb(241,231,230);font-weight:700;\n"
"    color:rgb(210,10,10);\n"
"}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"search_selected.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon6.addPixmap(QtGui.QPixmap(os.path.join(assets_path,"search_selected.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.search_btn.setIcon(icon6)
        self.search_btn.setIconSize(QtCore.QSize(15, 15))
        self.search_btn.setCheckable(True)
        self.search_btn.setChecked(False)
        self.search_btn.setObjectName("search_btn")
        self.sidebar_gridlayout.addWidget(self.search_btn, 0, 0, 1, 1)
        KindleHelper.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(KindleHelper)
        self.statusbar.setObjectName("statusbar")
        KindleHelper.setStatusBar(self.statusbar)

        self.retranslateUi(KindleHelper)
        self.stackedWidget.setCurrentIndex(0)
        self.downloadTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(KindleHelper)

    def retranslateUi(self, KindleHelper):
        _translate = QtCore.QCoreApplication.translate
        KindleHelper.setWindowTitle(_translate("KindleHelper", "Kindle助手"))
        self.downloadTab.setTabText(self.downloadTab.indexOf(self.direct_download), _translate("KindleHelper", "直接下载"))
        self.downloadTab.setTabText(self.downloadTab.indexOf(self.netpan), _translate("KindleHelper", "网盘"))
        #self.open_download_dir_btn.setText(_translate("KindleHelper", "打开目录"))
        self.send_btn.setText(_translate("KindleHelper", "推送文件"))
        self.done_btn.setText(_translate("KindleHelper", "下载完成"))
        self.about_btn.setText(_translate("KindleHelper", "关于软件"))
        self.downloading_btn.setText(_translate("KindleHelper", "正在下载"))
        #self.new_task_btn.setText(_translate("KindleHelper", "新建任务"))
        self.search_btn.setText(_translate("KindleHelper", "搜索一下"))

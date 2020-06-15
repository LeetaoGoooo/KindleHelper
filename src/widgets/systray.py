from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
import os


class SysTray(QSystemTrayIcon):
    trigger = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(SysTray, self).__init__(parent)
        self.setIcon(QIcon('kindle.icns'))
        self.show_menu()

    def show_menu(self):
        self.menu = QMenu()
        self.display_action = QAction(
            "显示主页面", self, triggered=self.dispaly_main_window)
        self.quit_action = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.display_action)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)

    def dispaly_main_window(self):
        self.trigger.emit({"visible": True, "quit": False})

    def quit(self):
        self.setVisible(False)
        self.trigger.emit({"quit": True, "visible": False})

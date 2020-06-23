from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QPixmap

import os
import json

from common import config_path, assets_path


class AboutPage(QWidget):

    def __init__(self, parent=None):
        super(AboutPage, self).__init__(parent)
        self.setGeometry(QRect(10, 20, 950, 800))
        os.makedirs(config_path,exist_ok=True)
        self.init_ui()

    def init_ui(self):
        self.about_layout = QFormLayout(self)
        self.about_layout.setVerticalSpacing(10)
        self.config_panel()
        self.wechat_panel()
        self.reward_panel()

    def config_panel(self):
        self.setStyleSheet("QLineEdit{border:1px solid rgb(242, 58, 58);border-radius:4px 4px 0 0}")

        self.send_email = QLineEdit(self)
        self.send_password = QLineEdit(self)
        self.receive_email = QLineEdit(self)
        self.save_btn = QPushButton('保存')
        self.save_btn.setFixedSize(120,40)
        self.save_btn.setStyleSheet("QPushButton{background-color:#ddd;border-radius:4px 4px 0 0;background-color:rgb(242, 58, 58);color:white;}")
        self.save_btn.clicked.connect(self.save_config)

        self.about_layout.addRow("推送邮箱", self.send_email)
        self.about_layout.addRow("推送邮箱密码", self.send_password)
        self.about_layout.addRow("kindle邮箱", self.receive_email)
        self.about_layout.addWidget(self.save_btn)
        
        self.init_config_panel()

    def init_config_panel(self):
        if os.path.exists(os.path.join(config_path,'kindle-send.json')):
            with open(os.path.join(config_path,'kindle-send.json'),'r') as f:
                kindle_send = json.load(f)
                self.send_email.setText(kindle_send.get("sender","").strip())
                self.send_password.setText(kindle_send.get("password","").strip())
                self.receive_email.setText(kindle_send.get("recevier","").strip())

    def wechat_panel(self):
        self.wx_label = QLabel()
        self.wx_label.setPixmap(QPixmap(os.path.join(assets_path,'wx.jpg')))
        self.about_layout.addRow('关注作者',self.wx_label)


    def reward_panel(self):
        self.reward_code_label = QLabel()
        self.reward_code_label.setPixmap(QPixmap(os.path.join(assets_path,'reward.jpg')))
        self.about_layout.addRow('赞助作者',self.reward_code_label)

    def save_config(self):
        send_email = self.send_email.text()
        send_password = self.send_password.text()
        revice_email = self.receive_email.text()
        if not all([send_email,send_password,revice_email]):
            QMessageBox.warning(self,'保存警告','请将信息补充完成')
            return
        config_dict = {
            "sender": send_email,
            "password": send_password,
            "recevier": revice_email
        }
        return self.write_config(config_dict)

    def write_config(self, config_dict):
        with open(os.path.join(config_path,'kindle-send.json'), 'w') as f:
            json.dump(config_dict, f)
        QMessageBox.information(self, "保存提示", "保存配置文件成功")

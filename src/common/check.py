
import os
import json

from PyQt5.QtWidgets import QMessageBox, QDialog,QPushButton,QLineEdit,QFormLayout
from PyQt5.QtCore import Qt
from .constans import config_path


class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowTitle('推送配置')
        self.setWindowFlags(Qt.Window)
        self.setFixedSize(400,200)
        self.send_email = QLineEdit(self)
        self.send_password = QLineEdit(self)
        self.receive_email = QLineEdit(self)
        self.save_btn = QPushButton('保存')
        self.save_btn.clicked.connect(self.save_config)

        layout = QFormLayout(self)
        layout.addRow("推送邮箱", self.send_email)
        layout.addRow("推送邮箱密码", self.send_password)
        layout.addRow("kindle邮箱",self.receive_email)
        layout.addWidget(self.save_btn)

    def save_config(self):
        send_email = self.send_email.text()
        send_password = self.send_password.text()
        revice_email = self.receive_email.text()
        config_dict = {
            "sender":send_email,
            "password":send_password,
            "recevier":revice_email
        }
        return self.write_config(config_dict)
    
    def write_config(self, config_dict):
        os.makedirs(config_path,exist_ok=True)
        with open(os.path.join(config_path,'kindle-send.json'),'w') as f:
            json.dump(config_dict,f)
        QMessageBox.information(self,"保存提示","保存配置文件成功")
        self.destroy()
           

def check_send_config():
    if not os.path.exists(os.path.join(config_path,'kindle-send.json')):
        return False
    with open(os.path.join(config_path,'kindle-send.json'),'r',encoding='utf-8') as f:
        config_dict = json.load(f)
        if 'sender' not in config_dict or 'password' not in config_dict:
            return False
    return True

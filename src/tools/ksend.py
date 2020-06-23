# -*- encoding:utf-8 -*-

'''
 Kindle 推送工具
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import os
import json

from exceptions import ConfigLackException, ConfigNotFoundError, EmailSendException, SendFileNotFoundError

from common import config_path

class KindleSend:
    
    def __init__(self):
        self.load_config()
        self.email_msg = MIMEMultipart()
        self.email_msg['From'] = self.sender
        self.email_msg['To'] = self.recevier


    def load_config(self):
        if not os.path.exists(os.path.join(config_path,'kindle-send.json')):
            raise ConfigNotFoundError('Kindle send config file not found!')
        with open(os.path.join(config_path, 'kindle-send.json'),'r',encoding='utf-8') as f:
            config_dict = json.load(f)
            if 'sender' not in config_dict or 'password' not in config_dict:
                raise ConfigLackException('sender/password/recevier was lacked')
            self.sender = config_dict['sender']
            self.password = config_dict['password']
            self.recevier = config_dict['recevier']
        
    def send(self, file_path):
        if not os.path.exists(file_path):
            raise SendFileNotFoundError(f'file {file_path} was not found!')
        file_name = os.path.basename(file_path)
        attach_file = MIMEApplication(open(file_path,'rb').read())
        attach_file.add_header('Content-Disposition', 'attachment', filename=file_name)
        self.email_msg['Subject'] = file_name
        self.email_msg.attach(attach_file)
        try:
            email_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            email_server.login(self.sender,self.password)
            email_server.sendmail(self.sender,self.recevier,self.email_msg.as_string())
            email_server.quit()
        except Exception as e:
            raise EmailSendException(f'send email failed:{e}')
        print(f'send {file_name} successfully!')
        return True

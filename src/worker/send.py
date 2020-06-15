
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from tools import KindleSend

from exceptions import ConfigLackException, ConfigNotFoundError, EmailSendException, SendFileNotFoundError


class SendWorker(QThread):
    send_trigger = pyqtSignal(dict)

    def __init__(self, send_dict):
        super(SendWorker, self).__init__()
        self.file_path = send_dict['file_path']
        self.kindle_send = KindleSend()
        self.send_dict = send_dict
    

    def run(self):
        exception_flag = False
        try:
            send_flag = self.kindle_send.send(self.file_path)
        except Exception as e:
            print(e)
            exception_flag = True

        if not exception_flag:
            if send_flag:
                self.send_dict['status'] = "1"
            else:
                self.send_dict['status'] = "-1"
        else:
            self.send_dict['status'] = "2"
        self.send_trigger.emit(self.send_dict)
            


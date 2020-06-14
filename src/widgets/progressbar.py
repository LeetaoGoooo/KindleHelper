# -*- encoding: utf-8 -*-
from random import randint
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QProgressBar

style_sheet = '''
#RedProgressBar {
    min-height: 6px;
    max-height: 6px;
    border-radius: 6px;
}
#RedProgressBar::chunk {
    border-radius: 6px;
    width:12px;
    background-color: #D20A0A;
}
#GreenProgressBar {
    min-height: 6px;
    max-height: 6px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    width:12px;
    background-color: #009688;
}

#BlueProgressBar {
    border: 2px solid #2196F3;/*边框以及边框颜色*/
    border-radius: 5px;
    background-color: #E0E0E0;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
    width: 10px;
    margin: 0.5px;
}
'''


class ProgressBar(QProgressBar):
    def __init__(self,*args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setStyleSheet(style_sheet)
        self.setValue(0)
    
    def start(self):
        if self.minimum() != self.maximum():
            self.timer = QTimer(self, timeout=self.on_timeout)
            self.timer.start(randint(1, 3) * 1000)

    def on_timeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)
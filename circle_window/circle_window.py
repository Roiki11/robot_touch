# This Python file uses the following encoding: utf-8
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *

path = os.path.dirname(__file__)
qtCreatorFile = "circle_dialog.ui"

Circle_Dialog, _ = uic.loadUiType(os.path.join(path,qtCreatorFile))

class circle_window(QtWidgets.QDialog, Circle_Dialog):
    def __init__(self):
       super(numpad, self).__init__()
       self.setupUi(self)
       circ_result = pyqtSignal(float)
       self.show()


    @pyqtSlot()
    def Result(self):
        s = numpad.entryline.text()
        self.circ_result.emit(s)



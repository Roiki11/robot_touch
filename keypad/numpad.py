# This Python file uses the following encoding: utf-8
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *

path = os.path.dirname(__file__)
qtCreatorFile = "dialog.ui"

Ui_Dialog, _ = uic.loadUiType(os.path.join(path,qtCreatorFile))
a = []
b=""

class numpad(QtWidgets.QDialog, Ui_Dialog):


    def __init__(self):
       super(numpad, self).__init__()
       self.setupUi(self)
       self.result = None

       self.num0.clicked.connect(lambda: self.button_clicked("0"))
       self.num1.clicked.connect(lambda: self.button_clicked("1"))
       self.num2.clicked.connect(lambda: self.button_clicked("2"))
       self.num3.clicked.connect(lambda: self.button_clicked("3"))
       self.num4.clicked.connect(lambda: self.button_clicked("4"))
       self.num5.clicked.connect(lambda: self.button_clicked("5"))
       self.num6.clicked.connect(lambda: self.button_clicked("6"))
       self.num7.clicked.connect(lambda: self.button_clicked("7"))
       self.num8.clicked.connect(lambda: self.button_clicked("8"))
       self.num9.clicked.connect(lambda: self.button_clicked("9"))
       self.dot.clicked.connect(lambda: self.button_clicked("."))
       self.clearButton.clicked.connect(self.clear_text)

       self.buttonBox.accepted.connect(self.accept)
       self.buttonBox.rejected.connect(self.reject)

       self.buttonBox.accepted.connect(self.Result)

       self.entryline.setValidator(QtGui.QDoubleValidator(0.001,999.999,3))
       
       

    def button_clicked(self, number):
        global a
        global b
        a.append(number)
        b.join(a)
        res=b.join(a)
        self.entryline.setText(res)

    def clear_text(self):
        global a
        global b
        self.entryline.clear()
        a=[]
        b=""

    def get_result(self):
        result = float(self.entryline.text())


    
    def Result(self):
        super(numpad,self).exec_()
        self.clear_text()
        return self.result


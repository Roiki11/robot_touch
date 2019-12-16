#!/usr/bin/python3

import sys
import os, traceback
import time
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5 import QtWidgets as qt

class Worker(QRunnable):

    @pyqtSlot
    def run(self):



class Ui(qt.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(os.getcwd'mainwindow.ui', self)  # Load the .ui file
        self.threadpool = QThreadPool

       
        self.Load_file.clicked.connect(self.openFileDialog)

        self.show()  # Show the GUI

    def openFileDialog(self):
         fname = qt.QFileDialog.getOpenFileName(self, 'Open file', '/home')
         file = open(fname, 'r')


    
    def saveFile(self):
        name = qt.QFileDialog.getSaveFileName()
        file = open(name,'w')
        #text = 
        file.write(text)
        file.close()


def main():

    app = qt.QApplication(sys.argv)

    window = Ui()
    app.exec_()

if __name__ == '__main__':
   main()

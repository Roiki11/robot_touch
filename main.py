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

         with file:
             text=file.read
             self.programView.setText(text)

    
    def saveFileDialog(self):
        pass


app = qt.QApplication(sys.argv)

window = Ui()
app.exec_()

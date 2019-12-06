import sys
import os
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtWidgets as qt


class Ui(qt.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi(os.getcwd('mainwindow.ui', self)  # Load the .ui file

       
        self.Load_file.clicked.connect(self.openFileNameDialog)

        self.show()  # Show the GUI

    def openFileNameDialog(self):
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

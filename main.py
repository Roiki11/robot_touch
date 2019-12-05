import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QObject, pyqtSlot


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('/home/joonas/Desktop/Robot_touch/mainwindow.ui',
                   self)  # Load the .ui file

       
        self.Load_file.clicked.connect(self.openFileNameDialog)

        self.show()  # Show the GUI

    def openFileNameDialog(self):
         fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
         file = open(fname, 'r')

         with file:
             text=file.read
             self.programView.setText(text)

    
    def saveFileDialog(self):
        pass


app = QtWidgets.QApplication(sys.argv)

window = Ui()
app.exec_()

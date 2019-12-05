import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QObject, pyqtSlot


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('/home/joonas/Desktop/Robot_touch/mainwindow.ui',
                   self)  # Load the .ui file

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        save_file = QtWidgets.QPushButton(save_file)
        load_file = QtWidgets.QPushButton(load_file)
        save_file.clicked.connect(self.saveFileDialog)
        load_file.clicked.connect(self.openFileNameDialog)

        self.show()  # Show the GUI

    def openFileNameDialog(self):
        filename, filter = QtGui.QFileDialog.GetOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.txt')
        from os.path import isfile

     if isfile(self.filename):
         text = open(self.filename)
         self.QtWidgets.PlainTextExit.setText(text)

    def saveFileDialog(self):
        pass


app = QtWidgets.QApplication(sys.argv)

window = Ui()
app.exec_()

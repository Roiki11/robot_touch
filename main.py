#!/usr/bin/python3

import sys
import os, traceback
import time
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5 import QtWidgets as qt
from PyQt5.Qsci import QsciScintilla

from .move import move
from .kinematics import kinematics
from .communications import communications
from .calibration import calibration

class Worker(QRunnable):
     def __init__(self, fn, *args, **kwargs):
             super(Worker, self).__init__()

             # Store constructor arguments (re-used for processing)
             self.fn = fn
             self.args = args
             self.kwargs = kwargs
             self.signals = WorkerSignals()

             # Add the callback to our kwargs
             self.kwargs['progress_callback'] = self.signals.progress

     def run(self):
            pass



class Ui(qt.QMainWindow):

    def openFileDialog(self):
        fname = qt.QFileDialog.getOpenFileName(self, 'Open file', '/Desktop')
        if fname:
            f = open(fname[0], 'r')
            for line in f:
                self.programView.addItem(line)



    def saveFile(self):
        fname = qt.QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
        if fname:
            file = open(fname[0],'w')
            items=[]
            for index in range(self.programView.count()):
                items.append(self.programView.item(index))

            for item in items:
                file.write(item.text())
        file.close()

    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        ui_file = os.path.join(sys.path[0], 'mainwindow.ui')
        uic.loadUi(ui_file, self)  # Load the .ui file
        self.threadpool = QThreadPool

        
        self.load_file.clicked.connect(self.openFileDialog)
        self.save_file.clicked.connect(self.saveFile)

        #self.jog1pos.clicked.connect(move.)

        self.jog1neg.clicked.connect(move.jogNeg(J1))
        self.jog2neg.clicked.connect(move.jogNeg(J2))
        self.jog3neg.clicked.connect(move.jogNeg(J3))
        self.jog4neg.clicked.connect(move.jogNeg(J4))
        self.jog5neg.clicked.connect(move.jogNeg(J5))
        self.jog6neg.clicked.connect(move.jogNeg(J6))

        self.show()  # Show the GUI



def main():

    app = qt.QApplication(sys.argv)

    window = Ui()
    app.exec_()

if __name__ == '__main__':
   main()

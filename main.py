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
from .file_handling import file

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

    def set_parameter(self, param):
        if param == alpha1:
            global DHa1 = self.dh_alpha1.text()
        elif param == alpha2:
            global DHa2 = self.dh_alpha2.text()
        elif param == alpha3:
            global DHa3 = self.dh_alpha1.text()
        elif param == alpha4:
            global DHa4 = self.dh_alpha1.text()
        elif param == alpha5:
            global DHa5 = self.dh_alpha1.text()
        elif param == alpha6:
            global DHa6 = self.dh_alpha1.text()
        elif param == a1:
            global DHr1 = self.dh_a1.text()
        elif param == a2:
            global DHr2 = self.dh_a2.text()
        elif param == a3:
            global DHr3 = self.dh_a3.text()
        elif param == a4:
            global DHr4 = self.dh_a4.text()
        elif param == a5:
            global DHr5 = self.dh_a5.text()
        elif param == a6:
            global DHr6 = self.dh_a6.text()
        elif param == d1:
            global DHd1 = self.dh_d1.text()
        elif param == d2:
            global DHd2 = self.dh_d2.text()
        elif param == d3:
            global DHd3 = self.dh_d3.text()
        elif param == d4:
            global DHd4 = self.dh_d4.text()
        elif param == d5:
            global DHd5 = self.dh_d5.text()
        elif param == d6:
            global DHd6 = self.dh_d6.text()
        elif param == theta1:
            global DHt1 = self.dh_theta1.text()
        elif param == theta2:
            global DHt2 = self.dh_theta2.text()
        elif param == theta3:
            global DHt3 = self.dh_theta3.text()
        elif param == theta4:
            global DHt4 = self.dh_theta4.text()
        elif param == theta5:
            global DHt5 = self.dh_theta5.text()
        elif param == theta6:
            global DHt6 = self.dh_theta6.text()





    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        ui_file = os.path.join(sys.path[0], 'mainwindow.ui')
        uic.loadUi(ui_file, self)  # Load the .ui file
        self.threadpool = QThreadPool

        ## File handling buttons ##
        self.load_file.clicked.connect(file.loadFile)
        self.save_file.clicked.connect(file.saveFile)
        self.new_File.clicked.connect(file.newFile)


        ##Jogging Buttons##
        #self.jog1pos.clicked.connect(move.)

        self.jog1neg.clicked.connect(move.jogNeg(J1))
        self.jog2neg.clicked.connect(move.jogNeg(J2))
        self.jog3neg.clicked.connect(move.jogNeg(J3))
        self.jog4neg.clicked.connect(move.jogNeg(J4))
        self.jog5neg.clicked.connect(move.jogNeg(J5))
        self.jog6neg.clicked.connect(move.jogNeg(J6))

        self.dh_alpha1.textChanged.connect(set_parameter(alpha1))
        self.dh_alpha1.setValidator(QtGui.QDoubleValidator.StandardNotation())

        self.show()  # Show the GUI



def main():

    app = qt.QApplication(sys.argv)

    window = Ui()
    app.exec_()

if __name__ == '__main__':
   main()

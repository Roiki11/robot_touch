#!/usr/bin/python3

import sys
import os, traceback
import time
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5 import QtWidgets as qt
from PyQt5.Qsci import QsciScintilla

#from move import move
#from kinematics import kinematics
#from communications import communications
#from calibration import calibration
from file_handling import fileHandling
from keypad import numpad

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

    def numpadDialog(self):
        w=InputNumPad()
        Value = w.getResults()





    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        ui_file = os.path.join(sys.path[0], 'mainwindow.ui')
        uic.loadUi(ui_file, self)  # Load the .ui file
        self.threadpool = QThreadPool

        ## File handling buttons ##
        self.load_file.clicked.connect(fileHandling.loadFile)
        self.save_file.clicked.connect(fileHandling.saveFile)
        self.new_File.clicked.connect(fileHandling.newFile)

        self.getvalue_button.clicked.connect(numpadDialog)


        ##Jogging Buttons##
        #self.jog1pos.clicked.connect(move.jogJoint(J1, 1)
        #self.jog1pos.clicked.connect(move.jogJoint(J2, 1)
        #self.jog1pos.clicked.connect(move.jogJoint(J3, 1)
        #self.jog1pos.clicked.connect(move.jogJoint(J4, 1)
        #self.jog1pos.clicked.connect(move.jogJoint(J5, 1)
        #self.jog1pos.clicked.connect(move.jogJoint(J6, 1)

        #self.jog1neg.clicked.connect(move.jogJoint(J1, 0))
        #self.jog2neg.clicked.connect(move.jogJoint(J2, 0))
        #self.jog3neg.clicked.connect(move.jogJoint(J3, 0))
        #self.jog4neg.clicked.connect(move.jogJoint(J4, 0))
        #self.jog5neg.clicked.connect(move.jogJoint(J5, 0))
        #self.jog6neg.clicked.connect(move.jogJoint(J6, 0))


        #DH parameter value field changes##
        self.dh_alpha1.textChanged.connect(set_parameter(alpha1))
        self.dh_alpha1.setValidator(QtGui.QDoubleValidator.StandardNotation())

        self.show()  # Show the GUI



def main():

    app = qt.QApplication(sys.argv)

    window = Ui()
    app.exec_()

if __name__ == '__main__':
   main()

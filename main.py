#!/usr/bin/python3import sys
import os, traceback
import time
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from queue import Queue
import rospy

from move import move
#from kinematics import kinematics
#from communications import communications
#from calibration import calibration
from file_handling import fileHandling
from keypad.numpad import numpad

program_queue = Queue()
robot_paused = False
robot_stopped = False
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    running = pyqtSignal(bool)
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
     @pyqtSlot
     def run(self):
        try:
            result = self.fn(
                *self.args, **self.kwargs,
                status=self.signals.status,
                progress=self.signals.progress
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class Ui(QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        ui_file = os.path.join(sys.path[0], 'mainwindow.ui')
        uic.loadUi(ui_file, self)  # Load the .ui file
        self.threadpool = QThreadPool()

        ## File handling buttons ##
        self.load_file.clicked.connect(fileHandling.loadFile)
        self.save_file.clicked.connect(fileHandling.saveFile)
        self.new_File.clicked.connect(fileHandling.newFile)

        self.getvalue_button.clicked.connect(self.launchDialog)


        ##Jogging Buttons##
        #self.jog1pos.clicked.connect(lambda: move.jogJoint(J1, 1)
        #self.jog2pos.clicked.connect(lambda:move.jogJoint(J2, 1)
        #self.jog3pos.clicked.connect(lambda:move.jogJoint(J3, 1)
        #self.jog4pos.clicked.connect(lambda:move.jogJoint(J4, 1)
        #self.jog5pos.clicked.connect(lambda:move.jogJoint(J5, 1)
        #self.jog6pos.clicked.connect(lambda:move.jogJoint(J6, 1)

        #self.jog1neg.clicked.connect(lambda:move.jogJoint(J1, 0))
        #self.jog2neg.clicked.connect(lambda:move.jogJoint(J2, 0))
        #self.jog3neg.clicked.connect(lambda:move.jogJoint(J3, 0))
        #self.jog4neg.clicked.connect(lambda:move.jogJoint(J4, 0))
        #self.jog5neg.clicked.connect(lambda:move.jogJoint(J5, 0))
        #self.jog6neg.clicked.connect(lambda:move.jogJoint(J6, 0))

        self.jog_increment001.clicked.connect(lambda: self.jogIncrementSelection(0.01))
        self.jog_increment01.clicked.connect(lambda: self.jogIncrementSelection(0.01))
        self.jog_increment1.clicked.connect(lambda: self.jogIncrementSelection(1))
        elf.jog_increment10.clicked.connect(lambda: self.jogIncrementSelection(10))

        self.show()  # Show the GUI
    def launchDialog(self):
        dlg = numpad()
        if dlg.exec():
            value = numpad.result(self)
            self.jogDistanceBox.setValue(float(value))

    def jogIncrementSelection(self, number):
        jog_increment = number
        if number == 0.01:
            self.jog_increment001.setStyleSheet("backround-color: blue")
            self.jog_increment01.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment1.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment10.setStyleSheet("background-color: rgb(186, 189, 182)")
        elif number == 0.1:
            self.jog_increment001.setStyleSheet("backround-color: rgb(186, 189, 182)")
            self.jog_increment01.setStyleSheet("background-color: blue")
            self.jog_increment1.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment10.setStyleSheet("background-color: rgb(186, 189, 182)")
        elif number == 1:
            self.jog_increment001.setStyleSheet("backround-color: rgb(186, 189, 182)")
            self.jog_increment01.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment1.setStyleSheet("background-color: blue")
            self.jog_increment10.setStyleSheet("background-color: rgb(186, 189, 182)")
        elif number == 10:
            self.jog_increment001.setStyleSheet("backround-color: rgb(186, 189, 182)")
            self.jog_increment01.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment1.setStyleSheet("background-color: rgb(186, 189, 182)")
            self.jog_increment10.setStyleSheet("background-color: rgb(186, 189, 182)")

    def runProgramThread(self):
        global program_queue
        while self.running:
            if not program_queue.empty():
               program_line = program_queue.get()
               move.codeParser(program_line)
               WorkerSignals.running.emit()

    def start_program(self):
        global open_program
        global program_queue
        for items in open_program:
            program_queue.put()

    def pause__resume_movement(self):
        global robot_paused
        if robot_paused is False:
            robot.pause_movement
            robot_paused = True
            rospy.loginfo("Robot Movement Paused")
        else:
            robot.resume_movement
            robot_paused = False
            rospy.loginfo("Robot movement Resumed")

    def stop_movement(self):
        robot.stop_movement
        rospy.loginfo("Robot movement Stopped")

    def teach_position(self):
        position = robot.get.current_pose()
    



####################

app = QApplication(sys.argv)
window = Ui()
worker=Worker(self.runProgramThread)

self.threadpool.start(worker)
rospy.init_node("robot_program_node")
app.exec_()

#!/usr/bin/python
import os, traceback
import time
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
#from queue import Queue


#from move import Move, Move_Signals
#from calibration import calibration
from keypad.numpad import numpad
#from circle_window import circle_window
#from Rviz.Rviz import Rviz
#from ros_publsher_subsriber import Ros_talkers

#program_queue = Queue()
#robot_paused = False
#robot_stopped = False
#jog_increment = 1

"""
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    running = pyqtSignal()
    is_paused = pyqtSignal()
    
    
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
     @pyqtSlot()
     def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
"""
class Ui(QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        ui_file = os.path.join(sys.path[0], 'mainwindow.ui')
        uic.loadUi(ui_file, self)  # Load the .ui file
        self.show()
        #self.threadpool = QThreadPool()

        self.numpad = numpad()
        #self.Ros_talkers = Ros_talkers()
        #self.Move_Signals = Move_Signals()
        

        ## File handling buttons ##
        self.load_file.clicked.connect(self.loadFile)
        self.save_file.clicked.connect(self.saveFile)
        self.new_File.clicked.connect(self.newFile)


        #Key dialog for jog distance
        self.getvalue_button.clicked.connect(self.launchKeypadDialog)

        #loop program signal.
        #self.Move_Signals.connect(self.start_program)

       # self.circTeachButton.clicked.connect(self.launchCircleDialog)

        #self.Ros_talkers.encoder_feedback.connect(self.update_encoder_displays)

    """        ##Jogging Buttons##
        self.jog1pos.clicked.connect(lambda:move.jogJoint(1, 1))
        self.jog2pos.clicked.connect(lambda:move.jogJoint(2, 1))
        self.jog3pos.clicked.connect(lambda:move.jogJoint(3, 1))
        self.jog4pos.clicked.connect(lambda:move.jogJoint(4, 1))
        self.jog5pos.clicked.connect(lambda:move.jogJoint(5, 1))
        self.jog6pos.clicked.connect(lambda:move.jogJoint(6, 1))

        self.jog1neg.clicked.connect(lambda:move.jogJoint(1, 0))
        self.jog2neg.clicked.connect(lambda:move.jogJoint(2, 0))
        self.jog3neg.clicked.connect(lambda:move.jogJoint(3, 0))
        self.jog4neg.clicked.connect(lambda:move.jogJoint(4, 0))
        self.jog5neg.clicked.connect(lambda:move.jogJoint(5, 0))
        self.jog6neg.clicked.connect(lambda:move.jogJoint(6, 0))

        self.jog_increment001.clicked.connect(lambda: self.jogIncrementSelection(0.01))
        self.jog_increment01.clicked.connect(lambda: self.jogIncrementSelection(0.01))
        self.jog_increment1.clicked.connect(lambda: self.jogIncrementSelection(1))
        self.jog_increment10.clicked.connect(lambda: self.jogIncrementSelection(10))


        def teach_joint_position(self):

            position = Move.robot.get_current_joint_states()


        def teach_ptp_position(self):
            position = Move.robot.get.current_pose()

        def teach_lin_position(self):
            position = Move.robot.get.current_pose()

        def teach_circ_position(self):
            position = Move.robot.get.current_pose()
   """
    
    @pyqtSlot(result=QVariant)
    def update_encoder_displays(self, data):
        self.j1pos.update(data[0])
        self.j2pos.update(data[1])
        self.j3pos.update(data[2])
        self.j4pos.update(data[3])
        self.j5pos.update(data[4])
        self.j6pos.update(data[5])

    def launchKeypadDialog(self):
        result = self.numpad.exec_()
        if result:
            a=str(result)
            sys.stderr.write(a)
            #self.jogDistanceBox.value(result)
        
    def launchCircleDialog(self):
        circle_window.show()

    def jogIncrementSelection(self, number):
        global jog_increment

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
            WorkerSignals.is_paused.emit()
            rospy.loginfo("Robot Movement Paused")
        else:
            robot.resume_movement
            robot_paused = False
            WorkerSignals.running.emit()
            rospy.loginfo("Robot movement Resumed")

    def stop_movement(self):
        robot.stop_movement
        rospy.loginfo("Robot movement Stopped")
        WorkerSignals.finished.emit()
    

    def clear_program(self):
        global open_program
        open_program = []
        self.programView.clear()



    def loadFile(self):
        global open_program
        global open_file
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/Desktop',"Text Files (*.txt)")
        if fname:
            open_file = fname
            f = open(fname[0], 'r')
            open_program =[]
            for line in f:
                self.programView.addItem(line)
                open_program.append(line)



    def saveFile(self):
        global open_file
        global open_program

        if open_file:
            file = open(open_file[0], 'w')
            for item in open_program:
                file.write(item.text())
            file.close()
        else:
                open_file = QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
                if open_file:
                    file = open(open_file[0],'w')
                    for item in open_program:
                        file.write(item.text())
                    file.close()

    def newFile(self):
        global open_file

        open_file = QFileDialog.getSaveFileName(self, 'Save File as', '/Desktop', '*.txt')
        if open_file:
            file = open(open_file[0],'w')
            text = '## Program Start##'
            file.write(text)
            self.programView.addItem(text)
    



####################

app = QApplication(sys.argv)
window = Ui()
#worker1 = Worker(self.runProgramThread)
#worker2 = Worker(Ros_talkers.listener)
#self.threadpool.start(worker1)
#self.threadpool.start(worker2)
#rospy.init_node("robot_program_node")
app.exec_()



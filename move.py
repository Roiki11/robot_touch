#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Point, Quaternion
from pilz_robot_programming.robot import *
import math 
from pyparsing import *
from PyQt5.QtCore import pyqtSignal, QObject

__REQUIRED_API_VERSION__ = "1"  # API version
__ROBOT_VELOCITY__ = 1        # velocity of the robot

robot = Robot(__REQUIRED_API_VERSION__)
robot_sequence = Sequence()


"""
Moving and robot program related functions are located here. 

    Robot code is in format : 
    PTP X111.111 Y111.111 Z111.111 qX qY qZ qW VSCALE RELATIVE
    N1 PTP X120.21 Y7.213 Z0.0123 qx1.00230 qy0.00293 qz1 qw0 RELATIVE
    N2 START_SQ 
    N342 SERVO 1 S160
    N32 SET_FRAME prbt_base
    N2 PTP J1:123.23 J2:12.221 J3:-231.321 J4:12.030 J5:95.33 J6:0.23 RELATIVE
    N12 CIRC X0 Y0 Z0 iX0 iY0 iZ0


Where:
PTP = the movement type of the PTP, LIN CIRC
XYZ = xyz co-ordinate point, units in mm, converted to meters in code which the API expects. Done this way to make code more similar to GCODE
qXqYqZ =  Rotation as quaternion
RPY = rotation in degrees, converted to radians in code. Done this way because radians are harder to visualize for people.
VSCALE = velocity scaling as set in pilz programming API. given as a fraction of 1 where 1 is 100%, so 0.2 is 20%
RELATIVE = Word to change the command relative to current robot position

in CIRC command the first point is the robot start point, the first point is the end point and second point is the interim. Points are in cartesian space.

START_SQ = Defines the start of sequence move
END_SQ =  ends the sequence move block and execute it.

SET_FRAME = Sets the reference frame of the move.

DI_ON = Sets Digital input on.

DI_OFF = Sets Digital INput off.

SERVO = Servo Angle command.

Comments marked with # are ignored.

START_PROGRAM and END_PROGRAM are just for logging.

CALL_PROGRAM calls for a named program and loads it into the input queue. Need to figure this one out.

REPEAT called at the end of program starts the execution loop again. Need to figure this one out too.

N numbers are line numbers and are ignored. Made this way so reading and navigating large code files becomes a little easier. Need to make functions to generate and update these.

The parse_string function returns list object that can be queried with .get("<key>") function, this returns the value if present, or None. Read more on pyparsing for more info.

"""
class Move_Signals(QObject):
    loop_program = pyqtSignal()
class Move:
    def __init__(self):
        signals = Move_Signals()    

    def jogJoints(self, joint, direction): #function to jog a single joint with an increment

        J1 = 0.0
        J2 = 0.0
        J3 = 0.0
        J4 = 0.0
        J5 = 0.0
        J6 = 0.0

        if direction is 1:
            a = math.radians(jog_increment)
        else:
            a = (math.radians(jog_increment) * -1)

        if joint == 1:
            J1 = a
        elif joint == 2:
            J2 = a
        elif joint == 3:
            J3 = a
        elif joint == 4:
            J4 = a
        elif joint == 5:
            J5 = a
        elif joint == 6:
            J6 = a 

        robot.move(Ptp(goal=[J1, J2, J3, J4, J5, J6], relative = True))

    def cartesianJog(self, axis):

        params= {"relative":True}
        pose=Pose()
        step = self.jogDistanceBox.value() / 100
        step2 = math.radians(jog_increment)
        if axis is x or y or z:
            pose.position.axis = step/100

        if axis is r:
            quat = robot.from_euler(step2, 0, 0)
        elif axis is p:
            quat = robot.from_euler(0, step2, 0)
        elif axis is y:
            quat = robot.from_euler(0,0,step2)

        
        pose.qorientation = quat

        self.execute(Ptp, pose, params)

    def teach_position(self):
        position = robot.get.current_pose()





    def parse_string(input):
        
        #Function to parse the input string from the code file. 
        number = Word(nums+'-.').setParseAction(lambda t: float(t[0]))
        N = Word(alphas+nums)
        command = Word(alphas + '_')
        J1 = Optional(Suppress('J1:') + number)
        J2 = Optional(Suppress('J2:') + number)
        J3 = Optional(Suppress('J3:') + number)
        J4 = Optional(Suppress('J4:') + number)
        J5 = Optional(Suppress('J5:') + number)
        J6 = Optional(Suppress('J6:') + number)
        X = Optional(Suppress('X') + number)
        Y = Optional(Suppress('Y') + number)
        Z = Optional(Suppress('Z') + number)
        iX = Optional(Suppress('iX') + number)
        iY = Optional(Suppress('iY') + number)
        iZ = Optional(Suppress('iZ') + number)
        R = Optional(Suppress('Z') + number)
        P = Optional(Suppress('P') + number)
        Y = Optional(Suppress('Y') + number)
        qX = Optional(Suppress('qx') + number)
        qY = Optional(Suppress('qy') + number)
        qZ = Optional(Suppress('qz') + number)
        qW = Optional(Suppress('qw') + number)
        blend_radi = Optional(Suppress('RAD') + number)
        relative = Optional(Word('RELATIVE'))
        vscale = Optional(Suppress('V') + number)
        seconds = Optional(Suppress('S') + number)
        start_sq = Optional(Word("START_SQ"))
        end_sq = Optional(Word("END_SQ"))
        servo_number = Optional(Word(nums))
        servo_degree = Optional(Suppress('S') + number)
        robot_frame = Optional(Word(alphanums + "_"))
        
        line = (Suppress(N)
                +command("command")
                +J1("J1")
                +J2("J2")
                +J3("J3")
                +J4("J4")
                +J5("J5")
                +J6("J6")
                +X("X")
                +Y("Y")
                +Z("Z")
                +X("iX")
                +Y("iY")
                +Z("iZ")
                +qX("qX")
                +qY("qY")
                +qZ("qZ")
                +qW("qW")
                +R("R")
                +P("P")
                +Y("Y")
                +blend_radi("RAD")
                +relative("relative")
                +vscale("vscale")
                +seconds("seconds")
                +servo_number("servo_number")
                +servo_degree("servo_degree")
                +robot_frame("robot_frame"))
        
        if input.find("#") is 0:
            return None
        else:
            codelist = line.parseString(input)
            return codelist

    def codeParser(self, codestring): # parse a line of code, get the command word and get the correct funtion to execute.
        parsed_code = parse_string(codestring)
        if parsed_code is not None:
            command = parsed_code.get("command")
            program = self.switcher(command)
            program(self, parsed_code, command)
        #Find the command and choose the execution method
    

    def switcher(self, command): #Switcher function to return the desired command function name.
        switcher = {
            "PTP": Ptp_lin,
            "LIN": Ptp_lin,
            "CIRC": Circ,
            "SERVO": servo,
            "GRIPPER": gripper,
            "SET_FRAME": set_frame,
            "WAIT": wait,
            "START_SQ": start_sq,
            "END_SQ": end_sq,
            "START_PROGRAM": start_program,
            "END_PROGRAM": start_program,
            "CALL_PROGRAM": call_program,
            "REPEAT": repeat_program
        }
        func = switcher.get(command, lambda: "Unknown command")
        return func()

        def execute(self, command, pose, params, center=None): #execute the desired command, if sequence is active, append it to sequence instead. A loop to try again if the planner is busy.
            global sequence_active
            global robot_sequence # check if moves are part of a sequence or not. Try execution 10 times with .5 second interval if API returns MoveAlreadyRunning error.
            i = 0
            while i < 10:
                i += 1
                try:
                    if center is not None:
                        if sequence_active is True:
                            robot_sequence.append(Circ(goal=pose, interim=center, **params))
                        else:
                             robot.move(Circ(goal=pose, interim=center, **params))
                    elif command == "PTP":
                            if sequence_active is True:
                                robot_sequence.append(Ptp(goal=pose, **params))
                            else:
                                robot.move(Ptp(goal=pose, **params))
                    elif command == "LIN":
                            if sequence_active is True:
                                  robot_sequence.append(Lin(goal=pose, **params))
                            else:
                                robot.move(Lin(goal=pose, **params))

                except RobotMoveAlreadyRunningError:
                    rospy.loginfo("Robot move already in progress")
                    time.sleep(0.5)
                    continue
                
                except RobotMoveFailed:
                    rospy.loginfo("Robot move failed")
                    raise           

    def Ptp_lin (self, parsed_code, command):
        global active_frame
        param_dict=dict()
        pose=Pose()

        X = float(str(parsed_code.get("X")).strip("[]")) / 100
        Y = float(str(parsed_code.get("Y")).strip("[]")) / 100
        Z = float(str(parsed_code.get("Z")).strip("[]")) / 100
        qX = float(str(parsed_code.get("qX")).strip("[]"))
        qY = float(str(parsed_code.get("qY")).strip("[]"))
        qZ = float(str(parsed_code.get("qZ")).strip("[]")) 
        qW = float(str(parsed_code.get("qW")).strip("[]")) 
        Relative = parsed_code.get("relative")
        Vscale = str(parsed_code.get("vscale")).strip("[]")

        if X is None: #See if we have Joint or Cartesian space by looking if X coordinate returns None, if yes get Joint values and append to list.
            pose = []
            J1 = float(str(parsed_code.get("X")).strip("[]"))
            J2 = float(str(parsed_code.get("X")).strip("[]"))
            J3 = float(str(parsed_code.get("X")).strip("[]"))
            J4 = float(str(parsed_code.get("X")).strip("[]"))
            J5 = float(str(parsed_code.get("X")).strip("[]"))
            J6 = float(str(parsed_code.get("X")).strip("[]"))

            pose.append(math.radians(J1))
            pose.append(math.radians(J2))
            pose.append(math.radians(J3))
            pose.append(math.radians(J4))
            pose.append(math.radians(J5))
            pose.append(math.radians(J6))
        else:
            pose.position = Point(X, Y, Z)
            if qX is not None:
                pose.orientation = Quaternion(qX, qY, qZ, qW)
                if qX is None and R is not None:

                    R = float(str(parsed_code.get("R")).strip("[]"))
                    P = float(str(parsed_code.get("P")).strip("[]"))
                    Y = float(str(parsed_code.get("Y")).strip("[]"))

                pose.orientation = robot.from_euler(math.radians(R), math.radians(P), math.radians(Y))

        if Relative is not None:
            param_dict['relative'] = True

        if Vscale is not None:
            param_dict['vel_scale'] = float(Vscale)
        
        if active_frame is not "prbt_base":
            param_dict['reference_frame'] = active_frame

        self.execute(command, pose, param_dict)


    def Circ(self, parsed_code, command): # Circle command execution
        param_dict=dict()
        endPose=Pose()
        intPose=Pose()

        X = float(str(parsed_code.get("X")).strip("[]")) / 100
        Y = float(str(parsed_code.get("Y")).strip("[]")) / 100
        Z = float(str(parsed_code.get("Z")).strip("[]")) / 100
        iX = float(str(parsed_code.get("iX")).strip("[]")) / 100
        iY = float(str(parsed_code.get("iY")).strip("[]")) / 100
        iZ = float(str(parsed_code.get("iZ")).strip("[]")) / 100
        Relative = parsed_code.get("relative")
        Vscale = str(parsed_code.get("vscale")).strip("[]")

        endPose.position = Point(X, Y, Z)
        intPose.position = Point(iX, iY, iZ)

        param_dict['interim'] = intPose

        if Relative is not None:
            param_dict['relative'] = True

        if Vscale is not None:
            param_dict['vel_scale'] = float(Vscale)
        
        if active_frame is not "prbt_base":
            param_dict['reference_frame'] = active_frame

        self.execute(command, pose, param_dict)


    def servo(self, param): # Servo command execution
        pass

    def gripper(self, param): #Gripper command execution
        pass

    def set_frame(self, param): #Define the active robot frame that's appended to movement commands
        global active_frame
        frame = str(param.get("robot_frame"))
        active_frame = frame

    def wait(self, param): #A simple command to wait X seconds.
        time = str(param.get("seconds")).strip("[]")
        time.sleep(float(time))
    
    def start_sq(self): #start the sequence and initialize a new sequence
        global sequence_active
        global robot_sequence
        sequence_active = True
        robot_sequence = Sequence()
    
    def end_sq(self): #end the sequence move and execute it.
        global sequence_active
        global robot_sequence
        sequence_active = False
        robot.move(robot_sequence)

    def start_program(self):
        rospy.loginfo("Starting program execution")

    def end_program(self):
        rospy.loginfo("Program finished")

    def call_program(self):
        rospy.loginfo("Calling program")
        #code here that calls a specic program,

    def repeat_program(self):
        self.signals.loop_program.emit()
        rospy.loginfo("Repeating program")
        #Code here that starts the program execution all over again.


        
        
    




    

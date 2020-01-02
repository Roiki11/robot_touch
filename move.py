#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Point
from pilz_robot_programming.robot import *
import math 
from pyparsing import *

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


Where:
PTP = the movement type of the PTP, LIN CIRC
XYZ = xyz co-ordinate point, units in mm
qXqYqZ =  Rotation as quaternion
RPY = rotation in degrees
VSCALE = velocity scaling as set in pilz programming API.
RELATIVE = Word to change the command relative to current robot position

START_SQ = Defines the start of sequence move
END_SQ =  ends the sequence move block and execute it.

SET_FRAME = Sets the reference frame of the move.

DI_ON = Sets Digital input on.

DI_OFF = Sets Digital INput off.

SERVO = Servo Angle command.

Comments marked with # are ignored.

N numbers are line numbers and are ignored.

The parse_string function returns list object that can be queried with .get("<key>") function, this returns the value if present, or None.

"""
class move:

    def jogJoints(self, joint, amount): #function to jog a single joint with an increment

        J1 = 0.0
        J2 = 0.0
        J3 = 0.0
        J4 = 0.0
        J5 = 0.0
        J6 = 0.0

        if joint == 1:
            J1 = amount
        elif joint == 2:
            J2 = amount
        elif joint == 3:
            J3 = amount
        elif joint == 4:
            J4 = amount
        elif joint == 5:
            J5 = amount
        elif joint == 6:
            J6 = amount 

        robot.move(Ptp(goal=[J1, J2, J3, J4, J5, J6], relative = True))



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
            "PTP": Ptp,
            "PTPTJ": ptpj,
            "LIN": Lin,
            "CIRC": Circ,
            "SERVO": servo,
            "GRIPPER": gripper,
            "SET_FRAME": set_frame,
            "WAIT": wait,
            "START_SQ": start_sq,
            "END_SQ": end_sq
        }
        func = switcher.get(command, lambda: "Unknown command")
        return func()

    def Ptp(self, param, command):
        global active_frame
        param_dict=dict()
        pose=Pose()

        X = str(param.get("X")).strip("[]") / 100
        Y = str(param.get("Y")).strip("[]") / 100
        Z = str(param.get("Z")).strip("[]") / 100
        qX = str(param.get("qX")).strip("[]")
        qY = str(param.get("qY")).strip("[]")
        qZ = str(param.get("qZ")).strip("[]")
        qW = str(param.get("qW")).strip("[]")
        Relative = param.get("relative")
        Vscale = str(param.get("vscale")).strip("[]")

        if X is None: #See if we have Joint or Cartesian space by looking if X coordinate returns None, if yes get Joint values and append to list.
            pose = []
            J1: float(str(param.get("X")).strip("[]"))
            J2: float(str(param.get("X")).strip("[]"))
            J3: float(str(param.get("X")).strip("[]"))
            J4: float(str(param.get("X")).strip("[]"))
            J5: float(str(param.get("X")).strip("[]"))
            J6: float(str(param.get("X")).strip("[]"))

            pose.append(J1)
            pose.append(J2)
            pose.append(J3)
            pose.append(J4)
            pose.append(J5)
            pose.append(J6)
        else:

            pose.position.x = float(X)
            pose.position.y = float(Y)
            pose.position.z = float(Z)

            if qX is not None:
                pose.orientation.x = float(qX)
                pose.orientation.y = float(qY)
                pose.orientation.z = float(qZ)
                pose.orientation.w = float(qW)
            if qX is None and R is not None:

                R = float(str(param.get("R")).strip("[]"))
                P = float(str(param.get("P")).strip("[]"))
                Y = float(str(param.get("Y")).strip("[]"))

                pose.orientation = robot.from_euler(math.degrees(R), math.degrees(P), math.degrees(Y))

        if Relative is not None:
            param_dict['relative'] = True

        if Vscale is not None:
            param_dict['vel_scale'] = float(Vscale)
        
        if active_frame is not "prbt_base":
            param_dict['reference_frame'] = active_frame

        self.execute(command, pose, param_dict)


    def Lin(self, param): # Linear command execution

    def Circ(self, param): # Circle command execution

    def servo(self, param): # Servo command execution

    def gripper(self, param): #Gripper command execution

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
        
        
    def execute(self, command, pose, params): #execute the desired command, if sequence is active, append it to sequence instead. A loop to try again if the planner is busy.
        global sequence_active
        global robot_sequence

        if sequence_active is False: # check if moves are part of a sequence or not. Try execution 10 times with .5 second interval if API returns MoveAlreadyRunning error.
            i = 0
            while i < 10:
                i += 1
                try:
                    robot.move(command(goal=pose, **params))

                except RobotMoveAlreadyRunningError:
                    rospy.loginfo("Robot move in progress")
                    time.sleep(0.5)
                    continue
            
                except RobotMoveFailed:
                    rospy.loginfo("Robot move failed")
                    raise           
        else: 
            robot_sequence.append(command(goal=pose, **params))




    

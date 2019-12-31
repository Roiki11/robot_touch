#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Point
from pilz_robot_programming.robot import *
import math 
from pyparsing import *

__REQUIRED_API_VERSION__ = "1"  # API version
__ROBOT_VELOCITY__ = 1        # velocity of the robot

robot = Robot(__REQUIRED_API_VERSION__)

"""
Moving and robot program related functions are located here. 

    Robot code is in format : 
    PTP X111.111 Y111.111 Z111.111 qX qY qZ qW VSCALE RELATIVE
    N1 PTP X120.21 Y7.213 Z0.0123 qx1.00230 qy0.00293 qz1 qw0 RELATIVE
    N2 START_SQ 
    N342 SERVO 1 S160
    N32 SET_FRAME prbt_base
    N2 PTPJ J1:123.23 J2:12.221 J3:-231.321 J4:12.030 J5:95.33 J6:0.23 RELATIVE


Where:
PTP = the movement type of the PTP, PTPJ, LIN CIRC
XYZ = xyz co-ordinate point, mm
qXqYqZ =  Rotation as quaternion
VSCALE = velocity scaling as set in pilz programming API.
RELATIVE = Word to change the command relative to current robot position

START_SQ = Defines the start of sequence move
END_SQ =  ends the sequence move block.

SET_FRAME = Sets the reference frame of the program.

DI_ON = Sets Digital input on.

DI_OFF = Sets Digital INput off.

SERVO = Servo Angle command.

Comments marked with # are ignored.

N numbers are line numbers and are ignored

The parse_string function returns list object that can be queried with .get("<key>") function, this returns the value if present, or None.

"""
class move:

    def defjogJoints(self, joint, amount):

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
        qX = Optional(Suppress('qx') + number)
        qY = Optional(Suppress('qy') + number)
        qZ = Optional(Suppress('qz') + number)
        qW = Optional(Suppress('qw') + number)
        relative = Optional(Word('RELATIVE'))
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
                +relative("relative")
                +servo_number("servo_number")
                +servo_degree("servo_degree")
                +robot_frame("robot_frame"))
        
        codelist = line.parseString(input)
    
    return codelist

    def codeParser(self, codestring):
        parsed_code = parse_string(codestring)

        command = parsed_code.get("command")

        #Find the command and choose the execution method

               
        




    

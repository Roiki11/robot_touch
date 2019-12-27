#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Point
from pilz_robot_programming.robot import *
import math 
import re

__REQUIRED_API_VERSION__ = "1"  # API version
__ROBOT_VELOCITY__ = 1        # velocity of the robot

robot = Robot(__REQUIRED_API_VERSION__)

"""
Moving and robot program related functions are located here. 

    Robot code is in format : MOVEL X111.111 Y111.111 Z111.111 qX qY qZ qW VSCALE ABS

Where:
MOVEL = the movement type of the move, linear, joint or circular
XYZ = xyz co-ordinate point, mm
qXqYqZ Rotation as quaternion
VSCALE = velocity scaling as set in pilz programming API.
ABS = define command as absolute position. Default is relative.

START_SQ = Defines the start of sequence move
END_SQ ends the sequence move block.

SET_FRAME = Sets the reference frame of the program.
SET_TCP = Sets the TCP

DI_ON = Sets Digital input on.

DI_OFF = Sets Digital INput off.

SERVO = Servo Angle command.

Comments marked with # are ignored.

"""
class move:

    def defjogJoints(self, joint, amount):

        J1 = 0
        J2= 0
        J3 = 0
        J4 = 0
        J5 = 0
        J6 = 0

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



    def parseProgramRow(self, command):
        
        x = re.search("X(-?\d+\.?\d*)", command)
        y = re.search("Y(\w*...\d)", command)
        z = re.search("Z(\w*...\d)", command)
        qx = re.search("qX(-?\d+\.?\d*)", command)
        qy = re.search("qY(-?\d+\.?\d*)", command)
        qz = re.search("qZ(-?\d+\.?\d*)", command)
        qw = re.search("qY(-?\d+\.?\d*)", command)
        vscale = re.search("VSCALE(-?\d+\.?\d*", command)
        absolute = re.search("ABS(-?\d+\.?\d*)", command)



       
        




    

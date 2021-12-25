#!/usr/bin/env python

from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from IKLib import *

from manipulator.srv import ValidateIKNode, ValidateIKNodeResponse, IKTask, IKTaskResponse
import rospy
import std_msgs.msg
from manipulator.msg import Point

def handleInverseKinematicsMsg(req):
    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now() # Note you need to call rospy.init_node() before this will work
    X = [0]
    Y = [0]
    Z = [0]
    point = Point(X, Y, Z)
    return IKTaskResponse(header, 11, [point]);

def handleInitMsg(req):
    return ValidateIKNodeResponse(True)

def IKServer():
    rospy.init_node('IKNode')
    s = rospy.Service('IKNodeValidator', ValidateIKNode, handleInitMsg)
    print("Ready to setup")

    IKMsgService = rospy.Service('IKTask', IKTask, handleInverseKinematicsMsg)
    print("IKTask performed!")
    rospy.spin()

if __name__ == "__main__":
    IKServer()

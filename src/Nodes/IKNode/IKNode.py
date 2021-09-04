#!/usr/bin/env python

from __future__ import print_function
from IKLib import *

from manipulator.srv import ValidateIKNode, ValidateIKNodeResponse
import rospy

def handleInverseKinematicsMsg(req):
    return ValidateIKNodeResponse(True)

def IKServer():
    rospy.init_node('IKNode')
    s = rospy.Service('IKNodeValidator', ValidateIKNode, handleInverseKinematicsMsg)
    print("Ready to setup")
    rospy.spin()

if __name__ == "__main__":
    IKServer()

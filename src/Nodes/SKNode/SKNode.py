#!/usr/bin/env python

from __future__ import print_function

from manipulator.srv import ValidateSKNode, ValidateSKNodeResponse
import rospy

def handleSimpleKinameticsMsg(req):
    return ValidateSKNodeResponse(True)

def SKServer():
    rospy.init_node('SKNode')
    s = rospy.Service('SKNodeValidator', ValidateSKNode, handleSimpleKinameticsMsg)
    print("Ready to setup")
    rospy.spin()

if __name__ == "__main__":
    SKServer()

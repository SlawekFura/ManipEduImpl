#!/usr/bin/env python

from __future__ import print_function

from manipulator.srv import ValidateLMNode, ValidateLMNodeResponse
import rospy

def handleLoadMonitorMsg(req):
    return ValidateLMNodeResponse(True)

def LMServer():
    rospy.init_node('LMNode')
    s = rospy.Service('LMNodeValidator', ValidateLMNode, handleLoadMonitorMsg)
    print("Ready to setup")
    rospy.spin()

if __name__ == "__main__":
    LMServer()

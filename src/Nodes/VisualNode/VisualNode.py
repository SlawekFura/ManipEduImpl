#!/usr/bin/env python

from __future__ import print_function

from manipulator.srv import ValidateVisualNode, ValidateVisualNodeResponse
import rospy

def handleVisualMsg(req):
    return ValidateVisualNodeResponse(True)

def VisualServer():
    rospy.init_node('VisualNode')
    s = rospy.Service('VisualNodeValidator', ValidateVisualNode, handleVisualMsg)
    print("Ready to setup")
    rospy.spin()

if __name__ == "__main__":
    VisualServer()

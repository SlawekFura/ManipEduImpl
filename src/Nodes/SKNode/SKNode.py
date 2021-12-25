#!/usr/bin/env python

from __future__ import print_function

from manipulator.srv import ValidateSKNode, ValidateSKNodeResponse, SKTask, SKTaskResponse
import rospy
import std_msgs.msg
from manipulator.msg import Point, Param
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "Shared")
import SKLib as sk
from DHMatrix import *
import numpy as np

theta =  [np.pi,        np.pi/2,    np.pi/2]
alpha =  [np.pi/2,      -np.pi/2,       0.0]
a  =     [0.6,          0.0,            0.0]
lambda_ =[0.7,          0.0,            0.5]


def handleInitMsg(req):
    return ValidateSKNodeResponse(True)


def handleSimpleKinematicsMsg(req):
    print("Handle SKTask: KinReqType: ", req.reqType);

    theta1range = np.arange(-np.pi, np.pi, 0.1)
    theta2range = np.arange(-np.pi, np.pi, 0.3)
    lambda_range = np.arange(-2, 2, 0.5)
    numOfIterations = theta1range.size

    dhMatrix = DHMatrix()
    dhMatrix.addParams({"theta0"    : "var",        "theta1" : "var",       "theta2" : theta[2]})
    dhMatrix.addParams({"alpha0"    : alpha[0],     "alpha1" : alpha[1],    "alpha2" : alpha[2]})
    dhMatrix.addParams({"a0"        : a[0],             "a1" : a[1],            "a2" : a[2]})
    dhMatrix.addParams({"lambda0"   : lambda_[0],  "lambda1" : lambda_[1], "lambda2" : "var"})

    print(dhMatrix.params)
    defaultValues = []

    paramsRange = {"theta0" : theta1range, "theta1" : theta2range, "lambda2" : lambda_range}
    points = sk.genPosPointsForRanges(paramsRange, dhMatrix)
    for x, y, z in points:
        print("x:" + str(x) + " y:" + str(y) + " z:" + str(z))
    
    print(len(points))

    #testParamRange = {"theta0" : theta1range, "theta1" : theta2range, "theta2" : np.arange(-np.pi, np.pi, 0.1),
    #                  "alpha0" : theta1range, "alpha1" : theta2range, "alpha2" : np.arange(-np.pi, np.pi, 0.1),
    #                  "a0" : np.arange(0, 1, 0.1), "a1" : np.arange(0, 1, 0.1), "a2" : np.arange(0, 1, 0.1),
    #                  "lambda0" : np.arange(-1, 1, 0.5), "lambda1" : np.arange(-1, 1, 0.5), "lambda2" : lambda_range}
    ##pl.plotManip(testParamRange, dhMatrix)

    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now() # Note you need to call rospy.init_node() before this will work
    X = [0]
    Y = [0]
    Z = [0]
    points = [Point(X, Y, Z)]
    
    params = [Param("P_0", points)] 

    return SKTaskResponse(header, params);


def SKServer():
    rospy.init_node('SKNode')
    s = rospy.Service('SKNodeValidator', ValidateSKNode, handleInitMsg)
    print("Ready to setup")

    SKMsgService = rospy.Service('SKTask', SKTask, handleSimpleKinematicsMsg)
    print("SKTask performed!")
    rospy.spin()


if __name__ == "__main__":
    SKServer()

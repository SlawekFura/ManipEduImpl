#!/usr/bin/env python

from __future__ import print_function

from manipulator.srv import ValidateVisualNode, ValidateVisualNodeResponse, SKTask, SKTaskResponse
from manipulator.msg import Joint

import rospy


def performSKPrint(req):
    testParamRange = {"theta0" : theta1range, "theta1" : theta2range, "theta2" : np.arange(-np.pi, np.pi, 0.1),
                      "alpha0" : theta1range, "alpha1" : theta2range, "alpha2" : np.arange(-np.pi, np.pi, 0.1),
                      "a0" : np.arange(0, 1, 0.1), "a1" : np.arange(0, 1, 0.1), "a2" : np.arange(0, 1, 0.1),
                      "lambda0" : np.arange(-1, 1, 0.5), "lambda1" : np.arange(-1, 1, 0.5), "lambda2" : lambda_range}
    pl.plotManip(testParamRange, dhMatrix)
    
    joints = []
    for key in testParamRange.keys():
        joints.append(Joint(key, testParamRange[key]))

    rospy.wait_for_service('manipulator1/SKTask')
    try:
        skTaskSrv = rospy.ServiceProxy('manipulator1/SKTask', SKTask)
        response = skTaskSrv(x, y)
        return response.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def handleInitMsg(req):
    return ValidateVisualNodeResponse(True)



def VisualServer():
    rospy.init_node('VisualNode')
    s = rospy.Service('VisualNodeValidator', ValidateVisualNode, handleVisualMsg)
    print("Ready to setup")
    #rospy.spin()

if __name__ == "__main__":
    VisualServer()
    performSKPrint()

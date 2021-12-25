import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../Shared")
from DHMatrix import DHMatrix
import TransitionMatrix
import numpy as np
from sympy import Matrix, eye


theta1range = np.arange(-np.pi, np.pi, 0.1)
theta2range = np.arange(-np.pi, np.pi, 0.3)
lambda_range = np.arange(-2, 2, 0.5)
numOfIterations = theta1range.size
print(numOfIterations)

def getXYZ(TMatrix):
    return [TMatrix[0,3], TMatrix[1,3], TMatrix[2,3]]

def getVariadicRange(paramsRange, param, i, dhMatrix):
    paramName = param + str(i)
    paramVal = dhMatrix.params[param][paramName]

    if paramVal == "var":
        # print("paramsRange", paramsRange[paramName])
        return paramsRange[paramName]
    # print("[paramVal]", [paramVal])
    return [paramVal]

def genPosPointsForRanges(paramsRange, dhMatrix):

    dhColumnSize = dhMatrix.getColSize()
    theta_Coord = {}; alpha_Coord = {}; a_Coord = {}; lambda_Coord = {}

    thetaValIter = {}
    lambdaValIter = {}

    for i in range(0, dhColumnSize):
        theta_Coord[i] = getVariadicRange(paramsRange, "theta", i, dhMatrix)
        alpha_Coord[i] = getVariadicRange(paramsRange, "alpha", i, dhMatrix)
        a_Coord[i] = getVariadicRange(paramsRange, "a", i, dhMatrix)
        lambda_Coord[i] = getVariadicRange(paramsRange, "lambda", i, dhMatrix)
        thetaValIter[i] = 0
        lambdaValIter[i] = 0

    thetaNameIter = 0
    lambdaNameIter = 0
    points = []

    for thetaIt, thetaRange in theta_Coord.items():
        for _ in thetaRange:
            for lambdaIt, lambdaRange in lambda_Coord.items():
                for _ in lambdaRange:
                    TMatrix = eye(4)
                    for transMatrixIt in range(0, dhColumnSize):
                        theta = theta_Coord[transMatrixIt][thetaValIter[transMatrixIt]]
                        lambda_ = lambda_Coord[transMatrixIt][lambdaValIter[transMatrixIt]]

                        TMatrix = TMatrix * TransitionMatrix.getMatrix(theta, alpha_Coord[transMatrixIt][0], a_Coord[transMatrixIt][0], lambda_)

                    # print("x: ", round(getXYZ(TMatrix)[0],2), "y: ", round(getXYZ(TMatrix)[1],2), "z:", round(getXYZ(TMatrix)[2],2))
                    points.append(getXYZ(TMatrix))

                    lambdaValIter[lambdaNameIter] += 1
                lambdaValIter[lambdaNameIter] = 0
                lambdaNameIter += 1
            lambdaNameIter = 0

            thetaValIter[thetaNameIter] += 1
        thetaValIter[thetaNameIter] = 0
        thetaNameIter += 1
        # print("thetaNameIter", thetaNameIter)
    return points

def genElemCoordForSingleParams(paramsValues, dhMatrix):
    dhColumnSize = dhMatrix.getColSize()
    points = []
    inputData = {"theta" : [], "alpha" : [], "a" : [], "lambda" : []}

    for i in range(0, dhColumnSize):
        for var in dhMatrix.params.keys():
            key = (var + str(i))
            if  key in paramsValues:
                inputData[var].append(paramsValues[key])
            else:
                inputData[var].append(dhMatrix.params[var][key])

    # print("inputData", inputData)

    TMatrix = eye(4)
    points.append(getXYZ(TMatrix))

    for transMatrixIt in range(0, dhColumnSize):
        # print("inputData[\"theta\"][transMatrixIt]", inputData["theta"][transMatrixIt])
        TMatrix = TMatrix * TransitionMatrix.getMatrix(inputData["theta"][transMatrixIt], inputData["alpha"][transMatrixIt],
                                       inputData["a"][transMatrixIt], inputData["lambda"][transMatrixIt])
        print(TMatrix)
        points.append(getXYZ(TMatrix))
        print("it",transMatrixIt, points[-1])

    return points

from sympy import Matrix, Symbol
from numpy import pi, arange

def genJacobianMatrix(SystemTransMatrix, TransMatrices, KinPairMode):
    idx = 0
    JacobianMatrix = Matrix()
    filterMatrix = Matrix([[0], [0], [1]])
    emptyMatrix = Matrix([[0], [0], [0]])
    for transMat in TransMatrices[:-1]:
        if KinPairMode[idx] == "R":
            col_top_left = transMat[:3, :3] * filterMatrix
            col_top_right = SystemTransMatrix[:3, -1] - TransMatrices[idx][:3, -1]
            # print("col_top_left", col_top_left)
            # print("col_top_right", col_top_right)
            col_top = col_top_left.cross(col_top_right)
            col_bot = TransMatrices[idx][:3, :3] * filterMatrix
            jacobi_col = col_top.row_insert(4, col_bot)
            # print("col_top", col_top)
            JacobianMatrix = JacobianMatrix.col_insert(idx, jacobi_col)
        else:
            jacobi_col = transMat[:3, :3] * filterMatrix
            jacobi_col = jacobi_col.row_insert(4, emptyMatrix)
            JacobianMatrix = JacobianMatrix.col_insert(idx, jacobi_col)
        idx += 1
    return JacobianMatrix

def genConfigVariablesValues(prevConfVariables, posIn, posExp, invertJacobianMatrix):
    d_x = 0.1
    # print("posIn", posIn, " posExp", posExp)
    # print("prevConfVariables_0", prevConfVariables)
    delta_x = posExp[0] - posIn[0]
    delta_y = posExp[1] - posIn[1]
    delta_z = posExp[2] - posIn[2]

    posDiffBase = abs(max(delta_x, delta_y, delta_z, key=abs))
    delta_t = posDiffBase / d_x
    d_x = delta_x / delta_t
    d_y = delta_y / delta_t
    d_z = delta_z / delta_t
    # print("delta_t: ",delta_t, "d_x: ",d_x, " d_y", d_y, " d_z", d_z)

    d_theta1sym = invertJacobianMatrix[0, 0] * d_x + invertJacobianMatrix[0, 1] * d_y + invertJacobianMatrix[0, 2]     * d_z
    d_theta2sym = invertJacobianMatrix[1, 0] * d_x + invertJacobianMatrix[1, 1] * d_y + invertJacobianMatrix[1, 2]     * d_z
    d_lambda3sym = invertJacobianMatrix[2, 0] * d_x + invertJacobianMatrix[2, 1] * d_y + invertJacobianMatrix[2, 2    ] * d_z

    currentTheta1 = prevConfVariables["theta0"]
    currentTheta2 = prevConfVariables["theta1"]
    currentLambda3 = prevConfVariables["lambda2"]

    d_theta1 = d_theta1sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lambd    a3") : currentLambda3})
    d_theta2 = d_theta2sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lambd    a3") : currentLambda3})
    d_lambda3 = d_lambda3sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lam    bda3") : currentLambda3})
    currentTheta1 += d_theta1 * delta_t
    currentTheta2 += d_theta2 * delta_t
    currentLambda3 += d_lambda3 *delta_t

    prevConfVariables = [currentTheta1, currentTheta2, currentLambda3]
    return prevConfVariables

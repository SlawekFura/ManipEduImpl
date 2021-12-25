import numpy

def getMatrix(theta, alpha, a, lambda_):
    from math import cos, sin
    return numpy.array(
     [[cos(theta),    -sin(theta) * cos(alpha),   sin(theta)*sin(alpha),      a*cos(theta)],
      [sin(theta),    cos(theta) * cos(alpha),    -cos(theta)*sin(alpha),     a*sin(theta)],
      [0,             sin(alpha),                 cos(alpha),                 lambda_     ],
      [0,             0,                          0,                          1           ]])


from sympy import Symbol, Matrix, sin, cos

def getSymbolicMatrix(theta_, alpha_, a_, lambda__):
    theta = Symbol(theta_) if isinstance(theta_,str) else theta_
    alpha = Symbol(alpha_) if isinstance(alpha_,str) else alpha_
    a = Symbol(a_) if isinstance(a_,str) else a_
    lambda_ = Symbol(lambda__) if isinstance(lambda__,str) else lambda__
    return Matrix(
    [[cos(theta),   -sin(theta) * cos(alpha),   sin(theta) * sin(alpha),    a * cos(theta)],
     [sin(theta),   cos(theta) * cos(alpha),    -cos(theta) * sin(alpha),   a * sin(theta)],
     [0,            sin(alpha),                 cos(alpha),                 lambda_],
     [0,            0,                          0,                          1]])


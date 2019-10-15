import numpy as np

def E(X):
    return sum(X)/len(X)

def Var(X):
    expected = E(X)
    result = 0
    for i in X:
        result += (i-expected)**2
    return result/(len(X)-1)

def Covariance(X,Y):
    expected_X = E(X)
    expected_Y = E(Y)
    result = 0
    for i in X:
        for j in Y:
            result += (i-expected_X)*(j-expected_Y)
    return result/(len(X)-1)

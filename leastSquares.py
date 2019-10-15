import numpy as np

# Current model can only take in a nx1 matrix
# I need to work out how to make numpy work with 1d array as well as 2d
class leastSquaresModel:
    def __init__(self,X,y):
        (n,d) = np.shape(X)
        Z = np.ones((n,1))
        Z = np.hstack((Z,X))
        self.w = np.linalg.solve(Z.T@Z,Z.T@y)

    def predict(self,Xhat):
        (n,d) = np.shape(Xhat)
        Z = np.ones((n,1))
        Z = np.hstack((Z,Xhat))
        return Z@self.w

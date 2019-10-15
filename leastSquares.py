import numpy as np

# Current model can only take in a nx1 matrix
# I need to work out how to make numpy work with 1d array as well as 2d
class leastSquaresModel:
    def __init__(self,X,y):
        self.w = np.linalg.solve(X.T@X,X.T@y)

    def predict(self,Xhat):
        return Xhat*self.w

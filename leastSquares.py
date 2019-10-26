import numpy as np

# Current model can only take in a nx1 matrix
# I need to work out how to make numpy work with 1d array as well as 2d
class leastSquaresModel:
    def __init__(self,X,y,p,k):
        (n,d) = np.shape(X)
        Z = np.ones((n,1))
        Z = np.hstack((Z,X))
        # Changing features into polynomials
        for i in range(2,p+1):
            Z = np.hstack((Z,np.power(X,i)))
        # Sine manipulation on features
        for i in range(2,k+1):
            Z = np.hstack((Z,np.sin(X*i)))
        self.w = np.linalg.solve(Z.T@Z,Z.T@y)
        self.p = p
        self.k = k

    def predict(self,Xhat):
        (n,d) = np.shape(Xhat)
        Z = np.ones((n,1))
        Z = np.hstack((Z,Xhat))
        # Changing features into polynomial
        for i in range(2,self.p+1):
            Z = np.hstack((Z,np.power(Xhat,i)))
        # Sine manipulation on features
        for i in range(2,self.k+1):
            Z = np.hstack((Z,np.sin(Xhat*i)))
        return Z@self.w

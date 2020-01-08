import numpy as np
from misc import *
import matplotlib.pyplot as plt

# Current model can only take in a nx1 matrix
# I need to work out how to make numpy work with 1d array as well as 2d
# As in I am currently only taking in 1 variable of input e.g. only taking in price for X
class leastSquaresModel:
    def __init__(self,X,y,p,k):
        (n,d) = np.shape(X)
        Z = np.ones((n,1))
        Z = np.hstack((Z,X))
        # Changing features into polynomials
        for i in range(2,p+1):
            Z = np.hstack((Z,np.power(X,i)))
        # Sine manipulation on features
        # for i in range(2,k+1):
        #     Z = np.hstack((Z,np.sin(X*i)))
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
        # for i in range(2,self.k+1):
        #     Z = np.hstack((Z,np.sin(Xhat*i)))
        return Z@self.w

# Simple regression using Open as parameter and Adj close as output
# This is bad as it requires the opening price of today to predict todays close
def linearOLS(df):
	y = df['Adj Close']
	# X = np.linspace(1,len(y),len(y))
	# Using Open price as the features
	X = df['Open']
	X = np.array(X).reshape(len(X),1)
	y = np.array(y).reshape(len(y),1)
	slice = round(len(X)/2)
	Xtrain = X[0:slice]
	ytrain = y[0:slice]
	Xtest = X[slice:len(X)]
	ytest = y[slice:len(y)]
	regress = leastSquaresModel(Xtrain,ytrain,3,5)
	yhat_train = regress.predict(Xtrain)
	# print((yhat_train - ytrain))
	testError = E((yhat_train - ytrain)**2)
	print("Training Error =", testError)
	yhat = regress.predict(Xtest)
	testError = E((yhat - ytest)**2)
	print("Testing Error =", testError)
	yplot = np.vstack((yhat_train, yhat))
	plt.plot(df['Date'], y, label='Stock Price', color='blue')
	# Plots Training
	plt.plot(df['Date'][:slice], yhat_train, label='Training', color='green')
	# Plots Testing
	plt.plot(df['Date'][slice:], yhat, label='Testing', color='red')
	plt.legend()
	plt.show()

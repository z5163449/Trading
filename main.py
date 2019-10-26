from datareader import *
import matplotlib.pyplot as plt
from plotting import *
import statsmodels.api as sm
from misc import *
import leastSquares as lsModel
import numpy as np

def main():

	# Load all asx200 companies as csv files
	# df_asx200 = pd.read_csv('asx200_list.csv')
	# for code in df_asx200['Code']:
	# 	tmp = backtest_database(code + '.AX','2018-01-30','2019-08-11',1)
	# 	tmp.create_csv()

	ANZ = backtest_database('ANZ.AX','2018-01-30','2019-08-11',1)
	df_ANZ = ANZ.read_csv()
	linearOLS(df_ANZ)


# Simple regression using date as parameter and Adj close as output\
def linearOLS(df):
	y = df['Adj Close']
	X = np.linspace(1,len(y),len(y))
	X = np.array(X).reshape(len(X),1)
	y = np.array(y).reshape(len(y),1)
	slice = round(len(X)/2)
	Xtrain = X[0:slice]
	ytrain = y[0:slice]
	Xtest = X[slice:len(X)]
	ytest = y[slice:len(y)]
	regress = lsModel.leastSquaresModel(Xtrain,ytrain,3,5)
	yhat_train = regress.predict(Xtrain)
	# print((yhat_train - ytrain))
	testError = E((yhat_train - ytrain)**2)
	print("Training Error =", testError)
	yhat = regress.predict(Xtest)
	testError = E((yhat - ytest)**2)
	print("Training Error =", testError)
	yplot = np.vstack((yhat_train, yhat))
	plt.plot(df['Date'], y, label='Stock Price', color='blue')
	# Plots Training
	plt.plot(df['Date'][:slice], yhat_train, label='Training', color='green')
	# Plots Testing
	# plt.plot(df['Date'][slice:], yhat, label='Testing', color='red')
	plt.legend()
	plt.show()


if __name__ == "__main__":
	main()

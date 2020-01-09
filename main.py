from datareader import *
import matplotlib.pyplot as plt
from plotting import *
import statsmodels.api as sm
from misc import *
import leastSquares as lsModel
import numpy as np
from sklearn import kernel_ridge

def main():
	# Load all asx200 companies as csv files
	# df_asx200 = pd.read_csv('asx200_list.csv')
	# for code in df_asx200['Code']:
	# 	tmp = backtest_database(code + '.AX','2018-01-30','2019-08-11',1)
	# 	tmp.create_csv()

	stock = backtest_database('A2M.AX','2018-01-30','2019-08-11',1)
	df_stock = stock.read_csv()
	# lsModel.linearOLS(df_stock)
	# print(df_stock)
	Xtrain,Xvalid,ytrain,yvalid = load_df(df_stock,ydays=30,valid=1)

	# Trying some random shit with scikitlearn
	# Xtrain = df[0:10]
	# ytrain = df['Adj Close'][10:20]
	# Xvalid = df[20:30]
	# yvalid = df['Adj Close'][30:40]
	model = kernel_ridge.KernelRidge(alpha=1)
	model.fit(Xtrain, ytrain)
	abc = model.predict(Xtrain)
	yhat = model.predict(Xvalid)
	print(yhat)
	print(yvalid)
	print(df_stock['Adj Close'][76])
	plt.plot(df_stock['Date'][15:106], df_stock['Adj Close'][15:106], label='Actual Close Price', color='blue')
	plt.plot(df_stock['Date'][76:106],yhat.T,label='Predicted Close price', color='red')
	plt.legend()
	plt.show()

# Splits df to training data and y is a 60x15 matrix
# Matrix y contains the adj close of the next 15 days as this is what we want to predict
def load_df(df_stock,span=15,train=60,valid=15,ydays=15):
	Xtrain = pd.DataFrame()
	ytrain = pd.DataFrame(columns=range(ydays))
	Xvalid = pd.DataFrame()
	yvalid = pd.DataFrame(columns=range(ydays))

	# from span days to trian + span days since we need at least span number of days for ewm
	Xtrain['Open'] = df_stock.Open[span:train+span]
	Xtrain['Adj Close'] = df_stock['Adj Close'][span:train+span]
	Xtrain['Volume'] = df_stock.Volume[span:train+span]
	Xtrain['{} day ewm'.format(span)] = df_stock['Adj Close'].ewm(span=span, adjust=False).mean()[span:train+span]

	for i in range(1,train+1):
		ytrain.loc[i] = df_stock['Adj Close'][span+i:span+ydays+i].values

	Xvalid['Open'] = df_stock.Open[train+span:train+span+valid]
	Xvalid['Adj Close'] = df_stock['Adj Close'][span+train:train+span+valid]
	Xvalid['Volume'] = df_stock.Volume[span+train:train+span+valid]
	Xvalid['15 day ewm'] = df_stock['Adj Close'].ewm(span=span, adjust=False).mean()[span+train:train+span+valid]

	for i in range(1,valid+1):
		yvalid.loc[i] = df_stock['Adj Close'][span+train+i:span+ydays+train+i].values
	return Xtrain,Xvalid,ytrain,yvalid

if __name__ == "__main__":
	main()

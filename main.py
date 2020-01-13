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

	# stock = backtest_database('A2M.AX','2018-01-30','2019-08-11',1)
	stock = backtest_database('MYX.AX','2018-01-30','2019-08-11',1)
	df_stock = stock.read_csv()
	# lsModel.linearOLS(df_stock)
	# print(df_stock)
	Xtrain,Xvalid,ytrain,yvalid = adj_close_loader(df_stock,train=300,ydays=5,valid=1)

	# Trying some random shit with scikitlearn
	# Xtrain = df[0:10]
	# ytrain = df['Adj Close'][10:20]
	# Xvalid = df[20:30]
	# yvalid = df['Adj Close'][30:40]
	model = kernel_ridge.KernelRidge(alpha=1)
	model.fit(Xtrain, ytrain)
	abc = model.predict(Xtrain)
	yhat = model.predict(Xvalid)
	# print(yhat)
	# print(yvalid)
	plt.plot(df_stock['Date'][300:320],df_stock['Adj Close'][300:320], label='Actual Close Price', color='blue')
	plt.plot(df_stock['Date'][315:320],yhat.T,label='Predicted Close price', color='red')
	plt.legend()
	plt.show()

# Splits df to training data and y is a 60x15 matrix
# Matrix y contains the adj close of the next 15 days as this is what we want to predict
# Loads dataset for predicting the next adj close prices.
def adj_close_loader(df_stock,span=15,train=60,valid=15,ydays=15):
	Xtrain = pd.DataFrame()
	ytrain = pd.DataFrame(columns=range(ydays))
	Xvalid = pd.DataFrame()
	yvalid = pd.DataFrame(columns=range(ydays))

	# from span days to trian + span days since we need at least span number of days for ewm
	Xtrain['Open'] = df_stock.Open[span:train+span].values
	Xtrain['Prev Adj Close'] = df_stock['Adj Close'][span-1:train+span-1].values
	Xtrain['Prev Volume'] = df_stock.Volume[span-1:train+span-1].values
	Xtrain['{} day ewm'.format(span)] = df_stock['Adj Close'].ewm(span=span, adjust=False).mean()[span-1:train+span-1].values
	# Xtrain['% price change per day'] = (df_stock['Adj Close'][span-1:train+span-1].values - df_stock.Open[span-1:train+span-1].values)/df_stock.Open[span-1:train+span-1].values
	Xtrain['% volume change per day'] = (df_stock.Volume[span-1:train+span-1].values - df_stock.Volume[span-2:train+span-2].values)/df_stock.Volume[span-2:train+span-2].values
	Xtrain['% price change overnight'] = (df_stock.Open[span:train+span].values - df_stock['Adj Close'][span-1:train+span-1].values)/df_stock['Adj Close'][span-1:train+span-1].values

	for i in range(0,train):
		ytrain.loc[i] = df_stock['Adj Close'][span+i:span+ydays+i].values

	Xvalid['Open'] = df_stock.Open[train+span:train+span+valid].values
	Xvalid['Prev Adj Close'] = df_stock['Adj Close'][span+train-1:train+span+valid-1].values
	Xvalid['Prev Volume'] = df_stock.Volume[span+train-1:train+span+valid-1].values
	Xvalid['{} day ewm'.format(span)] = df_stock['Adj Close'].ewm(span=span, adjust=False).mean()[span+train-1:train+span+valid-1].values
	# Xvalid['% change per day'] = (df_stock['Adj Close'][span+train-1:train+span+valid-1].values - df_stock.Open[span+train-1:train+span+valid-1].values)/df_stock.Open[span-1:span+train-1:train+span+valid-1].values
	Xvalid['% volume change per day'] = (df_stock.Volume[span+train-1:train+span+valid-1].values - df_stock.Volume[span+train-2:train+span+valid-2].values)/df_stock.Volume[span+train-2:train+span+valid-2].values
	Xvalid['% price change overnight'] = (df_stock.Open[train+span:train+span+valid].values - df_stock['Adj Close'][span+train-1:train+span+valid-1].values)/df_stock['Adj Close'][span+train-1:train+span+valid-1].values

	for i in range(0,valid):
		yvalid.loc[i] = df_stock['Adj Close'][span+train+i:span+ydays+train+i].values

	return Xtrain,Xvalid,ytrain,yvalid

if __name__ == "__main__":
	main()

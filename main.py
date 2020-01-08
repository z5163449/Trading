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
	df = load_df(df_stock)

	# Trying some random shit with scikitlearn
	# Xtrain = df[0:10]
	# ytrain = df['Adj Close'][10:20]
	# Xvalid = df[20:30]
	# yvalid = df['Adj Close'][30:40]
	# model = kernel_ridge.KernelRidge(alpha=1)
	# model.fit(Xtrain, ytrain)
	# abc = model.predict(Xtrain)
	# yhat = model.predict(Xvalid)
	# print(yhat)
	# print(yvalid)
	# plt.plot(df_stock['Date'][15:55], df_stock['Adj Close'][15:55], label='Actual Close Price', color='blue')
	# plt.plot(df_stock['Date'][45:55],yhat,label='Predicted Close price', color='red')
	# plt.legend()
	# plt.show()

# Splits df to training data and y is a 60x15 matrix
def load_df(df_stock,span=15,train=60):
	Xtrain = pd.DataFrame()
	ytrain = pd.DataFrame(columns=range(15))
	# Xvalid = pd.DataFrame()
	# yvalid = pd.DataFrame()
	# df['Date'] = df_stock.Date[15:]
	Xtrain['Open'] = df_stock.Open[span:train+span]
	Xtrain['Adj Close'] = df_stock['Adj Close'][span:train+span]
	Xtrain['Volume'] = df_stock.Volume[span:train+span]
	Xtrain['15 day ewm'] = df_stock['Adj Close'].ewm(span=span, adjust=False).mean()[span:train+span]
	for i in range(1,train):
		ytrain.loc[i] = df_stock['Adj Close'][span+i:2*span+i].values

	return Xtrain

if __name__ == "__main__":
	main()

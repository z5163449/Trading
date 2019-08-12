from datareader import *

def main():

	CBA = backtest_database('CBA.AX','2017-01-30','2019-08-11',1)

	df_CBA = CBA.read_csv()
	#df_CBA.plot(kind='line', x ='Date', y = 'Open', color='blue')

	#extr_open = df_CBA.Open

	#sma_30 = extr_open.rolling(window=30).mean()
	#sma_50 = extr_open.rolling(window=50).mean()
	#plt.plot(df_CBA.Date, sma_30, label='CBA 30 Day Average', color='red')
	#plt.plot(df_CBA.Date, sma_50, label='CBA 50 Day Average', color='pink')

	#plt.show()




if __name__ == "__main__":
	main()

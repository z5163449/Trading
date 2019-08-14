from datareader import *
import statsmodels.api as sm

def main():

	CBA = backtest_database('CBA.AX','2017-01-30','2019-08-11',1)
	#CBA.create_csv()

	df_CBA = CBA.read_csv()
	df_CBA = df_CBA.dropna(how='any', axis=0)
	df_CBA.plot(kind='line', x ='Date', y = 'Adj Close', color='blue')

	extr_adj_close = df_CBA['Adj Close']
	dates = df_CBA['Date']

	ewm_30 = extr_adj_close.ewm(span=30, adjust=False).mean()
	ewm_50 = extr_adj_close.ewm(span=50, adjust=False).mean()

	plt.plot(df_CBA.Date, df_CBA['Adj Close'], label='Adj Close', color='blue')
	plt.plot(df_CBA.Date, ewm_30, label='CBA 30 Day Average', color='red')
	plt.plot(df_CBA.Date, ewm_50, label='CBA 50 Day Average', color='green')
	plt.gca().legend(('Adj Close', 'CBA 30 Day Average','CBA 50 Day Average'))
	#plt.show()


	model = sm.OLS(extr_adj_close, dates).fit()

	np.random.seed(123)
	df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list('ABC'))

	# assign dependent and independent / explanatory variables
	variables = list(df.columns)
	y = 'A'
	x = [var for var in variables if var not in y]

	# Ordinary least squares regression
	model_Simple = sm.OLS(df[y], df[x]).fit()

	# Add a constant term like so:
	model = sm.OLS(df[y], sm.add_constant(df[x])).fit()

	model.summary()

if __name__ == "__main__":
	main()

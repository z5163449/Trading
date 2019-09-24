from datareader import *
import statsmodels.api as sm

def main():

	# Load all asx200 companies as csv files
	# df_asx200 = pd.read_csv('asx200_list.csv')
	# for code in df_asx200['Code']:
	# 	tmp = backtest_database(code + '.AX','2017-01-30','2019-08-11',1)
	# 	tmp.create_csv()

	# CBA = backtest_database('CBA.AX','2017-01-30','2019-08-11',1)
	# CBA.create_csv()

	# CBA.plot_adj_close()
	# CBA.plot_ewm(30,'red')
	# CBA.plot_ewm(50,'green')
	# CBA.scatter_plot()
	# CBA.show_plot()
	# df_CBA = CBA.read_csv()
	# model = sm.OLS(df_CBA['Adj Close'], df_CBA['Date']).fit()
	#
	# np.random.seed(123)
	# df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list('ABC'))

	# assign dependent and independent / explanatory variables
	# variables = list(df.columns)
	# y = 'A'
	# x = [var for var in variables if var not in y]
	# Ordinary least squares regression
	# model_Simple = sm.OLS(df[y], df[x]).fit()
	#
	# # Add a constant term like so:
	# model = sm.OLS(df[y], sm.add_constant(df[x])).fit()
	#
	# model.summary()

if __name__ == "__main__":
	main()

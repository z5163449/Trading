from datareader import *
import matplotlib.pyplot as plt
from plotting import *
import statsmodels.api as sm
from misc import *
import leastSquares as lsModel
import masim as mAvgSim
import numpy as np
import pandas as pd
import statistics as stat

def main():
	# scrape_data(pd.read_csv('china_stocks.csv'),location='chineseStocks/',
							# start='2019-09-16',end='2020-02-17')
	# df_stock = pd.read_csv('603131.csv')
	# df_cypt = pd.read_csv('ETH-USD.csv')
	# df_stock = backtest_database('BAL.AX','2019-09-16','2020-02-16',1).read_csv()
	# sim = mAvgSim.movingAverageSim(df_stock)
	# net,num_trades = sim.run_simulation()
	# sim = mAvgSim.movingAverageSim(df_cypt)
	# sim.plot_graph()
	# test_stock_list(stock_list=pd.read_csv('china_stocks.csv'),location='chineseStocks/')
	daily_signal_checker('china_stocks.csv',location='chineseStocks/')
	# tmp = backtest_database('300261.SZ','2019-09-16','2020-02-16',1)
	# df_stock = tmp.read_csv('chineseStocks/')
	# open_price = tmp.get_today_open()
	# df_stock = df_stock.append({'Open' : open_price},ignore_index=True)
	# sim = mAvgSim.movingAverageSim(df_stock)
	# sim.run_simulation(ndays=5)
	# signals = sim.produce_buy_sell(ndays=1)
	# print(signals)

def update_portfolio():
	portfolio = pd.read_csv(portfolio)

def daily_signal_checker(stocks,location):
	#requires manul changing because I cbf to learn how to parse dates properly
	ndays=2
	# scrape_data(pd.read_csv(stocks),location='chineseStocks/',
							# start='2019-09-16',end='2020-02-18')
	stock_list = pd.read_csv(stocks)
	for code in stock_list['Code']:
		tmp = backtest_database(code,'2019-09-16','2020-02-17',1)
		df_stock = tmp.read_csv(location=location)
		# print(code)
		open_price = tmp.get_today_open()
		df_stock = df_stock.append({'Open' : open_price},ignore_index=True)
		# print(df_stock.tail())
		sim = mAvgSim.movingAverageSim(df_stock)
		signals = sim.produce_buy_sell(ndays=ndays)
		print("Company:",code,
			"Signals:",signals)

def scrape_data(stock_list,location,start,end):
	for code in stock_list['Code']:
		print("Got Code:",code)
		tmp = backtest_database(code,start,end,1)
		tmp.create_csv(location=location)

def test_stock_list(stock_list,location):
	returns = pd.DataFrame(columns=['Company','No. Trades','Net return'])
	for code in stock_list['Code']:
		df_stock = backtest_database(code,'2019-09-16','2020-02-178',1).read_csv(location=location)
		sim = mAvgSim.movingAverageSim(df_stock)
		net,num_trades = sim.run_simulation(ndays=5)
		if num_trades == 0:
			continue
		returns = returns.append({
			'Company' : code,
			'No. Trades' : num_trades,
			'Net return' : net,
		},ignore_index=True)
		# print('Company:',code,'\n Number of Trades',num_trades,'\n Net % return',net)
	net_profit = np.sum(returns['Net return'])
	companies_traded = len(returns)
	mean = stat.mean(returns['Net return'])
	std = stat.stdev(returns['Net return'])
	print("Net Profit =",net_profit,
		'\n Total number of companies traded =',companies_traded,
		'\n Mean Profit =',mean,
		'\n Standard Deviation',std)
	print(returns)


if __name__ == "__main__":
	main()

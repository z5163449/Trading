from datareader import *
import matplotlib.pyplot as plt
from plotting import *
from misc import *
import leastSquares as lsModel
import masim as mAvgSim
import numpy as np
import pandas as pd
import statistics as stat
from datetime import datetime as dt
from time import mktime

def main():
	# scrape_data(pd.read_csv('china_stocks.csv'),location='chineseStocks/',
	# 						start='2019-09-16',end='2020-11-12')
	# cypt_scrape = backtest_database('LINK-USD','2019-09-16','2020-11-12',1)
	# cypt_scrape.create_csv('/Users/jimmylin/Desktop/Quant_Trading/Trading/')
	# df_stock = pd.read_csv('603131.csv')
	# df_cypt = pd.read_csv('LINK-USD.csv')
	# df_stock = backtest_database('603993.SS','2019-09-16','2020-11-17',1).read_csv(location='chineseStocks/')
	# sim = mAvgSim.movingAverageSim(df_stock)
	# sim = mAvgSim.movingAverageSim(df_cypt)
	# net,num_trades,test_error = sim.run_simulation(ndays=15)
	# sim.plot_graph()
	# test_stock_list(stock_list=pd.read_csv('china_stocks.csv'),location='chineseStocks/',ndays=15)
	daily_signal_checker('china_stocks.csv',location='chineseStocks/')
	# update_open_close('china_stocks.csv',location='chineseStocks/')
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
	ndays=2
	# Get updated stock prices (whole csv)
	# scrape_data(pd.read_csv(stocks),location='chineseStocks/',
	# 						start='2019-09-16',end='2020-11-18')
	# Run through stock list to get opens and predict
	stock_list = pd.read_csv(stocks)
	for code in stock_list['Code']:
		tmp = backtest_database(code,'2019-09-16','2020-11-18',1)
		df_stock = tmp.read_csv(location=location)
		open_price = float(tmp.get_today_open())
		# print(open_price)
		df_stock = df_stock.append({'Open' : open_price},ignore_index=True)
		sim = mAvgSim.movingAverageSim(df_stock)
		signals = sim.produce_buy_sell(ndays=ndays)
		print("Company:",code,
			"Signals:",signals)

def scrape_data(stock_list,location,start,end):
	for code in stock_list['Code']:
		print("Got Code:",code)
		tmp = backtest_database(code,start,end,1)
		tmp.create_csv(location=location)

def test_stock_list(stock_list,location,ndays):
	returns = pd.DataFrame(columns=['Company','No. Trades','Net return','Test Error'])
	for code in stock_list['Code']:
		print(code)
		df_stock = backtest_database(code,'2019-09-16','2020-02-17',1).read_csv(location=location)
		sim = mAvgSim.movingAverageSim(df_stock)
		net,num_trades,test_error = sim.run_simulation(ndays=ndays)
		if num_trades == 0:
			continue
		returns = returns.append({
			'Company' : code,
			'No. Trades' : num_trades,
			'Net return' : net,
			'Test Error' : test_error
		},ignore_index=True)
		# print('Company:',code,'\n Number of Trades',num_trades,'\n Net % return',net)
	print("Mean Test Error = ", np.mean(returns['Test Error']))
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

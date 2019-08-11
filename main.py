from datareader import *

def main():
	CBA = backtest_database('CBA.AX','1998-1-1','2019-1-1')
	CBA.create_csv()
	df_CBA = CBA.read_csv()
	print(df_CBA['High'])

if __name__ == "__main__":
	main()

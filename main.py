from datareader import *

def main():
	CBA = backtest_database('CBA.AX','1998-01-01','2019-11-08',1)
	CBA.create_csv()
	# df_CBA = CBA.read_csv()
	# print(df_CBA)

if __name__ == "__main__":
	main()

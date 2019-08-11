import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

class backtest_database:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end

    def create_csv(self):
        df = web.get_data_yahoo(self.ticker, self.start, self.end)
        df.to_csv(self.ticker + '.csv')

    def set_start_date(self, newStartDate):
        self.start = newStartDate

    def set_end_date(self, newEndDate):
        self.end = newEndDate

    def read_csv(self):
        return pd.read_csv(self.ticker + '.csv')

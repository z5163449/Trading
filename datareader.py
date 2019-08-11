from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import os
import re
import requests
from time import mktime

class backtest_database:
    def __init__(self, ticker, start, end, interval):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval

    def set_start_date(self, newStartDate):
        self.start = newStartDate

    def set_end_date(self, newEndDate):
        self.end = newEndDate

    def read_csv(self):
        return pd.read_csv(self.ticker + '.csv')

    # WEBSCRAPING FUNCTIONS
    def _get_crumbs_and_cookies(self):
        url = 'https://finance.yahoo.com/quote/{}/history'.format(self.ticker)
        with requests.session():
            header = {'Connection': 'keep-alive',
                   'Expires': '-1',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
                   }
            website = requests.get(url, headers=header)
            soup = BeautifulSoup(website.text, 'lxml')
            crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))
            return (header, crumb[0], website.cookies)

    def convert_to_unix(self, date):
        datum = dt.strptime(date, '%Y-%m-%d').timetuple()
        return int(mktime(datum))

    def create_csv(self):
        day_begin_unix = self.convert_to_unix(self.start)
        day_end_unix = self.convert_to_unix(self.end)
        header, crumb, cookies = self._get_crumbs_and_cookies()
        # print(crumb)
        with requests.session():
            url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
                  '{stock}?period1={day_begin}&period2={day_end}&interval={interval}&events=history&crumb={crumb}' \
                  .format(stock=self.ticker, day_begin=day_begin_unix, day_end=day_end_unix, interval=self.interval, crumb=crumb)
            print(url)
            website = requests.get(url, headers=header, cookies=cookies)
            website.text.split('\n')[:-1]

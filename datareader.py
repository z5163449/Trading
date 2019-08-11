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
from request.auth import HTTPBasicAuth

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
        session = requests.Session()
            # header = {'Connection': 'keep-alive',
            #        'Expires': '-1',
            #        'Upgrade-Insecure-Requests': '1',
            #        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)' \
            #        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            #        }
        jar = requests.cookies.RequestsCookieJar()
        jar.set('B','2hk21p1cfof63&b=3&s=7d')
        session.cookies = jar
        website = session.get(url, auth=HTTPBasicAuth('user','pass'))#, headers=header)
        #print(website.cookies)
        soup = BeautifulSoup(website.text, 'lxml')
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))
        return (crumb[0], session.cookies)

    def convert_to_unix(self, date):
        datum = dt.strptime(date, '%Y-%m-%d').timetuple()
        return int(mktime(datum))

    def create_csv(self):
        day_begin_unix = self.convert_to_unix(self.start)
        day_end_unix = self.convert_to_unix(self.end)
        crumb, cookies = self._get_crumbs_and_cookies()
        # print(crumb)
        with requests.session():
            url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
                  '{stock}?period1={day_begin}&period2={day_end}&interval={interval}&events=history&crumb={crumb}' \
                  .format(stock=self.ticker, day_begin=day_begin_unix, day_end=day_end_unix, interval=self.interval, crumb=crumb)
            print(url)
            website = requests.get(url, cookies=cookies)
            website.text.split('\n')[:-1]
            # print(website)

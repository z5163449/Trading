from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import os
import re
import requests
from time import mktime
from requests.auth import HTTPBasicAuth

style.use('ggplot')

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

    def plot_adj_close(self):
        df = self.read_csv()
        df = df.dropna(how='any', axis=0)
        df.plot(kind='line', x ='Date', y = 'Adj Close', color='blue')

    def plot_ewm(self, span, colour):
        df = self.read_csv()
        ewm = df['Adj Close'].ewm(span=span, adjust=False).mean()
        plt.plot(df['Date'], ewm, label='CBA {} Day Average'.format(span), color=colour)

    def show_plot(self):
        plt.legend()
        plt.show()

    # def scatter_plot(self):
    #     df = self.read_csv()
    #     plt.scatter(df["Date"], df["Volume"], alpha=0.8, s=30, c='red', label="Volume")
    #     plt.scatter(df["Date"], df["Close"], alpha=0.8, s=30, c='green', label="Close")
    #     plt.title("Adj Close vs Open")
    #     plt.xlabel('Time')
    #     plt.ylabel('Price')

    def read_csv(self):
        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
        r = pd.read_csv('asx200/' + self.ticker + '.csv', parse_dates=['Date'], date_parser=dateparse)
        return r.dropna()

    # WEBSCRAPING FUNCTIONS
    def _get_crumbs_and_cookies(self):
        url = 'https://finance.yahoo.com/quote/{}/history'.format(self.ticker)
        session = requests.Session()
        jar = requests.cookies.RequestsCookieJar()
        jar.set('B','2hk21p1cfof63&b=3&s=7d')
        session.cookies = jar
        website = session.get(url)
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
        with requests.session():
            url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
                  '{stock}?period1={day_begin}&period2={day_end}&interval={interval}d&events=history&crumb={crumb}' \
                  .format(stock=self.ticker, day_begin=day_begin_unix, day_end=day_end_unix, interval=self.interval, crumb=crumb)
            website = requests.get(url, cookies=cookies)
            if website.status_code == 200:
                decoded_content = website.content.decode('utf-8')
                with open('asx200/' +self.ticker + '.csv', 'w') as f:
                    f.writelines(decoded_content)

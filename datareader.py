import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

def get_csv():
    stock = 'CBA.AX'
    start = '1992-01-01'
    end = dt.date.today();
    df = web.get_data_yahoo(stock, start, end)
    df.to_csv('CBA.csv')

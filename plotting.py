from datetime import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import os
import re
import numpy
from datareader import *

def plot_adj_close(stockList):
    for stock in stockList:
        df = stock.read_csv()
        plt.plot(df['Date'],df['Adj Close'],label='{} Adj Close'.format(stock),c=numpy.random.rand(3,))

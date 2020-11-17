import numpy as np
from misc import *
import pandas as pd
import statistics as stat
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier

class movingAverageSim:
    def __init__(self,df_stock):
        self.df_stock = df_stock
        self.ma30 = df_stock['Adj Close'].rolling(30).mean()
        self.ma20 = df_stock['Adj Close'].rolling(20).mean()
        self.ma10 = df_stock['Adj Close'].rolling(10).mean()
        self.ma5 = df_stock['Adj Close'].rolling(5).mean()
        self.rsi = self.calculate_rsi()
        self.returns = pd.DataFrame(columns=['Bought Date','Sold Date','% return'])

    def produce_buy_sell(self,ndays):
        Xtrain,ytrain,Xhat,ytest = self.create_prediction_data(valid=0,test=ndays)
        # print(Xhat)
        clf = self.random_forest_signals(Xtrain,ytrain)
        signal = clf.predict(Xhat)
        return signal

    def run_simulation(self,ndays=30):
        holding = False
        validation = 0
        testing = ndays
        Xtrain,ytrain,Xhat,ytest = self.create_prediction_data(valid=validation,test=testing)
        ytest = np.ravel(ytest)
        clf = self.random_forest_signals(Xtrain,ytrain)
        signals = clf.predict(Xhat)
        test_error = 1-clf.score(Xhat[:-1],ytest)
        print("Testing Error rate =",test_error)
        count = 0
        transaction_cost = 1.002
        print(signals)
        print(ytest)
        # print(Xhat)
        for i in range(len(self.df_stock)-testing,len(self.df_stock)-1):
            # print(self.df_stock['Date'][i])
            price = (self.df_stock['Open'][i] + self.df_stock['Adj Close'][i])/2
            if (signals[count] == 1 and holding == False):
                holding = True
                bought_at = price*transaction_cost
                bought_date = self.df_stock['Date'][i]
                # print("Bought at",bought_date)
                # print("Closed at",self.df_stock['Close'][i])
            if (signals[count] == -1 and holding == True):
                holding = False
                sold_at = price
                sold_date = self.df_stock['Date'][i]
                self.returns = self.returns.append({'Bought Date' : bought_date,
        						'Sold Date' : sold_date,
        						'% return' :(sold_at - bought_at)/bought_at}, ignore_index=True)
            count+=1
        net = self.calculate_profits()
        return net,len(self.returns),test_error


    def calculate_profits(self):
        if self.returns.empty:
            # print("No trades made.")
            return 0
        net = np.sum(self.returns['% return'])
        mean = stat.mean(self.returns['% return'])
        # std = stat.stdev(self.returns['% return'])
        # print(self.returns)
        # print(self.returns['Bought Date']-self.returns['Sold Date'])
        # print("Net Profit =",net)
        # print("Mean =",mean)
        return net

    def calculate_rsi(self,ndays=10):
        delta = self.df_stock['Adj Close'].diff()
        dUp, dDown = delta.copy(), delta.copy()
        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0
        rolUp = dUp.rolling(ndays).mean()
        rolDown = np.abs(dDown.rolling(ndays).mean())

        rs = rolUp/rolDown
        rsi = 100 - 100/(1+rs)
        return rsi

    # Using RandomForestClassifier to classify signals
    def random_forest_signals(self,Xtrain,ytrain):
        clf = RandomForestClassifier(n_estimators=50,max_depth=4,
                                    random_state=0,bootstrap=False)
        ytrain = ytrain.astype('int')
        clf.fit(Xtrain,np.ravel(ytrain))
        # print("Training Error:",1-clf.score(Xtrain,ytrain))
        return clf

    def create_prediction_data(self,valid=30,test=30):
        Xtrain = pd.DataFrame(columns=['Open','pAdj_close'
                                        ,'pma30_open','pma20_open','pma10_open','pma5_open'
                                        ,'pma30_20','pma30_10','pma30_5','pma20_10'
                                        ,'pma20_5','pma10_5','rsi'])
        ytrain = pd.DataFrame(columns=['Classification'])
        Xvalid = pd.DataFrame(columns=['Open','pAdj_close'
                                        ,'pma30_open','pma20_open','pma10_open','pma5_open'
                                        ,'pma30_20','pma30_10','pma30_5','pma20_10'
                                        ,'pma20_5','pma10_5','rsi'])
        yvalid = pd.DataFrame(columns=['Classification'])
        Xhat = pd.DataFrame(columns=['Open','pAdj_close'
                                        ,'pma30_open','pma20_open','pma10_open','pma5_open'
                                        ,'pma30_20','pma30_10','pma30_5','pma20_10'
                                        ,'pma20_5','pma10_5','rsi'])
        ytest = pd.DataFrame(columns=['Classification'])

        Xtrain['Open'] = self.df_stock['Open']
        Xtrain['pAdj_close'] = self.df_stock['Adj Close']/self.df_stock['Open'] - 1
        Xtrain['pma30_open'] = (self.ma30.shift(1)/self.df_stock['Open']) - 1
        Xtrain['pma20_open'] = (self.ma20.shift(1)/self.df_stock['Open']) - 1
        Xtrain['pma10_open'] = (self.ma10.shift(1)/self.df_stock['Open']) - 1
        Xtrain['pma5_open'] = (self.ma5.shift(1)/self.df_stock['Open']) - 1
        Xtrain['pma30_20'] = (self.ma30/self.ma20).shift(1) - 1
        Xtrain['pma30_10'] = (self.ma30/self.ma10).shift(1) - 1
        Xtrain['pma30_5'] = (self.ma30/self.ma5).shift(1) - 1
        Xtrain['pma20_10'] = (self.ma20/self.ma10).shift(1) - 1
        Xtrain['pma20_5'] = (self.ma20/self.ma5).shift(1) - 1
        Xtrain['pma10_5'] = (self.ma10/self.ma5).shift(1) - 1
        Xtrain['rsi'] = self.rsi.shift(1)
        Xtrain = Xtrain.dropna()
        # print(Xtrain)


        def classification_func(value):
            if (value < 0.02):
                return -1
            if (value > 0.02):
                return 1
        ytrain['Classification'] = ((self.df_stock['Adj Close'].shift(-1)
                                    - self.df_stock['Open'])/self.df_stock['Open']).dropna().values
        ytrain['Classification'] = ytrain.apply(lambda x: classification_func(x['Classification']),
                                                axis=1)
        ytrain = ytrain.iloc[30:]
        # Xvalid = Xtrain[len(Xtrain)-valid-test:len(Xtrain)-test]
        # yvalid = ytrain[len(yvalid)-valid-test:len(Xtrain)-test]
        Xhat = Xtrain[len(Xtrain)-test:]
        ytest = ytrain[len(Xtrain)-test:]
        Xtrain = Xtrain[:len(Xtrain)-test-1]
        ytrain = ytrain[:len(Xtrain)]
        # print(self.df_stock['Open'][29],self.df_stock['Adj Close'][30],self.df_stock['Open'][30])
        return Xtrain,ytrain,Xhat,ytest

    def plot_graph(self):
        # plt.plot(self.df_stock['Date'],ma30, label='30 day average Close Price')
        # plt.plot(self.df_stock['Date'],ma20d, label='20 day average Close Price')
        # plt.plot(self.df_stock['Date'],ma10d, label='10 day average Close Price')
        # plt.plot(self.df_stock['Date'],ma5d, label='5 day average Close Price')
        plt.plot(self.df_stock['Date'][30:],self.df_stock['Adj Close'][30:], label='Adjusted Close Price')
        plt.plot(self.df_stock['Date'][30:],self.df_stock['Open'][30:], label='Open')
        # plt.plot(self.df_stock['Date'],self.rsi, label='rsi')
        plt.legend()
        plt.show()

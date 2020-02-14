import numpy as np
from misc import *
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

class movingAverageSim:
    def __init__(self,df_stock):
        self.df_stock = df_stock
        self.ma30 = df_stock['Adj Close'].rolling(30).mean()
        self.ma20 = df_stock['Adj Close'].rolling(20).mean()
        self.ma10 = df_stock['Adj Close'].rolling(10).mean()
        self.ma5 = df_stock['Adj Close'].rolling(5).mean()
        self.rsi = self.calculate_rsi()
        self.returns = pd.DataFrame(columns=['Bought Date','Sold Date','% return'])

    def run_simulation(self):
        holding = False
        validation = 60
        Xtrain,Xvalid,ytrain,yvalid = self.create_prediction_data(valid=validation)
        signals = self.random_forest_signals(Xtrain,ytrain,Xvalid)
        yvalid = np.ravel(yvalid)
        print("Validation Error rate =",np.count_nonzero(yvalid-signals)/np.size(signals))

        count = 0
        for i in range(len(self.df_stock)-validation,len(self.df_stock)):
            if (signals[count] == 1 and holding == False):
                holding = True
                bought_at = self.df_stock['Open'][i]
                bought_date = self.df_stock['Date'][i]
                # print("Bought at",bought_at)
                # print("Closed at",self.df_stock['Close'][i])
            if (signals[count] == -1 and holding == True):
                holding = False
                sold_at = self.df_stock['Open'][i]
                sold_date = self.df_stock['Date'][i]
                self.returns = self.returns.append({'Bought Date' : bought_date,
        						'Sold Date' : sold_date,
        						'% return' :(sold_at - bought_at)/bought_at}, ignore_index=True)
            count+=1

        self.calculate_profits()


    def calculate_profits(self):
        # Note this is saying that the portfolio only has one security so you can't really calcuate sharpe
        net = np.sum(self.returns['% return'])
        mean = np.mean(self.returns['% return'])
        std = np.std(self.returns['% return'])
        print(self.returns)
        print("Net Profit =",net)
        print("Mean =",mean)
        print("Standard Deviation =",std)
        print("Sharpe =",(mean-0.03)/std)

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
    def random_forest_signals(self,Xtrain,ytrain,Xvalid):
        clf = RandomForestClassifier(n_estimators=100,max_depth=10,random_state=0)
        clf.fit(Xtrain,np.ravel(ytrain))
        yhat = clf.predict(Xvalid)
        return yhat

    def create_prediction_data(self,valid=30):
        Xtrain = pd.DataFrame(columns=['Open','ma30_20','ma30_10','ma30_5',
                                        'ma20_10','ma20_5','ma10_5','pma30_20',
                                        'pma30_10','pma30_5','pma20_10'
                                        ,'pma20_5','pma10_5','rsi'])
        ytrain = pd.DataFrame(columns=['Classification'])
        Xvalid = pd.DataFrame(columns=['Open','ma30_20','ma30_10','ma30_5',
                                                'ma20_10','ma20_5','ma10_5','pma30_20',
                                                'pma30_10','pma30_5','pma20_10'
                                                ,'pma20_5','pma10_5','rsi'])
        yvalid = pd.DataFrame(columns=['Classification'])

        Xtrain['Open'] = self.df_stock['Open']
        Xtrain['ma30_20'] = self.ma30 - self.ma20
        Xtrain['ma30_10'] = self.ma30 - self.ma10
        Xtrain['ma30_5'] = self.ma30 - self.ma5
        Xtrain['ma20_10'] = self.ma20 - self.ma10
        Xtrain['ma20_5'] = self.ma20 - self.ma5
        Xtrain['ma10_5'] = self.ma10 - self.ma5
        Xtrain['pma30_20'] = np.sign(self.ma30 - self.ma20).shift(1)
        Xtrain['pma30_10'] = np.sign(self.ma30 - self.ma10).shift(1)
        Xtrain['pma30_5'] = np.sign(self.ma30 - self.ma5).shift(1)
        Xtrain['pma20_10'] = np.sign(self.ma20 - self.ma10).shift(1)
        Xtrain['pma20_5'] = np.sign(self.ma20 - self.ma5).shift(1)
        Xtrain['pma10_5'] = np.sign(self.ma10 - self.ma5).shift(1)
        Xtrain['rsi'] = self.rsi
        Xtrain = Xtrain.dropna()

        ytrain['Classification'] = np.sign(self.df_stock['Adj Close'][30:].values
                                            - self.df_stock['Open'][30:].values)

        Xvalid = Xtrain[len(Xtrain)-valid:len(Xtrain)]
        yvalid = ytrain[len(yvalid)-valid:len(Xtrain)]
        # Xhat = Xtrain[len(Xtrain)-test:]
        Xtrain = Xtrain[:len(Xtrain)-valid]
        ytrain = ytrain[:len(ytrain)-valid]

        return Xtrain,Xvalid,ytrain,yvalid

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

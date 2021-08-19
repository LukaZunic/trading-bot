import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import yfinance as yf
nt = None  # default='warn'

pd.options.mode.chained_assignment = None  # default='warn'

   
def fillMoves(data):
    for _day in range(1, len(data)):
        _previousDay = _day-1
        data['Down Move'][_day] = 0
        data['Up Move'][_day] = 0

        if data['Adj Close'][_day] > data['Adj Close'][_previousDay]:
            data['Up Move'][_day] = data['Adj Close'][_day] - data['Adj Close'][_previousDay]
            

        if data['Adj Close'][_day] < data['Adj Close'][_previousDay]:
            data['Down Move'][_day] = abs(data['Adj Close'][_day] - data['Adj Close'][_previousDay])

    return data


def fillAverages(data):

    _data = data
    ## First 10days Avg
    _data['Average Up'][10] = _data['Up Move'][1:11].mean()
    _data['Average Down'][10] = _data['Down Move'][1:11].mean()

    ## Rest Avgs
    for _day in range(11,len(_data)):
        _previousDay = _day-1
        
        _data['Average Up'][_day] = (_data['Average Up'][_previousDay]*9 + _data['Up Move'][_day])/10
        _data['Average Down'][_day] = (_data['Average Down'][_previousDay]*9 + _data['Down Move'][_day])/10 

    return _data


def fillRelativeStrength(data):
    _data = fillAverages(data)

    ## First 10days RS
    _data['RS'][10] = _data['Average Up'][10] / _data['Average Down'][10]

    ## Rest RelativeStrengths
    for _day in range(11,len(_data)):
        _data['RS'][_day] = _data['Average Up'][_day] / _data['Average Down'][_day]

    return _data    

def fillRsi(data):
    _data = fillRelativeStrength(data)

    # First 10Days RSI
    _data['RSI'][10] = 100 - (100 / (1 + _data['RS'][10]))

    # Rest RSIs
    for _day in range(11,len(_data)):
        _data['RSI'][_day] = 100 - (100/ (1+_data['RS'][_day]))
    return _data    
    
def pltRsi(data):
    fig,axs = plt.subplots(2, sharex=True, figsize=(13,9))
    fig.suptitle('BTC Stock Price (top) - 10 day RSI (bottom)')
    axs[0].plot(data['Adj Close'])
    axs[1].plot(data['RSI'])
    axs[0].grid()
    axs[1].grid()
    

def calculateSignals(data):
    _data = data
    for _day in range(11,len(_data)):
        _previousDay = _day - 1
        # Calculate "Long Tomorrow" column
        if ((_data['RSI'][_day]<=30) & (_data['RSI'][_previousDay]>30)):
            _data['Long Tomorrow'][_day] = True
        elif ((_data['Long Tomorrow'][_previousDay]==True) & (_data['RSI'][_day]<=70)):
            _data['Long Tomorrow'][_day] = True
        else:
            _data['Long Tomorrow'][_day] = False
        
        # Calculate "Buy Signal" column
        if ((_data['Long Tomorrow'][_day]==True) & (_data['Long Tomorrow'][_previousDay]==False)):
            _data['Buy Signal'][_day] = _data['Adj Close'][_day]
            _data['Buy RSI'][_day] = _data['RSI'][_day]

        # Calculate "Sell Signal" column
        if((_data['Long Tomorrow'][_day]==False) & (_data['Long Tomorrow'][_previousDay]==True)):
            _data['Sell Signal'][_day] = _data['Adj Close'][_day]
            _data['Sell RSI'][_day] = _data['RSI'][_day]
        
    ## Calculate Strategy Perfomance
    _data['Strategy'][11] = _data['Adj Close'][11]

    for _day in range(12,len(_data)):
        _previousDay = _day - 1 
        if _data['Long Tomorrow'][_previousDay]==True:
            _data['Strategy'][_day] = _data['Strategy'][_previousDay] * ( _data['Adj Close'][_day] / _data['Adj Close'][_previousDay])
        else:
            _data['Strategy'][_day] = _data['Strategy'][_previousDay]
    
    return _data 


def pltSignals(data):
    _data = data
    fig, axs = plt.subplots(2, sharex=True, figsize=(13,9))
    fig.suptitle('Stock price(top) & 10day RSI(bottom)')

    ## Chart the stock close price & buy/sell signals:
    axs[0].scatter(_data.index, _data['Buy Signal'], color='green', marker='^', alpha=1)
    axs[0].scatter(_data.index, _data['Sell Signal'], color='red', marker='v', alpha=1)

    axs[0].plot(_data['Adj Close'], alpha = 0.8)
    axs[0].grid()

    ## Chart RSI & buy/sell signals:
    axs[1].scatter(_data.index, _data['Buy RSI'], color='green', marker='^', alpha=1)
    axs[1].scatter(_data.index, _data['Sell RSI'], color='red', marker='v', alpha=1)

    axs[1].plot(_data['RSI'], alpha = 0.8)
    axs[1].grid()
    return _data

def calculateRsi(data):
    data = fillMoves(data)
    for _day in range (1,len(data)):
        if(~(data['Down Move'][_day]>0)):
            data['Down Move'][_day]=0
    data = fillRsi(data)
    return data

def rsi(name, data_, end):
    data = data_
    
    data['Down Move'] = np.nan
    data['Average Up'] = np.nan
    data['Average Down'] = np.nan
        
        # Relative Strength
    data['RS'] = np.nan

        # Relative Strength Index
    data['RSI'] = np.nan

    data = calculateRsi(data)

    pltRsi(data)

    # Calculate the buy & sell signals
    ## Initialize the columns that we need
    data['Long Tomorrow'] = np.nan
    data['Buy Signal'] = np.nan
    data['Sell Signal'] = np.nan
    data['Buy RSI'] = np.nan
    data['Sell RSI'] = np.nan
    data['Strategy'] = np.nan

    
    data = calculateSignals(data)
    pltSignals(data)
    ## Trade Performance
    trade_count = data['Buy Signal'].count()

    ## Avg Profit per trade

    average_profit = ((data['Strategy'][-1] / data['Strategy'][11]) ** (1/trade_count)) - 1

    ## Number of days per trade
    total_days = data['Long Tomorrow'].count()
    average_days = int(total_days/trade_count)

    print('Strategy yield', trade_count, 'trades')
    print('Avrage trade lasted', average_days, 'days per trade')
    print('Average profit per trade was', average_profit*100, '%')
    #data.to_excel("RSI_data_table.xlsx")

def get_data(name_, start_, end_):
    data = yf.download(name_, start=start_, end=end_)
    return data

time = datetime.now()
dt_string = time.strftime("%Y-%m-%d")

name = sys.argv[1]
start = sys.argv[2]
end = str(dt_string)  #sell "2021-04-29" #buy "2020-06-04"

data = get_data(name,start,end)

rsi(name,data,end)
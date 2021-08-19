import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


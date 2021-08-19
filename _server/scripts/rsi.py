import json
import pandas as pd
import numpy as np

from datetime import datetime
import sys

import requests
import yfinance as yf
#nt = None  # default='warn'

#pd.options.mode.chained_assignment = None  # default='warn'

   
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

    

def calculateSignals(id_, name_, data):
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
        
        hodling = hodling_check(id_,"RSI")
        # Calculate "Buy Signal" column
        if ((_data['Long Tomorrow'][_day]==True) & (_data['Long Tomorrow'][_previousDay]==False)):
            _data['Buy Signal'][_day] = _data['Adj Close'][_day]
            _data['Buy RSI'][_day] = _data['RSI'][_day]
            time = datetime.now()
            print('BUYYYY!!!!! RSII !!!!!')
            print('Bought at the price of:', _data['Close'][_day],'$')
            r = requests.post('http://localhost:3014/api/order', json={
                "wallet_id" : id_,
                "timestamp" : str(time),
                "type": "BUY",
                "name": name_,
                "quantity": str(float(get_wallet_balance(id_,"RSI"))/_data['Close'][_day]),
                "price":float(_data['Close'][_day]),
                "method":"RSI"
            })
            buying_rebalance(id_, _data['Close'][_day],str(float(get_wallet_balance(id_,"RSI"))/_data['Close'][_day]), "RSI")
            print(r.json())
            hodling = True

        # Calculate "Sell Signal" column
        if hodling==True:
            if((_data['Long Tomorrow'][_day]==False) & (_data['Long Tomorrow'][_previousDay]==True)):
                _data['Sell Signal'][_day] = _data['Adj Close'][_day]
                _data['Sell RSI'][_day] = _data['RSI'][_day]
                print('SELLLLLL!!!! RSI!!!')
                print('Sold at the price of:', _data['Close'][_day])
                time = datetime.now()
                quantity = get_wallet_quantity(id_,"RSI")
                r = requests.post('http://localhost:3014/api/order', json={
                    "wallet_id" : id_,
                    "timestamp" : str(time),
                    "type": "SELL",
                    "name": name_,
                    "quantity": str(quantity),
                    "price":float(_data['Close'][_day]),
                    "method":"RSI"
                })
                selling_rebalance(id_,str(float(quantity)*float(_data['Close'][_day])),"RSI")
                hodling=False

        
    ## Calculate Strategy Perfomance
    _data['Strategy'][11] = _data['Adj Close'][11]

    for _day in range(12,len(_data)):
        _previousDay = _day - 1 
        if _data['Long Tomorrow'][_previousDay]==True:
            _data['Strategy'][_day] = _data['Strategy'][_previousDay] * ( _data['Adj Close'][_day] / _data['Adj Close'][_previousDay])
        else:
            _data['Strategy'][_day] = _data['Strategy'][_previousDay]
    
    return _data 


def calculateRsi(data):
    data = fillMoves(data)
    for _day in range (1,len(data)):
        if(~(data['Down Move'][_day]>0)):
            data['Down Move'][_day]=0
    data = fillRsi(data)
    return data


def create_wallet(id_,name, balance, method):
    requests.post('http://localhost:3014/api/createWallet', json={"id":id_,"name":name,"balance":balance,"method":method})

def get_wallet_balance(id_,method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"id":id_, "method":method})
    return r.json()['data'][0]['balance']

def buying_rebalance(id_,buying_price, quantity, method):
    balance = float(get_wallet_balance(id_,method))
    rebalance1 = balance/buying_price
    rebalance = float(balance - (rebalance1*float(buying_price)))
    if rebalance < 1:
        rebalance = "0"
    requests.post('http://localhost:3014/api/rebalance', json={"rebalance": rebalance, "quantity":quantity, "method":method})

def selling_rebalance(id_,revenue, method):
    balance = get_wallet_balance(id_,method)
    rebalance = float(balance) + float(revenue)
    requests.post('http://localhost:3014/api/rebalance', json={"rebalance": rebalance, "quantity":"0", "method":method})

def get_wallet_quantity(id_,method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"id":id_, "method":method})
    return r.json()['data'][0]['quantity']

def hodling_check(id_,method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"id":id_, "method":method})
    if int(r.json()['data'][0]['quantity']) == 0 and int(r.json()['data'][0]['balance'])!=0:
        return False
    else:
        return True


def rsi(id_, name_, data_, end):
    data = data_
    
    data['Down Move'] = np.nan
    data['Average Up'] = np.nan
    data['Average Down'] = np.nan
        
        # Relative Strength
    data['RS'] = np.nan

        # Relative Strength Index
    data['RSI'] = np.nan

    data = calculateRsi(data)

   

    # Calculate the buy & sell signals
    ## Initialize the columns that we need
    data['Long Tomorrow'] = np.nan
    data['Buy Signal'] = np.nan
    data['Sell Signal'] = np.nan
    data['Buy RSI'] = np.nan
    data['Sell RSI'] = np.nan
    data['Strategy'] = np.nan

    
    data = calculateSignals(id_, name_, data)
    
    ### Trade Performance
    #trade_count = data['Buy Signal'].count()
#
    ### Avg Profit per trade
#
    #average_profit = ((data['Strategy'][-1] / data['Strategy'][11]) ** (1/trade_count)) - 1
#
    ### Number of days per trade
    #total_days = data['Long Tomorrow'].count()
    #average_days = int(total_days/trade_count)
#
    #print('Strategy yield', trade_count, 'trades')
    #print('Avrage trade lasted', average_days, 'days per trade')
    #print('Average profit per trade was', average_profit*100, '%')
    ##data.to_excel("RSI_data_table.xlsx")

def get_data(name_, start_, end_):
    data = yf.download(name_, start=start_, end=end_)
    return data

time = datetime.now()
dt_string = time.strftime("%Y-%m-%d")


id_ = sys.argv[1]
name = sys.argv[2]
start = sys.argv[3]
end = str(dt_string)  #sell "2021-04-29" #buy "2020-06-04"

data = get_data(name,start,end)

rsi(id_,name,data,end)
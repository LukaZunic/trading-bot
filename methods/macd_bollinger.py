import numpy as np
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import sys

def get_data(name_, start_, end_):
    data = yf.download(name_, start=start_, end=end_)
    return data

def get_last_date(end):
    last_date = end
    day = str(last_date[-2] + last_date[-1])
    month = str(last_date[-5] + last_date[-4])
    year = str(last_date[2] + last_date[3])
    if day=='01' and month=='01':
        year=str(int(year)-1)
        day='31'
        month='12'
    else:
        if day=='01':
            if month=='03':
                if int(year)%4==0:
                    month='02'
                    day='29'
                else:
                    month='02'
                    day='28'
            elif month=='02' or month=='04' or  month=='06' or month=='08' or month=='09' or month=='11':
                month=str(int(month)-1)
                day='31'
            else:
                month=str(int(month)-1)
                day='30'
        else:
            if int(day)<=10:
                day = '0' + str(int(day)-1)
            else:
                day = str(int(day)-1)


    last_date_with_value = str('20' + year + '-' + month + '-' + day)
    return last_date_with_value



def get_latest_data(data, last_date_with_value):
    curr_close_price = data.loc[last_date_with_value]['Close']
    curr_span_a = data.loc[last_date_with_value]['senkou_span_A']
    curr_span_b = data.loc[last_date_with_value]['senkou_span_B']
    curr_kijun = data.loc[last_date_with_value]['kijun_sen']
    curr_tenkan = data.loc[last_date_with_value]['tenkan_sen']
    return curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan



def macd_buy_sell_check(id_,data,end,hodling):
    last_date = get_last_date(end)
    date_before_last = get_last_date(last_date)
    curr_macd_line = data.loc[last_date]['macd']
    curr_signal_line = data.loc[last_date]['signal_line']
    prev_macd_line = data.loc[date_before_last]['macd']
    prev_signal_line = data.loc[date_before_last]['signal_line']
    if prev_macd_line == prev_signal_line or abs(prev_macd_line - prev_signal_line) < 0.8:
        if curr_macd_line < curr_signal_line:
                return 'Sell'
        else:
            return 'Buy'
    else:
        return 'Wait'

def bollinger_macd_buy_sell(id_,name, data, end):
    hodling = hodling_check(id_,"BB & MACD")
    check_macd = macd_buy_sell_check(id_,data, end, hodling)
    last_date = get_last_date(end)
    distance = abs(data.loc[last_date]['upper_band'] - data.loc[last_date]['lower_band'])
    curr_close = data.loc[last_date]['Close']
    if check_macd == 'Buy':
        if data.loc[last_date]['Close'] < data.loc[last_date]['upper_band'] and data.loc[last_date]['Close'] > (data.loc[last_date]['upper_band']-(distance/3)):
            print("BUUUUYYY!!!!")
            time = datetime.now()
            r = requests.post('http://localhost:3014/api/order', json={
                    "wallet_id": id_,
                    "timestamp": str(time),
                    "type":"BUY",
                    "name": name,
                    "quantity": str(float(get_wallet_balance(id_,"BB & MACD"))/curr_close),
                    "price":float(curr_close),
                    "method": "BB & MACD"
            })
            buying_rebalance(id_,curr_close, str(float(get_wallet_balance(id_,"BB & MACD"))/curr_close), "BB & MACD")
            hodling = True
        else:
            print("MACD says buy, but must waiting for BB confirmation!")
    elif check_macd == 'Sell':
        if data.loc[last_date]['Close'] > data.loc[last_date]['lower_band'] and data.loc[last_date]['Close'] < ((distance/3)+data.loc[last_date]['lower_band']):
            if hodling == True:
                print("SEEELLLL!!!!")
                time = datetime.now()
                quantity = get_wallet_quantity(id_,"BB & MACD")
                r = requests.post('http://localhost:3014/api/order', json={
                    "wallet_id": id_,
                    "timestamp": str(time),
                    "type":"SELL",
                    "name": name,
                    "quantity": str(quantity),
                    "price": float(curr_close),
                    "method": "BB & MACD"
                })
                selling_rebalance(id_,str(float(quantity)*float(curr_close)),"BB & MACD")
                hodling = False
            else:
                print("U dont own any coins/stocks atm to sell!")
        else:
            print("MACD says sell, but must waiting for BB confirmation!")
    else:
        print('Wait, still speculating!')


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

time = datetime.now()
dt_string = time.strftime("%Y-%m-%d")

id_ = sys.argv[1]
name = sys.argv[2]
start = sys.argv[3]
end = str(dt_string)  #sell "2021-04-29" #buy "2020-06-04"

data = get_data(name, start, end)

data['MA_20'] = (data['High'].rolling(window=20).mean() + data['Low'].rolling(window=20).mean() + data['Close'].rolling(window=20).mean())/3
data['STD_20'] = (data['High'].rolling(window=20).std() + data['Low'].rolling(window=20).std() + data['Close'].rolling(window=20).std())/3
data['upper_band'] = data['MA_20'] + (data['STD_20']*2)
data['lower_band'] = data['MA_20'] - (data['STD_20']*2)

data['12_period_ema'] = (data['High'].ewm(span=12, adjust=False).mean() + data['Low'].ewm(span=12, adjust=False).mean() + data['Close'].ewm(span=12, adjust=False).mean())/3
data['26_period_ema'] = (data['High'].ewm(span=26, adjust=False).mean() + data['Low'].ewm(span=26, adjust=False).mean() + data['Close'].ewm(span=26, adjust=False).mean())/3
data['macd'] = data['12_period_ema'] - data['26_period_ema']
data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()

bollinger_macd_buy_sell(id_,name, data, end)
import numpy as np
from numpy.core.fromnumeric import take
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


def macd_buy_sell(id_,name, end, stop_loss, take_profit, data):
    hodling = hodling_check(id_, "MACD")
    last_date = get_last_date(end)
    date_before_last = get_last_date(last_date)
    curr_macd_line = data.loc[last_date]['macd']
    curr_signal_line = data.loc[last_date]['signal_line']
    curr_close = data.loc[last_date]['Close']
    prev_macd_line = data.loc[date_before_last]['macd']
    prev_signal_line = data.loc[date_before_last]['signal_line']
    balance = get_wallet_balance(id_,"MACD")
    
    if str(balance) <= str(stop_loss) or str(balance) >= str(take_profit):
        print("TERMINATE TRADING BOT")
    if prev_macd_line == prev_signal_line or abs(prev_macd_line - prev_signal_line) < 0.5:
        if curr_macd_line < curr_signal_line:
            if hodling==True:
                print("SELL!")
                print('Sold at the price of:',curr_close,'$')
                time = datetime.now()
                quantity = get_wallet_quantity(id_,"MACD")
                r = requests.post('http://localhost:3014/api/order', json={
                    "wallet_id": id_,
                    "timestamp": str(time),
                    "type":"SELL",
                    "name": name,
                    "quantity": str(quantity),
                    "price": float(curr_close),
                    "method": "MACD"
                })
                selling_rebalance(id_, str(float(quantity)*float(curr_close)),"MACD")
                hodling=False
        else:
            if hodling==False:
                print("BUY!")
                print('Bought at the price of:',curr_close,'$')
                time = datetime.now()
                r = requests.post('http://localhost:3014/api/order', json={
                        "wallet_id": id_,
                        "timestamp": str(time),
                        "type":"BUY",
                        "name": name,
                        "quantity": str(float(get_wallet_balance(id_,"MACD"))/curr_close),
                        "price":float(curr_close),
                        "method": "MACD"
                })
                buying_rebalance(id_,curr_close, str(float(get_wallet_balance(id_,"MACD"))/curr_close), "MACD")
                hodling=True
            else:
                print("ALREADY HODLING!")
    else:
        print("Still watching the trend. Nothing to trade atm!")

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
    requests.post('http://localhost:3014/api/rebalance', json={"id": id_, "rebalance": rebalance, "quantity":quantity, "method":method})

def selling_rebalance(id_,revenue, method):
    balance = get_wallet_balance(id_,method)
    rebalance = float(balance) + float(revenue)
    requests.post('http://localhost:3014/api/rebalance', json={"id": id_, "rebalance": rebalance, "quantity":"0", "method":method})

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
stop_loss = sys.argv[4]
take_profit = sys.argv[5]
end = str(dt_string)  #sell "2020-06-27" #buy "2020-05-08"

data = get_data(name, start, end)
data['12_period_ema'] = (data['High'].ewm(span=12, adjust=False).mean() + data['Low'].ewm(span=12, adjust=False).mean() + data['Close'].ewm(span=12, adjust=False).mean())/3
data['26_period_ema'] = (data['High'].ewm(span=26, adjust=False).mean() + data['Low'].ewm(span=26, adjust=False).mean() + data['Close'].ewm(span=26, adjust=False).mean())/3
data['macd'] = data['12_period_ema'] - data['26_period_ema']
data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()

macd_buy_sell(id_, name, end, stop_loss, take_profit, data)
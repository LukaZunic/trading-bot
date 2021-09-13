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

def stoppers_check(id_, stop_loss, take_profit, curr_close_price):

    curr_close = curr_close_price
    balance = get_wallet_balance(id_,"ICHIMOKU CLOUD")
    if float(balance) == 0:
        quantity = get_wallet_quantity(id_,"ICHIMOKU CLOUD")
        if (float(quantity) * float(curr_close)) >= float(take_profit) or (float(quantity) * float(curr_close)) <= float(stop_loss):
            print("TERMINATE TRADING BOT")
            time = datetime.now()
            quantity = get_wallet_quantity(id_,"ICHIMOKU CLOUD")
            r = requests.post('http://localhost:3014/api/order', json={
                    "wallet_id": id_,
                    "timestamp": str(time),
                    "type":"SELL",
                    "name": name,
                    "quantity": str(quantity),
                    "price": float(curr_close_price),
                    "method": "ICHIMOKU CLOUD"
            })
            selling_rebalance(id_,str(float(quantity)*float(curr_close_price)),"ICHIMOKU CLOUD")
        else:
            print("RUNNING 1")
    else:
        if float(balance)>=float(take_profit) or float(balance)<=float(stop_loss):
            print("TERMINATE TRADING BOT")
        else:
            print("RUNNING 2")

def ichimoku_cloud_buy_sell(id_,stop_loss, take_profit, name, curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan):
    hodling = hodling_check(id_,"ICHIMOKU CLOUD")
    stoppers_check(id_,stop_loss, take_profit, curr_close_price)
    if curr_close_price > curr_span_a and curr_close_price > curr_span_b:
        if curr_tenkan-curr_kijun >= 0 and curr_tenkan-curr_kijun <= 2.5:
            if hodling==False:
                print("BUY SIGNAL TRIGGERED!")
                print('Bought at the price of:',curr_close_price,'$')
                time = datetime.now()
                r = requests.post('http://localhost:3014/api/order', json={
                        "wallet_id": id_,
                        "timestamp": str(time),
                        "type":"BUY",
                        "name": name,
                        "quantity": str(float(get_wallet_balance(id_,"ICHIMOKU CLOUD"))/curr_close_price),
                        "price":float(curr_close_price),
                        "method": "ICHIMOKU CLOUD"
                })
                buying_rebalance(id_,curr_close_price, str(float(get_wallet_balance(id_,"ICHIMOKU CLOUD"))/curr_close_price), "ICHIMOKU CLOUD")
                print(r.json())
                hodling = True
            else:
                print("ALREADY HODLING!")
        else:
            print("Watch for conversion and base line! Might buy soon!")
    else:
        if hodling==True:
            if curr_close_price < curr_span_a and curr_close_price < curr_span_b:
                if curr_kijun-curr_tenkan >= 0 and curr_kijun-curr_tenkan <= 2.5:
                    print("SELL SIGNAL TRIGGERED!")
                    print('Sold at the price of:',curr_close_price,'$')
                    time = datetime.now()
                    quantity = get_wallet_quantity(id_,"ICHIMOKU CLOUD")
                    r = requests.post('http://localhost:3014/api/order', json={
                            "wallet_id": id_,
                            "timestamp": str(time),
                            "type":"SELL",
                            "name": name,
                            "quantity": str(quantity),
                            "price": float(curr_close_price),
                            "method": "ICHIMOKU CLOUD"
                    })
                    selling_rebalance(id_,str(float(quantity)*float(curr_close_price)),"ICHIMOKU CLOUD")
                    hodling=False
                else:
                    print("Watch for conversion and base line! Might sell soon!")
            else:
                print("Doing nothing, still above cloud!")
        else:
            print("Still waiting for a good opportunity!")

def get_latest_data(data, last_date_with_value):
    curr_close_price = data.loc[last_date_with_value]['Close']
    curr_span_a = data.loc[last_date_with_value]['senkou_span_A']
    curr_span_b = data.loc[last_date_with_value]['senkou_span_B']
    curr_kijun = data.loc[last_date_with_value]['kijun_sen']
    curr_tenkan = data.loc[last_date_with_value]['tenkan_sen']
    return curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan


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
end = str(dt_string)  #sell "2020-08-19" #buy "2020-07-07"

#id_= "testing"
#name = "ADA-USD"
#start = "2020-01-01"
#stop_loss = 40000
#take_profit = 100000
#end = "2021-06-11" #"2020-06-01"

data = get_data(name, start, end)
index = pd.date_range(end, periods=25, freq='D')
columns = data.columns
data_pred = pd.DataFrame(index=index, columns=columns)
data = pd.concat([data,data_pred])

data['tenkan_sen'] = (data['High'].rolling(window = 9).max() + data['Low'].rolling(window = 9).min()) / 2
data['kijun_sen'] = (data['High'].rolling(window = 26).max() + data['Low'].rolling(window = 26).min()) / 2
data['senkou_span_A'] = ((data['tenkan_sen'] + data['kijun_sen']) / 2).shift(26)
data['senkou_span_B'] = ((data['High'].rolling(window=52).max() + data['Low'].rolling(window=52).min()) / 2).shift(26)
data['chikou_span'] = data['Close'].shift(-26)

last_date_with_value = get_last_date(end)

curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan = get_latest_data(data,last_date_with_value)
ichimoku_cloud_buy_sell(id_,stop_loss, take_profit,name, curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan)
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import sys

def get_data(name_, start_, end_):
    data = yf.download(name_, start=start_, end=end_)
    return data

def plot_data(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'], name = 'market data')
    )
    fig.update_layout(
        title='Live share price evolution',
        yaxis_title='Coin/Stock Price (US Dollars)'
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(step="all")
            ])
        )
    )
    fig.show()

def plot_ichimoku(data):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name = 'Market Data'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['tenkan_sen'],
        line=dict(
            color='royalblue',
            width=.8
        ),
        name = 'Tenkan Sen'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['kijun_sen'],
        line=dict(
            color='red',
            width=.8
        ),
        name = 'Kijun Sen'
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['senkou_span_A'],
        line=dict(
            color='black',
            width=.8
        ),
        name = 'Senkou Span A'
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['senkou_span_B'],
        line=dict(
            color='purple',
            width=.8
        ),
        name = 'Senkou Span B',
        fill = 'tonexty',
        fillcolor= 'lightgreen',
        opacity=0.01
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['chikou_span'],
        line=dict(
            color='orange',
            width=.8
        ),
        name = 'Chikou Span'
        )
    )


    fig.show()
    fig.write_html("./ichimoku.html")

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

def ichimoku_cloud_buy_sell(name, curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan):
    hodling = hodling_check("ICHIMOKU CLOUD")
    if curr_close_price > curr_span_a and curr_close_price > curr_span_b:
        if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
            print("BUUUUY!!!")
            print('Bought at the price of:',curr_close_price,'$')
            time = datetime.now()
            r = requests.post('http://localhost:3014/api/order', json={
                    "timestamp": str(time),
                    "type":"BUY",
                    "name": name,
                    "quantity": str(float(get_wallet_balance("ICHIMOKU CLOUD"))/curr_close_price),
                    "price":float(curr_close_price),
                    "method": "ICHIMOKU CLOUD"
            })
            buying_rebalance(curr_close_price, str(float(get_wallet_balance("ICHIMOKU CLOUD"))/curr_close_price), "ICHIMOKU CLOUD")
            print(r.json())
            hodling = True
        else:
            print("Watch for conversion and base line! Might buy soon!")
    else:
        if hodling==True:
            if curr_close_price < curr_span_a and curr_close_price < curr_span_b:
                if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
                    print("SEEEELLL!!!!")
                    print('Sold at the price of:',curr_close_price,'$')
                    time = datetime.now()
                    quantity = get_wallet_quantity("ICHIMOKU CLOUD")
                    r = requests.post('http://localhost:3014/api/order', json={
                            "timestamp": str(time),
                            "type":"SELL",
                            "name": name,
                            "quantity": str(quantity),
                            "price": float(curr_close_price),
                            "method": "ICHIMOKU CLOUD"
                    })
                    selling_rebalance(str(float(quantity)*float(curr_close_price)),"ICHIMOKU CLOUD")
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

def plot_bollinger(data):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name = 'Market Data'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['upper_band'],
        line=dict(
            color='blue',
            width=.8
        ),
        name = 'Upper Bollinger Band'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['lower_band'],
        line=dict(
            color='red',
            width=.8
        ),
        name = 'Lower Bollinger Band'
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_20'],
        line=dict(
            color='black',
            width=.8
        ),
        name = 'Moving average 20 period'
        )
    )
    

    fig.show()
    fig.write_html("./bollinger.html")

def plot_macd(data):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name = 'Market Data'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['macd'],
        line=dict(
            color='purple',
            width=.8
        ),
        name = 'MACD line'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['signal_line'],
        line=dict(
            color='green',
            width=.8
        ),
        name = 'Signal Line'
        )
    )

    fig.show()
    fig.write_html("./macd.html")

def macd_buy_sell(name, end, data):
    hodling = hodling_check("MACD")
    last_date = get_last_date(end)
    date_before_last = get_last_date(last_date)
    curr_macd_line = data.loc[last_date]['macd']
    curr_signal_line = data.loc[last_date]['signal_line']
    curr_close = data.loc[last_date]['Close']
    prev_macd_line = data.loc[date_before_last]['macd']
    prev_signal_line = data.loc[date_before_last]['signal_line']
    if prev_macd_line == prev_signal_line or abs(prev_macd_line - prev_signal_line) < 0.5:
        if curr_macd_line < curr_signal_line:
            if hodling==True:
                print("SEEEELLL!!!!")
                print('Sold at the price of:',curr_close,'$')
                time = datetime.now()
                quantity = get_wallet_quantity("MACD")
                r = requests.post('http://localhost:3014/api/order', json={
                    "timestamp": str(time),
                    "type":"SELL",
                    "name": name,
                    "quantity": str(quantity),
                    "price": float(curr_close),
                    "method": "MACD"
                })
                selling_rebalance(str(float(quantity)*float(curr_close)),"MACD")
                hodling=False
        else:
            if hodling==False:
                print("BUUUUUYY!!!!")
                print('Bought at the price of:',curr_close,'$')
                time = datetime.now()
                r = requests.post('http://localhost:3014/api/order', json={
                        "timestamp": str(time),
                        "type":"BUY",
                        "name": name,
                        "quantity": str(float(get_wallet_balance("MACD"))/curr_close),
                        "price":float(curr_close),
                        "method": "MACD"
                })
                buying_rebalance(curr_close, str(float(get_wallet_balance("MACD"))/curr_close), "MACD")
                hodling=True
            else:
                print("ALREADY HODLING!")
    else:
        print("Still watching the trend. Nothing to trade atm!")

def plot_bollinger_macd(data):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name = 'Market Data'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['macd'],
        line=dict(
            color='purple',
            width=.8
        ),
        name = 'MACD line'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['signal_line'],
        line=dict(
            color='green',
            width=.8
        ),
        name = 'Signal Line'
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['upper_band'],
        line=dict(
            color='blue',
            width=.8
        ),
        name = 'Upper Bollinger Band'
        )
    )

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['lower_band'],
        line=dict(
            color='red',
            width=.8
        ),
        name = 'Lower Bollinger Band'
        )
    )
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_20'],
        line=dict(
            color='black',
            width=.8
        ),
        name = 'Moving average 20 period'
        )
    )

    fig.show()
    fig.write_html("./bollinger-macd.html")

def macd_buy_sell_check(data,end,hodling):
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

def bollinger_macd_buy_sell(name, data, end):
    hodling = hodling_check("BB & MACD")
    check_macd = macd_buy_sell_check(data, end, hodling)
    last_date = get_last_date(end)
    distance = abs(data.loc[last_date]['upper_band'] - data.loc[last_date]['lower_band'])
    curr_close = data.loc[last_date]['Close']
    if check_macd == 'Buy':
        if data.loc[last_date]['Close'] < data.loc[last_date]['upper_band'] and data.loc[last_date]['Close'] > (data.loc[last_date]['upper_band']-(distance/3)):
            print("BUUUUYYY!!!!")
            time = datetime.now()
            r = requests.post('http://localhost:3014/api/order', json={
                    "timestamp": str(time),
                    "type":"BUY",
                    "name": name,
                    "quantity": str(float(get_wallet_balance("BB & MACD"))/curr_close),
                    "price":float(curr_close),
                    "method": "BB & MACD"
            })
            buying_rebalance(curr_close, str(float(get_wallet_balance("BB & MACD"))/curr_close), "BB & MACD")
            hodling = True
        else:
            print("MACD says buy, but must waiting for BB confirmation!")
    elif check_macd == 'Sell':
        if data.loc[last_date]['Close'] > data.loc[last_date]['lower_band'] and data.loc[last_date]['Close'] < ((distance/3)+data.loc[last_date]['lower_band']):
            if hodling == True:
                print("SEEELLLL!!!!")
                time = datetime.now()
                quantity = get_wallet_quantity("BB & MACD")
                r = requests.post('http://localhost:3014/api/order', json={
                    "timestamp": str(time),
                    "type":"SELL",
                    "name": name,
                    "quantity": str(quantity),
                    "price": float(curr_close),
                    "method": "BB & MACD"
                })
                selling_rebalance(str(float(quantity)*float(curr_close)),"BB & MACD")
                hodling = False
            else:
                print("U dont own any coins/stocks atm to sell!")
        else:
            print("MACD says sell, but must waiting for BB confirmation!")
    else:
        print('Wait, still speculating!')

def create_wallet(name, balance, method):
    requests.post('http://localhost:3014/api/createWallet', json={"name":name,"balance":balance,"method":method})

def get_wallet_balance(method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"method":method})
    return r.json()['data'][0]['balance']

def buying_rebalance(buying_price, quantity, method):
    balance = float(get_wallet_balance(method))
    rebalance1 = balance/buying_price
    rebalance = float(balance - (rebalance1*float(buying_price)))
    if rebalance < 1:
        rebalance = "0"
    requests.post('http://localhost:3014/api/rebalance', json={"rebalance": rebalance, "quantity":quantity, "method":method})

def selling_rebalance(revenue, method):
    balance = get_wallet_balance(method)
    rebalance = float(balance) + float(revenue)
    requests.post('http://localhost:3014/api/rebalance', json={"rebalance": rebalance, "quantity":"0", "method":method})

def get_wallet_quantity(method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"method":method})
    return r.json()['data'][0]['quantity']

def hodling_check(method):
    r = requests.get('http://localhost:3014/api/getWallet', json={"method":method})
    if int(r.json()['data'][0]['quantity']) == 0 and int(r.json()['data'][0]['balance']!=0):
        return False
    else:
        return True

time = datetime.now()
dt_string = time.strftime("%Y-%m-%d")

name = sys.argv[1]
start = sys.argv[2]
end = str(dt_string)  #sell "2020-06-27" #buy "2020-05-08"

data = get_data(name, start, end)
data['12_period_ema'] = (data['High'].ewm(span=12, adjust=False).mean() + data['Low'].ewm(span=12, adjust=False).mean() + data['Close'].ewm(span=12, adjust=False).mean())/3
data['26_period_ema'] = (data['High'].ewm(span=26, adjust=False).mean() + data['Low'].ewm(span=26, adjust=False).mean() + data['Close'].ewm(span=26, adjust=False).mean())/3
data['macd'] = data['12_period_ema'] - data['26_period_ema']
data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()


macd_buy_sell(name, end, data)
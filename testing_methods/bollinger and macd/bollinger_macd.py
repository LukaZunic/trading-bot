import numpy as np
import pandas as pd
import yfinance as yf
import functions as func

name = "NKLA"
start = "2020-03-25"
#end = "2020-06-04" #buying date
end = "2021-04-29" #selling date

data = func.get_data(name, start, end)
data['MA_20'] = (data['High'].rolling(window=20).mean() + data['Low'].rolling(window=20).mean() + data['Close'].rolling(window=20).mean())/3
data['STD_20'] = (data['High'].rolling(window=20).std() + data['Low'].rolling(window=20).std() + data['Close'].rolling(window=20).std())/3
data['upper_band'] = data['MA_20'] + (data['STD_20']*2)
data['lower_band'] = data['MA_20'] - (data['STD_20']*2)
data['12_period_ema'] = (data['High'].ewm(span=12, adjust=False).mean() + data['Low'].ewm(span=12, adjust=False).mean() + data['Close'].ewm(span=12, adjust=False).mean())/3
data['26_period_ema'] = (data['High'].ewm(span=26, adjust=False).mean() + data['Low'].ewm(span=26, adjust=False).mean() + data['Close'].ewm(span=26, adjust=False).mean())/3
data['macd'] = data['12_period_ema'] - data['26_period_ema']
data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()

func.bollinger_macd_buy_sell(name, data, end)
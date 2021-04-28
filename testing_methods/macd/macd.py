import numpy as np
import pandas as pd
import yfinance as yf
import functions as func

name = "NKLA"
start = "2020-01-01"
end = "2020-05-08" #date of buy
#end = "2020-06-27" #date of sell

data = func.get_data(name, start, end)
data['12_period_ema'] = (data['High'].ewm(span=12, adjust=False).mean() + data['Low'].ewm(span=12, adjust=False).mean() + data['Close'].ewm(span=12, adjust=False).mean())/3
data['26_period_ema'] = (data['High'].ewm(span=26, adjust=False).mean() + data['Low'].ewm(span=26, adjust=False).mean() + data['Close'].ewm(span=26, adjust=False).mean())/3
data['macd'] = data['12_period_ema'] - data['26_period_ema']
data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()

func.macd_buy_sell(name, end, data)
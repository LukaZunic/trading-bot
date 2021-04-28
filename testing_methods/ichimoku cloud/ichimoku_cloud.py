import plotly.graph_objs as go
import numpy as np
import pandas as pd
import yfinance as yf
import functions as func

name = "NKLA"
start = "2020-01-01"
#end = "2020-07-07" #znamo da bi tada bot kupio
end = "2020-08-19" #znamo da bi tada bot prodo

data = func.get_data(name, start, end)
index = pd.date_range(end, periods=25, freq='D') # datumi narednih 25 dana od zadnjeg dana u podacima
columns = data.columns
data_pred = pd.DataFrame(index=index, columns=columns) #prazna tablica za predikciju sljedecih 25 dana
data = pd.concat([data,data_pred])

data['tenkan_sen'] = (data['High'].rolling(window = 9).max() + data['Low'].rolling(window = 9).min()) / 2
data['kijun_sen'] = (data['High'].rolling(window = 26).max() + data['Low'].rolling(window = 26).min()) / 2
data['senkou_span_A'] = ((data['tenkan_sen'] + data['kijun_sen']) / 2).shift(26)
data['senkou_span_B'] = ((data['High'].rolling(window=52).max() + data['Low'].rolling(window=52).min()) / 2).shift(26)
data['chikou_span'] = data['Close'].shift(-26)

last_date_with_value = func.get_last_date(end)

curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan = func.get_latest_data(data,last_date_with_value)
func.ichimoku_cloud_buy_sell(name, curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan)
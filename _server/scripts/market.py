import yfinance as yf
from datetime import datetime

def get_data(name_, start_, end_):
    data = yf.download(name_, start=start_, end=end_)
    print(data)
    return data

time = datetime.now()
dt_string = time.strftime("%Y-%m-%d")

get_data('BTC-USD', "2020-01-01", dt_string)
get_data('ETH-USD', "2020-01-01", dt_string)
get_data('XRP-USD', "2020-01-01", dt_string)
get_data('DOGE-USD', "2020-01-01", dt_string)
get_data('BCH-USD', "2020-01-01", dt_string)
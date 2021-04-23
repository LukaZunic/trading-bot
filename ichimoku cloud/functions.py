import plotly.graph_objs as go
import numpy as np
import pandas as pd
import yfinance as yf

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
        title='Nikola Corporation live share price evolution',
        yaxis_title='NKLA Price (US Dollars)'
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
    fig.write_html("./ichimoku.html") #za laksi preview na netu

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
            day = str(int(day)-1)


    last_date_with_value = str('20' + year + '-' + month + '-' + day)
    return last_date_with_value

def ichimoto_cloud_buy_sell(curr_open_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan, hodling):
    if curr_open_price > curr_span_a and curr_open_price > curr_span_b:
        if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
            print("BUUUUY!!!")
            #INSERT BUYING CODE HERE
            hodling = True
        else:
            print("Watch for conversion and base line! Might buy soon!")
    else:
        if hodling==True:
            if curr_open_price < curr_span_a and curr_open_price < curr_span_b:
                if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
                    print("SEEEELLL!!!!")
                    #INSERT SELLING CODE HERE
                    hodling=False
                else:
                    print("Watch for conversion and base line! Might sell soon!")
            else:
                print("Doing nothing, still above cloud!")
        else:
            print("Still waiting for a good opportunity!")


def get_latest_data(data, last_date_with_value):
    curr_open_price = data.loc[last_date_with_value]['Open']
    curr_span_a = data.loc[last_date_with_value]['senkou_span_A']
    curr_span_b = data.loc[last_date_with_value]['senkou_span_B']
    curr_kijun = data.loc[last_date_with_value]['kijun_sen']
    curr_tenkan = data.loc[last_date_with_value]['tenkan_sen']
    return curr_open_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan
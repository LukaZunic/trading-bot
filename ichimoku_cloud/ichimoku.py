import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go


class Ichimoku:

    def get_data(self, name_, start_, end_):
        data = yf.download(name_, start=start_, end=end_)
        return data

    def plot_data(self, data):
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

    def plot_ichimoku(self, data):
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

    def get_last_date(self, end):
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

    def ichimoku_cloud_buy_sell(self, curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan, hodling):
        if curr_close_price > curr_span_a and curr_close_price > curr_span_b:
            if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
                print("BUUUUY!!!")
                print('Bought at the price of:',curr_close_price,'$')
                #INSERT BUYING CODE HERE
                hodling = True
            else:
                print("Watch for conversion and base line! Might buy soon!")
        else:
            if hodling==True:
                if curr_close_price < curr_span_a and curr_close_price < curr_span_b:
                    if abs(curr_kijun-curr_tenkan) >= 0 and abs(curr_kijun-curr_tenkan) <= 2.5:
                        print("SEEEELLL!!!!")
                        print('Sold at the price of:',curr_close_price,'$')
                        #INSERT SELLING CODE HERE
                        hodling=False
                    else:
                        print("Watch for conversion and base line! Might sell soon!")
                else:
                    print("Doing nothing, still above cloud!")
            else:
                print("Still waiting for a good opportunity!")


    def get_latest_data(self, data, last_date_with_value):
        curr_close_price = data.loc[last_date_with_value]['Close']
        curr_span_a = data.loc[last_date_with_value]['senkou_span_A']
        curr_span_b = data.loc[last_date_with_value]['senkou_span_B']
        curr_kijun = data.loc[last_date_with_value]['kijun_sen']
        curr_tenkan = data.loc[last_date_with_value]['tenkan_sen']
        return curr_close_price, curr_span_a, curr_span_b, curr_kijun, curr_tenkan

    def plot_bollinger(self, data):
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

    def plot_macd(self, data):
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


    def macd_buy_sell(self, end, data, hodling):
        last_date = self.get_last_date(end)
        date_before_last = self.get_last_date(last_date)
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
                    #INSERT SELL CODE HERE
                    hodling=False
            else:
                print("BUUUUUYY!!!!")
                print('Bought at the price of:',curr_close,'$')
                #INSERT BUYING CODE HERE
                hodling=True
        else:
            print("Still watching the trend. Nothing to trade atm!")


    def plot_bollinger_macd(self, data):
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


    def macd_buy_sell_check(self, data, end, hodling):
        last_date = self.get_last_date(end)
        date_before_last = self.get_last_date(last_date)
        curr_macd_line = data.loc[last_date]['macd']
        curr_signal_line = data.loc[last_date]['signal_line']
        prev_macd_line = data.loc[date_before_last]['macd']
        prev_signal_line = data.loc[date_before_last]['signal_line']
        if prev_macd_line == prev_signal_line or abs(prev_macd_line - prev_signal_line) < 0.5:
            if curr_macd_line < curr_signal_line:
                    return 'Sell'
            else:
                return 'Buy'
        else:
            return 'Wait'

    def bollinger_macd_buy_sell(self, data, end, hodling):
        check_macd = self.macd_buy_sell_check(data, end, hodling)
        last_date = self.get_last_date(end)
        distance = abs(data.loc[last_date]['upper_band'] - data.loc[last_date]['lower_band'])
        if check_macd == 'Buy':
            if data.loc[last_date]['Close'] > data.loc[last_date]['lower_band'] and data.loc[last_date]['Close'] < ((distance/4)+data.loc[last_date]['lower_band']):
                print("BUUUUYYY!!!!")
                #INSERT CODE TO BUY
                hodling = True
            else:
                print("MACD says buy, but must waiting for BB confirmation!")
        elif check_macd == 'Sell':
            if data.loc[last_date]['Close'] < data.loc[last_date]['upper_band'] and data.loc[last_date]['Close'] < ((distance/4)-data.loc[last_date]['lower_band']):
                if hodling == True:
                    print("SEEELLLL!!!!")
                    #INSERT CODE TO SELL
                    hodling = False
                else:
                    print("U dont own any coins/stocks atm to sell!")
        else:
            print('Wait, still speculating!')
import os, csv
import talib
import yfinance as yf
import pandas as pd
from flask import Flask, escape, request, render_template
import plotly.express as px
from plotly.offline import plot
from patterns import candlestick_patterns
import requests

app = Flask(__name__, static_folder='images')

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,mr;q=0.8',
            'cache-control': 'max-age=0'}

@app.route('/snapshot')
def snapshot():
    firstLine = True
    with open('datasets/NSE_Equity_Codes.csv') as f:
        for line in f:
            if firstLine:
                firstLine = False
                continue

            if "," not in line:
                continue

            symbol = line.split(",")[0] + ".NS"
            data = yf.download(symbol, start="2022-01-01")
            if len(data) > 1:
                data.to_csv('datasets/data/{}.csv'.format(symbol))

    return {
        "code": "success"
    }

@app.route('/')
def index():
    pattern  = request.args.get('pattern', False)
    stocks = {}
    
    firstLine = True
    with open('datasets/NSE_Equity_Codes.csv') as f:
        for row in csv.reader(f):
            if firstLine:
                firstLine = False
                continue
            stocks[row[0]] = {'company': row[1], 'security': row[0]}

    if pattern:
        for filename in os.listdir('datasets/data'):
            if '.zip' in filename or '.BO' in filename:
                continue
            #print(filename)
            df = pd.read_csv('datasets/data/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.csv')[0].replace('.NS', '')

            #try:
            results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
            last = results.tail(1).values[0]
            #stocks[symbol]['df'] = df
            #fig = px.line(df, x='Date', y='Close', title=f'Closing price of {stocks[symbol]["company"]}')
            # plot_div = plot(fig, output_type='div')
            # stocks[symbol]['plot_div'] = plot_div

            # if stocks[symbol]['security'].strip("*") + ".png" not in os.listdir('images'):
            #     url = "https://stockcharts.com/c-sc/sc?s={}.IN&p=D&b=5&g=0&i=0&r=1674715076850".format(stocks[symbol]['security'])
            #     response = requests.get(url, headers= headers)
            #     with open("images/{}.png".format(stocks[symbol]['security'].strip("*")), "wb") as f:
            #         f.write(response.content)

            if last > 0:
                stocks[symbol][pattern] = 'Bullish'
            elif last < 0:
                stocks[symbol][pattern] = 'Bearish'
            else:
                stocks[symbol][pattern] = None

            # except Exception as e:
            #     print('failed on filename: ', filename, e)
            #     break

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

if __name__ == '__main__':
    app.run(debug=True)

import os, csv
import talib
import yfinance as yf
import pandas as pd
from flask import Flask, escape, request, render_template
import plotly.express as px
from plotly.offline import plot
from patterns import candlestick_patterns

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    firstLine = True
    with open('datasets/BSE_Equity_Codes.csv') as f:
        for line in f:
            if firstLine:
                firstLine = False
                continue

            if "," not in line:
                continue

            symbol = line.split(",")[0] + ".BO"
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
    with open('datasets/BSE_Equity_Codes.csv') as f:
        for row in csv.reader(f):
            if firstLine:
                firstLine = False
                continue
            stocks[row[0]] = {'company': row[1], 'df' : None, 'plot_div' : None}

    if pattern:
        for filename in os.listdir('datasets/data'):
            df = pd.read_csv('datasets/data/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.csv')[0].strip('.BO')

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]
                stocks[symbol]['df'] = df
                fig = px.line(df, x='Date', y='Close', title=f'Closing price of {stocks[symbol]["company"]}')
                plot_div = plot(fig, output_type='div')
                stocks[symbol]['plot_div'] = plot_div

                if last > 0:
                    stocks[symbol][pattern] = 'Bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'Bearish'
                else:
                    stocks[symbol][pattern] = None

            except Exception as e:
                print('failed on filename: ', filename, e)
                break

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

if __name__ == '__main__':
    app.run(debug=True)

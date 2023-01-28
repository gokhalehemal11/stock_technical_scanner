# import talib
# import yfinance as yf

# data = yf.download("SPY", start="2020-01-01", end="2020-08-01")

# morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

# engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

# data['Morning Star'] = morning_star
# data['Engulfing'] = engulfing

# engulfing_days = data[data['Engulfing'] != 0]

# print(engulfing_days)


# from nse_stock_codes import nse_stock_codes
# for stock in nse_stock_codes:
#   print(stock)

# import os, csv
# import pandas as pd
# import plotly.express as px
# from plotly.offline import plot

# stocks = {}

# with open('datasets/BSE_Equity_Codes.csv') as f:
#     for row in csv.reader(f):

#         stocks[row[0]] = {'company': row[1], 'plot_div' : None}
#         #print(stocks)

# filenames = os.listdir('datasets/data')
# for filename in filenames[: len(filenames)//5]:
#     if '.zip' in filename:
#         continue
#     df = pd.read_csv('datasets/data/{}'.format(filename))
#     symbol = filename.split('.csv')[0].strip('.BO')

#     fig = px.line(df, x='Date', y='Close', title=f'Closing price of {stocks[symbol]["company"]}')
#     plot_div = plot(fig, output_type='div')
#     stocks[symbol]['plot_div'] = plot_div


# print(stocks)





# import requests
# import csv, os

# datalist = os.listdir('datasets/data')
# imagelist = os.listdir('images')

# stocks = {}
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'accept-encoding': 'gzip, deflate, br',
#             'accept-language': 'en-US,en;q=0.9,mr;q=0.8',
#             'cache-control': 'max-age=0'}
    
# firstLine = True
# with open('datasets/NSE_Equity_Codes.csv') as f:
#     for row in csv.reader(f):
#         if firstLine:
#             firstLine = False
#             continue
#         stocks[row[0]] = {'company': row[1], 'security': row[0]}

#     for filename in datalist:
#         if '.zip' in filename or '.BO' in filename:
#             continue
#         symbol = filename.split('.csv')[0].replace('.NS', '')
#         security = stocks[symbol]['security']

#         if '{}.png'.format(security) in imagelist:
#             continue

#         url = "https://stockcharts.com/c-sc/sc?s={}.IN&p=D&b=5&g=0&i=0&r=1674715076850".format(security)
#         response = requests.get(url, headers= headers)

#         with open("images/{}.png".format(security), "wb") as f:
#             f.write(response.content)



import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import csv
import pandas as pd
from gspread_dataframe import set_with_dataframe
import time
from done import done

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1gx7Og_9EwMIa0FUjRbJ-EgefFd0VRXDeltz8-obVFY0/edit?usp=sharing'

# Share spreadsheet it with the client email
spreadsheet = client.open_by_url(spreadsheet_url)

# Get the directory where the CSV files are stored
directory = 'datasets/data'

# loop through the csv files in the directory
for file in os.listdir(directory):
    if file.endswith(".csv"):
        # read the csv file as a dataframe
        if file in done:
            continue

        print(file)
        df = pd.read_csv('datasets/data/{}'.format(file))
        try:
            # add the worksheet with the name of the file
            worksheet = spreadsheet.add_worksheet(title=file.replace(".csv", ""), rows=len(df), cols=len(df.columns))
            # set the dataframe to the worksheet
            set_with_dataframe(worksheet, df)
            

        except Exception as e:
            print(file, e)
            time.sleep(1)

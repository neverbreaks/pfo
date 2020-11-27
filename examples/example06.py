import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from pfo.market_data import download, Source, clean_data
from pfo.portfolio.portfolio import Portfolio
from pfo.portfolio.valuations import pf_valuation

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)

#
# for i in range(10000):
#     v = random_weights(44)
#     print(v)
start_date = datetime.datetime(2017, 11, 24)
end_date = datetime.datetime(2020, 11, 24)
path = (Path.cwd() /'..' / "cache" / "data.csv").resolve()
data = pd.read_csv(path, index_col = 0,  parse_dates=['Date'])

tickers = ['CSCO', 'V', 'ABBV', 'SBUX', 'MCD', 'INTC', \
           'GM', 'HPQ', 'EA', 'FDX', 'NKE', 'BERY', \
           'GOOGL', 'GOOG', 'WMT', 'NVDA', 'TSLA', 'GE', \
           'AAL', 'AMD', 'ADBE', 'AMZN', 'PYPL', 'MSFT', \
           'ATVI', 'FB', 'NEM', 'NFLX', 'AVGO', \
           'QCOM', 'BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
           'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
           'DIS', 'PFE', 'BMY']
#
# tickers = ['BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
#            'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
#            'DIS', 'PFE', 'BMY']

#tickers = ['AKRN', 'PIKK', 'PLZL', 'SELG']


data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)
data = clean_data(data)
#data.to_csv(path)
#
#
pf = Portfolio(data=data, risk_free_rate=0.01, freq=252)
pf.mc_simulation()
pf.plot_mc_simulation()
pf.print_mc_results()
plt.show()

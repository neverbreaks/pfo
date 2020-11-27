import datetime
import matplotlib.pyplot as plt
from pfo.stocks.ratios import ratios
from pfo.portfolio.portfolio import portfolio
import pandas as pd
import numpy as np

from pfo.market_data import download, Source, clean_data

start_date = datetime.datetime(2017, 11, 20)
end_date = '2020-11-20'

tickers = ['CSCO', 'V', 'ABBV', 'SBUX', 'MCD', 'INTC', \
           'GM', 'HPQ', 'EA', 'FDX', 'NKE', 'BERY', \
           'GOOGL', 'GOOG', 'WMT', 'NVDA', 'TSLA', 'GE', \
           'AAL', 'AMD', 'ADBE', 'AMZN', 'PYPL', 'MSFT', \
           'ATVI', 'FB', 'NEM', 'NFLX', 'AVGO', \
           'QCOM', 'BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
           'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
           'DIS', 'PFE', 'BMY']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)
data = clean_data(data)
pf = portfolio(data=data, risk_free_rate=0.001, freq=252)

msr = pf.max_sharpe_ratio()
pf1 = portfolio(data=data, weights=msr['x'], risk_free_rate=0.001, freq=252)
msr1 = pf1.max_sharpe_ratio()
print(np.round(msr['x'],decimals = 4))
print(np.round(msr1['x'],decimals = 4))

#print(pf.sharp)
#print(pf.sortino)

#pf.print_pf_result()
#pf1.print_pf_result()

plt.show()


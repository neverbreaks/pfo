import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from pfo.market_data import download, Source, clean_data
from pfo.portfolio import portfolio
from pfo.efficient_frontier import efficient_frontier
from pfo.quants import pf_valuation


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)

start_date = datetime.datetime(2017, 11, 20)
end_date = datetime.datetime(2020, 11, 10)
# path = (Path.cwd() /'..' / "cache" / "data.csv").resolve()
# data = pd.read_csv(path, index_col = 0,  parse_dates=['Date'])

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

#tickers = ['AAPL', 'TSLA', 'AMD', 'AMZN']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)
data = clean_data(data)
# data.to_csv(path)


pf = portfolio(data=data, risk_free_rate=0.001, freq=252, num_portfolios=1000)
pf.plot_portfolios()
pf.print_results()

ef = efficient_frontier(data=data)
msr = ef.max_sharpe_ratio()
mv = ef.min_volatility()

res = pf_valuation(msr['x'], data=data)
print(res)
print(np.round(msr['x'],decimals = 4))

#ef.efficient_portfolios()

plt.show()

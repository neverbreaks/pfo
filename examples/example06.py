import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pfo.market_data import download, Source, clean_data
from pfo.portfolio import portfolio
from pfo.efficient_frontier import efficient_frontier


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)

start_date = datetime.datetime(2017, 11, 20)
end_date = datetime.datetime(2020, 11, 19)


tickers = ['CSCO', 'V', 'ABBV', 'SBUX', 'MCD', 'INTC', \
           'GM', 'HPQ', 'EA', 'FDX', 'NKE', 'BERY', \
           'GOOGL', 'GOOG', 'WMT', 'NVDA', 'TSLA', 'GE', \
           'AAL', 'AMD', 'ADBE', 'AMZN', 'PYPL', 'MSFT', \
           'ATVI', 'FB', 'NEM', 'NFLX', 'AVGO', \
           'QCOM', 'BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
           'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
           'DIS', 'PFE', 'BMY']

tickers = ['BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
           'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
           'DIS', 'PFE', 'BMY']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)


pf = portfolio(data=data, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf.plot_portfolios()
pf.print_results()

ef = efficient_frontier(data=data)
msr = ef.max_sharpe_ratio()
mv = ef.min_volatility()
print(msr)
print(mv)
ef.efficient_portfolios()

plt.show()

import datetime
import matplotlib.pyplot as plt
from pfo.data_utils import clean_data
from pfo.stocks import ratios
from pfo.portfolio import portfolio
import pandas as pd

from pfo.market_data import download, Source

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
df_ratios = ratios(data=data)
df_sharp = df_ratios[df_ratios['Sharp Ratio'] > 1.0]
df_sortino = df_ratios[df_ratios['Sortino Ratio'] > 1.0]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_sharp)
    print(df_sortino)

pf_stocks_sortino = df_sortino.index.to_list()
pf_stocks_sharp = df_sortino.index.to_list()

sortino_data = download(source=Source.YFINANCE, tickers = pf_stocks_sortino, start_date=start_date, end_date=end_date)
sortino_data = clean_data(sortino_data)
pf_sortino = portfolio(data=sortino_data, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf_sortino.plot_portfolios()

pf_sortino.print_results()

sharp_data = download(source=Source.YFINANCE, tickers = pf_stocks_sharp, start_date=start_date, end_date=end_date)
sharp_data = clean_data(sharp_data)
pf_sharp = portfolio(data=sharp_data, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf_sharp.plot_portfolios()
plt.show()
pf_sharp.print_results()

plt.show()


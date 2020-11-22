import datetime
import matplotlib.pyplot as plt
from pfo.stocks import ratios, yearly_returns
from pfo.quants import portfolio_yearly_returns, portfolio_valuation
from pfo.portfolio import portfolio
import pandas as pd
import numpy as np
from pfo.market_data import download, Source, clean_data



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)



start_date14_17 = datetime.datetime(2014, 11, 20)
end_date14_17 = datetime.datetime(2017, 11, 19)

start_date17_20 = datetime.datetime(2017, 11, 20)
end_date17_20 = datetime.datetime(2020, 11, 19)


tickers = ['CSCO', 'V', 'ABBV', 'SBUX', 'MCD', 'INTC', \
           'GM', 'HPQ', 'EA', 'FDX', 'NKE', 'BERY', \
           'GOOGL', 'GOOG', 'WMT', 'NVDA', 'TSLA', 'GE', \
           'AAL', 'AMD', 'ADBE', 'AMZN', 'PYPL', 'MSFT', \
           'ATVI', 'FB', 'NEM', 'NFLX', 'AVGO', \
           'QCOM', 'BABA', 'MA', 'AAPL', 'BA', 'TWTR', \
           'MU', 'T', 'F', 'BIDU', 'BIIB', 'XOM', \
           'DIS', 'PFE', 'BMY']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date14_17, end_date=end_date14_17)
data = clean_data(data)
df_ratios = ratios(data=data)
df_sortino = df_ratios[df_ratios['Sortino Ratio'] > 1.0]

pf_stocks_sortino = df_sortino.index.to_list()

print('=' * 80)
print('Sortino portfolio 14-17')

sortino_data14_17 = download(source=Source.YFINANCE, tickers = pf_stocks_sortino, start_date=start_date14_17, end_date=end_date14_17)
sortino_data14_17 = clean_data(sortino_data14_17)
pf_sortino14_17 = portfolio(data=sortino_data14_17, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf_sortino14_17.plot_portfolios()
pf_sortino14_17.print_results()
pf_proposed_sortino14_17 = pf_sortino14_17.max_sortino_port


print('=' * 80)
print('Sortino portfolio 17-20')
df_weights_sortino = pd.DataFrame(pf_proposed_sortino14_17, index = pf_stocks_sortino)
sortino_data17_20 = download(source=Source.YFINANCE, tickers = pf_stocks_sortino, start_date=start_date17_20, end_date=end_date17_20)
sortino_data17_20 = clean_data(sortino_data17_20)
pf_val1 = portfolio_valuation(weights=df_weights_sortino, data = sortino_data14_17)
pf_val2 = portfolio_valuation(weights=df_weights_sortino, data = sortino_data17_20)


stocks_yearly_returns = yearly_returns(sortino_data17_20)
returns = pd.concat([df_weights_sortino, stocks_yearly_returns],
                    keys=['Weights', 'Yearly returns'], join='inner', axis=1)
returns.columns = returns.columns.droplevel(1)
returns['Weighted return'] = returns['Weights'] * returns['Yearly returns']
ret17_20 = returns['Weighted return'].sum()
print(f'Yearly returns - 17 - 20 :{ret17_20}')

print(pf_val1)
print(pf_val2)

plt.show()

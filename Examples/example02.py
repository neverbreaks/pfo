import datetime
import matplotlib.pyplot as plt
from pfo.data_utils import clean_data
from pfo.portfolio import portfolio


from pfo.market_data import download, Source

start_date = datetime.datetime(2017, 11, 20)
end_date = '2020-11-20'

tickers_pf1 = ['AAPL', 'ADBE', 'AMZN', 'MA', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'PYPL', 'QCOM', 'TWTR']
tickers_pf2 = ['AVGO', 'BABA', 'DIS', 'FB', 'GOOG', 'GOOGL', 'MCD', 'NEM', 'SBUX', 'V', 'WMT']

data_pf1 = download(source=Source.YFINANCE, tickers = tickers_pf1, start_date=start_date, end_date=end_date)
data_pf1 = clean_data(data_pf1)
pf1 = portfolio(data=data_pf1, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf1.plot_portfolios()
plt.show()
pf1.print_results()


data_pf2 = download(source=Source.YFINANCE, tickers = tickers_pf2, start_date=start_date, end_date=end_date)
data_pf2 = clean_data(data_pf2)
pf2 = portfolio(data=data_pf2, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf2.plot_portfolios()
plt.show()
pf2.print_results()
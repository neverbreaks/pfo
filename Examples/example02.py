import datetime
import matplotlib.pyplot as plt
from pfo.data_utils import clean_data
from pfo.portfolio import portfolio


from pfo.market_data import download, Source

start_date = datetime.datetime(2017, 11, 20)
end_date = '2020-11-20'

tickers = ['AAPL', 'ADBE', 'AMZN', 'MA', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'PYPL', 'QCOM', 'TWTR']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)
data = clean_data(data)
pf = portfolio(data=data, risk_free_rate=0.001, freq=252, num_portfolios=10000)
pf.plot_portfolios()
plt.show()

pf.print_results()
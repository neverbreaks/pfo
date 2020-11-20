import datetime
import matplotlib.pyplot as plt
from pfo.data_utils import clean_data
from pfo.stocks import ratios

from pfo.market_data import download, Source

start_date = datetime.datetime(2015, 11, 20)
end_date = '2020-11-20'

tickers = ['AAPL', 'ADBE', 'AMZN', 'MA', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'PYPL', 'QCOM', 'TWTR']

data = download(source=Source.YFINANCE, tickers = tickers, start_date=start_date, end_date=end_date)
data = clean_data(data)
ratios(data=data)

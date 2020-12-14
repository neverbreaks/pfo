import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pfo.stocks.cluster import cluster_stocks
from pfo.stocks.stock import Stock
from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data

start_date = datetime.datetime(2018, 11, 20)
end_date = datetime.datetime(2020, 11, 20)

data = download(
    source=Source.MOEX, tickers=[], boards=[{"board": "TQBR", "shares": "shares"}]
)
data = clean_data(data)
data = data[start_date:end_date]
isnull = data.isnull().sum()
for ticker in data.columns:
    try:
        if isnull[ticker] > 50:
            data.drop(ticker, axis=1, inplace=True)
    except:
        pass

pf_stocks = []
for ticker in data.columns:
    stk = Stock(ticker=ticker, data=data)
    if stk.sharp >= 1.0 or stk.sortino >= 1.0:
        stk.plot_prices()
        pf_stocks.append(ticker)

data1 = pd.DataFrame(data, columns=pf_stocks)
pfs = cluster_stocks(data1, 7, verbose=True)

plt.show()

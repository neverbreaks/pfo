import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from pfo.stocks.cluster import cluster_stocks
from pfo.stocks.stock import stock


start_date = datetime.datetime(2019, 11, 20)
end_date = datetime.datetime(2020, 11, 20)
path = (Path.cwd() /'..' / "cache" / "moex.csv").resolve()
data = pd.read_csv(path, index_col = 0,  parse_dates=['TRADEDATE'])

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
    stk = stock(ticker=ticker, data=data)
    if stk.sharp>= 1.0 or stk.sortino >= 1.0:
        pf_stocks.append(ticker)

data1 = pd.DataFrame(data, columns=pf_stocks)
pfs = cluster_stocks(data1, 7, verbose=True)

plt.show()
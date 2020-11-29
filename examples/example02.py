import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pfo.pf.portfolio import Portfolio
from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data
from pfo.stocks.stock import stock


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 150)

start_date = datetime.datetime(2020, 8, 27)
end_date = datetime.datetime(2020, 11, 27)

data = download(
    source=Source.MOEX,
    tickers=["AFKS", "APTK", "LNZL", "MAGEP", "MRKS", "PLZL", "ROLO", "SELG"],
    board={"board": "TQBR", "shares": "shares"},
    start_date=start_date,
    end_date=end_date,
)
data = clean_data(data)

pf_stocks = []
for ticker in data.columns:
    stk = stock(ticker=ticker, data=data)
    stk.plot_prices()
    stk.plot_daily_returns()
    pf_stocks.append(ticker)

pf1 = Portfolio(data=data, risk_free_rate=0.01, freq=252)
pf1.mc_simulation(10000)
pf1.plot_mc_simulation()
pf1.print_mc_results()
msr1 = pf1.max_sharpe_ratio()
pf1.efficient_portfolios()
pf1.print_pf_result()
pf1.plot_stocks()

plt.show()

import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pfo.pf.portfolio import Portfolio
from pfo.utils.market_data import download, Source
from  pfo.utils.data_utils import clean_data



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)

start_date = datetime.datetime(2018, 11, 20)
end_date = datetime.datetime(2020, 11, 20)

data = download(source=Source.MOEX, tickers = ['AFKS', 'APTK', 'LNZL', 'MAGEP', 'MRKS', 'PLZL', 'ROLO', 'SELG'], board = {'board': 'TQBR', 'shares': 'shares'})
data = clean_data(data)

pf1 = Portfolio(data=data, risk_free_rate=0.01, freq=252)
pf1.mc_simulation(10000)
pf1.plot_mc_simulation()
pf1.print_mc_results()
msr1 = pf1.max_sharpe_ratio()
print(np.round(msr1['x'],decimals = 4))
pf1.efficient_portfolios()

plt.show()

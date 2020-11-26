import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from pfo.portfolio.portfolio import portfolio
from pfo.portfolio.efficient_frontier import efficient_frontier
from pfo.portfolio.valuations import pf_valuation

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 150)

start_date = datetime.datetime(2018, 11, 20)
end_date = datetime.datetime(2020, 11, 20)
path = (Path.cwd() /'..' / "cache" / "moex.csv").resolve()
data = pd.read_csv(path, index_col = 0,  parse_dates=['TRADEDATE'])

pf1_data = pd.DataFrame(data, columns=['AFKS', 'APTK', 'LNZL', 'MAGEP', 'MRKS', 'PLZL', 'ROLO', 'SELG'])

pf1 = portfolio(data=pf1_data, risk_free_rate=0.01, freq=252)
pf1.mc(100000)
pf1.plot_portfolios()
pf1.print_results()
msr1 = pf1.max_sharpe_ratio()
print(np.round(msr1['x'],decimals = 4))
pf1.efficient_portfolios()
# #
ef1 = efficient_frontier(data=pf1_data)
msr1 = ef1.max_sharpe_ratio()
mv1 = ef1.min_volatility()
#
res1 = pf_valuation(msr1['x'], data=pf1_data)
print(res1)
print(np.round(msr1['x'],decimals = 4))

ef1.efficient_portfolios()

plt.show()

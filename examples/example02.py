import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from pfo.portfolio.portfolio import portfolio


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
pf1.mc_simulation(1000000)
pf1.plot_mc_simulation()
pf1.print_mc_results()
msr1 = pf1.max_sharpe_ratio()
print(np.round(msr1['x'],decimals = 4))
pf1.efficient_portfolios()

plt.show()

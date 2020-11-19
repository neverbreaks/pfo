import numpy as np
import pandas as pd
from pfo.valuations import cov_matrix, yearly_returns, daily_log_returns
import datetime
from pathlib import Path
import pandas as pd
import pytest
from pfo.data_utils import clean_data
from pfo.valuations import cov_matrix, yearly_returns, daily_log_returns, volatility
from pfo.quants import mc_random_portfolios

from pfo.market_data import download, Source

path = (Path.cwd() /".."/ "data").resolve()
start_date = datetime.datetime(2014, 12, 31)
end_date = '2020-01-01'

###############################################################################
#                                   TICKERS                                   #
###############################################################################

tickers_pass_csv = [
    ['AAPL', 'NKE', 'GOOGL', 'AMZN']
]

###############################################################################
#                                     PARAMS                                  #
###############################################################################

d_pass_csv = [
    {'source': Source.CSV, 'tickers': tickers_pass_csv[0], 'path': path, 'start_date': start_date, 'end_date': end_date},
]



def portfolio_avg(data, weights):
    weighted_portfolio = weights * data
    return pd.DataFrame(weighted_portfolio.sum(axis=1))

def mc_random_portfolios_v1(data, risk_free_rate=0.0425, num_portfolios = 10000, yr_calc_alg = 'log', freq = 252):

    pf_ret = [] # Define an empty array for portfolio returns
    pf_vol = [] # Define an empty array for portfolio volatility
    pf_weights = [] # Define an empty array for asset weights
    pf_sharp_ratio = []  # Define an empty array for Sharp ratio



    # stocks_downsides_daily_returns = stocks_daily_returns.copy(deep=True)
    # num_of_obseravtions = len(stocks_downsides_daily_returns.index)
    # stocks_downsides_daily_returns[stocks_downsides_daily_returns > 0] = 0
    # stocks_downsides_daily_returns = stocks_downsides_daily_returns[stocks_downsides_daily_returns <= 0]**2


    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        pf_weights.append(weights)
        weighted_portfolio = portfolio_avg(data, weights)
        # Returns are the product of individual expected returns of asset and its weights
        returns = yearly_returns(weighted_portfolio).sum()
        pf_ret.append(returns)

        vol = volatility(weighted_portfolio, freq = freq).sum() # Annual standard deviation = volatility
        pf_vol.append(vol)

        pf_sharp_ratio.append((returns-risk_free_rate)/vol)


    df_rv = {'Returns': pf_ret, 'Volatility': pf_vol, 'Sharp Ratio': pf_sharp_ratio}

    for counter, symbol in enumerate(data.columns, start=0):
        df_rv[symbol] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)

    return portfolios

if __name__ == '__main__':
    d = d_pass_csv[0]
    data = download(**d)
    data = clean_data(data)
    num_assets= len(tickers_pass_csv[0])
    weights = np.random.random(num_assets)
    weights = weights / np.sum(weights)

    weighted_portfolio = portfolio_avg(data, weights)
    dlr = daily_log_returns(weighted_portfolio)
    yr = yearly_returns(weighted_portfolio)
    vol = volatility(weighted_portfolio)

    portfolios = mc_random_portfolios(data, num_portfolios = 10000)

    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
    max_sharpe_port = portfolios.iloc[portfolios['Sharp Ratio'].idxmax()]
    min_vol_port.rename_axis("Min Volatiity")
    max_sharpe_port.rename_axis("Max Sharpe Ratio")

    df_out = pd.concat([min_vol_port, max_sharpe_port], keys=["Min Volatiity", "Max Sharpe Ratio"], join='inner', axis=1)
    print("=" * 80)
    print(df_out)
    print("=" * 80)

    #vol = volatility(weighted_portfolio)
    print(vol)
    print("end")
    #print(weighted_portfolio)

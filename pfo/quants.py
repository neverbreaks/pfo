import numpy as np
import pandas as pd
from pfo.valuations import cov_matrix, yearly_returns, daily_log_returns, downside_log_return


def portfolio_variance(cov_matrix, weights):
    return cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()

def portfolio_daily_returns(weights, daily_returns):
    return  weights * daily_returns

def portfolio_yearly_returns(weights, yearly_returns):
    return np.dot(weights, yearly_returns)

def portfolio_yearly_volatility(weights, pf_cvm, freq = 252):
    var = portfolio_variance(pf_cvm, weights)  # Portfolio Variance
    daily_volatility = np.sqrt(var)  # Daily standard deviation
    return daily_volatility * np.sqrt(freq)  # Annual standard deviation = volatility

def mc_random_portfolios(data, risk_free_rate=0.01, num_portfolios = 10000, yr_calc_alg = 'log', freq = 252):

    pf_ret = [] # Define an empty array for portfolio returns
    pf_vol = [] # Define an empty array for portfolio volatility
    pf_down_vol = [] # Define an empty array for portfolio downside volatility
    pf_weights = [] # Define an empty array for asset weights
    pf_sharp_ratio = []  # Define an empty array for Sharp ratio
    pf_sortino_ratio = []  # Define an empty array for Sortino ratio

    cvm = cov_matrix(data)
    stocks_yearly_returns = yearly_returns(data, freq=freq, type='log')
    stocks_yearly_downside_vol = downside_log_return(data).std() * np.sqrt(freq)

    num_assets=len(data.columns)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        pf_weights.append(weights)
        # Returns are the product of individual expected returns of asset and its weights
        returns = portfolio_yearly_returns(weights, stocks_yearly_returns)
        pf_ret.append(returns)

        volatility = portfolio_yearly_volatility(weights, cvm, freq = freq) # Annual standard deviation = volatility
        pf_vol.append(volatility)

        pf_sharp_ratio.append((returns-risk_free_rate)/volatility)

        pf_stocks_yearly_downside_vol = (stocks_yearly_downside_vol * weights).sum()
        pf_down_vol.append(pf_stocks_yearly_downside_vol)

        pf_sortino_ratio.append((returns-risk_free_rate) / pf_stocks_yearly_downside_vol)

    df_rv = {'Returns': pf_ret, 'Volatility': pf_vol, 'Down. Volatility': pf_down_vol,'Sharp Ratio': pf_sharp_ratio, 'Sortino Ratio': pf_sortino_ratio}

    for counter, symbol in enumerate(data.columns, start=0):
        df_rv[symbol] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)

    return portfolios

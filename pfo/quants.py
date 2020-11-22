import numpy as np
import pandas as pd

from pfo.stocks import yearly_returns, downside_volatility, cov_matrix


def mc_random_portfolios(data: pd.DataFrame, risk_free_rate=0.01, num_portfolios=10000, freq=252):
    pf_ret = []  # Define an empty array for portfolio returns
    pf_vol = []  # Define an empty array for portfolio volatility
    pf_down_vol = []  # Define an empty array for portfolio downside volatility
    pf_weights = []  # Define an empty array for asset weights
    pf_sharp_ratio = []  # Define an empty array for Sharp ratio
    pf_sortino_ratio = []  # Define an empty array for Sortino ratio

    cvm = cov_matrix(data)
    stocks_yearly_returns = yearly_returns(data, freq=freq, type='log')
    stocks_yearly_downside_vol = downside_volatility(data)

    num_assets = len(data.columns)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        pf_weights.append(weights)
        # Returns are the product of individual expected returns of asset and its weights
        returns = portfolio_yearly_returns(weights, stocks_yearly_returns)
        pf_ret.append(returns)

        volatility = portfolio_yearly_volatility(weights, cvm, freq=freq)  # Annual standard deviation = volatility
        pf_vol.append(volatility)

        sh_ratio = (returns - risk_free_rate) / volatility
        pf_sharp_ratio.append(sh_ratio)

        pf_stocks_yearly_downside_vol = portfolio_downside_volatility(stocks_yearly_downside_vol, weights)
        pf_down_vol.append(pf_stocks_yearly_downside_vol)

        sor_ratio = (returns - risk_free_rate) / pf_stocks_yearly_downside_vol
        pf_sortino_ratio.append(sor_ratio)

    df_rv = {'Returns': pf_ret, 'Volatility': pf_vol, 'Down. Volatility': pf_down_vol, 'Sharp Ratio': pf_sharp_ratio,
             'Sortino Ratio': pf_sortino_ratio}

    for counter, symbol in enumerate(data.columns, start=0):
        df_rv[symbol] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)

    return portfolios


def portfolio_valuation(weights, data: pd.DataFrame, risk_free_rate=0.01, freq=252):
    cvm = cov_matrix(data)
    stocks_yearly_returns = yearly_returns(data, freq=freq, type='log')
    stocks_yearly_downside_vol = downside_volatility(data, freq=freq)

    returns = portfolio_yearly_returns(weights, stocks_yearly_returns)
    volatility = portfolio_yearly_volatility(weights, cvm, freq=freq)  # Annual standard deviation = volatility
    sh_ratio = (returns - risk_free_rate) / volatility
    pf_stocks_yearly_downside_vol = portfolio_downside_volatility(stocks_yearly_downside_vol, weights)
    sor_ratio = (returns - risk_free_rate) / pf_stocks_yearly_downside_vol

    return {'Returns': returns, 'Volatility': volatility, 'Sharp': sh_ratio,
            'Downside volatility': pf_stocks_yearly_downside_vol, 'Sortino': sor_ratio}


def sharp_ratio(returns, risk_free_rate, volatility):
    return (returns - risk_free_rate) / volatility


def portfolio_variance(weights, cov_matrix):
    return cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()


def portfolio_daily_returns(weights, daily_returns):
    return weights * daily_returns


def portfolio_yearly_returns(weights, yearly_returns):
    return np.dot(weights, yearly_returns)


def portfolio_yearly_volatility(weights, pf_cvm, freq=252):
    var = portfolio_variance(weights, pf_cvm)  # Portfolio Variance
    daily_volatility = np.sqrt(var)  # Daily standard deviation
    return daily_volatility * np.sqrt(freq)  # Annual standard deviation = volatility


def portfolio_downside_volatility(weights, stocks_yearly_downside_vol):
    return (stocks_yearly_downside_vol * weights).sum()

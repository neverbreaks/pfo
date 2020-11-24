import numpy as np
import pandas as pd
from pfo.stocks.valuations import cov_matrix, mean_returns, downside_volatility


def random_weights(num_assets: int):
    Y = np.random.exponential(scale=1.0, size=num_assets)
    Tk = Y.sum()
    E_list = []
    for i in range(num_assets):
        Ei = Y[i]/Tk
        E_list.append(Ei)

    return np.array(E_list)



def mc_random_portfolios(data: pd.DataFrame, risk_free_rate=0.01, num_portfolios=10000, freq=252):
    pf_ret = []  # Define an empty array for portfolio returns
    pf_vol = []  # Define an empty array for portfolio volatility
    pf_down_vol = []  # Define an empty array for portfolio downside volatility
    pf_weights = []  # Define an empty array for asset weights
    pf_sharp_ratio = []  # Define an empty array for Sharp ratio
    pf_sortino_ratio = []  # Define an empty array for Sortino ratio

    cvm = cov_matrix(data)
    stocks_returns = mean_returns(data, freq=freq, type='log')
    stocks_negative_volatility = downside_volatility(data)

    num_assets = len(data.columns)

    for portfolio in range(num_portfolios):
        # weights = np.random.random(num_assets)
        # weights = weights / np.sum(weights)

        weights = random_weights(num_assets)

        pf_weights.append(weights)
        # Returns are the product of individual expected returns of asset and its weights
        returns = pf_mean_returns(weights, stocks_returns)
        pf_ret.append(returns)

        volatility = pf_volatility(weights, cvm, freq=freq)  # Annual standard deviation = volatility
        pf_vol.append(volatility)

        sh_ratio = (returns - risk_free_rate) / volatility
        pf_sharp_ratio.append(sh_ratio)

        pf_stocks_yearly_downside_vol = pf_negative_volatility(weights=weights,
                                                               stocks_yearly_downside_vol=stocks_negative_volatility)
        pf_down_vol.append(pf_stocks_yearly_downside_vol)

        sor_ratio = (returns - risk_free_rate) / pf_stocks_yearly_downside_vol
        pf_sortino_ratio.append(sor_ratio)

    df_rv = {'Returns': pf_ret, 'Volatility': pf_vol, 'Down. Volatility': pf_down_vol, 'Sharp Ratio': pf_sharp_ratio,
             'Sortino Ratio': pf_sortino_ratio}

    for counter, symbol in enumerate(data.columns, start=0):
        df_rv[symbol] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)

    return portfolios


def pf_valuation(weights, data: pd.DataFrame, risk_free_rate=0.001, freq=252):
    weights_ndarray = None
    if isinstance(weights, pd.DataFrame):
        if len(weights.columns) > 1:
            raise ValueError('Incorrect dataframe with weights provided. Expected 1 column with weights')

        weights_list = []
        for column in data.columns:
            stock_weight = weights.at[column, weights.columns[0]]
            weights_list.append(stock_weight)

        weights_ndarray = np.array(weights_list)

    elif isinstance(weights, np.ndarray):
        weights_ndarray = weights
    else:
        raise ValueError('Weights should be numpy ndarray or pd.DataFrame')

    if len(weights_ndarray) < len(data.columns) or len(weights_ndarray) > len(data.columns):
        raise ValueError('Incorrect data or weights were provided')

    cvm = cov_matrix(data)
    stocks_yearly_returns = mean_returns(data, freq=freq, type='log')
    stocks_yearly_downside_vol = downside_volatility(data, freq=freq)

    returns = pf_mean_returns(weights_ndarray, stocks_yearly_returns)
    volatility = pf_volatility(weights_ndarray, cvm, freq=freq)  # Annual standard deviation = volatility
    sh_ratio = (returns - risk_free_rate) / volatility
    pf_stocks_yearly_downside_vol = pf_negative_volatility(weights=weights_ndarray,
                                                           stocks_yearly_downside_vol=stocks_yearly_downside_vol)
    sor_ratio = (returns - risk_free_rate) / pf_stocks_yearly_downside_vol

    return {'Returns': returns, 'Volatility': volatility, 'Sharp': sh_ratio,
            'Downside volatility': pf_stocks_yearly_downside_vol, 'Sortino': sor_ratio}


def pf_variance(weights, cov_matrix):
    return cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()


def pf_daily_returns(weights, daily_returns):
    return weights * daily_returns


def pf_mean_returns(weights, yearly_returns):
    return np.dot(weights, yearly_returns)


def pf_volatility(weights, pf_cvm, freq=252):
    var = pf_variance(weights, pf_cvm)  # Portfolio Variance
    daily_volatility = np.sqrt(var)  # Daily standard deviation
    return daily_volatility * np.sqrt(freq)  # Annual standard deviation = volatility


def pf_negative_volatility(weights, stocks_yearly_downside_vol):
    return (stocks_yearly_downside_vol * weights).sum()

import numpy as np
import pandas as pd
from pfo.stocks.returns import cov_matrix, mean_returns, downside_volatility


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

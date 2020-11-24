import pandas as pd
import numpy as np
from pfo.stocks import mean_returns
from pfo.stocks.valuations import cov_matrix
from pfo.quants import pf_valuation, pf_volatility
from pfo.market_data import clean_data
import scipy.optimize as sco
import matplotlib.pyplot as plt


class efficient_frontier(object):
    """An class to show efficient frontier for a portfolio based on
    - Pandas dataframe with prices
    - Risk free rate
    - Freq - period


    """

    def __init__(self, data: pd.DataFrame, risk_free_rate=0.001, freq=252):
        if not isinstance(freq, int):
            raise ValueError('Frequency must be an integer')
        elif freq <= 0:
            raise ValueError('Freq must be > 0')
        else:
            self._freq = freq

        if not isinstance(risk_free_rate, (float, int)):
            raise ValueError('Risk free rate must be a float or an integer')
        else:
            self._risk_free_rate = risk_free_rate

        if not isinstance(data, pd.DataFrame):
            raise ValueError('data should be a pandas.DataFrame')

        if isinstance(data.columns, pd.MultiIndex):
            self._data = clean_data(data)
        else:
            self._data = data

        self._efficient_portfolios = None

    def max_sharpe_ratio(self):
        num_stocks = len(self._data.columns)
        args = (self._data, self._risk_free_rate, self._freq)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_stocks))

        result = sco.minimize(self._neg_sharp_ratio, num_stocks * [1. / num_stocks, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def min_volatility(self):
        num_stocks = len(self._data.columns)
        cvm = cov_matrix(self._data)
        args = (cvm, self._freq)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_stocks))

        result = sco.minimize(pf_volatility, num_stocks * [1. / num_stocks, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)

        return result

    def efficient_return(self, target):
        num_stocks = len(self._data.columns)
        cvm = cov_matrix(self._data)

        args = (cvm, self._freq)

        def _pf_return(weights):
            ret = pf_valuation(weights=weights, data=self._data,
                               risk_free_rate=self._risk_free_rate,
                               freq=self._freq).get('Returns')
            return ret

        constraints = ({'type': 'eq', 'fun': lambda x: _pf_return(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_stocks))
        result = sco.minimize(pf_volatility, num_stocks * [1. / num_stocks, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def efficient_frontier(self, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.efficient_return(ret))
        return efficients

    def efficient_portfolios(self, plot = True):
        max_sharpe = self.max_sharpe_ratio()
        min_vol = self.min_volatility()

        res_max = pf_valuation(weights=max_sharpe['x'], data=self._data,
                               risk_free_rate=self._risk_free_rate, freq=self._freq)

        returns_max = res_max.get('Returns')
        volatility_max = res_max.get('Volatility')

        res_min = pf_valuation(weights=min_vol['x'], data=self._data,
                               risk_free_rate=self._risk_free_rate, freq=self._freq)

        returns_min = res_min.get('Returns')
        volatility_min = res_min.get('Volatility')

        target = np.linspace(returns_min, returns_max, 50)
        self._efficient_portfolios = self.efficient_frontier(returns_range=target)

        if plot:
            plt.plot([p['fun'] for p in self._efficient_portfolios], target, 'k-x',
                     label='efficient frontier', color = 'g')

        return self._efficient_portfolios



    def _neg_sharp_ratio(self, weights, data, risk_free_rate, freq=252):
        sharp = pf_valuation(weights=weights, data=data, risk_free_rate=risk_free_rate, freq=freq).get('Sharp')
        return -sharp

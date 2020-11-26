import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as sco
import numpy as np
from pfo.portfolio.mc import mc_random_portfolios
from pfo.market_data import clean_data
from pfo.portfolio.valuations import pf_valuation, pf_volatility, pf_mean_returns
from pfo.stocks.returns import cov_matrix, mean_returns


class portfolio(object):
    """Object that contains information about a investment portfolio.
    """

    def __init__(self, data: pd.DataFrame, weights = None, risk_free_rate=0.0425, freq=252):
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

        self._portfolios = None
        self._min_vol_port = None
        self._min_downside_vol_port = None
        self._max_sharpe_port = None
        self._max_sortino_port = None
        self._df_results = None

        #####################
        if weights is None:
           self._weights = np.array([1./len(self._data.columns) for i in range(len(self._data.columns))])
        else:
            self._weights = np.array(weights)

        self._cvm = cov_matrix(self._data)
        self._mr = mean_returns(self._data, freq=self._freq)


    @property
    def min_vol_port(self):
        return self._min_vol_port

    @property
    def min_downside_vol_port (self):
        return self._min_downside_vol_port

    @property
    def max_sharp_port(self):
        return self._max_sharpe_port

    @property
    def max_sortino_port(self):
        return self._max_sortino_port

    @property
    def data(self):
        return self._data


    ###############################################################################
    #                                     PLOT                                   #
    ###############################################################################
    def plot_portfolios(self):
        self._portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True,
                                      figsize=[16, 10])
        plt.scatter(self._min_vol_port[1], self._min_vol_port[0], color='r', marker='*', s=500)
        plt.scatter(self._min_downside_vol_port[1], self._min_downside_vol_port[0], color='c', marker='*', s=500)
        plt.scatter(self._max_sharpe_port[1], self._max_sharpe_port[0], color='g', marker='*', s=500)
        plt.scatter(self._max_sortino_port[1], self._max_sortino_port[0], color='y', marker='*', s=500)

    def plot_ef(self):
        pass

    ###############################################################################
    #                                     REPORTING                               #
    ###############################################################################

    def print_results(self):
        print('\n')
        print('=' * 80)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self._df_results)
        print('=' * 80)

    def store_to_xls(self):
       pass


    ###############################################################################
    #                                     SIMULATION                              #
    ###############################################################################
    def mc(self, num_portfolios=10000):
        self._portfolios = mc_random_portfolios(data=self._data, risk_free_rate=self._risk_free_rate,
                                                num_portfolios=num_portfolios, freq=self._freq)

        self._min_vol_port = self._portfolios.iloc[self._portfolios['Volatility'].idxmin()]
        self._min_downside_vol_port = self._portfolios.iloc[self._portfolios['Down. Volatility'].idxmin()]
        self._max_sharpe_port = self._portfolios.iloc[self._portfolios['Sharp Ratio'].idxmax()]
        self._max_sortino_port = self._portfolios.iloc[self._portfolios['Sortino Ratio'].idxmax()]
        self._min_vol_port.rename_axis('Min Volatiity')
        self._min_downside_vol_port.rename_axis('Down. Volatility')
        self._max_sharpe_port.rename_axis('Max Sharpe Ratio')
        self._max_sortino_port.rename_axis('Max Sortino Ratio')

        self._df_results = pd.concat(
            [self._min_vol_port, self._min_downside_vol_port, self._max_sharpe_port, self._max_sortino_port],
            keys=['Min Volatiity', 'Down. Volatility', 'Max Sharpe Ratio', 'Max Sortino Ratio'], join='inner', axis=1)


    ###############################################################################
    #                                     EFFICIENT FRONTIER                      #
    ###############################################################################

    def max_sharpe_ratio(self):
        num_stocks = len(self._data.columns)
        #args = (self._data, self._risk_free_rate, self._freq)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_stocks))

        #returns, risk_free_rate, volatility

        result = sco.minimize(self._neg_sharp_ratio, num_stocks * [1. / num_stocks, ], args=(),
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
            ret = pf_mean_returns(weights, self._mr)
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

    def sharp_ratio(self, weights):
        ret= pf_mean_returns(weights, self._mr)
        vol = pf_volatility(weights, self._cvm, freq=self._freq)
        return (ret - self._risk_free_rate)/vol

    def _neg_sharp_ratio(self, weights):
        return -self.sharp_ratio(weights)

    def _neg_sortino_ratio(self, weights, data, risk_free_rate, freq=252):
        sharp = pf_valuation(weights=weights, data=data, risk_free_rate=risk_free_rate, freq=freq).get('Sortino')
        return -sharp
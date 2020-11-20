import matplotlib.pyplot as plt
import pandas as pd

from pfo.quants import mc_random_portfolios


class portfolio(object):
    """Object that contains information about a investment portfolio.
    To initialise the object, it does not require any input.
    To commence the analysis the portfolio must be initiated
    with ''build'' function.
    """

    def __init__(self, data: pd.DataFrame, risk_free_rate=0.0425, freq=252, num_portfolios=10000, yr_calc_alg='log'):
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

        self._portfolios = None
        self._min_vol_port = None
        self._min_downside_vol_port = None
        self._max_sharpe_port = None
        self._max_sortino_port = None
        self._df_results = None
        self._num_portfolios = num_portfolios
        self._yr_calc_alg = yr_calc_alg
        # stocks prices
        self._data = data

        self._calc()

    @property
    def data(self):
        return self._data

    def _ef(self):
        pass

    def _calc(self):
        self._portfolios = mc_random_portfolios(data=self._data, risk_free_rate=self._risk_free_rate, \
                                                num_portfolios=self._num_portfolios, freq=self._freq, \
                                                yr_calc_alg=self._yr_calc_alg)

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

        self._ef()

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

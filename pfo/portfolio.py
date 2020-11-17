import pandas as pd
import matplotlib.pyplot as plt
from pfo.config import price_column
from pfo.valuations import daily_log_returns, volatility
from pfo.valuations import cov_matrix, corr_matrix, yearly_returns
from pfo.quants import mc_random_portfolios

class Portfolio(object):
    """Object that contains information about a investment portfolio.
    To initialise the object, it does not require any input.
    To commence the analysis the portfolio must be initiated
    with ''build'' function.
    """

    def __init__(self):
        self._portfolios = pd.DataFrame()
        self._min_vol_port = pd.DataFrame()
        self._optimal_risky_port = pd.DataFrame()
        # stocks prices
        self._data = pd.DataFrame()
        # Risk free rate. I default with CBR ate
        self._risk_free_rate = 0
        # Final calculations are annualised so 252 work days are selected as basis
        self._freq = 252



    def _clean_data(self, dt: pd.DataFrame)->pd.DataFrame:
       columns = []
       priority_column = price_column(dt.columns.get_level_values(0))
       for index, item in enumerate(dt.columns.get_level_values(0), start=0):  # Python indexes start at zero
           if item == priority_column:
               columns.append(index)

       return dt.iloc[:, columns]

    @property
    def data(self):
        return self._data

    def plot_portfolios(self):
        self._portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[16, 10])
        plt.scatter(self._min_vol_port[1], self._min_vol_port[0], color='r', marker='*', s=500)
        plt.scatter(self._optimal_risky_port[1], self._optimal_risky_port[0], color='g', marker='*', s=500)
        plt.show()


    def _ef(self):
       pass

    def _calc(self):
        self._portfolios = mc_random_portfolios(self._data)
        self._min_vol_port = self._portfolios.iloc[self._portfolios['Volatility'].idxmin()]
        self._optimal_risky_port = self._portfolios.iloc[self._portfolios['Sharp Ratio'].idxmax()]
        self.plot_portfolios()
        self._ef()


    def build(self, data: pd.DataFrame, risk_free_rate=0.0425, freq=252):
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
            raise ValueError('Data should be a pandas.DataFrame')
        elif not isinstance(data.columns, pd.MultiIndex) > 0:
            raise ValueError('Multiindex pandas.DataFrame is expected like Close/AAPL')
        elif price_column(data.columns.get_level_values(0)) == None:
            raise ValueError('Can not find a column with prices')
        else:
            self._data= self._clean_data(data)

        self._calc()

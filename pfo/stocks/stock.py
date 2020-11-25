from typing import Any, Union

import pandas as pd
from matplotlib import pylab as plt
from pfo.market_data import clean_data
from pfo.stocks.valuations import mean_returns, volatility, downside_volatility, daily_log_returns


class stock(object):
    """Object that contains information about a stock.
    The class allows to show all ratios and plots required
    for analysis
    """

    def __init__(self, ticker, data: pd.DataFrame, **kwargs):
        if not isinstance(data, pd.DataFrame):
            raise ValueError('data should be a pandas.DataFrame')

        if isinstance(data.columns, pd.MultiIndex):
            self._data = clean_data(data)
        else:
            self._data = data

        if not (ticker in self._data.columns):
            raise ValueError(f'Ticker {ticker} is not provided in DataFrame')

        self._ticker = ticker
        self._data = pd.DataFrame(self._data[ticker])

        self._risk_free_rate = kwargs.get('risk_free_rate', 0.001)
        self._freq = kwargs.get('freq', 252)
        self._type = kwargs.get('type', 'log')

        self._daily_returns = daily_log_returns(self._data)

        ##########PROPERTIES##########
        self._returns = mean_returns(self._data, freq=self._freq, type=self._type).values[0]
        self._volatility = volatility(self._data).values[0]
        self._downside_volatility = downside_volatility(self._data).values[0]
        self._sharp = (self._returns - self._risk_free_rate)/self._volatility
        self._sortino = (self.returns - self._risk_free_rate)/self._downside_volatility
        self._skew = self._data.skew().values[0]
        self._kurtosis = self._data.kurt().values[0]


    @property
    def returns(self):
        return self._returns

    @property
    def volatility(self):

        return self._volatility

    @property
    def downside_volaitulity(self):
        return self._downside_volitility

    @property
    def sortino(self):
        return  self._sortino

    @property
    def sharp(self):
        return  self._sharp

    @property
    def skew(self):
        return  self._skew

    @property
    def kurtosis(self):
        return self._kurtosis

    def plot_daily_returns(self):

        plt.figure(figsize=(16, 10))
        #ax = fig.add_subplot(111, projection='polar')

        plt.plot(self._daily_returns[self._ticker].cumsum(), 'black', linewidth=1)
        plt.title(f'{self._ticker}')
        plt.ylabel("Daily returns cumulative sum")
        plt.xticks(rotation=30)
        plt.grid(True)


    def plot_prices(self):

        plt.figure(figsize=(16, 10))
        #ax = fig.add_subplot(111, projection='polar')

        plt.plot(self._data[self._ticker], 'black', linewidth=1)
        plt.title(f'{self._ticker}')
        plt.ylabel("Price")
        plt.xticks(rotation=30)
        plt.grid(True)

import pandas as pd

from pfo.market_data import clean_data


class stock(object):
    """Object that contains information about a stock.
    The class allows to show all ratios and plots required
    for analysis
    """

    def __init__(self, ticker, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError('data should be a pandas.DataFrame')

        if isinstance(data.columns, pd.MultiIndex):
            self._data = clean_data(data)
        else:
            self._data = data

        if not (ticker in self._data.columns):
            raise ValueError(f'Ticker {ticker} is not provided in DataFrame')

        self._data = pd.DataFrame(self._data[ticker])
import pandas as pd


class Portfolio(object):
    """Object that contains information about a investment portfolio.
    To initialise the object, it does not require any input.
    To commence the analysis the portfolio must be initiated
    with ''build'' function.
    """

    def __init__(self):
        # stocks prices
        self._data = pd.DataFrame()
        # Risk free rate. I default with CBR ate
        self._risk_free_rate = 0
        # Final calculations are annualised so 252 work days are selected as basis
        self._freq = 252

    def _calc(self):
        pass

    def _clean_data(self, dt: pd.DataFrame):
       columns = [label for label in dt.columns]
       print(dt.iloc[:, dt.columns.get_level_values(1) == 'AAPL'])
       print(columns)




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
            raise ValueError('Multiindex pandas.DataFrame is expected')
        else:
            self._data = data
            self._clean_data(data)

        self._calc()

        return self

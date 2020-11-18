import pandas as pd

_price_col_names = ['WAPRICE', 'Adj. Close', 'Adj Close', 'CLOSE', 'close', 'Close']


def price_column(columns):
    unique_names = list(set(columns))

    for name in unique_names:
        if name in _price_col_names:
            return name

    return None


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    priority_column = price_column(data.columns.get_level_values(0))

    if not isinstance(data, pd.DataFrame):
        raise ValueError('Data should be a pandas.DataFrame')
    elif not isinstance(data.columns, pd.MultiIndex):
        raise ValueError('Multiindex pandas.DataFrame is expected like Close/AAPL')
    elif priority_column == None:
        raise ValueError('Can not find a column with prices')

    columns = []
    for index, item in enumerate(data.columns.get_level_values(0), start=0):  # Python indexes start at zero
        if item == priority_column:
            columns.append(index)

    data = data.iloc[:, columns]
    data.columns = data.columns.droplevel(0)
    return data

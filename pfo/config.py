_price_col_names = ['WAPRICE', 'Adj. Close', 'Adj Close', 'CLOSE', 'close', 'Close']

def price_column(columns):
    unique_names = list(set(columns))

    for name in  unique_names:
        if name in _price_col_names:
            return name

    return None
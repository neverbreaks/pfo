import warnings
import pytest
from pathlib import Path
from pfo.market_data import _download_csv
import datetime
import pandas as pd

tickers_pass = ['AAPL', 'AMD']
tickers_warn = ['AAPL', 'AMD', 'UNKN']
path = (Path.cwd() / ".." / "data").resolve()
start_date = datetime.datetime(2017, 1, 1)
end_date = "2019-12-31"

d_pass = [
    {'tickers': tickers_pass, 'path': path, 'start_date': start_date, 'end_date' : end_date},
]

d_warn = [
    {'tickers': tickers_warn, 'path': path, 'start_date': start_date, 'end_date' : end_date},
]

def test_download_csv_pass_0():
    d = d_pass[0]
    data = _download_csv(**d)
    print(data)
    isinstance(data, pd.DataFrame)

def test_download_csv_warn_0():
    d = d_warn[0]
    with pytest.warns(UserWarning):
        data = _download_csv(**d)

    print(data)
    isinstance(data, pd.DataFrame)
import warnings
import pytest
from pathlib import Path
from pfo.market_data import download, Source, _download_csv
import datetime
import pandas as pd

tickers_pass = ['AAPL', 'AMD']
tickers_warn = ['AAPL', 'AMD', 'UNKN']
tickers_moex = ['SBER', 'GAZP', 'MTSS']
path = (Path.cwd() / ".." / "data").resolve()
start_date = datetime.datetime(2017, 1, 1)
end_date = "2019-12-31"

d_pass = [
    {'source': Source.CSV, 'tickers': tickers_pass, 'path': path, 'start_date': start_date, 'end_date' : end_date},
    {'source': Source.CSV, 'tickers': tickers_pass, 'path': path},
    {'source': Source.CSV, 'tickers': tickers_pass},
    {'source': Source.YFINANCE, 'tickers': tickers_pass},
    {'source': Source.YFINANCE, 'tickers': tickers_pass, 'start_date': start_date, 'end_date' : end_date},
    {'source': Source.MOEX, 'tickers': tickers_moex, 'start_date': start_date, 'end_date' : end_date},
]

d_warn = [
    {'tickers': tickers_warn, 'path': path, 'start_date': start_date, 'end_date' : end_date},
]

def test_download_csv_pass_0():
    d = d_pass[0]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_csv_pass_1():
    d = d_pass[1]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_csv_warn_0():
    d = d_pass[2]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_csv_warn_1():
    d = d_warn[0]
    with pytest.warns(UserWarning):
        data = _download_csv(**d)

    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_yfinance_pass_0():
    d = d_pass[3]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_yfinance_pass_1():
    d = d_pass[4]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

def test_download_moex_pass_0():
    d = d_pass[5]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)

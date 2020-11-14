"""The module provides 2 services:
   1. Extrqct market data from 3 sources : MOEX, YFINANCE and csv files with market data.
   2. Cache market data to scv files
"""

import pandas as pd
import yfinance
from pathlib import Path, WindowsPath
from enum import Enum


class Source(Enum):
    MOEX = 1
    YFINANCE = 2
    CSV = 3


def _download_csv(tickers, path, start_date, end_date) -> pd.DataFrame:
    data = pd.DataFrame()

    if isinstance(path, str):
        p = Path(path)
    elif isinstance(path, (Path, WindowsPath)):
        p = path
    else:
        raise Exception(f'Varibale path should be str, pathlib.Path or pathlib.WindowsPath')

    if not p.exists():
        raise Exception(f'File or folder {path} does not exist')

    files = []
    if p.is_dir():
        files = p.glob('*.csv')
    else:
        raise Exception('Param path should lead to folder')

    available_tickers = [f.stem for f in files]

    if len(tickers) == 0:
        tickers = available_tickers
    else:
        missing_tickers = list(set(tickers) - set(available_tickers))
        if len(missing_tickers) > 0:
            warning_message = "-" * 50
            warning_message += "\n"
            warning_message += "\nMissing stocks: {}".format(missing_tickers)
            warning_message += "\n"
            warning_message += "-" * 50
            import warnings
            warnings.warn(warning_message)

    data = pd.DataFrame()
    for ticker in tickers:
        try:
            ticker_path = Path(path / f'{ticker}.csv')

            if start_date is None or end_date is None:
                data[ticker] = \
                    pd.read_csv(ticker_path, parse_dates=['Date'], skipinitialspace=True, index_col=0, sep=',') \
                        ['Adj. Close']
            else:
                data[ticker] = \
                    pd.read_csv(ticker_path, parse_dates=['Date'], skipinitialspace=True, index_col=0, sep=',') \
                        ['Adj. Close'][start_date:end_date]

        except:
            continue

    return data


def _download_yfinance(tickers, start_date, end_date) -> pd.DataFrame:
    data = pd.DataFrame()

    if len(tickers) == 0:
        raise Exception(f'No tickers provided')

    if start_date is None or end_date is None:
        data = yfinance.download(tickers, period="max")
    else:
        data = yfinance.download(tickers, start=start_date, end=end_date)

    return data



def download(source: Source, **kwargs) -> pd.DataFrame:
    """This function returns pandas.DataFrame with market data for analysis.
    :Input:
     :source:  ``market_data.Source`` Source.MOEX, Source.YFINANCE or Source.CSV.
     :tickers = list of str, tickers like [AAPL, SBER.ME]
     :start_date: (optional) ``string``/``datetime`` start date of stock data to be
         requested through `yfinance` (default: ``None``).
     :end_date: (optional) ``string``/``datetime`` end date of stock data to be
         requested through `yfinance` (default: ``None``).
     :path (optional): folder where .csv files with prices are stored. file should be
      named as ticker.csv, i.e. AAPL.csv
    :Output:
     : rates: pandas.DataFrame, index = Date,
    """
    tickers = kwargs.get('tickers', [])
    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)
    path = kwargs.get('path', '')

    rates = pd.DataFrame()
    if source == Source.CSV:
        rates = _download_csv(tickers=tickers, start_date=start_date, end_date=end_date, path=path)

    if source == Source.YFINANCE:
        rates = _download_yfinance(tickers=tickers, start_date=start_date, end_date=end_date)


    return rates


def cache(source: Source, path, **kwargs):

    print("")

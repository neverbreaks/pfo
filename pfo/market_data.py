"""The module provides 2 services:
   1. Extrqct market data from 3 sources : MOEX, YFINANCE and csv files with market data.
   2. Cache market data to scv files
"""

import pandas as pd
from pathlib import Path
from enum import Enum


class Source(Enum):
    MOEX = 1
    YFINANCE = 2
    CSV = 3


def _download_csv(tickers, path, start_date, end_date) -> pd.DataFrame:
    data = pd.DataFrame()

    p = Path(path)

    if not p.exists():
        raise Exception(f"File or folder {rpts_path} does not exist")

    files = []
    if p.is_dir():
        files = p.glob("*.csv")
    else:
        files = [path]

    ticker_files = []
    if len(tickers) > 0:
        ticker_files = [t+'.csv' for t in tickers]
    else:
        ticker_files = files

    data = pd.DataFrame()
    for ticker in ticker_files:
        try:
            data[ticker] = \
            pd.read_csv(path + ticker + '.csv', parse_dates=['Date'], skipinitialspace=True, index_col=0, sep=',') \
                ['Adj. Close'][start_date:end_date]
        except:
            continue

    return data



def download(**kwargs) -> pd.DataFrame:
    """This function returns pandas.DataFrame with market data for analysis.
    :Input:
     :tickers = list of str, tickers like [AAPL, SBER.ME]
     :source:  ``market_data.Source`` MOEX, YFINANCE or CSV.
     :start_date: (optional) ``string``/``datetime`` start date of stock data to be
         requested through `yfinance` (default: ``None``).
     :end_date: (optional) ``string``/``datetime`` end date of stock data to be
         requested through `yfinance` (default: ``None``).
     :path (optional): folder where .csv files with prices are stored. file should be
     called as ticker.csv, i.e. AAPL.csv
    :Output:
     : rates: pandas.DataFrame, index = Date,
    """
    print("")


def cache(**kwargs):
    """This function builds and returns an instance of ``Portfolio``
       given a set of input arguments.
    :Input:
     :source:  ``market_data.Source`` with the required data column
         labels ``Name`` and ``Allocation`` of the stocks. If not given, it is
         automatically generated with an equal weights for all stocks
         in the resulting portfolio.
     :names: (optional) A ``string`` or ``list`` of ``strings``, containing the names
         of the stocks, e.g. "GOOG" for Google.
     :start_date: (optional) ``string``/``datetime`` start date of stock data to be
         requested through `quandl`/`yfinance` (default: ``None``).
     :end_date: (optional) ``string``/``datetime`` end date of stock data to be
         requested through `quandl`/`yfinance` (default: ``None``).
    :Output:
     :pf: Instance of ``Portfolio`` which contains all the information
         requested by the user.
    """
    print("")
"""The module provides 2 services:
   1. Extrqct market data from 3 sources : MOEX, YFINANCE and csv files with market data.
   2. Cache market data to scv files
"""

import pandas as pd
import yfinance
import apimoex
import requests
from pathlib import Path, WindowsPath
from enum import Enum
import datetime


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

    missing_tickers = []
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

    stocks_prices = []
    for ticker in tickers:
        if ticker not in missing_tickers:
            stock_df = pd.DataFrame()
            try:
                ticker_path = Path(path / f'{ticker}.csv')
                if start_date is None or end_date is None:
                    stock_df = \
                        pd.read_csv(ticker_path, index_col = 0,  parse_dates=['Date'], skipinitialspace=True,  sep=',') \
                            ['Adj. Close']
                else:
                    stock_df = \
                        pd.read_csv(ticker_path, index_col = 0,  parse_dates=['Date'], skipinitialspace=True, sep=',') \
                            ['Adj. Close'][start_date:end_date]

            except:
                continue

            stock_df = pd.DataFrame(stock_df)

            stock_df = pd.concat([stock_df], axis=1, keys=[ticker]).swaplevel(0, 1, 1)
            stocks_prices.append(stock_df)

    if len(stocks_prices) > 0:
        data = pd.concat(stocks_prices, join='inner', axis=1)

    return data


def _download_yfinance(tickers, start_date, end_date) -> pd.DataFrame:
    data = pd.DataFrame()

    if len(tickers) == 0:
        raise Exception(f'No tickers provided')

    try:
        if start_date is None or end_date is None:
            data = yfinance.download(tickers, period="max")
        else:
            data = yfinance.download(tickers, start=start_date, end=end_date)

    except Exception:
        raise Exception(
            "Error during download of stock data with `yfinance`"
        )

    if not isinstance(data.columns, pd.MultiIndex) > 0:
        # adding multiindex
        stock_tuples = [(col, tickers[0]) for col in list(data.columns)]
        data.columns = pd.MultiIndex.from_tuples(stock_tuples)

    return data


def _download_moex(tickers, start_date, end_date, boards) -> pd.DataFrame:
    data = pd.DataFrame()
    arguments = {'securities.columns': ('SECID,'
                                        'REGNUMBER,'
                                        'LOTSIZE,'
                                        'SHORTNAME')}
    for board in boards:
        brd = board.get('board')
        shares = board.get('shares')
        request_url = ('https://iss.moex.com/iss/engines/stock/'
                       f'markets/{shares}/boards/{brd}/securities.json')

        print("-" * 80)
        print(f'Loading {board}:')

        with requests.Session() as session:
            iss = apimoex.ISSClient(session, request_url, arguments)
            iis_data = iss.get()
            board_df = pd.DataFrame(iis_data['securities'])
            board_df.set_index('SECID', inplace=True)

            columns = ['TRADEDATE', 'WAPRICE', 'CLOSE']
            stocks_prices = []
            for stock in board_df.index:
                if stock in tickers:
                    print(f' ---{stock}:')

                    stock_data = apimoex.get_board_history(session=session, security=stock, start=start_date, \
                                                           end=end_date, columns=columns, market=shares, board=brd)

                    stock_df = pd.DataFrame(stock_data)
                    stock_df['TRADEDATE'] = pd.to_datetime(stock_df['TRADEDATE'])
                    stock_df.set_index('TRADEDATE', inplace=True)
                    stock_df = pd.concat([stock_df], axis=1, keys=[stock]).swaplevel(0, 1, 1)
                    stocks_prices.append(stock_df)

            if len(stocks_prices) > 0:
                data = pd.concat(stocks_prices, join='inner', axis=1)

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
     :boards : union, MOEX boards and type of share like boards = [
                                                             {'board': 'TQBR', 'shares': 'shares'},
                                                             {'board': 'TQTF', 'shares': 'shares'},
                                                             {'board': 'FQBR', 'shares': 'foreignshares'},
                                                         ]
    :Output:
     : rates: pandas.DataFrame, index = Date,
    """
    tickers = kwargs.get('tickers', [])
    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)
    path = kwargs.get('path', '')
    boards = kwargs.get('boards', [{'board': 'TQBR', 'shares': 'shares'}])

    rates = pd.DataFrame()
    if source == Source.CSV:
        rates = _download_csv(tickers=tickers, start_date=start_date, end_date=end_date, path=path)

    if source == Source.YFINANCE:
        rates = _download_yfinance(tickers=tickers, start_date=start_date, end_date=end_date)

    if source == Source.MOEX:
        rates = _download_moex(tickers=tickers, start_date=start_date, end_date=end_date, boards=boards)

    return rates


def cache(source: Source, path, **kwargs):
    print("")

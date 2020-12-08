import datetime
from pathlib import Path
import pandas as pd
import pytest

from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data
from pfo.utils.moex import get_board_tickers

path = (Path.cwd() / "data").resolve()
start_date = datetime.datetime(2017, 1, 1)
end_date = "2019-12-31"


###############################################################################
#                                   TICKERS                                   #
###############################################################################

tickers_pass_csv = [
    ["AAPL"],
    ["AAPL", "AMD"],
]

tickers_pass_yfinance = [
    ["AAPL"],
    ["AAPL", "AMD"],
]

tickers_pass_moex = [
    ["SBER", "GAZP", "MTSS"],
    ["SBER", "GAZP", "MTSS", "UNKN"],
    ["SBER"],
    [],
    ["AAPL-RM", "FXDE", "SBSP", "SBER", "AFLT"],
]

tickers_warn_csv = [
    ["AAPL", "AMD", "UNKN"],
]

###############################################################################
#                                     PARAMS                                  #
###############################################################################

d_pass_csv = [
    {
        "source": Source.CSV,
        "tickers": tickers_pass_csv[0],
        "path": path,
        "start_date": start_date,
        "end_date": end_date,
    },
    {"source": Source.CSV, "tickers": tickers_pass_csv[1], "path": path},
]

d_warn_csv = [
    {
        "source": Source.CSV,
        "tickers": tickers_warn_csv[0],
        "path": path,
        "start_date": start_date,
        "end_date": end_date,
    },
    {"source": Source.CSV, "tickers": tickers_pass_csv[1]},
]

d_pass_yfinance = [
    {"source": Source.YFINANCE, "tickers": tickers_pass_yfinance[0]},
    {
        "source": Source.YFINANCE,
        "tickers": tickers_pass_yfinance[1],
        "start_date": start_date,
        "end_date": end_date,
    },
]

d_pass_moex = [
    {
        "source": Source.MOEX,
        "tickers": tickers_pass_moex[0],
        "start_date": start_date,
        "end_date": end_date,
    },
    {
        "source": Source.MOEX,
        "tickers": tickers_pass_moex[1],
        "start_date": start_date,
        "end_date": end_date,
    },
    {"source": Source.MOEX, "tickers": tickers_pass_moex[2]},
    {"source": Source.MOEX, "tickers": tickers_pass_moex[3]},
    {
        "source": Source.MOEX,
        "tickers": tickers_pass_moex[4],
        "boards": [
            {"board": "TQBR", "shares": "shares"},
            {"board": "TQTF", "shares": "shares"},
            {"board": "FQBR", "shares": "foreignshares"},
        ],
    },
]


###############################################################################
#                                       CSV                                   #
###############################################################################
def test_download_csv_pass_0():
    d = d_pass_csv[0]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_csv_pass_1():
    d = d_pass_csv[1]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_csv_warn_0():
    d = d_warn_csv[0]
    with pytest.warns(UserWarning):
        data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_csv_warn_1():
    d = d_warn_csv[1]
    with pytest.warns(UserWarning):
        data = download(**d)

    print(data.head())
    isinstance(data, pd.DataFrame)


###############################################################################
#                                       YFINANCE                              #
###############################################################################


def test_download_yfinance_pass_0():
    d = d_pass_yfinance[0]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_yfinance_pass_1():
    d = d_pass_yfinance[1]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


###############################################################################
#                                       MOEX                                  #
###############################################################################


def test_download_moex_pass_0():
    d = d_pass_moex[0]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_moex_pass_1():
    d = d_pass_moex[1]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_moex_pass_2():
    d = d_pass_moex[2]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_moex_pass_3():
    d = d_pass_moex[3]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)


def test_download_moex_pass_4():
    d = d_pass_moex[4]
    data = download(**d)
    print(data.head())
    isinstance(data, pd.DataFrame)
    data = clean_data(data)
    tickers = data.columns.tolist()
    print(tickers)
    assert sorted(tickers) == sorted(tickers_pass_moex[4])


def test_get_board_tickers_pass_0():
    tickers = get_board_tickers()
    print(tickers)


def test_get_board_tickers_pass_0():
    tickers = get_board_tickers()
    assert "SBER" in tickers
    assert "AAPL-RM" not in tickers
    print(tickers)


def test_get_board_tickers_pass_1():
    tickers = get_board_tickers(board={"board": "FQBR", "shares": "foreignshares"})
    assert "SBER" not in tickers
    assert "AAPL-RM" in tickers
    print(tickers)

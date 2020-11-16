import datetime
from pathlib import Path
import pandas as pd
import pytest

from pfo.market_data import download, Source
import pfo.portfolio as pf

path = (Path.cwd() / "data").resolve()
start_date = datetime.datetime(2017, 1, 1)
end_date = "2019-12-31"

###############################################################################
#                                   TUCKERS                                   #
###############################################################################

tickers_pass_csv = [
    ['AAPL', 'AMD', 'V'],
    ['AAPL', 'AMD'],
]

###############################################################################
#                                     PARAMS                                  #
###############################################################################

d_pass_csv = [
    {'source': Source.CSV, 'tickers': tickers_pass_csv[0], 'path': path, 'start_date': start_date, 'end_date': end_date},
    {'source': Source.CSV, 'tickers': tickers_pass_csv[1], 'path': path},
]

###############################################################################
#                                       CSV                                   #
###############################################################################
def test_portfolio_csv_pass_0():
    d = d_pass_csv[0]
    data = download(**d)
    portfolio = pf.Portfolio()
    portfolio.build(data)


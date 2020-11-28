import datetime
from pathlib import Path

from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data
from pfo.pf.portfolio import Portfolio

path = (Path.cwd() / "data").resolve()
start_date = datetime.datetime(2018, 11, 19)
end_date = '2020-11-18'


###############################################################################
#                                   TUCKERS                                   #
###############################################################################

tickers_pass_csv = [
    ['TSLA', 'FB'],
    ['AAPL', 'AMD'],
    ['AAPL', 'NKE', 'GOOGL', 'AMZN']
]

tickers_pass_yfinance = [
    ['AAPL'],
    ['AAPL', 'AMD'],
    ['V', 'ADBE', 'AMZN', 'MSFT', 'ATVI', 'EA', 'FB', 'NEM', 'GOOG', 'AVGO', 'QCOM', 'BABA', 'MA', 'AAPL']
]

tickers_pass_moex = [
    ['SBER', 'GAZP', 'MTSS', 'AFLT', 'MOEX'],
    ['SBER', 'GAZP', 'MTSS', 'UNKN'],
    ['SBER'],
]

###############################################################################
#                                     PARAMS                                  #
###############################################################################

d_pass_csv = [
    {'source': Source.CSV, 'tickers': tickers_pass_csv[2], 'path': path, 'start_date': start_date, 'end_date': end_date},
    {'source': Source.CSV, 'tickers': tickers_pass_csv[1], 'path': path},
]

d_pass_yfinance = [
    {'source': Source.YFINANCE, 'tickers': tickers_pass_yfinance[0]},
    {'source': Source.YFINANCE, 'tickers': tickers_pass_yfinance[1], 'start_date': start_date, 'end_date': end_date},
    {'source': Source.YFINANCE, 'tickers': tickers_pass_yfinance[2], 'start_date': start_date, 'end_date': end_date},
]

d_pass_moex = [
    {'source': Source.MOEX, 'tickers': tickers_pass_moex[0], 'start_date': start_date, 'end_date': end_date},
    {'source': Source.MOEX, 'tickers': tickers_pass_moex[1], 'start_date': start_date, 'end_date': end_date},
    {'source': Source.MOEX, 'tickers': tickers_pass_moex[2]},
]


###############################################################################
#                                       CSV                                   #
###############################################################################
def test_portfolio_csv_pass_0():
    d = d_pass_csv[0]
    data = download(**d)
    data = clean_data(data)
    pf = Portfolio(data = data)
    pf.mc_simulation()
    pf.plot_mc_simulation()
    pf.print_mc_results()

###############################################################################
#                                      MOEX                                   #
###############################################################################
def test_portfolio_moex_pass_0():
    d = d_pass_moex[0]
    data = download(**d)
    data = clean_data(data)
    pf = Portfolio(data = data)
    pf.mc_simulation()
    pf.plot_mc_simulation()
    pf.print_mc_results()


def test_portfolio_yfinance_pass_0():
    d = d_pass_yfinance[2]
    data = download(**d)
    data = clean_data(data)
    pf = Portfolio(data=data, risk_free_rate=0.001, freq=252)
    pf.mc_simulation(num_portfolios=100)
    pf.plot_mc_simulation()
    pf.print_mc_results()

def test_portfolio_yfinance_pass_1():
    d = d_pass_yfinance[0]
    data = download(**d)
    data = clean_data(data)
    pf = Portfolio(data=data, risk_free_rate=0.001, freq=252)
    pf.mc_simulation()
    pf.plot_mc_simulation()
    pf.print_mc_results()
import datetime
import matplotlib.pyplot as plt
from pfo.pf.portfolio import Portfolio
import numpy as np
from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data

start_date = datetime.datetime(2019, 1, 1)
end_date = "2020-11-20"

tickers = [
    "GM",
    "WMT",
    "NVDA",
    "TSLA",
    "GE",
    "AAL",
    "AMD",
    "ADBE",
    "AMZN",
]

data = download(
    source=Source.YFINANCE, tickers=tickers, start_date=start_date, end_date=end_date
)
data = clean_data(data)
pf = Portfolio(data=data, risk_free_rate=0.001, freq=252)
pf.discrete_allocation()

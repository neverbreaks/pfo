import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pfo.stocks.cluster import cluster_stocks
from pfo.stocks.stock import Stock
from pathlib import Path, WindowsPath

from pfo.utils.market_data import download, Source
from pfo.utils.data_utils import clean_data

path = (Path.cwd() / ".." / "cache" / "moex_all.csv").resolve()
data = download(
    Source.MOEX,
    tickers=[],
    boards=[
        {"board": "TQBR", "shares": "shares"},
        {"board": "TQTF", "shares": "shares"},
        {"board": "FQBR", "shares": "foreignshares"},
    ],
)

data = clean_data(data)
data.to_csv(path)

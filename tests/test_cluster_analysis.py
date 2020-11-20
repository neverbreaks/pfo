from pathlib import Path
import numpy as np
from pfo.market_data import download, Source
from pfo.stocks import cluster_stocks

path = (Path.cwd() / "data").resolve()

start_date = "2015-12-31"
end_date = "2019-12-31"

d_pass_csv = [
    {'source': Source.CSV, 'tickers': [], 'path': path, 'start_date': start_date, 'end_date': end_date},
]


def test_cluster_stocks_pass_0():
    d = d_pass_csv[0]
    data = download(**d)
    data.dropna(how="all").replace([np.inf, -np.inf], np.nan)
    cluster_stocks(data, n_clusters=4, verbose=True)



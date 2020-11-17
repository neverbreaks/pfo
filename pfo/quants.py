import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pfo.valuations import cov_matrix, variance, yearly_returns

def mc_random_portfolios(data, rfr = 0.01, num_portfolios = 10000):

    pf_ret = [] # Define an empty array for portfolio returns
    pf_vol = [] # Define an empty array for portfolio volatility
    pf_weights = [] # Define an empty array for asset weights

    num_assets = len(data.columns)
    pf_cvm = cov_matrix(data)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        pf_weights.append(weights)

        returns = np.dot(weights, yearly_returns(data,type='year')) # Returns are the product of individual expected returns of asset and its
                                          # weights
        pf_ret.append(returns)

        var = variance(pf_cvm, weights) # Portfolio Variance
        sd = np.sqrt(var) # Daily standard deviation
        ann_sd = sd*np.sqrt(252) # Annual standard deviation = volatility
        pf_vol.append(ann_sd)

    df_rv = {'Returns': pf_ret, 'Volatility': pf_vol}

    for counter, symbol in enumerate(data.columns.get_level_values(1), start=0):
        df_rv[symbol + ' weight'] = [w[counter] for w in pf_weights]

    portfolios = pd.DataFrame(df_rv)
    portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[16, 10])

    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
    print(min_vol_port)
    plt.subplots(figsize=[16, 10])
    plt.scatter(portfolios['Volatility'], portfolios['Returns'], marker='o', s=10, alpha=0.3)
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)

    optimal_risky_port = portfolios.iloc[((portfolios['Returns'] - rfr) / portfolios['Volatility']).idxmax()]
    print(optimal_risky_port)
    # Plotting optimal portfolio
    #plt.subplots(figsize=(10, 10))
    #plt.scatter(portfolios['Volatility'], portfolios['Returns'], marker='o', s=10, alpha=0.3)
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)


    plt.show()
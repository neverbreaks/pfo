import pandas as pd

from pfo.stocks.returns import mean_returns, volatility, downside_volatility


def ratios(data: pd.DataFrame, risk_free_rate=0.001, verbouse = False):
    yearly = mean_returns(data, type='log')
    vol = volatility(data)
    downside_vol =  downside_volatility(data)

    df_results = pd.concat(
        [yearly, vol, downside_vol],
        keys=['Yearly mean returns', 'Volatility', 'Downside Volatility'], join='inner', axis=1)

    df_results['Sharp Ratio'] =  (df_results['Yearly mean returns']-risk_free_rate)/df_results['Volatility']
    df_results['Sortino Ratio'] = (df_results['Yearly mean returns'] - risk_free_rate) / df_results['Downside Volatility']

    if verbouse:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df_results)

    return df_results
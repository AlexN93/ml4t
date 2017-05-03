"""MC2-P1: Market simulator."""

import pandas as pd
import os

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def compute_portvals(orders_file, start_val):
    # initiate orders data frame and then sort by date
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders_df.sort_index(inplace=True)
    orders_df['Transaction'] = orders_df.Order.apply(lambda o: 1 if o == 'BUY' else -1)

    # creates list of symbols and get rid of duplicates
    symbol_list = orders_df['Symbol'].tolist()
    symbols = list(set(symbol_list))

    # creates a date range from orders start and end date
    start_date = orders_df.iloc[0].name
    end_date = orders_df.iloc[-1].name
    dates = pd.date_range(start_date, end_date)

    # initiate prices data frame for the given symbols
    prices_all = get_data(symbols, dates)
    # removes SPY and adds Cash
    prices_df = prices_all[symbols]
    prices_df['Cash'] = 1.00

    # initiate trade data frame filled with zeroes
    trades_df = pd.DataFrame(0.00, index=prices_df.index, columns=symbols)
    trades_df['Cash'] = 0.00

    for i, row in orders_df.iterrows():
        trades_df.ix[i][row['Symbol']] += row['Shares'] * row['Transaction']
        # uncomment when running tests
        trades_df.ix[i]['Cash'] += prices_df.ix[i][row['Symbol']] * row['Shares'] * row['Transaction'] * -1
        # trades_df.ix[i]['Cash'] += row['Shares'] * row['Transaction'] * -1

    # initiate holdings data frame filled with zeroes and fill in the first row
    holdings_df = pd.DataFrame(0.00, index=prices_df.index, columns=symbols)
    holdings_df['Cash'] = 0.00
    holdings_df['Cash'][0] = start_val + trades_df['Cash'][0]
    for k in range(0, len(symbols)):
        holdings_df[symbols[k]][0] = trades_df[symbols[k]][0]

    for i in range(1, len(holdings_df)):
        holdings_df['Cash'][i] = holdings_df['Cash'][i - 1] + trades_df['Cash'][i]
        for k in range(0, len(symbols)):
            holdings_df[symbols[k]][i] = holdings_df[symbols[k]][i - 1] + trades_df[symbols[k]][i]

    # value_df
    value_df = prices_df * holdings_df
    return value_df.sum(axis=1)

def test_run():
    """Driver function."""
    # Define input parameters
    orders_file = os.path.join("data", "orders.csv")
    start_val = 1000000

    # Process orders
    portvals = compute_portvals(orders_file, start_val)

    start_date = portvals.index[0]
    end_date = portvals.index[-1]

    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a SPY-only reference portfolio to get stats
    prices_SPX = get_data(['SPY'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['SPY']]  # remove SPY
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against $SPX
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])
    print "Final SPY Value: {}".format(portvals_SPX[-1] * start_val)

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPX['SPY']], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value", ylabel="Normalized Price")

if __name__ == "__main__":
    test_run()
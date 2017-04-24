import numpy as np
import pandas as pd
import datetime as dt

from util import get_data, plot_normalized_data

# compute portfolio value for each and every day of the period and return a dataset
# https://screencloud.net/v/6r0V
def compute_portfolio_value(prices, allocs, sv=1):
    normed = prices/prices.ix[0]
    alloced = normed*allocs
    pos_vals = alloced*sv
    port_val = pos_vals.sum(axis=1)
    return port_val


def compute_portfolio_stats(prices, allocs, rfr=0.0, sf=252.0, sv=1):
    port_val = compute_portfolio_value(prices, allocs, sv)

    # daily return - dataset of daily returns (positive or negative)
    daily_ret = port_val.pct_change()[1:]

    # cumulative return
    cum_ret = (port_val[-1] / port_val[0]) - 1

    # average daily return
    avg_daily_ret = daily_ret.mean()

    # standart diviation
    std_daily_ret = daily_ret.std()

    # sharpe ratio
    sharpe_ratio = np.sqrt(sf) * ((daily_ret - rfr).mean() / std_daily_ret)

    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


def assess_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1),
                     syms=['GOOG','AAPL','GLD','XOM'],
                     allocs=[0.1,0.2,0.3,0.4],
                     sv=1000000, rfr=0.0, sf=252.0,
                     gen_plot=False):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(prices, allocs, rfr, sf, sv)

    # Print statistics
    print "Start Date:", sd
    print "End Date:", ed
    print "Symbols:", syms
    print "Allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret
    print "\n"

    df_temp = pd.concat([compute_portfolio_value(prices, allocs, sv), prices_all['SPY']], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, "Daily portfolio value and SPY")


if __name__ == "__main__":
    assess_portfolio(dt.datetime(2010,1,1), dt.datetime(2010,12,31), ['GOOG','AAPL','GLD','XOM'], [0.2, 0.3, 0.4, 0.1])

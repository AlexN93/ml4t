"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_normalized_data
from analysis import compute_portfolio_value, compute_portfolio_stats


def sharpe_maximizer(allocs, prices):
    """Optimization function to be passed to the optimizer.
    
    Parameters
    ----------
        prices: daily prices for each stock in portfolio
        allocs: Allocation for each portfolio component
    
    Returns
    -------
        sharpe_ratio: Negative sharpe ratio so the minimizer finds the maximum
    
    """
    #Get portfolio statistics
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(prices, allocs)

    return -sharpe_ratio
    
    
def find_optimal_allocations(prices):
    """Find optimal allocations for a stock portfolio, optimizing for Sharpe ratio.

    Parameters
    ----------
        prices: daily prices for each stock in portfolio

    Returns
    -------
        allocs: optimal allocations, as fractions that sum to 1.0
    """

    #Initial guess, equally weighted portfolio
    init_guess = np.ones(prices.shape[1], dtype=np.float64) * 1.0 / prices.shape[1]
    alloc_bounds = [(0, prices.shape[1])] * 4
    alloc_constraint = ({ 'type': 'eq', 'fun': lambda x: np.sum(x) - 1 })
    # alloc_constraint = ({'type': 'eq', 'fun': lambda x: 50.0 - np.sum(x)})
    min_result = spo.minimize(sharpe_maximizer, init_guess, args=(prices, ),
                              method='SLSQP', options={'disp': True},
                              bounds=alloc_bounds, constraints=alloc_constraint)

    # Print optimization results
    # print min_result
    return min_result.x

# optimize the porfolio (funds allocation) by sharpe ratio, when we do that we get a better end returns and portfolio
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):
    """Simulate and optimize portfolio allocations."""
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get optimal allocations for sharpe ration and tehn compute portfolio stats - THE DIFFERENCE FROM MC1_P1
    allocs = find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations, if they don't sum to 1.0

    # Get daily portfolio value (already normalized since we use default start_val=1.0)
    port_val = compute_portfolio_value(prices, allocs)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(prices, allocs)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Optimal allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    df_temp = pd.concat([port_val, prices_all['SPY']], keys=['Portfolio', 'SPY'], axis=1)
    plot_normalized_data(df_temp, "Daily portfolio value and SPY")

    return allocs, cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


if __name__ == "__main__":
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']

    allocs, cr, adr, sddr, sr = optimize_portfolio(start_date, end_date, symbols)



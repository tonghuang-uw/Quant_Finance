import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from scipy.optimize import minimize

def getData(portfolio, start, end = datetime.today().strftime('%Y-%m-%d')):
    df = yf.download(portfolio, start = start, end = end)
    df = df['Adj Close']
    return df

def getStats(price):
    ret = price.pct_change()
    
    # annualize metrics
    mu = ret.mean() * 252
    std = ret.std() * np.sqrt(252)
    cov_mat = ret.cov() * 252

    # transform into numpy array
    mu_vec = np.array(mu)
    std_vec = np.array(std)
    cov_mat = np.array(cov_mat)
    return mu_vec, std_vec, cov_mat

def portfolio_variance(weight, cov_mat):
    return weight.T @ cov_mat @ weight

def minimum_variance_portfolio(portfolio, start, end = datetime.today().strftime('%Y-%m-%d')):
    num_assets = len(portfolio)
    df = getData(portfolio, start)
    mu_vec, std_vec, cov_mat = getStats(df)

    constraints = (
        {
            'type':'eq',
            'fun':lambda weights: sum(weights) - 1

        }
    )
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_weights = np.ones(num_assets) / num_assets
    optimal_portfolio = minimize(lambda weights: portfolio_variance(weights, cov_mat), initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    optimal_weights = optimal_portfolio.x
    return optimal_weights

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import minimize
from minimum_variance_portfolio import getStats, getData
from portfolio_metrics import port_ret, port_variance

def portfolio_variance(weight, cov_mat):
    return weight.T @ cov_mat @ weight

def efficientFrontier(portfolio, start, end = datetime.today().strftime('%Y-%m-%d')):

    num_assets = len(portfolio)
    num_port = 100

    df = getData(portfolio, start, end)
    mu_vec, std_vec, cov_mat = getStats(df)

    # assign empty array
    port_weight = np.zeros((num_port, 2))
    port_ret_vec = np.zeros(num_port)
    port_std_vec = np.zeros(num_port)
    port_rtol_vec = np.zeros(num_port)


    # Construct # of num_port - portfolio

    for nport in range(1, num_port+1):
        rtol = (nport-1) * 0.04
        constraints = (
        {
            'type': 'eq',
            'fun': lambda weights: sum(weights) - 1,
        }
    )
        bounds = tuple((0, 1) for asset in range(num_assets))
        initial_weights = np.ones(num_assets) / num_assets
        optimal_portfolio = minimize(lambda weights: portfolio_variance(weights, cov_mat) - rtol * mu_vec.T @ weights,
                                    initial_weights,
                                    method = 'SLSQP',
                                    bounds = bounds,
                                    constraints = constraints)
        port_weight[nport-1, 0], port_weight[nport-1, 1] = optimal_portfolio.x
        port_ret_vec[nport-1] = port_ret(port_weight[nport-1], mu_vec)
        port_std_vec[nport-1] = np.sqrt(port_variance(port_weight[nport-1], cov_mat))
        port_rtol_vec[nport-1] = rtol
    
    return port_weight, port_ret_vec, port_std_vec, port_rtol_vec

portfolio = ['AAPL', 'TSLA']
port_weight, port_ret_vec, port_std_vec, port_rtol_vec = efficientFrontier(portfolio, '2015-01-01')

# Assume a risk-free rate of 0.03
rf = 0.03

optimal_idx = np.argmax((port_ret_vec - rf)/port_std_vec)
optimal_ret = port_ret_vec[optimal_idx]
optimal_std = port_std_vec[optimal_idx]
slope = (optimal_ret - rf)/optimal_std

cal_std = np.array([0, optimal_std * 2])
cal_ret = rf + slope * cal_std

plt.plot(port_std_vec, port_ret_vec)
plt.plot(port_std_vec[optimal_idx], port_ret_vec[optimal_idx], '*')
plt.plot(cal_std, cal_ret, 'r--', label='Capital Allocation Line')
plt.xlabel('Portfolio Standard Deviation')
plt.ylabel('Portfolio Return')
plt.title('Efficient Frontier')
plt.show()
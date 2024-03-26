import numpy as np
import pandas as pd


def port_ret(weights, ret_vec):
    return weights.T @ ret_vec

def port_variance(weights, cov_mat):
    return weights.T @ cov_mat @ weights

def port_sharpe(ret, variance, rf):
    return (ret - rf)/np.sqrt(variance)
import numpy as np
from scipy.optimize import minimize
from scipy.stats import t
from scipy.stats import skew
from scipy.special import beta
from scipy.special import gamma

def nu(lam, p, q):
    
    a = 1 + 3 * lam ** 2
    b = beta(3/p, q - 2/p) / beta(1/p, q)
    c = 4 * lam ** 2
    d = (beta(2/p, q - 1/p) ** 2) / (beta(1/p, q) ** 2)

    numerator = q ** (- 1/p)
    denominator = np.sqrt(a * b - c * d)

    return numerator / denominator


def m(lam, nu, sigma, p, q):
    a = lam * nu * sigma
    b = (2 * q ** (1/p) * beta(2/p, q - 1/p)) / beta(1/p, q)

    return a * b


def pdf(x, mu, sigma, lam, p, q):
    a = 2 * nu(lam, p, q) * sigma * q ** (1/p) * beta(1/p, q)

    b = x - mu + m(lam, nu(lam, p, q), sigma, p, q)

    c = np.abs(b) ** p

    d = q * (nu(lam, p, q) * sigma) ** p

    e = (1 + lam * np.sign(b)) ** p

    den = a * (1 + c / (d * e)) ** (1/p + q)

    return p/den

def neg_likelihood_function(params, data):
    mu, sigma, lam, p, q = params

    pdf_values = pdf(data, mu, sigma, lam, p, q)
    return -np.sum(np.log(pdf_values))

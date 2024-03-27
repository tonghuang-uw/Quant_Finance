# Modern Portfolio Theory

This repository delves into the subject of portfolio theory, detailing the creation of the efficient frontier, the composition of the optimal portfolio, and the delineation of the capital allocation line. Additionally, it features a straightforward mean-variance portfolio using FAANG stocks. Furthermore, there is a project included that highlights the necessary skills an allocator would need to assemble portfolios tailored to various specific needs.

## Note

Modern portfolio theory is a mathematical framework to maximize the portfolio expected return and minimize the volatility. MPT assumes that investors are risk averse, meaning that given two portfolios that offer the same expected return, investors will prefer the less risky one. Thus, an investor will take on increased risk only if compensated by higher expected returns.

## Efficient Frontier

### Efficient Frontier Calculation using Matrices

Matrices are preferred for calculations of the efficient frontier.

In matrix form, for a given "risk tolerance" $\( q \in [0, \infty) \)$, the efficient frontier is found by minimizing the following expression:

$\( w^T \Sigma w - q R^T w \)$

where

- $\( w \in \mathbb{R}^N \)$ is a vector of portfolio weights and $\( \sum w_i = 1 \)$. (The weights can be negative);
- $\( \Sigma \in \mathbb{R}^{N \times N} \)$ is the covariance matrix for the returns on the assets in the portfolio;
- $\( q \geq 0 \)$ is a "risk tolerance" factor, where 0 results in the portfolio with minimal risk and $\( \infty \)$ results in the portfolio infinitely far out on the frontier with both expected return and risk unbounded; and
- $\( R \in \mathbb{R}^N \)$ is a vector of expected returns.
- $\( w^T \Sigma w \in \mathbb{R} \)$ is the variance of portfolio return.
- $\( R^T w \in \mathbb{R} \)$ is the expected return on the portfolio.

## Risk-free asset and the capital allocation line

The introduction of a risk-free asset creates a new efficient frontier, depicted as a straight line in the graph that touches the hyperbola at the point where the purely risky portfolio exhibits the maximum Sharpe ratio. This efficient half-line is called the capital allocation line (CAL), and its formula can be shown to be:

$\ E(R_C) = R_F + \sigma_C \frac{E(R_P) - R_F}{\sigma_P} \$

In this formula P is the sub-portfolio of risky assets at the tangency with the Markowitz bullet, F is the risk-free asset, and C is a combination of portfolios P and F.

## Mean Variance portfolio Demonstration

### Efficient Frontier Plot with FAANG
![Efficient Frontier](https://github.com/tonghuang-uw/Quant_Finance/assets/62912258/fd373bee-c11f-407c-b723-cc3a961cae6e)

### Optimal Weight Plot with FAANG
![Optimal Weight](https://github.com/tonghuang-uw/Quant_Finance/assets/62912258/e8d378b7-e685-4638-a165-451e35ed221a)

## Asset Allocation Project

[project](Asset_Allocation_Project/README.md)



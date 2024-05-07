# Portfolio Analysis

## Project Overview

The purpose of this project is to Calculate Market and Credit Value at Risk (VaR) and Expected Short Fall (ES) of a portfolio of “Corporate” Zero Coupon Bonds with different maturities.

## Data

- The “US treasury.csv” file contains the time-series of annual yield term structure yt, for t =30 days, 90 days, ..., 10950 days (real = 30years). These yields correspond to the discount rate (risk free) one should use to price any instrument on a given time.
- File “TransitionMatrix.csv” contains the 1 year transition probability matrix for different credit ratings
- File “credit spreads.csv” contains the credit spreads (annual rates) that need to be added to the risk free rate in order to compensate for possibility of default of the counterparty. The lower the credit rating, the more likely the bond issuer will default, and hence the higher the credit spread.

## Methodology

We assume that the credit spread term structure remains constant. That is, today the credit spread of a BBB bond with 2 year maturity is 0.1902% (continuously compounded), while 1 year from now another BBB bond that also matures in 2 years (i.e., 3 years from now) also has 0.1902% credit spread.

In general, the value of a corporate zero-coupon bond maturing in one year with $100 face value is given by

$$
B(t, t_M, R_t, \rho) = 100 e^{-y_{t_M} \frac{t_M - t}{365} } (1_{\{\tau > t\}} \mathrm{P}[1_{\tau > t_M}] + \rho (1 - 1_{\tau > t} \mathrm{P}[1_{\tau > t_M} ] ))
$$

$$
= 100 e^{-y_{t_M} \frac{t_M - t}{365}} (1_{\tau > t} e^{-s_{t_m}^{R_t} \frac{t_M-t}{365}} + \rho (1 - 1_{\tau > t} e^{-s_{t_m}^{R_t} \frac{t_M-t}{365}}))
$$

where $t \geq 0$ is the current time (or the time of valuation), $t_M > t$ is the maturity time, $R_t$ is the credit rating of the bond at time $t$ (at time of valuation), $\theta \in [0, 1]$ is the recovery rate (\% of notional received at maturity if the bond has defaulted by time $T_M$), $y_{t_M}$ is the yield rate (risk free) for a bond maturing at time $T_M$, and $s^R_{t_M}$ is the credit spread used to discount a bond maturing at time $T_M$ which has credit rating $R_t$ at time $t$.


### The standard Ornstein Uhlenbeck Model

Consider the stochastic process $(X_t)_{t \geq 0}$ described by the SDE,

$$ dX_t = k (\theta - X_t) dt + \sigma dB_t , \quad X_t \in \mathbb{R}, X_0 = x $$

where $k > 0$ is the mean reverting rate, $\theta \in \mathbb{R}$ is the long-run mean, $\sigma > 0$ is the volatility and $B_t$ is the standard
Brownian motion. The solution to this SDE is given by

$$ X_t = \theta (1 - e^{-kt}) + x e^{-kt} + \sigma \int^t_0 e^{-k(t-s)} dB_s, \quad t \geq 0 $$

We get 

$$ \mathbb{E} [X_t | X_0 = x] = xe^{-kt} + \theta (1 - e^{-kt}) $$

and

$$ Cov (X_t , X_s | X_0 = x) = \frac{\sigma^2}{2k}(e^{-k|t-s|} - e^{-k(t+s)})$$


### Parameter Estimation

The Ornstein-Uhlenbeck (OU) process is closely related to the Autoregressive (AR(1)) process. For discrete observations $X = (X_0, X_1, \ldots, X_n)$, we can express the OU process in discrete form as follows, given the time intervals $\Delta t = t_i - t_{i-1}$:

$$x_i = (1 - e^{-k\Delta t}) + e^{-k\Delta t}x_{i-1} + \frac{\sigma}{\sqrt{2k}}(1 - e^{-2k\Delta t})^{1/2}z, \quad z \sim N(0,1)$$

Using the Itô isometry, we transform the stochastic integral, enabling the equation to be represented as a linear model:

$$ \tilde{x}_i = a + b \tilde{x} _{i-1} + \epsilon $$

Where $\epsilon$ is the residual term. By applying Ordinary Least Squares (OLS), we can estimate the parameters $a$, $b$, and $\epsilon$. The parameters of the OU process can be derived as:

$$\kappa = -\frac{\ln(b)}{\Delta t}$$
$$\theta = \frac{a}{1 - b}$$
$$\sigma = \frac{\text{Std}(\epsilon)}{\sqrt{\Delta t}} \sqrt{-2\ln(b)(1 - b^2)}$$

In a multivariate setting, the OU process for each dimension $j$ is expressed as:

$$X_t^j = \theta_j (1 - e^{-k_j t}) + x_j e^{-k_j t} + \sigma_j \int_0^t e^{-k_j (t-s)} dB_s^j$$

Correlations between different dimensions can be calculated through the correlation of their respective Brownian motions:

$$\text{Corr}(B_t^k, B_t^j) = \rho_{k,j}$$

Residuals from each OU process can also be correlated to investigate the relationships between different processes:

$$\rho_{k,j} = \text{Corr}(\epsilon_k, \epsilon_j)$$

### Monte Carlo Simulation

The Ornstein-Uhlenbeck (OU) process is normally distributed with the mean and standard deviation dependent on time and the initial state. The mean and variance at time $t$ are given by:

$$\mu_t = \theta (1 - e^{-k(t-s)}) + X_s e^{-k(t-s)}$$
$$\sigma_t = \frac{\sigma}{\sqrt{2k}} \sqrt{1 - e^{-2k(t-s)}}$$

#### Simulation Procedure
To simulate a sample path over a time grid $T = \{t_0, t_1, \ldots, t_N\}$, follow these steps sequentially:

##### Pseudo Code
1. Generate the time-grid $T = \{t_0, t_1, \ldots, t_N\}$
2. Set $x[0] = X_{t_0}$
3. For $i = 1$ to $N$:
   - Obtain $\mu_t$ and $\sigma_t$ using $x[i - 1]$ and $(t - s) = t_i - t_{i-1}$
   - Draw a random variable $z$ from $N(\mu_t, \sigma_t^2)$
   - Set $x[i] = z$

##### Extending to Multivariate Case
The procedure can be extended to a multivariate setting where $(X_t^1, X_t^2, \ldots, X_t^n)$ follows a multivariate normal distribution with means $\mu_t = (\mu_t^1, \ldots, \mu_t^n)$ and covariance matrix $\Sigma_t = D\rho_t D$. Here, $D$ is a diagonal matrix of the instantaneous volatilities $(\sigma_1, \ldots, \sigma_n)$, and $\rho_t$ (time-dependent) is given by the matrix whose elements are:

$$\rho_{t_{ij}} = \frac{\rho_{ij} (1 - e^{-(\kappa_i + \kappa_j)(t-s)})}{\kappa_i + \kappa_j}, \quad i, j = 1, \ldots, n.$$

Here $\rho_{ij}$ is the instantaneous correlation of Brownian motions.




# Portfolio Analysis

## Project Overview

The purpose of this project is to Calculate Market and Credit Value at Risk (V aR) and Expected Short Fall (ES) of a portfolio of “Corporate” Zero Coupon Bonds with different maturities.

## Data

- The “US treasury.csv” file contains the time-series of annual yield term structure yt, for t =30 days, 90 days, ..., 10950 days (real = 30years). These yields correspond to the discount rate (risk free) one should use to price any instrument on a given time.
- File “TransitionMatrix.csv” contains the 1 year transition probability matrix for different credit ratings
- File “credit spreads.csv” contains the credit spreads (annual rates) that need to be added to the risk free rate in order to compensate for possibility of default of the counterparty. The lower the credit rating, the more likely the bond issuer will default, and hence the higher the credit spread.

## Methodology

We assume that the credit spread term structure remains constant. That is, today the credit spread of a BBB bond with 2 year maturity is 0.1902% (continuously compounded), while 1 year from now another BBB bond that also matures in 2 years (i.e., 3 years from now) also has 0.1902% credit spread.

In general, the value of a corporate zero-coupon bond maturing in one year with $100 face value is given by

$$B(t, t_M, R_t, \theta) = 100 e^{-y_{t_M} \frac{t_M - t}{365}} \left( \mathbf{1}_{\{ \tau > t \}} \mathbb{P}[\tau > t_M] + \theta (1 - \mathbf{1}_{\{ \tau > t \}}) \mathbb{P}[\tau > t_M] \right) $$

$$ = 100 e^{-y_{t_M} \frac{t_M - t}{365}} \left( \mathbf{1}_{\{ \tau > t \}} e^{-s^R_{t_M} \frac{t_M - t}{365}} + \theta (1 - \mathbf{1}_{\{ \tau > t \}}) e^{-s^R_{t_M} \frac{t_M - t}{365}} \right)
$$

where $t \geq 0$ is the current time (or the time of valuation), $t_M > t$ is the maturity time, $R_t$ is the credit rating of the bond at time $t$ (at time of valuation), $\theta \in [0, 1]$ is the recovery rate (\% of notional received at maturity if the bond has defaulted by time $T_M$), $y_{t_M}$ is the yield rate (risk free) for a bond maturing at time $T_M$, and $s^R_{t_M}$ is the credit spread used to discount a bond maturing at time $T_M$ which has credit rating $R_t$ at time $t$.


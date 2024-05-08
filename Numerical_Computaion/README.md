# Numerical Computation for Derivative Pricing

In the realm of financial derivatives, European call options hold a position of great impor- tance and widespread application. 
These options provide the holder the right, but not the obligation, to purchase an underlying asset at a predetermined price, 
known as the strike price, on a specific expiration date. They are not only a fundamental tool for risk manage- ment and speculative 
activities but also serve as critical components in hedging strategies and portfolio optimization. Given their central role, accurately 
pricing these options is a task of paramount importance for both individual investors and financial institutions. 
At its core, the model employs a partial differential equation (PDE) to describe the dynamics of option pricing, 
factoring in elements such as the underlying asset’s price, time to expiration, volatility, and the risk-free interest rate.


The Black-Scholes Partial Differential Equation(PDE) is described below:

$$ \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0$$

## Methodology

- Forward Euler: 
Simplicity and ease of implementation. Computationally efficient, requiring minimal computational resources.
- Backward Euler: 
Unconditionally stable, making it suitable for long-term options and high-volatility

## Model Setup

Let $u(t, S) := V(T - t, S)$. Replace $S \rightarrow \infty$ with $\bar{S}$ where $\bar{S}$ is 
sufficiently larger than the strike price K. Then, the problem reads

$$\frac{\partial u}{\partial t} = \frac{\sigma^2}{2} S^2 \frac{\partial^2 u}{\partial S^2} + rS \frac{\partial u}{\partial S} - ru,
\quad S \in [0, \bar{S}], t \in [0, T]$$

The boundary conditions are:

$$
u(0, S) = \mathrm{Max}(S-K,0)
$$

$$
u(t, \bar{S}) = \bar{S} - Ke^{-r(T)},
\quad t \in [0, T]
$$

$$
u(t,0) = 0
$$

Choose $1 < m \in \mathbb{N}$, let $h = \frac{\bar{S}}{m}$ and $S_k = k \cdot h$ for $k = 0, \ldots, m$. Approximate

$$
\frac{\partial^2 u}{\partial S^2}(t, S_k) \approx \frac{u(t, S_{k+1}) - 2u(t, S_k) + u(t, S_{k-1})}{h^2}
$$

$$
\frac{\partial u}{\partial S}(t, S_k) \approx \frac{u(t, S_{k+1}) - u(t, S_{k-1})}{2h}
$$

For all $k = 1, \ldots, m-1$ and $t \in [0, T]$. This yields the ODE

$$
v'(t) = M^{(m)} v(t) + f^{(m)}(t)
$$

where

$$
M^{(m)} := \frac{\sigma^2}{2} D^{(m)} + \frac{1}{h^2} A^{(m)} + rD \frac{1}{2h} B^{(m)} - rI
$$

The initial condition is

$$
v(0) = \left( u(0, S_1), \ldots, u(0, S_{m-1}) \right)^T.
$$

### Analytic Solution

The price of a European call option $C(S, t)$ is given by the Black-Scholes formula:

$$
C(S, t) = S_0 N(d_1) - K e^{-r(T - t)} N(d_2)
$$

where,

$$
d_1 = \frac{\ln\left(\frac{S_0}{K}\right) + \left(r + \frac{\sigma^2}{2}\right)(T - t)}{\sigma \sqrt{T - t}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T - t}
$$

## Result

### Forward Euler
![forward euler](https://github.com/tonghuang-uw/Quant_Finance/assets/62912258/f9e93f1a-86c8-4117-8738-595d4c79a666)

### Backward Euler
![Backward_Euler](https://github.com/tonghuang-uw/Quant_Finance/assets/62912258/e6cc9ab1-7d49-48b7-b9d7-2d34ee9fd757)

### True Solution
![True_solution](https://github.com/tonghuang-uw/Quant_Finance/assets/62912258/c589ef81-b3d2-435c-b319-44b0eea8a3aa)





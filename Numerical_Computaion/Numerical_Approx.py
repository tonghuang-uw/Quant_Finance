import numpy as np
import matplotlib.pyplot as plt
import scipy
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
import pandas as pd
## First to determine constants
# Evaluating a European call option that has the strike price 100, expires in 6 months, volatility is 0.2,
# interest rate is 0.01

k = 50  # Strike price
T = 0.5  # Time to expiration in years
sigma = 0.2  # Volatility
r = 0.01

# setting up stock price S, S has interval [0, \bar{S}], where \bar{S} can be chosen as a number that is large enough,
# we make \bar{S} to be four times the strike price

S_bar = 4*k

# Choose dt and ds. 
# First we choose dt = 0.05 and ds = 5

t0 = 0
dt = 0.0005

s0 = 0
ds = 1
df_dict = {}
err_dict = {}
t = np.linspace(T, 0, int(T/dt)+1)
s = np.arange(s0, S_bar + ds/2, ds)
Nt = len(t)
Ns = len(s)
print(t)
print(s)
U = np.zeros((Ns, Nt))
U[:, 0] = np.maximum(s-k, 0)
U[0, :] = 0
U[-1, :] = S_bar - k * np.exp(-r*t)


def metrics(m):
    print(m)
    time_index = np.argmin(np.abs(t - 0.4))
    # Then we find the indices in the stock price grid that corresponds to s=[100, 105,...,200]
    s_values = np.arange(100, 200 + ds/2, ds*10)
    stock_indices = [(np.abs(s - S_i)).argmin() for S_i in s_values]
    # Now we can extract the desired values from the grid U
    U_desired = m[stock_indices, time_index]
    return U_desired

# True solution of European Call

def European_call(S, K, T, r, sigma):
    '''
    True solution of European call option
    s: float - current stock price
    k: float - strike price
    T: float - maturity date
    r: float - interest rate
    sigma: float - volatility

    Return:
    float - value of european price
    '''
    if T == 0:  # At expiration, return intrinsic value
        return max(0, S - K)
    else:
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
        return call_price
True_call_solution = np.zeros((Ns, Nt))

for i, S_i in enumerate(s):
    for j, t_j in enumerate(t):
        True_call_solution[i, j] = European_call(S_i, k, T - t_j, r, sigma)

T, S = np.meshgrid(t, s)
# ax = plt.axes(projection = '3d')
# ax.plot_surface(T, S, True_call_solution, cmap = 'viridis')
# ax.set_xlabel('Time to maturity')
# ax.set_ylabel('Stock price')
# ax.set_zlabel('Option value')
# ax.set_title('European call price (True Solution)')
# plt.show()

df_dict["Analytics"] = metrics(True_call_solution)

# create the diagonal matrix for stock price s

d = np.diag(s[1:-1])
A = np.diag(-2 * np.ones(Ns - 2)) + np.diag(np.ones(Ns - 3), 1) + np.diag(np.ones(Ns - 3), -1)
B = np.diag(np.ones(Ns - 3), 1) + np.diag(-np.ones(Ns - 3), -1)
I = np.eye(Ns - 2)

M = ((sigma**2 / 2) * d**2) @ (A / ds**2) + (r * d) @ (B / (2 * ds)) - r * I

def c(t):
    c_vector = np.zeros((Ns - 2,1))
    c_vector[-1] = ((sigma**2 * S_bar**2)/(2*ds**2) + (r*S_bar)/(2*ds)) * (S_bar - k * np.exp(-r * t))
    return c_vector

def f(t, vec_c, u):
    return M @ u + vec_c

# Forward Euler

for j in range(Nt - 1):
    U[1:-1, (j+1):(j+2)] = U[1:-1, j:(j+1)] + dt * f(t[j], c(t[j]), U[1:-1, j:(j+1)])

forward_err = np.max(np.abs(U - True_call_solution))

df_dict["Forward_Euler"] = metrics(U)
err_dict["FE_err"] = df_dict["Forward_Euler"] - df_dict["Analytics"]


T,S = np.meshgrid(t, s)
# ax = plt.axes(projection = '3d')
# ax.plot_surface(T,S,U, cmap = 'viridis')
# ax.set_xlabel('Time to Maturity')
# ax.set_ylabel('Stock Price')
# ax.set_zlabel('Option Value')
# plt.title('European Call Option Value by Forward Euler')
# plt.show()

# Backward Euler

lhs = I - dt*M

for j in range(Nt-1):
    U[1:-1, (j+1):(j+2)] = np.linalg.solve(lhs, U[1:-1, j:(j+1)] + dt * c(t[j+1]))

backward_err = np.mean(np.abs(U - True_call_solution))
print(backward_err)
T,S = np.meshgrid(t, s)

df_dict["Backward_Euler"] = metrics(U)
err_dict["BW_err"] = df_dict["Backward_Euler"] - df_dict["Analytics"]


# ax = plt.axes(projection = '3d')
# ax.plot_surface(T,S,U, cmap = 'viridis')
# ax.set_xlabel('Time to Maturity')
# ax.set_ylabel('Stock Price')
# ax.set_zlabel('Option Value')
# plt.title('European Call Option Value by Backward Euler')
# plt.show()

# Trapezoidal method

lhs = I - (dt/2)*M
rhs = I + (dt/2)*M

for j in range(Nt-1):
    c_term = dt/2 * (c(t[j]) + c(t[j+1]))
    U[1:-1, (j+1):(j+2)] = np.linalg.solve(lhs, rhs @ U[1:-1, j:(j+1)] + c_term)

T,S = np.meshgrid(t, s)
# ax = plt.axes(projection = '3d')
# ax.plot_surface(T,S,U, cmap = 'viridis')
# ax.set_xlabel('Time to Maturity')
# ax.set_ylabel('Stock Price')
# ax.set_zlabel('Option Value')
# plt.title('European Call Option Value by Trapezoidal Method')
# plt.show()

df_dict["Trapezoidal"] = metrics(U)
err_dict["Trap_err"] = df_dict["Trapezoidal"] - df_dict["Analytics"]



# Mid point and use trapezoidal method for the first step

U[1:-1, 1:2] = np.linalg.solve(lhs, rhs @ U[1:-1, 0:1] + dt/2 * (c(t[0]) + c(t[1])))

for j in range(1, Nt-1):
    U[1:-1, (j+1):(j+2)] = U[1:-1, (j-1):(j)] + 2 * dt * f(t[j], c(t[j]), U[1:-1, j:(j+1)])

T,S = np.meshgrid(t, s)
# ax = plt.axes(projection = '3d')
# ax.plot_surface(T,S,U, cmap = 'viridis')
# ax.set_xlabel('Time to Maturity')
# ax.set_ylabel('Stock Price')
# ax.set_zlabel('Option Value')
# plt.title('European Call Option Value by Midpoint Method')
# plt.show()

df_dict["Midpoint"] = metrics(U)
err_dict["Mid_err"] = df_dict["Midpoint"] - df_dict["Analytics"]
s_range = np.arange(100, 200+ds/2, ds*10)
s_range = ["S = "+ str(i) for i in s_range]
df_approx = pd.DataFrame(df_dict, index = s_range)
df_err = pd.DataFrame(err_dict, index = s_range)
df_approx = df_approx[["Forward_Euler", "Backward_Euler", "Trapezoidal", "Midpoint", "Analytics"]]
df_err = df_err[[ "FE_err", "BW_err", "Trap_err", "Mid_err"]]
df_err = df_err.round(5)
df_approx = df_approx.round(5)
print(df_approx)
print(df_err)
df_approx.to_csv('table_t04_dt0001_ds1.csv')
df_err.to_csv('err_table_t04_dt0001_ds1.csv')
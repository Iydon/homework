import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
# 比较模拟结果的分布特性.
import scipy.stats as scs
# 字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


def print_statistics(a1, a2):
    """
    Prints selected statistics.

    Parameters
    ==========
    al, a2 : ndarray objects
    results object from simulation
    """
    # 主体
    sta1 = scs.describe(a1)
    sta2 = scs.describe(a2)
    print("%14s %14s %14s"%("statistic", "data set 1", "data set 2"))
    print("-" * 45)
    print("%14s %14.3f %14.3f"%("size", sta1[0], sta2[0]))
    print("%14s %14.3f %14.3f"%("min", sta1[1][0], sta2[1][0]))
    print("%14s %14.3f %14.3f"%("max", sta1[1][1], sta2[1][1]))
    print("%14s %14.3f %14.3f"%("mean", sta1[2], sta2[2]))
    print("%14s %14.3f %14.3f"%("std", np.sqrt(sta1[3]), np.sqrt(sta2[3])))
    print("%14s %14.3f %14.3f"%("skew", sta1[4], sta2[4]))
    print("%14s %14.3f %14.3f"%("kurtosis", sta1[5], sta2[5]))


S0    = 100    # initial value
r     = 0.05   # constant short rate
sigma = 0.25   # constant volatility
T     = 2.0    # in years
I     = 10000  # number of random draws

ST1   = S0 * np.exp(
            (r-sigma**2/2)*T + sigma*np.sqrt(T)*npr.standard_normal(I)
        )
ST2   = S0 * npr.lognormal(mean  = (r-sigma**2/2)*T,
                           sigma = sigma*np.sqrt(T),
                           size  = I)
print_statistics(ST1, ST2)

"""
plt.hist(ST1, bins=50)
plt.xlabel("index level")
plt.ylabel("frequency")
plt.grid(True)
plt.show()
"""


# 几何布朗运动
S0    = 100    # initial value
r     = 0.05   # constant short rate
sigma = 0.25   # constant volatility

M  = 50
T  = 2.0
I  = 10000
dt = T / M
S  = np.zeros((M+1, I))
S[0] = S0
for t in range(1, M+1):
    S[t] = S[t-1] * npr.lognormal(mean  = (r-sigma**2/2)*dt,
                                 sigma = sigma*np.sqrt(dt),
                                 size  = I)

plt.plot(S[:, :10], lw=1.5)
plt.title("模拟几何布朗运动路径")
plt.xlabel("time")
plt.ylabel("index level")
plt.grid(True)
plt.show()


# 平方根扩散(欧拉格式)
x0    = 0.05
kappa = 3.0
theta = 0.02
sigma = 0.1

M  = 50
T  = 2.0
I  = 10000
dt = T / M
x  = np.zeros((M+1, I))
x[0] = x0
clamp = lambda x: np.maximum(x, 0)
for t in range(1, M+1):
    x[t] = x[t-1] + kappa*(theta-clamp(x[t-1]))*dt \
         + sigma*np.sqrt(clamp(x[t-1]))*np.sqrt(dt)*npr.standard_normal(I)
x = clamp(x)

plt.plot(x[:, :10], lw=1.5)
plt.title("模拟平方根扩散路径(欧拉格式)")
plt.xlabel("time")
plt.ylabel("index level")
plt.grid(True)
plt.show()


# 平方根扩散(精确格式)
x0    = 0.05
kappa = 3.0
theta = 0.02
sigma = 0.1

M  = 50
T  = 2.0
I  = 10000
dt = T / M
y  = np.zeros((M+1, I))
y[0] = x0
for t in range(1, M+1):
    df = 4*theta*kappa / sigma**2
    c  = (sigma**2 * (1-np.exp(-kappa*dt))) / (4*kappa)
    nc = np.exp(-kappa*dt) * y[t-1] / c
    y[t] = c * npr.noncentral_chisquare(df, nc, size=I)

plt.plot(y[:, :10], lw=1.5)
plt.title("模拟平方根扩散路径(精确格式)")
plt.xlabel("time")
plt.ylabel("index level")
plt.grid(True)
plt.show()


# 比较欧拉格式与精确格式
print_statistics(x[-1], y[-1])


# 随机波动率
r     = 0.05
v0    = 0.1
kappa = 3.0
theta = 0.25
sigma = 0.1
rho   = 0.6

M  = 50
T  = 2.0
I  = 10000
dt = T / M
v  = np.zeros((M+1, I))
v[0] = v0

ran_num = npr.standard_normal((2, M+1, I))
corr_mat = np.array([[1.0,rho], [rho,1.0]])
cho_mat  = np.linalg.cholesky(corr_mat)
clamp    = lambda x: np.maximum(x, 0)
for t in range(1, M+1):
    ran = np.dot(cho_mat, ran_num[:,t,:])
    v[t] = v[t-1] + kappa*(theta-clamp(v[t-1]))*dt \
         + sigma*np.sqrt(clamp(v[t-1]))*np.sqrt(dt)*ran[1]
v = clamp(v)

w0 = 100
w  = np.zeros((M+1, I))
w[0] = w0
for t in range(1, M+1):
    ran = np.dot(cho_mat, ran_num[:,t,:])
    w[t] = w[t-1] * np.exp((r-v[t])*dt +
                           np.sqrt(v[t])*np.sqrt(dt)*ran[0])

fig,(ax1,ax2) = plt.subplots(2, 1, sharex=True, figsize=(7,6))
ax1.plot(w[:,:10], lw=1.5)
ax1.set_title("模拟随机波动率模型路径")
ax1.set_ylabel("index level")
ax1.grid(True)
ax2.plot(v[:,:10], lw=1.5)
ax2.set_xlabel("time")
ax2.set_ylabel("volatility")
ax2.grid(True)

fig.show()

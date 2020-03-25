#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/01/23 14:00
# @Author   : Iydon
# @File     : bolling.py

# 绘图
import matplotlib.pyplot as plt
# 字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


def date_to_num(dates:list):
    """
    ["2017-01-01", "2017-01-02", ...]
    =>
    [736330.0, 736331.0, ...]
    """
    # 数据
    import datetime
    from matplotlib.pylab import date2num
    # 主体
    strptime = datetime.datetime.strptime
    return [date2num(strptime(date, "%Y-%m-%d")) for date in dates]

def get_data():
    """
    Get demo data.
    """
    # 数据
    import tushare as ts
    # 主体
    data = ts.get_k_data("002738", "2018-06-01", "2018-12-01")
    ret  = data.values
    ret[:,0] = date_to_num(ret[:,0])
    return ret

def bolling(asset:list, samples:int=20, alpha:float=0, width:float=2):
    """
    According to MATLAB:

    BOLLING(ASSET,SAMPLES,ALPHA,WIDTH) plots Bollinger bands for given ASSET
    data vector.  SAMPLES specifies the number of samples to use in computing
    the moving average.  ALPHA is an optional input that specifies the exponent
    used to compute the element weights of the moving average.  The default
    ALPHA is 0 (simple moving average).  WIDTH is an optional input that
    specifies the number of standard deviations to include in the envelope.  It
    is a multiplicative factor specifying how tight the bounds should be made
    around the simple moving average.  The default WIDTH is 2.  This calling
    syntax plots the data only and does not return the data.

    Note: The standard deviations are normalized by (N-1) where N is the
    sequence length.
    """
    # build weight vector
    import numpy as np
    # 主体
    r = len(asset)
    i = np.arange(1,samples+1) ** alpha
    w = i / sum(i)
    # build moving average vectors with for loops
    a = np.zeros((r-samples, 1))
    b = a.copy()
    for i in range(samples, r):
        a[i-samples] = np.sum( asset[i-samples:i] * w )
        b[i-samples] = width * np.sum(np.std( asset[i-samples:i] * w ))
    return a,a+b,a-b


data = get_data()
date = data[:,0]

samples = 20
mav,uband,lband = bolling(data[:,1], samples, 0, 2)
ind = range(samples, len(data[:,1]))

fig,ax = plt.subplots(figsize=(15,5))
plt.plot(date[ind], data[ind,1])
plt.plot(date[ind], mav)
plt.plot(date[ind], uband)
plt.plot(date[ind], lband)
plt.legend(['原始资产数据','移动平均值','移动平均值上界','移动平均值下界'])

plt.xticks(rotation=30)
ax.xaxis_date()
plt.xlabel('Date')
plt.ylabel('Price')

plt.grid(True)
plt.show()

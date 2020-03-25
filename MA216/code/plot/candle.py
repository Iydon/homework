#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/01/23 14:00
# @Author   : Iydon
# @File     : candle.py

# 绘图
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_finance as mpf


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


data = get_data()

fig,ax = plt.subplots(figsize=(15,5))
mpf.candlestick_ochl(ax, data[:,:-2], width=0.6, colorup='g', colordown='r', alpha=1.0)

plt.xticks(rotation=30)
ax.xaxis_date()
plt.xlabel('Date')
plt.ylabel('Price')

plt.grid(True)
plt.show()

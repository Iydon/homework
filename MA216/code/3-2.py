# -*- encode: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
# font
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['simhei']



start, end = '20170831', '20190927'
file = f'data/stock:{start}-{end}.csv'
time = pd.date_range(start, end)
data = pd.read_csv(file)

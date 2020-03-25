# -*- encode: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from cfgs import CFGS


def visualize_data(data, is_train:bool=True):
    day,hour,time = data
    titles = ["Day", "Hour", "Time"]
    if is_train:
        visualize_day_data(day, range(365))
        visualize_hour_data(hour, range(24*7))
    else:
        visualize_day_data(day)
        visualize_hour_data(hour)
    visualize_time_data(time)


def visualize_day_data(day, index=None):
    """Example
    >>> day = [day_train_x, day_train_y]
    >>> visualize_day_data(day)
    """
    cols = eval(CFGS["DATA"]["NOMCOL"])
    length = day[0].shape[0]
    index  = index or range(length)
    data_x = day[0][cols].iloc[index]
    data_y = day[1].iloc[index]
    plt.subplot(121)
    plt.plot(index, data_x)
    plt.legend(data_x.columns)
    plt.subplot(122)
    plt.plot(index, data_y)
    plt.legend(data_y.columns)
    plt.show()


def visualize_hour_data(hour, index=None):
    """Example
    >>> hour = [hour_train_x, hour_train_y]
    >>> visualize_hour_data(hour)
    """
    cols = eval(CFGS["DATA"]["NOMCOL"])
    length = hour[0].shape[0]
    index  = index or range(length)
    data_x = hour[0][cols].iloc[index]
    data_y = hour[1].iloc[index]
    plt.subplot(121)
    plt.plot(index, data_x)
    plt.legend(data_x.columns)
    plt.subplot(122)
    plt.plot(index, data_y)
    plt.legend(data_y.columns)
    plt.show()


def visualize_time_data(time, index=None):
    """Example
    >>> time = [time_train_x, time_train_y]
    >>> visualize_time_data(time)
    """
    length = time[0].shape[0]
    index  = np.array(index or range(length))
    time_x = time[0].iloc[index]
    time_y = time[1].iloc[index]
    for key,val in eval(CFGS["DATA"]["PLOTTIMECOL"]).items():
        for i in range(val[0], val[1]+1):
            idx = time_x[key] == i
            plt.plot(index[idx], time_y[idx], "--")
        plt.title(key)
        # plt.legend(["springer", "summer", "fall", "winter"])
        plt.show()

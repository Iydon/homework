# -*- encode: utf-8 -*-
import os
from datetime import datetime
import pandas as pd
from cfgs import CFGS


def split_data(data):
    """Split data into train and test.
    """
    def is_train(date_str):
        date = datetime.strptime(date_str,
            CFGS["TIME"]["PATTERN"])
        return date.day < 20

    index_tr = list(map(is_train,
        data[CFGS["DATA"]["DATECOL"]]))
    index_te = list(map(lambda x: not x, index_tr))
    return data[index_tr], data[index_te]

def split_xy(data):
    """Split data into covariate vector and response.
    """
    igno_index = ["INSCOL", "DATECOL"]
    igno_index = [CFGS["DATA"][i] for i in igno_index]
    resp_index = ["CASCOL", "REGCOL", "CNTCOL"]
    resp_index = [CFGS["DATA"][i] for i in resp_index]
    data_ = data.drop(igno_index, axis=1)
    return data_.drop(resp_index,axis=1), data_[resp_index]




day  = pd.read_csv(
    os.path.join(
        CFGS["DATA"]["DIR"],CFGS["DATA"]["DAY"]),
    encoding=CFGS["IO"]["ENCODE"])
day_train,day_test = split_data(day)
day_train = split_xy(day_train)
day_test  = split_xy(day_test)

hour = pd.read_csv(
    os.path.join(
        CFGS["DATA"]["DIR"],CFGS["DATA"]["HOUR"]),
    encoding=CFGS["IO"]["ENCODE"])
hour_train,hour_test = split_data(hour)
hour_train = split_xy(hour_train)
hour_test  = split_xy(hour_test)

time_index = eval(CFGS["DATA"]["TIMECOL"])
time_train = [hour_train[0][time_index], hour_train[-1]]
time_test  = [hour_test[0][time_index], hour_test[-1]]

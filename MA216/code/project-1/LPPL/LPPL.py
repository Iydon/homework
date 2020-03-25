import matlab
import matlab.engine

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime
from pandas_datareader.data import get_data_yahoo


# MATLAB
if "eng" not in locals():
    eng = matlab.engine.start_matlab()


# Data Maintain
choice = ["000001.SS", "^DJI", "^GSPC"]
ticket = choice[0]
start,end = datetime(2017,4,1),datetime(2018,4,1)
if "Data" not in locals():
    Data = get_data_yahoo(ticket, start=start, end=end)
Close = Data.Close.copy()
N = Data.Close.size
n = int(0.5*N)

# Pre-processing
Times  = list(range(1,N+1))
Times  = matlab.double(Times)
Prices = Data.Close.tolist()
Prices = matlab.double(Prices)
X0     = matlab.double([N+200]) 

# MATLAB Plot
Para   = eng.LPPL(Times[:n], Prices[:n], X0)
eng.title(ticket)

# Python Plot
Times   = np.array(Times)[0]
Prices  = np.array(Prices)[0]

Predict = lambda t: np.exp(
              Para["A"] + Para["B"]*(Para["tc"]-t)**Para["m"] + \
              Para["C1"]*(Para["tc"]-t)**Para["m"]*np.cos(Para["omega"]*np.log(Para["tc"]-t)) + \
              Para["C2"]*(Para["tc"]-t)**Para["m"]*np.sin(Para["omega"]*np.log(Para["tc"]-t))
          )

plt.plot(Times, Predict(Times));
plt.plot(Times, Close);
plt.plot(Times[:n], Prices[:n], "--");
plt.legend(["Path of LPPL", "Real price", "Data used for modeling"]);
plt.xlabel("Number of Days from %s"%start);
plt.ylabel("The Price of %s"%ticket);
plt.show()



# Debug
debug = False

if debug:
    while True:
        ___ = input(">>> ")
        if ___.rstrip()[-1]==":":
            while True:
                ____ = input("... ")
                if ____:
                    ___ += "\n" + ____
                else:
                    try:
                        print(___)
                        exec(___)
                    except Exception as _____:
                        print(_____)
                    break
        elif ___=="exit":
            break
        else:
            try:
                exec(___)
            except Exception as _____:
                print(_____)

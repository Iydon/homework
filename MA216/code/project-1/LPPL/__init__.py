from datetime import datetime
from random import choice
from warnings import filterwarnings

import matplotlib.pyplot as plt
import numpy as np

import matlab
import matlab.engine


eng = matlab.engine.start_matlab()
eng.addpath(eng.genpath(__package__));
filterwarnings("ignore")  # ignore warnings


class Model:
	def __init__(self, source, code, start, end, tt_ratio, eo_ratio):
		'''
		Argument
		=======
			source: Callable, `tushare.get_hist_data` or \
				`pandas_datareader.data.get_data_yahoo`
			code: str
			start: str
			end: str
			tt_ratio: float, ratio of train and test data
			et_ratio: float, ratio of extended and original time
		'''
		# pre-process
		self._code = code
		self._data = source(code, start=start, end=end)
		self._close = self._getattr(self._data, 'close')
		self._time = self._data.index
		self._size = self._close.size
		self._train_size = int(tt_ratio * self._size)
		self._extend_size = int(eo_ratio * self._size)

		self._matlab_time = matlab.double(
			list(range(1, self._size+1)))
		self._matlab_close = matlab.double(
			self._close.to_list())
		self.matlab_init_value = matlab.double(
			[choice(self._close)])
		# MATLAB interface
		self._parameters = eng.LPPL(self._matlab_time[:self._train_size],
			self._matlab_close[:self._train_size], self.matlab_init_value)

	def __repr__(self):
		'''Return `repr(self)`.
		'''
		return '<LPPL Model @ {}>'.format(hash(self))

	def predict(self, t):
		'''Prediction.

		Argument
		=======
			t: float or numpy.array
		'''
		p = self._parameters
		delta = p['tc'] - t
		delta_p = delta ** p['m']
		return np.exp(
              p['A'] + p['B']*delta_p + \
              p['C1']*delta_p*np.cos(p['omega']*np.log(delta)) + \
              p['C2']*delta_p*np.sin(p['omega']*np.log(delta))
          )

	def plot(self, *args, **kwargs):
		'''Plot self.
		'''
		prefix = 'plot_'
		for func in dir(self):
			if func.startswith(prefix):
				getattr(self, func)(*args, **kwargs)

	def plot_origin(self, file_name=''):
		'''Plot original figure.
		'''
		plt.plot(self._time, self._close)
		plt.grid()
		plt.title('Original Data')
		plt.xlabel('Date')
		plt.ylabel(f'Price of {self._code}')
		if file_name:
			plt.savefig(file_name)
		else:
			plt.show()

	def plot_predict(self, file_name=''):
		'''Plot the prediction.
		'''
		# pre-process
		time = np.arange(self._extend_size)
		# plot
		plt.plot(time, self.predict(time))
		plt.plot(time[:self._size], self._close)
		plt.plot(time[:self._train_size], self._close[:self._train_size])
		plt.title('Prediction by LPPL Model')
		plt.legend(["Path of LPPL", "Real price", "Data used for modeling"]);
		plt.grid()
		plt.xlabel(f'Number of Trading Days from {self._time[0]}')
		plt.ylabel(f'Price of {self._code}')
		if file_name:
			plt.savefig(file_name)
		else:
			plt.show()

	def _getattr(self, key, attr):
		if hasattr(key, attr.lower()):
			return getattr(key, attr.lower())
		elif hasattr(key, attr.capitalize()):
			return getattr(key, attr.capitalize())
		raise AttributeError

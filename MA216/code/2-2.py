# -*- encode: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from random import randint


class _Option:
	def __init__(self, E, volume=1, hold=True):
		'''
		Argument
		=======
			E: int or float, exercise price
			volume: int
			hold: bool
		'''
		self.E = E
		self.volume = volume
		self.hold = hold
		self._type = type(self)

	def __repr__(self):
		name = self._type.__name__
		sign = '+' if self.hold else '-'
		value = self.E
		return f'<{name}({sign}{value})>'

	def __mul__(self, value):
		assert isinstance(value, int), 'Argument `value` must be int.'

		if value < 0:
			return self._type(self.E, abs(value)*self.volume, not self.hold)
		return self._type(self.E, value*self.volume, self.hold)

	def __rmul__(self, value):
		return self.__mul__(value)

	def __neg__(self):
		return self._type(self.E, self.volume, not self.hold)

	def value_at(self, S_T):
		'''
		Argument
		=======
			S_T: numpy.ndarray
		'''
		if __debug__:
			assert isinstance(S_T, np.ndarray), 'Type of `S_T` is wrong.'
		return self.value_at__(S_T)
	def value_at__(self, S_T):
		raise NotImplementedError(type(self).__name__)

	def payoff_at(self, S_T):
		'''
		Argument
		=======
			S_T: numpy.ndarray
		'''
		if __debug__:
			assert isinstance(S_T, np.ndarray), 'Type of `S_T` is wrong.'
		return self.payoff_at__(S_T)
	def payoff_at__(self, S_T):
		raise NotImplementedError(type(self).__name__)

		
class CallOption(_Option):
	def value_at__(self, S_T):
		if self.hold:
			return self.volume * (S_T-self.E).clip(min=0)
		else:
			return self.volume * (self.E - (S_T-self.E).clip(min=0))

	def payoff_at__(self, S_T):
		if self.hold:
			return self.volume * (S_T-self.E).clip(min=0)
		else:
			return - self.volume * (S_T-self.E).clip(min=0)


class PutOption(_Option):
	def value_at__(self, S_T):
		if self.hold:
			return self.volume * (self.E-S_T).clip(min=0)
		else:
			return self.volume * (self.E - (self.E-S_T).clip(min=0))

	def payoff_at__(self, S_T):
		if self.hold:
			return self.volume * (self.E-S_T).clip(min=0)
		else:
			return - self.volume * (self.E-S_T).clip(min=0)


def Option(E, type_='call', volume=1, hold=True):
	'''Return an option.
	Argument
	=======
		type_: str, type_ in {'call', 'put'}
	'''
	if type_.lower() == 'call':
		return CallOption(E, volume, hold)
	elif type_.lower() == 'put':
		return PutOption(E, volume, hold)
	else:
		raise TypeError(f'Unrecognized type: {type_}')


class Options:
	def __init__(self, *options):
		if __debug__:
			for option in options:
				assert isinstance(option, (CallOption, PutOption))

		self.options = options

	def __repr__(self):
		return '<Options ({})>'.format(len(self.options))

	def plot(self, S_T, type_='value', figname=''):
		'''plot the corresponding payoff diagram

		Argument
		=======
			S_T: np.ndarray
			type_: str, type_ in {'value', 'payoff'}
			figname: str
		'''
		if type_.lower() == 'value':
			values = [option.value_at(S_T) for option in self.options]
			yaxis = 'Value at Expiry'
			title = yaxis + ' Diagram'
		elif type_.lower() == 'payoff':
			values = [option.payoff_at(S_T) for option in self.options]
			yaxis = 'Payoff'
			title = yaxis + ' Diagram'
		else:
			raise TypeError(f'Unrecognized type: {type_}')
		legend = [None]*len(self.options)

		fig = plt.figure()
		ax1 = fig.add_subplot(211)
		for i, value in enumerate(values):
			ax1.plot(S_T, value, ':')
			legend[i] = repr(self.options[i])
		ax1.legend(legend)

		ax2 = fig.add_subplot(212)
		ax2.plot(S_T, sum(values))

		ax1.set_title(title)
		ax1.set_xlabel('$S_T$')
		ax2.set_xlabel('$S_T$')
		ax1.set_ylabel(yaxis)
		ax2.set_ylabel(yaxis)
		ax1.grid()
		ax2.grid()
		plt.savefig(figname) if figname else plt.show()


if __name__ == '__main__':
	# variable
	number = 3
	prices = 1, 9
	figname = '../figures/2019-09-27-payoff-diagram-2.png'
	# code
	options = [None] * number
	for ith in range(number):
		E = randint(*prices)
		type_ = 'call' if randint(0, 1) else 'put'
		hold = randint(0, 1)
		options[ith] = Option(E, type_=type_, hold=hold)

	options = Options(*options)
	S_T = np.linspace(0, sum(prices), 100)
	options.plot(S_T, 'payoff', figname)

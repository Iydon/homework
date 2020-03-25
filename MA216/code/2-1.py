# -*- encode: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def question_1(E1, E3, E2=0, number=0, plot=False, figname=''):
	'''Question 1
	Hold two European call option with E1 and E2
	Write two calls with E2
	'''
	# declare variable
	E2 = E2 or (E1+E3)/2
	m, M = 0, E1+E3
	number = number or 100*M # default precision: ￥0.01
	ST = np.linspace(m, M, number)

	# calculate the value at expiry
	value_hold  = (ST-E1).clip(min=0) + (ST-E3).clip(min=0)
	value_write = - (ST-E2).clip(min=0)
	value = value_hold + 2*value_write

	# plot the corresponding payoff diagram
	if plot:
		plt.plot(ST, value)
		plt.xlabel('$S_T$')
		plt.ylabel('Payoff')
		plt.title('The Corresponding Payoff Diagram')
		plt.grid()
		plt.savefig(figname) if figname else plt.show()

	# return value
	return value


if __name__ == '__main__':
	E1, E3 = 2, 4
	figname = '../figures/2019-09-27-payoff-diagram.png'
	value = question_1(E1, E3, plot=True, figname=figname)

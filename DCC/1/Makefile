# example: https://github.com/jbornschein/mpi4py-examples
NUM = 4
CMD = mpirun -np $(NUM) --use-hwthread-cpus python

all:
	# NotImplementedError

test:
	$(CMD) test.py

bench:
	$(CMD) bench.py

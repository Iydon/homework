# example: https://github.com/jbornschein/mpi4py-examples
NUM = 4
CMD = mpirun -np $(NUM) --use-hwthread-cpus python
MAIN = main.py

all:
	$(CMD) $(MAIN)

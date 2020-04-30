PYTHON = python3
# PYTHON = pypy3

all:
	$(PYTHON) setup.py build_ext
	cp -n build/*/model.* ./
	rm model.c model.o

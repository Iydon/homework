PYTHON = python3
# PYTHON = pypy3

all:
	$(PYTHON) setup.py build_ext
	cp -n build/lib.linux-x86_64-3.*/model.*.so ./
	rm model.c

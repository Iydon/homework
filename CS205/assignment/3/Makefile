DIRECTORY = blas
FILENAME = main


test:
	g++ $(FILENAME).cpp -O3 -fconcepts-ts \
		-I $(DIRECTORY)/include \
		-L $(DIRECTORY)/lib \
		-l openblas \
		-fopenmp \
		-o $(FILENAME)

clear:
	rm --force *.exe

openblas:
	git clone https://github.com/xianyi/OpenBLAS
	cd OpenBLAS
	make
	make install PREFIX=../$(DIRECTORY)

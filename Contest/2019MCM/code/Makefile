all:
	cython3 utils/plot_utils.pyx
	g++ -o main main.cpp -std=c++11 -O -I /usr/include/python3.5/ -l python3.5m
clean:
	rm main

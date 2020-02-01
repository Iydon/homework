tex:
	touch wordcount && rm wordcount
	latexmk -xelatex -shell-escape main

show:
	qpdfview main.pdf

clean:
	latexmk -c

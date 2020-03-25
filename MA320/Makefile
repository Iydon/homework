help:
	# t --- tex
	# d --- docx
	# s --- show
	# e --- edit
	# c --- clean
h: help

tex:
	latexmk -xelatex main
t: tex

docx:
	python sections/*.py
	mv *.docx doc
d: docx

show:
	qpdfview main.pdf
s: show

edit:
	subl3 ./
e: edit

clean:
	latexmk -c
c: clean

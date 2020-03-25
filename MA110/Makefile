MAIN = main
PASSWORD = SUSTech
OUTPUT = MA110-11711217-IydonLiang

tex:
	@latexmk -xelatex -shell-escape $(MAIN)

encrypt:
	@qpdf $(MAIN).pdf --encrypt $(PASSWORD) $(PASSWORD) 256 -- $(OUTPUT).pdf

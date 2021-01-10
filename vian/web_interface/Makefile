# https://www.microsoft.com/en-us/download/details.aspx?id=48145
OUTPUT = main.dist


.PHONY: all
all:
	# compile
	nuitka.bat \
		--standalone --recurse-all --show-progress --show-memory --plugin-enable=pylint-warnings \
		--windows-icon-from-ico="static\favicon.ico" --output-dir="$(OUTPUT)" \
		main.py
	# necessary files
	cp config.json $(OUTPUT)
	cp -r api $(OUTPUT)
	cp -r templates $(OUTPUT)
	cp -r static $(OUTPUT)
	cp -r cache $(OUTPUT)
	# demo files
	cp main.py models.py standalone.py Pipfile Pipfile.lock Makefile $(OUTPUT)

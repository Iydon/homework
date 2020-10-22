FILENAME = main
TARGETNAME = math
DEMONAME = demo


compile:
	g++ -O3 -std=c++17 $(FILENAME).cpp -o $(TARGETNAME)

demo:
	./$(TARGETNAME) $(DEMONAME).math

compare:
	@echo "=== Math ==="
	./$(TARGETNAME) $(DEMONAME).math
	@echo

	@echo "=== C++ ==="
	g++ $(DEMONAME).cpp -o _ && ./_ $(DEMONAME).math
	@echo

	@echo "=== Python ==="
	python $(DEMONAME).py

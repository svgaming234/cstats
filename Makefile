.PHONY: build clean

build:
	python3 -m PyInstaller --onefile cstats.py

clean:
	rm -rf build/ dist/ cstats.spec


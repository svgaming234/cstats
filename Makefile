.PHONY: build clean

build:
	python -m PyInstaller --onefile cstats.py

clean:
	rm -rf build/ dist/ cstats.spec


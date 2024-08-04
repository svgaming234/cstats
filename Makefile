.PHONY: build clean install_deps

build:
	pyinstaller --onefile cstats.py

clean:
	rm -rf build/ dist/ cstats.spec

install_deps:
	python -m pip install requests pyinstaller

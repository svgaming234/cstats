build:
	pyinstaller --onefile cstats.py

clean:
	rm -r build/ dist/ cstats.spec

install_deps:
	python -m pip install colorama requests pyinstaller
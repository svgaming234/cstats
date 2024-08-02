build:
	pyinstaller --onefile cstats.py

clean:
	rm -r build/ dist/ cstats.spec

install_pyinstaller:
	python -m pip install -U pyinstaller
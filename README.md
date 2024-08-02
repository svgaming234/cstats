# cstats

Unofficial command line based j-stats.xyz alternative for RetroMC  

## Running the program (recommended way)

### Windows
Go to the "Releases" option, and grab the EXE file of the latest release. You can also compile the program yourself, or run the python file directly.

### Linux
Go to the “Releases” option, and grab the latest Linux binary. You can also run the Python file directly, or compile the program yourself.

### Other
Install Python and run the file directly.

## Running the program directly
First, install Python. Afterwards, install colorama and requests by running this in the console:
```
python -m pip install colorama requests
```
The command may vary by platform. Afterwards, you can just run the Python file.
```
python cstats.py
```

## Compiling
First, install Python. Afterwards, install colorama, requests and pyinstaller by running this in the console:
```
python -m pip install colorama requests pyinstaller
```
Afterwards you can run `make_windows.bat` on Windows or the Makefile (`make build`) on Linux included in the cstats repository to compile it. The executable will be located in the `dist` folder of the repository.


## Credits

Based on a player list Python script created by Noggisoggi  
API by JohnyMuffin  
zavdav for telling me about the `getUser` api on `statistics.retromc.org` and for testing

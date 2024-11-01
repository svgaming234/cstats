# cstats

Unofficial command line based j-stats.xyz alternative for RetroMC  

## Running the program (recommended way)

### Windows

Go to the "Releases" option, and grab the EXE file of the latest release. You can also compile the program yourself, or run the python file directly.

### Linux

Go to the “Releases” option, and grab the latest Linux binary. You can also run the Python file directly, or compile the program yourself. 

If you are on Arch Linux, you can also use the [AUR package](https://aur.archlinux.org/packages/cstats). You should be able to install it with your favorite AUR helper.

### Other

Install Python and run the file directly.

## Running the program directly

First, install Python. Afterwards, install colorama and requests by running this in the console (if you are on a platform other than Windows, you can remove colorama from the list):

```sh
python -m pip install colorama requests
```

The command may vary by platform. Afterwards, you can just run the Python file.

```sh
python cstats.py
```

## Compiling

First, install Python. Afterwards, install colorama, requests and pyinstaller by running this in the console (if you are on a platform other than Windows, you can remove colorama from the list):

```sh
python -m pip install colorama requests pyinstaller
```

Afterwards you can run `make_windows.bat` on Windows or the Makefile (`make build`) on Linux included in the cstats repository to compile it. The executable will be located in the `dist` folder of the repository.

## Credits

SvGaming - Project lead
Noggisoggi - Creator of player list script which cstats is based on  
JohnyMuffin - Creator of APIs utilized by cstats  
zavdav - Lead tester, told me about the getUser API, gave ideas for improving the ping feature
Jaoheah - Switched the options around on the menu


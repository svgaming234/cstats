# cstats

Unofficial command line based statistics program for RetroMC and BetaMC  

## Running the program (recommended way)

### Windows

Go to the "Releases" option, and grab the EXE file of the latest release. Keep in mind the file will likely be falsely detected as malware due to pyinstaller being frequently detected as a false positive. If you would like to avoid this, you can run the python file directly as described below.

### Linux

#### Arch based distributions (Arch, Artix, EndavourOS, CachyOS...)

You can install the [AUR package](https://aur.archlinux.org/packages/cstats) with your favorite AUR helper or manually with `makepkg`.

For example using `yay`:

```sh
yay -S cstats
```

#### Debian-based distributions (Debian, Devuan, Ubuntu, Mint, PopOS...)

You can install the .deb file provided with the "Releases" option in this repository.

#### Other Linux distributions (glibc-based)

Go to the “Releases” option, and grab the latest Linux binary.

After setting it as executable, it should just run if glibc of a new enough version is provided (most Linux distributions are glibc based).

For example:

```sh
chmod +x cstats-0.10.0-linux-glibc
./cstats-0.10.0-linux-glibc
```

If your system is not using glibc or is using an older version, you can run the file directly with Python or compile your own binary using pyinstaller as described below.

### Other

Install Python and run the file directly as described below.

## Running the program directly

First, install Python. Afterwards, install colorama and requests using pip (colorama is only required for Windows, otherwise it can be removed):

```sh
python3 -m pip install colorama requests
```

**NOTE: Most Linux distributions have Python packages provided as part of their package manager, which should be used instead (the package for `requests` is usually called `python-requests` or `python3-requests`.**

The command may vary by platform. Afterwards, you can just run the Python file.

```sh
python3 cstats.py
```

## Compiling

First follow the steps to run the program directly as described earlier. Afterwards, install pyinstaller in order to build the package:

Using pip:

```sh
python3 -m pip install pyinstaller
```

**NOTE: Most Linux distributions have Python packages provided as part of their package manager, which should be used instead (the package for `pyinstaller` is usually called `pyinstaller` or `python3-pyinstaller`.**

Afterwards you can run `make_windows.bat` on Windows or the Makefile (`make build`) on Linux included in the cstats repository to compile it (located in `builds/pyinstaller/`). The executable will be located in the `dist` folder inside the directory.

## Contributions

Pull requests to cstats are welcome as long as no AI written or assisted content is submitted.

## Credits

SvGaming - Project lead

Noggisoggi - Creator of player list script which cstats is based on  

JohnyMuffin - Creator of RetroMC and Legacy Tracker related APIs utilized by cstats  

zavdav - Tester, told me about the getUser API, gave ideas for improving the ping feature, creator of BetaMC APIs used by cstats

Pilzhut5 - contribution of .deb build scripts and .desktop file

Jaoheah - Switched the options around on the menu

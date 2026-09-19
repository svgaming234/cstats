#!/bin/dash
# Pilzhut5's debian build script for cstats

set -eu

echo "checking dependencies"
for dep in gzip dh dpkg-buildpackage
do
    if command -v "$dep" >/dev/null 2>&1
    then
        echo "FOUND: $dep"
    else
        echo "ERROR: $dep appears to be missing!"
        false
    fi
done

read -p "did you make sure that debian/changelog is up-to-date? (y/n)" ChangelogConfirmation

if [ "$ChangelogConfirmation" = "y" ]
then
    mv Makefile Destroyfile
    mkdir temp
    cp cstats.py temp/cstats
    cp cstats128.png temp/cstats.png
    chmod +x debian/rules temp/cstats
    dpkg-buildpackage --no-sign --build=binary || true
    chmod -x debian/rules
    mv Destroyfile Makefile
    rm -rv temp/ debian/cstats/ debian/files debian/cstats.substvars debian/debhelper-build-stamp
    echo
    echo "DONE! take a look at the package in ../"
else
    echo "ok, aborted package build"
fi

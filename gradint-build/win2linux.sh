#!/bin/bash

# Convert a Windows gradint.exe or gradint-bundle.exe
# (optionally with bundled samples, partials etc) into
# a GNU/Linux installation of Gradint.  Use this to
# support both Windows and GNU/Linux from one bundle.

# (c) 2013,2021 Silas S. Brown.  License: GPL v3 (as Gradint)

# This script can be placed on a USB stick or whatever, in
# the same directory as:

# (1) gradint.exe or gradint-bundle.exe

# (2) 7za binary (for correct CPU type and libraries), if
# 7za is not installed on the system,

# (3) espeak binary (ditto)

# (4) any *.deb files to install with dpkg, e.g. python-tk
# and its dependencies (e.g. blt tk-8.5)
# (these will be installed with --force-depends, in case
# you're doing an offline install and can manage without
# having the most up-to-date dependencies - do this at
# your own risk)

# You can also put the 7za, espeak and deb files into a
# bin/ subdirectory.

export DoneDeb=0
if ! test "$(echo *.deb)" == "*.deb"; then
  echo "Installing *.deb (with --force-depends)"
  sudo dpkg --force-depends -i *.deb
  export DoneDeb=1
elif ! test "$(echo bin/*.deb)" == "bin/*.deb"; then
  echo "Installing bin/*.deb (with --force-depends)"
  sudo dpkg --force-depends -i bin/*.deb
  export DoneDeb=1
fi
# TODO: if got internet, sudo apt-get update ; sudo apt-get -f install
if test -f espeak || test -f bin/espeak; then
  echo "Copying espeak binary to /usr/local/bin"
  if test -f espeak; then sudo cp espeak /usr/local/bin/
  else sudo cp bin/espeak /usr/local/bin/; fi
elif ! which espeak 2>/dev/null >/dev/null && ! which speak 2>/dev/null >/dev/null; then
  echo "Warning: no espeak binary found on system, and none to install" # TODO: try to apt-get it?  but might not have an Internet connection
  echo -n "Press Enter: " ; read
fi
mkdir -p "$HOME/gradint0"
if test -e gradint-bundle.exe; then
  PATH="$PATH:.:./bin" 7za "-o$HOME/gradint0" x gradint-bundle.exe || exit 1
else PATH="$PATH:.:./bin" 7za "-o$HOME/gradint0" x gradint.exe || exit 1; fi
cd "$HOME/gradint0" || exit 1
mv gradint .. || exit 1
cd .. && rm -rf gradint0
cd gradint || exit 1
unzip library.zip gradint.py || exit 1
rm -rf tcl library.zip ./*.exe ./*.pyd ./*.dll
if python -c 'import tkinter'; then
 if test -e ~/Desktop && ! test -e ~/Desktop/Gradint; then
  echo "Creating symlink on Desktop"
  ln -s "$(pwd)/gradint.py" ~/Desktop/Gradint
  # TODO: what about the menus of various front-ends? (might need to make .desktop files in .local/share/applications or something)
 else echo "Not creating symlink on desktop" # TODO: cater for more possibilities
 fi
else echo "Warning: no tkinter on this system; gradint will be command-line only" ; echo -n "Press Enter: " ; read # TODO: if internet, try sudo apt-get install python-tk
fi
echo "Copying espeak-data to /usr/share/"
sudo cp -r espeak/espeak-data /usr/share/ && rm -rf espeak
echo "win2linux.sh finished"
if test $DoneDeb == 1; then
  echo
  echo "WARNING: Have installed packages with dpkg --force-depends."
  echo "If you're connected to the Internet, you might now wish to do:"
  echo "  sudo apt-get update ; sudo apt-get -f install"
  echo "or if the machine will later be connected to the"
  echo "Internet without you, you might wish to do:"
  echo "  (echo apt-get update; echo apt-get -yf install) | sudo at -M midnight"
fi

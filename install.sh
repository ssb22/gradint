#!/bin/bash

# Installing Gradint on GNU/Linux systems
# ---------------------------------------

# Gradint does not need to be installed, it can
# just run from the current directory.

# If you do want to make a system-wide installation
# (for example if you want to make a package for a
# GNU/Linux distribution), I suggest running as root
# the commands below.

# For a distribution you might also have to write
# man pages and tidy up the help text etc.

# Depends: python + a sound player (e.g. alsa-utils)
# Recommends: python-tk python-tksnack sox libsox-fmt-all madplay

# ---------------------------------------

set -e
PREFIX=/usr/local # or /usr
if which python >/dev/null 2>/dev/null; then PYTHON=python; else PYTHON=python3; fi

mkdir -p "$PREFIX/share/gradint"
mv gradint.py "$PREFIX/share/gradint/"
cd samples/utils
for F in *.py *.sh; do
  DestFile="$PREFIX/bin/gradint-$(echo $F|sed -e 's/\..*//')"
  mv "$F" "$DestFile"
  chmod +x "$DestFile"
done
cd ../.. ; rm -rf samples/utils
tar -zcf "$PREFIX/share/gradint/new-user.tgz" \
  advanced.txt settings.txt vocab.txt samples

cat > "$PREFIX/bin/gradint" <<'EOF'
#!/bin/bash
if ! [ -e "$HOME/gradint" ]; then
  echo -n "Unpacking new user Gradint configuration... "
  mkdir "$HOME/gradint"
  cd "$HOME/gradint"
EOF
echo "  tar -zxf \"$PREFIX/share/gradint/new-user.tgz\"" >> "$PREFIX/bin/gradint"
cat >> "$PREFIX/bin/gradint" <<'EOF'
  echo "done."
fi
cd "$HOME/gradint"
EOF
echo "$PYTHON \"$PREFIX/share/gradint/gradint.py\" "'$@' >> "$PREFIX/bin/gradint"
chmod +x "$PREFIX/bin/gradint"

mkdir -p "$PREFIX/share/applications"
cat > "$PREFIX/share/applications/gradint.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Gradint
Comment=Graduated-interval recall
Exec=$PREFIX/bin/gradint
Categories=Education;Languages
EOF

echo; echo "Installation complete."
echo "To uninstall: sudo rm -rf \"$PREFIX/bin/gradint\" \"$PREFIX/share/gradint\" \"$PREFIX/share/applications/gradint.desktop\" "

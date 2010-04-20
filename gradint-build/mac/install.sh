#!/bin/bash
# Do NOT modify this stub without changing the bs= count.
if test -d "$HOME/Desktop/Gradint.app"; then export A="Gradint 2.app"; else export A=Gradint.app; fi
dd if="$0" of="$HOME/Desktop/gradint.tbz" bs=393 skip=1 && cd "$HOME/Desktop" || exit 1
echo "Please wait..."
open gradint.tbz
sleep 1
while ! test -e "$A/vocab.txt"; do sleep 1; done
echo "Opening $A..."
open "$A" ; exit

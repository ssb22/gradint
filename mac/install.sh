#!/bin/bash
# Do NOT modify this stub without changing the bs= count.
if [ -d "$HOME/Desktop/Gradint.app" ]; then A="Gradint 2.app"; else A=Gradint.app; fi
dd if="$0" of="$HOME/Desktop/gradint.tbz" bs=377 skip=1 && cd "$HOME/Desktop" || exit 1
echo "Please wait..."
open gradint.tbz
sleep 1
while ! [ -e "$A/vocab.txt" ]; do sleep 1; done
echo "Opening $A..."
open "$A" ; exit

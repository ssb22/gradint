#!/bin/bash
# Do NOT modify this stub without changing the bs= count.
dd if="$0" of="$HOME/Desktop/gradint.tbz" bs=359 skip=1 && cd "$HOME/Desktop" && open gradint.tbz
sleep 1
while ! (if test -d "Gradint 2.app"; then test -e "Gradint 2.app/vocab.txt"; else test -e "Gradint.app/vocab.txt"; fi); do sleep 1; done
open "Gradint 2.app" || open Gradint.app
exit

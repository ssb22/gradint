#!/usr/bin/env python
# (should work in both Python 2 and Python 3)

# Simple sound-playing server
# Silas S. Brown - public domain - no warranty

# connect to port 8124 (assumes behind firewall)
# and each connection can send WAV or MP3 data

# so gradint advanced.txt can do
# wavPlayer = mp3Player = "nc HostName 8124 -q 0 <"

import socket, os
os.environ["PATH"] += ":/usr/local/bin"
s=socket.socket()
s.bind(('',8124))
s.listen(5)
if type(b"")==type(""): S=lambda x:x # Python 2
else: S=lambda x:x.decode("latin1") # Python 3
while True:
    c,a = s.accept()
    d = S(c.recv(4))
    if d=='RIFF': # WAV
        player = "play - 2>/dev/null"
    elif d=='STOP':
        c.close()
        while not d=='START':
            c,a = s.accept()
            d = S(c.recv(5)) ; c.close()
        continue
    else: player = "mpg123 - 2>/dev/null" # MP3
    player = os.popen(player,"w")
    d = d.encode("latin1") # no-op on Python 2
    while d:
        try:
            try: player.write(d)
            except TypeError: # Python 3
                player.buffer.write(d)
        except IOError: break # it was probably killed
        d = c.recv(4096)
    try:
        c.close() ; player.close()
    except: pass

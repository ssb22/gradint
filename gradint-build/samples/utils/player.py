#!/usr/bin/env python
# (should work in both Python 2 and Python 3)

# Simple sound-playing server v1.2
# Silas S. Brown - public domain - no warranty

# connect to port 8124 (assumes behind firewall)
# and each connection can send WAV or MP3 data

# so gradint advanced.txt can do
# wavPlayer = mp3Player = "nc HostName 8124 -q 0 <"

import socket, os, sys, os.path
for a in sys.argv:
  if a.startswith("--rpi-bluetooth-eth="):
    # tested on Raspberry Pi 400 with Raspbian 11
    eth=a.split('=')[1]
    os.system("if ! pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then while true; do bluetoothctl --timeout 1 disconnect "+eth+" ; sleep 5 ; while ! bluetoothctl --timeout 5 connect "+eth+" | egrep 'Connection.successful|Connected'; do sleep 5; done ; Got=0; for Try in 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z; do if pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then Got=1; break; fi; sleep 1; done; if [ $Got = 1 ] ; then break; fi; done; fi; pacmd set-default-sink bluez_sink."+eth.replace(":","_")+".a2dp_sink; play /usr/share/scratch/Media/Sounds/Animal/Dog1.wav; echo Ready")
  elif a.startswith("--rpi-bluetooth-setup-eth="):
    eth=a.split('=')[1]
    os.system('mkdir -p /home/pi/.config/lxsession/LXDE-pi && cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/ && echo python '+os.path.join(os.getcwd(),sys.argv[0])+' --rpi-bluetooth-eth='+eth+' >> /home/pi/.config/lxsession/LXDE-pi/autostart && sudo "usermod -G bluetooth -a pi ; (echo load-module module-switch-on-connect;echo load-module module-bluetooth-policy;echo load-module module-bluetooth-discover) >> /etc/pulse/default.pa ; (echo [General];echo FastConnectable = true) >> /etc/bluetooth/main.conf ; reboot"')

os.environ["PATH"] += ":/usr/local/bin"
s=socket.socket()
s.bind(('',8124))
s.listen(5)
if type(b"")==type(""): S=lambda x:x # Python 2
else: S=lambda x:x.decode("latin1") # Python 3
while True:
    c,a = s.accept()
    c.settimeout(10)
    try: d = S(c.recv(4))
    except: # e.g. timeout, or there was an error reading the file on the remote side and we got 0 bytes
        c.close() ; continue
    if d=='RIFF': # WAV
        player = "play - 2>/dev/null"
    elif d=='STOP':
        c.close()
        while not d=='START':
            c,a = s.accept()
            try: d = S(c.recv(5))
            except: d = ""
            c.close()
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
        try: d = c.recv(4096)
        except: d = ""
    try:
        c.close() ; player.close()
    except: pass

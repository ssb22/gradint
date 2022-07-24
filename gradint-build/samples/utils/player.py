#!/usr/bin/env python
# (should work in both Python 2 and Python 3)

# Simple sound-playing server v1.4
# Silas S. Brown - public domain - no warranty

# connect to port 8124 (assumes behind firewall)
# and each connection can send WAV or MP3 data

# so gradint advanced.txt can do
# wavPlayer = mp3Player = "nc HostName 8124 -q 0 <"
# (most of this script assumes GNU/Linux)

import socket, os, sys, os.path, time
for a in sys.argv:
  if a.startswith("--rpi-bluetooth-eth="):
    # tested on Raspberry Pi 400 with Raspbian 11
    eth=a.split('=')[1]
    os.system("if ! pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then while true; do bluetoothctl --timeout 1 disconnect "+eth+" ; sleep 5 ; while ! bluetoothctl --timeout 5 connect "+eth+" | egrep 'Connection.successful|Connected'; do sleep 5; done ; Got=0; for Try in 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z; do if pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then Got=1; break; fi; sleep 1; done; if [ $Got = 1 ] ; then break; fi; done; fi; pacmd set-default-sink bluez_sink."+eth.replace(":","_")+".a2dp_sink; play /usr/share/scratch/Media/Sounds/Animal/Dog1.wav; echo Ready")
  elif a.startswith("--rpi-bluetooth-setup-eth="):
    eth=a.split('=')[1]
    os.system('mkdir -p /home/pi/.config/lxsession/LXDE-pi && cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/ && echo python '+os.path.join(os.getcwd(),sys.argv[0])+' --rpi-bluetooth-eth='+eth+' >> /home/pi/.config/lxsession/LXDE-pi/autostart && sudo "usermod -G bluetooth -a pi ; (echo load-module module-switch-on-connect;echo load-module module-bluetooth-policy;echo load-module module-bluetooth-discover) >> /etc/pulse/default.pa ; (echo [General];echo FastConnectable = true) >> /etc/bluetooth/main.conf ; reboot"')
  elif a=="--aplay": use_aplay = True # aplay and madplay, for older embedded devices, NOT tested together with --rpi-bluetooth-* above
  elif a.startswith("--delegate="): # --delegate=IP address, will ping that IP and delegate all sound to it when it's up.  E.g. if it has better amplification but it's not always switched on.
    delegate_to_check=a.split('=')[1]

os.environ["PATH"] += ":/usr/local/bin"
try: use_aplay
except: use_aplay = False
try: delegate_to_check
except: delegate_to_check = None
delegate_known_down = 0
s=socket.socket()
s.bind(('',8124))
s.listen(5)
if type(b"")==type(""): S=lambda x:x # Python 2
else: S=lambda x:x.decode("latin1") # Python 3
while True:
    c,(a,port) = s.accept()
    c.settimeout(10)
    try: d = S(c.recv(4))
    except: # e.g. timeout, or there was an error reading the file on the remote side and we got 0 bytes
        c.close() ; continue
    if delegate_to_check and not a==delegate_to_check and delegate_known_down < time.time()-60 and not os.system("ping -c 1 -w 0.5 '"+delegate_to_check+"' >/dev/null 2>/dev/null"): player = "nc -N '"+delegate_to_check+"' 8124"
    elif d=='RIFF': # WAV
        if use_aplay: player = "aplay -q"
        else: player = "play - 2>/dev/null"
    elif d=='STOP':
        c.close()
        while not d=='START':
            c,a = s.accept()
            try: d = S(c.recv(5))
            except: d = ""
            c.close()
        continue
    elif use_aplay: player = "madplay -Q -o wav:- - | aplay -q" # MP3
    else: player = "mpg123 - 2>/dev/null" # MP3 non-aplay
    if delegate_known_down < time.time()-60 and not player.startswith("nc -N "): delegate_known_down = time.time()
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

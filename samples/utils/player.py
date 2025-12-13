#!/usr/bin/env python
# (should work in both Python 2 and Python 3)

# Simple sound-playing server v1.61
# Silas S. Brown - public domain - no warranty

# connect to port 8124 (assumes behind firewall)
# and each connection can send WAV or MP3 data

# so gradint advanced.txt can do
# wavPlayer = mp3Player = "nc HostName 8124 -q 0 <"
# (most of this script assumes GNU/Linux)

import socket, select, os, sys, os.path, time, re
for a in sys.argv[1:]:
  if a.startswith("--rpi-bluetooth-setup"):
    # tested on Raspberry Pi 400 and Raspberry Pi Zero W with OS versions 11 through 13
    # (also tested on Raspberry Pi Zero W with Raspbian 10 Lite with the device already paired: needed to say "scan on", "discovery on", remove + pair in bluetoothctl)
    # Note that the setup command reboots the system.
    # Once set up, send Eth=(bluetooth Ethernet addr) to start.
    # Alternative non-PulseAudio setup: Don't run with --rpi-bluetooth-setup, just install bluez-alsa-utils bluez madplay, systemctl enable and start bluealsa, sudo rfkill unblock bluetooth, pair with bluetoothctl and run with --aplay (will aplay either to local speakers or to Bluetooth if Eth= specified, but clock-chime is always to local speakers).  Caution: some a2dp stacks (including Echo Dot 3) may need device restart if incoming audio is interrupted in this setup; also playback may be slightly glitchy and may finish more slowly.
    os.system(r'if ! grep "$(cat ~/.ssh/*.pub)" ~/.ssh/authorized_keys; then cat ~/.ssh/*.pub >> ~/.ssh/authorized_keys;fi && (echo "[Unit]";echo "Description=Gradint player utility";echo "[Service]";echo "Type=oneshot";echo "ExecStart=bash -c \"while ! ssh localhost true; do sleep 1; done; ssh localhost '+os.path.join(os.getcwd(),sys.argv[0])+r'\"";echo "WorkingDirectory='+os.getcwd()+'";echo User="$(whoami)";echo "[Install]";echo "WantedBy=multi-user.target") > player.service && sudo mv player.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable player && chmod +x '+sys.argv[0]+' && sudo bash -c "apt-get -y install sox mpg123 pulseaudio pulseaudio-module-bluetooth && usermod -G bluetooth -a $USER && (echo load-module module-switch-on-connect;echo load-module module-bluetooth-policy;echo load-module module-bluetooth-discover) >> /etc/pulse/default.pa && (echo [General];echo FastConnectable = true) >> /etc/bluetooth/main.conf && reboot"') # (eee off: improves reliability of gigabit ethernet on RPi400)
  elif a=="--aplay": use_aplay = True # aplay and madplay, for older embedded devices, NOT tested together with --rpi-bluetooth-* above
  elif a.startswith("--delegate="): delegate_to_check=a.split('=')[1] # will ping that IP and delegate all sound to it when it's up.  E.g. if it has better amplification but it's not always switched on.
  elif a.startswith("--chime="): chime_mp3=a.split('=')[1] # if clock bell desired, e.g. echo '$i-14vfff$c48o0l1b- @'|mwr2ly > chime.ly && lilypond chime.ly && timidity -Ow chime.midi && audacity chime.wav (amplify + trim) + mp3-encode (keep default 44100 sample rate so ~38 frames per sec).  Not designed to work with --delegate.  Pi1's 3.5mm o/p doesn't sound very good with this bell.
  else: assert 0, "unknown option "+a

os.environ["PATH"] += ":/usr/local/bin"
try: use_aplay
except: use_aplay = False
try: delegate_to_check
except: delegate_to_check = None
try: chime_mp3
except: chime_mp3 = None
last_chime = last_play = 0
delegate_known_down = 0
s=socket.socket()
s.bind(('',8124))
s.listen(5)
if type(b"")==type(""): S=lambda x:x # Python 2
else: S=lambda x:x.decode("latin1") # Python 3
eth = ""
while True:
    if chime_mp3:
        t = time.time()
        if t > last_chime+60 and t%1800 < 60 and not t<last_play+20:
            last_chime = t ; h,m=time.localtime(t)[3:5]
            if m>1: numChimes = 1
            elif not h%12: numChimes = 12
            else: numChimes = h%12
            if not 7<=h%24<=22: pass # silence the chime at night
            elif use_aplay:
              if numChimes > 1: os.system("(madplay -Q -t 1 -o wav:- '"+chime_mp3+"'"+(";madplay -Q -t 1 -o raw:- '"+chime_mp3+"'")*(numChimes-2)+";madplay -Q -o raw:- '"+chime_mp3+"') | aplay -q")
              else: os.system("madplay -Q -o wav:- '%s' | aplay -q" % chime_mp3)
            elif numChimes > 1: os.system("(mpg123 -w - -n 38 --loop %d '%s' ; mpg123 -s '%s') 2>/dev/null | play -t wav --ignore-length - 2>/dev/null" % (numChimes-1,chime_mp3,chime_mp3))
            else: os.system("mpg123 -q '%s'" % chime_mp3)
        if not select.select([s],[],[],1800-time.time()%1800)[0]: continue
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
    elif d=='QUIT':
        s.close() ; break
    elif d=="Eth=": # Eth=ethernet address to connect via Bluetooth (see --rpi-bluetooth-setup above)
        eth = S(c.recv(17))
        assert re.match("^[A-Fa-f0-9:]+$",eth)
        if use_aplay: os.system("bluetoothctl connect "+eth)
        else: os.system("E="+eth+";if ! pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then while true; do rfkill block bluetooth; rfkill unblock bluetooth; bluetoothctl --timeout 1 power on; bluetoothctl --timeout 1 disconnect | grep Missing >/dev/null||sleep 5;T=5;while ! bluetoothctl --timeout $T connect $E | egrep \"Connection successful|Device $E Connected: yes\"; do sleep 5; T=10;bluetoothctl --timeout 1 devices;echo Retrying $E; done ; Got=0; for Try in 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z; do if pacmd list-sinks | grep "+eth.replace(":","_")+" >/dev/null; then Got=1; break; fi; sleep 1; done; if [ $Got = 1 ] ; then break; fi; done; fi; pacmd set-default-sink bluez_sink."+eth.replace(":","_")+".a2dp_sink") # ; play /usr/share/scratch/Media/Sounds/Animal/Dog1.wav # (not really necessary if using 'close the socket' to signal we're ready)
        c.close() ; continue
    elif d=="Eth0":
      if eth: os.system("bluetoothctl --timeout 1 disconnect "+eth)
      c.close() ; continue
    elif use_aplay: player = "madplay -Q -o wav:- - | aplay -q" # MP3
    else: player = "mpg123 - 2>/dev/null" # MP3 non-aplay
    if delegate_known_down < time.time()-60 and not player.startswith("nc -N "): delegate_known_down = time.time()
    if use_aplay and eth: player=player.replace("-Q","-Q -S -R 48000")+" -B 2000000 -D bluealsa:PROFILE=a2dp,DEV="+eth
    player = os.popen(player,"w")
    if type(d)==type(u""): d = d.encode("latin1")
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
    last_play = time.time()

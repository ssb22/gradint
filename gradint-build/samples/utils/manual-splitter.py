#!/usr/bin/env python

# Like splitter.py, but lets you use Audacity etc to split in non-realtime.
# You must export the segments in order.

# ('mv && increment count' in a loop: ok as long as in same dir so no complicatns w cross-device & still-open)

# python 3+:
try: input
except: input=lambda x:eval(raw_input(x))

fToWatch = raw_input("File to watch for, e.g. recording.wav (must be in /tmp): ")

lang1=lang2=None
while not lang1: lang1=raw_input("Enter first language to be export (e.g. en): ")
interleaved=input("Are two languages interleaved? (1/0): ") # (horrible hack)
if interleaved:
    while not lang2: lang2=raw_input("Enter second language to be export (e.g. zh): ")
else:
    lang2=lang1

import os,time,sys
os.chdir("/tmp")
sys.stdout.write("Press Ctrl-C to stop the script\n")
counter = 0 ; lang = lang1
while 1:
    time.sleep(1)
    if os.system("mv %s %03d_%s.wav 2>/dev/null" % (fToWatch,counter,lang)): continue # nothing there
    if lang==lang2: # important to compare with lang2 FIRST, because maybe lang1==lang2
        lang = lang1
        counter += 1
    else: lang = lang2

#!/usr/bin/env python

import os,commands,sys

def equalise():
    oldDir=os.getcwd()
    for l in os.listdir(oldDir):
        isDir = 0
        try:
            os.chdir(l)
            isDir=1
        except: pass
        if isDir:
            equalise()
            os.chdir(oldDir)
        elif l.endswith("wav"):
            vol = commands.getoutput('sox "%s" t.nul stat' % (l,)).split("\n")[-1].split()[-1]
            os.system('sox -t wav - -t wav __adjusted vol %s < "%s"' % (vol,l))
            os.remove(l) ; os.rename('__adjusted',l)
            try: os.remove('t.nul')
            except: pass

sys.stdout.write("""WARNING - Use this script ONLY if there is a large
perceptual variation in the volume levels.  Works on all
samples in current directory and subdirectories.  Really go
ahead?
Press Ctrl-C to cancel or Enter to continue\n""")
raw_input()
equalise()

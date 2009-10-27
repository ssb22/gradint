#!/usr/bin/env python

# list2cache.py language

# See list-synth.py for what this is.  It puts
# sequentially-numbered files (00_zh.wav,
# 01_zh.wav etc) into the synth cache, as
# directed by cache-list.txt.
# It also appends cache-list.txt to cachelist-done.txt,
# the contents of which is omitted from future runs of list-synth.py

# Run in the same directory as gradint.py with
# all the settings.

underscore = ""
# Set this to "_" to have underscores (_) before all cache
# additions (i.e. to add them in test mode).  Set to "" for
# non-test mode.

import sys,os,time
lang = sys.argv[1:]
if not lang:
    sys.stderr.write("Please run with a language abbreviation on the command line.  See comments at the start of this script for details.\n")
    sys.exit()
lang=lang[0]
sys.argv = []
import gradint
if not gradint.synthCache:
    sys.stderr.write("Error - synthCache is not set in advanced.txt\n") ; sys.exit()
lines = []
for l in filter(lambda x:x,gradint.u8strip(open("cache-list"+gradint.dottxt).read().replace("\r","\n")).split("\n")):
    l=l.strip()
    if l.endswith(","): l=l[:-1]
    lines.append(l)
toMove = []
for i in range(len(lines)):
    for ext in [gradint.dotwav,gradint.dotmp3]:
        for zeros in ["","0","00","000"]:
            fname = zeros+str(i)+"_"+lang+ext
            if gradint.fileExists(fname): toMove.append((fname,underscore+lines[i]+"_"+lang+ext))
sys.stderr.write("Moving %d items to %s\n" % (len(toMove),gradint.synthCache))
count = 0
for tmpfile,dest in toMove:
    try:
        os.rename(tmpfile,gradint.synthCache+os.sep+dest)
    except OSError: # not a valid filename
        while gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+gradint.dotwav) or gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+gradint.dotmp3): count += 1
        os.rename(tmpfile,gradint.synthCache+os.sep+("__file%d" % count)+tmpfile[tmpfile.rfind(gradint.extsep):])
        open(gradint.synthCache+os.sep+gradint.transTbl,"ab").write("__file%d%s %s\n" % (count,tmpfile[tmpfile.rfind(gradint.extsep):],dest))
open("cachelist-done"+gradint.dottxt,"a").write("\n".join(lines)+"\n")

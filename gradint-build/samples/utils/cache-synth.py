#!/usr/bin/env python

# cache-synth.py [--test] language [language ...]

# cache all words that can be synthesized -
# useful if you sometimes need to run gradint on
# a different system that doesn't have one or
# more of the synthesizers installed.  Run in
# the same directory as gradint.py with all the
# settings.

import sys,os,time
langs = sys.argv[1:] ; testMode = False
if langs and langs[0]=='--test':
    langs = langs[1:] ; testMode = True
if not langs:
    sys.stderr.write("Please put a language abbreviation (or a list of them separated by spaces) on the command line.  See comments at the start of this script for details.\n")
    sys.exit()
sys.argv = []
import gradint
if not gradint.synthCache:
    sys.stderr.write("Error - synthCache is not set in advanced.txt\n") ; sys.exit()
gradint.cache_maintenance_mode=1
gradint.soundCollector=1 # (so don't prefer play-on-demand synths)
gradint.__name__='__main__' # (so PttsSynth on Neospeech Lily doesn't pause too much on punctuation)

try: trans = open(gradint.synthCache+os.sep+gradint.transTbl).read().replace("\n"," ")+" "
except: trans = ""
def synth_fileExists(f):
    try:
        open(gradint.synthCache+os.sep+f)
        return 1
    except: return (" "+f+" ") in trans

toMove = []
generating = {}
def maybe_cache(s,directory):
    if not s: return # in case poetry has some 2nd-language only
    if '!synth:' in s and "_" in s: textToSynth, langToSynth = gradint.textof(s),gradint.languageof(s)
    elif s.endswith(gradint.extsep+"txt"): textToSynth, langToSynth = gradint.readText(directory+os.sep+s), gradint.languageof(s,directory==gradint.promptsDirectory)
    else: return
    if not langToSynth in langs: return # we're not caching that language
    if synth_fileExists((textToSynth+"_"+langToSynth+gradint.dotwav).lower()) or synth_fileExists((textToSynth+"_"+langToSynth+gradint.dotmp3).lower()): return # it's already been done
    if synth_fileExists(("__rejected_"+textToSynth+"_"+langToSynth+gradint.dotwav).lower()) or synth_fileExists(("__rejected_"+textToSynth+"_"+langToSynth+gradint.dotmp3).lower()): return # it's been rejected by the GUI
    if (textToSynth.lower(),langToSynth) in generating: return # we're already generating it
    generating[(textToSynth.lower(),langToSynth)]=1
    sys.stderr.write("Generating %s\n" % (textToSynth,))
    toMove.append((gradint.synth_event(langToSynth,textToSynth).getSound(),(textToSynth+"_"+langToSynth+gradint.dotwav).lower()))

for _,s1,s2 in gradint.scanSamples()+gradint.parseSynthVocab(gradint.vocabFile):
    if type(s1)==type([]): [maybe_cache(i,gradint.samplesDirectory) for i in s1]
    else: maybe_cache(s1,gradint.samplesDirectory)
    maybe_cache(s2,gradint.samplesDirectory)
for f in gradint.AvailablePrompts().lsDic.values():
    for f2 in f:
        if f2.endswith("txt"): maybe_cache(f2,gradint.promptsDirectory)
for l in langs: gradint.get_synth_if_possible(l).finish_makefile()
count=0
gradint.soundCollector=0
if toMove: sys.stderr.write("Renaming\n")
else: sys.stderr.write("No additional words need to be synthesized\n")
for tmpfile,dest in toMove:
    oldDest = dest
    try:
        os.rename(tmpfile,gradint.synthCache+os.sep+dest)
    except OSError: # not a valid filename
        while gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+gradint.dotwav) or gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+gradint.dotmp3): count += 1
        os.rename(tmpfile,gradint.synthCache+os.sep+("__file%d" % count)+gradint.dotwav)
        open(gradint.synthCache+os.sep+gradint.transTbl,"ab").write("__file%d%s %s\n" % (count,gradint.dotwav,dest))
        dest = "__file%d%s" % (count,gradint.dotwav)
    if testMode:
        sys.stderr.write(oldDest+"\n")
        e=gradint.SampleEvent(gradint.synthCache+os.sep+dest)
        t=time.time() ; e.play()
        while time.time() < t+e.length: time.sleep(1) # in case play() is asynchronous
sys.stderr.write("All done\n")

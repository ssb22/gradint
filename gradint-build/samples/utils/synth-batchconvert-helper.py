#!/usr/bin/env python

# Script to assist with using TextAloud or similar program
# that can batch-synthesize a collection of text files
# provided it is run interactively to start the batch conversion.

# This script will generate appropriate *.txt files for the
# words in vocab.txt etc, and rename the resulting *.mp3 or *.wav
# files into the synth cache.

# Should be useful if you are on Linux and want to run a
# non-English speech synth in the Windows Emulator (since
# ptts can have trouble, but tools like TextAloud still work).
# Note: This script currently assumes that the filesystem
# can take all the characters used in the strings; that should
# probably be changed on Windows etc.  However, if you're on
# Windows and are using a Windows-based synth then you shouldn't
# need this script; use cache-synth.py instead (more fully automated).

# You need to set these variables:

languageToCache = "zh" # the language we are interested in

hanziOnly = 1  # 1 or 0.  If 1 then only phrases consisting
# entirely of Chinese characters will be listed (could be useful
# for voices like MeiLing which can't really manage anything else)

newStuff = "new-stuff" # the directory in which *.txt files
# will be created, and to look for the resulting *.mp3/*.wav files

sporadic = 1  # 1 or 0, whether or not to ask for the cached words
# to be generated in "sporadic" mode (i.e. not used 100% of the time)

delete_old = 1  # if 1 (and if sporadic) then older cached
# files (that are still marked sporadic) are deleted.  This
# requires that you don't delete the .txt files from synthCache when
# this script moves them there, as that's how it identifies its
# "own" mp3/wav files (as opposed to anything else you may have cached).

# -----------------------------------------

import sys,os,time

if sporadic: sporadic="_"
else: sporadic=""

try: os.mkdir(newStuff)
except: pass

sys.argv = []
import gradint
gradint.cache_maintenance_mode = 1
assert gradint.synthCache, "need a synthCache for this to work"
try: trans = open(gradint.synthCache+os.sep+gradint.transTbl).read().replace("\n"," ")+" "
except: trans = ""
def synth_fileExists(f):
    try:
        open(gradint.synthCache+os.sep+f)
        return 1
    except: return (" "+f+" ") in trans

# Check for previous newStuff .txt's, and any results from them
generating = {}
fname2txt = {}
for l in os.listdir(newStuff):
    if l.endswith(gradint.dottxt) and "_" in l:
        txt = open(newStuff+os.sep+l).read().decode('utf-16')
        txt = (sporadic+txt,l[l.rindex("_")+1:l.rindex(gradint.extsep)])
        generating[txt] = 1 ; fname2txt[l[:l.rindex(gradint.extsep)]]=txt
for l in os.listdir(newStuff):
    if l.endswith(gradint.dotwav) or l.endswith(gradint.dotmp3):
        k=l[:l.rindex(gradint.extsep)]
        if k in fname2txt: generating[fname2txt[k]]=newStuff+os.sep+l
del fname2txt # now 'generating' maps (txt,lang) to 1 or filename

def getTxtLang(s):
    if '!synth:' in s and "_" in s: return gradint.textof(s).decode('utf-8'),gradint.languageof(s)
    elif s.endswith(gradint.extsep+"txt"): return gradint.readText(s).decode('utf-8'), gradint.languageof(s)
    else: return None,None

def decache(s):
    textToSynth,langToSynth = getTxtLang(s)
    if not textToSynth: return
    textToSynth="_"+textToSynth # sporadic mode
    generating[(textToSynth.lower(),langToSynth)]=1 # don't re-generate it
    textToSynth=textToSynth.encode('utf-8')
    s=textToSynth.lower()+"_"+langToSynth
    if delete_old and langToSynth==languageToCache and gradint.fileExists_stat(gradint.synthCache+os.sep+s+gradint.dottxt):
        for ext in [gradint.dottxt,gradint.dotwav,gradint.dotmp3]:
            try: os.remove(gradint.synthCache+os.sep+s+ext)
            except: pass

samples = gradint.scanSamples() # MUST call before sporadic so variantFiles is populated

if sporadic:
  if delete_old: print "Checking for old words to remove"
  else: print "Sporadic mode: Checking for old words to avoid"
  for t,prompt,target in gradint.ProgressDatabase().data:
    if t>=gradint.reallyKnownThreshold:
        if type(prompt)==type([]):
            for p in prompt: decache(p)
        else: decache(prompt)
        decache(target)

count = 0

def maybe_cache(s):
    textToSynth,langToSynth = getTxtLang(s)
    if not textToSynth: return
    if not langToSynth==languageToCache: return
    if hanziOnly and not gradint.fix_compatibility(textToSynth).replace(" ","")==gradint.hanzi_and_punc(textToSynth).replace(" ",""): return
    for txt in [textToSynth, sporadic+textToSynth]:
      if synth_fileExists((txt.encode('utf-8')+"_"+langToSynth+gradint.dotwav).lower()) or synth_fileExists((txt.encode('utf-8')+"_"+langToSynth+gradint.dotmp3).lower()): return # it's already been done
      if synth_fileExists(("__rejected_"+txt.encode('utf-8')+"_"+langToSynth+gradint.dotwav).lower()) or synth_fileExists(("__rejected_"+txt.encode('utf-8')+"_"+langToSynth+gradint.dotmp3).lower()): return # it's been rejected
    textToSynth=sporadic+textToSynth
    k = (textToSynth.lower(),langToSynth)
    if generating.has_key(k):
        if not generating[k]==1: # a file already exists
            # don't use os.rename - can get problems cross-device
            open(gradint.synthCache+os.sep+textToSynth.encode('utf-8')+'_'+langToSynth+generating[k][generating[k].rindex(gradint.extsep):],"wb").write(open(generating[k],"rb").read())
            #open(gradint.synthCache+os.sep+textToSynth.encode('utf-8')+'_'+langToSynth+gradint.dottxt,"wb").write(open(generating[k][:generating[k].rindex(gradint.extsep)]+gradint.dottxt,"rb").read())
            os.remove(generating[k])
            os.remove(generating[k][:generating[k].rindex(gradint.extsep)]+gradint.dottxt)
            generating[k]=1
        return
    generating[k]=1
    global count
    while gradint.fileExists(newStuff+os.sep+str(count)+"_"+langToSynth+gradint.dottxt): count += 1
    open(newStuff+os.sep+str(count)+"_"+langToSynth+gradint.dottxt,"w").write(textToSynth[len(sporadic):].encode('utf-16'))
    count += 1

print "Checking for new ones"
for _,s1,s2 in samples+gradint.parseSynthVocab("vocab.txt"):
    if type(s1)==type([]): [maybe_cache(i) for i in s1]
    else: maybe_cache(s1)
    maybe_cache(s2)

if count: print "Now convert the files in "+newStuff+" and re-run this script.\nYou might also want to adjust the volume if appropriate, e.g. mp3gain -r -d 6 -c *.mp3"
else: print "No extra files needed to be made."

#!/usr/bin/env python

# Script to assist with using TextAloud or similar program
# that can batch-synthesize a collection of text files
# provided it is run interactively to start the batch conversion.

# This script will generate appropriate *.txt files for the
# words in vocab.txt etc, and rename the resulting *.mp3 or *.wav
# files into the synth cache.

# Should be useful if you are not on Windows and want to run a
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

# (Note: If you need to artificially specify a
# division between two hanzi words, use a hyphen
# (-) to do it.  MeiLing and Gradint/Yali will
# both recognise this as a word boundary that is
# not to be pronounced.)

newStuff = "new-stuff" # the directory in which *.txt files
# will be created, and to look for the resulting *.mp3/*.wav files

sporadic = 1  # 1 or 0, whether or not to ask for the cached words
# to be generated in "sporadic" mode (i.e. not used 100% of the time)

delete_old = 1  # if 1 (and if sporadic) then older cached
# files (that are still marked sporadic) are deleted.  This
# requires that you don't delete the .txt files from synthCache when
# this script moves them there, as that's how it identifies its
# "own" mp3/wav files (as opposed to anything else you may have cached).

actually_generate = 0 # if 1, will call gradint to generate
# the cached sound using its choice of voice for that language,
# instead of relying on your use of TextAloud etc.
# Might be useful if you need to move it to another machine that
# doesn't have that voice, and you still want to use sporadic
# etc (like a more advanced version of cache-synth.py)
testMode = 0 # if 1 and actually_generate is 1, will play too

# -----------------------------------------

import sys,os,time

if sporadic: sporadic="_"
else: sporadic=""

try: os.mkdir(newStuff)
except: pass

sys.argv = []
import gradint
from gradint import dottxt,dotwav,dotmp3
assert gradint.synthCache, "need a synthCache for this to work"
gradint.cache_maintenance_mode = 1
try: trans = open(gradint.synthCache+os.sep+gradint.transTbl).read().replace("\n"," ")+" "
except: trans = ""
scld=gradint.list2dict(os.listdir(gradint.synthCache))
def synth_fileExists(f):
    if f in scld: return True
    else: return (" "+f+" ") in trans

# Check for previous newStuff .txt's, and any results from them
generating = {}
fname2txt = {}
for l in os.listdir(newStuff):
    if l.endswith(dottxt) and "_" in l:
        txt = open(newStuff+os.sep+l).read().decode('utf-16')
        txt = (sporadic+txt,l[l.rindex("_")+1:l.rindex(gradint.extsep)])
        generating[txt] = 1 ; fname2txt[l[:l.rindex(gradint.extsep)]]=txt
for l in os.listdir(newStuff):
    if l.endswith(dotwav) or l.endswith(dotmp3):
        k=l[:l.rindex(gradint.extsep)]
        if k in fname2txt: generating[fname2txt[k]]=newStuff+os.sep+l
del fname2txt # now 'generating' maps (txt,lang) to 1 or filename

def getTxtLang(s):
    if '!synth:' in s and "_" in s: return gradint.textof(s).decode('utf-8'),gradint.languageof(s)
    elif s.endswith(gradint.extsep+"txt"):
        langToSynth = gradint.languageof(s)
        if langToSynth==languageToCache: return gradint.readText(s).decode('utf-8'), langToSynth # else don't bother reading the file (it might be over ftpfs)
    return None,None

def decache(s):
    textToSynth,langToSynth = getTxtLang(s)
    if not textToSynth: return
    textToSynth="_"+textToSynth # sporadic mode
    generating[(textToSynth.lower(),langToSynth)]=1 # don't re-generate it
    s=textToSynth.lower().encode('utf-8')+"_"+langToSynth
    if delete_old and langToSynth==languageToCache:
        for ext in [dottxt,dotwav,dotmp3]:
            if s+ext in scld:
                os.remove(gradint.synthCache+os.sep+s+ext)
                del scld[s+ext]

samples = gradint.scanSamples() # MUST call before sporadic so variantFiles is populated

if sporadic:
  pd = gradint.ProgressDatabase()
  if delete_old: print "Checking for old words to remove"
  else: print "Sporadic mode: Checking for old words to avoid"
  for t,prompt,target in pd.data:
    if t>=gradint.reallyKnownThreshold:
        if type(prompt)==type([]):
            for p in prompt: decache(p)
        else: decache(prompt)
        decache(target)

count = 0 ; toMove = []

def rename(old,new):
    # don't use os.rename - can get problems cross-device
    open(new,"wb").write(open(old,"rb").read())
    os.remove(old)

def maybe_cache(s):
    textToSynth,langToSynth = getTxtLang(s)
    if not textToSynth: return
    if not langToSynth==languageToCache: return
    if hanziOnly and not gradint.fix_compatibility(textToSynth).replace(" ","")==gradint.hanzi_and_punc(textToSynth).replace(" ",""): return
    for txt in [textToSynth, sporadic+textToSynth]:
      if synth_fileExists((txt.encode('utf-8')+"_"+langToSynth+dotwav).lower()) or synth_fileExists((txt.encode('utf-8')+"_"+langToSynth+dotmp3).lower()): return # it's already been done
      if synth_fileExists(("__rejected_"+txt.encode('utf-8')+"_"+langToSynth+dotwav).lower()) or synth_fileExists(("__rejected_"+txt.encode('utf-8')+"_"+langToSynth+dotmp3).lower()): return # it's been rejected
    textToSynth=sporadic+textToSynth
    k = (textToSynth.lower(),langToSynth)
    if generating.has_key(k):
        if not generating[k]==1: # a file already exists
            fname = textToSynth.lower().encode('utf-8')+'_'+langToSynth+generating[k][generating[k].rindex(gradint.extsep):]
            rename(generating[k],gradint.synthCache+os.sep+fname)
            scld[fname] = 1
            #rename(generating[k][:generating[k].rindex(gradint.extsep)]+dottxt,gradint.synthCache+os.sep+textToSynth.lower().encode('utf-8')+'_'+langToSynth+dottxt)
            os.remove(generating[k][:generating[k].rindex(gradint.extsep)]+dottxt)
            generating[k]=1
        return
    if actually_generate:
        tm = [gradint.synth_event(langToSynth,textToSynth[len(sporadic):].encode('utf-8')).getSound(),(textToSynth.encode('utf-8')+"_"+langToSynth+dotwav).lower()]
        if gradint.got_program("lame"):
            # we can MP3-encode it (TODO make this optional)
            n = tm[0][:-len(dotwav)]+dotmp3
            if not os.system("lame --cbr -h -b 48 -m m \"%s\" \"%s\"" % (tm[0],n)):
              os.remove(tm[0])
              tm[0] = n
              tm[1] = tm[1][:-len(dotwav)]+dotmp3
        toMove.append(tm)
        scld[textToSynth.lower().encode('utf-8')+'_'+langToSynth+dotwav] = 1
        return
    generating[k]=1
    global count
    while gradint.fileExists(newStuff+os.sep+str(count)+"_"+langToSynth+dottxt): count += 1
    open(newStuff+os.sep+str(count)+"_"+langToSynth+dottxt,"w").write(textToSynth[len(sporadic):].encode('utf-16'))
    count += 1

print "Checking for new ones"
for _,s1,s2 in samples+gradint.parseSynthVocab(gradint.vocabFile):
    if type(s1)==type([]): [maybe_cache(i) for i in s1]
    else: maybe_cache(s1)
    maybe_cache(s2)

if toMove: sys.stderr.write("Renaming\n")
for tmpfile,dest in toMove:
    oldDest = dest
    try:
        rename(tmpfile,gradint.synthCache+os.sep+dest)
    except OSError: # not a valid filename
        while gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+dotwav) or gradint.fileExists(gradint.synthCache+os.sep+("__file%d" % count)+dotmp3): count += 1
        rename(tmpfile,gradint.synthCache+os.sep+("__file%d" % count)+dotwav)
        open(gradint.synthCache+os.sep+gradint.transTbl,"ab").write("__file%d%s %s\n" % (count,dotwav,dest))
        dest = "__file%d%s" % (count,dotwav)
    if testMode:
        print oldDest
        e=gradint.SampleEvent(gradint.synthCache+os.sep+dest)
        t=time.time() ; e.play()
        while time.time() < t+e.length: time.sleep(1) # in case play() is asynchronous
    
if count: print "Now convert the files in "+newStuff+" and re-run this script.\nYou might also want to adjust the volume if appropriate, e.g. mp3gain -r -d 6 -c *.mp3"
elif not toMove: print "No extra files needed to be made."
else: print "All done"

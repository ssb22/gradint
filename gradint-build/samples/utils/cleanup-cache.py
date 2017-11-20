#!/usr/bin/env python

# delete cached synthesized words that are not used
# (i.e. not mentioned in vocab.txt or samples).
# Run in the same directory as gradint.py with all the settings.

quarantine = 0 # set to 1 to move the samples to "unused" instead of deleting them
also_remove_words_that_can_be_synthesized_by_partials = 0  # set to 1 if you want

import sys,os,time
import gradint
if not gradint.synthCache:
    sys.stderr.write("Error - synthCache is not set in advanced.txt\n") ; sys.exit()
gradint.cache_maintenance_mode=1
def transLineToTuple(l):
    x,y = l.split(None,1)
    y="!synth:"+y
    if gradint.extsep in x: x=x[:x.rindex(gradint.extsep)] # make comparison easier (extensions don't matter to us)
    return (gradint.textof(y)+"_"+gradint.languageof(y),x)
try: trans = dict([transLineToTuple(l) for l in filter(lambda x:x,open(gradint.synthCache+os.sep+gradint.transTbl).read().split("\n"))])
except IOError: trans = {}
unused = dict([(a[:a.rindex(gradint.extsep)],a) for a in filter(lambda x:gradint.extsep in x,os.listdir(gradint.synthCache))]) # (strip extensions - they don't matter for our purposes)
try: del unused[gradint.transTbl[:gradint.transTbl.rfind(gradint.extsep)]]
except KeyError: pass
def mark_as_used(s,directory):
    if s and '!synth:' in s and "_" in s: textToSynth, langToSynth = gradint.textof(s),gradint.languageof(s)
    elif s and s.endswith(gradint.extsep+"txt"): textToSynth, langToSynth = gradint.readText(directory+os.sep+s), gradint.languageof(s,directory==gradint.promptsDirectory)
    else: return
    k=(textToSynth+"_"+langToSynth).lower()
    k=trans.get(k,k)
    for p in ["__rejected_","__rejected__"]:
        if p+k in unused: del unused[p+k]
    if not k in unused:
        if "_"+k in unused: k="_"+k
        else: return
    if also_remove_words_that_can_be_synthesized_by_partials and gradint.synth_from_partials(textToSynth,langToSynth): return
    del unused[k]

for _,s1,s2 in gradint.scanSamples()+gradint.parseSynthVocab(gradint.vocabFile):
    if type(s1)==type([]): [mark_as_used(i,gradint.samplesDirectory) for i in s1]
    else: mark_as_used(s1,gradint.samplesDirectory)
    mark_as_used(s2,gradint.samplesDirectory)
for f in gradint.AvailablePrompts().lsDic.values():
    for f2 in f:
        if f2.endswith("txt"): mark_as_used(f2,gradint.promptsDirectory)

if quarantine:
    try: os.mkdir(gradint.synthCache+os.sep+"unused")
    except: pass
for k,v in unused.items():
    if quarantine: os.rename(gradint.synthCache+os.sep+v,gradint.synthCache+os.sep+"unused"+os.sep+v)
    else: os.unlink(gradint.synthCache+os.sep+v)
if quarantine: sys.stdout.write("Moved "+str(len(unused))+" unused items to "+gradint.synthCache+os.sep+"unused\n")
else: sys.stdout.write("Deleted "+str(len(unused))+" unused items\n")

# TODO delete from TRANS.TBL file any lines not referenced in 'trans'  (or make cache-synth.py check for actual existence of the files mentioned in TRANS.TBL, like gradint.py does, before concluding that they don't need to be generated)

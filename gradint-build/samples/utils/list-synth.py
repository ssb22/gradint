#!/usr/bin/env python

# list-synth.py language [language ...]
# list all words that can be synthesized

# Run in the same directory as gradint.py with
# all the settings.

paragraph_size = 255
# if not 0, will try to split into paragraphs of max this
# number of characters (after decoding the utf-8)

hanzi_only = 1
# This is a hack for Chinese: if it's not 0, anything in
# language "zh" will be listed only if it's entirely hanzi,
# not pinyin (use for quick testing your vocab on an online
# demo synth that supports only hanzi)

reverse_grouping = 1
# if set, paragraphs will be grouped backwards
# from the end of the list (useful if newest
# words are at end and you don't want a trailing
# half-paragraph)

# ------------------------------------------------------

outFilename = "cache-list"

import sys,os,time
lang = sys.argv[1:]
if not lang:
    sys.stderr.write("Please put a language abbreviation on the command line.  See comments at the start of this script for details.\n")
    sys.exit()
lang=lang[0]
sys.argv = []
import gradint
if not gradint.synthCache:
    sys.stderr.write("Error - synthCache is not set in advanced.txt\n") ; sys.exit()
gradint.cache_maintenance_mode=1
toList = []
wroteChars = 0 ; listed = {}
if gradint.fileExists("cachelist-done"+gradint.dottxt): listed=gradint.list2set(filter(lambda x:x,gradint.u8strip(open("cachelist-done"+gradint.dottxt).read().replace("\r","\n")).split("\n")))
def maybe_list(s,directory):
    if not s: return # in case poetry has some 2nd-language only
    if '!synth:' in s and "_" in s: textToSynth, langToSynth = gradint.textof(s),gradint.languageof(s)
    elif s.endswith(gradint.dottxt): textToSynth, langToSynth = gradint.readText(directory+os.sep+s), gradint.languageof(s,directory==gradint.promptsDirectory)
    else: return
    if not langToSynth==lang: return # we're not listing that language
    if textToSynth.lower() in listed: return
    d=textToSynth.decode('utf-8')
    if hanzi_only and langToSynth=="zh" and not gradint.fix_compatibility(d).replace(" ","")==gradint.hanzi_and_punc(d): return
    global wroteChars
    if paragraph_size and wroteChars and wroteChars+len(d)>paragraph_size:
        toList.append("") ; wroteChars = 0
    wroteChars += (len(d)+2) # comma and \n
    toList.append(textToSynth+",")
    listed[textToSynth.lower()]=1

inList = gradint.scanSamples()+gradint.parseSynthVocab(gradint.vocabFile)
if reverse_grouping: inList.reverse() # will be reversed again on output
for _,s1,s2 in inList:
    if type(s1)==type([]): [maybe_list(i,gradint.samplesDirectory) for i in s1]
    else: maybe_list(s1,gradint.samplesDirectory)
    maybe_list(s2,gradint.samplesDirectory)
for f in gradint.AvailablePrompts().lsDic.values():
    for f2 in f:
        if f2.endswith("txt"): maybe_list(f2,gradint.promptsDirectory)

if reverse_grouping: toList.reverse()
for i in range(len(toList)+1):
    if i and (i==len(toList) or toList[i]=="\n") and toList[i-1].endswith(","):
        toList[i-1]=toList[i-1][:-1] # don't need last comma of each paragraph
listFile = open(outFilename+gradint.dottxt,"w")
listFile.write('\xef\xbb\xbfEdit this file, deleting this message and the phrases you don\'t want,\nget it recorded or synthesized, and split the recording into lines\n(using HardDiskOgg or Audacity or one of the utils)\nthen feed edited list + recordings to list2cache.py to get into '+gradint.synthCache+'\n\n')
listFile.write("\n".join(toList))
listFile.close()
sys.stdout.write("List written to %s\n" % (outFilename+gradint.dottxt+" (in utf-8)"))
if gradint.textEditorCommand: os.system(gradint.textEditorCommand+" "+outFilename+gradint.dottxt)

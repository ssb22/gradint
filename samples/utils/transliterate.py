#!/usr/bin/env python2

# transliterate.py - print a 2nd-language-transliterated version of vocab.txt and any .txt pairs in samples
# (may be useful for grepping, loading to Latin-only PDA, etc)
# (note: leaves comments untransliterated, + may not translit all text if gradint is set up so a transliterating synth will not be used)

# (c) 2008 Silas S. Brown, version 1.1.  License: GPL

from gradint import *
import re
synth = get_synth_if_possible(secondLanguage,0,to_transliterate=True)
def prep(txt):
    translit = None
    if synth: translit = synth.transliterate(secondLanguage,txt)
    if translit and txt==translit: translit=None
    if translit: txt = translit
    if secondLanguage=="zh" and re.match(r"^[A-Za-z]*[1-5]( [A-Za-z]*[1-5])*$",txt): txt=txt.replace(" ","") # rm spaces if it looks like single word with spaced-out syllables - may help with searching (and does not seem to compromise tcr compression ratios) (TODO + do we want to do this unconditionally if we transliterated and no space in original? could save misleading grouping from espeak exceptions, but may squash a long phrase)
    if translit: txt="["+txt+"]" # indicate was translit'd
    return txt
langs=[secondLanguage,firstLanguage]
def has_unicode(t):
    try: unicode(t,"ascii")
    except UnicodeDecodeError: return 1
for l in u8strip(open(vocabFile).read()).replace("\r\n","\n").split("\n"):
    if l.startswith("set language"): langs=l.split()[2:]
    elif ('=' in l or has_unicode(l)) and not l.startswith("#"):
        l2 = []
        for lang,word in zip(langs,l.split("=",len(langs)-1)):
            if lang==secondLanguage: word=prep(word)
            l2.append(word)
        l="=".join(l2)
    sys.stdout.write(l+"\n")
list2=guiVocabList(scanSamples()) # TODO that will leave out any _meaning stuff implemented as .txt pairs
if list2:
    sys.stdout.write("# words from "+samplesDirectory+":\n")
    for l2,l1 in list2: sys.stdout.write(prep(l2)+"="+l1+"\n")

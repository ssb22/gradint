# -*- coding: utf-8 -*-

# cantonese.py - Python functions for processing Cantonese transliterations
# (uses eSpeak and Gradint for help with some of them)

# (c) 2013 Silas S. Brown.  License: GPL

dryrun_mode = False # True makes get_jyutping just batch it up for later
jyutping_cache = {} ; jyutping_dryrun = set()

def get_jyutping(hanzi,mustWork=1):
  global espeak
  if not espeak:
      espeak = import_gradint().ESpeakSynth()
      if not espeak.works_on_this_platform(): # must call
          raise Exception("espeak.works_on_this_platform")
      assert espeak.supports_language("zhy")
  global jyutping_dryrun
  if dryrun_mode:
      jyutping_dryrun.add(hanzi)
      return "aai1" # dummy value
  elif jyutping_dryrun:
      jyutping_dryrun = list(jyutping_dryrun)
      vals = espeak.transliterate_multiple("zhy",jyutping_dryrun,0)
      assert len(jyutping_dryrun)==len(vals)
      for k,v in zip(jyutping_dryrun,vals):
        jyutping_cache[k]=v
      jyutping_dryrun = set()
  if hanzi in jyutping_cache: jyutping = jyutping_cache[hanzi]
  else: jyutping_cache[hanzi] = jyutping = espeak.transliterate("zhy",hanzi,forPartials=0).replace("7","1").lower() # .lower() needed because espeak sometimes randomly capitalises e.g. 2nd hanzi of 'hypocrite' (Mandarin xuwei de ren)
  if mustWork: assert jyutping.strip(), "No translit. result for "+repr(hanzi)
  elif not jyutping.strip(): jyutping=""
  return jyutping
espeak = 0

def jyutping_to_lau(j):
  j = j.lower().replace("j","y").replace("z","j")
  for k,v in jlRep: j=j.replace(k,v)
  return j.lower()
jlRep = [(unchanged,unchanged.upper()) for unchanged in "aai aau aam aang aan aap aat aak ai au am ang an ap at ak a ei eng ek e iu im ing in ip it ik i oi ong on ot ok ung uk".split()] + [("eoi","UI"),("eon","UN"),("eot","UT"),("eok","EUK"),("oeng","EUNG"),("oe","EUH"),("c","ch"),("ou","O"),("o","OH"),("yu","UE"),("u","OO")]
jlRep.sort(lambda a,b:len(b[0])-len(a[0]))
# u to oo includes ui to ooi, un to oon, ut to oot
# yu to ue includes yun to uen and yut to uet
# drawing from the table on http://www.omniglot.com/writing/cantonese.htm plus this private communication:
# Jyutping "-oeng" maps to Sidney Lau "-eung".
# Jyutping "jyu" maps to Sidney Lau "yue". (consequence of yu->ue, j->y)

def ping_or_lau_to_syllable_list(j):
  j = re.sub(r"[^a-zA-Z0-9]"," ",j)
  for digit in "123456789": j=j.replace(digit,digit+" ")
  return j.split()
import re

def hyphenate_ping_or_lau_syl_list(sList,groupLens=None):
    if type(sList) in [str,unicode]:
        sList = ping_or_lau_to_syllable_list(sList)
    if not groupLens: groupLens = [len(sList)]
    else: assert sum(groupLens) == len(sList)
    r = [] ; start = 0
    for g in groupLens:
        r.append("-".join(sList[start:start+g]))
        start += g
    return " ".join(r)
    
def jyutping_to_yale_TeX(j):
  ret=[]
  for syl in ping_or_lau_to_syllable_list(j.lower().replace("eo","eu").replace("oe","eu").replace("j","y").replace("yyu","yu").replace("z","j").replace("c","ch")):
    vowel=None
    for i in range(len(syl)):
      if syl[i] in "aeiou":
        vowel=i ; break
    if not vowel:
      ret.append(syl.upper()) ; continue # English word or letter in the Chinese?
    if syl[vowel:vowel+2] == "aa" and (len(syl)<vowel+2 or syl[vowel+2] in "123456"):
      syl=syl[:vowel]+syl[vowel+1:] # final aa -> a
    # the tonal 'h' goes after all the vowels but before any consonants:
    for i in range(len(syl)-1,-1,-1):
      if syl[i] in "aeiou":
        lastVowel=i ; break
    if syl[-1] in "456":
      syl=syl[:lastVowel+1]+"h"+syl[lastVowel+1:-1]+str(int(syl[-1])-3)
    if syl[-1] in "123":
      ret.append(syl[:vowel]+[r"\`",r"\'",r""][int(syl[-1])-1]+syl[vowel:-1]) # TODO do we want \= in the 3rd one?  what if it's over an i ?
    else: ret.append(syl.upper()) # English word or letter in the Chinese?
  return ' '.join(ret)

def superscript_digits_TeX(j):
  # for jyutping and Sidney Lau
  for digit in "123456789": j=j.replace(digit,r"$^"+digit+r"$\hspace{0pt}")
  return j

def superscript_digits_HTML(j):
  for digit in "123456789": j=j.replace(digit,"<sup>"+digit+"</sup>")
  return j

def superscript_digits_UTF8(j):
  # WARNING: not all fonts have all digits; many have only the first 3.  superscript_digits_HTML might be better for browsers, even though it does produce more bytes.
  for digit in range(1,10): j=j.replace(str(digit),u"¹²³⁴⁵⁶⁷⁸⁹"[digit-1].encode('utf-8'))
  return j

import sys

def annogen_reannotate(input_c,annotate_func):
    # re-annotates any annogen o() and o2() calls
    
    # TODO: annotate_func is called separately for each
    # o() and o2() call; should we group and degroup it
    # so it has access to the whole phrase?

    # (Could also post-process annogen's output, but the
    # result would run slower than an altered C program.
    # Could integrate 2+ annotations into the same program
    # but that would make it larger and slow down loading
    # etc - not so good if only one of the annotations is
    # going to be used at any one time.)

    global dryrun_mode ; dryrun_mode = True
    for m in re.finditer(r'o2?\("([^"]*)","[^"]*"(,"[^"]*")?\);',input_c): get_jyutping(m.groups()[0])
    dryrun_mode = False

    i = 0 ; out = []
    for m in re.finditer(r'(o2?)\("([^"]*)","[^"]*"(,"[^"]*")?\);',input_c):
      out.append(input_c[i:m.start()])
      rest = m.groups()[2]
      if not rest: rest = ""
      out.append(m.groups()[0]+'("'+m.groups()[1]+'","'+annotate_func(m.groups()[1])+'"'+rest+');')
      i = m.end()
    out.append(input_c[i:])
    return "".join(out)

def import_gradint():
    global gradint
    try: return gradint
    except: pass
    # when importing gradint, make sure no command line
    tmp,sys.argv = sys.argv,sys.argv[:1]
    import gradint
    sys.argv = tmp
    return gradint

if __name__ == "__main__":
    # command-line use: redo annotator.c on stdin to S.Lau
    sys.stdout.write(annogen_reannotate(sys.stdin.read(),lambda h:superscript_digits_HTML(hyphenate_ping_or_lau_syl_list(jyutping_to_lau(get_jyutping(h,0))))))

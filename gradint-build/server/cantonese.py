#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  (should work with either Python 2 or Python 3)

# cantonese.py - Python functions for processing Cantonese transliterations
# (uses eSpeak and Gradint for help with some of them)

# v1.32 (c) 2013-15,2017-21 Silas S. Brown.  License: GPL

dryrun_mode = False # True makes get_jyutping batch it up for later (then run and save cache on first call with False)
jyutping_cache = {} ; jyutping_dryrun = set()
import re, pickle
try: jyutping_cache = pickle.Unpickler(open("/tmp/.jyutping-cache","rb")).load()
except: pass

extra_zhy_dict = { # TODO: add these to the real zhy_list in eSpeak
  u"\u9c85":"bat3",u"\u9b81":"bat3",
}

def S(v): # make sure it's a string in both Python 2 and 3
  if type("")==type(u""): # Python 3
    try: return v.decode('utf-8') # in case it's bytes
    except: return v
  else: return v
def B(v): # make sure it's bytes in Python 3, str in Python 2
  if type(v)==type(u""): return v.encode('utf-8')
  return v

def get_jyutping(hanzi,mustWork=1):
  if not type(hanzi)==type(u""): hanzi=hanzi.decode('utf-8')
  for k,v in extra_zhy_dict.items(): hanzi=hanzi.replace(k,v)
  global espeak
  if not espeak:
      espeak = import_gradint().ESpeakSynth()
      if not espeak.works_on_this_platform(): # must call
          raise Exception("espeak.works_on_this_platform")
      assert espeak.supports_language("zhy")

  global jyutping_dryrun
  if dryrun_mode:
      if not hanzi in jyutping_cache: jyutping_dryrun.add(hanzi)
      return "aai1" # dummy value
  elif jyutping_dryrun:
      jyutping_dryrun = list(jyutping_dryrun)
      vals = espeak.transliterate_multiple("zhy",jyutping_dryrun,0)
      assert len(jyutping_dryrun)==len(vals)
      for k,v in zip(jyutping_dryrun,vals):
        jyutping_cache[k]=S(v).replace("7","1").lower() # see below
      jyutping_dryrun = set()
      try: pickle.Pickler(open("/tmp/.jyutping-cache","wb"),-1).dump(jyutping_cache)
      except: pass
  if hanzi in jyutping_cache: jyutping = jyutping_cache[hanzi]
  else: jyutping_cache[hanzi] = jyutping = S(espeak.transliterate("zhy",hanzi,forPartials=0)).replace("7","1").lower() # .lower() needed because espeak sometimes randomly capitalises e.g. 2nd hanzi of 'hypocrite' (Mandarin xuwei de ren)
  if mustWork: assert jyutping.strip(), "No translit. result for "+repr(hanzi)
  elif not jyutping.strip(): jyutping=""
  return jyutping
espeak = 0

def hanzi_only(unitext): return u"".join(filter(lambda x:0x4e00<=ord(x)<0xa700 or ord(x)>=0x10000, list(unitext)))
def adjust_jyutping_for_pinyin(hanzi,jyutping,pinyin):
  # If we have good quality (proof-read etc) Mandarin pinyin, this can sometimes improve the automatic Cantonese transcription
  if not type(hanzi)==type(u""): hanzi = hanzi.decode('utf-8')
  hanzi = hanzi_only(hanzi)
  if not re.search(py2j_chars,hanzi): return jyutping
  if not type(pinyin)==type(u""): pinyin = pinyin.decode('utf-8')
  assert pinyin.strip(), "blank pinyin" # saves figuring out a findall TypeError
  py2 = espeak.transliterate("zh",pinyin,forPartials=0) # TODO: dryrun_mode ?  (this transliterate just does tone marks to numbers, adds 5, etc; forPartials=0 because we DON'T want to change letters like X into syllables, as that won't happen in jyutping and we're going through it tone-by-tone)
  assert py2 and py2.strip(), "espeak.transliterate returned %s for %s" % (repr(py2),repr(pinyin))
  pinyin = re.findall('[A-Za-z]*[1-5]',S(py2))
  if not len(pinyin)==len(hanzi): return jyutping # can't fix
  jyutping = S(jyutping)
  i = 0 ; tones = re.finditer('[1-7]',jyutping) ; j2 = []
  for h,p in zip(list(hanzi),pinyin):
    try: j = tones.next().end()
    except StopIteration: raise Exception("Ran out of tones in "+jyutping+" when zipping "+repr(hanzi)+'/'+repr(pinyin))
    j2.append(jyutping[i:j]) ; i = j
    if h in py2j and p.lower() in py2j[h]: j2[-1]=j2[-1][:re.search("[A-Za-z]*[1-7]$",j2[-1]).start()]+py2j[h][p.lower()]
  return "".join(j2)+jyutping[i:]
py2j={
u"\u4E2D":{"zhong1":"zung1","zhong4":"zung3"},
u"\u4E3A\u70BA":{"wei2":"wai4","wei4":"wai6"},
u"\u4E50\u6A02":{"le4":"lok6","yue4":"ngok6"},
u"\u4EB2\u89AA":{"qin1":"can1","qing4":"can3"},
u"\u4F20\u50B3":{"chuan2":"cyun4","zhuan4":"zyun6"},
u"\u4FBF":{"bian4":"pin4","pian2":"bin6"},
u"\u5047":{"jia3":"gaa2","jia4":"gaa3"},
u"\u5174\u8208":{"xing1":"hing1","xing4":"hing3"},
# u"\u5207":{"qie4":"cai3","qie1":"cit3"}, # WRONG (rm'd v1.17).  It's cit3 in re4qie4.  It just wasn't in yiqie4 (which zhy_list has as an exception anyway)
u"\u521B\u5275":{"chuang1":"cong1","chuang4":"cong3"},
u"\u53EA":{"zhi1":"zek3","zhi3":"zi2"},
u"\u53F7\u865F":{"hao4":"hou6","hao2":"hou4"},
u"\u548C":{"he2":"wo4","he4":"wo6"},
u"\u54BD":{"yan1":"jin1","yan4":"jin3","ye4":"jit3"},
u"\u5708":{"juan4":"gyun6","quan1":"hyun1"},
u"\u597D":{"hao3":"hou2","hao4":"hou3"},
u"\u5C06\u5C07":{"jiang1":"zoeng1","jiang4":"zoeng3"},
u"\u5C11":{"shao3":"siu2","shao4":"siu3"},
u"\u5DEE":{"cha4":"caa1","cha1":"caa1","chai1":"caai1"},
u"\u5F37\u5F3A":{"qiang2":"koeng4","qiang3":"koeng5"},
u"\u62C5\u64D4":{"dan1":"daam1","dan4":"daam3"},
u"\u6323\u6399":{"zheng4":"zaang6","zheng1":"zang1"},
u"\u6570\u6578":{"shu3":"sou2","shu4":"sou3"},
u"\u671D":{"chao2":"ciu4","zhao1":"ziu1"},
u"\u6ED1":{"hua2":"waat6","gu3":"gwat1"},
u"\u6F02":{"piao1":"piu1","piao3 piao4":"piu3"},
u"\u76DB":{"sheng4":"sing6","cheng2":"sing4"},
u"\u76F8":{"xiang1":"soeng1","xiang4":"soeng3"},
u"\u770B":{"kan4":"hon3","kan1":"hon1"},
u"\u79CD\u7A2E":{"zhong3":"zung2","zhong4":"zung3"},
u"\u7EF7\u7E43":{"beng1":"bang1","beng3":"maang1"},
u"\u8208":{"xing1":"hing1","xing4":"hing3"},
u"\u843D":{"luo1 luo4 lao4":"lok6","la4":"laai6"},
u"\u8457":{"zhu4":"zyu3","zhuo2":"zoek3","zhuo2 zhao2 zhao1 zhe5":"zoek6"},
u"\u8981":{"yao4":"jiu3","yao1":"jiu1"},
u"\u89C1\u898B":{"jian4":"gin3","xian4":"jin6"},
u"\u89C9\u89BA":{"jue2":"gok3","jiao4":"gaau3"},
u"\u8B58\u8BC6":{"shi2 shi4":"sik1","zhi4":"zi3"},
u"\u8ABF\u8C03":{"diao4":"diu6","tiao2":"tiu4"},
u"\u91CF":{"liang2":"loeng4","liang4":"loeng6"},
u"\u9577\u957F":{"chang2":"coeng4","zhang3":"zoeng2"},
u"\u9593\u95F4":{"jian1":"gaan1","jian4":"gaan3"},
u"\u96BE\u96E3":{"nan2":"naan4","nan4":"naan6"}}
for k in list(py2j.keys()):
   if len(k)>1:
    for c in list(k): py2j[c]=py2j[k]
    del py2j[k]
for _,v in py2j.items():
  for k in list(v.keys()):
    if len(k.split())>1:
      for w in k.split(): v[w]=v[k]
      del v[k]
py2j_chars = re.compile(u'['+''.join(list(py2j.keys()))+']')

def jyutping_to_lau(j):
  j = S(j).lower().replace("j","y").replace("z","j")
  for k,v in jlRep: j=j.replace(k,v)
  return j.lower().replace("aa","a").replace("ohek","euk")
def incomplete_lau_to_jyutping(l):
  # incomplete: assumes Lau didn't do the "aa" -> "a" rule
  l = S(l).lower().replace("euk","ohek")
  for k,v in ljRep: l=l.replace(k,v)
  return l.lower().replace("j","z").replace("y","j")
def incomplete_lau_to_yale_u8(l): return jyutping_to_yale_u8(incomplete_lau_to_jyutping(l))
jlRep = [(unchanged,unchanged.upper()) for unchanged in "aai aau aam aang aan aap aat aak ai au am ang an ap at ak a ei eng ek e iu im ing in ip it ik i oi ong on ot ok ung uk".split()] + [("eoi","UI"),("eon","UN"),("eot","UT"),("eok","EUK"),("oeng","EUNG"),("oe","EUH"),("c","ch"),("ou","O"),("o","OH"),("yu","UE"),("u","OO")]
jlRep.sort(key=lambda a:-len(a[0])) # longest 1st
# u to oo includes ui to ooi, un to oon, ut to oot
# yu to ue includes yun to uen and yut to uet
# drawing from the table on http://www.omniglot.com/writing/cantonese.htm plus this private communication:
# Jyutping "-oeng" maps to Sidney Lau "-eung".
# Jyutping "jyu" maps to Sidney Lau "yue". (consequence of yu->ue, j->y)
ljRep=[(b.lower(),a.upper()) for a,b in jlRep]
ljRep.sort(key=lambda a:-len(a[0])) # longest 1st

def ping_or_lau_to_syllable_list(j): return re.sub(r"([1-9])(?![0-9])",r"\1 ",re.sub(r"[!-/:-@^-`]"," ",S(j))).split()

def hyphenate_ping_or_lau_syl_list(sList,groupLens=None):
    if type(sList) in [str,type(u"")]:
        sList = ping_or_lau_to_syllable_list(sList)
    return hyphenate_syl_list(sList,groupLens)
def hyphenate_yale_syl_list(sList,groupLens=None):
    # (if sList is a string, the syllables must be space-separated,
    #  which will be the case if to_yale functions below are used)
    if not type(sList)==list: sList = sList.split()
    return hyphenate_syl_list(sList,groupLens)
def hyphenate_syl_list(sList,groupLens=None):
    assert type(sList) == list
    if not groupLens and '--hyphenate-all' in sys.argv: groupLens = [len(sList)] # this might be suitable for re-annotating hanzi+pinyin to Cantonese in annogen.py's --reannotator option, although it would be better if spacing could be copied from the pinyin for cases where the pinyin line is spaced but the hanzi line is not
    if not groupLens: groupLens = [1]*len(sList) # don't hyphenate at all if we don't know
    else: assert sum(groupLens) == len(sList), "sum("+repr(groupLens)+")!=len("+repr(sList)+")"
    r = [] ; start = 0
    for g in groupLens:
        r.append("-".join(S(x) for x in sList[start:start+g]))
        start += g
    return " ".join(r)
    
def jyutping_to_yale_TeX(j): # returns space-separated syllables
  ret=[]
  for syl in ping_or_lau_to_syllable_list(S(j).lower().replace("eo","eu").replace("oe","eu").replace("j","y").replace("yyu","yu").replace("z","j").replace("c","ch")):
    vowel=lastVowel=None
    for i in range(len(syl)):
      if syl[i] in "aeiou":
        vowel=i ; break
    if vowel==None and re.match(r"h?(m|ng)[456]",syl): # standalone nasal syllables
      vowel = syl.find('m')
      if vowel<0: vowel = syl.index('n')
      lastVowel = syl.find('g')
      if lastVowel<0: lastVowel = vowel
    if vowel==None:
      ret.append(syl.upper()) ; continue # English word or letter in the Chinese?
    if syl[vowel:vowel+2] == "aa" and (len(syl)<vowel+2 or syl[vowel+2] in "123456"):
      syl=syl[:vowel]+syl[vowel+1:] # final aa -> a
    # the tonal 'h' goes after all the vowels but before any consonants:
    for i in range(len(syl)-1,-1,-1):
      if syl[i] in "aeiou":
        lastVowel=i ; break
    if syl[-1] in "1234567":
      # get_jyutping replaces 7 with 1 because zhy_list is
      # more Canton-type than Hong Kong-type Cantonese and
      # there is considerable disagreement on which "1"s
      # should be "7"s, but if you pass any "7" into the
      # jyutping_to_yale functions we can at least process
      # it here:
      tone = ["\=",r"\'","",r"\`",r"\'","",r"\`"][int(syl[-1])-1]
      if syl[-1] in "456":
        syl=syl[:lastVowel+1]+"h"+syl[lastVowel+1:]
      ret.append((syl[:vowel]+tone+syl[vowel:-1]).replace(r"\=i",r"\=\i{}").replace(r"\=I",r"\=\I{}"))
    else: ret.append(syl.upper()) # English word or letter in the Chinese?
  return ' '.join(ret)

def jyutping_to_yale_u8(j): # returns space-separated syllables
  import unicodedata
  def mysub(z,l):
    for x,y in l:
      z = re.sub(re.escape(x)+r"(.)",r"\1"+y,z)
    return z
  if type(u"")==type(""): U=str # Python 3
  else: U=unicode # Python 2
  return unicodedata.normalize('NFC',mysub(U(jyutping_to_yale_TeX(j).replace(r"\i{}","i").replace(r"\I{}","I")),[(r"\`",u"\u0300"),(r"\'",u"\u0301"),(r"\=",u"\u0304")])).encode('utf-8')

def superscript_digits_TeX(j):
  # for jyutping and Sidney Lau
  j = S(j)
  for digit in "123456789": j=j.replace(digit,r"\raisebox{-0.3ex}{$^"+digit+r"$}\hspace{0pt}")
  return j

def superscript_digits_HTML(j):
  j = S(j)
  for digit in "123456789": j=j.replace(digit,"<sup>"+digit+"</sup>")
  return j

def superscript_digits_UTF8(j):
  # WARNING: not all fonts have all digits; many have only the first 3.  superscript_digits_HTML might be better for browsers, even though it does produce more bytes.
  j = S(j)
  for digit in range(1,10): j=j.replace(str(digit),S(u"¹²³⁴⁵⁶⁷⁸⁹"[digit-1].encode('utf-8')))
  if type(j)==type(u""): j=j.encode('utf-8') # Python 3
  return j

import sys

def import_gradint():
    global gradint
    try: return gradint
    except: pass
    # when importing gradint, make sure no command line
    tmp,sys.argv = sys.argv,sys.argv[:1]
    import gradint
    sys.argv = tmp
    return gradint

def do_song_subst(hanzi_u8): return B(hanzi_u8).replace(unichr(0x4f7f).encode('utf-8'),unichr(0x38c8).encode('utf-8')) # Mandarin shi3 (normally jyutping sai2) is usually si3 in songs, so substitute a rarer character that unambiguously has that reading before sending to get_jyutping

if __name__ == "__main__":
    # command-line use: output Lau for each line of stdin
    # (or Yale if there's a --yale in sys.argv, or both
    # with '#' separators if --yale#lau in sys.argv);
    # if there's a # in the line, assume it's hanzi#pinyin
    # (for annogen.py --reannotator="##python cantonese.py")
    lines = sys.stdin.read().replace("\r\n","\n").split("\n")
    if lines and not lines[-1]: del lines[-1]
    dryrun_mode = True
    def songSubst(l):
      if '--song-lyrics' in sys.argv: l=do_song_subst(l)
      return l
    for l in lines:
      if '#' in l: l=l[:l.index('#')]
      get_jyutping(songSubst(l))
    dryrun_mode = False
    for l in lines:
      if '#' in l: l,pinyin = l.split('#')
      else: pinyin = None
      jyutping = get_jyutping(songSubst(l),0)
      if pinyin: jyutping = adjust_jyutping_for_pinyin(l,jyutping,pinyin)
      if "--yale#lau" in sys.argv: print (hyphenate_yale_syl_list(jyutping_to_yale_u8(jyutping))+"#"+superscript_digits_HTML(hyphenate_ping_or_lau_syl_list(jyutping_to_lau(jyutping))))
      elif "--yale#lau#ping" in sys.argv: print (hyphenate_yale_syl_list(jyutping_to_yale_u8(jyutping))+"#"+superscript_digits_HTML(hyphenate_ping_or_lau_syl_list(jyutping_to_lau(jyutping)))+"#"+jyutping.replace(' ',''))
      elif "--yale" in sys.argv: print (hyphenate_yale_syl_list(jyutping_to_yale_u8(jyutping)))
      else: print (superscript_digits_HTML(hyphenate_ping_or_lau_syl_list(jyutping_to_lau(jyutping))))

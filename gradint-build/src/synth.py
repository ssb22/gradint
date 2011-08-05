# This file is part of the source code of
# gradint v0.9978 (c) 2002-2011 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of synth.py - drive various speech synthesizers

def quickGuess(letters,lettersPerSec): return math.ceil(letters*1.0/lettersPerSec)

class Synth(object):
    # Subclasses need to re-implement these:
    def supports_language(self,lang): return 0
    def not_so_good_at(self,lang): return 0
    def works_on_this_platform(self): return 0
    # def guess_length(self,lang,text) - MUST define this.
    # OPTIONAL def play(self,lang,text) play in realtime, returns a non-(False,0,None) value on error
    # OPTIONAL def makefile(self,lang,text) return unique filename (doesn't have to be ready yet) + finish_makefile(self) (ensure all files ready (may get more synth requests later))
    # (at least one of the above must be defined; if don't define the second then can't use this synth offline)
    # Remember to include it in all_synth_classes below
    ################## don't have to re-implement below
    def __init__(self): self.fileCache = {}
    def __del__(self):
        import os # as it might already have been gc'd
        for v in self.fileCache.values():
            try: os.remove(v)
            except: pass # someone may have removed it already, e.g. cache-synth.py's renaming
    def makefile_cached(self,lang,text):
        if type(text)==type([]): textKey=repr(text)
        else: textKey=text
        if (lang,textKey) in self.fileCache: return self.fileCache[(lang,textKey)]
        t = self.makefile(lang,text)
        self.fileCache[(lang,textKey)] = t
        return t
    def finish_makefile(self): pass
    def transliterate(self,lang,text,forPartials=1): return None # could return a transliteration for the GUI if you want (forPartials is 1 if the translit. is for synth from partials, 0 if is for GUI - may not translit. quite so aggressively in the latter case - but NB if partials are used then the GUI will show them instead of calling with 0)
    def can_transliterate(self,lang): return 0

try:
    import warnings
    warnings.filterwarnings("ignore","tempnam is a potential security risk to your program")
except ImportError: pass

def unzip_and_delete(f,specificFiles="",ignore_fail=0):
    if ignore_fail:
        # we had better at least check that the unzip command exists
        if not got_program("unzip"):
            show_warning("Please unzip "+f+" (Gradint cannot unzip it for you as there's no 'unzip' program on this system)")
            return 1
    show_info("Attempting to extract %s, please wait\n" % (f,))
    if os.system("unzip -uo "+f+" "+specificFiles) and not ignore_fail:
        show_warning("Warning: Failed to unzip "+f)
        return 0
    else:
        # unzip seemed to work
        os.remove(f)
        show_info(f+" unpacked successfully\n")
        return 1

class OSXSynth_Say(Synth):
    def __init__(self): Synth.__init__(self)
    def works_on_this_platform(self):
        if not (macsound and fileExists("/usr/bin/say")): return False
        self.voices = self.scanVoices() ; return True
    def supports_language(self,lang): return lang in self.voices
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("say %s\"%s\"" % (self.voices[lang],text.replace('"','')))
    # TODO 10.7+ may also support -r rate (WPM), make that configurable in advanced.txt ?
    def makefile(self,lang,text):
        fname = os.tempnam()+extsep+"aiff"
        system("say -o %s %s\"%s\"" % (fname,self.voices[lang],text.replace('"','')))
        return aiff2wav(fname)
    def scanVoices(self):
        d = {}
        try: from AppKit import NSSpeechSynthesizer
        except: return {"en":""} # no -v parameter at all
        for vocId in NSSpeechSynthesizer.availableVoices():
            vocAttrib = NSSpeechSynthesizer.attributesForVoice_(vocId)
            lang = vocAttrib['VoiceLanguage']
            if lang.startswith("en-"): lang="en" # TODO do any others need hyphen dropping?  careful / check 10.7's Cantonese etc
            if not lang in d: d[lang]=[]
            d[lang].append(vocAttrib['VoiceName'].encode('utf-8'))
        found=0
        for k,v in d.items()[:]:
            if k in macVoices:
                for m in macVoices[k].split():
                    if m in v:
                        d[k] = [m] ; found=1 ; break
            if len(d[k])>1: d[k]=[d[k][0]]
        if d.keys()==['en'] and not found: return {"en":""} # just use the default
        for k,v in d.items()[:]: d[k]='-v "'+v[0]+'" '
        return d

def aiff2wav(fname):
    if not system("sox \"%s\" \"%s\"" % (fname,fname[:-4]+"wav")):
        # good, we converted it to wav
        os.remove(fname)
        fname=fname[:-4]+"wav"
    # else just return aiff and hope for the best (TODO won't work with cache-synth)
    return fname

class OSXSynth_OSAScript(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return macsound and fileExists("/usr/bin/osascript")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    # def play(self,lang,text): os.popen("osascript","w").write('say "%s"\n' % (text,)) # better not have the realtime one because osascript can introduce a 2-3second delay (and newer machines will not be using this class anyway; they'll be using OSXSynth_Say)
    def makefile(self,lang,text):
        fname = os.tempnam()+extsep+"aiff"
        os.popen("osascript","w").write('say "%s" saving to "%s"\n' % (text,fname))
        return aiff2wav(fname)
# TODO: if the user has installed an OS X voice that supports another language, can use say -v voicename  ( or 'using \"voicename\"' for the osascript version )  (but I have no access to a suitably-configured Mac for testing this)

class OldRiscosSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return riscos_sound and not os.system("sayw .")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("sayw %s" % (text,))

class S60Synth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en" # (audio.say always uses English even when other languages are installed on the device)
    def works_on_this_platform(self): return appuifw and hasattr(audio,"say")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text):
        if not text=="Error in graddint program.": # (just in case it's unclear)
          if text.endswith(';'): doLabel(text[:-1])
          else: doLabel(text)
        audio.say(text)

if winsound or mingw32: toNull=" > nul"
else: toNull=" >/dev/null" # stdout only, not stderr, because we want to see any errors that happen

def ensure_unicode(text):
    if type(text)==type(u""): return text
    else:
        try: return unicode(text,"utf-8")
        except UnicodeDecodeError: raise Exception("problem decoding "+repr(text))

class PttsSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.program=None
        self.offlineOnly = False
        if ptts_program: self.program=ptts_program
        elif not winsound and not mingw32 and not cygwin: return
        # You can rename ptts.exe to ptts-offline.exe as a hack if you think your SAPI works only when generating words offline but not for actually playing them.  This is no longer documented in vocab.txt because usually if the system is that broken then it won't work offline either.
        if not self.program:
          for i in ["ptts.exe","ptts-offline.exe"]:
            if fileExists(i):
                # must keep the full path even on non-cygwin because we're adding ,1 to changeToDirOf (hope we don't hit a Windows version that doesn't like this).  But we can keep relative paths if tempdir_is_curdir. (TODO if this breaks when not tempdir_is_curdir, could try copying ptts.exe to temp, but would need to delete it afterwards)
                if cygwin or not tempdir_is_curdir: self.program='"'+os.getcwd()+cwd_addSep+i+'"'
                else: self.program = i
                self.offlineOnly = 'offline' in i
                break
        if not self.program:
            # (in case someone's running on Windows from source)
            show_warning("Warning: ptts.exe not found (required for SAPI 5 speech) - get it from the Windows gradint distribution (or elsewhere)")
        if cygwin: self.lily_file = win2cygwin(lily_file)
        else: self.lily_file = lily_file
        if fileExists(self.lily_file):
            self.old_lily_data=read(self.lily_file)
            if "zh" in sapiVoices and sapiVoices["zh"][0].lower()=="vw lily": del sapiVoices["zh"] # because we don't want to bypass our own interface to lily if a user set that without realising it's not needed
        else: self.lily_file = None
    def supports_language(self,lang): return lang in sapiVoices or lang=="en" or (self.lily_file and lang=="zh")
    # Voice list: os.popen("echo | "+self.program+" -vl").read().split("\n").  If any .lower() contain "espeak-" then after the "-" is an espeak language code see ESpeakSynth (it may not want unicode).  Other voices may also have support for specific languages - may sometimes be able to use <lang langid="locale-hex-code"/> (e.g. 809 UK, 804 Chinese (PRC) 404 Taiwan, 411 Japan) but no way for gradint to tell if successful
    def works_on_this_platform(self): return self.program
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate, especially if they're going to set the speed in the control panel!
    def play(self,lang,text):
        if self.offlineOnly: return SampleEvent(self.makefile_cached(lang,text)).play()
        if lang in sapiVoices:
            d=os.getcwd()
            ret=self.sapi_unicode(sapiVoices[lang][0],ensure_unicode(text),speed=sapiSpeeds.get(lang,None))
            os.chdir(d) ; return ret
        elif lang=='en':
            p=os.popen(self.program+self.speedParam(sapiSpeeds.get(lang,None))+toNull,"w")
            p.write(text+"\n")
            return p.close()
        elif lang=='zh':
            d=os.getcwd()
            ret=self.sapi_unicode("VW Lily",self.preparePinyinPhrase(text),speed=sapiSpeeds.get(lang,None))
            self.restore_lily_dict()
            os.chdir(d) ; return ret
    def sapi_unicode(self,voice,unicode_string,toFile=None,sampleRate=None,speed=None):
        # Speaks unicode_string in 'voice'.  toFile (if present) must be something that was returned by tempnam.  May change the current directory.
        if voice=="Ekho Cantonese": unicode_string = preprocess_chinese_numbers(fix_compatibility(unicode_string),isCant=2) # hack to duplicate the functionality of EkhoSynth
        unifile=os.tempnam() ; open(unifile,"wb").write(codecs.utf_16_encode(unicode_string)[0])
        if not toFile: extra=""
        else:
            extra=' -w '+changeToDirOf(toFile,1)+' -c 1'
            if sampleRate: extra += (' -s '+str(sampleRate))
        ret=system(self.program+' -u '+changeToDirOf(unifile,1)+' -voice "'+voice+'"'+extra+self.speedParam(speed)+toNull) # (both changeToDirOf will give same directory because both from tempnam)
        os.unlink(unifile) ; return ret
    def speedParam(self,speed):
        if speed: return " -r "+str(speed)
        else: return ""
    def makefile(self,lang,text):
        fname = os.tempnam()+dotwav
        oldcwd=os.getcwd()
        if lang in sapiVoices: self.sapi_unicode(sapiVoices[lang][0],ensure_unicode(text),fname,sapiVoices[lang][1],speed=sapiSpeeds.get(lang,None))
        elif lang=="en": os.popen(self.program+' -c 1 -w '+changeToDirOf(fname,1)+self.speedParam(sapiSpeeds.get(lang,None))+toNull,"w").write(text+"\n") # (can specify mono but can't specify sample rate if it wasn't mentioned in sapiVoices - might make en synth-cache bigger than necessary but otherwise no great problem)
        elif lang=='zh':
            self.sapi_unicode("VW Lily",self.preparePinyinPhrase(text),fname,16000,speed=sapiSpeeds.get(lang,None))
            self.restore_lily_dict()
        os.chdir(oldcwd)
        d = sapi_sox_bug_workaround(read(fname)); open(fname,"wb").write(d)
        if cygwin: os.system("chmod -x '"+fname+"'")
        return fname
    def preparePinyinPhrase(self,pinyin):
        def stripPunc(p,even_full_stop=1): # because synth won't like punctuation in the dictionary entries
            toStrip=',?;":\'!' # (see note below re hyphens)
            if even_full_stop: toStrip+='.'
            for punc in toStrip: p=p.replace(punc,"")
            return p
        if __name__=="__main__": pinyin=stripPunc(pinyin,0) # (if not running as a library, strip ALL punctuation ANYWAY, because the voice can pause a bit long) (but don't strip full stops)
        # Split it into words to avoid it getting too long
        # (max 30 chars in a word, max 30 syllables & 240 bytes in its definition, no duplicate entries.  Splitting into words should be OK, but perhaps had better make sure the words on the left don't get too long in case the user omits spaces.)
        pinyin=ensure_unicode(pinyin) # allow existing hanzi as well (TODO also allow/convert unicode tone marks)
        # mark all existing hanzi with @ :
        i=0
        while i<len(pinyin):
            if ord(pinyin[i])>128:
                pinyin=pinyin[:i]+" @"+pinyin[i]+" "+pinyin[i+1:]
                i+=4
            else: i+=1
        pinyin=pinyin.replace("na4",u' @\u637a ').replace("yong4",u' @\u7528 ') # bug workarounds (sometimes na4 is pronounced as nei4 if left as pinyin, etc) (TODO it sometimes still is, whatever character we set it to, e.g. if 'na4 ge5 [cz..]' - it might be right; what are the rules anyway?)
        pinyin=pinyin.split()
        rVal=[]; dicWrite=[]; count=0
        for p in pinyin:
            if p.startswith('@') or (not '1' in p and not '2' in p and not '3' in p and not '4' in p and not '5' in p): # it's the hanzi we added, or it's not a pinyin word, so don't add it to the dictionary
                if not p.startswith('@'): # it's an english word
                    if True in map(lambda x: 'a'<=x<='z',list(p.lower())): show_warning("NOTE: Lily will synthesize '"+p+"' as English because there are no digits 1-5")
                    if rVal and not '_' in rVal[-1] and not rVal[-1].startswith('@'): rVal.append(' ') # 2 English words
                rVal.append(p)
                continue
            p2=stripPunc(p)
            kVal="_%d" % count ; count += 1 # better not make kVal too long otherwise the voice can insert awkward pauses
            dicWrite.append('"%s","%s","p"\r\n' % (kVal,p2))
            rVal.append(p.replace(p2,kVal)) # (leave in full stops etc; assumes p2 is a substring of p, which is why hyphens are taken out before stripPunc)
        open(self.lily_file,"wb").write(''.join(dicWrite))
        return ''.join(rVal).replace('@','') # (WITHOUT spaces, otherwise pauses far too much)
    def restore_lily_dict(self): open(self.lily_file,"wb").write(self.old_lily_data) # done ASAP rather than on finalise, because need to make sure it happens (don't leave the system in an inconsistent state for long)
def sapi_sox_bug_workaround(wavdata):
    # SAPI writes an 'EVNT' block after the sound data, and some versions of sox don't recognise this.  NB this hack is not very portable (relies on SAPI5 guaranteeing to write exactly one EVNT chunk and the bytes 'EVNT' never occur inside it, otherwise would need proper parsing)
    f=wavdata.rfind("EVNT")
    if f>-1: return wavdata[:f]
    else: return wavdata
py_final_letters="aeginouvrAEGINOUVR:" # (don't just pick up on tone numbers, but on numbers after finals, otherwise will have trouble if there's numeric input)
def sort_out_pinyin_3rd_tones(pinyin):
    # Tone sandhi blocking rules: Need to stop 3rd-tones sortout at end of any 2-syllable word + "gei3 ni3" + "wo3 xiang3".
    # Also need to stop at phrase breaks and any English word (or hanzi, although may get awkward cases with 3rd-tone hanzi mixed with pinyin, but that's no big worry as lily isn't too reliable anyway and with partials it'll be transliterated)
    segments = [] ; thisSeg = "" ; syls = 0
    def endsWithSpecialWordpair(segLower): return segLower.endswith("gei3 ni3") or segLower.endswith("gei3 wo3") or segLower.endswith("ni3 xiang3") or segLower.endswith("wo3 xiang3")
    for c in pinyin:
        if ord(c)>128 or c in ".,?;" or (c==" " and syls==2) or endsWithSpecialWordpair(thisSeg.lower()):
            segments.append(thisSeg) ; thisSeg="" ; syls = 0
        elif c==" ": syls = 0
        elif c in "12345": syls += 1
        thisSeg += c
    segments.append(thisSeg)
    # Now go for each segment
    ret = []
    for seg in segments:
      i=0
      while i<len(seg):
        while i<len(seg) and seg[i] not in '12345': i+=1
        if i<len(seg) and seg[i]=='3' and i and seg[i-1] in py_final_letters:
            toneToChange = i ; numThirdsAfter = 0
            j = i
            while True:
                j += 1
                while j<len(seg) and seg[j] not in '12345': j+=1
                if j<len(seg) and seg[j]=='3' and seg[j-1] in py_final_letters: numThirdsAfter+=1
                else: break
            if numThirdsAfter % 2: seg=seg[:toneToChange]+'2'+seg[toneToChange+1:]
        i += 1
      ret.append(seg)
    return "".join(ret)

class FliteSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return got_program("flite")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("flite -t \"%s\"" % (text.replace('"',''),))
    def makefile(self,lang,text):
        fname = os.tempnam()+dotwav
        system("flite -t \"%s\" -o \"%s\"" % (text,fname))
        return fname
if winsound or mingw32 or cygwin: del FliteSynth.play # because on some (even high-spec) systems flite.exe gets intermittently stuck when playing in realtime.  Safer just to generate everything offline.

if macsound:
    # See if we need to unpack eSpeak and/or set the variables
    import commands
    f=commands.getoutput("echo espeak*-OSX.zip")
    if fileExists(f): unzip_and_delete(f)
    f=commands.getoutput("echo espeak*/speak")
    if fileExists(f) and fileExists(f[:-5]+"espeak-data/phontab"):
      os.environ["ESPEAK_DATA_PATH"]=os.getcwd()+cwd_addSep+f[:-6]
      os.environ["PATH"]=os.getcwd()+cwd_addSep+f[:-6]+":"+os.environ["PATH"]
elif winsound or mingw32 or cygwin:
    # See if we need to set the variables for eSpeak
    # (you can unpack it in the current directory or the espeak subdirectory, but not espeak-N.N )
    for dir in [".","espeak"]:
        if fileExists(dir+os.sep+"espeak-data"+os.sep+"phontab"):
            os.environ["ESPEAK_DATA_PATH"] = os.getcwd()+cwd_addSep+dir
            break

# If you are using the eSpeak speech synthesizer, you can
# optionally define a Python dictionary espeak_language_aliases
# that maps your language abbreviations onto eSpeak's, so
# that gradint will recognise yours as an alternative to eSpeak's.
# For example the following will cause "cant" to be a valid
# alternative to "zhy" when specifying a language for synthesized text
# in espeak (or when using synth partials).
espeak_language_aliases = { "cant":"zhy" }
# TODO does the above need to be moved to advanced.txt?
# (maybe not as 'cant' is probably the only example for now)

class SimpleZhTransliterator(object): # if not got eSpeak on system
    def can_transliterate(self,lang): return lang=="zh"
    def transliterate(self,lang,text,forPartials=1,from_espeak=0):
        if lang=="zh" and not text.find("</")>-1: # (not </ - don't do this if got SSML)
            text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode("utf-8")
            found=0
            for t in text:
                if ord(t)>=128:
                    found=1 ; break
            if not found and text.lower()==fix_pinyin(text,[]): return text # don't need espeak
            elif from_espeak: return [text] # This transliterate() and ESpeakSynth's transliterate() work together - don't call espeak if there aren't any special characters (this saves launching a lot of espeak processes unnecessarily when synthing from partials), but DO proceed if fix_pinyin changes something, as in this case we need to check for embedded en words so fix_pinyin doesn't add spurious 5's, + embedded letters etc.
            elif not found: return fix_pinyin(text,[]) # No ESpeak on system and fix_pinyin needed to do something - best we can do is hope there aren't any embedded English words (because if there are, they'll have spurious 5's added)
simpleZhTransliterator = SimpleZhTransliterator()

def shell_escape(text):
    text = text.replace('\\','\\\\').replace('"','\\"')
    if unix: text=text.replace("$","\\$").replace("`","\\`").replace("!","! ")
    return '"'+text+'"'

espeakTranslitCacheFile = "espeak-translit-cache"+extsep+"bin" # TODO to advanced.txt?
class ESpeakSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.languages = {} ; self.program=""
        tryList = []
        if riscos_sound and 'eSpeak$dir' in os.environ: tryList=[os.environ['eSpeak$dir']+'.espeak-dat',os.environ['eSpeak$dir']+'.espeak-data']
        elif winsound or mingw32: tryList=[programFiles+"\\eSpeak\\espeak-data"]
        elif winCEsound: tryList=["\\espeak-data"] # Can't try \\Storage Card because our eSpeak compile can't cope with spaces (and quoting it does not work)
        else:
            tryList=[os.environ.get("HOME","")+"espeak-data","/usr/share/espeak-data","/usr/local/share/espeak-data"]
            if cygwin: tryList.append(programFiles+"/eSpeak/espeak-data")
        if os.environ.get("ESPEAK_DATA_PATH",""): tryList.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"espeak-data")
        langList = []
        for tryplace in tryList:
            try:
                self.place = tryplace
                langList = os.listdir(self.place+os.sep+"voices")
            except: self.place = None
            if langList: break
        for l in langList[:]:
            if l in ["default","!v","mb"]: langList.remove(l)
            elif isDirectory(self.place+os.sep+"voices"+os.sep+l):
                for ll in os.listdir(self.place+os.sep+"voices"+os.sep+l):
                    self._add_lang(ll,l+os.sep+ll)
            else: self._add_lang(l,l)
        self.theProcess = None
        self.translitCache = {}
        if pickle and fileExists(espeakTranslitCacheFile):
            try: placeStat,tc = pickle.Unpickler(open(espeakTranslitCacheFile,"rb")).load()
            except: placeStat,tc = (),{}
            if placeStat==tuple(os.stat(self.place)): self.translitCache = tc # otherwise regenerate it because eSpeak installation has changed (TODO if you overwrite an existing _dict file in-place, it might not update the stat() of espeak-data and the cache might not be re-generated when it should; espeak's --compile seems ok though)
        if self.place: self.place=self.place[:self.place.rindex(os.sep)] # drop the \espeak-data, so can be used in --path=
    def _add_lang(self,lang,fname):
        if "~" in lang: return # emacs backup files
        self.languages[lang]=fname
        for l in open(self.place+os.sep+"voices"+os.sep+fname).read(256).replace("\r","\n").split("\n"):
            if l.startswith("language "):
                l=l[9:].strip(wsp)
                if not l==lang:
                    if l in espeak_language_aliases.values(): # aliasing to an alias - update it
                        for k,v in espeak_language_aliases.items():
                            if v==l: espeak_language_aliases[k]=lang
                    espeak_language_aliases[l] = lang
    def describe_supported_languages(self):
        ret=[]
        items=self.languages.items() ; items.sort()
        for k,v in items:
            if "-" in k and not k=="zh-yue": continue # skip variants in the report (but do recognise them)
            o=open(self.place+os.sep+"espeak-data"+os.sep+"voices"+os.sep+v)
            line=""
            for t in range(10):
                line=o.readline()
                if line.find("name")>-1:
                    lname = line.split()[1].replace("_test","").replace("-test","").replace("-experimental","").replace("-expertimental","") # (delete the -test etc for more screen real-estate, as this is used only for explaining what the language abbreviations mean)
                    if not lname: continue
                    lname=lname[0].upper()+lname[1:]
                    ret.append(k+"="+lname)
                    break
        return " ".join(ret)
    def supports_language(self,lang): return espeak_language_aliases.get(lang,lang) in self.languages
    def not_so_good_at(self,lang): return lang not in prefer_espeak
    def works_on_this_platform(self):
        if len(self.languages.items())==0: return 0
        if winCEsound:
            for d in ["","\\Storage Card"]: # TODO check other language versions of Windows Mobile
                if fileExists(d+"\\bin\\speak"):
                    self.program = d+"\\bin\\speak" ; return True
            return False
        elif winsound or mingw32: toTry=[programFiles.replace("Program Files","progra~1")+"\\eSpeak\\command_line\\espeak.exe"] # progra~1 because "C:\Program Files" in os.system doesn't always work despite the quotes
        elif cygwin: toTry=[programFiles+"/eSpeak/command_line/espeak.exe"]
        else: toTry = []
        if toTry: # windows or cygwin
            if "ESPEAK_DATA_PATH" in os.environ:
                toTry.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"espeak.exe")
                toTry.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"command_line"+os.sep+"espeak.exe")
            for t in toTry:
                if fileExists(t):
                    if " " in t: self.program='"'+t+'"'
                    else: self.program = t
                    return True
            return False
        else: # not windows or cygwin
            self.program="speak"
            if riscos_sound: return True # we've already confirmed <eSpeak$dir> works in the constructor
            import commands
            loc=commands.getoutput("locale -a|grep -i 'utf-*8$'|head -1").strip(wsp)
            if loc: loc="LC_CTYPE="+loc+" " # in case espeak can't find a utf-8 locale by itself
            self.program=loc+"speak"
            if got_program("speak"): return True
            # if 'speak' is not available then also check for 'espeak', because some packages install only that:
            self.program = loc+"espeak"
            return got_program("espeak")
    def guess_length(self,lang,text):
        if text.find("</")>-1: # might be SSML - don't count inside <...>
            l=inSsml=0
            for c in text:
                if c=="<": inSsml=1
                elif c==">": inSsml=0
                elif not inSsml: l += 1
        else: l=len(text)
        return quickGuess(l,12)+cond(winCEsound,1.3,0) # TODO need a better estimate.  Overhead on 195MHz Vario (baseline?) >1sec (1.3 seems just about ok)
    def can_transliterate(self,lang): return espeak_language_aliases.get(lang,lang) in ["zh","zhy","zh-yue"] and not riscos_sound # TODO it's OK on RISC OS if the eSpeak version is recent enough to do --phonout=filename; TODO aliases for zhy (but not usually a problem as can_transliterate is called only for preference)
    def winCE_run(self,parameters,expectedOutputFile,infileToDel=None):
        self.winCE_start(parameters)
        time.sleep(0.3) # 0.2 not always long enough for transliterations (get empty output file if try to read too soon, then loop waiting for it to have contents)
        return self.winCE_wait(expectedOutputFile,infileToDel)
    def winCE_start(self,parameters):
        s = ShellExecuteInfo(60,File=u""+self.program,Parameters=u"--path="+self.place+" "+parameters,fMask=0x40)
        ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(s))
        self.hProcess = s.hProcess # TODO check it's not NULL (failed to run)
    def winCE_wait(self,expectedOutputFile,infileToDel=None,needDat=1):
        # won't always work: if app and not app.Label["text"].strip(): app.setLabel("Waiting for eSpeak") # in case it doesn't produce output
        ctypes.cdll.coredll.WaitForSingleObject(self.hProcess,4294967295) # i.e. 0xFFFFFFFF but that throws up a warning on Python 2.3
        ctypes.cdll.coredll.CloseHandle(self.hProcess)
        # In some rare circumstances, that command won't wait (e.g. process hadn't started despite the fact we delayed), so check the output files also.
        # (Leave WaitForSingleObject in as it could save some CPU cycles / potential OS crashes on some WinCE versions)
        firstIter = 2
        while True:
            if firstIter: firstIter -= 1
            else: time.sleep(0.2),check_for_interrupts() # (latter needed in case it gets stuck)
            try:
              if needDat: dat=read(u""+expectedOutputFile)
              else: dat=open(u""+expectedOutputFile).read(8)
            except: continue # error on trying to read output
            if not dat: continue # output read as empty
            if expectedOutputFile.endswith(dotwav) and (len(dat)<8 or dat[6:8]=="\xff\x7f"): continue # length field not yet written
            # (TODO how could we make sure a long transliteration has finished, if the OS lets us open the file before done and if WaitForSingleObject doesn't work?)
            if not firstIter: time.sleep(0.2) # just in case
            if infileToDel:
                try: os.unlink(infileToDel)
                except: continue # still got the input file open
            return dat
    def update_translit_cache(self,lang,textList): # forPartials=1 assumed
        if not lang=="zh": return # TODO if expand 'transliterate' to do other languages, make sure to update this also, and the cache format
        if self.translitCache: textList=filter(lambda x:x not in self.translitCache, textList)
        step = 1000 # should be about right?
        for i in range(0,len(textList),step):
            tl = textList[i:i+step]
            tlr = self.transliterate_multiple(lang,tl,keepIndexList=1)
            if not tlr: return # espeak's not up to it
            for i in self.lastIndexList: self.translitCache[tl[i]]=tlr[i]
            if winCEsound: ctypes.cdll.coredll.SystemIdleTimerReset() # TODO here may not be often enough if auto-switchoff is an especially short time and/or CPU is especially slow (but then plugging it into external power would probably be best anyway)
        if textList:
            try: pickle.Pickler(open(espeakTranslitCacheFile,"wb"),-1).dump((tuple(os.stat(self.place+os.sep+"espeak-data")),self.translitCache))
            except IOError: pass # 'permission denied' is ok
    def transliterate(self,lang,text,forPartials=1):
        if lang=="zh" and text in self.translitCache: return self.translitCache[text] # (TODO add "and forPartials"? but don't need to bother with this extra condition on slow systems)
        return self.transliterate_multiple(lang,[text],forPartials)[0] # and don't cache it - could be experimental, and we don't want cache to grow indefinitely
    def transliterate_multiple(self,lang,textList,forPartials=1,keepIndexList=0):
      # Call eSpeak once for multiple transliterations, for greater efficiency (especially on systems where launching a process is expensive e.g. WinCE).
      # Note: Don't make textList TOO long, because the resulting data must fit on the (RAM)disk and in memory.
      retList = [] ; write_to_espeak = [] ; indexList = []
      split_token = "^^^" # must be something not defined in the _rules files
      for text in textList: # DON'T escape_jyutping (treat as en words)
        if lang=="zh":
         if keepIndexList: # making the cache - can we go a bit faster?
           try: t = unicode(text,"ascii") # if no utf, know is OK (but ONLY if keepIndexList, as the result is imprecise)
           except UnicodeDecodeError: t = simpleZhTransliterator.transliterate(lang,text,from_espeak=1)
         else: t = simpleZhTransliterator.transliterate(lang,text,from_espeak=1)
        else: t=[fix_compatibility(ensure_unicode(text)).encode("utf-8")]
        if t and not riscos_sound: # same TODO as above re RISC OS
            if type(t)==type([]):
                indexList.append(len(retList))
                retList.append(None) # result not filled in yet
                if lang=="zh": tt=pinyin_uColon_to_V(t[0].replace("-","/")) # NB fix_compatibility has already been done (as has preprocess_chinese_numbers), by simpleZhTransliterator above
                else: tt=t[0]
                write_to_espeak.append(fix_commas(tt).replace(split_token," "))
                # (replacing - with / because espeak zh voice treats / as a silent word separator but - is ignored; - is used as a word separator in MeiLing etc.  so if you want to write the hanzi for wei2ren2 but you want it to be wei4+ren2, you can hack in this way.  TODO document?)
            else: retList.append(t)
        else: retList.append(None)
      if keepIndexList: self.lastIndexList = indexList
      if not indexList: return retList
      fname = os.tempnam()
      open(fname,"w").write((".\n"+split_token+" ").join(write_to_espeak))
      oldcwd=os.getcwd()
      if winCEsound:
          translit_out = os.tempnam()
          data=self.winCE_run(' -v%s -q -X -f %s --phonout=%s' % (espeak_language_aliases.get(lang,lang),fname,translit_out),translit_out)
          os.remove(translit_out)
      else: data=os.popen(self.program+' -v%s -q -X -f %s%s' % (espeak_language_aliases.get(lang,lang),changeToDirOf(fname,1),cond(unix," 2>&1","")),"rb").read() # popen2 might not work, so had better do it this way:
      os.chdir(oldcwd) ; os.remove(fname)
      data = data.replace("\r\n","\n").split("\nTranslate '"+split_token+"'\n")
      if len(data)==2*len(indexList)-1:
        # split points are doubled - better take every ODD item.  (NB the text in between is NOT necessarily blank - espeak can flush its sentence cache there)
        d2 = []
        for i in xrange(0,len(data),2): d2.append(data[i])
        data = d2
      if not len(data)==len(indexList):
          if not (winsound or macsound): show_warning("Warning: eSpeak's transliterate returned wrong number of items (%d instead of %d).  Falling back to separate runs for each item (slower)." % (len(data),len(indexList)))
          return None
      for index,dat in zip(indexList,data):
          en_words={} # any en words that espeak found embedded in the text
          r=[] ; lastWasBlank=False
          delete_last_r_if_blank = 0
          thisgroup_max_priority,thisgroup_enWord_priority = 0.5,0
          for l in dat.strip(wsp).split("\n"):
              # get en_words for fix_pinyin (and for making sure we embed them in cant)
              lWords = l.split()
              if lWords: int0 = intor0(lWords[0])
              else: int0 = 0
              if int0:
                  if int0 > thisgroup_max_priority:
                      thisgroup_max_priority = int0
                      if lWords[-1]=="[_^_]": thisgroup_enWord_priority = int0 # so far it looks like this is going to be an English word
              else: # a split between the groups
                  if thisgroup_enWord_priority == thisgroup_max_priority: # the choice with the highest priority was the one containing the [_^_] to put the word into English
                      en_words[r[-1]]=1
                  thisgroup_max_priority,thisgroup_enWord_priority = 0.5,0
              # end of getting en_words
              if lang=="zh" and not lastWasBlank and r and (l.startswith("Replace") or l.startswith("Translate") or l.startswith("Found")): r[-1]+="," # (because not-blank is probably the line of phonemes)
              elif not lang=="zh" and l.startswith("_|") and r: r[-1] += "," # works for zh-yue
              if delete_last_r_if_blank and not l: r=r[:-1] # "Translate" followed by blank line is probably corner-brackets or something; don't want that confusing the transliteration (especially if it's for partials)
              delete_last_r_if_blank = 0
              foundLetter=0
              if l.startswith("Translate "):
                  toAppend=l[l.index("'")+1:-1].replace("\xc3\xbc","v")
                  if not (toAppend in en_words and r and toAppend==r[-1]):
                    # TODO what about partial English words? e.g. try "kao3 testing" - translate 'testing' results in a translate of 'test' also (which assumes it's already in en mode), resulting in a spurious word "test" added to the text box; not sure how to pick this up without parsing the original text and comparing with the Replace rules that occurred
                    r.append(toAppend)
                    delete_last_r_if_blank = 1
                  else: en_words[toAppend]=1
              else: # not Translate
                  if lang=="zh" and l.startswith("Found: ") and ((l[7]==l[9]=="'" and "a"<=l[8]<="z") or (l[8]==" " and "a"<=l[7]<="z")): # an alphabetical letter - we can say this as a Chinese letter and it should be compatible with more partials-based synths.  But DON'T do this if going to give it to a unit-selection synth - 'me1' and 'ne1' don't have hanzi and some synths will have difficulty saying them.
                      if l[8]==' ': letter=l[7]
                      else: letter=l[8]
                      if forPartials: r.append("a1 bo1 ci1 de1 e1 fou1 ge1 he1 yi1 ji1 ke1 le1 me1 ne1 wo1 po1 qi1 ri4 si1 te4 yu1 wei4 wu1 xi1 ye1 zi1".split()[ord(letter)-ord('a')])
                      else: r.append(letter)
                      foundLetter = 1
                  elif not lang=="zh" and l.startswith("Found: ") and (ord(l[7])>127 or (l[7]=="'" and ord(l[8])>127)): # (espeak 1.40 puts in l[7], 1.44 surrounds in quotes)
                      r.append(l[l.index("[")+1:l.index("]")])
              lastWasBlank=(l.startswith("Replace") or not l or foundLetter) # (take 'Replace' lines as blank, so 'Translate' doesn't add a second comma.  ditto letters thing.)
          while r and r[-1] and r[-1][-1]==',': r[-1]=r[-1][:-1] # strip any trailing commas
          if lang=="zh": retList[index]=fix_pinyin(" ".join(r),en_words)
          else: retList[index]=" ".join(r)
      return retList
    def escape_jyutping(self,text): return re.sub(r"([abcdefghjklmnopstuwz][a-z]*[1-7])",r"[[\1]]",text) # TODO what if user already escaped it?
    def play(self,lang,text):
        if espeak_language_aliases.get(lang,lang) in ["zhy","zh-yue"]: text=self.escape_jyutping(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=1).encode("utf-8"))
        elif lang=="zh": text=fix_commas(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode('utf-8'))
        if winCEsound: # need to play via makefile, and careful not to leave too many tempfiles or take too long
            ret = 0
            if len(text)>15: # not a short phrase - let's split it up
                l = [] ; pos=0
                for i in xrange(len(text)-1):
                    if text[i] in ",.;!?" and text[i+1]==" " and i-pos>20: # (don't split TOO short)
                        l.append(text[pos:i+1])
                        pos = i+2
                if pos<len(text): l.append(text[pos:])
                text = l
            else: text=[text]
            try:
              for i in range(len(text)):
                f=self.makefile(lang,text[i])
                if len(text)>5: doLabel("("+str(int(100*i/len(text)))+"%)")
                if i<len(text)-1: self.makefile(lang,text[i+1],1) # give it a hint about the next phrase
                ret = SampleEvent(f,isTemp=1).play() # TODO ret is not checked unless it's the last one (but should be OK for short in-lesson phrases, and 'ret' might not show up the errors anyway)
                if emulated_interruptMain: check_for_interrupts()
                ctypes.cdll.coredll.SystemIdleTimerReset()
            finally:
              if hasattr(self,"winCEhint"): os.unlink(self.makefile(lang,"")) # make sure to clean up on interrupt
            return ret
        elif winsound or mingw32 or cygwin:
            # Windows command line is not always 100% UTF-8 safe, so we'd better use a pipe.  (Command line ok on other platforms, and must do it on riscos - no pipes.)  (espeak_pipe_through only needs supporting on non-Windows - it's for aplay etc)
            p=os.popen(self.program+cond(text.find("</")>-1," -m","")+' -v%s -a%d' % (espeak_language_aliases.get(lang,lang),100*soundVolume),"wb")
            p.write(text+"\n") ; return p.close()
        else: return system(self.program+cond(text.find("</")>-1," -m","")+' -v%s -a%d %s %s' % (espeak_language_aliases.get(lang,lang),100*soundVolume,shell_escape(text),espeak_pipe_through)) # (-m so accepts SSML tags)
    def makefile(self,lang,text,is_winCEhint=0):
        if espeak_language_aliases.get(lang,lang) in ["zhy","zh-yue"]: text=self.escape_jyutping(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=1).encode("utf-8"))
        elif lang=="zh": text=fix_commas(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode('utf-8'))
        if hasattr(self,"winCEhint"): # waiting for a previous async one that was started with is_winCEhint=1
            fname,fnameIn = self.winCEhint
            del self.winCEhint
            self.winCE_wait(fname,fnameIn,needDat=0)
            return fname
        fname = os.tempnam()+dotwav
        oldcwd=os.getcwd()
        sysCommand = cond(winCEsound,"",self.program)+cond(text.find("</")>-1," -m","")+' -w %s -v%s' % (changeToDirOf(fname,1),espeak_language_aliases.get(lang,lang))
        # (eSpeak wavs are 22.05k 16-bit mono; not much point down-sampling to 16k to save 30% storage at expense of CPU)
        if winsound or mingw32: os.popen(sysCommand,"w").write(text+"\n") # must pipe the text in
        elif riscos_sound: os.system(sysCommand+' '+shell_escape(text))
        elif winCEsound:
            fnameIn = os.tempnam() ; open(fnameIn,"w").write(text)
            if is_winCEhint:
                self.winCEhint = (fname,fnameIn)
                self.winCE_start(sysCommand+' -f '+fnameIn)
            else: self.winCE_run(sysCommand+' -f '+fnameIn,fname,fnameIn)
        else:
            # we can make it asynchronously
            if cygwin: sysCommand='echo "'+text.replace('"','\\"')+'"|'+sysCommand # (still need to pipe)
            else: sysCommand += (' "'+text.replace('"','\\"')+'"')
            if not self.theProcess: self.theProcess = os.popen("/bin/bash","w")
            self.theProcess.write('cd "'+os.getcwd()+'"\n'+sysCommand+"\n")
            self.theProcess.flush()
        os.chdir(oldcwd)
        return fname
    def finish_makefile(self):
        if self.theProcess: self.theProcess.close()
        self.theProcess = None

def fix_commas(text):
  # some versions of espeak won't honour ordinary commas in among Chinese text if the ordinary commas don't have spaces after
  # also put 2 spaces after full stop, and make sure capitalised
  i=0
  while i<len(text)-1:
    if text[i] in '.,?;!':
      tRest = text[i+1:].strip(wsp)
      if tRest and (ord(tRest[0])>=128 or 'a'<=tRest[0].lower()<='z'):
        text=text[:i+1]+cond(text[i] in ".?!","  "+tRest[0].upper()," "+tRest[0])+tRest[1:]
    i+=1
  return text

def fix_pinyin(pinyin,en_words):
  # fix pinyin numbers in 'wrong' place, e.g. ta4i to tai4 (which can result from espeak being given tone marks or from non-standard user input to the GUI), and add missing 5's
  if en_words:
    ret=[]
    def stripPunc(w):
      i=0 ; j=len(w) ; w=w.lower()
      while i<len(w) and not 'a'<=w[i]<='z': i+=1
      while j>1 and not ('a'<=w[j-1]<='z' or '1'<w[j-1]<='5'): j-=1
      return w[i:j]
    for w in pinyin.split():
      if stripPunc(w) in en_words: ret.append(w)
      else: ret.append(fix_pinyin(w,[]))
    return ' '.join(ret)
  i=0
  pinyin=pinyin_uColon_to_V(pinyin)+"@@@" # (includes .lower; @@@ for termination)
  while i<len(pinyin):
    if pinyin[i] in "12345":
      moveBy=0
      if pinyin[i+1] in "iuv": moveBy=1 # these are never initial letters
      elif pinyin[i+1]=="o" and not pinyin[i+2] in "u12345": moveBy=1 # "o" and "ou" are valid syllables, but a number before "o" is likely to be premature especially if the "o" is not itself followed by a number (or "u")
      elif pinyin[i+1:i+3]=="ng" and not pinyin[i+3] in "aeiouv": moveBy=2 # before an -ng, but NOT before a -n g-(vowel)
      elif pinyin[i+1] in "nr" and not pinyin[i+2] in "aeiouv" and not (pinyin[i+1]=="r" and i and not pinyin[i-1]=="e") and not pinyin[i+1:i+3]=="r5": moveBy=1 # before -n or -r (as final not as initial) (but NB -r is only on -er, otherwise it's an r5.  and if it already says r5, leave it.)
      if moveBy: pinyin=pinyin[:i]+pinyin[i+1:i+moveBy+1]+pinyin[i]+pinyin[i+moveBy+1:]
    i+=1
  i=0
  while i<len(pinyin): # check for missing 5's
    if (pinyin[i] in "aeiouvr" and pinyin[i+1] not in "aeiouv12345") or (ord('a')<=ord(pinyin[i])<=ord('z') and not (ord("a")<=ord(pinyin[i+1])<=ord("z") or pinyin[i+1] in "12345")): # ("alnum and next is not alnum" is not strictly necessary, but we do need to add 5's after en-like words due to 'fix_pinyin(t)==t' being used as a do-we-need-proper-translit. condition in SimpleZhTransliterator, otherwise get problems with things like "c diao4" going to eSpeak when it could go to partials-with-letter-substitutions)
      if pinyin[i+1:i+3]=="ng" and not pinyin[i+3] in "aeiouv":
        if pinyin[i+3] not in "12345": pinyin=pinyin[:i+3]+"5"+pinyin[i+3:]
      elif (pinyin[i+1]=="n" or pinyin[i:i+2]=="er") and not pinyin[i+2] in "aeiouv" and not pinyin[i]=="r":
        if pinyin[i+2] not in "12345": pinyin=pinyin[:i+2]+"5"+pinyin[i+2:]
      else: pinyin=pinyin[:i+1]+"5"+pinyin[i+1:]
    i+=1
  return pinyin[:-3] # remove the @@'s

def remove_tone_numbers(utext): # for hanzi_and_punc to take out numbers that can't be transliterated
    i=1
    while i<len(utext):
        if "1"<=utext[i]<="5" and "a"<=utext[i-1].lower()<="z" and (i==len(utext)-1 or not "0"<=utext[i+1]<="9"): utext=utext[:i]+utext[i+1:]
        i+=1
    return utext
def preprocess_chinese_numbers(utext,isCant=0): # isCant=1 for Cantonese, 2 for hanzi (and if 1 or 2, also assumes input may be jyutping not just pinyin)
    # Hack for reading years digit by digit:
    for year in ["nian2",u"\u5e74"]: # TODO also " nian2" to catch that? what of multiple spaces?
        while utext.find(year)>=4 and 1200 < intor0(utext[utext.find(year)-4:utext.find(year)]) < 2300: # TODO is that range right?
            yrStart = utext.find(year)-4
            utext = utext[:yrStart] + " ".join(list(utext[yrStart:yrStart+4]))+" "+utext[yrStart+4:]
    # End of hack for reading years
    i=0
    while i<len(utext):
        if "0"<=utext[i]<="9" and not ("1"<=utext[i]<=cond(isCant,"7","5") and i and "a"<=utext[i-1].lower()<="z" and (i==len(utext)-1 or not "0"<=utext[i+1]<="9")): # number that isn't a tone digit
            j=i
            while j<len(utext) and utext[j] in "0123456789.": j += 1
            while utext[j-1]==".": j -= 1 # exclude trailing point(s)
            num = read_chinese_number(utext[i:j])
            if isCant:
              for mand,cant in zip("ling2 yi1 er4 san1 si4 wu3 liu4 qi1 ba1 jiu3 dian3 yi4 qian1 bai3 shi2 wan4".split(),cond(isCant==2,u"\u96f6 \u4e00 \u4e8c \u4e09 \u56db \u4e94 \u516d \u4e03 \u516b \u4e5d \u70b9 \u4ebf \u5343 \u767e \u5341 \u4e07","ling4 jat1 ji6 saam7 sei3 ng5 luk6 cat7 baat3 gau2 dim2 jik1 cin7 baak3 sap6 maan6").split()): num=num.replace(mand,cant)
            utext=utext[:i]+num+utext[j:]
            i += len(num)
        else: i += 1
    return utext
def read_chinese_number(num):
    digits="ling2 yi1 er4 san1 si4 wu3 liu4 qi1 ba1 jiu3".split()
    nums=num.split(".")
    if len(nums)==1: # normal number
        columns=("yi4 qian1 bai3 shi2 wan4 qian1 bai3 shi2".split()+[""])
        has_wan = not ("00000000"+num)[-8:-4]=="0000"
        if len(num)>len(columns) or (num and num[0]=="0"): return "".join([digits[ord(d)-ord("0")] for d in num]) # far too many digits, or something starting with 0 - read one at a time
        r=[]
        for d,c,i in zip(list(num),columns[-len(num):],range(len(num))):
            if d=="0":
                if c=="wan4" and has_wan: r.append(c)
                elif c and not (r and r[-1]=="ling2"): r.append("ling2")
                # else nothing
            elif d=="1" and c=="shi2" and (i==0 or (r and r[-1]=="ling2")): r.append(c) # 10, 1010
            else: r.append(digits[ord(d)-ord("0")]+c)
        if len(r)>1 and r[-1]=="ling2": del r[-1] # e.g. 100
        return "".join(r)
    elif len(nums)==2: # read digits after the point one at a time
        rVal = [read_chinese_number(nums[0]),"dian3"]
        for d in nums[1]: rVal.append(digits[ord(d)-ord("0")])
        return "".join(rVal)
    else: return "dian3".join([read_chinese_number(n) for n in nums]) # probably a complex version number

def fix_compatibility(utext): # convert 'compatibility full-width' characters to ASCII, also simplify some quote marks etc
    r = []
    for c in utext:
        if 0xff01<=ord(c)<=0xff5e: r.append(unichr(ord(c)-0xfee0))
        elif 0x2010 <= ord(c) <= 0x2015: r.append("-")
        elif c==unichr(0x201a): r.append(",") # sometimes used as comma (incorrectly)
        elif 0x2018 <= ord(c) <= 0x201f: r.append('"')
        elif c==unichr(0xff61): r.append(".")
        else: r.append(c)
    return u"".join(r)

# Older versions of eSpeak output WAVs with 0 length and can't be piped through aplay
espeak_pipe_through = "" # or "--stdout|..." (NOT on Windows)
def espeak_stdout_works():
    assert unix, "espeak_stdout_works should be called only if unix"
    # recent enough for --stdout to work.  Don't be tempted to look for "zh" in languages
    # because espeak 1.31 shipped with zh (broken) and a broken --stdout (length marked as 0)
    versionLine = (filter(lambda x:x,os.popen("(speak --help||espeak --help) 2>/dev/null").read().split("\n"))+[""])[0]
    versionLine = versionLine[versionLine.find(":")+1:].strip()
    versionLine = versionLine[:versionLine.find(" ")]
    versionLine = (versionLine+".")[:versionLine.find(".",versionLine.find(".")+1)] # if x.y.z just have x.y
    try: return (float(versionLine)>=1.32)
    except ValueError: return False
def espeak_volume_ok():
    # if has "zh", should be recent enough
    return "zh" in ESpeakSynth().languages
if unix and not macsound and not (oss_sound_device=="/dev/sound/dsp" or oss_sound_device=="/dev/dsp"):
    if playProgram=="aplay" and espeak_stdout_works(): espeak_pipe_through="--stdout|aplay -q" # e.g. NSLU2
    else: del ESpeakSynth.play # because we have no way of sending it to the alternative device, so do it via a file
    if hasattr(FliteSynth,"play"): del FliteSynth.play
if hasattr(ESpeakSynth,"play") and (soundVolume<0.04 or (soundVolume<0.1 and not espeak_volume_ok()) or soundVolume>2): del ESpeakSynth.play # old versions of espeak are not very good at less than 10% volume, so generate offline and use sox

# ESpeakSynth's c'tor may modify espeak_language_aliases, and it has to be consistent at the time of partial scanning.  Plus c'tor called too often.  Hack for now:
globalEspeakSynth = ESpeakSynth()
class ESpeakSynth(ESpeakSynth):
    def __init__(self): self.__dict__ = globalEspeakSynth.__dict__

class EkhoSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        if ekho_speed_delta: self.prog="ekho -s %d" % ekho_speed_delta
        else: self.prog="ekho"
    def supports_language(self,lang): return lang in ["zhy","zh-yue","cant"] # not Mandarin unless we can check we have a version of ekho that does 3rd tones correctly
    def works_on_this_platform(self): return got_program("ekho")
    def guess_length(self,lang,text): return quickGuess(len(text),6) # TODO need a better estimate
    def play(self,lang,text):
        text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=2).encode("utf-8")
        infile = os.tempnam()+dottxt ; open(infile,"w").write(text) # Ekho 4.5 takes "-f -" for stdin, but 4.1 can't
        r = system(self.prog+" --voice=Cantonese -f \""+infile+"\"")
        os.remove(infile)
        return r
    def makefile(self,lang,text):
        text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=2).encode("utf-8")
        fname = os.tempnam()+dotwav # TODO can also have dotmp3 (with -t mp3 added), and the resulting mp3 can be smaller than gradint's
        infile = os.tempnam()+dottxt ; open(infile,"w").write(text)
        system(self.prog+" --voice=Cantonese -f \""+infile+"\" -o \""+fname+"\"")
        os.remove(infile)
        return fname

class FestivalSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def startProcess(self):
        self.theProcess = os.popen("festival -i >/dev/null 2>/dev/null","w")
        self.theProcess.write("(Parameter.set 'Audio_Required_Format 'riff)\n(Parameter.set 'Audio_Method 'Audio_Command)\n")
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): # can *assume* this *will* be called, so put the startProcess check here (no need to call this in duplicate from init)
        r=(unix and not macsound and got_program("festival"))
        if r: self.startProcess()
        return r
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    if oss_sound_device:
      def play(self,lang,text):
        if not self.theProcess: self.startProcess()
        self.theProcess.write("(Parameter.set 'Audio_Command \"play --device=%s \$FILE vol %.1f\")\n(tts_text \"%s\" nil)\n" % (oss_sound_device,5*soundVolume,text)) # (tts_text text nil) can be better than (SayText text) because it splits into multiple utterances if necessary
        self.theProcess.flush()
    # else send it via a file, because we haven't got code to give it to play to the other devices directly
    def makefile(self,lang,text):
        if not self.theProcess: self.startProcess()
        fname = os.tempnam()+dotwav
        self.theProcess.write("(Parameter.set 'Audio_Command \"sox \$FILE %s vol 5\")\n(SayText \"%s\")\n" % (fname,text))
        self.theProcess.flush()
        return fname
    def finish_makefile(self):
        if self.theProcess: self.theProcess.close()
        self.theProcess = None

class GeneralSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang):
        for l,c in extra_speech:
            if l==lang: return 1
        return 0
    def works_on_this_platform(self): return extra_speech
    def guess_length(self,lang,text): return quickGuess(len(text),10) # TODO need a better estimate
    def play(self,lang,text):
        for l,c in extra_speech:
            if l==lang: return system('%s %s' % (c,shell_escape(text)))

class GeneralFileSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.letters = {} ; self.duration = {}
    def supports_language(self,lang):
        for l,c,f in extra_speech_tofile:
            if l==lang: return 1
        return 0
    def works_on_this_platform(self): return extra_speech_tofile
    def guess_length(self,lang,text):
        if not lang in self.letters: self.letters[lang]=self.duration[lang]=0
        if self.letters[lang]<25:
            self.letters[lang] += len(text)
            self.duration[lang] += SampleEvent(self.makefile_cached(lang,text)).exactLen
            assert self.duration[lang], "GeneralFileSynth didn't put sound in file?"
        return quickGuess(len(text),self.letters[lang]/self.duration[lang]) # (doing it this way so don't synth the whole list, but do make sure got a big enough sample)
    # (note: above works only because finish_makefile() is not necessary in this class)
    def makefile(self,lang,text):
        for l,c,f in extra_speech_tofile:
            if l==lang:
                if os.system(c % shell_escape(text)): raise Exception("Your extra_speech_tofile command failed on "+repr(text))
                fname = os.tempnam()+extsep+soundFileType(f)
                if unix: os.system('mv "'+f+'" "'+fname+'"') # because os.rename() can throw an exception if renaming cross-device on some systems
                else: os.rename(f,fname)
                return fname

all_synth_classes = [GeneralSynth,GeneralFileSynth] # at the beginning so user can override
for s in synth_priorities.split(): # synth_priorities no longer in advanced.txt (see system.py above) but we can still support it
    if s.lower()=="ekho": all_synth_classes.append(EkhoSynth)
    elif s.lower()=="espeak": all_synth_classes.append(ESpeakSynth)
    elif s.lower()=="macos":
       all_synth_classes.append(OSXSynth_Say)
       all_synth_classes.append(OSXSynth_OSAScript) # (prefer _Say if >=10.3 because it's faster)
    elif s.lower()=="sapi": all_synth_classes.append(PttsSynth)
all_synth_classes = all_synth_classes + [FestivalSynth,FliteSynth,OldRiscosSynth,S60Synth]
prefer_espeak = prefer_espeak.split()

viable_synths = []
warned_about_nosynth = {}
getsynth_cache = {}
def setSoundCollector(sc):
    # for GUI etc - need to reset the available synths when changing it
    global soundCollector, viable_synths, getsynth_cache
    soundCollector,viable_synths,getsynth_cache = sc,[],{}
def get_synth_if_possible(language,warn=1,to_transliterate=False):
    if language in getsynth_cache and not to_transliterate: return getsynth_cache[language] # most common case (vocab.txt parse)
    if language==None:
        if not None in getsynth_cache: getsynth_cache[None]=Partials_Synth()
        return getsynth_cache[None]
    global viable_synths, warned_about_nosynth
    if not viable_synths:
        for C in all_synth_classes:
            instance = C()
            if instance.works_on_this_platform() and (not soundCollector or hasattr(instance,"makefile")): viable_synths.append(instance)  # TODO: what if soundCollector is later set in the GUI and there's an online-only synth?
    if to_transliterate: # for partials: return a synth that can transliterate the language, if possible
        for synth in viable_synths:
            if synth.supports_language(language) and synth.can_transliterate(language): return synth
        if language=="zh": return simpleZhTransliterator # in case haven't got eSpeak
    for synth in viable_synths:
        if synth.supports_language(language) and not synth.not_so_good_at(language):
            getsynth_cache[language]=synth ; return synth
    for synth in viable_synths:
        if synth.supports_language(language):
            getsynth_cache[language]=synth ; return synth
    if (not warn) or language not in [firstLanguage,secondLanguage]+possible_otherLanguages: return None # without printing a warning
    if not language in warned_about_nosynth:
        warned_about_nosynth[language] = 1
        canSay = []
        if language in synth_partials_voices: canSay.append("recorded syllables (partials)")
        if synthCache: canSay.append("recorded phrases (synthCache)")
        if canSay: canSay="\n  - can use only "+" and ".join(canSay)
        else: canSay="\n  (did you read ALL the comments in vocab.txt?)"
        show_warning(("Warning: No speech synthesizer installed for language '%s'"+cond(appuifw or winCEsound,"",canSay)) % (language,))
    return None # and do NOT set getsynth_cache (see parseSynthVocab)

def synth_event(language,text,is_prompt=0):
    synth = get_synth_if_possible(language) ; assert synth, "Cannot get synth for '%s'" % (language,)
    return SynthEvent(text,synth,language,is_prompt)

def pinyin_uColon_to_V(pinyin):
    pinyin = pinyin.lower()

    pristineU = unichr(0xfc).encode('utf-8')
    pinyin = pinyin.replace("j"+pristineU,"ju").replace("q"+pristineU,"qu").replace("x"+pristineU,"xu").replace(pristineU,"v").replace(unichr(0xea).encode('utf-8'),"e") # for pristine's pinyin
    
    return pinyin.replace("u:","v").replace("leu","lv").replace("neu","nv")

class SynthEvent(Event):
    def __init__(self,text,synthesizer,language,is_prompt=0):
        assert text,"Trying to speak zero-length text"
        self.text = text ; self.synthesizer = synthesizer
        self.modifiedText = self.text
        if language=="en":
            self.modifiedText = self.modifiedText.replace("\xE2\x80\xA7","").replace("\xE2\x80\xB2","") # remove syllable boundaries and primes (usually just confuse speech synths)
            if not self.text[-1] in ";.!?-" and not (';' in self.text and ';' in self.text[self.text.index(';')+1:]): self.modifiedText += ';' # prosody hack (some synths sound a bit too much like 'disjointed strict commands' without this)
        elif language=="zh":
            # normalise pinyin
            # (note - this code is NOT used for partials synth, only for passing to espeak etc.  see elsewhere for partials synth)
            self.modifiedText = pinyin_uColon_to_V(self.modifiedText) # includes .lower()
            # and put space between every syllable of w, if it's one word only (the Lily voice seems to stand a better chance of getting it right that way, and occasionally other voices do too, e.g. "chang2yuan3" in at least some versions of eSpeak, not to mention Loquendo Lisheng
            self.modifiedText = self.modifiedText.replace("-"," ") # for Lily, Lisheng etc.  NB replace hyphen with space not with "", otherwise can get problems with phrases like "wang4en1-fu4yi4"
            if (not " " in self.modifiedText) and ("1" in self.modifiedText or "2" in self.modifiedText or "3" in self.modifiedText or "4" in self.modifiedText or "5" in self.modifiedText):
                self.modifiedText=fix_pinyin(self.modifiedText,[]) # better call that before doing the following (in case any digits in the wrong place)
                for f in py_final_letters:
                    for t in "12345": self.modifiedText=self.modifiedText.replace(f+t,f+t+" ")
            if synthesizer.__class__ in [GeneralSynth, GeneralFileSynth]:
                # some e.g. eSpeak use capitals to start a new sentence, so need to undo some of the .lower() that pinyin_uColon_to_V did.
                # (ESpeakSynth already calls fix_commas in play() and makefile() so don't need to do it here.)
                self.modifiedText=fix_commas(fix_compatibility(ensure_unicode(self.modifiedText)).encode('utf-8'))
            elif synthesizer.__class__ in [PttsSynth]: self.modifiedText = sort_out_pinyin_3rd_tones(self.modifiedText) # for Lily, and in some cases for Lisheng
        self.language = language
        self.is_prompt = is_prompt ; self.sound = None
        if soundCollector and lessonIsTight():
            # non-realtime and a tight-fitting lesson, so it's worth taking time to calculate length more accurately
            self.sound = synthesizer.makefile_cached(language,self.modifiedText) ; synthesizer.finish_makefile()
            length = SampleEvent(self.sound).length
        else: length = synthesizer.guess_length(language,self.modifiedText)
        Event.__init__(self,length)
    def __repr__(self):
        if not self.language: return eventList_repr(self.text) # partials-synth list
        return str(self.text)
    def __setstate__(self,state):
        synth = get_synth_if_possible(state['language'])
        assert synth, "Error: Trying to play a previously-stored lesson under conditions that prevent one of the speech synths from working as before (maybe trying to use an online-only synth offline?)"
        self.__init__(state['text'],synth,state['language'],state['is_prompt'])
    def __getstate__(self): return {"text":self.text,"language":self.language,"is_prompt":self.is_prompt}
    def makesSenseToLog(self): return not self.is_prompt
    def will_be_played(self):
        if not soundCollector and not hasattr(self.synthesizer,"play"):
            self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText) # don't need to do that here if soundCollector, do it on demand below (it might get partially cancelled anyway).  Only need to do it here if generating ahead of real-time.
        else: self.sound = None # in case restoring a lesson that was previously to file but now to speaker (TODO is this still necessary now got __setstate__ above?)
    def getSound(self): # used in caching
        if not self.sound: self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText)
        return self.sound
    def play(self):
        if soundCollector and not self.sound:
            self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText)
            self.synthesizer.finish_makefile()
        if sample_table_hack:
            if not self.sound in sample_table_hack_lengthDic: sample_table_hack_lengthDic[self.sound]=SampleEvent(self.sound).exactLen
            soundCollector.addFile(self.sound,sample_table_hack_lengthDic[self.sound])
            open(self.sound,"wb") # i.e. truncate at 0 bytes to save space (but keep around so no name clashes)
        elif self.sound:
            # If synthesizing asynchronously, hopefully self.sound will have been synthesized by now, but just in case, we'll have a loop
            for t in range(10):
                try: e = SampleEvent(self.sound)
                except IOError:
                    time.sleep(1) ; continue
                return e.play()
            raise IOError("IOError after 10 tries on "+repr(self.sound))
        else:
            assert (not soundCollector) and hasattr(self.synthesizer,"play"),"Should have called will_be_played before playing offline"
            return self.synthesizer.play(self.language,self.modifiedText)
sample_table_hack_lengthDic = {}

class ShellEvent(Event): # used in just_synthesize below, and in concatenative synth as an optimisation on some platforms
    def __init__(self,command,retryOnFail=False):
        Event.__init__(self,0)
        self.command = command
        self.retryOnFail = retryOnFail
    def play(self):
        if soundCollector and hasattr(self,"equivalent_event_list"):
            for e in self.equivalent_event_list:
                if type(e)==type([]): # we have a list of lists-separated-by-pauses
                    for ee in e: ee.play()
                elif e.__class__==Event: soundCollector.addSilence(e.length,False)
                else: e.play()
            return
        elif hasattr(self,"VolReplace"): r = system(self.command.replace("$Vol$",str(eval(self.VolReplace))))
        else: r = system(self.command)
        if self.retryOnFail: return r # else None
    def makesSenseToLog(self): return hasattr(self,"is_prompt") and not self.is_prompt
    def __repr__(self):
        if hasattr(self,"equivalent_event_list"): return eventList_repr(self.equivalent_event_list)
        else: return "ShellEvent: "+self.command

def eventList_repr(el):
    r=[]
    def fname(p):
        if os.sep in p: p=p[p.rindex(os.sep)+1:]
        if extsep in p: p=p[:p.rindex(extsep)]
        return p
    for e in el:
        if type(e)==type([]) or hasattr(e,"eventList"):
            if not type(e)==type([]): e=e.eventList
            for ee in e:
                if not ee.__class__==Event: r.append(fname(str(ee)))
            r.append(",")
        elif not e.__class__==Event: r.append(fname(str(e)))
    return " ".join(r)

def abspath_from_start(p): # for just_synthesize to check for paths relative to the original starting directory if this is different from the gradint directory (see system.py)
    d=os.getcwd()
    os.chdir(starting_directory)
    try: r=os.path.abspath(p)
    except: r="" # library problems on Windows?
    os.chdir(d)
    return r

def just_synthesize(callSanityCheck=0,lastLang_override=None):
    # Handle the justSynthesize setting (see advanced.txt)
    global startAnnouncement,endAnnouncement,logFile,synth_partials_cache
    synth_partials_cache = {} # to stop 'memory leak' when running from the GUI
    oldStart,oldEnd,oldLogfile = startAnnouncement,endAnnouncement,logFile
    startAnnouncement=endAnnouncement=logFile=None
    if app: app.setLabel("") # not "wait a moment"
    called_synth = 0
    # we re-generate the lesson on each repeat, so sporadic-synthcache stuff works
    global repeatMode ; repeatMode = 1
    while repeatMode:
      repeatMode = 0
      less = Lesson()
      lastStartTime = lastEndTime = lastWasDelay = 0
      if lastLang_override: lastLanguage = lastLang_override
      else: lastLanguage = secondLanguage
      def checkCanSynth(fname):
          ret=can_be_synthesized(fname)
          if ret: return fileToEvent(fname)
          else: show_warning("Can't say "+repr(fname)) # previous warnings should have said why (e.g. partials-only language)
      for line in justSynthesize.split("#"):
        line = line.strip(wsp) ; l = line.split(None,1)
        if extsep in line and fileExists(line): event = fileToEvent(line,"")
        elif extsep in line and fileExists(abspath_from_start(line)): event = fileToEvent(abspath_from_start(line),"")
        elif line=='R':
            repeatMode=1 ; continue
        elif len(l)==1:
            try: delayVal = float(l[0])
            except ValueError: delayVal = None
            if delayVal==None:
                # no float value; assume it's a single word to synth in secondLanguage or whatever was the last language used
                show_warning("Assuming that %s is a word to synthesize in language '%s'" % (repr(l[0]),lastLanguage))
                if callSanityCheck and sanityCheck(l[0],lastLanguage,1): return
                event = checkCanSynth("!synth:"+l[0]+"_"+lastLanguage)
                if not event: continue # couldn't synth
                called_synth = 1
            else:
                lastWasDelay = 1
                if delayVal<0: lastEndTime = lastStartTime-delayVal
                else: lastEndTime += delayVal
                continue
        elif len(l)==2:
            lang, text = l
            if lang=="sh:": event = ShellEvent(text)
            else:
                fname = "!synth:"+text+"_"+lang
                if not can_be_synthesized(fname):
                    if lang in [firstLanguage,secondLanguage]+otherLanguages:
                        show_warning("Can't say %s in %s" % (repr(text),repr(lang)))
                        lastLanguage=lang ; continue
                    # otherwise, user might have omitted lang by mistake
                    show_warning("Assuming %s was meant to be synthesized in language '%s'" % (cond("#" in justSynthesize or len(repr(line))<10,"that '"+repr(line)+"'","this line"),lastLanguage))
                    if callSanityCheck and sanityCheck(line,lastLanguage,1): return
                    event = checkCanSynth("!synth:"+line+"_"+lastLanguage)
                else:
                    if callSanityCheck and sanityCheck(text,lang,1): return
                    event = checkCanSynth(fname)
                    lastLanguage = lang
                if not event: continue
                called_synth = 1
        else: continue # len(l)==0: ignore empty strings between #s
        event.addToEvents(less.events,lastEndTime)
        lastWasDelay = 0
        lastStartTime = lastEndTime
        lastEndTime += event.length
      if lastWasDelay: Event(0).addToEvents(less.events,lastEndTime)
      global dbase ; dbase = None # for handleInterrupt
      less.play()
    startAnnouncement,endAnnouncement,logFile = oldStart,oldEnd,oldLogfile
    if not called_synth: return None
    return lastLanguage

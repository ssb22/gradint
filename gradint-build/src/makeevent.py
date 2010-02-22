# This file is part of the source code of
# gradint v0.9952 (c) 2002-2010 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of makeevent.py - make events from recorded words,
# synthesized words, cached synthesized words, or partials

def filesToEvents(files,dirBase=None):
    # Normally will be one file, but might be a list
    # (e.g. when learning poetry, may have a composite
    # prompt)
    if not type(files)==type([]): files = [files]
    return CompositeEvent(map(lambda x:fileToEvent(x,dirBase),files))

class Partials_Synth(Synth):
    # text is really a list of lists of filenames
    def guess_length(self,lang,text):
        l=(len(text)-1)*0.3
        for phrase in text: l+=quickGuess(len(phrase),1.5) # TODO assumes average of 1.5 partials/sec; needs to be better than that
        return l
    def play(self,lang,text):
        if len(text)<=2 or self.guess_length(lang,text)<=10: return SampleEvent(self.makefile(lang,text),isTemp=1).play()
        # If it's big, it might be better to synth one phrase at a time.  (Unfortunately we can't pipeline this on all architectures.  Hopefully this synth-in-the-pauses is OK for now.)
        t=0
        for phrase in text:
            e=SampleEvent(self.makefile(lang,[phrase]),isTemp=1)
            time.sleep(max(0,betweenPhrasePause-(time.time()-t)))
            e.play()
            t=time.time()
    def makefile(self,lang,text):
        # text is a list of syllable-lists
        # the first syllable in 1st list can optionally be the header file to use
        fname = os.tempnam()+dotwav
        o=open(fname,"wb")
        if not (text and text[0] and text[0][0].endswith(dotwav)): o.write(open(partialsDirectory+os.sep+"header"+dotwav,"rb").read())
        for phrase in text:
            datFileInUse = 0
            for f in phrase:
                if f in audioDataPartials:
                    datFile,offset,size = audioDataPartials[f]
                    if not datFileInUse: datFileInUse = open(partialsDirectory+os.sep+datFile,"rb")
                    datFileInUse.seek(offset) ; o.write(datFileInUse.read(size))
                else: o.write(open(partialsDirectory+os.sep+f,"rb").read())
            if not phrase==text[-1]: o.write(chr(0)*partials_raw_0bytes)
        # MUST fix the length, for Windows etc:
        wavLen = o.tell()-8
        o.seek(4) ; o.write(chr(wavLen&0xFF)+chr((wavLen>>8)&0xFF)+chr((wavLen>>16)&0xFF)+chr(wavLen>>24))
        wavLen -= 36 ; o.seek(40) ; o.write(chr(wavLen&0xFF)+chr((wavLen>>8)&0xFF)+chr((wavLen>>16)&0xFF)+chr(wavLen>>24))
        return fname

def fileToEvent(fname,dirBase=None):
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    orig_fname = fname
    if os.sep in fname and fname.find("!synth:")==-1: dirBase,fname = dirBase+fname[:fname.rindex(os.sep)+1], fname[fname.rindex(os.sep)+1:]
    if "_" in fname: lang = languageof(fname)
    else: lang="-unknown-" # so can take a simple wav file, e.g. for endAnnouncement
    if dirBase+fname in variantFiles:
        variantFiles[dirBase+fname]=variantFiles[dirBase+fname][1:]+[variantFiles[dirBase+fname][0]] # cycle through the random order of variants
        fname=variantFiles[dirBase+fname][0]
    if fname.lower().endswith(dottxt) and "_" in fname: fname = "!synth:"+u8strip(open(dirBase+fname,"rb").read()).strip(wsp)+'_'+lang
    if fname.find("!synth:")>-1:
        s = synthcache_lookup(fname)
        if type(s)==type([]): # trying to synth from partials
            if partials_raw_mode: e=synth_event(None,s)
            else: e=optimise_partial_playing_list([CompositeEvent(map(lambda x:SampleEvent(partialsDirectory+os.sep+x,useExactLen=True),phrase)) for phrase in s]) # (tell SampleEvent to useExactLen in this case - don't want ANY pause between them)
            if not e: # can't make a ShellEvent from the whole lot; try making individual ShellEvents:
                e=[]
                for phrase in s:
                    e.append(optimise_partial_playing(CompositeEvent(map(lambda x:SampleEvent(partialsDirectory+os.sep+x,useExactLen=True),phrase))))
                    e.append(Event(betweenPhrasePause))
                e=CompositeEvent(e[:-1]) # omit trailing pause
            if not lessonIsTight(): e.length=math.ceil(e.length) # (TODO slight duplication of logic from SampleEvent c'tor)
        elif s: e=SampleEvent(synthCache+os.sep+s) # single file in synth cache
        else: e=synth_event(languageof(fname),textof(fname))
        e.is_prompt=(dirBase==promptsDirectory+os.sep)
    else: e=SampleEvent(dirBase+fname)
    e.setOnLeaves('wordToCancel',orig_fname)
    return e

transTbl = "TRANS"+extsep+"TBL"
if synthCache:
    # this listdir() call can take ages on rpcemu if it's large
    if riscos_sound: show_info("Reading synthCache... ")
    try: synthCache_contents = os.listdir(synthCache)
    except: synthCache_contents = synthCache = []
    for i in synthCache_contents:
        if i.upper()==transTbl: # in case it's a different case
            transTbl=i ; break
    synthCache_contents = list2set(synthCache_contents)
    if riscos_sound: show_info("done\n")
synthCache_transtbl = {}
if synthCache and transTbl in synthCache_contents:
    ensure_nodups = {} # careful of duplicate filenames being appended to trans.tbl, make sure they override previous entries
    for l in open(synthCache+os.sep+transTbl).readlines():
        v,k = l.strip(wsp).split(None,1)
        if v in ensure_nodups: del synthCache_transtbl[ensure_nodups[v]]
        ensure_nodups[v]=k ; synthCache_transtbl[k]=v
    del ensure_nodups
def textof(fname): return fname[fname.find('!synth:')+7:fname.rfind('_')]
last_partials_transliteration = None
synth_partials_cache = {}
def synthcache_lookup(fname,dirBase=None,printErrors=0,justQueryCache=0):
    # if justQueryCache (used by the GUI), return value is (synthCache_transtbl key, result if any).  If key starts with _, we got a sporadic one.
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    lang = languageof(fname)
    if fname.lower().endswith(dottxt):
        try: fname = fname[:fname.rfind("_")]+"!synth:"+u8strip(open(dirBase+fname,"rb").read()).strip(wsp)+"_"+lang # there *will* be a _ otherwise languageof would have failed
        except IOError: return 0,0 # probably trying to synthcache_lookup a file with variants without first choosing a variant (e.g. in anticipation() to check for sporadic cache entries in old words) - just ignore this
    text = textof(fname)
    useSporadic = -1 # undecided (no point accumulating counters for potentially-unbounded input)
    if justQueryCache: useSporadic=1
    if synthCache:
      for init in "_","":
        for ext in "wav","mp3":
            k=init+text.lower()+"_"+lang+extsep+ext
            s=synthCache_transtbl.get(k,k)
            if s in synthCache_contents: ret=s
            elif s.lower().endswith(dotwav) and s[:-len(dotwav)]+dotmp3 in synthCache_contents: ret=s[:-len(dotwav)]+dotmp3
            else: ret=0
            if ret:
                if justQueryCache: ret=(k,ret)
                if init=="_":
                    if useSporadic==-1: useSporadic=decide_subst_synth(text)
                    if useSporadic: return ret
                else: return ret
    if justQueryCache: return 0,0
    if lang not in partials_langs: l,translit=None,None # don't bother trying to transliterate here if there aren't even any partials for that language
    elif (lang,text) not in synth_partials_cache:
        # See if we can transliterate the text first.
        synth,translit = get_synth_if_possible(lang,0,to_transliterate=True),None
        if synth: translit=synth.transliterate(lang,text)
        if translit: text=translit
        if lang=="zh": t2=sort_out_pinyin_3rd_tones(pinyin_uColon_to_V(text)) # need to do this BEFORE stripPuncEtc, for correct sandhi blocking
        else: t2=text
        l = [synth_from_partials(phrase,lang) for phrase in stripPuncEtc(t2.lower())] # TODO do we really want to be able to pick new voices at every phrase?  if not, would have to pass the pause points into synth_from_partials itself
        if None in l: l=None # if any of the partials-phrases failed, fail all (don't mix partials and synth for different parts of the same phrase, it's too confusing)
        synth_partials_cache[(lang,text)]=(l,translit)
    else: l,translit=synth_partials_cache[(lang,text)]
    if l and partials_are_sporadic:
        if useSporadic==-1: useSporadic=decide_subst_synth(("partials",text))
        if not useSporadic: l=translit=None
    if l and translit: # record it for the GUI
        global last_partials_transliteration
        last_partials_transliteration=translit
    if l: return l
    if printErrors and synthCache and not (app and winsound): show_info("Not in cache: "+repr(text.lower()+"_"+lang)+"\n",True)
def can_be_synthesized(fname,dirBase=None,lang=None):
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    if not lang: lang = languageof(fname)
    if get_synth_if_possible(lang,0): return True
    elif synthcache_lookup(fname,dirBase,1): return True
    else: return get_synth_if_possible(lang) # and this time print the warning
def stripPuncEtc(text):
    # For sending text to synth_from_partials.  Removes spaces and punctuation from text, and returns a list of the text split into phrases.
    for t in " -'\"": text=text.replace(t,"")
    for t in ".!?:;": text=text.replace(t,",")
    return filter(lambda x:x,text.split(","))

if riscos_sound:
    if fileExists("yali-voice/exe") or fileExists(samplesDirectory+".yali-voice/exe") or fileExists(os.getcwd()[:os.getcwd().rindex(".")]+".yali-voice/exe"): show_warning("RISC OS users: Please rename the file yali-voice/exe to yali-voice/zip and unpack it into the gradint directory.")
elif not winsound: # ok if mingw32, appuifw etc (unzip_and_delete will warn)
    # check for yali-voice.exe
    for d in [os.getcwd()+cwd_addSep,".."+os.sep,samplesDirectory+os.sep]:
        f=d+"yali-voice.exe"
        if fileExists(f): unzip_and_delete(f,ignore_fail=1) # ignore the error exit status from unzip, which will be because of extra bytes at the beginning

# Filename / Unicode translation - need some safety across filesystems.  synthCache(+utils) could be done this way also rather than having TRANS.TBL (however I'm not sure it would save that much code)
non_normal_filenames = {} ; using_unicode_filenames=0
def filename2unicode(f):
    if type(f)==type(u""):
        global using_unicode_filenames
        using_unicode_filenames = 1
        return f
    def u8_or_raw(s):
        try: return unicode(s,"utf-8")
        except UnicodeDecodeError: return unicode(s,"latin1") # (actually should try the local codepage on Windows for correct display, but at least this stops a crash)
    if f.find("_u")>-1 or f.find("_U")>-1:
        try: return unicode(f.replace("_u","\\u").replace("_U","\\u"),"unicode_escape")
        except UnicodeDecodeError: # oops, need to be more careful
            ret = []
            while True:
                i = f.lower().find("_u")
                if i==-1: break
                ret.append(u8_or_raw(f[:i]))
                f=f[i:]
                try:
                    r=unicode("\\u"+f[2:6],"unicode_escape")
                    f=f[6:]
                except UnicodeDecodeError:
                    r=f[:2] ; f=f[2:]
                ret.append(r)
            return u"".join(ret+[f])
    u=u8_or_raw(f)
    if filter(lambda x:ord(x)>=128, list(u)): non_normal_filenames[u] = f # make at least some attempt to keep the old one for GUI rename()s etc, TODO this might not always cope with directories in the path being non-normal, so let's hope they don't set that up manually and then expect the GUI to cope with it
    return u
def unicode2filename(u):
    if using_unicode_filenames: return u
    if u in non_normal_filenames: return non_normal_filenames[u]
    f=u.encode("unicode_escape").replace("\\u","_u")
    for unsafe_char in "?+*<=": f=f.replace(unsafe_char,"_u%04x" % ord(unsafe_char))
    return f

synth_partials_voices = {} # lang -> list of voices, each being a tuple of (directory,startDict,midDict,endDict,flags); see comments below for the dictionary format
partials_cache_file="partials-cache"+extsep+"bin"
if partialsDirectory and isDirectory(partialsDirectory):
  dirsToStat = []
  if pickle and fileExists(partials_cache_file):
    try: partials_langs,partials_raw_mode,synth_partials_voices,audioDataPartials,dirsToStat = pickle.Unpickler(open(partials_cache_file,"rb")).load()
    except: dirsToStat = []
    for d,result in dirsToStat:
      if not tuple(os.stat(d))==result:
        dirsToStat=[] ; break
  if not dirsToStat: # need to re-scan
    if riscos_sound or winCEsound: show_info("Scanning partials... ")
    partials_langs = os.listdir(partialsDirectory)
    dirsToStat.append((partialsDirectory,os.stat(partialsDirectory)))
    audioDataPartials = {}
    partials_raw_mode = "header"+dotwav in partials_langs
    for l in partials_langs:
        try: voices = os.listdir(partialsDirectory+os.sep+l)
        except: voices = []
        if voices: dirsToStat.append((partialsDirectory+os.sep+l,os.stat(partialsDirectory+os.sep+l)))
        thisLangVoices = [] ; voices.sort()
        for v in voices:
            start,mid,end = [],[],[] ; flags=0
            try: files = os.listdir(partialsDirectory+os.sep+l+os.sep+v)
            except: files = []
            if files: dirsToStat.append((partialsDirectory+os.sep+l+os.sep+v,os.stat(partialsDirectory+os.sep+l+os.sep+v)))
            def addFile(f):
                global flags
                if riscos_sound and "." in f: f=f.replace(".",extsep) # in case made filelist on another system
                if f=="!calibrated":
                    flags|=1 # calibrated
                if partials_raw_mode and f=="header"+dotwav:
                    flags|=2 # has a separate header.wav
                if f=="audiodata"+extsep+"dat": # parse audiodata.dat
                    dirsToStat.append((partialsDirectory+os.sep+l+os.sep+v+os.sep+f,os.stat(partialsDirectory+os.sep+l+os.sep+v+os.sep+f)))
                    offset=0 ; f=l+os.sep+v+os.sep+f
                    ff=open(partialsDirectory+os.sep+f,"rb")
                    amend = []
                    while True:
                        fftell = ff.tell()
                        char = ff.read(1)
                        if not "0"<=char<="9": break
                        size,fname = (char+ff.readline(256)).strip(wsp).split(None,1)
                        try: size=int(size)
                        except: break # binary just happened to start with "0"-"9"
                        addFile(fname)
                        amend.append(l+os.sep+v+os.sep+fname)
                        audioDataPartials[l+os.sep+v+os.sep+fname] = (f,offset,size)
                        offset += size
                    for k in amend: audioDataPartials[k]=(audioDataPartials[k][0],audioDataPartials[k][1]+fftell,audioDataPartials[k][2])
                    del ff,amend,offset
                if partials_raw_mode:
                    if not f.endswith(extsep+"raw"): return
                elif not f.endswith(dotwav) or f.endswith(dotmp3): return
                if f.find("-s")>-1 or f.find("-i")>-1: start.append(f) # 'start' or 'initial'
                elif not "-" in f or f.find('-m')>-1: mid.append(f)
                elif f.find('-e')>-1 or f.find('-f')>-1: end.append(f) # 'end' or 'finish'
            for f in files: addFile(f)
            def byReverseLength(a,b): return len(b)-len(a)
            start.sort(byReverseLength) ; mid.sort(byReverseLength) ; end.sort(byReverseLength) # important if there are some files covering multiple syllables (and do it to start,mid,end not to files initially, so as to catch files within audiodata.dat also)
            def toDict(l): # make the list of filenames into a dict of short-key -> [(long-key, filename) list].  short-key is the shortest possible key.
                if not l: return {}
                l2 = [] ; kLen = len(l[0])
                for i in l:
                    if "-" in i: key=i[:i.index("-")]
                    else: key=i[:i.rindex(extsep)]
                    if key.find("_u")>-1 or key.find("_U")>-1: # a unicode partial with a portable filename?
                        key = filename2unicode(key).encode('utf-8')
                    l2.append((key,i))
                    kLen=min(kLen,len(key))
                l = {}
                for k,i in l2:
                    if not k[:kLen] in l: l[k[:kLen]]=[]
                    l[k[:kLen]].append((k,i))
                return l
            thisLangVoices.append((v,toDict(start),toDict(mid),toDict(end),flags))
        synth_partials_voices[l] = thisLangVoices
    if riscos_sound or winCEsound: show_info("done\n")
    if pickle:
      try: pickle.Pickler(open(partials_cache_file,"wb"),-1).dump((partials_langs,partials_raw_mode,synth_partials_voices,audioDataPartials,dirsToStat))
      except: pass # ignore write errors as it's only a cache
  if partials_raw_mode:
    (wtype,wrate,wchannels,wframes,wbits) = sndhdr.what(partialsDirectory+os.sep+"header"+dotwav)
    partials_raw_0bytes = int(betweenPhrasePause*wrate)*wchannels*(wbits/8)
else: partials_langs,partials_raw_mode = [],None

def synth_from_partials(text,lang,voice=None,isStart=1):
    text=text.strip(wsp) # so whitespace between words is ignored on the recursive call
    if lang=="zh": # hack for Mandarin - higher tone 5 after a tone 3
        lastNum = None
        for i in range(len(text)):
            if text[i] in "123456":
                if text[i]=="5" and lastNum=="3":
                    # see if we got a "tone 6" (higher tone 5)
                    # don't worry too much if we haven't
                    r=synth_from_partials(text[:i]+"6"+text[i+1:],lang,voice,isStart)
                    if r: return r
                    else: break
                elif lastNum: break # don't look beyond 1st 2
                lastNum = text[i]
    if not voice: # try all voices for the language, see if we can find one that can say all the necessary parts
        if not lang in synth_partials_voices: return None
        needCalibrated=False
        if lang=="zh": # hack for Mandarin - avoid consecutive 1st tones on non-calibrated voices
            # (DON'T do 3rd tone sandhi here - that's the caller's responsibility and we don't want it done twice now there's sandhi-blocking rules)
            lastNum=None
            for c in text:
                if c=="1" and lastNum=="1":
                    needCalibrated=True ; break # TODO: unless this syllable is exactly the same as the last syllable (a repeated syllable is always ok to use even if uncalibrated)
                if c in "123456": lastNum=c
            # end of hack for Mandarin
        for v in synth_partials_voices[lang]:
            if needCalibrated and not v[-1]&1: continue
            r = synth_from_partials(text,lang,v)
            if r:
                if partials_raw_mode and v[-1]&2: r.insert(0,"header"+dotwav)
                return map(lambda x:lang+os.sep+v[0]+os.sep+x,r)
        return None
    dir, start, mid, end, flags = voice
    def lookup_dic(text,dic):
        if dic:
            for k,v in dic.get(text[:len(dic.keys()[0])],[]):
                if text.startswith(k): return k,v
        return None,None
    if not text: return [] # (shouldn't happen)
    k,v = lookup_dic(text,end)
    if text==k: return [v] # whole of (rest of) text matches a 'final' sound
    if isStart: preferredOrder = [start, mid]
    else: preferredOrder = [mid, start] # (can usually get away with re-using a 'start' sound as a 'mid' or vice versa, but can't usually use an 'end' as anything else without it sounding too 'choppy')
    for l in preferredOrder:
        k,v = lookup_dic(text,l)
        if k: # matched a syllable or so - can we do the rest?
            if text==k: return [v] # finished.  (Comment out this line to use *only* 'end' sounds at the end.)
            rest = synth_from_partials(text[len(k):],lang,voice,0)
            if rest: return [v]+rest
            else: return None # (could leave this out and carry on searching, but it's unlikely)

def optimise_partial_playing(ce):
    # ce is a CompositeEvent of SampleEvents.  See if we can change it to a ShellEvent that plays all partial-samples in a single command - this helps with continuity on some low-end platforms.
    if soundCollector and not saveLesson: return ce # no point doing this optimisation if won't ever play in real time
    fileType = soundFileType(ce.eventList[0].file)
    hasPauses = 0
    for e in ce.eventList[1:]:
        if not soundFileType(e.file)==fileType: return ce # must be all the same type for this optimisation
    s = None
    if fileType=="mp3" and madplay_program and not macsound and not cygwin: # (don't do this on cygwin because cygwin will require changeToDirOf and that could get awkward)
        # mp3 probably has encoding gaps etc, but we can try our best
        if playProgram=="aplay": s=ShellEvent(madplay_program+' -q -A $Vol$'+''.join(map(lambda x:' "'+x.file+'"', ce.eventList))+' -o wav:-|aplay -q',True) # (set retryOnFail=True)
        else: s=ShellEvent(madplay_program+' -q -A $Vol$'+''.join(map(lambda x:' "'+x.file+'"', ce.eventList)),True)
        s.VolReplace="soundVolume_dB"
    elif (not fileType=="mp3") and playProgram in ["aplay","sox"]:
        # if they're all the same format, we can use sox concatenation (raw, with an unspecified-length wav header at start)
        # (don't try to do that if different formats - the low-end hardware may not take the rate conversion)
        ok=gotSox
        if ok:
            format = simplified_header(ce.eventList[0].file)
            for e in ce.eventList[1:]:
                if not simplified_header(e.file)==format:
                    ok=False ; break
        if ok:
            s=ShellEvent('set -o pipefail;('+'&&'.join(['cat "%s" | sox -t %s - -t wav - $Vol$ 2>/dev/null' % (ce.eventList[0].file,fileType)]+['cat "%s" | sox -t %s - -t raw - $Vol$'%(e.file,fileType) for e in ce.eventList[1:]])+')|'+cond(playProgram=="aplay",'aplay -q','sox -t wav - '+sox_type+' '+oss_sound_device),True)
            s.VolReplace="sox_effect"
        elif playProgram=="aplay" and not sox_effect: s=ShellEvent('aplay -q '+''.join(map(lambda x:' "'+x.file+'"', ce.eventList)),True) # (which is not quite as good but is the next best thing) (and hope they don't then try to re-play a saved lesson with a volume adjustment)
    if s:
        s.length = ce.length
        s.equivalent_event_list = ce.eventList
        return s
    else: return ce # can't figure out an optimisation in these circumstances
def simplified_header(fname):
    h=sndhdr.what(fname)
    # ignore num frames i.e. h[3], just compare formats
    if h: return h[:3]+h[4:]
def optimise_partial_playing_list(ceList):
    # similar to above, but returns a ShellEvent for a list of ce's that are to be separated by short pauses, or None if can't do this optimisation.  This is because sox on NSLU2's etc has too much latency for the short pauses.
    if (soundCollector and not saveLesson) or not playProgram=="aplay" or not gotSox: return
    format = None ; l = [] ; theLen = 0
    for ce in ceList:
        for e in ce.eventList:
            if not soundFileType(e.file)=="wav": return
            if not format: format=simplified_header(e.file)
            elif not format==simplified_header(e.file): return
            if not l: l.append('sox "%s" -t wav - $Vol$ 2>/dev/null' % (e.file,))
            else: l.append('sox "%s" -t raw - $Vol$'%(e.file,))
            theLen += e.length
        if not ce==ceList[-1]:
            l.append('dd if=/dev/zero bs=%d count=1 2>/dev/null' % (int(betweenPhrasePause*format[1])*format[2]*(format[-1]/8)))
            theLen += betweenPhrasePause
    s=ShellEvent('('+';'.join(l)+')|aplay -q',True)
    s.length = theLen
    s.VolReplace="sox_effect"
    s.equivalent_event_list = []
    for ce in ceList[:-1]:
        # equivalent_event_list can be a list of 'lists with pauses in between'.
        # Event()s are interpreted correctly only if preceeded by lists.  (TODO this is getting hacky)
        s.equivalent_event_list.append(ce.eventList)
        s.equivalent_event_list.append(Event(betweenPhrasePause))
    s.equivalent_event_list.append(ceList[-1])
    return s


# This file is part of the source code of
program_name = "gradint v0.9928 (c) 2002-2009 Silas S. Brown. GPL v3+."
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of filescan.py - check for available samples and prompts and read in synthesized vocabulary

limitedFiles = {} # empty this before calling scanSamples if
                  # scanSamples ever gets called a second
                  # time (really need to put it in an object
                  # but...) - lists sample (RHS) filenames
                  # that are in 'limit' dirs
dirsWithIntros = [] # ditto
filesWithExplanations = {} # ditto
singleLinePoems = {} # ditto (keys are any poem files which are single line only, so as to avoid saying 'beginning' in prompts)
def scanSamples(directory=None):
    if not directory: directory=samplesDirectory
    # Scans the samples directory for pairs of
    # files like someword_zh.wav, someword_en.wav
    # Recurses through subdirectories (but en/zh pairs must
    # be in the same subdirectory)
    # (Note: Rest of program now also supports LISTS of
    # files to use for a given "word" - currently used in
    # poetry learning)
    retVal = []
    doLabel("Scanning samples")
    if import_recordings_from:
        try: l=os.listdir(import_recordings_from)
        except: l=[]
        destDir = None
        for f in l:
            if (f.lower().endswith(dotwav) or f.lower().endswith(dotmp3)) and f[-5] in "0123456789":
                if not destDir:
                    if not getYN("Import the recordings that are in "+import_recordings_from+"?"): break
                    prefix=time.strftime("%Y-%m-%d") ; i=0
                    while isDirectory(prefix+cond(i,"_"+str(i),"")): i+=1
                    destDir=directory+os.sep+prefix+cond(i,"_"+str(i),"")
                    try: os.mkdir(directory) # make sure samples directory exists
                    except: pass
                    os.mkdir(destDir)
                    open(destDir+os.sep+"settings"+dottxt,"w").write("firstLanguage=\""+firstLanguage+"\"\nsecondLanguage=\""+secondLanguage+"\"\n")
                try: os.rename(import_recordings_from+os.sep+f,destDir+os.sep+f)
                except:
                    try:
                        import shutil
                        shutil.copy2(import_recordings_from+os.sep+f,destDir+os.sep+f)
                    except: open(destDir+os.sep+f,"wb").write(import_recordings_from+os.sep+f).read()
                    os.remove(import_recordings_from+os.sep+f)
    scanSamples_inner(directory,retVal,0)
    return retVal
def exec_in_a_func(x): # helper function for below (can't be nested in python 2.3)
   # Also be careful of http://bugs.python.org/issue4315 (shadowing globals in an exec) - better do this in a dictionary
   d={"firstLanguage":firstLanguage,"secondLanguage":secondLanguage}
   exec x in d
   return d["secondLanguage"],d["firstLanguage"]
def scanSamples_inner(directory,retVal,doLimit):
    if not (directory.find(exclude_from_scan)==-1): return
    firstLangSuffix = "_"+firstLanguage+extsep
    secLangSuffix = "_"+secondLanguage+extsep
    try: ls = os.listdir(directory)
    except OSError: return # (can run without a 'samples' directory at all if just doing synth)
    if "settings"+dottxt in ls:
        # Sort out the o/p from import_recordings_from above (and legacy record-with-HDogg.bat if anyone's still using that)
        oddLanguage,evenLanguage = exec_in_a_func(u8strip(open(directory+os.sep+"settings"+dottxt,"rb").read().replace("\r\n","\n")).strip(wsp))
        if oddLanguage==evenLanguage: oddLanguage,evenLanguage="_"+oddLanguage,"-meaning_"+evenLanguage # if user sets languages the same, assume they want -meaning prompts
        else: oddLanguage,evenLanguage="_"+oddLanguage,"_"+evenLanguage
        for f in ls:
            if "_" in f or not extsep in f: continue
            i=f.rfind(extsep)
            while i>0 and f[i-1] in "0123456789": i-=1
            num=f[i:f.rfind(extsep)]
            if not num: continue # no number to adjust
            os.rename(directory+os.sep+f,directory+os.sep+f[:i]+(("%0"+str(len(str(len(ls))))+"d") % (int((int(num)-1)/2)*2+1))+cond(int(num)%2,oddLanguage,evenLanguage)+f[f.rfind(extsep):])
        os.remove(directory+os.sep+"settings"+dottxt)
        ls = os.listdir(directory)
    ls.sort() ; lsDic = {}
    for file in ls:
        filelower = file.lower()
        # in lsDic if it's in the list (any extension); =filename if it's an extension we know about (see comment below for reason for this)
        if (filelower.endswith(dottxt) and file.find("_")>-1 and can_be_synthesized(file,directory)) or filelower.endswith(dotwav) or filelower.endswith(dotmp3): val = file
        else:
            val = 0
            if filelower.endswith(extsep+"zip"): show_warning("Warning: Ignoring "+file+" (please unpack it first)") # so you can send someone a zip file for their recorded words folder and they'll know what's up if they don't unpack it
        if filelower.endswith(dottxt) and (file+extsep)[:file.find(extsep)] in lsDic: continue # don't let a .txt override a recording if both exist
        else: lsDic[(file+extsep)[:file.find(extsep)]] = val
    intro = intro_filename+"_"+firstLanguage
    if intro in lsDic: dirsWithIntros.append((directory[len(samplesDirectory)+len(os.sep):],lsDic[intro]))
    if not doLimit: doLimit = limit_filename in lsDic
    doPoetry = poetry_filename in lsDic
    if doPoetry:
        # check which language the poetry is to be in
        doPoetry = ""
        for file in ls:
            if file.find(secLangSuffix)>-1 and not doPoetry: doPoetry=secLangSuffix
            elif (not file.find(firstLangSuffix)>-1):
                for l in otherLanguages:
                    if file.find("_"+l+extsep)>=0:
                        doPoetry="_"+l+extsep; break
    prefix = directory[len(samplesDirectory)+len(os.sep):] # the directory relative to samplesDirectory
    if prefix: prefix += os.sep
    lastFile = None # for doPoetry
    for file in ls:
        if not lsDic.get(file[:file.rfind(extsep)]):
            lastFile = None # avoid problems with connecting poetry lines before/after a line that's not in the synth cache or something
            if isDirectory(directory+os.sep+file) and not directory+os.sep+file==promptsDirectory: # (NB putting that 'if' here, not before previous one, because isDirectory() can take time when got thousands of files.  Hopefully the risk of people putting ".wav" extensions on their directory names is low enough.)
                if file=="RENAME.ME":
                    # Hack for record-with-HDogg.bat: Rename any directory called RENAME.ME, in case the user forgot to do it
                    newName = "%d-%02d-%02d" % time.localtime()[:3]
                    count = 1
                    while isDirectory(directory+os.sep+newName) or fileExists(directory+os.sep+newName):
                        count += 1
                        newName = "%d-%02d-%02d-%d" % (time.localtime()[:3]+[count])
                    os.rename(directory+os.sep+file,directory+os.sep+newName)
                    file=newName
                scanSamples_inner(directory+os.sep+file,retVal,doLimit)
            else: continue # no extension, or not an extension we know about - ignore (DO need this, because one way of temporarily disabling stuff is to rename it to another exension)
        elif not file==lsDic.get(file[:file.rfind(extsep)]): continue # different extensions with same filename (e.g. both .txt and .wav) - ignore all but the "best" one
        elif file.find(firstLangSuffix)==-1 or firstLanguage==secondLanguage:
            # not a prompt word and not a directory
            if doPoetry and not file.find(doPoetry)>-1: continue # save confusion
            # check for second & other languages
            # (there might not be a 1st-language prompt if learning poetry)
            if file.find(secLangSuffix)>=0: wordSuffix=secLangSuffix
            else:
                wordSuffix=None
                for l in otherLanguages:
                    if file.find("_"+l+extsep)>=0:
                        wordSuffix="_"+l+extsep ; break
                if not wordSuffix: continue # can't do anything with this file
            if firstLanguage==secondLanguage: promptFile=None
            else:
                promptFile=file.replace(wordSuffix,firstLangSuffix) # TODO what if some user puts wordSuffix earlier in the filename?  really want to replace only the LAST one.
                promptFile = lsDic.get(promptFile[:promptFile.rfind(extsep)],0)
            explanationFile = lsDic.get(file[:file.rfind(wordSuffix)]+wordSuffix[:-1]+"_explain_"+firstLanguage,0)
            if not promptFile and not wordSuffix==secLangSuffix:
                # May have prompt from second language to another language (TODO explanationFile also??)
                promptFile = file.replace(wordSuffix,secLangSuffix)
                promptFile = lsDic.get(promptFile[:promptFile.rfind(extsep)],0)
            if not promptFile:
                # Try looking for a "-meaning" file
                promptFile = file.replace(wordSuffix,"-meaning"+wordSuffix)
                promptFile = lsDic.get(promptFile[:promptFile.rfind(extsep)],0)
            if promptFile:
                # There is a simpler-language prompt
                if doPoetry and lastFile:
                    if lastFile[0]: promptToAdd = [prefix+lastFile[0], prefix+promptFile, prefix+lastFile[1]] # both last line's and this line's prompt, then last line's contents
                    else: promptToAdd = [prefix+lastFile[1], prefix+promptFile] # last line didn't have a prompt, so put last line's contents before this line's prompt
                else: promptToAdd = prefix+promptFile
            elif doPoetry:
                # poetry without first-language prompts
                if lastFile:
                    promptToAdd = prefix+lastFile[-1]
                    if directory[len(samplesDirectory)+len(os.sep):]+lastFile[-1] in singleLinePoems: del singleLinePoems[directory[len(samplesDirectory)+len(os.sep):]+lastFile[-1]]
                else:
                    promptToAdd = prefix+file # 1st line is its own prompt
                    singleLinePoems[directory[len(samplesDirectory)+len(os.sep):]+file]=1
            else: continue # can't do anything with this file
            retVal.append((0,promptToAdd,prefix+file))
            if explanationFile: filesWithExplanations[prefix+file]=explanationFile
            if doLimit: limitedFiles[prefix+file]=prefix
            lastFile = [promptFile,file]

cache_maintenance_mode=0 # hack so cache-synth.py etc can cache promptless words for use in justSynthesize
def parseSynthVocab(fname,forGUI=0):
    if not fname: return []
    langs = [secondLanguage,firstLanguage] ; someLangsUnknown = 0 ; maxsplit = 1
    ret = []
    count = 1 ; doLimit = 0 ; limitNo = 0 ; doPoetry = 0
    lastPromptAndWord = None
    try: o=open(fname,"rb")
    except IOError: return []
    doLabel("Reading "+fname)
    allLangs = list2set([firstLanguage,secondLanguage]+otherLanguages)
    for l in u8strip(o.read()).replace("\r","\n").split("\n"):
        # TODO can we make this any faster on WinCE with large vocab lists? (tried SOME optimising already)
        if not "=" in l: # might be a special instruction
            if not l: continue
            canProcess = 0 ; l2=l.strip(wsp)
            if not l2 or l2[0]=='#': continue
            l2=l2.lower()
            if l2.startswith("set language ") or l2.startswith("set languages "):
                langs=l.split()[2:] ; someLangsUnknown = 0
                maxsplit = len(langs)-1
                for l in langs:
                    if not l in allLangs: someLangsUnknown = 1
            elif l2.startswith("limit on"):
                doLimit = 1 ; limitNo += 1
            elif l2.startswith("limit off"): doLimit = 0
            elif l2.startswith("begin poetry"): doPoetry,lastPromptAndWord = True,None
            elif l2.startswith("end poetry"): doPoetry = lastPromptAndWord = None
            elif l2.startswith("poetry vocab line:"): doPoetry,lastPromptAndWord = 0,cond(lastPromptAndWord,lastPromptAndWord,0) # not None, in case we're at the very start of a poem (see "just processed"... at end)
            else: canProcess=1
            if not canProcess: continue
        elif "#" in l and l.strip(wsp)[0]=='#': continue # guard condition '"#" in l' improves speed
        if forGUI: strCount=""
        else:
            strCount = "%05d!synth:" % (count,)
            count += 1
        langsAndWords = zip(langs,l.split("=",maxsplit)) # don't try strip on a map() - it's faster to do it as-needed below
        # (maxsplit means you can use '=' signs in the last language, e.g. if using SSML with eSpeak)
        if someLangsUnknown: langsAndWords = filter(lambda x:x[0] in allLangs, langsAndWords)
        # Work out what we'll use for the prompt.  It could be firstLanguage, or it could be one of the other languages if we see it twice (e.g. if 2nd language is listed twice then the second one will be the prompt for 2nd-language-to-2nd-language learning), or it could be the only language if we're simply listing words for cache maintenance
        prompt = None
        if firstLanguage==secondLanguage: langsAlreadySeen = {}
        else: langsAlreadySeen = {firstLanguage:True}
        i=onePastPromptIndex=0
        while i<len(langsAndWords):
            lang,word = langsAndWords[i] ; i += 1
            isReminder = cache_maintenance_mode and len(langsAndWords)==1 and not doPoetry
            if (lang in langsAlreadySeen or isReminder) and (lang in getsynth_cache or can_be_synthesized("!synth:"+word+"_"+lang)): # (check cache because most of the time it'll be there and we don't need to go through all the text processing in can_be_synthesized)
                if not word: continue
                elif word[0] in wsp or word[-1] in wsp: word=word.strip(wsp) # avoid call if unnecessary
                prompt = strCount+word+"_"+lang
                if not isReminder: onePastPromptIndex=i
                break
            langsAlreadySeen[lang]=True
        prompt_L1only = prompt # before we possibly change it into a list etc.  (Actually not necessarily L1 see above, but usually is)
        if doPoetry:
            if prompt and lastPromptAndWord:
                if lastPromptAndWord[0]: prompt=[lastPromptAndWord[0],prompt,lastPromptAndWord[1]] # L1 for line 1, L1 for line2, L2 for line 1
                else: prompt=[lastPromptAndWord[1],prompt] # line 1 doesn't have L1 but line 2 does, so have L2 for line 1 + L1 for line 2
            elif not prompt:
                if lastPromptAndWord:
                    prompt=lastPromptAndWord[-1]
                    if lastPromptAndWord[-1] in singleLinePoems: del singleLinePoems[lastPromptAndWord[-1]]
                else:
                    prompt = 1 # file itself (see below)
        if prompt:
            i=0
            while i<len(langsAndWords):
                lang,word = langsAndWords[i] ; i+=1
                if i==onePastPromptIndex or (lang==firstLanguage and not firstLanguage==secondLanguage) or not word: continue # if 1st language occurs more than once (target as well as prompt) then don't get confused - this vocab file is probably being used with reverse settings
                elif word[0] in wsp or word[-1] in wsp: word=word.strip(wsp) # avoid call if unnecessary
                if lang in getsynth_cache or can_be_synthesized("!synth:"+word+"_"+lang):
                    f=strCount+word+"_"+lang
                    if prompt==1 or prompt==f: # a file with itself as the prompt (either explicitly or by omitting any other prompt)
                        prompt=f
                        singleLinePoems[f]=1
                    ret.append((0,prompt,f))
                    if doLimit: limitedFiles[f]="synth:"+str(limitNo)
                    if doPoetry: lastPromptAndWord = [prompt_L1only,f]
                elif doPoetry: lastPromptAndWord=None # if one of the lines can't be synth'd, don't connect the lines before/after it
        if not lastPromptAndWord==None: doPoetry = 1 # just processed a "poetry vocab line:" (lastPromptAndWord is either the real last prompt and word, or 0 if we were at the start)
    return ret

# Prompt file syntax: word_language.wav
# or: word_language_2.wav .. (alternatives chosen at random)
# ('word' can also be a language name)
class PromptException(Exception):
    def __init__(self,message): self.message = message
    def __repr__(self): return self.message
class AvailablePrompts(object):
    reservedPrefixes = list2set(["whatmean","meaningis","repeatAfterMe","sayAgain","longpause","begin","end",firstLanguage,secondLanguage] + otherLanguages + possible_otherLanguages)
    def __init__(self):
        try: ls = os.listdir(promptsDirectory)
        except: ls = [] # (won't be able to do a normal gradint run, but report that later)
        self.prefixes = [] ; self.lsDic = {}
        for file in ls:
            filelower = file.lower()
            if file.find("_")>-1 and (filelower.endswith(dotwav) or filelower.endswith(dotmp3) or (filelower.endswith(dottxt) and can_be_synthesized(file,promptsDirectory))):
                # TODO this needs to be re-written in case some users make prompts with extra '_' characters in them.  We're assuming there are at most 2 _s, like sthg_lang_variant.{txt,wav}
                self.prefixes.append(file[:file.index("_")])
                second_ = file.find("_",file.index("_")+1)
                if second_ > -1:
                    normalised_name = file[:second_]
                else: normalised_name = file[:file.rfind(extsep)]
                if not normalised_name in self.lsDic:
                    self.lsDic[normalised_name] = []
                self.lsDic[normalised_name].append(file)
        self.user_is_advanced = None
    def getRandomPromptList(self,promptsData,language):
        random.shuffle(self.prefixes)
        for p in self.prefixes:
            if p in self.reservedPrefixes: continue
            try:
                theList = self.getPromptList(p,promptsData,language)
                return theList
            except PromptException: pass
        raise PromptException("Can't find a non-reserved prompt suitable for language '%s'" % (language))
    def fromLsDic(self,key):
        return random.choice(self.lsDic[key])
    def getPromptList(self,prefix,promptsData,language):
        # used for introducing foreign-language prompts to
        # beginners.  language is the suffix of the language we're *learning*.
        if self.user_is_advanced==None:
            self.user_is_advanced = 0
            for p in promptsData.values():
                if p > advancedPromptThreshold2:
                    self.user_is_advanced = 1 ; break # got a reasonably advanced user
        beginnerPrompt = prefix+"_"+firstLanguage
        if not beginnerPrompt in self.lsDic:
            if self.user_is_advanced and not language==secondLanguage and prefix+"_"+secondLanguage in self.lsDic: beginnerPrompt=prefix+"_"+secondLanguage # No first language prompt, but in advanced mode may be able to find a second-language prompt for a 3rd language
            else: beginnerPrompt = None
        advancedPrompt = prefix+"_"+language
        if not advancedPrompt in self.lsDic:
            # Must use beginnerPrompt
            if beginnerPrompt: r=[self.fromLsDic(beginnerPrompt)]
            else:
                if language in [firstLanguage,secondLanguage]: raise PromptException("Can't find "+prefix+"_"+firstLanguage+" or "+prefix+"_"+secondLanguage)
                else: raise PromptException("Can't find "+prefix+"_"+language+", "+prefix+"_"+firstLanguage+" or "+prefix+"_"+secondLanguage)
        elif not beginnerPrompt:
            # Must use advancedPrompt
            if (not self.user_is_advanced) and cond(language==secondLanguage,advancedPromptThreshold,advancedPromptThreshold2): raise PromptException("Prompt '%s' is too advanced; need '%s_%s' (unless you set %s=0 in advanced%stxt)" % (advancedPrompt,prefix,firstLanguage,cond(language==secondLanguage,"advancedPromptThreshold","advancedPromptThreshold2"),extsep))
            r=[self.fromLsDic(advancedPrompt)]
        elif promptsData.get(advancedPrompt,0) >= cond(language==secondLanguage,advancedPromptThreshold,advancedPromptThreshold2): r=[self.fromLsDic(advancedPrompt)]
        elif promptsData.get(advancedPrompt,0) >= cond(language==secondLanguage,transitionPromptThreshold,transitionPromptThreshold2): r=[self.fromLsDic(advancedPrompt), self.fromLsDic(beginnerPrompt)]
        else: r=[self.fromLsDic(beginnerPrompt)]
        # (NB may seem to go forward/backward across
        # thresholds in a lesson because things are added by
        # sequence, not chronological order, but that
        # doesn't matter)

        # Increment advancedPrompt, taking care not to go
        # past the threshold if it's not available yet
        adv = promptsData.get(advancedPrompt,0)
        if advancedPrompt in self.lsDic or adv <= cond(language==secondLanguage,transitionPromptThreshold,transitionPromptThreshold2):
            adv += 1
        promptsData[advancedPrompt] = adv
        # and finally,
        if not language==secondLanguage and not prefix==language and not prefix=="meaningis": r=self.getPromptList(language,promptsData,language)+r # yes, before - works better than after
        return r
# availablePrompts = AvailablePrompts() # do NOT construct here - if a warning is printed (e.g. can't find a synth) then it might go to the wrong place if GUI has not yet started.  Constructor moved to main_loop().

def introductions(zhFile,progressData):
    toIntroduce = []
    for d,fname in dirsWithIntros[:]:
        found = 0
        for p in progressData:
            if p[-1].startswith(d) and p[0]:
                # this dir has already been introduced
                found=1 ; dirsWithIntros.remove((d,fname)) ; break
        if found: continue
        if zhFile.startswith(d): toIntroduce.append((d,fname))
    toIntroduce.sort() # should put shorter ones 1st
    return map(lambda (x,fname): fileToEvent(cond(x,x+os.sep,"")+fname), toIntroduce)

def explanations(zhFile):
    if zhFile in filesWithExplanations: return fileToEvent(zhFile.replace(dotmp3,dotwav).replace(dottxt,dotwav).replace(dotwav,"_explain_"+firstLanguage+filesWithExplanations[zhFile][-len(dotwav):]))


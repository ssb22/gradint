# This file is part of the source code of
# gradint v0.9982 (c) 2002-2012 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of filescan.py - check for available samples and prompts and read in synthesized vocabulary

def init_scanSamples():
  global limitedFiles,dirsWithIntros,filesWithExplanations,singleLinePoems,variantFiles
  limitedFiles = {} # lists sample (RHS) filenames that are in 'limit' dirs
  dirsWithIntros = []
  filesWithExplanations = {}
  singleLinePoems = {} # keys are any poem files which are single line only, so as to avoid saying 'beginning' in prompts
  variantFiles = {} # careful with clearing this if prompts is using it also (hence called only below and in loop.py before prompt scan)
init_scanSamples() ; emptyCheck_hack = 0
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
    if not emptyCheck_hack: doLabel("Scanning samples")
    if import_recordings_from: import_recordings()
    scanSamples_inner(directory,retVal,0)
    return retVal

def words_exist(): # for GUI (but do NOT call from GUI thread)
  global emptyCheck_hack ; emptyCheck_hack = 1
  r = scanSamples() or parseSynthVocab(vocabFile)
  emptyCheck_hack = 0
  return r

class CannotOverwriteExisting(Exception): pass
def import_recordings(destDir=None):
    global import_recordings_from
    if not type(import_recordings_from)==type([]): # legacy settings
        if import_recordings_from: import_recordings_from=[import_recordings_from]
        else: import_recordings_from = []
    numFound=0
    for checkFirst in [1,0]:
      if checkFirst:
        if destDir: curFiles=list2set(os.listdir(destDir))
        else: continue # no point checking for existing files in a new directory
      for importDir in import_recordings_from:
        try: l=os.listdir(importDir)
        except: l=[]
        for f in l:
            if (f.lower().endswith(dotwav) or f.lower().endswith(dotmp3)) and f[-5] in "0123456789":
                if checkFirst:
                  for lang in [firstLanguage,secondLanguage]:
                   for ext in [dotwav,dotmp3]:
                    if f[:f.rfind(extsep)]+"_"+lang+ext in curFiles: raise CannotOverwriteExisting()
                  continue
                if not destDir:
                    if not getYN("Import the recordings that are in "+importDir+"?"): break
                    prefix=time.strftime("%Y-%m-%d") ; i=0
                    while isDirectory(prefix+cond(i,"_"+str(i),"")): i+=1
                    destDir=directory+os.sep+prefix+cond(i,"_"+str(i),"")
                    try: os.mkdir(directory) # make sure samples directory exists
                    except: pass
                    os.mkdir(destDir)
                try: os.rename(importDir+os.sep+f,destDir+os.sep+f)
                except:
                    try:
                        import shutil
                        shutil.copy2(importDir+os.sep+f,destDir+os.sep+f)
                    except: open(destDir+os.sep+f,"wb").write(read(importDir+os.sep+f))
                    os.remove(importDir+os.sep+f)
                numFound += 1
    if numFound: open(destDir+os.sep+"settings"+dottxt,"w").write("firstLanguage=\""+firstLanguage+"\"\nsecondLanguage=\""+secondLanguage+"\"\n")
    return numFound

def exec_in_a_func(x): # helper function for below (can't be nested in python 2.3)
   # Also be careful of http://bugs.python.org/issue4315 (shadowing globals in an exec) - better do this in a dictionary
   d={"firstLanguage":firstLanguage,"secondLanguage":secondLanguage}
   exec x in d
   return d["secondLanguage"],d["firstLanguage"]
def check_has_variants(directory,ls):
    if directory==promptsDirectory: return True
    else:
        for file in ls:
            if (file+extsep)[:file.rfind(extsep)]==variants_filename: return True

# TODO can we make it so samples like ".wav.mp3" (lame's default o/p naming convention) work?  They already work if !variants is set and it's lang_zh_variant, because the .wav is then interpreted as part of the variant name.  Otherwise .wav is interpreted as part of the language name so file will be ignored.

def getLsDic(directory):
    # Helper function for samples and prompts scanning
    # Calls os.listdir, returns dict of filename-without-extension to full filename
    # Puts variants into variantFiles and normalises them
    # Also sorts out import_recordings output (pointless for prompts, but settings.txt shouldn't be found in prompts)
    if not (directory.find(exclude_from_scan)==-1): return {}
    try: ls = os.listdir(directory)
    except: return {} # (can run without a 'samples' directory at all if just doing synth)
    if "settings"+dottxt in ls:
        # Sort out the o/p from import_recordings (and legacy record-with-HDogg.bat if anyone's still using that)
        oddLanguage,evenLanguage = exec_in_a_func(u8strip(read(directory+os.sep+"settings"+dottxt).replace("\r\n","\n")).strip(wsp))
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
    has_variants = check_has_variants(directory,ls)
    for file in ls:
        filelower = file.lower()
        # in lsDic if it's in the list (any extension); =filename if it's an extension we know about; =None if it's a directory (in which case the key is the full filename), ottherwise =""
        if has_variants and file.find("_",file.find("_")+1)>-1: languageOverride=file[file.find("_")+1:file.find("_",file.find("_")+1)]
        else: languageOverride=None
        if filelower.endswith(dottxt) and (file+extsep)[:file.rfind(extsep)] in lsDic: continue # don't let a .txt override a recording if both exist
        if (filelower.endswith(dottxt) and file.find("_")>-1 and can_be_synthesized(file,directory,languageOverride)) or filelower.endswith(dotwav) or filelower.endswith(dotmp3): val = file
        else:
            val = ""
            if filelower.endswith(extsep+"zip"): show_warning("Warning: Ignoring "+file+" (please unpack it first)") # so you can send someone a zip file for their recorded words folder and they'll know what's up if they don't unpack it
            elif isDirectory(directory+os.sep+file):
                lsDic[file]=None # a directory: store full name even if it has extsep in it.  Note however that we don't check isDirectory() if it's .wav etc as that would take too long.  (however some dirnames can contain dots)
                # (+ NB need to store the directories specifically due to cases like course/ and course.pdf which may otherwise result in 2 traversals of "course" if we check isDirectory on 'extension is either none or unknown')
                continue
            elif (file+extsep)[:file.rfind(extsep)] in lsDic: continue # don't let a .txt~ or other unknown extension override a .txt
        lsDic[(file+extsep)[:file.rfind(extsep)]] = val # (this means if there's both mp3 and wav, wav will overwrite as comes later)
    if has_variants:
        ls=list2set(ls) ; newVs = []
        for k,v in lsDic.items():
            # check for _lang_variant.ext and take out the _variant,
            # but keep them in variantFiles dict for fileToEvent to put back
            if not v or (not directory==promptsDirectory and v.find("_explain_")>-1): continue # don't get confused by that
            last_ = v.rfind("_")
            if last_==-1: continue
            penult_ = v.rfind("_",0,last_)
            if penult_==-1: continue
            del lsDic[k]
            newK,newV = k[:k.rfind("_")], v[:v.rfind("_")]+v[v.rfind(extsep):]
            if not newK in lsDic: lsDic[newK] = newV
            else: # variants of different file types? better store them all under one (fileToEvent will sort out).  (Testing if the txt can be synth'd has already been done above)
                if v.endswith(dottxt) and not lsDic[newK].endswith(dottxt): # if any variants are .txt then we'd better ensure the key is, so transliterate etc finds it. So move the key over to the .txt one.
                    old_dirV = directory+os.sep+lsDic[newK]
                    d = variantFiles[old_dirV]
                    del variantFiles[old_dirV]
                    lsDic[newK] = newV
                    variantFiles[directory+os.sep+newV] = d
                    lsDic[newK] = newV # just add to the previous key
                else: newV = lsDic[newK]
            dir_newV = directory+os.sep+newV
            if not dir_newV in variantFiles:
                variantFiles[dir_newV] = []
                if newV in ls: variantFiles[dir_newV].append(newV) # the no-variants name is also a valid option
            variantFiles[dir_newV].append(v)
            newVs.append(dir_newV)
        for v in newVs: random.shuffle(variantFiles[v])
    return lsDic

def scanSamples_inner(directory,retVal,doLimit):
    firstLangSuffix = "_"+firstLanguage
    secLangSuffix = "_"+secondLanguage
    lsDic = getLsDic(directory)
    intro = intro_filename+"_"+firstLanguage
    if intro in lsDic: dirsWithIntros.append((directory[len(samplesDirectory)+len(os.sep):],lsDic[intro]))
    if not doLimit: doLimit = limit_filename in lsDic
    doPoetry = poetry_filename in lsDic
    if doPoetry:
        # check which language the poetry is to be in (could be L1-to-L2, L2-to-L3, L2-only, or L3-only)
        def poetry_language():
         ret = ""
         for file,withExt in lsDic.items():
          if withExt:
            if file.endswith(secLangSuffix): ret=secLangSuffix # but stay in the loop
            elif (not file.endswith(firstLangSuffix)):
                llist = [firstLanguage,secondLanguage]+otherFirstLanguages
                for l in otherLanguages:
                    if not l in llist and file.endswith("_"+l): return "_"+l
         return ret
        doPoetry = poetry_language()
    prefix = directory[len(samplesDirectory)+cond(samplesDirectory,len(os.sep),0):] # the directory relative to samplesDirectory
    if prefix: prefix += os.sep
    lastFile = None # for doPoetry
    items = lsDic.items() ; items.sort()
    for file,withExt in items:
        swapWithPrompt = 0
        if not withExt:
            lastFile = None # avoid problems with connecting poetry lines before/after a line that's not in the synth cache or something
            if withExt==None and (cache_maintenance_mode or not directory+os.sep+file==promptsDirectory): # a directory
                scanSamples_inner(directory+os.sep+file,retVal,doLimit)
                if emptyCheck_hack and retVal: return
            # else no extension, or not an extension we know about - ignore (DO need this, because one way of temporarily disabling stuff is to rename it to another exension)
        elif file.find("_")==-1: continue # save confusion (!poetry, !variants etc)
        elif (doPoetry and file.endswith(doPoetry)) or (not doPoetry and (not file.endswith(firstLangSuffix) or firstLanguage==secondLanguage)): # not a prompt word
            if file.endswith(secLangSuffix): wordSuffix=secLangSuffix
            else:
                wordSuffix=None
                for l in otherLanguages:
                    if not l in [firstLanguage,secondLanguage] and file.endswith("_"+l):
                        if l in otherFirstLanguages: swapWithPrompt=1
                        wordSuffix="_"+l ; break
                if not wordSuffix: continue # can't do anything with this file
            if swapWithPrompt or firstLanguage==secondLanguage: promptFile=None
            else: promptFile = lsDic.get(file[:-len(wordSuffix)]+firstLangSuffix,0)
            explanationFile = lsDic.get(file[:-len(wordSuffix)]+wordSuffix+"_explain_"+firstLanguage,0)
            if not promptFile and not wordSuffix==secLangSuffix:
                # May have prompt from second language to another language (TODO explanationFile also??)
                promptFile = lsDic.get(file[:-len(wordSuffix)]+secLangSuffix,0)
            if not promptFile:
                # Try looking for a "-meaning" file
                promptFile = lsDic.get(file[:-len(wordSuffix)]+"-meaning"+wordSuffix,0)
            if promptFile:
                # There is a simpler-language prompt
                if swapWithPrompt: promptFile,withExt = withExt,promptFile
                if doPoetry and lastFile:
                    if lastFile[0]: promptToAdd = [prefix+lastFile[0], prefix+promptFile, prefix+lastFile[1]] # both last line's and this line's prompt, then last line's contents
                    else: promptToAdd = [prefix+lastFile[1], prefix+promptFile] # last line didn't have a prompt, so put last line's contents before this line's prompt
                else: promptToAdd = prefix+promptFile
            elif doPoetry:
                # poetry without first-language prompts
                if lastFile:
                    promptToAdd = prefix+lastFile[-1]
                    if promptToAdd in singleLinePoems: del singleLinePoems[promptToAdd]
                else:
                    promptToAdd = prefix+withExt # 1st line is its own prompt
                    singleLinePoems[promptToAdd]=1
            elif cache_maintenance_mode: promptToAdd = prefix+withExt
            else: continue # can't do anything with this file
            retVal.append((0,promptToAdd,prefix+withExt))
            if emptyCheck_hack: return
            if explanationFile: filesWithExplanations[prefix+withExt]=explanationFile
            if doLimit: limitedFiles[prefix+withExt]=prefix
            lastFile = [promptFile,withExt]

cache_maintenance_mode=0 # hack so cache-synth.py etc can cache promptless words for use in justSynthesize, and words in prompts themselves
def parseSynthVocab(fname,forGUI=0):
    if not fname: return []
    langs = [secondLanguage,firstLanguage] ; someLangsUnknown = 0 ; maxsplit = 1
    ret = []
    count = 1 ; doLimit = 0 ; limitNo = 0 ; doPoetry = disablePoem = 0
    lastPromptAndWord = None
    if not fileExists(fname): return []
    if not emptyCheck_hack: doLabel("Reading "+fname)
    allLangs = list2set([firstLanguage,secondLanguage]+otherLanguages)
    for l in u8strip(read(fname)).replace("\r","\n").split("\n"):
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
            elif l2.startswith("begin poetry"): doPoetry,lastPromptAndWord,disablePoem = True,None,False
            elif l2.startswith("end poetry"): doPoetry = lastPromptAndWord = None
            elif l2.startswith("poetry vocab line"): doPoetry,lastPromptAndWord = 0,cond(lastPromptAndWord,lastPromptAndWord,0) # not None, in case we're at the very start of a poem (see "just processed"... at end)
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
        if firstLanguage==secondLanguage: langsAlreadySeen = {}
        else: langsAlreadySeen = {firstLanguage:True}
        def findPrompt():
            i=0
            while i<len(langsAndWords):
                lang,word = langsAndWords[i] ; i += 1
                isReminder = cache_maintenance_mode and len(langsAndWords)==1 and not doPoetry
                if (lang in langsAlreadySeen or isReminder) and (lang in getsynth_cache or can_be_synthesized("!synth:"+word+"_"+lang)): # (check cache because most of the time it'll be there and we don't need to go through all the text processing in can_be_synthesized)
                    if not word: continue
                    elif word[0] in wsp or word[-1] in wsp: word=word.strip(wsp) # avoid call if unnecessary
                    return strCount+word+"_"+lang, cond(isReminder,0,i)
                langsAlreadySeen[lang]=True
            return None,0
        prompt,onePastPromptIndex = findPrompt()
        if not prompt and len(langsAndWords)>1: # 1st language prompt not found; try 2nd language to 3rd language etc
            langsAlreadySeen = list2dict(otherFirstLanguages) ; prompt,onePastPromptIndex = findPrompt()
            if not prompt:
                langsAlreadySeen = {secondLanguage:True} ; prompt,onePastPromptIndex = findPrompt()
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
                  if not (doPoetry and disablePoem):
                    f=strCount+word+"_"+lang
                    if prompt==1 or prompt==f: # a file with itself as the prompt (either explicitly or by omitting any other prompt)
                        prompt=f
                        singleLinePoems[f]=1
                    ret.append((0,prompt,f))
                    if emptyCheck_hack: return ret
                    if doLimit: limitedFiles[f]="synth:"+str(limitNo)
                    if doPoetry: lastPromptAndWord = [prompt_L1only,f]
                elif doPoetry: disablePoem=1 # if one of the lines can't be synth'd, disable the rest of the poem (otherwise get wrongly connected lines, disconnected lines, or re-introduction of isolated lines that were previously part of a poem but can't be synth'd on this platform)
        if not lastPromptAndWord==None: doPoetry = 1 # just processed a "poetry vocab line" (lastPromptAndWord is either the real last prompt and word, or 0 if we were at the start)
    return ret

def sanitise_otherLanguages():
    for l in otherFirstLanguages:
        if not l in otherLanguages: otherLanguages.append(l)
    for l in otherLanguages:
        if not l in possible_otherLanguages: possible_otherLanguages.append(l)
sanitise_otherLanguages()

# Prompt file syntax: word_language.wav
# or: word_language_2.wav .. (alternatives chosen at random)
# ('word' can also be a language name)
class PromptException(Exception):
    def __init__(self,message): self.message = message
    def __repr__(self): return self.message
class AvailablePrompts(object):
    reservedPrefixes = list2set(map(lambda x:x.lower(),["whatmean","meaningis","repeatAfterMe","sayAgain","longPause","begin","end",firstLanguage,secondLanguage] + possible_otherLanguages))
    def __init__(self):
        self.lsDic = getLsDic(promptsDirectory)
        self.prefixes = {}
        for k,v in self.lsDic.items():
            if v: self.prefixes[k[:k.rfind("_")]]=1 # delete language
            else: del self.lsDic[k] # !poetry etc doesn't make sense in prompts
        self.prefixes = self.prefixes.keys()
        self.user_is_advanced = None
    def getRandomPromptList(self,promptsData,language):
        random.shuffle(self.prefixes)
        for p in self.prefixes:
            if p.lower() in self.reservedPrefixes: continue
            try:
                theList = self.getPromptList(p,promptsData,language)
                return theList
            except PromptException: pass
        raise PromptException("Can't find a non-reserved prompt suitable for language '%s'" % (language))
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
            if beginnerPrompt: r=[self.lsDic[beginnerPrompt]]
            else:
                if language in [firstLanguage,secondLanguage]: raise PromptException("Can't find "+prefix+"_"+firstLanguage+" or "+prefix+"_"+secondLanguage)
                else: raise PromptException("Can't find "+prefix+"_"+language+", "+prefix+"_"+firstLanguage+" or "+prefix+"_"+secondLanguage)
        elif not beginnerPrompt:
            # Must use advancedPrompt
            if (not self.user_is_advanced) and cond(language==secondLanguage,advancedPromptThreshold,advancedPromptThreshold2): raise PromptException("Prompt '%s' is too advanced; need '%s_%s' (unless you set %s=0 in advanced%stxt)" % (advancedPrompt,prefix,firstLanguage,cond(language==secondLanguage,"advancedPromptThreshold","advancedPromptThreshold2"),extsep))
            r=[self.lsDic[advancedPrompt]]
        elif promptsData.get(advancedPrompt,0) >= cond(language==secondLanguage,advancedPromptThreshold,advancedPromptThreshold2): r=[self.lsDic[advancedPrompt]]
        elif promptsData.get(advancedPrompt,0) >= cond(language==secondLanguage,transitionPromptThreshold,transitionPromptThreshold2): r=[self.lsDic[advancedPrompt], self.lsDic[beginnerPrompt]]
        else: r=[self.lsDic[beginnerPrompt]]
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
# Do NOT construct availablePrompts here - if a warning is printed (e.g. can't find a synth) then it might go to the wrong place if GUI has not yet started.  Constructing moved to lesson_loop().

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


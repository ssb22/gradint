# This file is part of the source code of
# gradint v0.9988 (c) 2002-2013 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of lessonplan.py - tracking progress and planning a lesson

class ProgressDatabase(object):
    def __init__(self,alsoScan=1,fromString=0):
        self.data = [] ; self.promptsData = {}
        self.unavail = [] ; self.saved_completely = 0
        if fromString or not self._load_from_binary():
            self._load_from_text(fromString)
            if self.data and not fromString: self.save_binary(self.data) # even before starting, to save time if they press Cancel and then try loading again without futher progressFile changes
        self.oldPromptsData = self.promptsData.copy() # in case have to save partial (see below)
        if alsoScan:
          global is_first_lesson ; is_first_lesson = (not self.data and not self.unavail) # hack
          self.data += self.unavail # because it might have become available again
          self.unavail = mergeProgress(self.data,scanSamples()+parseSynthVocab(vocabFile))
          if not cache_maintenance_mode:
            doLabel("Checking transliterations")
            tList = {}
            def addVs(ff,dirBase):
                if dirBase: dirBase += os.sep
                if dirBase+ff in variantFiles:
                   if os.sep in ff: ffpath=ff[:ff.rfind(os.sep)+1]
                   else: ffpath=""
                   variantList=map(lambda x:ffpath+x,variantFiles[dirBase+ff])
                else: variantList = [ff]
                l=languageof(ff)
                for f in variantList:
                  if f.lower().endswith(dottxt): text=u8strip(read(dirBase+f)).strip(wsp)
                  elif f.find("!synth")==-1: continue # don't need to translit. filenames of wav's etc
                  else: text = textof(f)
                  if not l in tList: tList[l]={}
                  tList[l][text]=1
            for ff in availablePrompts.lsDic.values(): addVs(ff,promptsDirectory)
            for _,l1,l2 in self.data:
                if not type(l1)==type([]): l1=[l1]
                for ff in l1+[l2]: addVs(ff,samplesDirectory)
            doLabel("Transliterating")
            for lang,dic in tList.items():
                s = get_synth_if_possible(lang,0)
                if s and hasattr(s,"update_translit_cache"): s.update_translit_cache(lang,dic.keys())
        self.didScan = alsoScan
    def _load_from_binary(self):
        if pickledProgressFile and fileExists(pickledProgressFile):
            if pickle and not (fileExists(progressFile) and os.stat(progressFile)[8] > os.stat(pickledProgressFile)[8]): # we can unpickle the binary version, and text version has not been manually updated since it, so do this
                global firstLanguage, secondLanguage, otherLanguages
                if compress_progress_file or (unix and got_program("gzip")):
                    if paranoid_file_management: open(pickledProgressFile) # ensure ready
                    f = os.popen('gzip -fdc "'+pickledProgressFile+'"',"rb")
                else: f=open(pickledProgressFile,"rb")
                try: thingsToSet, tup = pickle.Unpickler(f).load()
                except: return False # probably moved to a different Python version or something
                exec(thingsToSet)
                return True
            # otherwise drop out and return None
    def _load_from_text(self,fromString=0):
        if fromString: expr=fromString
        elif fileExists(progressFile):
            if compress_progress_file or (unix and got_program("gzip")):
                if paranoid_file_management: open(progressFile) # ensure ready
                expr = os.popen('gzip -fdc "'+progressFile+'"',"rb").read()
            else: expr = read(progressFile)
        else: expr = None
        if expr:
            expr = u8strip(expr) # just in case progress.txt has been edited in Notepad
            # First, try evaluating it as self.data (legacy progress.txt from older versions).  If that doesn't work, execute it (newer versions).
            global firstLanguage, secondLanguage, otherLanguages
            try: self.data = eval(expr)
            except TypeError: raise Exception(progressFile+" has not been properly decompressed") # 'expected string without null bytes'
            except SyntaxError:
                try: import codeop
                except: codeop = 0
                if codeop: # try a lower-memory version (in case text file has been edited by hand and we're on NSLU2 or something) - don't compile all of it at once
                    lineCache = []
                    for l in expr.replace("\r\n","\n").split("\n"):
                        lineCache.append(l)
                        if lineCache[-1].endswith(","): continue # no point trying to compile if it's obviously incomplete
                        code = codeop.compile_command("\n".join(lineCache))
                        if code:
                            lineCache = []
                            exec code
                else: exec(expr)
            del expr
        # Remove legacy extentions in promptsData (needed only when loading from text, as this was before pickledProgressFile was added)
        for k in self.promptsData.keys():
            if k.endswith(dotwav) or k.endswith(dotmp3):
                self.promptsData[k[:-len(dotwav)]]=self.promptsData[k]
                del self.promptsData[k]
    def save(self,partial=0):
        if need_say_where_put_progress: show_info("Saving "+cond(partial,"partial ","")+"progress to "+progressFile+"... ")
        else: show_info("Saving "+cond(partial,"partial ","")+"progress... ")
        global progressFileBackup
        # Remove 0-repeated items (helps editing by hand)
        data = [] # don't use self.data - may want to make another lesson after saving
        for a,b,c in self.data:
            if a: data.append(denumber_filelists(a,b,c))
        data.sort(cmpfunc) # to normalise when using diff etc
        if progressFileBackup:
            try:
                import shutil
                shutil.copy2(progressFile,progressFileBackup) # preserve timestamp etc if shutil is available
            except:
                try: write(progressFileBackup,read(progressFile))
                except IOError: pass # maybe progressFile not made yet
            progressFileBackup = None
        while True:
          try:
            if compress_progress_file:
              if paranoid_file_management: fn=os.tempnam() # on some ftpfs setups gzip can fail causing silent corruption
              else: fn=progressFile
              f=os.popen('gzip -9 > "'+fn+'"','w')
            else: f = open(progressFile,'w')
            f.write(progressFileHeader)
            f.write("firstLanguage=\"%s\"\nsecondLanguage=\"%s\"\n# otherLanguages=%s\n" % (firstLanguage,secondLanguage,otherLanguages)) # Note: they're declared "global" above (and otherLanguages commented out here for now, since may add to it in advanced.txt) (Note also save_binary below.)
            if self.didScan: f.write("# collection=%d done=%d left=%d lessonsLeft=%d\n" % (len(self.data),len(data),len(self.data)-len(data),(len(self.data)-len(data)+maxNewWords-1)/maxNewWords))
            prettyPrintLongList(f,"self.data",data)
            f.write("self.promptsData=") ; pprint.PrettyPrinter(indent=2,width=60,stream=f).pprint(self.promptsData)
            prettyPrintLongList(f,"self.unavail",self.unavail)
            f.close()
            if compress_progress_file and paranoid_file_management: write(progressFile,read(fn)),os.remove(fn)
            self.save_binary(data)
          except IOError: # This can happen for example on some PocketPC devices if you reconnect the power during progress save (which is likely if you return the device to the charger when lesson finished)
            if app or appuifw or android:
              if getYN("I/O fault when saving progress. Retry?"): continue
              # TODO else try to restore the backup?
            else: raise
          break
        if not partial: self.saved_completely = 1
        if not app and not appuifw and not android: show_info("done\n")
    def save_binary(self,data): # save a pickled version if possible (no error if not)
        if not (pickledProgressFile and pickle): return
        try:
            if compress_progress_file:
              if paranoid_file_management: fn=os.tempnam()
              else: fn=pickledProgressFile # TODO near-duplicate code with above
              f=os.popen('gzip -9 > "'+fn+'"','wb')
            else: f = open(pickledProgressFile,'wb')
            pickle.Pickler(f,-1).dump(("self.data,self.promptsData,self.unavail,firstLanguage,secondLanguage = tup", (data,self.promptsData,self.unavail,firstLanguage,secondLanguage)))
            f.close()
            if compress_progress_file and paranoid_file_management: write(pickledProgressFile,read(fn)),os.remove(fn)
        except IOError: pass # OK if not got permissions to do it (NB need to catch the write as well because popen won't throw, and don't have to worry about a corrupted partial binary because loader would ignore it)
    def savePartial(self,filesNotPlayed):
        curPD,curDat = self.promptsData, self.data[:] # in case want to save a more complete one later
        self.promptsData = self.oldPromptsData # partial recovery of prompts not implemented
        if hasattr(self,"previous_filesNotPlayed"):
            i=0
            while i<len(filesNotPlayed):
                if filesNotPlayed[i] in self.previous_filesNotPlayed: i+=1
                else: del filesNotPlayed[i] # cumulative effects if managed to play it last time but not this time (and both lessons incomplete)
        self.previous_filesNotPlayed = filesNotPlayed = list2set(filesNotPlayed)
        if not filesNotPlayed:
            # actually done everything on overlaps
            self.promptsData=curPD
            return self.save()
        changed = 0
        for i in xrange(len(self.data)):
            if type(self.data[i][1])==type([]): l=self.data[i][1][:]
            else: l=[self.data[i][1]]
            l.append(self.data[i][2])
            found=0
            for ii in l:
              if ii in filesNotPlayed:
                  self.data[i] = self.oldData[i]
                  found=1 ; break
            if not found and not self.data[i] == self.oldData[i]: changed = 1
        if changed: self.save(partial=1)
        elif app==None and not appuifw and not android: show_info("No sequences were fully complete so no changes saved\n")
        self.promptsData,self.data = curPD,curDat
    def makeLesson(self):
        global maxLenOfLesson
        self.l = Lesson()
        self.data.sort(cmpfunc) ; jitter(self.data)
        self.oldData = self.data[:] # for handling interrupts & partial progress saves
        self.exclude = {} ; self.do_as_poem = {}
        # First priority: Recently-learned old words
        # (But not too many - want room for new words)
        num=self.addToLesson(1,knownThreshold,1,recentInitialNumToTry,maxReviseBeforeNewWords)
        if num < maxReviseBeforeNewWords:
            # Weren't enough recently-learned old words
            # Do try to add SOMETHING before the new words
            num += self.addToLesson(knownThreshold,reallyKnownThreshold,1,recentInitialNumToTry,maxReviseBeforeNewWords-num)
            if num < maxReviseBeforeNewWords: self.addToLesson(reallyKnownThreshold,-1,1,1,maxReviseBeforeNewWords-num)
        # Now some new words
        self.addToLesson(0,0,newWordsTryAtLeast,newInitialNumToTry,maxNewWords)
        # Now some more recently-learned old words
        self.addToLesson(1,knownThreshold,1,recentInitialNumToTry,-1)
        self.addToLesson(knownThreshold,reallyKnownThreshold,1,recentInitialNumToTry,-1)
        # Finally, fill in the gaps with ancient stuff (1 try only of each)
        # But watch out for known poems
        poems, self.responseIndex = find_known_poems(self.data)
        for p in poems:
            for l in p: self.do_as_poem[self.responseIndex[l]] = p
        self.addToLesson(reallyKnownThreshold,-1,1,1,-1)
        l = self.l ; del self.l, self.responseIndex, self.do_as_poem
        if not l.events: raise Exception("Didn't manage to put anything in the lesson")
        if commentsToAdd: l.addSequence(commentSequence())
        if orderlessCommentsToAdd:
            for c in orderlessCommentsToAdd:
                try:
                    l.addSequence([GluedEvent(Glue(1,maxLenOfLesson),fileToEvent(c,""))])
                except StretchedTooFar:
                    show_info(("Was trying to add %s\n" % (c,)),True)
                    raise
        # Add note on "long pause", for beginners
        longpause = "longpause_"+firstLanguage
        if not advancedPromptThreshold and not longpause in availablePrompts.lsDic: longpause = "longpause_"+secondLanguage
        o=maxLenOfLesson ; maxLenOfLesson = max(l.events)[0]
        if longpause in availablePrompts.lsDic and self.promptsData.get(longpause,0)==0:
            try:
                def PauseEvent(): return fileToEvent(availablePrompts.lsDic[longpause],promptsDirectory)
                firstPauseMsg = PauseEvent()
                # the 1st potentially-awkward pause is likely to be a beepThreshold-length one
                l.addSequence([GluedEvent(Glue(1,maxLenOfLesson),CompositeEvent([firstPauseMsg,Event(max(5,beepThreshold-firstPauseMsg.length))]))])
                while True:
                    l.addSequence([GluedEvent(Glue(1,maxLenOfLesson),CompositeEvent([PauseEvent(),Event(50)]))])
                    self.promptsData[longpause] = 1
            except StretchedTooFar: pass
        maxLenOfLesson = o
        # Add "this is the end"
        try:
            pl=availablePrompts.getPromptList("end",self.promptsData,secondLanguage)
        except PromptException: pl = []
        t,event = max(l.events)
        t += event.length
        for p in pl:
            end_event = fileToEvent(p,promptsDirectory)
            l.events.append((t,end_event))
            t += end_event.length
        if not pl and fileExists(promptsDirectory+os.sep+"end"+dotwav):
            l.events.append((t,SampleEvent(promptsDirectory+os.sep+"end"+dotwav)))
            show_warning("Warning: Using legacy end"+dotwav+" - please change it to end_"+firstLanguage+dotwav+" and end_"+secondLanguage+dotwav+" (or "+extsep+"txt if you have synthesis)")
        l.cap_max_lateness()
        return l
    def addToLesson(self,minTimesDone=0,maxTimesDone=-1,minNumToTry=0,maxNumToTry=0,maxNumToAdd=-1):
        # Service routine - adds some words to the lesson
        # Words added must conform to the criteria specified
        # (i.e. range of how many times they've been done
        # before, and how many tries we can fit in now)
        # This is called a few times with different criteria
        # for the different priorities
        if maxNumToAdd==None: return 0
        numberAdded = 0
        newWordTimes = {}
        for numToTry in range(maxNumToTry,minNumToTry-1,-1):
            numFailures = 0 ; startTime = time.time() # for not taking too long
            for i in xrange(len(self.data)):
                if maxNumToAdd>-1 and numberAdded >= maxNumToAdd: break # too many
                if i in self.exclude: continue # already had it
                (timesDone,promptFile,zhFile)=self.data[i]
                if timesDone < minTimesDone or (maxTimesDone>=0 and timesDone > maxTimesDone): continue # out of range this time
                if timesDone >= knownThreshold: thisNumToTry = min(random.choice([2,3,4]),numToTry)
                else: thisNumToTry = numToTry
                if timesDone >= randomDropThreshold and random.random() <= calcDropLevel(timesDone):
                    # dropping it at random
                    self.exclude[i] = 1 # pretend we've done it
                    continue
                if i in self.do_as_poem:
                    # this is part of a "known poem" and let's try to do it in sequence
                    self.try_add_poem(self.do_as_poem[i]) ; continue
                oldPromptsData = self.promptsData.copy()
                seq=anticipationSequence(promptFile,zhFile,timesDone,timesDone+thisNumToTry,self.promptsData,introductions(zhFile,self.data))
                seq[0].timesDone = timesDone # for diagram.py (and now status messages) to know if it's a new word
                global earliestAllowedEvent ; earliestAllowedEvent = 0
                if not timesDone and type(promptFile)==type([]):
                    # for poems: if any previously-added new word makes part of the prompt, try to ensure this one is introduced AFTER that one
                    for f,t in newWordTimes.items():
                        if f in promptFile: earliestAllowedEvent = max(earliestAllowedEvent,t)
                if not timesDone: newWordTimes[zhFile] = maxLenOfLesson # by default (couldn't fit it in).  (add even if not type(promptFile)==type([]), because it might be a first line)
                try: self.l.addSequence(seq)
                except StretchedTooFar: # If this happens, couldn't fit the word in anywhere.  If this is "filling in gaps" then it's likely that we won't be able to fit in any more words this lesson, so stop trying.
                    earliestAllowedEvent = 0 # because there may be addSequence's outside this method
                    self.promptsData = oldPromptsData
                    numFailures += 1
                    if numFailures > 2 and time.time()>startTime+1: # TODO these numbers need to be constants.  (the +1 could also be cond(soundCollector,10,1) but we might want offline-generation to run fast also and it doesn't seem to make much difference)
                        break # give up trying to add more (we're taking too long)
                    else: continue
                except IOError: # maybe this file isn't accessible at the moment; keep the progress data though
                    show_warning("Excluding %s (problems reading)" % str(zhFile))
                    earliestAllowedEvent = 0 # because there may be addSequence's outside this method
                    self.exclude[i] = 1 # save trouble
                    continue
                numFailures = 0
                earliestAllowedEvent = 0 # because there may be addSequence's outside this method
                numberAdded = numberAdded + 1
                self.exclude[i] = 1
                # Keep a count
                if not timesDone: self.l.newWords += 1
                else: self.l.oldWords += 1
                self.data[i]=(timesDone+thisNumToTry,promptFile,zhFile)
                if not timesDone: newWordTimes[zhFile] = seq[0].getEventStart(0) # track where it started
        return numberAdded
    def try_add_poem(self,poem):
        poemSequence = []
        isPrefix=0 # keep choosing until we get an instruction that's a prefix
        while not isPrefix: i,isPrefix = randomInstruction(2,self.promptsData,languageof(poem[0])) # 2 so not listen-repeat or sayAgain and not drop-altogether (assuming sensible thresholds)
        poemSequence.append(filesToEvents(i,promptsDirectory))
        poemSequence.append(fileToEvent(poem[0]))
        for line in poem:
            e=fileToEvent(line)
            poemSequence.append(Event(e.length))
            poemSequence.append(e)
            self.exclude[self.responseIndex[line]] = 1 # (don't try to add it again this lesson, whether successful or not)
        poemSequence = [GluedEvent(initialGlue(),CompositeEvent(poemSequence))]
        poemSequence[0].endseq = False # boolean 'is it a new word'
        try: self.l.addSequence(poemSequence)
        except StretchedTooFar: return
        self.l.oldWords += 1 # have to only count it as one due to endseq handling
        for line in poem: self.data[self.responseIndex[line]]=(self.data[self.responseIndex[line]][0]+1,)+self.data[self.responseIndex[line]][1:]
    def veryExperienced(self):
        # used for greater abbreviation in the prompts etc
        x = getattr(self,'cached_very_experienced',None)
        if x==None:
            covered = 0
            for timesDone,promptFile,zhFile in self.data:
                if timesDone: covered += 1
            x = (covered > 1000) # arbitrary
            self.cached_very_experienced = x
        return x
    def message(self):
        covered = 0 ; total = len(self.data)
        actualCovered = 0 ; actualTotal = 0
        for timesDone,promptFile,zhFile in self.data:
            if timesDone:
                covered += 1
                if zhFile.find(exclude_from_coverage)==-1: actualCovered += 1
            if zhFile.find(exclude_from_coverage)==-1: actualTotal += 1
        l=cond(app,localise,lambda x:x)
        toRet = (l("You have %d words in your collection") % total)
        if not total==actualTotal: toRet += (" (actually %d)" % actualTotal)
        if covered:
            toRet += ("\n("+(l("%d new words + %d old words") % (total-covered,covered))+")")
            if not covered==actualCovered: toRet += (" (actually %d new %d old)" % (actualTotal-actualCovered,actualCovered))
        return toRet

def prettyPrintLongList(f,thing,data):
    # help the low-memory compile by splitting it up (also helps saving on slow machines, see below)
    step = 50 # number of items to do in one go
    if winCEsound: p=0 # don't use WinCE's PrettyPrinter here - it inconsistently escapes utf8 sequences (result can't reliably be edited in MADE etc)
    else: p=pprint.PrettyPrinter(indent=2,width=60,stream=f)
    for start in range(0,len(data),step):
        if start: f.write(thing+"+=")
        else: f.write(thing+"=")
        if p:
            t = time.time()
            p.pprint(data[start:start+step])
            if not start and (time.time()-t)*(len(data)/step) > 5: p=0 # machine is too slow - use faster version on next iteration
        else: # faster version - not quite as pretty
            f.write("[")
            for d in data[start:start+step]: f.write("  "+repr(d)+",\n")
            f.write("]\n")

def calcDropLevel(timesDone):
    # assume timesDone > randomDropThreshold
    if timesDone > randomDropThreshold2:
        return randomDropLevel2
    # or linear interpolation between the two thresholds
    return dropLevelK * timesDone + dropLevelC
# K*rdt1 + c = l1, K*rdt2 + c = l2
# K = (l2-l1)/(rdt2-rdt1)
# c = l1 - K*rdt1
try:
    dropLevelK = (randomDropLevel2-randomDropLevel)/(randomDropThreshold2-randomDropThreshold)
    dropLevelC = randomDropLevel-dropLevelK*randomDropThreshold
except ZeroDivisionError: # thresholds are the same
    dropLevelK = 0
    dropLevelC = randomDropLevel

def cmpfunc(x,y):
    # Comparison function for sorting progress data.  It's a hack for dealing with the problem caused by the ASCII code of '-' being lower than that of '/', so "directory-2/file" comes before "directory/file" unless hacked with this.  NB needs to be fast - don't "".join() unnecessarily.
    r = cmpfunc_test(x[0],y[0])
    if r: return r # skipping the rest if x[0]!=y[0]
    if x[0]: return cmpfunc_test(x,y) # our special order is needed only for new words (to ensure correct order of introduction)
    def my_toString(x):
        if type(x)==type([]): return "".join(x)
        else: return x
    x2 = (my_toString(x[1]).replace(os.sep,chr(0)), my_toString(x[2]).replace(os.sep,chr(0)))
    y2 = (my_toString(y[1]).replace(os.sep,chr(0)), my_toString(y[2]).replace(os.sep,chr(0)))
    return cmpfunc_test(x2,y2)
def cmpfunc_test(x,y):
    if x < y: return -1
    elif x > y: return 1
    else: return 0

def denumber_filelists(r,x,y):
    if type(x)==type([]): x=map(lambda z:denumber_synth(z),x)
    else: x=denumber_synth(x)
    if type(y)==type([]): y=map(lambda z:denumber_synth(z),y)
    else: y=denumber_synth(y)
    return (r,x,y)
def denumber_synth(z,also_norm_extsep=0):
    zf = z.find("!synth:")
    if zf>-1:
        z=lower(z[zf:]) # so ignores the priority-number it had (because the vocab.txt file might have been re-organised hence changing all the numbers).  Also a .lower() so case changes don't change progress.  (Old versions of gradint said .lower() when parsing vocab.txt, but this can cause problems with things like Mc[A-Z].. in English espeak)
        if z.endswith(dotwav) or z.endswith(dotmp3): return z[:z.rindex(extsep)] # remove legacy extensions from synth vocab
    elif also_norm_extsep: return z.replace("\\","/").replace(".","/") # so compares equally across platforms with os.sep and extsep differences
    return z

def norm_filelist(x,y):
    def noext(x): return (x+extsep)[:x.rfind(extsep)] # so user can change e.g. wav to mp3 without disrupting progress.txt
    if type(x)==type([]): x=tuple(map(lambda z:denumber_synth(noext(z),1),x))
    else: x=denumber_synth(noext(x),1)
    if type(y)==type([]): y=tuple(map(lambda z:denumber_synth(noext(z),1),y))
    else: y=denumber_synth(noext(y),1)
    return (x,y)
def mergeProgress(progList,scan):
    # Merges a progress database with a samples scan, to
    # pick up any new samples that were added since last
    # time.  Appends to progList.  Return value see below.
    proglistDict = {} ; scanlistDict = {} ; n = 0
    while n<len(progList):
        i,j,k = progList[n]
        if i:
            proglistDict[norm_filelist(j,k)]=n
            # (DO need to call denumber_synth (called by
            # norm_filelist) on existing data, because might
            # be loading a legacy progress.txt which has
            # numbers before !synth) (as well as the .lower() thing)
            n += 1
        else: del progList[n]
        # (take out any 0s - add them back in only if still
        # in the scan.  This makes re-organisation etc
        # easier.  NB this duplicates the functionality in
        # save(), but useful if upgrading from an old
        # version.)
    renames = {}
    for (_,j,k) in scan:
        key = norm_filelist(j,k)
        if key in proglistDict:
            # an existing item - but in the case of synth'd vocab, we need to take the capitals/lower-case status from the scan rather than from the progress file (see comment above in denumber_synth) so:
            progList[proglistDict[key]]=(progList[proglistDict[key]][0],j,k)
        elif type(key[0])==type("") and (key[0]+key[1]).find("!synth")==-1 and ("_" in key[0] and "_" in key[1]):
            # a file which might have been renamed and we may be able to catch a case of appending text to digits (but we don't (yet?) support doing this with poetry, hence the type() precondition)
            # TODO document that we do this in samples/readme and possibly the autosplit scripts etc, although nowadays recording GUI is more likely to be used and it lends itself to rename-all-but-digits.
            normK = key[1]
            lastDirsep = normK.rfind(os.sep)
            ki = len(normK)-1 ; found=0
            while ki>lastDirsep:
                while ki>lastDirsep and not "0"<=normK[ki]<="9": ki -= 1
                if ki<=lastDirsep: break
                key2 = (key[0][:ki+1]+key[0][key[0].rindex("_"):],key[1][:ki+1]+key[1][key[1].rindex("_"):])
                if key2 in proglistDict:
                    if not key2 in renames: renames[key2] = []
                    renames[key2].append((j,k))
                    found=1 ; break
                while ki>lastDirsep and "0"<=normK[ki]<="9": ki -= 1
            if not found: progList.append((0,j,k)) # new item
        else: progList.append((0,j,k)) # ditto
        scanlistDict[key]=1
    for k,v in renames.items():
        if k in scanlistDict or len(v)>1: # can't make sense of this one - just add the new stuff
            for jj,kk in v: progList.append((0,jj,kk))
        else: progList[proglistDict[k]]=(progList[proglistDict[k]][0],v[0][0],v[0][1])
    # finally, separate off any with non-0 progress that are
    # no longer available (keep them because they may come
    # back later, but useful to make the distinction in case
    # want to manually edit progress.txt)
    n = 0 ; unavailList = []
    while n<len(progList):
        i,j,k = progList[n]
        if not norm_filelist(j,k) in scanlistDict:
            unavailList.append((i,j,k))
            del progList[n]
        else: n += 1
    return unavailList

def jitter(list):
    # Adds some random 'jitter' to a list (in-place)
    # Assumes item is a tuple and item[0] might be ==
    # Doesn't touch "new" words (tries==0) (assumes they're
    # all at top, so doesn't have to test for new word after
    # already-tried word).
    # HOWEVER, now handles the 'limit' feature for new words

#     swappedLast = 0
#     for i in range(len(list)-1):
#         if list[i][0] and ((list[i][0] == list[i+1][0] and random.choice([1,2])==1) or (not list[i][0] == list[i+1][0] and random.choice([1,2,3,4,5,6])==1 and not swappedLast)):
#             x = list[i]
#             del list[i]
#             list.insert(i+1,x)
#             swappedLast = 1
#         else: swappedLast = 0

    # Algorithm below implemented 2005-04-13 to deal with
    # larger vocabularies (thousands of words - previously
    # only the first few hundred ever got considered even
    # with random drop).  Divide words into groups and
    # shuffle each group.  To begin with each group is the
    # items that have the same repetition count, but as this
    # gets large we rapidly tolerate increasing differences
    # in repetition count in the same group.
    i = 0 ; groupStart = -1
    while i <= len(list):
        if i<len(list) and not list[i][0]: pass # leave it
        elif i<len(list) and groupStart<0:
            groupStart = i
            try:
                incrementThreshold = int(math.exp(list[groupStart][0]*shuffleConstant/(randomDropThreshold+1)-shuffleConstant)) # (not sure about the +1) (NB strict int, NOT nearest)
            except OverflowError: incrementThreshold=sys.maxint
        elif groupStart>=0 and (i==len(list) or list[i][0] - list[groupStart][0] > incrementThreshold):
            l2 = list[groupStart:i] ; random.shuffle(l2)
            del list[groupStart:i]
            for item in l2: list.insert(groupStart,item)
            groupStart = -1
            continue
        i += 1

    # Handle 'limit' feature: Of the new words that are
    # limited, put all but limit_words of them at the end of
    # the list (but this is done for EACH limit).
    # Also, all but 1 of 3rd, 4th etc languages to end (and rely on
    # directory order not to introduce them too early)
    # -> latter has now been commented out because do sometimes
    # need to work on them more quickly, and can limit manually
    limitCounts = {} ; i = 0 ; imax = len(list)
    while i < imax:
        if list[i][0]==0 and (list[i][-1] in limitedFiles): # or not languageof(list[i][2])==secondLanguage):
            # if not languageof(list[i][2])==secondLanguage: countNo="other-langs"
            # else:
            countNo = limitedFiles[list[i][-1]]
            if not countNo in limitCounts: limitCounts [countNo] = 0
            limitCounts [countNo] += 1
            # (below is a hack: if already moved something, set limit_words to 1.  May want to do it better than that e.g. go back and ensure the first thing only left 1 as well, or share out limit_words among any concurrently available new items that are just about to be introduced)
            if limitCounts [countNo] > cond(imax==len(list),limit_words,1) or (countNo=="other-langs" and limitCounts [countNo] > 1):
                list.append(list[i])
                del list[i]
                imax -= 1 # don't re-check the ones already moved to the end
                continue # no need to increment i
        i += 1

def find_known_poems(progressData):
    # If every line of a poem is known then it might be better to recite the whole thing in sequence
    # This function goes through progressData and extracts "known poems".  Returns: (a) a list of poems (each being a list of lines), (b) dictionary line -> index into progressData
    nextLineDic = {} # line -> next line
    responseIndex = {} # target response -> index into progressData
    hasPreviousLine = {} # line -> does it have a previous line
    for i in xrange(len(progressData)):
        response = progressData[i][2]
        responseIndex[response] = i
        if type(progressData[i][1])==type([]): line=progressData[i][1][cond(len(progressData[i][1])==2,0,-1)] # (the L2 is normally in last position, but it's in 1st position in a 2-item list - see the "line 1 doesn't have L1 but line 2 does" comment)
        else: line=progressData[i][1]
        if languageof(line)==languageof(response) and not line==response: # looks like part of a poem (and not the 'beginning' first line).  (Don't need any extra code to avoid mistaking 2nd-language-to-2nd-language word pairs as poems, because responseIndex will not get the "first line" and the "poem" won't be viable.)
            nextLineDic[line]=response # TODO check what would happen if 2 different poems in vocab.txt share an identical line (or if responseIndex is ambiguous in any way)
            hasPreviousLine[response]=True
    poems = []
    for poemFirstLine in filter(lambda x:not x in hasPreviousLine,nextLineDic.keys()):
        poemLines = [] ; line = poemFirstLine
        poem_is_viable = True
        while True:
            poemLines.append(line)
            if not line in responseIndex or progressData[responseIndex[line]][0] < reallyKnownThreshold:
                poem_is_viable = False ; break # whole poem not in database yet, or is but not well-rehearsed
            if not line in nextLineDic: break
            line = nextLineDic[line]
        if poem_is_viable: poems.append(poemLines)
    return poems, responseIndex

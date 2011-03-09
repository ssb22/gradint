# This file is part of the source code of
# gradint v0.9969 (c) 2002-2011 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of sequence.py - make individual graduated-interval sequences to be interleaved into the lesson

def randomInstruction(numTimesBefore,promptsData,language):
    if not numTimesBefore: return (availablePrompts.getPromptList("repeatAfterMe",promptsData,language),0)
    if numTimesBefore==1: return (availablePrompts.getPromptList("sayAgain",promptsData,language),1)
    if (dbase.veryExperienced() and numTimesBefore>=reallyKnownThreshold) or (meaningTestThreshold and numTimesBefore>meaningTestThreshold and not random.choice([1,2,3])==1):
        if language==secondLanguage: return (None,1) # no instruction needed
        else: return (availablePrompts.getPromptList(language,promptsData,language),1) # just need the language name
    r = availablePrompts.getRandomPromptList(promptsData,language)
    # horrible hack: whatSay goes after the 1st-language
    # word; others go before
    for i in r:
        if i.startswith("whatSay_"): return (r,0)
    return (r,1)

def anticipation(promptFile,zhFile,numTimesBefore,promptsData):
    # Returns an item in an "anticipation sequence"
    # i.e. an event made up of prompt, 1st language, &
    # 2nd language, perhaps repeated 2-3 times depending
    # on progress.
    # 
    # (Note: numTimesBefore is from ALL LESSONS)
    # Set some parameters depending on numTimesBefore
    instructions, instrIsPrefix = randomInstruction(numTimesBefore,promptsData,languageof(zhFile))
    if instructions: instructions = map(lambda x:fileToEvent(x,promptsDirectory), instructions)
    else: instructions = [Event(1)]
    zhEvent = filesToEvents(zhFile) ; secondPause = 1+zhEvent.length
    promptEvent = filesToEvents(promptFile)
    if not numTimesBefore: anticipatePause = 1
    else: anticipatePause = secondPause
    # work out number of repetitions needed.  not sure if this should be configurable somewhere.
    first_repeat_is_unessential = 0
    if not numTimesBefore: # New word.  If there are L2 variants, introduce them all if possible.
        numVariants = min(3,len(variantFiles.get(samplesDirectory+os.sep+zhFile,[0]))) # TODO really max to 3? or 4? or .. ?
        if numVariants>1 and lessonIsTight(): numVariants = 1 # hack
        numRepeats = numVariants + cond(numVariants>=cond(availablePrompts.user_is_advanced,2,3),0,1)
    elif numTimesBefore == 1: numRepeats = 3
    elif numTimesBefore < 5: numRepeats = 2
    elif numTimesBefore < 10:
        numRepeats = random.choice([1,2])
        if numRepeats==2: first_repeat_is_unessential = 1
    else: numRepeats = 1
    if numRepeats==1:
      k,f = synthcache_lookup(zhFile,justQueryCache=1)
      if f and k[0]=="_" and not textof(zhFile) in subst_synth_counters:
        # Hack: an experimental cache entry but only 1 repetition - what do we do?
        c=random.choice([1,2,3])
        if c==1: pass # do nothing
        elif c==2: # have the word twice
            numRepeats = 2
            first_repeat_is_unessential = 1
        elif c==3: subst_synth_counters[textof(zhFile)]=1 # so it uses the cached version
    # Now ready to go
    theList = []
    if instrIsPrefix: theList = instructions
    theList.append(promptEvent)
    if promptFile==zhFile and not promptFile in singleLinePoems:
        # A multi-line poem with no first-language prompts, so we're using each fragment as a prompt for the next, but the first fragment is its own prompt, which means that 'prompt' is ambiguous.  Say "beginning" to disambiguate it.
        theList = theList + map(lambda x:fileToEvent(x,promptsDirectory), availablePrompts.getPromptList("begin",promptsData,languageof(zhFile)))
    if not instrIsPrefix: theList += instructions
    origZhEvent = zhEvent
    for i in range(numRepeats):
        if i:
            # re-generate zhEvent, in case using variants or cache sporadically or using first_repeat_is_unessential
            zhEvent = filesToEvents(zhFile)
            secondPause = 1+zhEvent.length
        theList.append(Event(anticipatePause))
        # (if first_repeat_is_unessential and we're running more than 1sec late, can drop the 1st repetition and pause after it without consequence)
        if i==1 and first_repeat_is_unessential: theList[-1].importance,theList[-1].max_lateness = 0,1 # the pause after the 1st repetition
        theList.append(zhEvent)
        if i==0 and first_repeat_is_unessential:
            theList[-1].setOnLeaves('max_lateness',1) # the 1st repetition itself
            theList[-1].setOnLeaves('wordToCancel','') # so it doesn't register as needing to cancel anything
            theList[-1].setOnLeaves('importance',0) # and doesn't try to cap the max lateness of earlier events
        anticipatePause = secondPause
    theList.append(Event(1))
    extraPauseAfter = random.choice([0,1,2])
    if extraPauseAfter:
        theList.append(Event(extraPauseAfter))
        theList[-1].importance,theList[-1].max_lateness = 0,1
    if not numTimesBefore:
        explanation = explanations(zhFile)
        if explanation:
            theList.insert(1,origZhEvent)
            theList.insert(1,explanation)
            theList.insert(1,origZhEvent)
    return CompositeEvent(theList)

def reverseAnticipation(promptFile,zhFile,promptsData):
    # Returns a "what does this mean" test
    zhEvent = filesToEvents(zhFile)
    promptEvent = filesToEvents(promptFile)
    theList = []
    theList.append(zhEvent)
    for p in availablePrompts.getPromptList("whatmean",promptsData,languageof(zhFile)): theList.append(fileToEvent(p,promptsDirectory))
    theList.append(Event(1))
    for p in availablePrompts.getPromptList("meaningis",promptsData,languageof(zhFile)): theList.append(fileToEvent(p,promptsDirectory))
    theList.append(promptEvent)
    theList.append(Event(random.choice([1,2,3])))
    return CompositeEvent(theList)

def languageof(file):
    assert "_" in file, "no _ in %s" % (file,)
    s=file[file.rindex("_")+1:]
    if extsep in s: return s[:s.rindex(extsep)]
    else: return s

def commentSequence():
    sequence = []
    for c in commentsToAdd:
        sequence.append(GluedEvent(Glue(1,maxLenOfLesson),fileToEvent(c,"")))
    return sequence

def anticipationSequence(promptFile,zhFile,start,to,promptsData,introList):
    # Returns a sequence of "anticipations" (as above) with
    # graduated-interval glue between the items
    # (try number from 'start' to 'to', EXCLUDING 'to')
    sequence = []
    # First one has initialGlue() whatever the value of 'start' is
    if meaningTestThreshold and to==start+1 and start>meaningTestThreshold and random.choice([1,2])==1 and not type(promptFile)==type([]) and promptFile.find("_"+firstLanguage+extsep)>=0:
        # *** not sure about that condition - should the random be more biased?
        # (the type() and following condition is a hack that ensures this is not used for poetry etc where there are composite prompts or the prompt is the previous line.  TODO would be better to keep track of which samples are poetic, because the above breaks down on the first line of a poem that has a translation into the first language because that looks like a normal prompt/response - but ok for now)
        firstItem = reverseAnticipation(promptFile,zhFile,promptsData)
    else: firstItem = anticipation(promptFile,zhFile,start,promptsData)
    if introList: firstItem=CompositeEvent(introList+[firstItem])
    sequence.append(GluedEvent(initialGlue(),firstItem))
    for i in range(start+1,to):
        sequence.append(GluedEvent(glueBefore(i),anticipation(promptFile,zhFile,i,promptsData)))
    return sequence

def glueBefore(num):
    global is_first_lesson # Hack: if 1st lesson and 1st event, bias for a LONGER delay before repeat so get a chance to put a 2nd new word in the gap.  (But don't do this for other events - compromises flexibility.)
    if is_first_lesson and num==1 and not is_first_lesson=="hadGlue":
        is_first_lesson = "hadGlue"
        return Glue(27,3)
    if num==0: return initialGlue()
    elif num==1: return Glue(15,15)
    elif num==2: return Glue(45,15)
    elif num==3: return Glue(130,30)
    elif num==4: return Glue(500,60)
    else: return Glue(500,150+3*(num-5))

randomAdjustmentThreshold = 500
# (if initial glue len >= this, it's randomly adjusted
# BEFORE checking for collisions - this avoids certain
# problems with repetitive lessons)


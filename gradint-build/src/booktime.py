# This file is part of the source code of
# gradint v0.9973 (c) 2002-2011 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of booktime.py - handle booking events into the lesson

# Bin-packing algorithm is a bit primitive but it
# should do

# Event - a single event, such as a Chinese phrase or an
# English question - has a length (including any reasonable
# pause after it).  ALSO 'glue' between events (e.g. a
# graduated interval) that is flexible and that can be
# interspersed with other events.  (A sequence of
# repetitions should START with glue.)

def initialGlue(): return Glue(0,maxLenOfLesson)

try: import bisect
except:
    class bisect: pass
    bisect=bisect()
    def insort(l,item):
        l.append(item) ; l.sort()
    bisect.insort = insort
class Schedule(object):
    # A sorted list of (start,finish) times that are booked
    def __init__(self): self.bookedList = []
    def book(self,start,finish): bisect.insort(self.bookedList,(start,finish))

earliestAllowedEvent = 0 # for "don't start before" hacks, so can keep all initial glue starting at 0

class GlueOrEvent(object):
    # 'invisible' is non-0 if this is "glue" and other
    # events can take place at the same time.
    def __init__(self,length=0,plusMinus=0,invisible=0):
        self.length = length
        self.plusMinus = plusMinus
        self.invisible = invisible
        # assert invisible or length > 0, "Length is %s" % (length,) # no longer valid now synth.py can generate a 0-length final event
    def makesSenseToLog(self): return 0
    def bookIn(self,schedule,start):
        if not self.invisible:
            schedule.book(start,start+self.length)
    def addToEvents(self,events,startTime):
        assert not self.invisible
        events.append((startTime,self))
    def overlaps(self,start,schedule,direction):
        # Returns how much it has to move, given 'start'
        # direction is +1 or -1 - which way to move
        # (return value is always unsigned)
        if self.invisible: return 0 # never has to move
        if not schedule.bookedList: return 0 # assume earliestAllowedEvent does not apply when schedule is empty
        oldStart = start
        if direction==1: # moving forwards
            start = max(start,earliestAllowedEvent)
            count = 0 ; blLen = len(schedule.bookedList)
            while count<blLen and schedule.bookedList[count][1] <= start: # finishes before or as we start - irrelevant
                count += 1
            while count<blLen and schedule.bookedList[count][0]<start+self.length: # starts before we finish
                start = schedule.bookedList[count][1]
                count += 1
            return start-oldStart
        else: # moving backwards
            if start<earliestAllowedEvent: return oldStart+1 # hack: force being placed before the beginning of the lesson, which should result in rejecting it
            count = len(schedule.bookedList)-1
            finish=start+self.length
            while count>=0 and schedule.bookedList[count][0] >= finish: # starts after or as we finish - irrelevant
                count -= 1
            while count>=0 and schedule.bookedList[count][1]>start: # finishes after we start
                start = schedule.bookedList[count][0]-self.length
                count -= 1
            return oldStart-start
    def will_be_played(self): pass
    def play(self): pass
    def setOnLeaves(self,name,value):
        # Set some value that should propagate to the "leaves" (only) of the event tree
        # i.e. to the events that matter to addToEvents.
        # (and only if they don't already have such an attribute, so we can put the exceptions first.)
        if not hasattr(self,name): exec('self.'+name+'='+repr(value))
    def setOnLastLeaf(self,name,value): self.setOnLeaves(name,value)
class Event (GlueOrEvent):
    def __init__(self,length):
        GlueOrEvent.__init__(self,length)
    def play(self):
        # Playing a "silence event".  Normally don't need to do anything.
        # However, if playing in real time and the scheduler is behind, then
        # this delay is probably important - so have at least most of it.
        # AND if not real-time then we DON'T want to beep during this silence
        # (long-phrase/pause/long-answer is different from pause between sequences)
        if soundCollector: soundCollector.addSilence(self.length*0.7,False)
        else: mysleep(min(3,self.length*0.7))
class CompositeEvent (Event):
    # An event made up of several others in sequence with
    # nothing intervening
    def __init__(self,eventList):
        length = 0
        for i in eventList: length += i.length
        Event.__init__(self,length)
        self.eventList = eventList
    def addToEvents(self,events,startTime):
        for i in self.eventList:
            i.addToEvents(events,startTime)
            startTime = startTime + i.length
    def play(self): # not normally called, except perhaps by partials, so don't worry about gap-events etc in eventList
        for e in self.eventList: e.play()
    def setOnLeaves(self,name,value):
        for e in self.eventList: e.setOnLeaves(name,value)
    def setOnLastLeaf(self,name,value): self.eventList[-1].setOnLastLeaf(name,value)
    def makesSenseToLog(self):
        if hasattr(self,"is_prompt"): return not self.is_prompt
        for e in self.eventList:
            if e.makesSenseToLog(): return True
    def __repr__(self): return "{"+(" ".join([str(e) for e in self.eventList]))+"}"
class Glue (GlueOrEvent):
    def __init__(self,length,plusMinus):
        GlueOrEvent.__init__(self,length,plusMinus,1)

def sgn(a):
    # Not all versions of Python have this built-in
    if a: return a/abs(a)
    else: return 1

class StretchedTooFar(Exception): pass
class GluedEvent(object):
    # Some glue before an event
    def __init__(self,glue,event):
        self.glue = glue
        self.event = event
        self.glue.adjustment = 0
        self.glue.preAdjustment = None
    def randomPreAdjustment(self):
        if self.glue.length < randomAdjustmentThreshold: self.glue.preAdjustment = 0
        elif is_first_lesson: # hack - bias against making the silences TOO long
            self.glue.preAdjustment = random.gauss(0,self.glue.plusMinus)
            if self.glue.preAdjustment<0: self.glue.preAdjustment = - self.glue.preAdjustment
            if self.glue.preAdjustment > self.glue.plusMinus: self.glue.preAdjustment = 0
            self.glue.preAdjustment -= self.glue.plusMinus
        else:
            self.glue.preAdjustment = random.gauss(0,self.glue.plusMinus)
            if abs(self.glue.preAdjustment) > self.glue.plusMinus:
                self.glue.preAdjustment = self.glue.plusMinus # err on the +ve side
    def adjustGlue(self,glueStart,schedule,direction):
        # How far does it need to move?
        # Use preAdjustment, not adjustment, in case
        # re-adjusting due to a change of direction
        needMove = self.event.overlaps(glueStart+self.glue.length+self.glue.preAdjustment,schedule,direction)
        # needMove*direction now gives delta from the
        # pre-adjusted glue end; need to add preAdjustment
        # to get delta from the unadjusted
        needMove=needMove*direction+self.glue.preAdjustment
        direction=sgn(needMove) ; needMove=abs(needMove)
        if needMove > self.glue.plusMinus \
           or (direction<0 and needMove > self.glue.length)\
           or glueStart+self.glue.length+needMove*direction+self.event.length > maxLenOfLesson:
            raise StretchedTooFar()
        self.glue.adjustment = needMove * direction
    def getAdjustedEnd(self,glueStart):
        return glueStart+self.glue.length+self.glue.adjustment+self.event.length
    def bookIn(self,schedule,glueStart):
        self.event.bookIn(schedule,glueStart+self.glue.length+self.glue.adjustment)
    def getEventStart(self,glueStart):
        return glueStart+self.glue.length+self.glue.adjustment
    def setOnLeaves(self,name,value): self.event.setOnLeaves(name,value)
    def setOnLastLeaf(self,name,value): self.event.setOnLastLeaf(name,value)

def setGlue(gluedEventList, schedule, glueStart = 0):
    # Uses tail recursion / backtracking with exceptions
    # (Note: can throw an exception to outermost level if
    # there is no solution)
    if not gluedEventList: return
    try:
        if gluedEventList[0].glue.preAdjustment==None: gluedEventList[0].randomPreAdjustment() # (Do NOT re-do on backtrack: should find a fit regardless of the pre-adjustment)
        gluedEventList[0].adjustGlue(glueStart,schedule,1)
        setGlue(gluedEventList[1:],schedule,gluedEventList[0].getAdjustedEnd(glueStart))
    except StretchedTooFar:
        if glueStart==0: raise StretchedTooFar # don't even try pushing it the other way (NB randomPreAdjustment will be 0 for the initial glue)
        gluedEventList[0].adjustGlue(glueStart,schedule,-1)
        setGlue(gluedEventList[1:],schedule,gluedEventList[0].getAdjustedEnd(glueStart))

def setGlue_wrapper(gluedEventList, schedule):
    # Normally setGlue will do "first fit" and will throw
    # an exception if the first fit can't possibly work with
    # the REST of the sequence.  Really want a good algorithm
    # that sorts it out properly, but meanwhile we can try
    # just a bit harder to fit it in if first-fit fails.
    # gluedEventList[0].glue.length should be 0 but we can increase it here (only).
    if len(gluedEventList)==1: return setGlue(gluedEventList,schedule) # no point doing the stuff below on length-1 lists
    worked = 0
    while (not worked) and gluedEventList[0].glue.length < maxLenOfLesson:
        try:
            setGlue(gluedEventList, schedule)
            worked = 1
        except StretchedTooFar:
            # try harder
            gluedEventList[0].glue.length += (10+gluedEventList[0].glue.adjustment) # (NB preAdjustment will be 0, so don't have to worry about that)
            # (TODO the 10 should be a constant)
    if not worked: raise StretchedTooFar()

def bookIn(gluedEventList,schedule):
    setGlue_wrapper(gluedEventList,schedule)
    glueStart = 0
    for i in gluedEventList:
        i.bookIn(schedule,glueStart)
        glueStart = i.getAdjustedEnd(glueStart)

gluedListTracker=None # set to [] if want to track them (used in utils/diagram.py)

class Lesson(object):
    def __init__(self):
        self.schedule = Schedule()
        self.events = [] # list of (time,event)
        self.newWords = self.oldWords = 0
        self.eventListCounter = 0
        if startAnnouncement:
            w = fileToEvent(startAnnouncement,"")
            w.bookIn(self.schedule,0)
            w.addToEvents(self.events,0)
        if endAnnouncement:
            w = fileToEvent(endAnnouncement,"")
            wStart = maxLenOfLesson-w.length
            w.bookIn(self.schedule,wStart)
            w.addToEvents(self.events,wStart)
    def message(self):
        t,event = max(self.events)
        finish = int(0.5+t+event.length)
        teacher_extra = ""
        if teacherMode:
            self.events.sort()
            for t,event in self.events:
                if event.makesSenseToLog():
                    teacher_extra="\nFirst word will be "+maybe_unicode(str(event))
                    break
        l=cond(app,localise,lambda x:x)
        if self.oldWords or teacherMode:
            return l("Today's lesson teaches %d new words\nand revises %d old words\n\nPlaying time: %d %s %d %s") % (self.newWords,self.oldWords,finish/60,singular(finish/60,"minutes"),finish%60,singular(finish%60,"seconds"))+teacher_extra
        else:
            # less confusing message for a beginner
            return l("Today we will learn %d words\nThis will require %d %s %d %s\nFollow the spoken instructions carefully") % (self.newWords,finish/60,singular(finish/60,"minutes"),finish%60,singular(finish%60,"seconds"))
    def addSequence(self,gluedEventList):
        bookIn(gluedEventList,self.schedule)
        if not gluedListTracker==None: gluedListTracker.append(gluedEventList)
        glueStart = 0 ; lastI = None
        for i in gluedEventList:
            i.event.setOnLeaves("sequenceID",self.eventListCounter) # for max_lateness stuff
            i.event.setOnLeaves("importance",len(gluedEventList)) # ditto
            startTime = i.getEventStart(glueStart)
            i.event.addToEvents(self.events,startTime)
            glueStart = i.getAdjustedEnd(glueStart)
            if lastI: lastI.event.setOnLeaves("max_lateness",max(1,10/len(gluedEventList))+min(lastI.glue.plusMinus-lastI.glue.adjustment,i.glue.plusMinus+i.glue.adjustment))
            # (Note that this setting of max_lateness is not particularly clever - it can detect if a sequence's existing scheduling has been pushed beyond its limits, but it can't dynamically re-schedule the sequence as a whole when that happens.  Hopefully people's emergency interruptions won't be too long.)
            lastI = i
        if lastI:
            lastI.event.setOnLeaves("max_lateness",max(1,10/len(gluedEventList))+lastI.glue.plusMinus-lastI.glue.adjustment)
            if hasattr(gluedEventList[0],"timesDone"): lastI.event.setOnLastLeaf("endseq",not gluedEventList[0].timesDone)
        self.eventListCounter += 1
    def cap_max_lateness(self):
        # if an event of importance I has a max lateness of M, then all previous events with importance <I have to cap their max lateness to M+(intervening gaps) so as not to make it late.
        # (sorts events as a side-effect)
        self.events.sort() ; self.events.reverse()
        latenessCap = {} ; nextStart = 0
        for t,event in self.events:
            if nextStart:
                for k in latenessCap.keys(): latenessCap[k] += (nextStart-(t+event.length)) # the gap
            nextStart = t
            if not hasattr(event,"importance"): continue # (wasn't added via addSequence, probably not a normal lesson)
            event.max_lateness=min(event.max_lateness,latenessCap.get(event.importance,maxLenOfLesson))
            for i in range(event.importance): latenessCap[i]=min(latenessCap.get(i,maxLenOfLesson),event.max_lateness)
            del event.importance # (might as well save some filespace in saveLesson while we're here)
        self.events.reverse() # so sorted again
    def play(self):
        if (synthCache_test_mode or synthCache_test_mode==[]) and not hasattr(self,"doneSubst"):
            subst_some_synth_for_synthcache(self.events)
            self.doneSubst=1
        global runner, finishTime, lessonLen, wordsLeft
        wordsLeft={False:self.oldWords,True:self.newWords}
        initLogFile()
        for (t,event) in self.events: event.will_be_played()
        if soundCollector:
            for synth in viable_synths: synth.finish_makefile() # TODO: might want to do that if realtime also, but on most reasonably-specified machines it should be OK to start playing before everything has been synth'd (see also play method in synth.py which makes allowance for slow start)
        finishTime = None # unspecified
        if self.events:
            lessonLen = self.events[-1][0]+self.events[-1][1].length
            if lessonLen>60: # otherwise probably a small justSynthesize job - don't clutter the terminal with progress
                finishTime = int(0.5+(time.time() + lessonLen))
                if (riscos_sound or winCEsound) and not app and not soundCollector: show_info("Started at %s, will finish at %s\n" % (time.strftime("%H:%M",time.localtime(time.time())),time.strftime("%H:%M",time.localtime(finishTime))))
        global sequenceIDs_to_cancel ; sequenceIDs_to_cancel = {}
        global copy_of_runner_events ; copy_of_runner_events = []
        global lessonStartTime ; lessonStartTime = 0 # will be set to time.time() on 1st event
        # make the runner as late as possible
        if soundCollector: runner = sched.scheduler(collector_time,collector_sleep)
        else: runner = sched.scheduler(time.time,mysleep)
        for (t,event) in self.events: copy_of_runner_events.append((event,runner.enter(t,1,play,(event,)),t))
        # TODO what if Brief Interrupt appears during that events loop and someone presses it (will act as a Cancel and go back to main)
        try: runner.run()
        except KeyboardInterrupt: handleInterrupt()
        runner = None
        if soundCollector: soundCollector.finished()
        if logFileHandle: logFileHandle.close()

subst_synth_counters = {} # global so it carries over when using justSynthesize in repeat mode
def decide_subst_synth(cache_fname):
    subst_synth_counters[cache_fname] = subst_synth_counters.get(cache_fname,0)+1
    return subst_synth_counters[cache_fname] in [2,4] or (subst_synth_counters[cache_fname]>5 and random.choice([1,2])==1)
def subst_some_synth_for_synthcache(events):
    # turn SOME synthcache events back into synth events (for testing new synths etc)
    reverse_transTbl = {}
    for k,v in synthCache_transtbl.items(): reverse_transTbl[v]=k
    for i in range(len(events)):
        if hasattr(events[i][1],"file") and events[i][1].file.startswith(synthCache+os.sep):
            cache_fname = events[i][1].file[len(synthCache+os.sep):]
            cache_fname = reverse_transTbl.get(cache_fname,cache_fname)
            if cache_fname[0]=="_": continue # a sporadically-used synthCache entry anyway
            if type(synthCache_test_mode)==type([]):
                found=0
                for str in synthCache_test_mode:
                    if (re and re.search(str,cache_fname)) or cache_fname.find(str)>-1:
                        found=1 ; break
                if found: continue
            lang = languageof(cache_fname)
            if get_synth_if_possible(lang) and decide_subst_synth(cache_fname): events[i] = (events[i][0],synth_event(lang,cache_fname[:cache_fname.rindex("_")]))

# This file is part of the source code of
# gradint v0.9989 (c) 2002-2014 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of loop.py - the main loop (not including Tk front-end etc)

def doOneLesson(dbase):
    global saveLesson
    if dbase:
        soFar = dbase.message()
        lesson = dbase.makeLesson()
    else:
        soFar = "Re-loading saved lesson, so not scanning collection."
        if compress_progress_file: lesson=pickle.Unpickler(os.popen('gzip -fdc "'+saveLesson+'"','rb')).load()
        else: lesson=pickle.Unpickler(open(saveLesson,'rb')).load()
    if app and not dbase: app.setNotFirstTime()
    while 1:
      global cancelledFiles ; cancelledFiles = []
      global askAgain_explain ; askAgain_explain = ""
      if not justSaveLesson:
        if emulated_interruptMain: check_for_interrupts() # (avoid confusion if cancel pressed before message shown)
        msg = soFar+"\n"+lesson.message() # +"\n(When you continue, there will be a 5 second delay\nto sit comfortably)"
        if waitBeforeStart:
            waitOnMessage(msg+interrupt_instructions())
            #time.sleep(5)
            time.sleep(2) # less confusing for beginners
        elif not app and not appuifw and not android: show_info(msg+interrupt_instructions()+"\n",True)
        if startFunction: startFunction()
        if app:
            app.setLabel("Starting lesson")
            app.cancelling = 0
        lesson.play()
      if dbase and saveProgress and not dbase.saved_completely: # justSaveLesson is a no-op if not first time through lesson (because scripts that use it probably mean "save if not already save"; certainly don't mean "play if is saved")
          if cancelledFiles: dbase.savePartial(cancelledFiles)
          else: dbase.save()
          if dbase.saved_completely and app: app.setNotFirstTime() # dbase.saved_completely could have been done by EITHER of the above (e.g. overlapping partial saves)
          if saveLesson:
              if compress_progress_file: pickle.Pickler(os.popen('gzip -9 > "'+saveLesson+'"','wb'),-1).dump(lesson) # TODO: paranoid_file_management ? (c.f. saveProgress)
              else: pickle.Pickler(open(saveLesson,"wb"),-1).dump(lesson)
              saveLesson = None # so saves only the first when doing multiple lessons
              if justSaveLesson: break
      if not app and not app==None: break # close box pressed
      if not waitBeforeStart or not getYN(cond(not askAgain_explain and (not dbase or not saveProgress or dbase.saved_completely),"Hear this lesson again?",askAgain_explain+"Start this lesson again?")): break

def disable_lid(restore): # for portable netbooks (like eee), can close lid & keep listening
  if unix:
   if app and not outputFile:
    import commands ; global oldLid,warnedAC
    try: warnedAC
    except: warnedAC=0
    if (not restore) and commands.getoutput("cat /proc/acpi/ac_adapter/AC*/state 2>/dev/null").find("off-line")>=0 and not warnedAC:
      waitOnMessage("Some quirky Linux battery managers turn speakers off mid-lesson, so AC power is recommended.") ; warnedAC=1 # (TODO what if pull out AC during the lesson without looking at the screen?  Spoken message??)
    ls = "et org.gnome.settings-daemon.plugins.power lid-close-" ; src=["ac","battery"]
    if restore and oldLid[0]: return [commands.getoutput("gsettings s"+ls+p+"-action "+q+" 2>/dev/null") for p,q in zip(src,oldLid)]
    oldLid = [commands.getoutput("gsettings g"+ls+p+"-action 2>/dev/null").replace("'","") for p in src]
    if oldLid[0]: [commands.getoutput("gsettings s"+ls+p+"-action blank 2>/dev/null") for p in src]

if loadLesson==-1: loadLesson=(fileExists(saveLesson) and time.localtime(os.stat(saveLesson).st_mtime)[:3]==time.localtime()[:3])

def lesson_loop():
  global app,availablePrompts,teacherMode
  if ask_teacherMode and not soundCollector and waitBeforeStart: teacherMode=getYN("Use teacher assistant mode? (say 'no' for self-study)")
  try:
    # doLabel("Scanning prompts") # rarely takes long even on low-end systems
    init_scanSamples() # in case was messed around with before
    availablePrompts = AvailablePrompts() # here so app is already initialised before any warnings
    global dbase # so can be accessed by interrupt handler
    if loadLesson: dbase=None
    else:
        doLabel("Loading progress data")
        dbase = ProgressDatabase()
        if not dbase.data:
            msg = "There are no words to put in the lesson."
            if app or appuifw or android:
                drop_to_synthloop = False
                msg = localise(msg)+"\n"+localise("Please add some words first.")
            else:
                drop_to_synthloop = (synth_partials_voices or get_synth_if_possible("en",0) or viable_synths) # the get_synth_if_possible call here is basically to ensure viable_synths is populated
                msg += "\nPlease read the instructions on the website\nwhich tell you how to add words.\n"+cond(drop_to_synthloop,"Dropping back to justSynthesize loop.\n","")
            if drop_to_synthloop:
                clearScreen() ; show_info(msg)
                primitive_synthloop()
            else: waitOnMessage(msg)
            return
    doLabel("Making lesson")
    doOneLesson(dbase)
  finally: teacherMode=0

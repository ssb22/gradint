# This file is part of the source code of
# gradint v0.99898 (c) 2002-2018 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of play.py - handle playing sounds or collecting them into output files

emergency_lessonHold_to = 0 # set to a time.time() value for resume from emergency holds
# (TODO: S2G problems! - both emergency_lessonHold_to and timeout_time below can be set to 0 to mean "always in the past"; this might not work if the clock wraps around.)
sequenceIDs_to_cancel = {} ; lessonStartTime = 0 ; wordsLeft={False:0,True:0}
def play(event):
    global copy_of_runner_events, lessonStartTime
    if soundCollector:
        secs = int(soundCollector.tell())
        t = "%d:%d" % (secs/60,secs%60)
    else:
        while time.time() < emergency_lessonHold_to: # (might be set to 0 by manual resume in the meantime)
            if not app: doLabel("Emergency brief interrupt: %d" % (emergency_lessonHold_to-time.time()))
            time.sleep(1)
        t = "%d:%02d:%02d" % time.localtime()[3:6]
    timeout_time = time.time() + max(10,event.length/3) # don't loop *forever* if unable to start playing (especially if we're being used in a reminder system etc, it may be best to exit eventually)
    if lessonStartTime and not soundCollector:
        if hasattr(event,"max_lateness"): timeout_time = min(timeout_time, lessonStartTime + (copy_of_runner_events[0][2]+event.max_lateness))
        if hasattr(event,"sequenceID") and event.sequenceID in sequenceIDs_to_cancel: timeout_time = 0
    play_error = "firstTime"
    while play_error and time.time()<=timeout_time: # use <= rather than < in case we have only 1sec precision
        if not play_error=="firstTime":
            if not app: show_info("Problem playing sound - retrying\n")
            time.sleep(0.2)
        if not teacherMode or (event.makesSenseToLog() and getYN("NOW say "+maybe_unicode(str(event))+"\nComputer say it instead?")): play_error = event.play()
        else: play_error = 0
    if not play_error and logFile and event.makesSenseToLog(): logFileHandle.write(t+" "+str(event)+"\n")
    if play_error and hasattr(event,"wordToCancel") and event.wordToCancel: # probably max_lateness exceeded, and we have something to cancel
        cancelledFiles.append(event.wordToCancel)
        if hasattr(event,"sequenceID"): sequenceIDs_to_cancel[event.sequenceID]=True # TODO what if its last event has "endseq" attribute, do we want to decrement wordsLeft early?
    if hasattr(event,"endseq"): wordsLeft[event.endseq] -= 1
    del copy_of_runner_events[0]
    if soundCollector: return doLabel("%d%% completed" % (soundCollector.tell()*100/lessonLen))
    line2 = "" # report what you'd lose if you cancel now (in case you're deciding whether to answer the phone etc), + say how many already cancelled (for diagnosing results of interruptions caused by phone events etc on those platforms)
    new,old=wordsLeft[True],wordsLeft[False]
    if new: line2="%d new " % new
    if old:
      if line2: line2 += ("+ %d old " % old)
      else: line2="%d old words " % old
    elif new: line2 += "words "
    if line2:
      line2=cond(app or appuifw or android,"\n",", ")+line2+"remain"
      if cancelledFiles: line2 += "\n("+str(len(cancelledFiles))+" cancelled)"
    if not lessonStartTime: lessonStartTime = time.time() # the actual time of the FIRST event (don't set it before as there may be delays).  (we're setting this at the END of the 1st event - the extra margin should be ok, and can help with start-of-lesson problems with slow disks.)
    if finishTime and time.time() >= emergency_lessonHold_to: doLabel("%s (finish %s)%s" % (time.strftime("%H:%M",time.localtime(time.time())),time.strftime("%H:%M",time.localtime(finishTime)),line2)) # was %I:%M but don't like leading '0' in PM times.  2nd condition added because might press 'brief interrupt' while playing.
def doLabel(labelText):
    labelText = ensure_unicode(labelText)
    if app: app.setLabel(labelText)
    elif appuifw:
        t=appuifw.Text() ; t.add(labelText)
        appuifw.app.body = t
    elif android: android.makeToast(labelText) # TODO alternatives?  method to cancel lessons etc would be nice
    elif not (riscos_sound or winCEsound): # (we don't have a way of updating a clock or progress indicator on those)
        global doLabelLastLen
        try: doLabelLastLen
        except NameError: doLabelLastLen=0
        show_info("   "+labelText+(" "*(doLabelLastLen-len(labelText)))+"\r")
        doLabelLastLen=len(labelText)
        if msvcrt and msvcrt.kbhit() and msvcrt.getche()==" ": raise KeyboardInterrupt() # for beginners, easier than Ctrl-C
def initLogFile():
    global logFileHandle
    logFileHandle = None
    if logFile:
        try:
            logFileHandle = open(logFile,'w')
        except: pass
runner = None

teacherMode = 0
if ask_teacherMode:
  old_mysleep = mysleep
  def mysleep(secs):
    if not teacherMode: return old_mysleep(secs)
    t=time.time() ; label = 0 ; timeToIndicate = secs
    for e in copy_of_runner_events:
        if e[0].makesSenseToLog():
            timeToIndicate += e[2]-copy_of_runner_events[0][2]
            label = maybe_unicode(str(e[0]))
            if hasattr(e[0],"max_lateness"): label=", max +"+str(int(e[0].max_lateness))+": "+label
            else: label=": "+label
            break
    while time.time()<t+secs:
        if label: doLabel("In "+str(int(t+timeToIndicate-time.time()))+" secs"+label)
        old_mysleep(1)

def maybe_unicode(label):
    if app or appuifw or android:
        try: return unicode(label,'utf-8')
        except: return label # ??
    else: return repr(label)

if (winsound or mingw32) and fileExists("madplay.exe"): madplay_path = "madplay.exe"
elif unix and hasattr(os,"popen"):
  madplay_path = os.popen("PATH=$PATH:. which madplay 2>/dev/null").read().strip(wsp)
  if not fileExists(cond(cygwin,madplay_path+".exe",madplay_path)): madplay_path="" # in case of a Unix 'which' returning error on stdout
  if madplay_path and not winsound and not mingw32: madplay_path='"'+madplay_path+'"' # in case there's spaces etc in the path
else: madplay_path = None
if madplay_path and not mp3Player: mp3Player=madplay_path

def intor0(v):
    try: return int(v)
    except ValueError: return 0

sox_effect=""
sox_8bit, sox_16bit, sox_ignoreLen, sox_signed = "-b", "-w", "", "-s"
# Older sox versions (e.g. the one bundled with Windows Gradint) recognise -b and -w only; sox v14+ recognises both that and -1/-2; newer versions recognise only -1/-2.  We check for newer versions if unix.  (TODO riscos / other?)
soundVolume_dB = math.log(soundVolume)*(-6/math.log(0.5))
if unix:
  if macsound: got_afplay = got_program("afplay") # 10.5+, use in preference to the bundled qtplay which requires PowerPC or Rosetta
  sox_formats=os.popen("sox --help 2>&1").read() # NOT .lower() yet
  sf2 = ' '.join(sox_formats.lower().split())
  if sf2.startswith("sox: sox v"):
    if sf2[10]==' ': soxMaj=15 # guess (broken HomeBrew install)
    else: soxMaj = intor0(sf2[10:sf2.index('.')])
  else: soxMaj=0
  if soxMaj>=14:
    if soxMaj==14 and sf2[13]<'3': pass
    else: sox_ignoreLen = "|sox --ignore-length -t wav - -t wav - 2>/dev/null"
    if soxMaj==14 and sf2[13]<'4': sox_8bit, sox_16bit = "-1", "-2" # see comment above
    else: sox_8bit, sox_16bit, sox_signed = "-b 8", "-b 16", "-e signed-integer" # TODO: check if 14.3 accepts these also (at least 14.4 complains -2 etc is deprecated)
  if sf2.find("wav")>=0: gotSox=1
  else:
    gotSox=0
    if got_program("sox"):
      if macsound: xtra=". (If you're on 10.8 Mountain Lion, try downloading a more recent sox binary from sox.sourceforge.net and putting it inside Gradint.app, but that will break compatibility with older PowerPC Macs.)" # TODO: ship TWO binaries? but we don't want the default gradint to get too big. See sox.README for more notes.
      elif cygwin: xtra=""
      else: xtra=". Ubuntu users please install libsox-fmt-all."
      show_warning("SoX found but can't handle WAV, so you won't be able to write lessons to files for later"+xtra)
else: gotSox = got_program("sox")
wavPlayer_override = not (not wavPlayer)
if winsound or mingw32:
    # in winsound can use PlaySound() but better not use it for LONGER sounds - find a wavPlayer anyway for those (see self.length condition in play() method below)
    # (TODO sndrec32.exe loads the whole of the file into memory before playing.  but mplayer/mplay32 sometimes halts on a yes/no dialogue about settings, and Media Player can't take files on command line so needs correct file association and executable permissions.  And many of the freeware command-line players have the same limitations as winsound.)
    # TODO now that we (usually) have tkSnack bundled with the Windows version, can we try that also (with file=) before sndrec32?
    if not wavPlayer and fileExists(os.environ.get("windir","C:\\Windows")+"\\system32\\sndrec32.exe"): wavPlayer = "start /min sndrec32 /play /close" # TODO could also use ShellExecute or some other utility to make it completely hidden
elif unix and not macsound:
    sox_type = "-t ossdsp -s "+sox_16bit # (we will check that sox can do ossdsp below) (always specify 16-bit because if we're adjusting the volume of 8-bit wav's then we could lose too many bits in the adjustment unless we first convert to 16-bit)
    if not soundVolume==1: sox_effect=" vol "+str(soundVolume)
    if sox_effect and not gotSox:
        show_warning("Warning: trying to adjust soundVolume when 'sox' is not on the system might not work")
        # (need a warning here, because if using 'aplay' then sox o/p is 2>/dev/null (see below) so a missing sox won't be obvious)
    if not oss_sound_device:
        dsps_to_check = []
        if sox_formats.find("ossdsp")>=0: dsps_to_check += ["/dev/sound/dsp","/dev/dsp"]
        if sox_formats.find("sunau")>=0: dsps_to_check += ["/dev/audio"]
        for dsp in dsps_to_check:
            if fileExists_stat(dsp):
                oss_sound_device = dsp
                if dsp=="/dev/audio": sox_type="-t sunau "+sox_signed+" "+sox_16bit
                break
    if sox_formats.find("-q")>=0: sox_type="-q "+sox_type
    if not wavPlayer:
      if oss_sound_device and not cygwin and gotSox: wavPlayer = "sox"
      elif cygwin and got_program("sndrec32"): # XP's Sound Recorder (vista's is called soundreorder.exe but won't do this) (+ don't have to worry about the >2G memory bug as not applicable to playing)
        wavPlayer = "sndrec32 /play /close" # prefer this to esdplay due to cygwin esdplay delaying every other call and being asynchronous
        if got_program("cmd"): wavPlayer = "cmd /c start /min "+wavPlayer # TODO could also use ShellExecute or some other utility to make it completely hidden
      elif cygwin and oss_sound_device and got_program("play"): wavPlayer = "play" # this is part of sox, but it'll be the sox installed in cygwin rather than any sox.exe in gradint directory from Windows version
      else:
        otherPrograms = ["aplay","esdplay","auplay","wavp","playmus","mplayer","playwave","alsaplayer"] # alsaplayer is a last resort because the text-mode version may or may not be installed; hopefully they'll have alsa-utils installed which includes 'aplay'. (playwave has been known to clip some files)
        for otherProgram in otherPrograms:
            if got_program(otherProgram):
                wavPlayer = otherProgram
                break
    if not cygwin and not mp3Player:
        for mpg in ["mpg123","mpg321","mad123","mplayer"]:
            if got_program(mpg):
                mp3Player = mpg ; break
    if not wavPlayer and not outputFile: show_warning("Warning: no known "+cond(mp3Player,"non-MP3 ","")+"sound-playing command found on this system\n  (checked for sox with /dev/dsp etc, also checked for play "+" ".join(otherPrograms)+")\n - expect problems with realtime lessons"+cond(mp3Player," unless everything is MP3",""))
may_need_mp3_warning = ((wavPlayer or winsound or riscos_sound or mingw32) and not (mp3Player or gotSox))
def maybe_warn_mp3():
    global may_need_mp3_warning
    if may_need_mp3_warning:
        show_warning("Warning: Dealing with MP3 files when there is no known MP3-playing command on this system.  Expect problems.")
        may_need_mp3_warning = 0
# We also set a couple of other variables:
# sox_same_endian is " -x" if it's needed to make sox the same endian-ness as the architecture (e.g. a PPC sox on an Intel Mac)
# sox_little_endian is " -x" if it's needed to make sox little-endian
sox_same_endian = sox_little_endian = ""
if gotSox and unix:
    # should only have to run this test if macsound (don't bother on NSLU2's etc):
    # (wav is little-endian, so if it doesn't pass the string through then it interpreted the i/p as big-endian)
    if macsound and os.popen('echo "This is a test" | sox -t raw -r 8000 '+sox_16bit+' '+sox_signed+' -c 1 - -t wav - 2>/dev/null').read().find("This is a test")==-1:
        sox_little_endian = " -x"
        if not big_endian: sox_same_endian = " -x"
    elif big_endian: sox_little_endian = " -x"

def changeToDirOf(file,winsound_also=0):
    # used before running a non-cygwin program in the cygwin environment (due to directory differences etc)
    # and (with winsound_also) before running a program on Windows without needing to quote the filename (e.g. because some versions of eSpeak won't write to a quoted wav file when called from popen).  Note windows os.chdir DOES change the drive also.  Use this only if filename will not contain special characters (e.g. should be able to use it for temp files).
    # NB if winsound_also is set, will return file "quoted" on other systems (so can set winsound_also and not worry about whether or not it should be quoted)
    if winCEsound and not ' ' in file: return file # don't need to quote
    elif winsound_also and not (winsound or mingw32 or cygwin): return '"'+file+'"'
    elif (cygwin or ((winsound or mingw32) and winsound_also)) and os.sep in file:
        os.chdir(file[:file.rfind(os.sep)])
        return file[file.rfind(os.sep)+1:]
    else: return file

def system(cmd):
    # Don't call os.system for commands like sound playing, because if you do then any Control-C interrupt will go to that rather than to gradint as we want, and it will pop up a large blank console window in Windows GUI-only version
    if riscos_sound or not hasattr(os,"popen"): return os.system(cmd) # no popen
    if unix and (';' in cmd or '<' in cmd): cmd='/bin/bash -c "'+cmd.replace('\\','\\\\').replace('"','\\"').replace('$','\\$')+'"' # not /bin/sh if it's complex
    try: r=os.popen(cmd)
    except: return os.system(cmd) # too many file descriptors open or something
    r.read() ; return r.close()
if unix:
  # Unix: make sure "kill" on gradint's pid includes the players:
  try:
    os.setpgrp()
    import signal
    def siggrp(sigNo,*args):
        signal.signal(sigNo,signal.SIG_IGN)
        os.killpg(os.getpgrp(),sigNo) # players etc
        raise KeyboardInterrupt # clean up, rm tempfiles etc
    signal.signal(signal.SIGTERM,siggrp)
  except: pass
else: signal=0

# Event(len) gives a pause of that length
# SampleEvent extends this to actually play something:

def soundFileType(file):
    if extsep in file: return file[file.rindex(extsep)+1:].lower()
    else: return "wav"

def lessonIsTight(): return maxLenOfLesson <= 10*60 * min(1.8,max(1,maxNewWords/5.0)) # ?

class SampleEvent(Event):
    def __init__(self,file,useExactLen=False,isTemp=False):
        if use_unicode_filenames: file=ensure_unicode(file)
        self.file = file
        self.exactLen = lengthOfSound(file)
        if isTemp: self.isTemp=1
        approxLen = self.exactLen
        if not lessonIsTight() and not useExactLen: approxLen = math.ceil(self.exactLen) # (if <=10min in lesson, don't round up to next second because we want a tighter fit)
        Event.__init__(self,approxLen)
    def __repr__(self):
        if use_unicode_filenames: return self.file.encode('utf-8')
        else: return self.file
    def __del__(self):
      if hasattr(self,"isTemp"):
        import time,os # in case gc'd
        while True:
          try: return os.unlink(self.file)
          except: time.sleep(0.2) # may have taken extra time for the player to load
          if not fileExists_stat(self.file): break # unlink suceeded and still threw exception ??
    def makesSenseToLog(self):
        if hasattr(self,"is_prompt"): return not self.is_prompt # e.g. prompt from synth-cache
        return not self.file.startswith(promptsDirectory) # (NB "not prompts" doesn't necessarily mean it'll be a sample - may be a customised additional comment)
    def play(self): # returns a non-{False,0,None} value on error
        if paranoid_file_management:
            if not hasattr(self,"isTemp"): open(self.file) # ensure ready for reading
        fileType=soundFileType(self.file)
        if soundCollector: soundCollector.addFile(self.file,self.exactLen)
        elif appuifw:
            fname = self.file
            if not fname[1]==":": fname=os.getcwd()+cwd_addSep+fname # must be full drive:\path
            sound = audio.Sound.open(ensure_unicode(fname))
            sound.play()
            try: time.sleep(self.length) # TODO or exactLen?
            finally: sound.stop()
            sound.close() # (probably not worth keeping it open for repeats - there may be a limit to how many can be open)
            return
        elif android:
            fname = self.file
            if not fname[0]=='/': fname=os.getcwd()+'/'+fname
            android.mediaPlay("file://"+fname)
            return
        elif fileType=="mp3" and madplay_path and mp3Player==madplay_path and not macsound and not wavPlayer=="aplay":
            oldcwd = os.getcwd()
            play_error = system(mp3Player+' -q -A '+str(soundVolume_dB)+' "'+changeToDirOf(self.file)+'"') # using changeToDirOf because on Cygwin it might be a non-cygwin madplay.exe that someone's put in the PATH.  And keeping the full path to madplay.exe because the PATH may contain relative directories.
            os.chdir(oldcwd)
            return play_error
        elif winCEsound and fileType=="mp3":
            # we can handle MP3 on WinCE by opening in Media Player.  Too bad it ignores requests to run minimized.
            fname = self.file
            if not fname[0]=="\\": fname=os.getcwd()+cwd_addSep+fname # must be full path
            r=not ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(ShellExecuteInfo(60,File=u""+fname)))
            time.sleep(self.length) # exactLen may not be enough
        elif (winsound and not (self.length>10 and wavPlayer)) or winCEsound: # (don't use winsound for long files if another player is available - it has been known to stop prematurely)
            if fileType=="mp3": file=theMp3FileCache.decode_mp3_to_tmpfile(self.file)
            else: file=self.file
            try:
                if winsound: winsound.PlaySound(file,winsound.SND_FILENAME)
                else: # winCEsound
                    fname = self.file
                    if not fname[0]=="\\": fname=os.getcwd()+cwd_addSep+fname # must be full path
                    ctypes.cdll.coredll.sndPlaySoundW(u""+fname,1) # 0=sync 1=async
                    time.sleep(self.exactLen) # if async.  Async seems to be better at avoiding crashes on some handhelds.
            except RuntimeError: return 1
        elif macsound:
          if got_afplay: player="afplay"
          else: player="qtplay"
          try: unicode(self.file,"ascii")
          except UnicodeDecodeError: # Mac command line can't always handle non-ASCII
            t=os.tempnam()+self.file[self.file.rindex(extsep):]
            write(t,open(self.file).read())
            ret=system(player+" \"%s\"" % (t,))
            os.remove(t)
            return ret
          return system(player+" \"%s\"" % (self.file,))
        elif riscos_sound:
            if fileType=="mp3": file=theMp3FileCache.decode_mp3_to_tmpfile(self.file) # (TODO find a RISC OS program that can play the MP3s directly?)
            else: file=self.file
            system("PlayIt_Play \"%s\"" % (file,))
        elif wavPlayer.find('sndrec32')>=0:
            if fileType=="mp3": file=theMp3FileCache.decode_mp3_to_tmpfile(self.file)
            else: file=self.file
            oldDir = os.getcwd()
            t=time.time()
            os.system(wavPlayer+' "'+changeToDirOf(file)+'"') # don't need to call our version of system() here
            if wavPlayer.find("start")>=0: time.sleep(max(0,self.length-(time.time()-t))) # better do this - don't want events overtaking each other if there are delays.  exactLen not always enough.  (but do subtract the time already taken, in case command extensions have been disabled and "start" is synchronous.)
            os.chdir(oldDir)
        elif fileType=="mp3" and mp3Player and not sox_effect and not (wavPlayer=="aplay" and mp3Player==madplay_path): return system(mp3Player+' "'+self.file+'"')
        elif wavPlayer=="sox":
            # To make it more difficult:
            # sox v12.x (c. 2001) - bug when filenames contain 2 spaces together, and needs input from re-direction in this case
            # sox 14.0 on Cygwin - bug when input is from redirection, unless using cat | ..
            # sox 14.1 on some systems - can't read wav files unless done by redirection (seek problems)
            # sox distributed with Windows version needs redirection, but must do using < operator not cat (don't need to worry about this when playing because will use winsound.PlaySound, but NB it for SoundCollector etc)
            # riscos can't do re-direction (so hope not using a buggy sox) (but again don't have to worry about this if playing because will use PlayIt)
            # + on some setups (e.g. Linux 2.6 ALSA with OSS emulation), it can fail without returning an error code if the DSP is busy, which it might be if (for example) the previous event is done by festival and is taking slightly longer than estimated
            t = time.time()
            play_error = system('cat "%s" | sox -t %s - %s %s%s >/dev/null' % (self.file,fileType,sox_type,oss_sound_device,sox_effect))
            if play_error: return play_error
            else:
                # no error, but did it take long enough?
                timeDiff = time.time()-t
                if timeDiff > self.exactLen/2.0: return 0 # (/2 so not confused by rounding/precision)
                if timeDiff==0 and self.exactLen < 1.5: return 0 # (we'll let that one off for systems that have limited clock precision)
                if not app: show_info("play didn't take long enough - maybe ") # .. problem playing sound
                return 1
        elif wavPlayer=="aplay" and ((not fileType=="mp3") or madplay_path or gotSox):
            if madplay_path and fileType=="mp3": return system(madplay_path+' -q -A '+str(soundVolume_dB)+' "'+self.file+'" -o wav:-|aplay -q') # changeToDirOf() not needed because this won't be cygwin (hopefully)
            elif gotSox and (sox_effect or fileType=="mp3"): return system('cat "'+self.file+'" | sox -t '+fileType+' - -t wav '+sox_16bit+' - '+sox_effect+' 2>/dev/null|aplay -q') # (make sure o/p is 16-bit even if i/p is 8-bit, because if sox_effect says "vol 0.1" or something then applying that to 8-bit would lose too many bits)
            # (2>/dev/null to suppress sox "can't seek to fix wav header" problems, but don't pick 'au' as the type because sox wav->au conversion can take too long on NSLU2 (probably involves rate conversion))
            else: return system('aplay -q "'+self.file+'"')
        # May also be able to support alsa directly with sox (aplay not needed), if " alsa" is in sox -h's output and there is /dev/snd/pcmCxDxp (e.g. /dev/snd/pcmC0D0p), but sometimes it doesn't work, so best stick with aplay
        # TODO: auplay can take -volume (int 0-100) and stdin; check esdplay capabilities also
        elif fileType=="mp3" and mp3Player and not sox_effect: return system(mp3Player+' "'+self.file+'"')
        elif wavPlayer:
            if fileType=="mp3" and not wavPlayer=="mplayer": file=theMp3FileCache.decode_mp3_to_tmpfile(self.file)
            else: file=self.file
            if sox_effect and wavPlayer.strip().endswith("<"): return system('sox "%s" -t wav - %s | %s' % (file,sox_effect,wavPlayer.strip()[:-1]))
            return system(wavPlayer+' "'+file+'"')
        elif fileType=="mp3" and mp3Player: return system(mp3Player+' "'+self.file+'"') # ignore sox_effect
        else: show_warning("Don't know how to play \""+self.file+'" on this system')

br_tab=[(0 , 0 , 0 , 0 , 0),
(32 , 32 , 32 , 32 , 8),
(64 , 48 , 40 , 48 , 16),
(96 , 56 , 48 , 56 , 24),
(128 , 64 , 56 , 64 , 32),
(160 , 80 , 64 , 80 , 40),
(192 , 96 , 80 , 96 , 48),
(224 , 112 , 96 , 112 , 56),
(256 , 128 , 112 , 128 , 64),
(288 , 160 , 128 , 144 , 80),
(320 , 192 , 160 , 160 , 96),
(352 , 224 , 192 , 176 , 112),
(384 , 256 , 224 , 192 , 128),
(416 , 320 , 256 , 224 , 144),
(448 , 384 , 320 , 256 , 160),
(0 , 0 , 0 , 0 , 0)]
def rough_guess_mp3_length(fname):
  try:
    maybe_warn_mp3() # in case there's no mp3 player
    # (NB this is only a rough guess because it doesn't support VBR
    # and doesn't even check all sync bits.  It should be fairly quick though.)
    o = open(fname,"rb") ; i = -1
    while True:
      head=o.read(512)
      if len(head)==0: raise IndexError # read the whole file and not found a \xFF byte??
      i=head.find('\xFF')
      if i==-1: continue
      if i+2 < len(head): head += o.read(3)
      o.seek(o.tell()-len(head)+i+2) ; b=ord(head[i+1])
      if b >= 0xE0: break # valid frame header starts w. 11 1-bits (not just 8: some files with embedded images could throw that off)
    s = o.tell() ; o.close()
    layer = 4-((b&6)>>1)
    if b&24 == 24: # bits are 11 - MPEG version is 1
      column = layer-1 # MPEG 1 layer 1, 2 or 3
    elif layer==1: column = 3 # MPEG 2+ layer 1
    else: column = 4 # MPEG 2+ layer 2+
    bitrate = br_tab[ord(head[i+2])>>4][column]
    if bitrate==0: bitrate=48 # reasonable guess for speech
    return (filelen(fname)-s)*8.0/(bitrate*1000)
  except IndexError: raise Exception("Invalid MP3 header in file "+repr(fname))

def filelen(fname):
    try: fileLen=os.stat(fname).st_size
    except: fileLen=len(read(fname))
    return fileLen

def lengthOfSound(file):
    if file.lower().endswith(dotmp3): return rough_guess_mp3_length(file)
    else: return pcmlen(file)

def pcmlen(file):
    header = sndhdr.what(file)
    if not header: raise IOError("Problem opening file '%s'" % (file,))
    (wtype,wrate,wchannels,wframes,wbits) = header
    if android:
        if wrate==6144: # might be a .3gp from android_recordFile
            d = open(file).read()
            if 'mdat' in d: return (len(d)-d.index('mdat'))/1500.0 # this assumes the bitrate is roughly the same as in my tests, TODO figure it out properly
    divisor = wrate*wchannels*wbits/8 # do NOT optimise with (wbits>>3), because wbits could be 4
    if not divisor: raise IOError("Cannot parse sample format of '%s'" % (file,))
    return (filelen(file) - 44.0) / divisor # 44 is a typical header length, and .0 to convert to floating-point

##########################################################

class SoundCollector(object):
    def __init__(self):
        self.rate = 44100 # so ok for oggenc etc
        if out_type=="raw" and write_to_stdout: self.o=sys.stdout
        elif out_type=="ogg": self.o=os.popen(oggenc()+" -o \"%s\" -r -C 1 -q 0 -" % (cond(write_to_stdout,"-",outputFile),),"wb") # oggenc assumes little-endian, which is what we're going to give it
        elif out_type=="aac":
            if got_program("neroAacEnc"): self.o=os.popen("sox %s - -t wav - | neroAacEnc -br 32000 -if - -of \"%s\"" % (self.soxParams(),cond(write_to_stdout,"-",outputFile)),"wb") # (TODO optionally use -2pass, on a physical input file like the afconvert code)
            else: self.o=os.popen("faac -b 32 -P%s -C 1 -o \"%s\" -" % (cond(big_endian,""," -X"),cond(write_to_stdout,"-",outputFile)),"wb") # (TODO check that faac on big-endian needs the -X removed when we're giving it little-endian.  It SHOULD if the compile is endian-dependent.)
        elif out_type=="mp3": self.o=os.popen("lame -r%s%s -m m --vbr-new -V 9 - \"%s\"" % (lame_endian_parameters(),lame_quiet(),cond(write_to_stdout,"-",outputFile)),"wb") # (TODO check that old versions of lame won't complain about the --vbr-new switch.  And some very old hardware players may insist on MPEG-1 rather than MPEG-2, which would need different parameters)
        # Older versions of gradint used BladeEnc, with these settings: "BladeEnc -br 48 -mono -rawmono STDIN \"%s\"", but lame gives much smaller files (e.g. 3.1M instead of 11M) - it handles the silences more efficiently for a start).
        # Typical file sizes for a 30-minute lesson: OGG 2.7M, neroAacEnc 3.0M at 32000 (you might be able to put up with 1.8M at 18000 or 2.2M at 24000), MP3 3.1M, MP2 3.4M, faac 3.7M, WAV 152M
        # TODO try AAC+?  aacplusenc wavfile(or -) aacfile kbits, 10,12,14,18,20,24,32,40 (or 48 for stereo), but will need a player to test it
        # (mp2 could possibly be made a bit smaller by decreasing the -5, but don't make it as low as -10)
        elif out_type=="spx":
            self.rate = 32000 # could also use 16000 and -w, or even 8000, but those are not so good for language learning
            self.o=os.popen("speexenc -u --vbr --dtx - "+cond(write_to_stdout,"-",outputFile),"wb") # and write 16-bit little-endian mono
        elif out_type=="mp2":
            self.rate = 22050
            self.o=os.popen("toolame %s -s %f -v -5 -p 4 -m m - \"%s\"" % (cond(big_endian,"-x",""),self.rate/1000.0,cond(write_to_stdout,"-",outputFile)),"wb") # TODO check that toolame compiled on big-endian architectures really needs -x to accept little-endian input
        elif not out_type=="raw":
            if out_type=="wav": self.rate=22050 # try not to take TOO much disk space
            self.o=os.popen("sox %s - -t %s \"%s\"" % (self.soxParams(),out_type,cond(write_to_stdout,"-",outputFile)),"wb")
        else: self.o = open(outputFile,"wb")
        self.theLen = 0
        self.silences = []
    def soxParams(self):
        # Have 16-bit mono, signed, little-endian
        return ("-t raw "+sox_16bit+" "+sox_signed+" -r %d -c 1" % (self.rate,))+sox_little_endian
    def tell(self):
        # How many seconds have we had?  (2 because 16-bit)
        return 1.0*self.theLen/self.rate/2
    def addSilence(self,seconds,maybeBeep=True):
        if maybeBeep and seconds > beepThreshold: return self.addBeeps(seconds)
        self.silences.append(seconds)
        # Must add an integer number of samples
        sampleNo = int(0.5+seconds*self.rate)
        if not sampleNo: sampleNo=1 # so don't lock on rounding errors
        byteNo = sampleNo*2 # since 16-bit
        outfile_writeBytes(self.o,"\0"*byteNo)
        self.theLen += byteNo
    def addFile(self,file,length): # length ignored in this version
        fileType=soundFileType(file)
        if fileType=="mp3": file,fileType = theMp3FileCache.decode_mp3_to_tmpfile(file),"wav" # in case the system needs madplay etc rather than sox
        if riscos_sound:
            os.system("sox -t %s \"%s\" %s tmp0" % (fileType,file,self.soxParams()))
            handle=open("tmp0","rb")
        elif winsound or mingw32: handle = os.popen(("sox -t %s - %s - < \"%s\"" % (fileType,self.soxParams(),file)),"rb")
        else: handle = os.popen(("cat \"%s\" | sox -t %s - %s -" % (file,fileType,self.soxParams())),"rb")
        self.theLen += outfile_writeFile(self.o,handle,file)
        if riscos_sound:
            handle.close() ; os.unlink("tmp0")
    def addBeeps(self,gap):
        global beepType ; beepType = 0
        while gap > betweenBeeps+0.05:
            t1 = self.tell()
            self.addSilence(betweenBeeps/2.0)
            if riscos_sound:
                os.system(beepCmd(self.soxParams(),"tmp0"))
                data=read("tmp0") ; os.unlink("tmp0")
            else: data=os.popen(beepCmd(self.soxParams(),"-"),"rb").read()
            outfile_writeBytes(self.o,data)
            self.theLen += len(data)
            self.addSilence(betweenBeeps/2.0)
            gap -= (self.tell()-t1)
        self.addSilence(gap)
    def finished(self):
        if outputFile_appendSilence: self.addSilence(outputFile_appendSilence)
        self.silences.sort() ; self.silences.reverse()
        ttl = 0
        for i in range(len(self.silences)):
            self.silences[i] = int(self.silences[i])
            if self.silences[i] < 5:
                del self.silences[i:]
                break
            else: ttl += self.silences[i]
        if not app: show_info("Lengths of silences: %s (total %s)\n" % (self.silences,ttl))
        if not outputFile=="-": outfile_close(self.o)
def outfile_writeBytes(o,bytes):
    try: o.write(bytes)
    except IOError: outfile_write_error()
def outfile_close(o):
    try: o.close()
    except IOError: outfile_write_error()
def outfile_writeFile(o,handle,filename):
    data,theLen = 1,0
    while data:
        data = handle.read(102400)
        outfile_writeBytes(o,data)
        theLen += len(data)
    if not filename.startswith(partialsDirectory+os.sep): assert theLen, "No data when reading "+filename+": check for sox crash" # (but allow empty partials e.g. r5.  TODO if it's from EkhoSynth it could be a buggy version of Ekho)
    return theLen
def outfile_write_error(): raise IOError("Error writing to outputFile: either you are missing an encoder for "+out_type+", or the disk is full or something.")
def oggenc(): # 2016: some Windows builds are now called oggenc2
    global cached_oggenc
    try: return cached_oggenc
    except: pass
    if got_program("oggenc"): cached_oggenc = "oggenc"
    else: cached_oggenc = "oggenc2"
    return cached_oggenc
def lame_endian_parameters():
  # The input to lame will always be little-endian regardless of which architecture we're on and what kind of sox build we're using.
  # lame 3.97 has -x (swap endian) parameter, needed with little-endian i/p on little-endian architecture
  # lame 3.98+ has changed the default of -x and introduced explicit --big-endian and --little-endian.
  # (Note: None of this would be needed if we give lame a WAV input, as email-lesson.sh does.  But lame 3.97 on Windows faults on wav inputs.)
  lameVer = os.popen("lame --version").read()
  if lameVer.find("version ")>=0:
    lameVer = lameVer[lameVer.index("version "):].split()[1]
    if lameVer and '.' in lameVer and (lameVer[0]>'3' or intor0(lameVer[2:4])>97):
      # Got 3.98+ - explicitly tell it the endianness (but check for alpha releases first - some of them don't deal with either this or the 3.97 behaviour very well)
      if lameVer.find("alpha")>=0 and lameVer[0]=="3" and intor0(lameVer[2:4])==98: show_warning("Warning: You have a 3.98 alpha release of LAME.\nIf the MP3 file is white noise, try a different LAME version.")
      return " --little-endian"
  # otherwise fall-through to older lame behaviour:
  if big_endian: return "" # TODO are we sure we don't need -x on lame 3.97 PPC as well?
  else: return " -x"

def lame_quiet():
    if hasattr(sys.stderr,"isatty") and not sys.stderr.isatty(): return " --quiet"
    else: return ""

betweenBeeps = 5.0
beepType = 0
beepCmds = ["sox -t nul - %s %s synth trapetz 880 trim 0 0:0.05",
"sox -t nul - %s %s synth sine 440 trim 0 0:0.05"]*3+["sox -t nul - %s %s synth trapetz 440 trim 0 0:0.05",
"sox -t nul - %s %s synth sine 440 trim 0 0:0.05"]*2+["sox -t nul - %s %s synth 220 trim 0 0:0.05"]
def beepCmd(soxParams,fname):
  global beepType
  r = beepCmds[beepType]
  beepType += 1
  if beepType==len(beepCmds): beepType=0
  if unix:
      # not all versions of sox support -t nul; /dev/zero is safer on Unix
      r=r.replace("-t nul -","%s /dev/zero" % (soxParams,))
  r = r % (soxParams,fname)
  return r

# -----------------------------------------------------

# A sound collector for our .sh shell-script format:
class ShSoundCollector(object):
    def __init__(self):
        self.file2command = {}
        self.commands = ["C() { echo -n $1% completed $'\r' 1>&2;}"]
        self.seconds = self.lastProgress = 0
        if write_to_stdout: self.o=sys.stdout
        else: self.o = open(outputFile,"wb")
        start = """#!/bin/bash
if echo "$0"|grep / >/dev/null; then export S="$0"; else export S=$(which "$0"); fi
export P="-t raw %s %s -r 44100 -c 1"
tail -1 "$S" | bash\nexit\n""" % (sox_16bit,sox_signed) # S=script P=params for sox (ignore endian issues because the wav header it generates below will specify the same as its natural endian-ness)
        outfile_writeBytes(self.o,start)
        self.bytesWritten = len(start) # need to keep a count because it might be stdout
        self.commands.append("sox $P - -t wav - </dev/null 2>/dev/null") # get the wav header with unspecified length
    def tell(self): return self.seconds
    def addSilence(self,seconds,maybeBeep=True):
        if maybeBeep and seconds > beepThreshold: return self.addBeeps(seconds)
        # Must add an integer number of samples
        sampleNo = int(0.5+seconds*44100)
        if not sampleNo: sampleNo=1 # so don't lock on rounding errors (however this is not worth a separate dd command, hence condition below)
        byteNo = sampleNo*2 # since 16-bit
        if sampleNo>1: self.commands.append("dd if=/dev/zero bs=%d count=1 2>/dev/null" % byteNo)
        self.seconds += sampleNo/44100.0
    def addBeeps(self,gap):
        global beepType ; beepType = 0
        while gap > betweenBeeps+0.05:
            t1 = self.tell()
            self.addSilence(betweenBeeps/2.0)
            self.commands.append(beepCmd("$P","-"))
            self.seconds += 0.05
            self.addSilence(betweenBeeps/2.0)
            gap -= (self.tell()-t1)
        self.addSilence(gap)
    def addFile(self,file,length):
        fileType=soundFileType(file)
        self.seconds += length
        if not file in self.file2command:
            if fileType=="mp3": fileData,fileType = decode_mp3(file),"wav" # because remote sox may not be able to do it
            elif compress_SH and unix: handle=os.popen("cat \""+file+"\" | sox -t "+fileType+" - -t "+fileType+" "+sox_8bit+" - 2>/dev/null","rb") # 8-bit if possible (but don't change sample rate, as we might not have floating point)
            else: handle = open(file,"rb")
            offset, length = self.bytesWritten, outfile_writeFile(self.o,handle,file)
            self.bytesWritten += length
            # dd is more efficient when copying large chunks - try to align to 1k
            first_few_bytes = min(length,(1024-(offset%1024))%1024)
            cmd = dd_command(offset,first_few_bytes)
            length -= first_few_bytes ; offset += first_few_bytes
            last_few_bytes = length % 1024
            cmd += dd_command(offset,length-last_few_bytes)
            cmd += dd_command(offset+length-last_few_bytes,last_few_bytes)
            assert cmd, "0-length file??"
            if len(cmd)==1: cmd=cmd[0]
            else: cmd="("+(";".join(cmd))+")"
            self.file2command[file] = cmd + " 2>/dev/null|sox -t "+fileType+" - $P -" # (don't want the stderr o/p from dd, but do want the stderr o/p from sox if any)
        self.commands.append(self.file2command[file])
        if int(self.seconds*100/lessonLen)>self.lastProgress:
            self.lastProgress = int(self.seconds*100/lessonLen)
            self.commands.append("C %d" % self.lastProgress)
    def finished(self):
        if outputFile_appendSilence: self.addSilence(outputFile_appendSilence,False)
        outfile_writeBytes(self.o,"\n") # so "tail" has a start of a line
        self.commands.append("C 100;echo 1>&2;exit")
        for c in self.commands: outfile_writeBytes(self.o,c+"\n")
        outfile_writeBytes(self.o,"tail -%d \"$S\" | bash\n" % (len(self.commands)+1))
        if not write_to_stdout:
            outfile_close(self.o)
            if unix: os.system("chmod +x \"%s\"" % (outputFile,))
def dd_command(offset,length):
    if not length: return []
    gcd,b = offset,length
    while b: gcd,b = b,gcd%b
    return ["dd if=\"$S\" bs=%d skip=%d count=%d" % (gcd,offset/gcd,length/gcd)]

warned_about_sox_decode = 0
def warn_sox_decode():
    global warned_about_sox_decode
    if not warned_about_sox_decode:
        r = []
        if macsound: r.append("the sox bundled with Mac Gradint was not compiled with MP3 support (please install madplay or a better sox)") # (or upgrade to a version of Mac OS that has afconvert)
        if not sox_ignoreLen: r.append("some versions of sox truncate the end of MP3s (please upgrade sox or install madplay/mpg123)") # sox 14.3+ (sox_ignoreLen set) should be OK
        if r: r.insert(0,"Had to use sox to decode MP3")
        if r: show_warning('; '.join(r))
        warned_about_sox_decode = 1
def decode_mp3(file): # Returns WAV data including header.  TODO: this assumes it's always small enough to read the whole thing into RAM (should be true if it's 1 word though, and decode_mp3 isn't usually used unless we're making a lesson file rather than running something in justSynthesize)
    if riscos_sound:
        warn_sox_decode()
        os.system("sox -t mp3 \""+file+"\" -t wav"+cond(compress_SH," "+sox_8bit,"")+" tmp0")
        data=read("tmp0") ; os.unlink("tmp0")
        return data
    elif madplay_path:
        oldDir = os.getcwd()
        d=os.popen(madplay_path+cond(compress_SH," -R 16000 -b 8","")+" -q \""+changeToDirOf(file)+"\" -o wav:-","rb").read()
        os.chdir(oldDir) ; return d
    elif got_program("mpg123"): # do NOT try to read its stdout (not only does it write 0 length, which we can fix, but some versions can also write wrong bitrate, which is harder for us to fix)
        oldDir = os.getcwd()
        tfil = os.tempnam()+dotwav
        os.system("mpg123 -q -w \""+tfil+"\" \""+changeToDirOf(file)+"\"")
        if compress_SH and gotSox: dat = os.popen("sox \""+tfil+"\" -t wav "+sox_8bit+" - ","rb").read()
        else: dat = open(tfil).read()
        os.unlink(tfil) ; os.chdir(oldDir) ; return dat
    elif macsound and got_program("afconvert"):
        tfil = os.tempnam()+dotwav
        system("afconvert -f WAVE -d I16@44100 \""+file+"\" \""+tfil+"\"")
        if compress_SH and gotSox: dat = os.popen("sox \""+tfil+"\" -t wav "+sox_8bit+" - ","rb").read()
        else: dat = open(tfil).read()
        os.unlink(tfil) ; return dat
    elif unix:
        if gotSox:
            warn_sox_decode()
            return os.popen("cat \""+file+"\" | sox -t mp3 - -t wav"+cond(compress_SH," "+sox_8bit,"")+" - ","rb").read()
        else:
            show_warning("Don't know how to decode "+file+" on this system")
            return ""
    else: raise Exception("decode_mp3 called on a setup that's not Unix and doesn't have MADplay.  Need to implement non-cat sox redirect.")

# while we're at it:
class Mp3FileCache(object):
    def __init__(self): self.fileCache = {}
    def __del__(self):
        import os # as it might already have been gc'd
        for v in self.fileCache.values():
            try: os.remove(v)
            except: pass # somebody may have removed it already
    def decode_mp3_to_tmpfile(self,file):
        if not file in self.fileCache:
            self.fileCache[file] = os.tempnam()+dotwav
            write(self.fileCache[file],decode_mp3(file))
        return self.fileCache[file]
theMp3FileCache = Mp3FileCache()

# -----------------------------------------------------

soundCollector = None # by default don't do this

try:
    # for legacy scripts using the old name
    outputFile = bigOutputFile
    outputFile_appendSilence = bigOutputFile_appendSilence
except NameError: pass

sample_table_hack = 0 # if 1, assumes collector will examine each sample only once and after that the file can be deleted (if temporary) although its name may again be given to the collector
if outputFile:
    # TODO: GUI duplicates some of this logic; need better encapsulation
    out_type,write_to_stdout = "raw",(outputFile=="-")
    if extsep in outputFile:
        out_type = outputFile[outputFile.rindex(extsep)+1:].lower()
        write_to_stdout = (outputFile.lower()=="-"+extsep+out_type)
        if riscos_sound and not out_type in ["raw","sh"]: sys.stderr.write("WARNING: On RISC OS, setting outputFile to \"%s\" will likely NOT work, because it needs Python's popen().  Continuing anyway because you might have a version of RISC OS Python that's better than the one I tested on, but if you get errors, try setting outputFile=\"rawfile\" and converting it as a separate step afterwards (needs lots of disk space), or try the .sh format mentioned in advanced/txt.\n" % (outputFile,))
    if write_to_stdout and winsound: sys.stderr.write("WARNING - outputting to stdout in Windows could give text-mode/binary-mode issues\n")
    assert gotSox or out_type=="sh", "Cannot have (non-SH) outputFile when 'sox' is not available on the system"
    if out_type=="sh": soundCollector,sample_table_hack = ShSoundCollector(), 1
    else: soundCollector = SoundCollector()
    waitBeforeStart = 0
    if unix and out_type in ["ogg","mp3"] and os.uname()[4].startswith("arm"): show_warning("Note: On armel, compile lame or oggenc with -fno-finite-math-only, or use lame -b 64 (or higher)")
if not (soundCollector and out_type=="sh"): compress_SH = False # regardless of its initial setting (because it's used outside ShSoundCollector)
def collector_time(): return soundCollector.tell()
def collector_sleep(s): soundCollector.addSilence(s)

##########################################################

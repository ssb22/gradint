# This file is part of the source code of
# gradint v0.9956 (c) 2002-2010 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of recording.py - GUI-based management of recorded words

try: import tkSnack
except: tkSnack = 0

class InputSource(object):
    def startRec(self,outFile,lastStopRecVal=None): pass # start recording to outFile
    def stopRec(self): pass # stop recording
    def close(self): pass # stop everything
    def currentTime(self): return 0 # (makes sense only for PlayerInput, but here just in case)
    def __del__(self): self.close()

class MicInput(InputSource):
    def __init__(self):
        rates = tkSnack.audio.rates()
        for rate in [22050, 16000, 24000, 44100]:
            if rate in rates:
                self.rate = rate ; return
        if rates: self.rate = max(rates)
        else: self.rate = None
    def startRec(self,outFile,lastStopRecVal=None):
        if not self.rate: return # TODO tell the user we can't record anything on this system (currently we just let them find out)
        self.sound = tkSnack.Sound(file=outFile, rate=self.rate, channels=1, encoding="Lin16")
        self.sound.record()
    def stopRec(self): self.sound.stop()

class PlayerInput(InputSource): # play to speakers while recording to various destinations
    def __init__(self,fileToPlay,startNow=True,startTime=0): # (if startNow=False, starts when you start recording)
        global paranoid_file_management
        if use_unicode_filenames: fileToPlay=ensure_unicode(fileToPlay)
        else:
            assert not type(fileToPlay)==type(u"")
            if not paranoid_file_management and filter(lambda x:ord(x)>=128,list(fileToPlay)): paranoid_file_management = True # hack to try to work around a Tkinter fault on Linux with utf-8 filenames
        if paranoid_file_management: # try to ensure it's ready for reading
            if filelen(fileToPlay)<1048576:
                # only small - copy to temp 1st
                self.fileToDel = os.tempnam()+fileToPlay[fileToPlay.rfind(extsep):]
                open(self.fileToDel,"wb").write(open(fileToPlay,"rb").read())
                fileToPlay=self.fileToDel
            else: open(fileToPlay)
        if fileToPlay.lower().endswith(dotwav) and filelen(fileToPlay)<1048576: self.sound=tkSnack.Sound(load=fileToPlay) # in-memory if <1M (saves problems with Windows keeping them open even after object deleted), TODO is this still needed now that .destroy() is called properly?  (but might be a good idea to keep it in anyway)
        else: self.sound = tkSnack.Sound(file=fileToPlay)
        self.startSample = 0
        self.sampleRate = self.sound.info()[1]
        self.length = self.sound.length()*1.0/self.sampleRate
        if not self.length: self.length=lengthOfSound(fileToPlay) # tkSnack bug workaround.  NB don't just set it to 3 because it may be less than that, and user may press Record before the 3secs are up, expecting to record from mic.
        self.autostop_thread_id = 0
        self.inCtor = 1
        if startNow: self.startPlaying(max(0,int(startTime*self.sampleRate)))
        self.inCtor = 0
    def startPlaying(self,curSample=0):
        theISM.nowPlaying = self
        tkSnack.audio.stop() # as we might be still in c'tor and just about to be assigned to replace the previously-playing sound (i.e. it might not have stopped yet), and we don't want to confuse elapsedTime
        self.sound.play(start=curSample)
        self.startSample = curSample ; self.startTime = time.time()
        self.autostop()
    def autostop(self,thread_id=None):
        if thread_id==None:
            self.autostop_thread_id += 1
            thread_id=self.autostop_thread_id
        elif not thread_id==self.autostop_thread_id: return # a stale autostop thread
        if not theISM or not theISM.nowPlaying==self or not tkSnack or not tkSnack.audio: return # closing down anyway
        elapsedTime = self.elapsedTime()
        if elapsedTime>=self.length-self.startSample*1.0/self.sampleRate: self.close()
        else:
            import thread
            def stopMe(self,thread_id):
                time.sleep(max(0.5,self.length-self.startSample*1.0/self.sampleRate-elapsedTime))
                self.autostop(thread_id)
            thread.start_new_thread(stopMe,(self,thread_id))
    def elapsedTime(self):
        try: t=tkSnack.audio.elapsedTime()
        except: t=0.0
        if t==0.0: t=time.time()-self.startTime
        return t
    def currentSample(self): return int(self.elapsedTime()*self.sampleRate)+self.startSample
    def currentTime(self): return self.currentSample()*1.0/self.sampleRate
    def startRec(self,outFile,lastStopRecVal=None):
        if lastStopRecVal: self.recordingStartSample = lastStopRecVal
        elif theISM.nowPlaying==self: self.recordingStartSample = self.currentSample()
        else:
            self.startPlaying()
            self.recordingStartSample = 0
        self.fileToWrite = outFile
    def stopRec(self,closing = False):
        if not hasattr(self,"fileToWrite"): return
        curSample = self.currentSample()
        self.sound.stop()
        self.sound.write(self.fileToWrite,start=self.recordingStartSample,end=curSample)
        if not closing: self.startPlaying(curSample)
        del self.fileToWrite
        return curSample
    def close(self):
        if not hasattr(self,"sound"): return # called twice?
        self.stopRec(True)
        if theISM.nowPlaying == self:
            theISM.nowPlaying = None
            self.sound.stop()
            self.sound.destroy()
        del self.sound
        if hasattr(self,"fileToDel"): os.unlink(self.fileToDel)
        theISM.finished(self)

        global theRecorderControls
        try: theRecorderControls
        except: theRecorderControls=0
        if theRecorderControls:
            if self.inCtor: # tried to skip off end - DO ensure the GUI resets its controls when that happens, even if it has "protected" itself due to restarting the sample at different position
                theRecorderControls.current_recordFrom_button = theRecorderControls.old_recordFrom_button
            app.todo.undoRecordFrom=True # we might not be the GUI thread

if not tkSnack:
  if macsound: # might still be able to use Audio Recorder
    if fileExists("AudioRecorder.zip"): unzip_and_delete("AudioRecorder.zip")
    if fileExists("Audio Recorder.app/plist"): # Audio Recorder with our special preferences list
        runAudioRecorderYet = 0
        def MacStartRecording():
            global runAudioRecorderYet
            if not runAudioRecorderYet: os.system("mv ~/Library/Preferences/com.benshan.AudioRecorder31.plist ~/Library/Preferences/com.benshan.AudioRecorder31.plist-OLD 2>/dev/null ; cp Audio\\ Recorder.app/plist ~/Library/Preferences/com.benshan.AudioRecorder31.plist; open Audio\\ Recorder.app")
            os.system("osascript -e 'Tell application \"Audio Recorder\" to Record'")
            runAudioRecorderYet = 1
        def MacStopRecording(): os.system("osascript -e 'Tell application \"Audio Recorder\" to Stop'")
        MacRecordingFile = "/tmp/audiorec-output-for-gradint.wav" # specified in the plist
        def quitAudioRecorder():
            if runAudioRecorderYet: os.system("osascript -e 'Tell application \"Audio Recorder\" to quit' ; rm ~/Library/Preferences/com.benshan.AudioRecorder31.plist ; mv ~/Library/Preferences/com.benshan.AudioRecorder31.plist-OLD ~/Library/Preferences/com.benshan.AudioRecorder31.plist 2>/dev/null")
        import atexit ; atexit.register(quitAudioRecorder)
        del MicInput
        class MicInput(InputSource): # Mac Audio Recorder version
            def startRec(self,outFile,lastStopRecVal=None):
                self.fileToWrite = outFile
                MacStartRecording()
            def stopRec(self):
                MacStopRecording()
                os.rename(MacRecordingFile,self.fileToWrite)
        tkSnack = "MicOnly"
  elif unix and isDirectory("/dev/snd") and got_program("arecord"): # no tkSnack, but can record via ALSA
    del MicInput
    class MicInput(InputSource):
        def startRec(self,outFile,lastStopRecVal=0.5):
            self.pid = os.spawnl(os.P_NOWAIT,"/bin/bash","/bin/bash","-c","arecord -f S16_LE -r 22050 "+shell_escape(outFile))
            time.sleep(lastStopRecVal) # allow process to start
        def stopRec(self):
            os.kill(self.pid,2) # INT
            return 0.3
    tkSnack = "MicOnly"

class InputSourceManager(object):
    def __init__(self):
        self.currentInputSource = None
        self.currentOutfile = self.nowPlaying = None
        # (nowPlaying is for PlayerInputSource to manage)
    def setInputSource(self,inputSource):
        self.stopRecording()
        if self.currentInputSource: self.currentInputSource.close()
        self.currentInputSource = inputSource
    def finished(self,inputSource): # called by the inputSource itself; we don't need to call its close()
        if not self.currentInputSource==inputSource: return # irrelevant
        self.stopRecording()
        self.currentInputSource = None
    def startRecording(self, newOutfile):
        if not self.currentInputSource: self.currentInputSource = MicInput()
        if self.currentOutfile: self.currentInputSource.startRec(newOutfile,self.currentInputSource.stopRec())
        else: self.currentInputSource.startRec(newOutfile)
        self.currentOutfile = newOutfile
    def stopRecording(self):
        if self.currentOutfile: self.currentInputSource.stopRec()
        self.currentOutfile = None
theISM = InputSourceManager() ; del InputSourceManager # singleton

def wavToMp3(directory):
    # Compress all WAVs in directory to MP3 (CBR for gradint i/p)
    # don't worry about progress.txt - mergeProgress will recognise WAVs replaced with mp3
    for l in os.listdir(directory):
        if l.lower().endswith(dotwav):
            needRetry = 1 ; tries = 0
            while needRetry:
                tries += 1
                needRetry = system("lame \"%s\" --cbr -b 48 -m m -o \"%s\"" % (directory+os.sep+l, directory+os.sep+l[:-len(dotwav)]+dotmp3))
                if not needRetry: os.remove(directory+os.sep+l)
                elif paranoid_file_management and tries<10: time.sleep(0.5)
                else:
                    show_warning("lame failed on "+directory+os.sep+l) ; break
        elif isDirectory(directory+os.sep+l):
            wavToMp3(directory+os.sep+l)

def makeMp3Zips(baseDir,outDir,zipNo=0,direc=None):
    zipSplitThreshold = 5*1048576 # to be safe (as will split when it goes OVER that)
    if baseDir==outDir: return zipNo # omit
    elif not direc:
        for f in os.listdir(baseDir): zipNo = makeMp3Zips(baseDir,outDir,zipNo,f)
    elif isDirectory(baseDir+os.sep+direc): zipNo = makeMp3Zips(baseDir+os.sep+direc,outDir,zipNo)
    else:
        if zipNo: zipNo -= 1
        zipfile = None
        while not zipfile or (fileExists(zipfile) and filelen(zipfile) >= zipSplitThreshold):
            zipNo += 1
            zipfile = outDir+os.sep+"zipfile"+str(zipNo)+extsep+"zip"
        system("zip -9 \"%s\" \"%s\"" % (zipfile,baseDir+os.sep+direc))
    return zipNo

class RecorderControls:
    def __init__(self):
        self.snack_initialized = 0
        self.currentDir = samplesDirectory
        setup_samplesDir_ifNec()
        self.coords2buttons = {}
        self.syncFlag = False
        self.always_enable_rerecord = self.always_enable_synth = False
        self.old_recordFrom_button = None
        self.renamevar_msg = "Renaming a variant from the GUI is not implemented yet. Please press the Advanced button and do it from the file manager."
    def changeDir(self,newDir):
        self.undraw()
        oldDir = self.currentDir
        self.currentDir = newDir
        self.draw(oldDir)
    def global_rerecord(self,*args):
        self.undraw()
        self.always_enable_rerecord = True
        self.draw()
    def enable_synth(self,*args):
        self.undraw()
        self.always_enable_synth = True
        self.draw()
    def finished(self,*args):
        app.master.title(appTitle)
        self.undraw()
        del app.scanrow
        if recorderMode: app.cancel()
        else: app.todo.set_main_menu=1
    def undraw(self):
        if hasattr(self,"renameToCancel"): del self.renameToCancel
        self.coords2buttons = {}
        del self.ourCanvas
        self.frame.pack_forget()
        theISM.setInputSource(None)
    def addButton(self,row,col,text,command,colspan=None):
        if (row,col) in self.coords2buttons: self.coords2buttons[(row,col)].grid_forget()
        b = makeButton(self.grid,text=text,command=command)
        b.bind('<FocusIn>',lambda *args:self.scrollIntoView(b))
        if not hasattr(app,"gotFocusInHandler"):
            # (see scrollIntoView method's use of justGotFocusIn)
            app.gotFocusInHandler=1
            def set(*args):
                def clear(*args):
                    try: del app.justGotFocusIn
                    except: pass
                app.justGotFocusIn = 1
                app.after(1, clear) # (that delay is quite short, but it shouldn't execute until after the current chain of FocusIn events finishes)
            app.bind('<FocusIn>',set)
        self.coords2buttons[(row,col)] = b
        if not colspan:
            if not col: colspan=1+3*len(self.languagesToDraw)
            else: colspan = 1
        if olpc and colspan==1: # don't have the biggest font otherwise can't get to Record buttons on rightmost column
            if len(text)>6: self.coords2buttons[(row,col)]["font"]="Helvetica 9"
            else: self.coords2buttons[(row,col)]["font"]="Helvetica 12"
        if col: self.coords2buttons[(row,col)].grid(row=row,column=col,columnspan=colspan)
        else: self.coords2buttons[(row,col)].grid(row=row,column=0,columnspan=colspan,sticky="w")
    def addLabel(self,row,col,utext):
        if (row,col) in self.coords2buttons: self.coords2buttons[(row,col)].grid_forget()
        self.coords2buttons[(row,col)] = self.makeLabel_lenLimit(utext)
        self.coords2buttons[(row,col)].grid(row=row,column=col,sticky="w")
        if col==0: self.coords2buttons[(row,col)].bind('<Button-1>',lambda *args:self.startRename(row,col,utext))
    def makeLabel_lenLimit(self,utext): return Tkinter.Label(self.grid,text=utext,wraplength=int(self.ourCanvas.winfo_screenwidth()/(1+len(self.languagesToDraw))))
    def addSynthLabel(self,filename,row,col):
        try: ftext = ensure_unicode(u8strip(open(filename).read().strip(wsp)))
        except IOError: return False
        l = self.makeLabel_lenLimit(ftext)
        l.grid(row=row,column=col,columnspan=2,sticky="w")
        l.bind('<Button-1>',lambda *args:self.startSynthEdit(l,row,col,filename))
        return True # do NOT put it in self.coords2buttons (not to do with space bar stuff etc)
    def startSynthEdit(self,l,row,col,filename):
        if hasattr(self,"renameToCancel"):
          rr,cc = self.renameToCancel
          self.cancelRename(rr,cc)
        if l: l.grid_forget()
        editText,editEntry = addTextBox(self.grid,"nopack")
        try: editText.set(ensure_unicode(u8strip(open(filename).read().strip(wsp))))
        except IOError: pass
        editEntry.grid(row=row,column=col,sticky='we',columnspan=2)
        editEntry.bind('<Return>',lambda *args:self.doEdit(editText,editEntry,row,col,filename))
        editEntry.bind('<Escape>',lambda *args:self.cancelEdit(editEntry,row,col,filename))
        focusButton(editEntry)
        if hasattr(self.coords2buttons.get((row-1,col+1),""),"is_synth_label"):
            self.addLabel(row-1,col+1,localise("(synth'd)"))
            self.coords2buttons[(row-1,col+1)].is_synth_label = True
    def doEdit(self,editText,editEntry,row,col,filename):
        text = asUnicode(editText.get()).encode("utf-8").strip(wsp)
        if text: open(filename,"w").write(text+"\n")
        else:
            try: os.remove(filename)
            except: pass
        self.cancelEdit(editEntry,row,col,filename)
        if row+1 < self.addMoreRow and (row+1,col+1) in self.coords2buttons: focusButton(self.coords2buttons[(row+1,col+1)]) # focus the next "synth" button if it exists (don't press it as well like file renaming because it might be a variant etc, TODO can we skip variants?)
    def cancelEdit(self,editEntry,row,col,filename):
        editEntry.grid_forget()
        labelAdded = self.addSynthLabel(filename,row,col)
        if hasattr(self.coords2buttons.get((row-1,col+1),""),"is_synth_label"):
            if labelAdded: self.addLabel(row-1,col+1,localise("(synth'd)"))
            else: self.addButton(row-1,col+1,text=localise("Synthesize"),command=(lambda *args:self.startSynthEdit(None,row,col,filename)))
            self.coords2buttons[(row-1,col+1)].is_synth_label = True
    def all2mp3_or_zip(self,*args):
        self.CompressButton["text"] = localise("Compressing, please wait")
        if got_program("lame"): wavToMp3(self.currentDir) # TODO not in the GUI thread !! (but lock our other buttons while it's doing it)
        if got_program("zip") and (explorerCommand or winCEsound) and (not got_program("lame") or tkMessageBox.askyesno(app.master.title(),localise("All recordings have been compressed to MP3.  Do you also want to make a ZIP file for sending as email?"))):
            try: os.mkdir(self.currentDir+os.sep+"zips")
            except: pass # already exists?
            numZips = makeMp3Zips(self.currentDir,self.currentDir+os.sep+"zips")
            if numZips:
                openDirectory(self.currentDir+os.sep+"zips",1)
                if numZips>1: app.todo.alert=localise("Please send the %d zip files as %d separate messages, in case one very large message doesn't get through.") % (zipNo,zipNo)
                else: app.todo.alert=localise("You may now send the zip file by email.")
            else: app.todo.alert=localise("No recordings found")
        self.undraw() ; self.draw()
    def startRename(self,row,col,filename):
        if hasattr(self,"renameToCancel"):
          rr,cc = self.renameToCancel
          self.cancelRename(rr,cc)
        if self.has_variants and filename.find(" (")>-1:
            app.todo.alert=self.renamevar_msg
            return
        self.renameToCancel = (row,col)
        if (row,col) in self.coords2buttons: self.coords2buttons[(row,col)].grid_forget()
        renameText,renameEntry = addTextBox(self.grid,"nopack")
        renameEntry['width']=min(8,len(filename)+2)
        renameEntry.theText = renameText
        renameEntry.origName = filename
        self.coords2buttons[(row,col)] = renameEntry
        renameEntry.grid(row=row,column=col,sticky='we')
        number=filename
        if number.startswith("word"): number=number[4:]
        if number and "0"<=number[0]<="9":
            renameText.set(number)
            selectAllFunc = selectAllButNumber
        else:
            renameText.set(filename)
            selectAllFunc = selectAll
        class E: pass
        e=E() ; e.widget = renameEntry
        self.ourCanvas.after(50,lambda *args:(e.widget.focus(),self.scrollIntoView(e.widget),selectAllFunc(e)))
        renameEntry.bind('<Return>',lambda *args:self.doRename(row,col))
        renameEntry.bind('<Escape>',lambda *args:self.cancelRename(row,col))
    def doRename(self,row,col):
        if hasattr(self,"renameToCancel"): del self.renameToCancel
        origName = self.coords2buttons[(row,col)].origName
        newNames = filter(lambda x:x,asUnicode(self.coords2buttons[(row,col)].theText.get()).split("\n")) # multiline paste, ignore blank lines
        for newName in newNames:
            if not origName: # extra lines - need to get their origNames
                if row==self.addMoreRow: self.addMore()
                elif not (row,col) in self.coords2buttons: row += 1 # skip extra row if there are notes
                origName=self.coords2buttons[(row,col)]["text"]
            if self.has_variants and origName.find(" (")>-1:
                app.todo.alert=self.renamevar_msg
                break
            if len(newNames)>1 and not '0'<=newName[0]<='9': # multiline paste and not numbered - we'd better keep the original number
                o2 = origName
                if o2.startswith("word"): o2=o2[4:]
                if intor0(o2): newName=o2+"-"+newName
            if isDirectory(unicode2filename(self.currentDir+os.sep+origName)):
                try: os.rename(unicode2filename(self.currentDir+os.sep+origName),unicode2filename(self.currentDir+os.sep+newName))
                except:
                    tkMessageBox.showinfo(app.master.title(),localise("Could not rename %s to %s") % (origName,newName))
                    return
                self.addButton(row,col,text=newName,command=(lambda e=None,f=self.currentDir+os.sep+newName:self.changeDir(f)))
            else: # not a directory - rename individual files
                self.doStop() # just in case
                for lang in self.languagesToDraw:
                    updated=False
                    for ext in [dottxt, dotwav, dotmp3]:
                      if fileExists_stat(unicode2filename(self.currentDir+os.sep+origName+"_"+lang+ext)):
                        try: os.rename(unicode2filename(self.currentDir+os.sep+origName+"_"+lang+ext),unicode2filename(self.currentDir+os.sep+newName+"_"+lang+ext))
                        except:
                            tkMessageBox.showinfo(app.master.title(),localise("Could not rename %s to %s") % (origName+"_"+lang+ext,newName+"_"+lang+ext)) # TODO undo any that did succeed first!  + check for destination-already-exists (OS may not catch it)
                            return
                        self.updateFile(unicode2filename(newName+"_"+lang+ext),row,self.languagesToDraw.index(lang),cond(ext==dottxt,0,2)) # TODO the 2 should be 1 if and only if we didn't just record it
                        updated=True
                    if not updated: self.updateFile(unicode2filename(newName+"_"+lang+dotwav),row,self.languagesToDraw.index(lang),0)
                self.addLabel(row,col,newName)
            # TODO what about updating progress.txt with wildcard changes (cld be going too far - we have the move script in utilities)
            origName = None # get any others from the form
            row += 1
        if len(newNames)==1 and row<self.addMoreRow: # put cursor on the next one
            if not (row,col) in self.coords2buttons: row += 1 # skip extra row if there are notes
            if row<self.addMoreRow:
              origName=self.coords2buttons[(row,col)]["text"]
              if not isDirectory(unicode2filename(self.currentDir+os.sep+origName)): self.startRename(row,0,origName)
    def cancelRename(self,row,col):
        if hasattr(self,"renameToCancel"): del self.renameToCancel
        origName = self.coords2buttons[(row,col)].origName
        if isDirectory(unicode2filename(self.currentDir+os.sep+origName)): self.addButton(row,col,text=origName,command=(lambda e=None,f=ensure_unicode(self.currentDir+os.sep+origName).encode('utf-8'):self.changeDir(f)))
        else: self.addLabel(row,col,origName)
    def updateFile(self,filename,row,languageNo,state,txtExists="unknown"): # state: 0 not exist, 1 already existed, 2 we just created it
        if not os.sep in filename: filename = self.currentDir+os.sep+filename
        recFilename = filename
        if recFilename.lower().endswith(dotmp3): recFilename=recFilename[:-len(dotmp3)]+dotwav # always record in WAV; can compress to MP3 after
        if state: # exists
            if not tkSnack or tkSnack=="MicOnly": self.addButton(row,2+3*languageNo,text="Play",command=(lambda e=None,f=filename:(self.doStop(),SampleEvent(f).play())))  # but if got full tkSnack, might as well use setInputSource instead to be consistent with the non-_ version:
            else: self.addButton(row,2+3*languageNo,text=localise("Play"),command=(lambda e=None,f=filename:(self.doStop(),theISM.setInputSource(PlayerInput(f,not self.syncFlag)))))
            if tkSnack and (state==2 or self.always_enable_rerecord):
                self.addButton(row,3+3*languageNo,text=localise("Re-record"),command=(lambda e=None,f=recFilename,r=row,l=languageNo:self.doRecord(f,r,l,needToUpdatePlayButton=(not filename==recFilename))))
            else:
                self.addLabel(row,3+3*languageNo,"")
                self.need_reRecord_enabler = not (not tkSnack)
        else: # does not exist
            synthFilename = filename[:filename.rfind(extsep)]+dottxt
            if txtExists=="unknown": txtExists=fileExists(synthFilename)
            if txtExists: self.addLabel(row,2+3*languageNo,localise("(synth'd)"))
            elif self.always_enable_synth and get_synth_if_possible(self.languagesToDraw[languageNo],0): self.addButton(row,2+3*languageNo,text=localise("Synthesize"),command=(lambda *args:self.startSynthEdit(None,row+1,1+3*languageNo,synthFilename)))
            else: self.addLabel(row,2+3*languageNo,localise("(empty)"))
            self.coords2buttons[(row,2+3*languageNo)].is_synth_label = True
            if winCEsound and not tkSnack: self.addLabel(row,3+3*languageNo,"")
            else: self.addButton(row,3+3*languageNo,text=localise("Record"),command=(lambda e=None,f=recFilename,r=row,l=languageNo:self.doRecord(f,r,l)))
    def add_addMore_button(self):
        if winCEsound and not tkSnack: pass # no 'add more words' button on WinCE; use PocketPC record button instead
        else: self.addButton(self.addMoreRow,0,text=localise("Add more words"),command=(lambda *args:self.addMore()),colspan=cond(self.need_reRecord_enabler,2,4))
        if self.need_reRecord_enabler: self.addButton(self.addMoreRow,2,text=localise("Re-record"),command=(lambda *args:self.global_rerecord()),colspan=2)
        self.addButton(self.addMoreRow,4,text=localise("New folder"),command=(lambda *args:self.newFolder()),colspan=3)
    def del_addMore_button(self):
        if (self.addMoreRow,0) in self.coords2buttons: self.coords2buttons[(self.addMoreRow,0)].grid_forget() # old 'add more' button
        if (self.addMoreRow,2) in self.coords2buttons: self.coords2buttons[(self.addMoreRow,2)].grid_forget() # old 're-record' button
        self.coords2buttons[(self.addMoreRow,4)].grid_forget() # old 'new folder' button
    def addMore(self,*args):
        self.del_addMore_button()
        for r in range(5):
            if self.maxPrefix<=99: prefix = "word%02d" % self.maxPrefix
            else: prefix = "word_%04d" % self.maxPrefix
            self.addLabel(self.addMoreRow,0,utext=prefix)
            for lang in self.languagesToDraw:
                self.updateFile(unicode2filename(prefix+"_"+lang+dotwav),self.addMoreRow,self.languagesToDraw.index(lang),state=0)
                self.gridLabel(lang,self.addMoreRow)
            self.addMoreRow += 2 ; self.maxPrefix += 1
        self.add_addMore_button()
    def gridLabel(self,lang,row): Tkinter.Label(self.grid,text=" "+localise(cond(lang.find("-meaning_")>-1,"meaning",lang))+": ").grid(row=row,column=1+3*self.languagesToDraw.index(lang))
    def doRecord(self,filename,row,languageNo,needToUpdatePlayButton=False):
        if not tkSnack: return tkMessageBox.showinfo(app.master.title(),localise("Sorry, cannot record on this computer because the tkSnack library (python-tksnack) is not installed."))
        theISM.startRecording(filename)
        if needToUpdatePlayButton: self.updateFile(filename,row,languageNo,2)
        self.coords2buttons[(row,3+3*languageNo)]["text"]=localise("Stop")
        self.updateForStopOrChange()
        self.currentRecording = (filename,row,languageNo)
        self.coords2buttons[(row,3+3*languageNo)]["command"]=(lambda *args:self.doStop())
        if app.scanrow.get()=="2": # "stop"
          focusButton(self.coords2buttons[(row,3+3*languageNo)])
        else:
          moved = 0
          if app.scanrow.get()=="1": # move along 1st
            while languageNo+1<len(self.languagesToDraw):
              languageNo += 1
              if (row,3+3*languageNo) in self.coords2buttons:
                  focusButton(self.coords2buttons[(row,3+3*languageNo)])
                  return
            languageNo = 0 # start of the row
          # fall-through - vertical movement
          for r in [row+1,row+2]:
            if r==self.addMoreRow: self.addMore()
            if (r,3+3*languageNo) in self.coords2buttons:
                return focusButton(self.coords2buttons[(r,3+3*languageNo)])
    def scrollIntoView(self,button):
        if hasattr(app,"justGotFocusIn"): return # ignore double <FocusIn> event - allows switch out of app and back in again w/out scrolling back to the keyboard-focused button
        self.scrollingIntoView = button
        self.continueScrollIntoView(button)
    def continueScrollIntoView(self,button):
        # TODO this logic should be separated from this class and used for the multiple-students scrollbar also (along with the FocusIn binding above)
        if not self.scrollingIntoView==button: return # some other button took over
        if not hasattr(self,"ourCanvas"): return # closing down?
        by,bh,cy,ch = button.winfo_rooty(),button.winfo_height(),self.ourCanvas.winfo_rooty(),self.ourCanvas.winfo_height()
        if not by or not bh or not cy or not ch: pass # wait a bit longer
        elif by+bh >= cy+ch-cond(ch>2*bh,bh,0):
            self.ourCanvas.yview("scroll","1","units") # can't specify pixels, so have to keep advancing until we get it
            if by+bh<=cy+ch: return # make this the last one - don't loop consuming CPU on bottom of list
        elif by < cy: self.ourCanvas.yview("scroll","-1","units")
        else: return # done
        app.after(10,lambda *args:self.continueScrollIntoView(button))
    def doStop(self,*args):
        theISM.stopRecording()
        self.updateForStopOrChange()
    def updateForStopOrChange(self):
        if hasattr(self,"currentRecording"):
            filename,row,languageNo = self.currentRecording
            del self.currentRecording
            self.updateFile(filename,row,languageNo,2)
    def reconfigure_scrollbar(self):
        if not hasattr(app,"scanrow"): return # closing down
        if hasattr(self,"ourCanvas"):
          c = self.ourCanvas
          bbox = c.bbox(Tkinter.ALL)
          if hasattr(self,"oldCanvasBbox") and bbox==self.oldCanvasBbox: pass
          else:
              self.oldCanvasBbox = bbox
              c.config(scrollregion=bbox,width=bbox[2],height=min(c["height"],c.winfo_screenheight()/2,bbox[3]))
        if hasattr(self,"currentRecording") and not theISM.currentOutfile: self.doStop() # ensure GUI updates the recording button after player auto-stop (for want of a better place to put it)
        app.after(cond(winCEsound,3000,600),lambda *args:self.reconfigure_scrollbar())
    def setSync(self,syncFlag): self.syncFlag = syncFlag
    def newFolder(self,*args):
        count=0
        while True:
            fname = "folder%d" % count
            try: os.mkdir(unicode2filename(self.currentDir+os.sep+fname))
            except:
                count += 1 ; continue
            break
        self.del_addMore_button()
        row=self.addMoreRow ; col=0
        self.addLabel(row,col,fname)
        self.addMoreRow += 1
        self.add_addMore_button()
        self.startRename(row,col,fname)
    def doRecordFrom(self,filename,row):
        self.doStop()
        theISM.setInputSource(PlayerInput(filename,not self.syncFlag))
        self.current_recordFrom_button = (row, self.coords2buttons[(row,0)])
        self.addButton(row,0,text=localise("Stop"),command=(lambda *args:(self.doStop(),theISM.setInputSource(MicInput()))),colspan=1)
        col = 1
        for inc in [-30, -5, 5, 30]:
            if inc<0: text="<"+str(-inc)
            else: text=str(inc)+">"
            self.addButton(row,col,text=text,command=(lambda e=None,i=inc:self.handleSkip(filename,i)))
            col += 1
    def handleSkip(self,filename,i):
        self.protect_currentRecordFrom()
        self.doStop()
        theISM.setInputSource(PlayerInput(filename,True,theISM.currentInputSource.currentTime()+i))
        if hasattr(app.todo,"undoRecordFrom"):  del app.todo.undoRecordFrom
        self.restore_currentRecordFrom()
    def protect_currentRecordFrom(self): self.old_recordFrom_button, self.current_recordFrom_button = self.current_recordFrom_button, None
    def restore_currentRecordFrom(self): self.current_recordFrom_button, self.old_recordFrom_button = self.old_recordFrom_button, None
    def undoRecordFrom(self):
        if hasattr(self,"current_recordFrom_button") and self.current_recordFrom_button:
            row, button = self.current_recordFrom_button
            for col in range(1+3*len(self.languagesToDraw)):
                if (row,col) in self.coords2buttons:
                    self.coords2buttons[(row,col)].grid_forget()
                    del self.coords2buttons[(row,col)]
            button.grid(row=row,column=0,columnspan=1+3*len(self.languagesToDraw),sticky="w")
            self.coords2buttons[(row,0)] = button
            del self.current_recordFrom_button
    def do_openInExplorer(self,*args):
        openDirectory(self.currentDir,1)
        tkMessageBox.showinfo(app.master.title(),localise("Gradint has opened the current folder for you to work on.  When you press OK, Gradint will re-scan the folder for new files."))
        self.undraw()
        self.draw()
    def pocketPCrecord(self,*args):
        # (apparently get 11.025kHz 16-bit mono.  Can set Notes to NOT switch to notes app when holding Recording button, in which case you then need the task manager to actually get into Notes.)
        if firstLanguage==secondLanguage: tup=("word","meaning","word")
        else: tup=(secondLanguage,firstLanguage,secondLanguage)
        if tkMessageBox.askyesno(app.master.title(),localise("Press and hold the PocketPC's Record button to record; release to stop. Record %s to 1st Note, %s to 2nd, %s to 3rd etc. Import all Notes now?") % tup):
          try:
            if import_recordings(self.currentDir):
                getLsDic(self.currentDir) # to rename them
                self.undraw() ; self.draw()
            else: app.todo.alert="No files found to import. Check this setting: import_recordings_from = "+repr(import_recordings_from)
          except CannotOverwriteExisting: app.todo.alert="Filenames conflict with those already in this folder. Clear the folder first, or choose another, then press the button again (your recordings have been left in the Notes app)."
    def do_recordFromFile(self,*args):
        if not tkSnack or tkSnack=="MicOnly": return tkMessageBox.showinfo(app.master.title(),localise("Sorry, cannot record from file on this computer because the tkSnack library (python-tksnack) is not installed"))
        msg1 = localise("You can record from an existing recording (i.e. copy parts from it) if you first put the existing recording into the samples folder and then press its Play button.")+"\n\n"
        if not self.has_recordFrom_buttons:
            openDirectory(self.currentDir,1)
            tkMessageBox.showinfo(app.master.title(),msg1+localise("Gradint has opened the current folder for you to do this.  When you press OK, Gradint will re-scan the folder for new files."))
            self.undraw()
            self.draw()
            msg1 = ""
        self.setSync(tkMessageBox.askyesno(app.master.title(),localise(msg1+"Do you want your next Play operation to be delayed until you also press a Record button?")))
    def draw(self,dirToHighlight=1): # 1 is used as a "not exist" token
        if secondLanguage==firstLanguage: self.languagesToDraw = [secondLanguage, firstLanguage+"-meaning_"+firstLanguage]
        else: self.languagesToDraw = [secondLanguage,firstLanguage] # each lang cn take 3 columns, starting at column 1 (DO need to regenerate this every draw - languages may have changed!)
        if self.currentDir==samplesDirectory: app.master.title(localise("Recordings manager"))
        else: app.master.title(localise("Recordings manager: ")+filename2unicode((os.sep+self.currentDir)[(os.sep+self.currentDir).rindex(os.sep)+1:]))
        if not self.snack_initialized:
            if tkSnack and not tkSnack=="MicOnly":
                tkSnack.initializeSnack(app)
                if paranoid_file_management and tkSnack.audio.playLatency()<500: tkSnack.audio.playLatency(500) # at least 500ms latency if we're paranoid_file_management, just in case (since tkSnack.audio.elapsedTime does not account for hold-ups)
            self.snack_initialized = True
        if not hasattr(app,"scanrow"):
            app.scanrow = Tkinter.StringVar(app) # (keep StringVars in app not self to avoid d'tor confusion when close box pressed)
            app.scanrow.set("0")
            self.reconfigure_scrollbar()
        if tkSnack: theISM.setInputSource(MicInput())
        self.frame=Tkinter.Frame(app.leftPanel) ; self.frame.pack()

        self.need_reRecord_enabler = 0 # no previously-existing words yet (when we get existing words we 'lock' them and have to unlock by pressing a global 'rerecord' button 1st, just in case)

        if winCEsound and not tkSnack: makeButton(self.frame,text=localise("PocketPC record..."),command=self.pocketPCrecord).grid(row=1,columnspan=2)
        else:
          r = Tkinter.Frame(self.frame)
          r.grid(row=1,sticky="e",columnspan=2)
          Tkinter.Label(r,text=localise("Action of spacebar during recording")).pack()
          r=Tkinter.Frame(r) ; r.pack()
          for button in [
              Tkinter.Radiobutton(r, text=localise("move down"), variable=app.scanrow, value="0", indicatoron=1),
              Tkinter.Radiobutton(r, text=localise("move along"), variable=app.scanrow, value="1", indicatoron=1),
              Tkinter.Radiobutton(r, text=localise("stop"), variable=app.scanrow, value="2", indicatoron=1)]:
              bindUpDown(button,True)
              button.pack({"side":"left"})
        self.grid,self.ourCanvas = setupScrollbar(self.frame,2)
        if hasattr(self,"oldCanvasBbox"): del self.oldCanvasBbox # unconditionally reconfigure scrollbar even if bounds are unchanged
        for languageNo in range(len(self.languagesToDraw)): self.grid.grid_columnconfigure(3+3*languageNo,weight=1) # prefer expanding the last col of each language rather than evenly
        
        curRow = 0 ; prefix2row = {}
        maxPrefix = 0 ; self.has_recordFrom_buttons = False

        if not self.currentDir==samplesDirectory and os.sep in self.currentDir:
            self.addButton(curRow,0,text=localise("(Up)"),command=(lambda e=None,f=self.currentDir[:self.currentDir.rindex(os.sep)]:self.changeDir(f)))
            curRow += 1
        l = os.listdir(self.currentDir)
        def cmpfunc(a,b): # sort alphabetically but ensure L2 comes before L1 for tab order
            if "_" in a and "_" in b and a[:a.rindex("_")]==b[:b.rindex("_")]: # the same apart from language? (TODO this won't work with variants)
                if languageof(a)==secondLanguage: a='1'
                elif languageof(a)==firstLanguage: a='2'
                if languageof(b)==secondLanguage: b='1'
                elif languageof(b)==firstLanguage: b='2'
            if a>b: return 1
            elif b>a: return -1
            else: return 0
        l.sort(cmpfunc)
        self.has_variants = check_has_variants(self.currentDir,l)
        allLangs = list2set([firstLanguage,secondLanguage]+possible_otherLanguages+otherLanguages)
        hadDirectories = False
        for fname in l:
            flwr = fname.lower() ; isMeaning=0
            if firstLanguage==secondLanguage and firstLanguage+"-meaning_"+secondLanguage in fname: isMeaning,languageOverride = True, firstLanguage+"-meaning_"+secondLanguage # hack for re-loading a dir of word+meaning in same language.  TODO hope not combining -meaning_ with variants
            elif self.has_variants and fname.find("_",fname.find("_")+1)>-1 and not fname.find("_explain_")>-1: languageOverride=fname[fname.find("_")+1:fname.find("_",fname.find("_")+1)]
            else: languageOverride=None
            if isDirectory(self.currentDir+os.sep+fname):
                 if not flwr in ["zips","utils","advanced utilities"]: # NOT "prompts", that can be browsed
                    newDir = self.currentDir+os.sep+fname
                    self.addButton(curRow,0,text=filename2unicode(fname),command=(lambda e=None,f=newDir:self.changeDir(f)))
                    # TODO if _disabled have an Enable button ?
                    # if not have a Disable ??
                    # (NB though the above button will have a column span)
                    if self.currentDir+os.sep+fname == dirToHighlight:
                        focusButton(self.coords2buttons[(curRow,0)])
                        dirToHighlight = None # done
                    curRow += 1
                    if fileExists(self.currentDir+os.sep+fname+os.sep+longDescriptionName): description=u8strip(open(self.currentDir+os.sep+fname+os.sep+longDescriptionName).read()).strip(wsp)
                    elif fileExists(self.currentDir+os.sep+fname+os.sep+shortDescriptionName): description=u8strip(open(self.currentDir+os.sep+fname+os.sep+shortDescriptionName).read()).strip(wsp)
                    else: description=None
                    if description:
                        l = Tkinter.Label(self.grid,text="     "+description,wraplength=self.ourCanvas.winfo_screenwidth())
                        l.grid(row=curRow,column=0,columnspan=1+3*len(self.languagesToDraw),sticky="w")
                        curRow += 1
                    if not flwr=="prompts": hadDirectories = True
            elif "_" in fname and (languageOverride in allLangs or languageof(fname) in allLangs): # something_lang where lang is a recognised language (don't just take "any _" because some podcasts etc will have _ in them)
              # TODO what about letting them record _explain_ files etc from the GUI (can be done but have to manually enter the _zh_explain bit), + toggling !poetry etc?
              if languageOverride:
                  prefix=fname[:fname.index("_")]
                  if not isMeaning: prefix += (" ("+(fname+extsep)[fname.find("_",fname.find("_")+1)+1:fname.rfind(extsep)]+")")
              else:
                  prefix=fname[:fname.rindex("_")]
                  languageOverride = languageof(fname)
              wprefix = prefix
              if wprefix.startswith("word"): wprefix=wprefix[4:] # ditch any "word" before the integer
              try: iprefix = int(wprefix)
              except: iprefix = -1
              if iprefix>maxPrefix: maxPrefix=iprefix # max existing numerical prefix
              if (flwr.endswith(dotwav) or flwr.endswith(dotmp3) or flwr.endswith(dottxt)): # even if not languageOverride in self.languagesToDraw e.g. for prompts - helps setting up gradint in a language it doesn't have prompts for (creates blank rows for the prefixes that other languages use). TODO do we want to add 'and languageOverride in self.languagesToDraw' if NOT in prompts?
                if not prefix in prefix2row:
                    self.addLabel(curRow,0,utext=filename2unicode(prefix))
                    foundTxt = {}
                    for lang in self.languagesToDraw:
                        if prefix+"_"+lang+dottxt in l: foundTxt[lang]=(self.currentDir+os.sep+prefix+"_"+lang+dottxt,2+3*self.languagesToDraw.index(lang))
                    prefix2row[prefix] = curRow
                    for lang in self.languagesToDraw:
                        if lang==languageOverride: # do it here to preserve tab order
                            self.updateFile(fname,curRow,self.languagesToDraw.index(lang),state=1)
                            languageOverride=None # so not done again
                        else: self.updateFile(prefix+"_"+lang+dotwav,curRow,self.languagesToDraw.index(lang),state=0,txtExists=(lang in foundTxt))
                        self.gridLabel(lang,curRow)
                    for filename,col in foundTxt.values(): self.addSynthLabel(filename,curRow+1,col)
                    curRow += 2
                if languageOverride in self.languagesToDraw and not flwr.endswith(dottxt):
                    self.updateFile(fname,prefix2row[prefix],self.languagesToDraw.index(languageOverride),state=1)
            elif (flwr.endswith(dotwav) or flwr.endswith(dotmp3)) and tkSnack and not tkSnack=="MicOnly": # no _ in it but we can still play it for splitting
                self.addButton(curRow,0,text=(localise("Record from %s") % (filename2unicode(fname),)),command=(lambda e=None,r=curRow,f=self.currentDir+os.sep+fname:self.doRecordFrom(f,r)))
                self.has_recordFrom_buttons = True
                curRow += 1
        self.addMoreRow = curRow ; self.maxPrefix = maxPrefix+1
        self.add_addMore_button()
        if curRow<3 and not hadDirectories: self.addMore() # anyway
        if not dirToHighlight==None: # didn't find it, so focus the first one
            b = self.coords2buttons.get((0,2),None)
            if not b: b = self.coords2buttons.get((0,0),None)
            if b: b.focus() # don't focusButton in this case - no Mac flashing
        r=Tkinter.Frame(self.frame)
        r.grid(columnspan=2)
        r2 = Tkinter.Frame(r) ; r2.pack(side="left")
        makeButton(r2,text=localise("Advanced"),command=self.do_openInExplorer).pack()
        makeButton(r2,text=localise("Record from file"),command=self.do_recordFromFile).pack()
        r2 = Tkinter.Frame(r) ; r2.pack(side="left")
        if not self.always_enable_synth: makeButton(r2,text=localise("Mix with computer voice"),command=self.enable_synth).pack()
        r = Tkinter.Frame(r2) ; r.pack()
        if got_program("lame"): self.CompressButton = makeButton(r,text=localise("Compress all"),command=(lambda *args:self.all2mp3_or_zip())) # was "Compress all recordings" but it takes too much width
        # TODO else can we see if it's possible to get the encoder on the fly, like in the main screen? (would need some restructuring)
        elif got_program("zip") and (explorerCommand or winCEsound): self.CompressButton = makeButton(r,text=localise("Zip for email"),command=(lambda *args:self.all2mp3_or_zip()))
        if hasattr(self,"CompressButton"): self.CompressButton.pack(side="left")
        makeButton(r,text=localise(cond(recorderMode,"Quit","Back to main menu")),command=self.finished).pack(side="left")
        
        if winCEsound and not tkSnack: msg="Click on filenames at left to rename; click synthesized text to edit it"
        else: msg="Choose a word and start recording. Then press space to advance (see control at top). You can also browse and manage previous recordings. Click on filenames at left to rename (multi-line pastes are allowed); click synthesized text to edit it."
        Tkinter.Label(self.frame,text=msg,wraplength=cond(olpc or winCEsound,self.ourCanvas.winfo_screenwidth(),min(int(self.ourCanvas.winfo_screenwidth()*.7),512))).grid(columnspan=2) # (512-pixel max. so the column isn't too wide to read on wide screens, TODO increase if the font is large)
        # (Don't worry about making the text files editable - editable filenames should be enough + easier to browse the result outside Gradint; can include both languages in the filename if you like - hope the users figure this out as we don't want to make the instructions too complex)

def doRecWords(): # called from GUI thread
    if hasattr(app,"LessonRow"): app.thin_down_for_lesson() # else recorderMode
    app.Label.pack_forget() ; app.CancelRow.pack_forget()
    global theRecorderControls
    try: theRecorderControls
    except: theRecorderControls=RecorderControls()
    theRecorderControls.draw()

# Functions for recording on S60 phones:
def s60_recordWord():
 if secondLanguage==firstLanguage: l1Suffix, l1Display = firstLanguage+"-meaning_"+firstLanguage, "meaning"
 else: l1Suffix, l1Display = firstLanguage, firstLanguage
 while True:
  l2 = s60_recordFile(secondLanguage)
  if not l2: return
  l1 = None
  while not l1:
    if (not maybeCanSynth(firstLanguage)) or getYN("Record "+l1Display+" too? (else computer voice)"): l1 = s60_recordFile(l1Suffix) # (TODO what if maybeCanSynth(secondLanguage) but not first, and we want to combine 2nd-lang synth with 1st-lang recorded? low priority as if recording will prob want to rec L2)
    else:
       l1txt = appuifw.query(u""+firstLanguage+" text:","text")
       if l1txt:
          l1 = "newfile_"+firstLanguage+dottxt
          open(l1,"w").write(l1txt.encode("utf-8"))
    if not l1 and getYN("Discard the "+secondLanguage+" recording?"):
       os.remove(l2) ; break
  if not l1: continue
  ls = list2set(os.listdir(samplesDirectory))
  def inLs(prefix):
    for ext in [dotwav,dotmp3,dottxt]:
      for l in [firstLanguage,secondLanguage]:
        if prefix+"_"+l+ext in ls: return 1
  c = 1
  while inLs("%02d" % c): c += 1
  origPrefix = prefix = u""+("%02d" % c)
  while True:
    prefix = appuifw.query(u"Filename:","text",prefix)
    if not prefix: # pressed cancel ??
      if getYN("Discard this recording?"):
        os.remove(l1) ; os.remove(l2) ; return
      else:
        prefix = origPrefix ; continue
    if not inLs(prefix) or getYN("File exists.  overwrite?"): break
  if samplesDirectory: prefix=samplesDirectory+os.sep+prefix
  os.rename(l1,prefix+l1[l1.index("_"):])
  os.rename(l2,prefix+l2[l2.index("_"):])
  if not getYN("Record another?"): break
def s60_recordFile(language):
 fname = "newfile_"+language+dotwav
 while True:
  S=audio.Sound.open(os.getcwd()+os.sep+fname)
  def forgetS():
    S.close()
    try: os.remove(fname)
    except: pass
  if not getYN("Press OK to record "+language+" word"): return forgetS()
  S.record()
  ret = getYN("Press OK to stop") ; S.stop()
  if not ret:
    forgetS() ; continue
  S.play()
  ret = getYN("Are you happy with this?")
  S.stop() ; S.close()
  if not ret:
    os.remove(fname) ; continue
  return fname

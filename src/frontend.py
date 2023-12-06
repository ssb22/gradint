# This file is part of the source code of Gradint
# (c) Silas S. Brown.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of frontend.py - Tk and other front-ends

def interrupt_instructions():
    if soundCollector or app or appuifw or android: return ""
    elif msvcrt: return "\nPress Space if you have to interrupt the lesson."
    elif riscos_sound: return "\nLesson interruption not yet implemented on RISC OS.  If you stop the program before the end of the lesson, your progress will be lost.  Sorry about that."
    elif winCEsound: return "\nLesson interruption not implemented on\nWinCE without GUI.  Can't stop, sorry!"
    elif macsound: return "\nPress Ctrl-C if you have to interrupt the lesson."
    else: return "\nPress Control-C if you have to interrupt the lesson."

appTitle += time.strftime(" %A") # in case leave 2+ instances on the desktop
def waitOnMessage(msg):
    global warnings_printed
    if type(msg)==type(u""): msg2=msg.encode("utf-8")
    else:
        try: msg2,msg=msg,msg.decode("utf-8")
        except AttributeError: msg2=msg # Python 2.1 has no .decode
    if appuifw:
        t=appuifw.Text() ; t.add(u"".join(warnings_printed)+msg) ; appuifw.app.body = t # in case won't fit in the query()  (and don't use note() because it doesn't wait)
        appuifw.query(msg,'query')
    elif android:
        # android.notify("Gradint","".join(warnings_printed)+msg) # doesn't work?
        android.dialogCreateAlert("Gradint","".join(warnings_printed)+msg)
        android.dialogSetPositiveButtonText("OK")
        android.dialogShow() ; android.dialogGetResponse()
    elif app:
        if not (winsound or winCEsound or mingw32 or cygwin): show_info(msg2+B("\n\nWaiting for you to press OK on the message box... "),True) # in case terminal is in front
        app.todo.alert = "".join(warnings_printed)+msg
        while True:
            try:
              if not hasattr(app.todo,"alert"): break
            except: break # app destroyed
            time.sleep(0.5)
        if not (winsound or winCEsound or mingw32 or cygwin): show_info("OK\n",True)
    else:
        if clearScreen(): msg2 = B("This is "+program_name.replace("(c)","\n(c)")+"\n\n")+msg2 # clear screen is less confusing for beginners, but NB it may not happen if warnings etc
        show_info(msg2+B("\n\n"+cond(winCEsound,"Press OK to continue\n","Press Enter to continue\n")))
        sys.stderr.flush() # hack because some systems don't do it (e.g. some mingw32 builds), and we don't want the user to fail to see why the program is waiting (especially when there's an error)
        try:
            raw_input(cond(winCEsound,"See message under this window.","")) # (WinCE uses boxes for raw_input so may need to repeat the message - but can't because the prompt is size-limited, so need to say look under the window)
            clearScreen() # less confusing for beginners
        except EOFError: show_info("EOF on input - continuing\n")
    warnings_printed = []

def getYN(msg,defaultIfEof="n"):
    if appuifw:
        appuifw.app.body = None
        return appuifw.query(ensure_unicode(msg),'query')
    elif android:
        android.dialogCreateAlert("Gradint",msg)
        android.dialogSetPositiveButtonText("Yes") # TODO do we have to localise this ourselves or can we have a platform default?
        android.dialogSetNegativeButtonText("No")
        android.dialogShow()
        try: return android.dialogGetResponse().result['which'] == 'positive'
        except KeyError: return 0 # or raise SystemExit, no 'which'
    elif app:
        app.todo.question = localise(msg)
        while app and not hasattr(app,"answer_given"): time.sleep(0.5)
        if not app: raise SystemExit
        ans = app.answer_given
        del app.answer_given
        return ans
    else:
        ans=None
        clearScreen() # less confusing for beginners
        while not ans=='y' and not ans=='n':
            try: ans = raw_input("%s\nPress y for yes, or n for no.  Then press Enter.  --> " % (msg,))
            except EOFError:
                ans=defaultIfEof ; print (ans)
        clearScreen() # less confusing for beginners
        if ans=='y': return 1
        return 0

def primitive_synthloop():
    global justSynthesize,warnings_printed
    lang = None
    interactive = appuifw or winCEsound or android or not hasattr(sys.stdin,"isatty") or sys.stdin.isatty()
    if interactive: interactive=cond(winCEsound and warnings_printed,"(see warnings under this window) Say:","Say: ") # (WinCE uses an input box so need to repeat the warnings if any - but can't because prompt is size-limited, so need to say move the window.)
    else: interactive="" # no prompt on the raw_input (we might be doing outputFile="-" as well)
    while True:
        old_js = justSynthesize
        if appuifw:
            if not justSynthesize: justSynthesize=""
            justSynthesize=appuifw.query(u"Say:","text",ensure_unicode(justSynthesize))
            if justSynthesize: justSynthesize=justSynthesize.encode("utf-8")
            else: break
        else:
            if android:
              justSynthesize = android.dialogGetInput("Gradint",interactive).result
              if type(justSynthesize)==type(u""): justSynthesize=justSynthesize.encode("utf-8")
            else:
              try: justSynthesize=raw_input(interactive)
              except EOFError: break
            if (winCEsound or riscos_sound or android) and not justSynthesize: break # because no way to send EOF (and we won't be taking i/p from a file)
            if interactive and not readline:
              interactive="('a' for again) Say: "
              if B(justSynthesize)==B("a"): justSynthesize=old_js
        oldLang = lang
        if justSynthesize: lang = S(just_synthesize(interactive,lang))
        # and see if it transliterates:
        if justSynthesize and lang and not B('#') in B(justSynthesize):
            if B(justSynthesize).startswith(B(lang)+B(" ")):
                t = transliterates_differently(justSynthesize[len(lang+" "):],lang)
                if t: t=lang+" "+t
            else: t = transliterates_differently(justSynthesize,lang)
            if t:
                if appuifw: justSynthesize = t
                else: show_info(B("Spoken as ")+t+B("\n"))
        if warnings_printed: # at end not beginning, because don't want to overwrite the info message if appuifw
            if appuifw:
                t=appuifw.Text()
                t.add(u"".join(warnings_printed))
                appuifw.app.body = t
            elif android: waitOnMessage("") # (makeToast doesn't stay around for very long)
            # else they'll have already been printed
            warnings_printed = []
        if not lang: lang=oldLang

if android:
  if not isDirectory("/mnt/sdcard/svox") and not isDirectory("/system/tts/lang_pico"): waitOnMessage("English voice might not be installed. Check under Home > Menu > Settings > Voice output > text to speech > Pico > English")

def startBrowser(url): # true if success
  if winCEsound: return None # user might be paying per byte! + difficult to switch back if no Alt-Tab program
  try:
      import webbrowser
      g=webbrowser.get()
  except: g=0
  if g and (winCEsound or macsound or (hasattr(g,"background") and g.background) or (hasattr(webbrowser,"BackgroundBrowser") and g.__class__==webbrowser.BackgroundBrowser) or (hasattr(webbrowser,"Konqueror") and g.__class__==webbrowser.Konqueror)):
      return g.open_new(S(url))
  # else don't risk it - it might be text-mode and unsuitable for multitask-with-gradint
  if winsound: return not os.system('start "%ProgramFiles%\\Internet Explorer\\iexplore.exe" '+url) # use os.system not system here (don't know why but system() doesn't always work for IE)
  # (NB DON'T replace % with %%, it doesn't work. just hope nobody set an environment variable to any hex code we're using in mp3web)

def clearScreen():
    global warnings_printed
    if not (winsound or mingw32 or unix): return # can't do it anyway
    if warnings_printed:
        # don't do it this time (had warnings etc)
        warnings_printed = []
        return
    if winsound or mingw32: os.system("cls")
    else: os.system("clear 1>&2") # (1>&2 in case using stdout for something else)
    return True

cancelledFiles = []
def handleInterrupt(): # called only if there was an interrupt while the runner was running (interrupts in setup etc are propagated back to mainmenu/exit instead, because lesson state could be anything)
    needCountItems = 0
    if saveProgress:
        if dbase and not dbase.saved_completely:
            show_info("Calculating partial progress... ") # (normally quite quick but might not be on PDAs etc, + we want this written if not app)
            needCountItems = 1 # used if not app
        elif dbase and not app: show_info("Interrupted on not-first-time; no need to save partial progress\n")
    # DON'T init cancelledFiles to empty - there may have been other missed events.
    while copy_of_runner_events:
        cancelledEvent = copy_of_runner_events[0][0]
        try: runner.cancel(copy_of_runner_events[0][1])
        except: pass # wasn't in the queue - must have slipped out
        del copy_of_runner_events[0]
        # cancelledEvent = runner.queue[0][-1][0] worked in python 2.3, but sched implementation seems to have changed in python 2.5 so we're using copy_of_runner_events instead
        if hasattr(cancelledEvent,"wordToCancel") and cancelledEvent.wordToCancel: cancelledFiles.append(cancelledEvent.wordToCancel)
    if not app and needCountItems and cancelledFiles: show_info("(%d cancelled items)...\n" % len(cancelledFiles))
    global repeatMode ; repeatMode = "interrupted"

tkNumWordsToShow = 10 # the default number of list-box items

def addStatus(widget,status,mouseOnly=0):
    # Be VERY CAREFUL with status line changes.  Don't do it on things that are focused by default (except with mouseOnly=1).  Don't do it when the default status line might be the widest thing (i.e. when list box is not displayed) or window size could jump about too much.  And in any event don't use lines longer than about 53 characters (the approx default width of the listbox when using monospace fonts).
    # (NB addStatus now takes effect only when the list box is displayed anyway, so OK for buttons that might also be displayed without it)
    widget.bind('<Enter>',lambda e=None,status=status:app.set_statusline(status))
    widget.bind('<Leave>',app.restore_statusline)
    if not mouseOnly:
        widget.bind('<FocusIn>',lambda e=None,app=app,status=status:app.set_statusline(status))
        widget.bind('<FocusOut>',app.restore_statusline)
def makeButton(parent,text,command):
    button = Tkinter.Button(parent)
    button["text"] = text
    button["command"] = command
    button.bind('<Return>',command) # so can Tab through them
    button.bind('<ButtonRelease-3>', app.wrongMouseButton)
    bindUpDown(button,True)
    return button
def addButton(parent,text,command,packing=None,status=None):
    button = makeButton(parent,text,command)
    if status: addStatus(button,status)
    if packing=="nopack": pass
    elif type(packing)==type(""): button.pack(side=packing)
    elif packing: button.pack(packing)
    else: button.pack()
    return button
def addLabel(row,label):
    label = Tkinter.Label(row,text=label)
    label.pack({"side":"left"})
    return label
def CXVMenu(e): # callback for right-click
    e.widget.focus()
    m=Tkinter.Menu(None, tearoff=0, takefocus=0)
    if macsound:
        cut,copy,paste = "<<Cut>>","<<Copy>>","<<Paste>>"
    else:
        ctrl="<Control-"
        cut,copy,paste = ctrl+'x>',ctrl+'c>',ctrl+'v>'
    def evgen(e,cmd): e.widget.event_generate(cmd)
    funclist = [("Paste",paste),("Delete",'<Delete>')]
    if not macsound:
        funclist = [("Cut",cut),("Copy",copy)]+funclist # doesn't work reliably on Mac Tk
    for l,cmd in funclist: m.add_command(label=l,command=(lambda e=e,c=cmd,evgen=evgen: e.widget.after(10,evgen,e,c)))
    m.add_command(label="Select All",command=(lambda e=e: e.widget.after(10,selectAll,e)))
    m.tk_popup(e.x_root-3, e.y_root+3,entry="0")
def selectAll(e):
    e.widget.event_generate('<Home>')
    e.widget.event_generate('<Shift-End>')
def selectAllButNumber(e): # hack for recording.py - select all but any number at the start
    e.widget.event_generate('<Home>')
    for i in list(e.widget.theText.get()):
        if "0"<=i<="9" or i=="_": e.widget.event_generate('<Right>')
        else: return e.widget.event_generate('<Shift-End>')
def addTextBox(row,wide=0):
    text = Tkinter.StringVar(row)
    entry = Tkinter.Entry(row,textvariable=text)
    entry.bind('<ButtonRelease-3>',CXVMenu)
    if macsound:
        entry.bind('<Control-ButtonRelease-1>',CXVMenu)
        entry.bind('<ButtonRelease-2>',CXVMenu)
    if winCEsound:
      if WMstandard: # non-numeric inputs no good on WMstandard Tkinter
        def doRawInput(text,entry):
            app.input_to_set = text
            app.menu_response="input"
        entry.bind('<Return>',lambda e,doRawInput=doRawInput,text=text,entry=entry:doRawInput(text,entry))
        if wide: # put help in 1st wide textbox
          global had_doRawInput
          try: had_doRawInput
          except:
            had_doRawInput=1
            text.set("(Push OK to type A-Z)") # (if changing this message, change it below too)
            class E: pass
            e=E() ; e.widget = entry
            entry.after(10,lambda _=None,e=e:selectAll(e))
      else: # PocketPC: try to detect long clicks. This is awkward. time.time is probably 1sec resolution so will get false +ves if go by that only.
        def timeStamp(entry): entry.buttonPressTime=time.time()
        entry.bind('<ButtonPress-1>',lambda e,timeStamp=timeStamp,entry=entry:timeStamp(entry))
        global lastDblclkAdvisory,lastDblclk
        lastDblclkAdvisory=lastDblclk=0
        def pasteInstructions(t):
            if t>=0.5: # they probably want tap-and-hold, which we don't do properly
                global lastDblclkAdvisory
                if t<2 and (lastDblclkAdvisory>time.time()-30 or lastDblclk>time.time()-90): return # reduce repeated false +ves
                lastDblclkAdvisory=time.time()
                app.todo.alert="Double-click in the box if you want to replace it with the clipboard contents"
        def doPaste(text,entry):
            text.set(entry.selection_get(selection="CLIPBOARD"))
            global lastDblclk ; lastDblclk=time.time()
        entry.bind('<ButtonRelease-1>',lambda e,entry=entry,pasteInstructions=pasteInstructions:pasteInstructions(time.time()-getattr(entry,"buttonPressTime",time.time())))
        entry.bind('<Double-Button-1>',lambda e,doPaste=doPaste,text=text,entry=entry:doPaste(text,entry))
    # Tkinter bug workaround (some versions): event_generate from within a key event handler can be unreliable, so the Ctrl-A handler delays selectAll by 10ms:
    entry.bind(cond(macsound,'<Command-a>','<Control-a>'),(lambda e:e.widget.after(10,lambda e=e:selectAll(e))))
    bindUpDown(entry,False)
    if wide=="nopack": pass
    elif wide:
        if winCEsound or olpc: entry["width"]=1 # so it will squash down rather than push off-screen any controls to the right (but DON'T do this on other platforms, where we want the window to expand in that case, e.g. when there are cache controls)
        entry.pack(side="left",fill=Tkinter.X,expand=1)
    else: entry.pack({"side":"left"})
    return text,entry
def bindUpDown(o,alsoLeftRight=False): # bind the up and down arrows to do shift-tab and tab (may be easier for some users, especially on devices where tab is awkward)
    tab=(lambda e:e.widget.after(10,lambda e=e:e.widget.event_generate('<Tab>')))
    shTab=(lambda e:e.widget.after(10,lambda e=e:e.widget.event_generate('<Shift-Tab>')))
    o.bind('<Up>',shTab)
    o.bind('<Down>',tab)
    if alsoLeftRight:
        o.bind('<Left>',shTab)
        o.bind('<Right>',tab)
def addLabelledBox(row,wide=0,status=None):
    label = addLabel(row,"") # will set contents later
    text,entry = addTextBox(row,wide)
    if status: addStatus(entry,status)
    return label,text,entry
def addRow(parent,wide=0):
    row = Tkinter.Frame(parent)
    if wide: row.pack(fill=Tkinter.X,expand=1)
    else: row.pack()
    return row
def addRightRow(widerow): # call only after adding any left-hand buttons.  better tab order than filling buttons from the right.
    rrow = Tkinter.Frame(widerow)
    rrow.pack(side="right") ; return rrow

def make_output_row(parent):
    # make a row of buttons for choosing where the output goes to
    # if there aren't any options then return None
    # we also put script-variant selection here, if any
    row = None
    def getRow(row,parent):
      if not row:
        row = Tkinter.Frame(parent)
        row.pack(fill=Tkinter.X,expand=1)
      return row
    GUIlang = GUI_languages.get(firstLanguage,firstLanguage)
    if checkIn("@variants-"+GUIlang,GUI_translations): # the firstLanguage has script variants
        row=getRow(row,parent)
        if not hasattr(app,"scriptVariant"): app.scriptVariant = Tkinter.StringVar(app)
        count = 0
        for variant in GUI_translations["@variants-"+GUIlang]:
            Tkinter.Radiobutton(row, text=u" "+variant+u" ", variable=app.scriptVariant, value=str(count), indicatoron=forceRadio).pack({"side":"left"})
            count += 1
        app.scriptVariant.set(str(scriptVariants.get(GUIlang,0)))
    if synth_partials_voices and guiVoiceOptions:
        row=getRow(row,parent)
        if not hasattr(app,"voiceOption"): app.voiceOption = Tkinter.StringVar(app)
        Tkinter.Radiobutton(row, text=u" Normal ", variable=app.voiceOption, value="", indicatoron=forceRadio).pack({"side":"left"})
        for o in guiVoiceOptions: Tkinter.Radiobutton(row, text=u" "+o[1].upper()+o[2:]+u" ", variable=app.voiceOption, value=o, indicatoron=forceRadio).pack({"side":"left"})
        app.voiceOption.set(voiceOption)
    if not gotSox: return row # can't do any file output without sox
    if not hasattr(app,"outputTo"):
        app.outputTo = Tkinter.StringVar(app) # NB app not parent (as parent is no longer app)
        app.outputTo.set("0") # not "" or get tri-state boxes on OS X 10.6
    row=getRow(row,parent)
    rightrow = addRightRow(row) # to show beginners this row probably isn't the most important thing despite being in a convenient place, we'll right-align
    def addFiletypeButton(fileType,rightrow):
        ftu = fileType.upper()
        t = Tkinter.Radiobutton(rightrow, text=cond(forceRadio,""," ")+ftu+" ", variable=app.outputTo, value=fileType, indicatoron=forceRadio)
        bindUpDown(t,True)
        addStatus(t,"Select this to save a lesson or\na phrase to a%s %s file" % (cond(ftu[0] in "AEFHILMNORSX","n",""),ftu))
        t.pack({"side":"left"})
    if winsound or mingw32: got_windows_encoder = fileExists(programFiles+"\\Windows Media Components\\Encoder\\WMCmd.vbs")
    elif cygwin: got_windows_encoder = fileExists(programFiles+"/Windows Media Components/Encoder/WMCmd.vbs")
    else: got_windows_encoder = 0
    Tkinter.Label(rightrow,text=localise("To")+":").pack({"side":"left"})
    t=Tkinter.Radiobutton(rightrow, text=cond(forceRadio,""," ")+localise("Speaker")+" ", variable=app.outputTo, value="0", indicatoron=forceRadio) # (must be value="0" not value="" for OS X 10.6 otherwise the other buttons become tri-state)
    addStatus(t,"Select this to send all sounds to\nthe speaker, not to files on disk")
    bindUpDown(t,True)
    t.pack({"side":"left"})
    if got_program("lame"): addFiletypeButton("mp3",rightrow)
    if got_windows_encoder: addFiletypeButton("wma",rightrow)
    if got_program("neroAacEnc") or got_program("faac") or got_program("afconvert"): addFiletypeButton("aac",rightrow)
    if got_program("oggenc") or got_program("oggenc2"): addFiletypeButton("ogg",rightrow)
    if got_program("toolame"): addFiletypeButton("mp2",rightrow)
    if got_program("speexenc"): addFiletypeButton("spx",rightrow)
    addFiletypeButton("wav",rightrow)
    # "Get MP3 encoder" and "Get WMA encoder" changed to "MP3..." and "WMA..." to save width (+ no localisation necessary)
    if unix and not got_program("lame") and got_program("make") and got_program("gcc") and (got_program("curl") or got_program("wget")): addButton(rightrow,"MP3...",app.getEncoder,status="Press this to compile an MP3 encoder\nso Gradint can output to MP3 files") # (checking gcc as well as make because some distros strangely have make but no compiler; TODO what if has a non-gcc compiler)
    # (no longer available) elif (winsound or mingw32) and not got_windows_encoder and not got_program("lame"): addButton(rightrow,"WMA...",app.getEncoder,status="Press this to download a WMA encoder\nso Gradint can output to WMA files")
    return row

def updateSettingsFile(fname,newVals):
    # leaves comments etc intact, but TODO does not cope with changing variables that have been split over multiple lines
    replacement_lines = []
    try: oldLines=u8strip(read(fname)).replace(B("\r\n"),B("\n")).split(B("\n"))
    except IOError: oldLines=[]
    for l in oldLines:
        found=0
        for k in list(newVals.keys()):
            if l.startswith(B(k)):
                replacement_lines.append(B(k+"="+repr(newVals[k])))
                del newVals[k]
                found=1
        if not found: replacement_lines.append(l)
    for k,v in list(newVals.items()): replacement_lines.append(B(k+"="+repr(v)))
    if replacement_lines and replacement_lines[-1]: replacement_lines.append(B("")) # ensure blank line at end so there's a \n but we don't add 1 more with each save
    writeB(open(fname,"w"),B("\n").join(replacement_lines))

def asUnicode(x): # for handling the return value of Tkinter entry.get()
    try: return u""+x # original behaviour
    except: # some localised versions of Windows e.g. German will return Latin1 instead of Unicode, so try interpreting it as utf-8 and Latin-1
        try: return x.decode("utf-8")
        except: return x.decode("iso-8859-1") # TODO can we get what it actually IS? (on German WinXP, sys.getdefaultencoding==ascii and locale==C but Tkinter still returns Latin1)

def setupScrollbar(parent,rowNo):
    onLeft = winCEsound or olpc
    s = Tkinter.Scrollbar(parent,takefocus=0)
    s.grid(row=rowNo,column=cond(onLeft,0,1),sticky="ns"+cond(onLeft,"w","e"))
    try: parent.rowconfigure(rowNo,weight=1)
    except: pass
    c=Tkinter.Canvas(parent,bd=0,width=200,height=100,yscrollcommand=s.set)
    c.grid(row=rowNo,column=cond(onLeft,1,0),sticky="nsw")
    s.config(command=c.yview)
    scrolledFrame=Tkinter.Frame(c) ; c.create_window(0,0,window=scrolledFrame,anchor="nw")
    # Mousewheel binding.  TODO the following bind_all assumes only one scrolledFrame on screen at once (redirect all mousewheel events to the frame; necessary as otherwise they'll go to buttons etc)
    app.ScrollUpHandler = lambda e=None,c=c:c.yview("scroll","-1","units")
    app.ScrollDownHandler = lambda e=None,c=c:c.yview("scroll","1","units")
    if macsound:
        def ScrollHandler(event):
            if event.delta>0: app.ScrollUpHandler()
            else: app.ScrollDownHandler()
        scrolledFrame.bind_all('<MouseWheel>',ScrollHandler)
        # DON'T bind <MouseWheel> on Windows - our version of Tk will segfault when it occurs. See http://mail.python.org/pipermail/python-bugs-list/2005-May/028768.html but we can't patch our library.zip's Tkinter anymore (TODO can we use newer Tk DLLs and ensure setup.bat updates them?)
    else: # for X11:
        scrolledFrame.bind_all('<Button-4>',app.ScrollUpHandler)
        scrolledFrame.bind_all('<Button-5>',app.ScrollDownHandler)
    return scrolledFrame, c

# GUI presets buttons:
shortDescriptionName = "short-description"+dottxt
longDescriptionName = "long-description"+dottxt
class ExtraButton(object):
    def __init__(self,directory):
        self.shortDescription = wspstrip(u8strip(read(directory+os.sep+shortDescriptionName)))
        if fileExists(directory+os.sep+longDescriptionName): self.longDescription = wspstrip(u8strip(read(directory+os.sep+longDescriptionName)))
        else: self.longDescription = self.shortDescription
        self.directory = directory
    def add(self):
        app.extra_button_callables.append(self) # so we're not lost when deleted from the waiting list
        self.button = addButton(app.rightPanel,localise("Add ")+unicode(self.shortDescription,"utf-8"),self,{"fill":"x"})
        self.button["anchor"]="w"
    def __call__(self,*args):
        if not tkMessageBox.askyesno(app.master.title(),unicode(self.longDescription,"utf-8")+"\n"+localise("Add this to your collection?")): return
        newName = self.directory
        if os.sep in newName: newName=newName[newName.rfind(os.sep)+1:]
        if newName.endswith(exclude_from_scan): newName=newName[:-len(exclude_from_scan)]
        if not newName: newName="1"
        ls = []
        try: ls = os.listdir(samplesDirectory)
        except: os.mkdir(samplesDirectory)
        name1=newName
        while checkIn(newName,ls): newName+="1"
        name2=newName
        newName = samplesDirectory+os.sep+newName
        os.rename(self.directory,newName)
        which_collection = localise(" has been added to your recorded words collection.")
        if fileExists(newName+os.sep+"add-to-vocab"+dottxt):
            which_collection = localise(" has been added to your collection.")
            o=open(vocabFile,"a")
            o.write("# --- BEGIN "+self.shortDescription+" ---\n")
            o.write(wspstrip(u8strip(read(newName+os.sep+"add-to-vocab"+dottxt)))+"\n")
            o.write("# ----- END "+self.shortDescription+" ---\n")
            if hasattr(app,"vocabList"): del app.vocabList # so re-reads
            os.remove(newName+os.sep+"add-to-vocab"+dottxt)
        if fileExists(newName+os.sep+"add-to-languages"+dottxt):
            changed = 0
            for lang in wspstrip(u8strip(read(newName+os.sep+"add-to-languages"+dottxt))).split():
                if not lang in [firstLanguage,secondLanguage]+otherLanguages:
                    otherLanguages.append(lang) ; changed = 1
            if changed: sanitise_otherLanguages(), updateSettingsFile("advanced"+dottxt,{"otherLanguages":otherLanguages,"possible_otherLanguages":possible_otherLanguages})
            os.remove(newName+os.sep+"add-to-languages"+dottxt)
        promptsAdd = newName+os.sep+"add-to-prompts"
        if isDirectory(promptsAdd):
            for f in os.listdir(promptsAdd):
                if fileExists_stat(promptsDirectory+os.sep+f): os.remove(promptsAdd+os.sep+f)
                else: os.rename(promptsAdd+os.sep+f, promptsDirectory+os.sep+f)
            os.rmdir(promptsAdd)
        if not name1==name2: which_collection += "\n(NB you already had a "+name1+" so the new one was called "+name2+" - you might want to sort this out.)"
        self.button.pack_forget()
        app.extra_button_callables.remove(self)
        if extra_buttons_waiting_list: app.add_extra_button()
        app.wordsExist = 1
        if tkMessageBox.askyesno(app.master.title(),unicode(self.shortDescription,"utf-8")+which_collection+"\n"+localise("Do you want to start learning immediately?")): app.makelesson()

extra_buttons_waiting_list = []
def make_extra_buttons_waiting_list():
    if os.sep in samplesDirectory:
        oneUp=samplesDirectory[:samplesDirectory.rfind(os.sep)]
        if not oneUp: oneUp=os.sep
    else: oneUp=os.getcwd()
    for d in [samplesDirectory,oneUp]:
        try: ls = os.listdir(d)
        except: continue
        ls.sort()
        for l in ls:
            if l.endswith(exclude_from_scan) and fileExists(d+os.sep+l+os.sep+shortDescriptionName): extra_buttons_waiting_list.append(ExtraButton(d+os.sep+l))

def focusButton(button):
    button.focus()
    if macsound: # focus() should display the fact on Windows and Linux, but doesn't on OS X so:
        def flashButton(button,state):
            try: button.config(state=state)
            except: pass # maybe not a button
        for t in range(250,1000,250): # (NB avoid epilepsy's 5-30Hz!)
          app.after(t,lambda e=None,flashButton=flashButton,button=button:flashButton(button,"active"))
          app.after(t+150,lambda e=None,flashButton=flashButton,button=button:flashButton(button,"normal"))
        # (Don't like flashing, but can't make it permanently active as it won't change when the focus does)

if WMstandard: GUI_omit_statusline = 1 # unlikely to be room (and can disrupt nav)

def startTk():
    class Application(Tkinter.Frame):
        def __init__(self, master=None):
            Tkinter.Frame.__init__(self, master)
            class EmptyClass: pass
            self.todo = EmptyClass() ; self.toRestore = []
            self.ScrollUpHandler = self.ScrollDownHandler = lambda e=None:True
            global app ; app = self
            make_extra_buttons_waiting_list()
            if olpc: self.master.option_add('*font',cond(extra_buttons_waiting_list,'Helvetica 9','Helvetica 14'))
            elif macsound:
                if Tkinter.TkVersion>=8.6: self.master.option_add('*font','System 13') # ok with magnification.  Note >13 causes square buttons.  (Including this line causes "Big print" to work)
                if "AppTranslocation" in os.getcwd(): self.todo.alert="Your Mac is using \"app translocation\" to stop Gradint from writing to its folder. This will cause many problems. Quit Gradint, drag it to a different folder and run it again."
            elif WMstandard: self.master.option_add('*font','Helvetica 7') # TODO on ALL WMstandard devices?
            if winsound or cygwin or macsound: self.master.resizable(1,0) # resizable in X direction but not Y (latter doesn't make sense, see below).  (Don't do this on X11 because on some distros it results in loss of automatic expansion as we pack more widgets.)
            elif unix:
                if getoutput("xlsatoms|grep COMPIZ_WINDOW").find("COMPIZ")>=0: # (not _COMPIZ_WM_WINDOW_BLUR, that's sometimes present outside Compiz)
                  # Compiz sometimes has trouble auto-resizing our window (e.g. on Ubuntu 11.10)
                  self.master.geometry("%dx%d" % (self.winfo_screenwidth(),self.winfo_screenheight()))
                  if not GUI_always_big_print: self.todo.alert = "Gradint had to maximize itself because your window manager is Compiz which sometimes has trouble handling Tkinter window sizes"
            self.extra_button_callables = []
            self.pack(fill=Tkinter.BOTH,expand=1)
            self.leftPanel = Tkinter.Frame(self)
            self.leftPanel.pack(side="left",fill=Tkinter.BOTH,expand=1)
            self.rightPanel = None # for now
            self.cancelling = 0 # guard against multiple presses of Cancel
            self.Label = Tkinter.Label(self.leftPanel,text="Please wait a moment")
            self.Label.pack()
            self.Label["wraplength"]=self.Label.winfo_screenwidth() # don't go off-screen in teacherMode
            # See if we can figure out what Tk is doing with the fonts (on systems without magnification):
            try:
                f=str(self.Label.cget("font")).split()
                nominalSize = intor0(f[-1])
                if nominalSize: f=" ".join(f[:-1])+" %d"
                else: # Tk 8.5+ ?
                    for f2 in ['set font [font actual '+' '.join(f)+']', # Tk 8.5
                               'set font [font actual default]']: # Tk 8.6
                      f=str(self.tk.eval(f2)).split()
                      upNext = 0
                      for i in range(len(f)):
                        if f[i]=="-size": upNext=1
                        elif upNext:
                            nominalSize=intor0(f[i])
                            if nominalSize<0: nominalSize,f[i] = -nominalSize,"-%d"
                            else: f[i]="%d"
                            break
                      if nominalSize==long(32768)*long(65536): nominalSize = 0 # e.g. Tk 8.6 on Ubuntu 16.04 when using the first eval string above
                      elif f2=='set font [font actual default]': nominalSize *= 0.77 # kludge for Tk 8.6 on Ubuntu 16.04 to make large-print calculation below work
                      if nominalSize: break
                    f=" ".join(f)
                    if (not checkIn("%d",f)) or not nominalSize: raise Exception("wrong format") # caught below
                pixelSize = self.Label.winfo_reqheight()-2*int(str(self.Label["borderwidth"]))-2*int(str(self.Label["pady"]))
                # NB DO NOT try to tell Tk a desired pixel size - you may get a *larger* pixel size.  Need to work out the desired nominal size.
                approx_lines_per_screen_when_large = 25 # TODO really? (24 at 800x600 192dpi 15in but misses the status line, but OK for advanced users.  setting 25 gives nominal 7 which is rather smaller.)
                largeNominalSize = int(nominalSize*self.Label.winfo_screenheight()/approx_lines_per_screen_when_large/pixelSize)
                if largeNominalSize >= nominalSize+3:
                    self.bigPrintFont = f % largeNominalSize
                    self.bigPrintMult = largeNominalSize*1.0/nominalSize
                    if GUI_always_big_print:
                        self.bigPrint0()
                else: self.after(100,self.check_window_position) # (needs to happen when window is already drawn if you want it to preserve the X co-ordinate)
            except: pass # wrong font format or something - can't do it
            if winCEsound and ask_teacherMode: self.Label["font"]="Helvetica 16" # might make it slightly easier
            self.remake_cancel_button(localise("Cancel lesson"))
            self.Cancel.focus() # (default focus if we don't add anything else, e.g. reader)
            self.copyright_string = u"This is "+ensure_unicode(program_name).replace("(c)",u"\n\u00a9").replace("-",u"\u2013")
            self.Version = Tkinter.Label(self.leftPanel,text=self.copyright_string)
            addStatus(self.Version,self.copyright_string)
            if olpc: self.Version["font"]='Helvetica 9'
            self.pollInterval = cond(winCEsound,300,100) # ms
            self.startTime=time.time()
            self.after(self.pollInterval,self.poll)
            # and hide the console on Mac OS:
            try: self.tk.call('console','hide')
            except: pass
            self.change_button_shown = 0
            self.bind("<Leave>",self.restore_copyright)
            self.bind("<FocusOut>",self.restore_copyright)
            global recorderMode
            if recorderMode:
                if tkSnack: doRecWords()
                else:
                    show_warning("Cannot do recorderMode because tkSnack library (python-tksnack) not installed")
                    recorderMode = 0
        def remake_cancel_button(self,text=""): # sometimes need to re-make it to preserve tab order
            self.CancelRow = addRow(self.leftPanel)
            self.Cancel = addButton(self.CancelRow,text,self.cancel,{"side":"left"})
            self.CancelRow.pack()
        def set_statusline(self,text): # ONLY from callbacks
            if GUI_omit_statusline or not hasattr(self,"ListBox"): return # status changes on main screen can cause too much jumping
            if not "\n" in text: text += "\n(TODO: Make that a 2-line message)" # being 2 lines helps to reduce flashing problems.  but don't want to leave 2nd line blank.
            self.Version["text"] = text
            if not winCEsound: self.balance_statusline,self.pollInterval = self.pollInterval,10
        def restore_statusline(self,*args): # ONLY from callbacks
            if not hasattr(self,"ListBox"): return
            # self.Version["text"] = self.copyright_string
            self.Version["text"] = "\n"
        def restore_copyright(self,*args): self.Version["text"] = self.copyright_string
        def addOrTestScreen_poll(self):
            if hasattr(self,"balance_statusline"): # try to prevent flashing on some systems/languages due to long statusline causing window resize which then takes the mouse out of the button that set the long statusline etc
                if self.Version.winfo_reqwidth() > self.ListBox.winfo_reqwidth(): self.ListBox["width"] = int(self.ListBox["width"])+1
                else:
                    self.pollInterval = self.balance_statusline
                    del self.balance_statusline
            self.sync_listbox_etc()
            if self.ListBox.curselection():
                if not self.change_button_shown:
                    self.ChangeButton.pack()
                    self.change_button_shown = 1
                    self.Cancel["text"] = localise("Cancel selection")
            else:
                if self.change_button_shown:
                    self.ChangeButton.pack_forget()
                    self.change_button_shown = 0
                    self.lastText1 = 1 # force update
            if self.toRestore:
                if not hasattr(self,"restoreButton"): self.restoreButton = addButton(self.TestEtcCol,localise("Restore"),self.restoreText,status="This button will undo\nGradint's transliteration of the input")
            elif hasattr(self,"restoreButton"):
                self.restoreButton.pack_forget() ; del self.restoreButton
            try:
                if hasattr(self,"set_watch_cursor"):
                    self.config(cursor="watch") ; self.TestTextButton.config(cursor="watch")
                    del self.set_watch_cursor
                if hasattr(self,"unset_watch_cursor"):
                    self.config(cursor="") ; self.TestTextButton.config(cursor="")
                    del self.unset_watch_cursor
            except: pass # (if the Tk for some reason doesn't support them then that's OK)
        def poll(self):
          try:
            global voiceOption
            if hasattr(self,"ListBox"): self.addOrTestScreen_poll()
            if hasattr(self,"scriptVariant"):
              v = self.scriptVariant.get()
              if v: v=int(v)
              else: v=0
              if not v==scriptVariants.get(firstLanguage,0): self.setVariant(v)
            if hasattr(self,"voiceOption") and not self.voiceOption.get()==voiceOption:
              voiceOption=self.voiceOption.get() ; updateSettingsFile(settingsFile,{"voiceOption":voiceOption})
            if hasattr(self,"outputTo"):
             outTo = self.outputTo.get()
             if hasattr(self,"lastOutTo") and self.lastOutTo==outTo: pass
             else:
              self.lastOutTo = outTo
              if outTo=="0": outTo=""
              if hasattr(self,"TestTextButton"):
                if outTo: self.TestTextButton["text"]=localise("To")+" "+outTo.upper()
                else: self.TestTextButton["text"]=localise("Speak")
                # used to be called "Test" instead of "Speak", but some people didn't understand that THEY'RE doing the testing (not the computer)
              if hasattr(self,"MakeLessonButton"):
                if outTo: self.MakeLessonButton["text"]=localise("Make")+" "+outTo.upper()
                else: self.MakeLessonButton["text"]=localise("Start lesson") # less confusing for beginners than "Make lesson", if someone else has set up the words
            if hasattr(self,"BriefIntButton"):
                if emergency_lessonHold_to < time.time(): t=localise("Brief interrupt")
                else: t=localise("Resume")+" ("+str(int(emergency_lessonHold_to-time.time()))+")"
                if not self.BriefIntButton["text"]==t:
                    self.BriefIntButton["text"]=t
                    if t==localise("Brief interrupt"): self.Label["text"]=localise("Resuming...")
            if not self.todo.__dict__: return # can skip the rest
            if hasattr(self.todo,"not_first_time"):
                self.Cancel["text"] = "Stop lesson"
                del self.todo.not_first_time
            if hasattr(self.todo,"set_main_menu") and not recorderMode:
                # set up the main menu (better do it on this thread just in case)
                self.cancelling = 0 # in case just pressed "stop lesson" on a repeat - make sure Quit button will now work
                self.Label.pack_forget()
                self.CancelRow.pack_forget()
                if self.todo.set_main_menu=="keep-outrow":
                    if hasattr(self,"OutputRow"): self.OutputRow.pack(fill=Tkinter.X,expand=1) # just done pack_forget in thindown
                else:
                    if hasattr(self,"OutputRow"): self.OutputRow.pack_forget()
                    outRow = make_output_row(self.leftPanel)
                    if outRow: self.OutputRow=outRow
                self.TestButton = addButton(self.leftPanel,localise(cond(self.wordsExist,"Manage word list","Create word list")),self.showtest) # used to be called "Add or test words", but "Manage word list" may be better for beginners.  And it seems that "Create word list" is even better for absolute beginners, although it shouldn't matter if self.wordsExist is not always set back to 0 when it should be.
                self.make_lesson_row()
                if userNameFile:
                    global GUI_usersRow
                    # if GUI_usersRow: GUI_usersRow.pack() else:  -- don't do this (need to re-create every time for correct tab order)
                    GUI_usersRow=addRow(self.leftPanel)
                    updateUserRow(1)
                if hasattr(self,"bigPrintFont"):
                    self.BigPrintButton = addButton(self.leftPanel,localise("Big print"),self.bigPrint)
                    try: self.BigPrintButton["font"]=self.bigPrintFont
                    except:
                        self.BigPrintButton.pack_forget() ; del self.BigPrintButton, self.bigPrintFont
                self.remake_cancel_button(localise("Quit"))
                if not GUI_omit_statusline: self.Version.pack(fill=Tkinter.X,expand=1)
                if olpc or self.todo.set_main_menu=="test" or GUI_for_editing_only: self.showtest() # olpc: otherwise will just get a couple of options at the top and a lot of blank space (no way to centre it)
                else: focusButton(self.TestButton)
                del self.todo.set_main_menu
                self.restore_copyright()
            if hasattr(self.todo,"alert"):
                # we have to do it on THIS thread (especially on Windows / Cygwin; Mac OS and Linux might get away with doing it from another thread)
                tkMessageBox.showinfo(self.master.title(),S(self.todo.alert))
                del self.todo.alert
            if hasattr(self.todo,"question"):
                self.answer_given = tkMessageBox.askyesno(self.master.title(),self.todo.question)
                del self.todo.question
            if hasattr(self.todo,"set_label"):
                self.Label["text"] = self.todo.set_label
                del self.todo.set_label
            if hasattr(self.todo,"thindown"):
                self.thin_down_for_lesson()
                self.setLabel(self.todo.thindown)
                del self.todo.thindown
            if hasattr(self.todo,"add_briefinterrupt_button") and runner:
                self.BriefIntButton = addButton(self.CancelRow,localise("Brief interrupt"),self.briefInterrupt,{"side":"left"}) # on RHS of Cancel = reminescient of the stop and pause controls on a tape recorder
                focusButton(self.BriefIntButton)
                del self.todo.add_briefinterrupt_button
            if hasattr(self.todo,"remove_briefinterrupt_button"):
                if hasattr(self,"BriefIntButton"):
                    self.BriefIntButton.pack_forget() ; del self.BriefIntButton
                elif hasattr(self.todo,"add_briefinterrupt_button"): del self.todo.add_briefinterrupt_button # cancel pressed while still making lesson
                del self.todo.remove_briefinterrupt_button
            if hasattr(self.todo,"clear_text_boxes"):
                self.Text1.set("") ; self.Text2.set("") ; self.Entry1.focus()
                del self.todo.clear_text_boxes
            if hasattr(self.todo,"undoRecordFrom"):
                theRecorderControls.undoRecordFrom()
                del self.todo.undoRecordFrom
            if hasattr(self.todo,"input_response"): # WMstandard
                self.input_to_set.set(self.todo.input_response)
                del self.todo.input_response,self.input_to_set
            if hasattr(self.todo,"exit_ASAP"):
                self.master.destroy()
                self.pollInterval = 0
          finally: # (try to make sure GUI exceptions at least don't stop the poll loop)
            if self.pollInterval: self.after(self.pollInterval,self.poll)
        def briefInterrupt(self,*args):
            global emergency_lessonHold_to
            if emergency_lessonHold_to:
                emergency_lessonHold_to = 0
                self.setLabel("")
            elif finishTime-lessonLen + 20 >= time.time(): # (TODO customise the 20?)
                global askAgain_explain
                askAgain_explain = "A brief interrupt when you've only just started is never a good idea.  "
                self.cancel()
            else:
                emergency_lessonHold_to = time.time() + briefInterruptLength
                self.setLabel(localise("Emergency brief interrupt"))
        def make_lesson_row(self): # creates but doesn't pack.  May need to re-make to preserve tab order.  (Assumes any existing one is pack_forget)
            words,mins = str(maxNewWords),cond(int(maxLenOfLesson/60)==maxLenOfLesson/60.0,str(int(maxLenOfLesson/60)),str(maxLenOfLesson/60.0))
            if hasattr(self,"NumWords"): words=self.NumWords.get()
            if hasattr(self,"Minutes"): mins=self.Minutes.get()
            self.LessonRow = addRow(self.leftPanel)
            if GUI_for_editing_only: return
            self.NumWords,entry = addTextBox(self.LessonRow)
            entry["width"]=2
            addStatus(entry,"Limits the maximum number of NEW words\nthat are put in each lesson")
            self.NumWords.set(words)
            addLabel(self.LessonRow,localise(cond(fileExists(progressFile),"new ","")+"words in"))
            self.Minutes,self.MinsEntry = addTextBox(self.LessonRow)
            addStatus(self.MinsEntry,"Limits the maximum time\nthat a lesson is allowed to take")
            self.MinsEntry["width"]=3
            self.Minutes.set(mins)
            addLabel(self.LessonRow,localise("mins"))
            self.MakeLessonButton=addButton(self.LessonRow,localise("Start lesson"),self.makelesson,{"side":"left"},status="Press to create customized lessons\nusing the words in your collection")
            self.lastOutTo=-1 # so it updates the Start Lesson button if needed
            self.MakeLessonButton.bind('<FocusIn>',(lambda e=None,app=app:app.after(10,lambda e=None,app=app:app.MinsEntry.selection_clear())))
        def sync_listbox_etc(self):
            if not hasattr(self,"vocabList"):
                if hasattr(self,"needVocablist"): return # already waiting for main thread to make one
                while self.ListBox.get(0): self.ListBox.delete(0) # clear completely (otherwise the following would just do a least-disruptive update)
                self.ListBox.insert(0,"Updating list from "+vocabFile+"...")
                self.needVocablist=1
                return
            elif hasattr(self,"needVocablist"):
                del self.needVocablist
                self.ListBox.delete(0) # the Loading...
                self.lastText1=1 # so continues below
            text1,text2 = asUnicode(self.Text1.get()),asUnicode(self.Text2.get())
            if text1==self.lastText1 and text2==self.lastText2: return
            self.lastText1,self.lastText2 = text1,text2
            if WMstandard and text1=="(Push OK to type A-Z)": text1=""
            for control,current,restoreTo in self.toRestore:
                if not asUnicode(control.get())==current:
                    self.toRestore = [] ; break
            if text1 or text2: self.Cancel["text"] = localise(cond(self.ListBox.curselection(),"Cancel selection","Clear input boxes"))
            else: self.Cancel["text"] = localise(cond(olpc or GUI_for_editing_only,"Quit","Back to main menu"))
            h = hanzi_only(text1)
            if Tk_might_display_wrong_hanzi and not self.Label1["text"].endswith(wrong_hanzi_message) and (h or hanzi_only(text2)): self.Label1["text"]+=("\n"+wrong_hanzi_message)
            if h and not u"".join(fix_compatibility(text1).split())==hanzi_and_punc(text1):
                # There is hanzi in the L2 text, but it's not all hanzi.  This might mean they've pasted in a mixture of hanzi+pinyin from ruby markup (or maybe even hanzi+pinyin+English), so offer to trim it down to hanzi only.  (Allow spacing differences.)
                if not hasattr(self,"stripButton"): self.stripButton=addButton(self.TestEtcCol,localise("Delete non-hanzi"),self.stripText,status="If you pasted a mix of hanzi and\nother annotations, this can remove the annotations.")
            elif hasattr(self,"stripButton"):
                self.stripButton.pack_forget() ; del self.stripButton
            if synthCache:
                cacheManagementOptions = [] # (text, oldKey, newKey, oldFile, newFile)
                for t,l in [(text1.encode('utf-8'),secondLanguage),(text2.encode('utf-8'),firstLanguage)]:
                    k,f = synthcache_lookup(B("!synth:")+t+B("_")+B(l),justQueryCache=1)
                    if f:
                      if (checkIn(partials_langname(l),synth_partials_voices) or get_synth_if_possible(l,0)): # (no point having these buttons if there's no chance we can synth it by any method OTHER than the cache)
                        if checkIn(k,synthCache_transtbl) and B(k[:1])==B("_"): cacheManagementOptions.append(("Keep in "+l+" cache",k,k[1:],0,0))
                        elif B(k[:1])==B("_"): cacheManagementOptions.append(("Keep in "+l+" cache",0,0,f,f[1:]))
                        if checkIn(k,synthCache_transtbl): cacheManagementOptions.append(("Reject from "+l+" cache",k,"__rejected_"+k,0,0))
                        else: cacheManagementOptions.append(("Reject from "+l+" cache",0,0,f,"__rejected_"+f))
                    else:
                      k,f = synthcache_lookup(B("!synth:__rejected_")+t+B("_"+l),justQueryCache=1)
                      if not f: k,f = synthcache_lookup(B("!synth:__rejected__")+t+B("_"+l),justQueryCache=1)
                      if f:
                        if checkIn(k,synthCache_transtbl): cacheManagementOptions.append(("Undo "+l+" cache reject",k,k[11:],0,0))
                        else: cacheManagementOptions.append(("Undo "+l+" cache reject",0,0,f,f[11:]))
                      elif l==secondLanguage and mp3web and not ';' in t: cacheManagementOptions.append(("Get from "+mp3webName,0,0,0,0))
                if not hasattr(self,"cacheManagementOptions"):
                    self.cacheManagementOptions = []
                    self.cacheManagementButtons = []
                if not cacheManagementOptions==self.cacheManagementOptions:
                    for b in self.cacheManagementButtons: b.pack_forget()
                    self.cacheManagementOptions = cacheManagementOptions
                    self.cacheManagementButtons = []
                    for txt,a,b,c,d in cacheManagementOptions: self.cacheManagementButtons.append(addButton(self.TestEtcCol,txt,lambda e=self,a=a,b=b,c=c,d=d:e.doSynthcacheManagement(a,b,c,d),status="This button is for synthCache management.\nsynthCache is explained in advanced"+extsep+"txt"))
            if self.ListBox.curselection():
                if not (text1 or text2): self.ListBox.selection_clear(0,'end') # probably just added a new word while another was selected (added a variation) - clear selection to reduce confusion
                else: return # don't try to be clever with searches when editing an existing item (the re-ordering can be confusing)
            text1,text2 = text1.lower().replace(" ",""),text2.lower().replace(" ","") # ignore case and whitespace when searching
            l=map(lambda x:x[0]+"="+x[1], filter(lambda x,text1=text1,text2=text2:x[0].lower().replace(" ","").find(text1)>-1 and x[1].lower().replace(" ","").find(text2)>-1,self.vocabList)[-tkNumWordsToShow:])
            l.reverse() ; synchronizeListbox(self.ListBox,l) # show in reverse order, in case the bottom of the list box is off-screen
        def doSynthcacheManagement(self,oldKey,newKey,oldFname,newFname):
            # should be a quick operation - might as well do it in the GUI thread
            if (oldKey,oldFname) == (0,0): # special for mp3web
                self.menu_response="mp3web" ; return
            if checkIn(oldKey,synthCache_transtbl):
                if newKey: synthCache_transtbl[newKey]=synthCache_transtbl[oldKey]
                else: del synthCache_transtbl[oldKey]
                open(synthCache+os.sep+transTbl,'wb').write(B("").join([v+B(" ")+k+B("\n") for k,v in list(synthCache_transtbl.items())]))
            if oldFname:
                del synthCache_contents[oldFname]
                if newFname:
                    os.rename(synthCache+os.sep+oldFname,synthCache+os.sep+newFname)
                    synthCache_contents[newFname]=1
                else: os.remove(synthCache+os.sep+oldFname)
            self.lastText1 = 1 # ensure different so cache-management options get updated
        def restoreText(self,*args):
            for control,current,restoreTo in self.toRestore:
                if asUnicode(control.get())==current: control.set(restoreTo)
            self.toRestore = []
        def stripText(self,*args):
            t = self.Text1.get()
            u = asUnicode(t)
            v = fix_commas(hanzi_and_punc(u))
            if t==u: v=asUnicode(v)
            self.Text1.set(v)
        def thin_down_for_lesson(self):
            if hasattr(self,"OutputRow"): self.OutputRow.pack_forget()
            if hasattr(self,"CopyFromButton"):
                self.CopyFromButton.pack_forget() ; del self.CopyFromButton
            self.LessonRow.pack_forget()
            if GUI_usersRow: GUI_usersRow.pack_forget()
            if hasattr(self,"BigPrintButton"):
                self.BigPrintButton.pack_forget() ; del self.BigPrintButton
            if hasattr(self,"TestButton"): self.TestButton.pack_forget()
            else:
                for i in [self.row1,self.row2,self.row3,self.row4,self.ListBox,self.rightPanel]: i.pack_forget()
                if hasattr(self,"alternateRightPanel"):
                    self.alternateRightPanel.pack_forget()
                    del self.alternateRightPanel
                if self.change_button_shown:
                    self.ChangeButton.pack_forget()
                    self.change_button_shown = 0
                del self.ListBox # so doesn't sync lists, or assume Cancel button is a Clear button
                if hasattr(self,"cacheManagementButtons"):
                    for b in self.cacheManagementButtons: b.pack_forget()
                    del self.cacheManagementButtons,self.cacheManagementOptions
                app.master.title(appTitle)
            self.CancelRow.pack_forget() ; self.Version.pack_forget()
            self.Label.pack() ; self.CancelRow.pack()
            self.Label["text"] = "Working..." # (to be replaced by time indication on real-time, not on output-to-file)
            self.Cancel["text"] = localise("Quit")
        def bigPrint0(self):
            self.master.option_add('*font',self.bigPrintFont)
            self.sbarWidth = int(16*self.bigPrintMult)
            self.master.option_add('*Scrollbar*width',self.sbarWidth) # (works on some systems; usually ineffective on Mac)
            self.Label["font"]=self.bigPrintFont
            del self.bigPrintFont # (TODO do we want an option to undo it?  or would that take too much of the big print real-estate.)
            self.isBigPrint=1
        def bigPrint(self,*args):
            self.thin_down_for_lesson()
            self.Version["font"]=self.bigPrintFont
            self.bigPrint0()
            if self.rightPanel: # oops, need to re-construct it
                global extra_buttons_waiting_list
                extra_buttons_waiting_list = []
                make_extra_buttons_waiting_list()
                self.rightPanel = None
            self.check_window_position()
            self.todo.set_main_menu = 1
        def check_window_position(self,*args): # called when likely to be large print and filling the screen
            try: self.master.geometry("+"+str(int(self.winfo_rootx()))+"+0")
            except: pass
        def makelesson(self,*args):
            if hasattr(self,"userNo"): select_userNumber(intor0(self.userNo.get())) # in case some race condition stopped that from taking effect before (e.g. WinCE)
            try:  numWords=int(self.NumWords.get())
            except:
                self.todo.alert = localise("Error: maximum number of new words must be an integer") ; return
            try:  mins=float(self.Minutes.get())
            except:
                self.todo.alert = localise("Error: minutes must be a number") ; return
            problem=0 # following message boxes have to be resistant to "I'm just going to click 'yes' without reading it" users who subsequently complain that Gradint is ineffective.  Make the 'yes' option put them back into the parameters, and provide an extra 'proceed anyway' on 'no'.
            if numWords>=10:
                if tkMessageBox.askyesno(self.master.title(),localise("%s new words is a lot to remember at once.  Reduce to 5?") % (str(numWords),)):
                    numWords=5 ; self.NumWords.set("5")
                else: problem=1
            if mins>30:
                if tkMessageBox.askyesno(self.master.title(),localise("More than 30 minutes is rarely more helpful.  Reduce to 30?")):
                  mins=30;self.Minutes.set("30")
                else: problem=1
            if mins<20:
                if tkMessageBox.askyesno(self.master.title(),localise("Less than 20 minutes can be a rush.  Increase to 20?")):
                  mins=20;self.Minutes.set("20")
                else: problem=1
            if problem and not tkMessageBox.askyesno(self.master.title(),localise("Proceed anyway?")): return
            global maxNewWords,maxLenOfLesson
            d={}
            if not maxNewWords==numWords: d["maxNewWords"]=maxNewWords=numWords
            if not maxLenOfLesson==int(mins*60): d["maxLenOfLesson"]=maxLenOfLesson=int(mins*60)
            if d: updateSettingsFile("advanced"+dottxt,d)
            self.thin_down_for_lesson()
            self.Cancel["text"] = localise("Cancel lesson")
            self.menu_response = "go"
        def showtest(self,*args): # Can assume main menu is shown at the moment.
            title = localise(cond(self.wordsExist,"Manage word list","Create word list"))
            if hasattr(self,"userNo"):
                try: uname = lastUserNames[intor0(self.userNo.get())]
                except IndexError: uname="" # can happen if it's 0 but list is empty
                if uname:
                    title += (": "+uname)
                    select_userNumber(intor0(self.userNo.get())) # in case some race condition stopped that from taking effect before (e.g. WinCE)
            app.master.title(title)
            if hasattr(self,"BigPrintButton"):
                self.BigPrintButton.pack_forget() ; del self.BigPrintButton
            self.TestButton.pack_forget() ; del self.TestButton
            for i in [self.LessonRow,self.CancelRow,self.Version]: i.pack_forget()
            if GUI_usersRow: GUI_usersRow.pack_forget()
            self.row1 = addRow(self.leftPanel,1)
            self.row2 = addRow(self.leftPanel,1)
            self.row3 = addRow(self.leftPanel)
            self.row4 = addRow(self.leftPanel,1)
            self.Label1,self.Text1,self.Entry1 = addLabelledBox(self.row1,True)
            self.TestEtcCol = addRow(self.row1) # effectively adding a column to the end of the row, for "Speak" and any other buttons to do with 2nd-language text (although be careful not to add too many due to tabbing)
            self.TestTextButton = addButton(self.TestEtcCol,"",self.testText,status="Use this button to check how the computer\nwill pronounce words before you add them") # will set text in updateLanguageLabels
            self.Label2,self.Text2,self.Entry2 = addLabelledBox(self.row2,True)
            if not WMstandard:
              self.Entry1.bind('<Return>',self.testText)
              self.Entry1.bind('<F5>',self.debugText)
              self.Entry2.bind('<Return>',self.addText)
              for e in [self.Entry1,self.Entry2]: addStatus(e,"Enter a word or phrase to add or to test\nor to search your existing collection",mouseOnly=1)
            self.AddButton = addButton(self.row2,"",self.addText,status="Adds the pair to your vocabulary collection\nor adds extra revision if it's already there") # will set text in updateLanguageLabels
            self.L1Label,self.L1Text,self.L1Entry = addLabelledBox(self.row3,status="The abbreviation of your\nfirst (i.e. native) language")
            self.L2Label,self.L2Text,self.L2Entry = addLabelledBox(self.row3,status="The abbreviation of the other\nlanguage that you learn most")
            self.L1Entry["width"]=self.L2Entry["width"]=3
            self.L1Entry.bind('<Return>',lambda e:e.widget.after(10,lambda e=e:e.widget.event_generate('<Tab>')))
            self.L2Entry.bind('<Return>',self.changeLanguages)
            for e in [self.L1Entry,self.L2Entry]: e.bind('<Button-1>',(lambda e:e.widget.after(10,lambda e=e:selectAll(e))))
            self.ChangeLanguageButton = addButton(self.row3,"",self.changeLanguages,status="Use this button to set your\nfirst and second languages") # will set text in updateLanguageLabels
            self.ChangeLanguageButton.bind('<FocusIn>',(lambda e=None,app=app:app.after(10,lambda e=None,app=app:app.L2Entry.selection_clear())))
            self.AddButton.bind('<FocusIn>',(lambda e=None,app=app:app.after(10,lambda e=None,app=app:app.L1Entry.selection_clear()))) # for backwards tabbing
            if GUI_omit_settings and (vocabFile==user0[1] or fileExists(vocabFile)): self.row3.pack_forget()
            if textEditorCommand:
                self.RecordedWordsButton = addButton(self.row4,"",self.showRecordedWords,{"side":"left"},status="This button lets you manage recorded\n(as opposed to computer-voiced) words")
                row4right = addRightRow(self.row4)
                self.EditVocabButton = addButton(row4right,"",self.openVocabFile,{"side":"left"},status="This button lets you edit your\nvocab collection in "+textEditorName)
                if not GUI_omit_settings: addButton(row4right,"advanced"+dottxt,self.openAdvancedTxt,{"side":"left"},status="Press this button to change voices,\nlearn multiple languages, etc")
                self.make_lesson_row()
            else: # no text editor, but can at least have Recorded Words button now we have a built-in manager
                self.make_lesson_row()
                self.RecordedWordsButton = addButton(self.LessonRow,"",self.showRecordedWords,{"side":"right"},status="This button lets you manage recorded\n(as opposed to computer-voiced) words")
            if textEditorCommand and lastUserNames and lastUserNames[0]: self.CopyFromButton = addButton(cond(GUI_omit_settings,row4right,self.LessonRow),localise("Copy from..."),self.showCopyFrom,{"side":"left"},status="This button lets you copy recorded\nand computer-voiced words from other users") # TODO if not textEditorCommand then only reason why can't have this is row4right won't be defined, need to fix that (however probably don't want to bother on XO etc)
            self.remake_cancel_button(localise(cond(olpc or GUI_for_editing_only,"Quit","Back to main menu")))
            self.ChangeButton = addButton(self.CancelRow,"",self.changeItem,{"side":"left"},status="Press to alter or to delete\nthe currently-selected word in the list") ; self.ChangeButton.pack_forget() # don't display it until select a list item
            self.updateLanguageLabels()
            self.LessonRow.pack() ; self.CancelRow.pack()
            self.ListBox = Tkinter.Listbox(self.leftPanel, takefocus=0) # TODO takefocus=0 for now. bindUpDown?  but up/down/left/right also need to work IN the listbox, this could be tricky.  Also need to populate the input boxes when on the list box.
            self.ListBox.bind('<ButtonRelease-1>', self.getListItem)
            self.ListBox.bind('<ButtonRelease-3>', self.wrongMouseButton)
            addStatus(self.ListBox,"This is your collection of computer-voiced words.\nClick to hear, change or remove an item.")
            self.ListBox["width"]=1 # so it will also squash down if window is narrow
            if winCEsound: self.ListBox["font"]="Helvetica 12" # larger is awkward, but it doesn't have to be SO small!
            elif macsound and Tkinter.TkVersion>=8.6: self.ListBox["font"]=cond(hasattr(self,"isBigPrint"),"System 20","System 16") # 16 ok with magnification, clearer than 13
            self.ListBox.pack(fill=Tkinter.X,expand=1) # DON'T fill Y as well, because if you do we'll have to implement more items, and that could lose the clarity of incremental search
            if not GUI_omit_statusline: self.Version.pack(fill=Tkinter.X,expand=1)
            self.lastText1,self.lastText2=1,1 # (different from empty string, so it sync's)
            if not self.rightPanel:
                self.rightPanel = Tkinter.Frame(self)
                for i in range(min(max_extra_buttons,len(extra_buttons_waiting_list))): self.add_extra_button()
            if not hasattr(self,"userNo") or not intor0(self.userNo.get()): self.rightPanel.pack({"side":"left"})
            elif self.extra_button_callables:
                self.alternateRightPanel = Tkinter.Frame(self)
                self.alternateRightPanel.pack({"side":"left"})
                curWidth = self.winfo_width()
                addLabel(self.alternateRightPanel,"Only the first user can access the preset collections, but you can copy the vocab lists and recordings from each other once you've added them.")["wraplength"]=int(curWidth/2) # (presets are not really compatible with multiple users, unless re-write for copy-and-track-what's-done, which would take double the disk space on a one-person setup AND would have trouble upgrading existing users who have started into their presets)
            self.Entry1.focus()
        def add_extra_button(self):
            global extra_buttons_waiting_list
            extra_buttons_waiting_list[0].add()
            extra_buttons_waiting_list = extra_buttons_waiting_list[1:]
        def openVocabFile(self,*args): self.fileToEdit, self.menu_response = vocabFile,"edit"
        def openAdvancedTxt(self,*args): self.fileToEdit, self.menu_response = "advanced"+dottxt,"edit"
        def showRecordedWords(self,*args): doRecWords()
        def showCopyFrom(self,*args):
            m=Tkinter.Menu(None, tearoff=0, takefocus=0)
            for i in range(len(lastUserNames)):
                if lastUserNames[i] and not i==intor0(self.userNo.get()):
                    if fileExists(addUserToFname(user0[1],i)): m.add_command(label=u"Copy vocab list from "+lastUserNames[i],command=(lambda e=None,i=i,self=self:self.copyVocabFrom(i)))
                    m.add_command(label=u"Copy recordings to/from "+lastUserNames[i],command=(lambda e=None,i=i,self=self:self.setToOpen((addUserToFname(user0[0],i),addUserToFname(user0[0],intor0(self.userNo.get()))))))
            m.tk_popup(self.CopyFromButton.winfo_rootx(),self.CopyFromButton.winfo_rooty(),entry="0")
        def setToOpen(self,toOpen): self.menu_response,self.toOpen = "samplesCopy",toOpen
        def copyVocabFrom(self,userNo):
            # Copy any NEW vocab lines (including comments).  TODO could also insert them in the right place (like 'diff' without the deletions)
            select_userNumber(userNo,updateGUI=0)
            vCopyFrom = vocabLinesWithLangs()
            select_userNumber(intor0(self.userNo.get()),updateGUI=0)
            vCurrent = list2set(vocabLinesWithLangs())
            o=appendVocabFileInRightLanguages()
            if not o: return # IOError
            langs = (secondLanguage,firstLanguage)
            for newLangs,line in vCopyFrom:
                if checkIn((newLangs,line),vCurrent): continue # already got it
                if not newLangs==langs: o.write(B("SET LANGUAGES ")+B(" ").join(list(newLangs))+B("\n"))
                o.write(B(line)+B("\n"))
                langs = newLangs
            o.close()
            if hasattr(self,"vocabList"): del self.vocabList # re-read
        def setVariant(self,v):
            scriptVariants[firstLanguage] = v
            updateSettingsFile(settingsFile,{"scriptVariants":scriptVariants})
            if hasattr(self,"TestButton"):
                self.thin_down_for_lesson()
                self.todo.set_main_menu="keep-outrow"
            else: self.updateLanguageLabels()
        def changeLanguages(self,*args):
            global firstLanguage,secondLanguage
            firstLanguage1=asUnicode(self.L1Text.get()).encode('utf-8')
            secondLanguage1=asUnicode(self.L2Text.get()).encode('utf-8')
            if (B(firstLanguage),B(secondLanguage)) == (firstLanguage1,secondLanguage1): # they didn't change anything
                langs = ESpeakSynth().describe_supported_languages()
                msg = (localise("To change languages, edit the boxes that say '%s' and '%s', then press the '%s' button.") % (firstLanguage,secondLanguage,localise("Change languages")))+"\n\n"+localise("Recorded words may be in ANY languages, and you may choose your own abbreviations for them.  However if you want to use the computer voice for anything then please use standard abbreviations.")
                if langs:
                    if tkMessageBox.askyesno(self.master.title(),msg+"  "+localise("Would you like to see a list of the standard abbreviations for languages that can be computer voiced?")): self.todo.alert = localise("Languages with computer voices (some better than others):")+"\n"+langs
                else: self.todo.alert = msg+"  "+localise("(Sorry, a list of these is not available on this system - check eSpeak installation.)")
                return
            need_redisplay = checkIn("@variants-"+GUI_languages.get(firstLanguage,firstLanguage),GUI_translations) or checkIn("@variants-"+GUI_languages.get(S(firstLanguage1),S(firstLanguage1)),GUI_translations) # if EITHER old or new lang has variants, MUST reconstruct that row.  (TODO also do it anyway to get the "Speaker" etc updated?  but may cause unnecessary flicker if that's no big problem)
            firstLanguage,secondLanguage = S(firstLanguage1),S(secondLanguage1)
            updateSettingsFile(settingsFile,{"firstLanguage":firstLanguage,"secondLanguage":secondLanguage})
            if need_redisplay:
                self.thin_down_for_lesson()
                self.todo.set_main_menu="test"
            else: self.updateLanguageLabels()
            if hasattr(self,"vocabList"): del self.vocabList # it will need to be re-made now
        def updateLanguageLabels(self):
            # TODO things like "To" and "Speaker" need updating dynamically with localise() as well, otherwise will be localised only on restart (unless the old or new lang has variants, in which case it will be repainted anyway above)
            self.Label1["text"] = (localise("Word in %s") % localise(secondLanguage))+":"
            self.Label2["text"] = (localise("Meaning in %s") % localise(firstLanguage))+":"
            self.L1Text.set(firstLanguage)
            self.L2Text.set(secondLanguage)
            self.L1Label["text"] = localise("Your first language")+":"
            self.L2Label["text"] = localise("second")+":"
            self.TestTextButton["text"] = localise("Speak") ; self.lastOutTo=-1 # so updates to "To WAV" etc if necessary
            if hasattr(self,"userNo") and intor0(self.userNo.get()): gui_vocabFile_name="vocab file" # don't expose which user number they are because that might change
            elif len(vocabFile)>15 and os.sep in vocabFile: gui_vocabFile_name=vocabFile[vocabFile.rindex(os.sep)+1:]
            else: gui_vocabFile_name=vocabFile
            if gui_vocabFile_name=="vocab.txt": gui_vocabFile_name=localise(gui_vocabFile_name)
            self.AddButton["text"] = localise("Add to %s") % gui_vocabFile_name
            self.ChangeLanguageButton["text"] = localise("Change languages")
            self.ChangeButton["text"] = localise("Change or delete item")
            if hasattr(self,"EditVocabButton"): self.EditVocabButton["text"] = cond(WMstandard,gui_vocabFile_name,localise(textEditorName)+" "+gui_vocabFile_name) # (save as much space as possible on WMstandard by omitting the "Edit " verb)
            if hasattr(self,"RecordedWordsButton"): self.RecordedWordsButton["text"] = localise("Recorded words")
        def wrongMouseButton(self,*args): self.todo.alert="Please use the OTHER mouse button when clicking on list and button controls." # Simulating it is awkward.  And we might as well teach them something.
        def getListItem(self,*args):
            sel = self.ListBox.curselection()
            if sel:
                item = self.ListBox.get(int(sel[0]))
                if not "=" in item: return # ignore clicks on the Loading message
                l2,l1 = item.split('=',1)
                self.Text1.set(l2) ; self.Text2.set(l1)
            elif not self.ListBox.size(): self.todo.alert="The synthesized words list is empty.  You need to add synthesized words before you can click in the list."
            else: self.todo.alert="Click on a list item to test, change or delete.  You can add a new item using the test boxes above." # Should never get here in Tk 8.4 (if click below bottom of list then last item is selected)
        def changeItem(self,*args):
            self.zap_newlines()
            sel = self.ListBox.curselection()
            l2,l1 = self.ListBox.get(int(sel[0])).split('=',1)
            self.toDelete = l2,l1
            if (asUnicode(self.Text1.get()),asUnicode(self.Text2.get())) == (l2,l1):
                if tkMessageBox.askyesno(self.master.title(),localise("You have not changed the test boxes.  Do you want to delete %s?") % (l2+"="+l1,)):
                    self.menu_response="delete"
            else: self.menu_response="replace"
        def testText(self,*args):
            self.zap_newlines() # (fullstop-quote-newline combinations have been known to confuse eSpeak)
            self.menu_response="test"
        def debugText(self,*args):
            # called when F5 is pressed on the 1st text box
            # currently adds Unicode values to the text, and shows as a dialogue
            # (for use when trying to diagnose people's copy/paste problems)
            setTo = []
            for c in asUnicode(self.Text1.get()): setTo.append(c+"["+hex(ord(c))[2:]+"]")
            setTo=u"".join(setTo)
            self.Text1.set(setTo) ; self.todo.alert = setTo
        def addText(self,*args):
            self.zap_newlines()
            self.menu_response="add"
        def zap_newlines(self): # in case someone pastes in text that contains newlines, better not keep them when adding to vocab
            text1,text2 = asUnicode(self.Text1.get()),asUnicode(self.Text2.get())
            # (also remove the simple visual markup that Wenlin sometimes adds)
            t1,t2=text1,text2
            for zap in ["\n","\r","<b>","</b>","<i>","</i>","<u>","</u>"]: t1,t2=t1.replace(zap,""),t2.replace(zap,"")
            t1,t2 = wspstrip(t1),wspstrip(t2)
            if not t1==text1: self.Text1.set(t1)
            if not t2==text2: self.Text2.set(t2)
        def getEncoder(self,*args):
            self.thin_down_for_lesson()
            self.menu_response="get-encoder"
        def setNotFirstTime(self): self.todo.not_first_time = 1
        def setLabel(self,t): self.todo.set_label = t
        def cancel(self,*args):
            if hasattr(self,"ListBox"): # it MIGHT be a 'clear' button
                text1,text2 = asUnicode(self.Text1.get()),asUnicode(self.Text2.get())
                if text1 or text2:
                    self.Text1.set("") ; self.Text2.set("")
                    if self.ListBox.curselection(): self.ListBox.selection_clear(int(self.ListBox.curselection()[0]))
                    self.Cancel["text"] = localise(cond(olpc or GUI_for_editing_only,"Quit","Back to main menu"))
                    return
                elif olpc or GUI_for_editing_only: pass # fall through to Quit
                else:
                    # (comment this out if you want the Quit button to really quit even from add/test words, but probably don't want this now there are other options on the main menu e.g. user switching)
                    self.thin_down_for_lesson()
                    self.todo.set_main_menu="keep-outrow" ; return
            if not self.cancelling:
                if emulated_interruptMain:
                    self.setLabel("Trying to interrupt main thread, please wait...")
                    global need_to_interrupt ; need_to_interrupt = 1
                else: thread.interrupt_main()
            self.cancelling = 1
    def appThread(appclass):
        global app ; appclass() # sets 'app' to itself on construction
        app.master.title(appTitle)
        app.wordsExist = words_exist()
        app.mainloop()
        closeBoxPressed = not hasattr(app.todo,"exit_ASAP")
        app = 0 # (not None - see 'app==None' below)
        if closeBoxPressed:
            if emulated_interruptMain:
                global need_to_interrupt ; need_to_interrupt = 1
                while RM_running: time.sleep(0.1) # ensure main thread is last to exit, sometimes needed
            else: thread.interrupt_main()
    def processing_thread():
        while not app: time.sleep(0.1) # make sure started
        # import cProfile as profile ; return profile.run('rest_of_main()',sort=2)
        rest_of_main()
    if Tkinter.TkVersion < 8.5: # we can do the processing in the main thread, so interrupt_main works
        thread.start_new_thread(appThread,(Application,))
        processing_thread()
    else: # GUI must have main thread
        global emulated_interruptMain ; emulated_interruptMain = 1
        thread.start_new_thread(processing_thread,())
        appThread(Application)

def hanzi_only(unitext): return u"".join(filter(lambda x:0x3000<ord(x)<0xa700 or ord(x)>=0x10000, list(unitext)))
def hanzi_and_punc(unitext): return u"".join(filter(lambda x:0x3000<ord(x)<0xa700 or ord(x)>=0x10000 or x in '.,?;:\'()[]!0123456789-', list(remove_tone_numbers(fix_compatibility(unitext))))) # no " as it could be from SGML markup
# (exclusion of 3000 in above is deliberate, otherwise get problems with hanzi spaces being taken out by fix-compat+strip hence a non-functional 'delete non-hanzi' button appears)
def guiVocabList(parsedVocab):
    # This needs to be fast.  Have tried writing interatively rather than filter and map, and assume stuff is NOT already unicode (so just decode rather than call ensure_unicode) + now assuming no !synth: (but can still run with .txt etc)
    sl2,fl2 = "_"+secondLanguage,"_"+firstLanguage
    sl3,fl3 = sl2+dottxt, fl2+dottxt # txt files
    # (sample files are omitted from the list)
    sl2Len,fl2Len = -len(sl2),-len(fl2)
    ret = []
    for a,b,c in parsedVocab:
        if c.endswith(sl2): c=c[:sl2Len]
        elif c.endswith(sl3): c=readText(c)
        else: continue
        if type(b)==type([]): b=b[cond(len(b)==3,1,-1)]
        if b.endswith(fl2): b=b[:fl2Len]
        elif b.endswith(fl3): b=readText(b)
        else: continue
        ret.append((ensure_unicode(c),ensure_unicode(b)))
    return ret
def readText(l): # see utils/transliterate.py (running guiVocabList on txt files from scanSamples)
    l = B(samplesDirectory)+B(os.sep)+B(l)
    if checkIn(l,variantFiles): # oops. just read the 1st .txt variant
        if B(os.sep) in l: lp=(l+B(os.sep))[:l.rfind(B(os.sep))]+B(os.sep)
        else: lp = B("")
        varList = filter(lambda x:x.endswith(B(dottxt)),variantFiles[l])
        varList.sort() # so at least it consistently returns the same one.  TODO utils/ cache-synth.py list-synth.py synth-batchconvert-helper.py all use readText() now, can we get them to cache the other variants too?
        l = lp + varList[0]
    return bwspstrip(u8strip(read(l)))

def singular(number,s):
  s=localise(s)
  if firstLanguage=="en" and number==1 and s[-1]=="s": return s[:-1]
  return s
def localise(s):
  if s=="zh-yue" or s=="zhy": k="cant"
  else: k=s
  d = GUI_translations.get(k,{}) ; s2 = 0
  GUIlang = GUI_languages.get(firstLanguage,firstLanguage)
  if scriptVariants.get(GUIlang,0): s2 = d.get(GUIlang+str(scriptVariants[GUIlang]+1),0)
  if not s2: s2 = d.get(GUIlang,s)
  return s2
if Tk_might_display_wrong_hanzi: localise=lambda s:s
if winCEsound: # some things need more squashing
    del localise
    def localise(s):
        s=GUI_translations.get(s,{}).get(firstLanguage,s)
        return {"Your first language":"1st","second":"2nd","Start lesson":"Start"}.get(s,s)

def synchronizeListbox(listbox,masterList):
    mi=li=0 ; toDelete = []
    while True:
        l=listbox.get(li)
        if mi==len(masterList):
            if not l: break
            elif l in masterList: listbox.delete(li) # re-ordering - unconditionally delete
            else:
                toDelete.append(li) ; li += 1
            continue
        if masterList[mi]==l: mi,li=mi+1,li+1
        elif (not l) or (l in masterList[mi+1:]): # masterList has an extra item before l, or at the end
            listbox.insert(li,masterList[mi])
            mi,li=mi+1,li+1
        elif l in masterList[:mi]: listbox.delete(li) # re-ordering - unconditionally delete
        else:
            toDelete.append(li) ; li += 1
    toDelete.reverse() # last one first so don't disrupt numbers
    i=0
    while i<len(toDelete):
        if not listbox.get(tkNumWordsToShow): break
        listbox.delete(toDelete[i]) ; i += 1
    # When list shrinks small enough, move words down instead of deleting
    li=len(masterList)+len(toDelete)-i # i.e. just past current end of list
    while i<len(toDelete):
        if not toDelete[i]==li-1: # not in right place already
            listbox.insert(li,listbox.get(toDelete[i]))
            listbox.delete(toDelete[i])
        i += 1 ; li -= 1

# Tk stuff (must be done outside of main() so the imported modules are globally visible)
if useTK:
    # Find editor and file-manager commands for the GUI to use
    textEditorName="Edit" ; textEditorWaits=0
    textEditorCommand=explorerCommand=None
    if winsound or mingw32 or cygwin:
        textEditorName="Notepad" ; textEditorWaits=1
        textEditorCommand="notepad"
        explorerCommand="explorer"
    elif macsound:
        textEditorName="TextEdit"
        textEditorCommand="open -e"
        if got_program("bbedit"):
            textEditorName="bbedit"
            textEditorCommand="bbedit -w" ; textEditorWaits=1
        elif got_program("edit"): # TextWrangler
            textEditorName="edit"
            textEditorCommand="edit -w" ; textEditorWaits=1
        if sys.version.startswith("2.3.5") and "DISPLAY" in os.environ: explorerCommand = None # 'open' doesn't seem to work when running from within Python in X11 on 10.4
        else: explorerCommand="open"
    elif unix:
        if "KDE_FULL_SESSION" in os.environ and got_program("kfmclient"):
            # looks like we're in a KDE session and can use the kfmclient command
            textEditorCommand=explorerCommand="kfmclient exec"
        elif not olpc and got_program("gnome-open"):
            textEditorCommand=explorerCommand="gnome-open"
        elif got_program("nautilus"): explorerCommand="nautilus"
        elif got_program("rox"):
            # rox is available - try using that to open directories
            # (better not use it for editor as it might not be configured)
            # (TODO if both rox and gnome are available, can we tell which one the user prefers?)
            explorerCommand="rox"
        # anyway, see if we can find a nice editor
        for editor in ["leafpad","featherpad","gedit","nedit","kedit","xedit"]:
            if got_program(editor):
                textEditorName=textEditorCommand=editor
                textEditorWaits = 1
                if textEditorName.endswith("edit"):
                    textEditorName=textEditorName[:-4]+"-"+textEditorName[-4:]
                    textEditorName=textEditorName[0].upper()+textEditorName[1:]
                break
    # End of finding editor - now start GUI
    try:
        try: import thread
        except ImportError: import _thread as thread
        try: import Tkinter,tkMessageBox
        except:
            import tkinter as Tkinter
            from tkinter import messagebox as tkMessageBox
        forceRadio=(macsound and 8.49<Tkinter.TkVersion<8.59) # indicatoron doesn't do very well in OS X 10.6 (Tk 8.5) unless we patched it
        if olpc:
            def interrupt_main(): os.kill(os.getpid(),2) # sigint
            thread.interrupt_main = interrupt_main
            # (os.kill is more reliable than interrupt_main() on OLPC, *but* on Debian Sarge (2.4 kernel) threads are processes so DON'T do this.)
        elif not hasattr(thread,"interrupt_main"): emulated_interruptMain = 1
        elif signal: # work around the "int object is not callable" thing on some platforms' interrupt_main
            def raise_int(*args): raise KeyboardInterrupt
            signal.signal(signal.SIGINT,raise_int)
    except RuntimeError:
        useTK = 0
        if __name__=="__main__": show_warning("Cannot start the GUI due to a Tk error")
    except ImportError:
        useTK = 0
        if __name__=="__main__" and not riscos_sound: show_warning("Cannot start the GUI because tkinter package is not installed on this system"+cond(fileExists("/var/lib/dpkg/status")," (try python-tk in Debian)","")+".")

def openDirectory(dir,inGuiThread=0):
    if winCEsound:
        if not dir[0]=="\\": dir=os.getcwd()+cwd_addSep+dir # must be absolute
        ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(ShellExecuteInfo(60,File=u"\\Windows\\fexplore",Parameters=ensure_unicode(dir))))
    elif explorerCommand:
        if ' ' in dir: dir='"'+dir+'"'
        cmd = explorerCommand+" "+dir
        if winsound or mingw32: cmd="start "+cmd # (not needed on XP but is on Vista)
        elif unix: cmd += "&"
        os.system(cmd)
    else:
        msg = ""
        if not dir.startswith(os.sep): msg=" (in %s)" % os.getcwd()
        msg = "Don't know how to start the file explorer.  Please open the %s directory%s" % (dir,msg)
        if inGuiThread: tkMessageBox.showinfo(app.master.title(),msg)
        else: waitOnMessage(msg)

def generalCheck(text,language,pauseOnError=0): # text is utf-8; returns error message if any
    if not text: return # always OK empty strings
    if pauseOnError:
        ret = generalCheck(text,language)
        if ret: waitOnMessage(ret)
        return ret
    if language=="zh":
        allDigits = True ; text=B(text)
        for i in xrange(len(text)):
            t = text[i:i+1]
            if ord(t)>127: return # got hanzi or tone marks
            if t in B("12345"): return # got tone numbers
            if t not in B("0123456789. "): allDigits = False
        if allDigits: return
        return B("Pinyin needs tones.  Please go back and add tone numbers to ")+text+B(".")+cond(startBrowser(B("http://www.mdbg.net/chinese/dictionary?wdqb=")+bwspstrip(fix_pinyin(text,[])).replace(B("5"),B("")).replace(B(" "),B("+"))),B(" Gradint has pointed your web browser at an online dictionary that might help."),B(""))

def check_for_slacking():
    if fileExists(progressFile): checkAge(progressFile,localise("It has been %d days since your last Gradint lesson.  Please try to have one every day."))
    else:
        installDateFile = progressFile.replace("progress","installed")
        if not fileExists(installDateFile):
            try: open(installDateFile,"w")
            except: pass
        else: checkAge(installDateFile,localise("It has been %d days since you installed Gradint and you haven't had a lesson yet.  Please try to have one every day."))
def checkAge(fname,message):
    days = int((time.time()-os.stat(fname)[8])/3600/24)
    if days>=5 and (days%5)==0: waitOnMessage(message % days)

def s60_addVocab():
  label1,label2 = ensure_unicode(localise("Word in %s") % localise(secondLanguage)),ensure_unicode(localise("Meaning in %s") % localise(firstLanguage))
  while True:
    result = appuifw.multi_query(label1,label2) # unfortunately multi_query can't take default items (and sometimes no T9!), but Form is too awkward (can't see T9 mode + requires 2-button save via Options) and non-multi query would be even more modal
    if not result: return # cancelled
    l2,l1 = result # guaranteed to both be populated
    while generalCheck(l2.encode('utf-8'),secondLanguage,1):
        l2=appuifw.query(label1,"text",u"")
        if not l2: return # cancelled
    # TODO detect duplicates like Tk GUI does?
    appuifw.note(u"Added "+l2+"="+l1,"conf")
    appendVocabFileInRightLanguages().write((l2+"="+l1+"\n").encode("utf-8"))
def s60_changeLang():
    global firstLanguage,secondLanguage
    result = appuifw.multi_query(ensure_unicode(localise("Your first language")+" (e.g. "+firstLanguage+")"),ensure_unicode(localise("second")+" (e.g. "+secondLanguage+")"))
    if not result: return # cancelled
    l1,l2 = result
    firstLanguage,secondLanguage = l1.encode('utf-8').lower(),l2.encode('utf-8').lower()
    updateSettingsFile(settingsFile,{"firstLanguage":firstLanguage,"secondLanguage":secondLanguage})
def s60_runLesson():
    global maxLenOfLesson
    ml = appuifw.query(u"Max number of minutes","number",int(maxLenOfLesson/60))
    if not ml: return
    maxLenOfLesson = int(float(ml)*60)
    lesson_loop()
def s60_viewVocab():
    global justSynthesize
    doLabel("Reading your vocab list, please wait...")
    vList = map(lambda x:x[0]+u"="+x[1], guiVocabList(parseSynthVocab(vocabFile,1)))
    if not vList: return waitOnMessage("Your computer-voiced vocab list is empty.")
    while True:
      appuifw.app.body = None
      sel = appuifw.selection_list(vList,search_field=1)
      if sel==None: return
      l2,l1 = vList[sel].split("=",1)
      action = appuifw.popup_menu([u"Speak (just "+secondLanguage+")",u"Speak ("+secondLanguage+" and "+firstLanguage+")",u"Change "+secondLanguage,u"Change "+firstLanguage,u"Delete item",u"Cancel"], vList[sel])
      if action==0 or action==1:
        doLabel("Speaking...")
        justSynthesize = B(secondLanguage)+B(" ")+l2.encode('utf-8')
        if action==1: justSynthesize += (B('#')+B(firstLanguage)+B(" ")+l1.encode('utf-8'))
        just_synthesize()
        justSynthesize = ""
      elif action==5: pass
      else:
          if action==4 and not getYN(u"Are you sure you want to delete "+vList[sel]+"?"): continue
          oldL1,oldL2 = l1,l2
          if action==2:
              first=1
              while first or (l2 and generalCheck(l2.encode('utf-8'),secondLanguage,1)):
                  first=0 ; l2=appuifw.query(ensure_unicode(secondLanguage),"text",l2)
              if not l2: continue
          elif action==3:
              l1 = appuifw.query(ensure_unicode(firstLanguage),"text",l1)
              if not l1: continue
          doLabel("Processing")
          delOrReplace(oldL2,oldL1,l2,l1,cond(action==4,"delete","replace"))
          if action==4:
              del vList[sel]
              if not vList: return # empty
          else: vList[sel] = l2+"="+l1
def android_addVocab():
  while True:
    l2 = None
    while not l2 or generalCheck(l2.encode('utf-8'),secondLanguage,1):
      l2 = android.dialogGetInput("Add word","Word in %s" % localise(secondLanguage)).result
      if not l2: return # cancelled
    l1 = android.dialogGetInput("Add word","Meaning in %s" % localise(firstLanguage)).result
    if not l1: return # cancelled
    # TODO detect duplicates like Tk GUI does?
    android.makeToast(u"Added "+l2+"="+l1)
    appendVocabFileInRightLanguages().write((l2+"="+l1+"\n").encode("utf-8"))
def android_changeLang():
    global firstLanguage,secondLanguage
    l1 = android.dialogGetInput("Gradint","Enter your first language",firstLanguage).result
    if not l1: return # cancelled
    l2 = android.dialogGetInput("Gradint","Enter your second language",secondLanguage).result
    if not l2: return # cancelled
    firstLanguage,secondLanguage = l1.encode('utf-8').lower(),l2.encode('utf-8').lower()
    updateSettingsFile(settingsFile,{"firstLanguage":firstLanguage,"secondLanguage":secondLanguage})

def delOrReplace(L2toDel,L1toDel,newL2,newL1,action="delete"):
    langs = [secondLanguage,firstLanguage]
    v=u8strip(read(vocabFile)).replace(B("\r\n"),B("\n")).replace(B("\r"),B("\n"))
    if paranoid_file_management:
        fname = os.tempnam()
        o = open(fname,"w")
    else: o=open(vocabFile,"w")
    found = 0
    if last_u8strip_found_BOM: writeB(o,LB('\xef\xbb\xbf')) # re-write it
    v=v.split(B("\n"))
    if v and not v[-1]: v=v[:-1] # don't add an extra blank line at end
    for l in v:
        l2=l.lower()
        if l2.startswith(B("set language ")) or l2.startswith(B("set languages ")):
            langs=map(S,l.split()[2:]) ; writeB(o,l+B("\n")) ; continue
        thisLine=map(bwspstrip,l.split(B("="),len(langs)-1))
        if (langs==[secondLanguage,firstLanguage] and thisLine==[L2toDel.encode('utf-8'),L1toDel.encode('utf-8')]) or (langs==[firstLanguage,secondLanguage] and thisLine==[L1toDel.encode('utf-8'),L2toDel.encode('utf-8')]):
            # delete this line.  and maybe replace it
            found = 1
            if action=="replace":
                if langs==[secondLanguage,firstLanguage]: writeB(o,newL2.encode("utf-8")+B("=")+newL1.encode("utf-8")+B("\n"))
                else: writeB(o,newL1.encode("utf-8")+B("=")+newL2.encode("utf-8")+B("\n"))
        else: writeB(o,l+B("\n"))
    o.close()
    if paranoid_file_management:
        write(vocabFile,read(fname))
        os.remove(fname)
    return found

def maybeCanSynth(lang): return checkIn(lang,synth_partials_voices) or get_synth_if_possible(lang,0) or synthCache
def android_main_menu():
  while True:
    menu=[]
    if maybeCanSynth(secondLanguage):
        menu.append((unicode(localise("Just speak a word")),primitive_synthloop))
        doVocab = maybeCanSynth(firstLanguage)
        if doVocab: menu.append((unicode(localise("Add word to my vocab")),android_addVocab))
        menu.append((unicode(localise("Make lesson from vocab")),lesson_loop))
        # if doVocab: menu.append((u"View/change vocab",android_viewVocab)) # (TODO but lower priority because SL4A has an editor)
    else: menu.append((unicode(localise("Make lesson")),lesson_loop))
    menu += [(unicode(localise("Record word(s) with mic")),android_recordWord),(unicode(localise("Change languages")),android_changeLang)]
    menu.append((unicode(localise("Quit")),None))
    android.dialogCreateAlert("Gradint","Choose an action")
    android.dialogSetItems(map (lambda x:x[0], menu))
    android.dialogShow()
    try: function = menu[android.dialogGetResponse().result['item']][1]
    except KeyError: break # probably an error condition: don't try to redisplay, just quit
    if function: function() # and redisplay after
    else: break # quit
def s60_main_menu():
  while True:
    appuifw.app.body = None # NOT text saying version no etc - has distracting blinking cursor
    menu=[]
    if maybeCanSynth(secondLanguage):
        menu.append((u"Just speak a word",primitive_synthloop)) # no localise() as S60 is not guaranteed to be able to display the characters
        doVocab = maybeCanSynth(firstLanguage)
        if doVocab: menu.append((u"Add word to my vocab",s60_addVocab))
        menu.append((u"Make lesson from vocab",s60_runLesson))
        if doVocab: menu.append((u"View/change vocab",s60_viewVocab))
    else: menu.append((u"Make lesson",s60_runLesson))
    menu += [(u"Record word(s) with mic",s60_recordWord),(u"Change languages",s60_changeLang)]
    if len(menu)<5: menu.append((u"Quit",None)) # see comment below
    choice = appuifw.popup_menu(map (lambda x:x[0], menu),u"Choose an action:") # (selection_list can be better than popup_menu(l,u"Choose an action:") if over 5 items, but may need further trimming the width of each item) (the Quit item can go however - can cancel the menu instead.  Or keep it & don't mind it being off-screen c.f. in-vocab-list popup.)
    try: function = menu[choice][1]
    except: break
    if function: function()
    else: break

def downloadLAME():
    # Sourceforge keep making this harder!
    # Removed code to check for latest version, as we
    # can't use v3.100 due to Lame bug 488.
    return not system("""if which curl >/dev/null 2>/dev/null; then Curl="curl -L"; else Curl="wget -O -"; fi
if ! [ -e lame*.tar.gz ]; then
  if ! $Curl "https://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz/download" > lame.tar.gz; then
    rm -f lame.tar.gz; exit 1
  fi
  if grep downloads.sourceforge lame.tar.gz 2>/dev/null; then
    Link="$(cat lame.tar.gz|grep downloads.sourceforge|head -1)"
    echo "Got HTML: $Link" 1>&2
    Link="$(echo "$Link"|sed -e 's/.*http/http/' -e 's,.*/projects,http://sourceforge.net/projects,' -e 's/".*//')"
    echo "Following link to $Link" 1>&2
    if ! $Curl "$Link" > lame.tar.gz; then
      rm -f lame.tar.gz; exit 1
    fi
  fi
fi""")

def gui_event_loop():
    app.todo.set_main_menu = 1 ; braveUser = 0
    global disable_once_per_day
    if disable_once_per_day==2:
      disable_once_per_day = cond(getYN(localise("Do you want Gradint to start by itself and remind you to practise?")),0,1)
      updateSettingsFile("advanced"+dottxt,{"disable_once_per_day":disable_once_per_day})
      if disable_once_per_day: # signal the background process to stop next time
        try: os.remove("background"+dottxt)
        except: pass
    if orig_onceperday&2: check_for_slacking()
    while app:
        while not hasattr(app,"menu_response"):
            if warnings_printed: waitOnMessage("") # If running gui_event_loop, better put any warnings in a separate dialogue now, rather than waiting for user to get one via 'make lesson' or some other method
            if hasattr(app,"needVocablist") and not hasattr(app,"vocabList"):
                v = guiVocabList(parseSynthVocab(vocabFile,1)) # (in non-GUI thread because can take a while when large)
                if app: app.vocabList = v # check again because there's a race condition if close the app while parseSynthVocab is running
                else: return
                del v
            if emulated_interruptMain: check_for_interrupts()
            time.sleep(0.3)
        menu_response = app.menu_response
        del app.menu_response
        if menu_response=="input": # WMstandard
            app.todo.input_response=raw_input()
        elif menu_response=="go":
            gui_outputTo_start()
            if not soundCollector: app.todo.add_briefinterrupt_button = 1
            try: lesson_loop()
            except PromptException:
                prEx = sys.exc_info()[1]
                waitOnMessage("Problem finding prompts:\n"+prEx.message) # and don't quit, user may be able to fix
            except KeyboardInterrupt: pass # probably pressed Cancel Lesson while it was still being made (i.e. before handleInterrupt)
            if app and not soundCollector: app.todo.remove_briefinterrupt_button = 1 # (not app if it's closed by the close box)
            gui_outputTo_end()
            if not app: return # (closed by the close box)
            else: app.todo.set_main_menu = 1
        elif menu_response=="edit":
            if not braveUser and fileExists(vocabFile) and open(vocabFile).readline().find("# This is vocab.txt.")==-1: braveUser=1
            if winCEsound:
                if braveUser or getYN("You must read what it says and keep to the same format.  Continue?"):
                    braveUser = 1
                    # WinCE Word does not save non-Western characters when saving plain text (even if there's a Unicode "cookie")
                    waitOnMessage("WARNING: Word may not save non-Western characters properly.  Try an editor like MADE instead (need to set its font).") # TODO Flinkware MADE version 2.0.0 has been known to insert spurious carriage returns at occasional points in large text files
                    if not app.fileToEdit[0]=="\\": app.fileToEdit=os.getcwd()+cwd_addSep+app.fileToEdit # must be absolute
                    if not fileExists(app.fileToEdit): open(app.fileToEdit,"w") # at least make sure it exists
                    ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(ShellExecuteInfo(60,File=ensure_unicode(app.fileToEdit))))
                    waitOnMessage("When you've finished editing "+app.fileToEdit+", close it and start gradint again.")
                    return
            elif textEditorCommand:
                if braveUser or getYN("Open "+app.fileToEdit+" in "+textEditorName+"?\n(You must read what it says and keep to the same format.)"):
                    braveUser = 1 ; fileToEdit=app.fileToEdit
                    if not fileExists(fileToEdit): open(fileToEdit,"w") # at least make sure it exists
                    if textEditorWaits:
                        oldContents = read(fileToEdit)
                        if paranoid_file_management: # run the editor on a temp file instead (e.g. because gedit can fail when saving over ftpfs)
                            fileToEdit=os.tempnam()+dottxt
                            open(fileToEdit,"w").write(oldContents)
                    cmd = textEditorCommand+" "+fileToEdit
                    if textEditorWaits:
                        if macsound: app.todo.thindown="Waiting for you to close the "+textEditorName+" window"
                        else: app.todo.thindown="Waiting for you to quit "+textEditorName
                        t = time.time()
                        system(cmd)
                        if time.time() < t+3: waitOnMessage(textEditorName+" returned control to Gradint in less than 3 seconds.  Perhaps you already had an instance running and it loaded the file remotely.  Press OK when you have finished editing the file.")
                        newContents = read(fileToEdit)
                        if not newContents==oldContents:
                            if paranoid_file_management: write(app.fileToEdit,newContents)
                            if app.fileToEdit==vocabFile:
                                app.wordsExist=1 ; del app.vocabList # re-read
                            else: waitOnMessage("The changes you made to "+app.fileToEdit+" will take effect when you quit Gradint and start it again.")
                        del oldContents,newContents
                        if paranoid_file_management: os.remove(fileToEdit) # the temp file
                        app.todo.set_main_menu = "test" # back to the Add/Test screen
                    else: # not textEditorWaits
                        if winsound or mingw32: cmd="start "+cmd
                        elif unix: cmd += "&"
                        os.system(cmd)
                        waitOnMessage("Gradint has started "+textEditorName+", and will now quit.\nWhen you have finished editing "+app.fileToEdit+", save it and start gradint again.")
                        return
            else: waitOnMessage("Don't know how to start the text editor.  Please edit %s yourself (in %s)" % (app.fileToEdit,os.getcwd()))
        elif menu_response=="samples":
            setup_samplesDir_ifNec()
            openDirectory(samplesDirectory)
        elif menu_response=="samplesCopy":
            for i in app.toOpen:
                setup_samplesDir_ifNec(i)
                openDirectory(i)
            del app.toOpen
            waitOnMessage("Gradint has opened both of the recorded words folders, so you can copy things across.")
        elif menu_response=="test":
            text1 = asUnicode(app.Text1.get()).encode('utf-8') ; text2 = asUnicode(app.Text2.get()).encode('utf-8')
            if not text1 and not text2: app.todo.alert=u"Before pressing the "+localise("Speak")+u" button, you need to type the text you want to hear into the box."
            else:
              if text1.startswith(B('#')): msg="" # see below
              else: msg=generalCheck(text1,secondLanguage)
              if msg: app.todo.alert=ensure_unicode(msg)
              else:
                app.set_watch_cursor = 1 ; app.toRestore = []
                global justSynthesize ; justSynthesize = ""
                def doControl(text,lang,control):
                    global justSynthesize ; text=B(text)
                    restoreTo = asUnicode(control.get())
                    if text.startswith(B('#')): justSynthesize = B(justSynthesize)+text # hack for direct control of just_synthesize from the GUI (TODO document it in advanced.txt? NB we also bypass the GUI transliteration in the block below)
                    elif text:
                        if can_be_synthesized(B("!synth:")+text+B("_")+B(lang)):
                            justSynthesize=B(justSynthesize)+(B("#")+B(lang)+B(" ")+B(text))
                        else: app.todo.alert=B("Cannot find a synthesizer that can say '")+text+B("' in language '")+B(lang)+B("' on this system")
                        t=S(transliterates_differently(text,lang))
                        if t: # (don't go straight into len() stuff, it could be None)
                          if unix and len(t)>300 and hasattr(app,"isBigPrint"): app.todo.alert="Transliteration suppressed to work around Ubuntu bug 731424" # https://bugs.launchpad.net/ubuntu/+bug/731424
                          else:
                            control.set(t) ; app.toRestore.append((control,t,restoreTo))
                doControl(text1,secondLanguage,app.Text1)
                def doSynth(openDir=True):
                    gui_outputTo_start() ; just_synthesize() ; gui_outputTo_end(openDir)
                    global justSynthesize ; justSynthesize = ""
                    if app: app.unset_watch_cursor = 1 # otherwise was closed by the close box
                if text1 and text2:
                  if app and hasattr(app,"outputTo") and app.outputTo.get() and not app.outputTo.get()=="0":
                    if getYN("Save %s and %s to separate files?" % (secondLanguage,firstLanguage)): doSynth(False)
                  elif ask_teacherMode: # Do the L2, then ask if actually WANT the L1 as well (might be useful on WinCE etc, search-and-demonstrate-L2)
                    doSynth()
                    if app and not getYN("Also speak the %s?" % firstLanguage):
                      continue
                doControl(text2,firstLanguage,app.Text2)
                doSynth()
        elif menu_response=="mp3web":
          url=[] ; text1 = asUnicode(app.Text1.get())
          for c in list(text1.encode("utf-8")):
            if ord(',')<=ord(c)<=ord('9') or ord('a')<=ord(c.lower())<=ord('z'): url.append(c)
            else: url.append("%"+hex(ord(c))[2:])
          def scanDirs():
           dd={} ; found=0
           for d in downloadsDirs:
            if isDirectory(d):
             found=1
             for f in os.listdir(d): dd[d+os.sep+f]=1
           return dd,found
          oldLs,found = scanDirs()
          if downloadsDirs and not found: app.todo.alert=localise("Please set downloadsDirs in advanced"+dottxt)
          elif not url: app.todo.alert=localise("You need to type a word in the box before you can press this button")
          elif not startBrowser(mp3web.replace("$Word","".join(url)).replace("$Lang",secondLanguage)): app.todo.alert = localise("Can't start the web browser")
          elif downloadsDirs:
            waitOnMessage(localise("If the word is there, download it. When you press OK, Gradint will check for downloads."))
            if not app: break
            found=0
            for f in scanDirs()[0].keys():
              if not checkIn(f,oldLs) and (f.lower().endswith(dotmp3) or f.lower().endswith(dotwav)) and getYN("Use "+f[f.rfind(os.sep)+1:]+"?"): # TODO don't ask this question too many times if there are many and they're all 'no'
                system("mp3gain -r -s r -k -d 10 \""+f+"\"") # (if mp3gain command is available; ignore errors if not (TODO document in advanced.txt)) (note: doing here not after the move, in case synthCache is over ftpfs mount or something)
                uf=scFile=text1.encode("utf-8")+"_"+secondLanguage+f[-4:].lower()
                try:
                  if winCEsound: raise IOError
                  else: o=open(synthCache+os.sep+scFile,"wb")
                except IOError:
                  uf=unicode2filename(text1+"_"+secondLanguage+f[-4:].lower())
                  o=open(synthCache+os.sep+uf,"wb")
                  synthCache_transtbl[scFile]=uf
                  open(synthCache+os.sep+transTbl,'a').write(uf+" "+scFile+"\n")
                synthCache_contents[uf]=1
                o.write(open(f,"rb").read()) ; o.close() ; os.remove(f)
                app.lastText1 = 1 # ensure different
                found=1 ; break
            if not found: app.todo.alert="No new sounds found"
        elif menu_response=="get-encoder":
          if winsound or mingw32:
            assert 0, "Windows Media Encoder no longer available for new installations"
            #if getYN("Gradint can use Windows Media Encoder to make WMA files, which can be played on most pocket MP3 players and mobiles etc.  Do you want to go to the Microsoft site to install Windows Media Encoder now?"):
            #  if not startBrowser('http://www.microsoft.com/windows/windowsmedia/forpros/encoder/default.mspx'): app.todo.alert = "There was a problem starting the web browser.  Please install manually (see notes in advanced.txt)."
            #  else:
            #    app.setLabel("Waiting for you to install Media Encoder")
            #    while not fileExists(programFiles+"\\Windows Media Components\\Encoder\\WMCmd.vbs"): time.sleep(1)
          else:
            if getYN("Do you really want to download and compile the LAME MP3 encoder? (this may take a while)"):
              app.setLabel("Downloading...") ; worked=0
              while True:
                if downloadLAME():
                  worked=1 ; break
                if not getYN("Download failed.  Try again?"): break
              if worked:
                app.setLabel("Compiling...")
                if system("""tar -zxvf lame*.tar.gz && cd lame-* && if ./configure && make; then ln -s $(pwd)/frontend/lame ../lame || true; else cd .. ; rm -rf lame*; exit 1; fi"""):
                    app.todo.alert = "Compile failed"
                    if macsound:
                        app.todo.alert += ". Check the system has Xcode with command-line license accepted (try running gcc from the Terminal)"
                        # might be asked to run: sudo xcodebuild -license
          app.todo.set_main_menu = 1
        elif (menu_response=="add" or menu_response=="replace") and not (app.Text1.get() and app.Text2.get()): app.todo.alert="You need to type text in both boxes before adding the word/meaning pair to "+vocabFile
        elif menu_response=="add" and hasattr(app,"vocabList") and checkIn((asUnicode(app.Text1.get()),asUnicode(app.Text2.get())),app.vocabList):
            # Trying to add a word that's already there - do we interpret this as a progress adjustment?
            app.set_watch_cursor = 1
            t1,t2 = asUnicode(app.Text1.get()),asUnicode(app.Text2.get())
            lang2,lang1=t1.lower(),t2.lower() # because it's .lower()'d in progress.txt
            d = ProgressDatabase(0)
            l1find = S(B("!synth:")+lang1.encode('utf-8')+B("_"+firstLanguage))
            found = 0
            msg=(ensure_unicode(localise("%s=%s is already in %s.")) % (t1,t2,vocabFile))
            for listToCheck in [d.data,d.unavail]:
              if found: break
              for item in listToCheck:
                if (item[1]==l1find or (type(item[1])==type([]) and checkIn(l1find,item[1]))) and item[2]==S(B("!synth:")+lang2.encode('utf-8')+B("_"+secondLanguage)):
                    if not item[0]: break # not done yet - as not-found
                    newItem0 = reviseCount(item[0])
                    app.unset_watch_cursor = 1
                    if getYN(msg+" "+localise("Repeat count is %d. Reduce this to %d for extra revision?" % (item[0],newItem0))):
                        app.set_watch_cursor = 1
                        listToCheck.remove(item)
                        listToCheck.append((newItem0,item[1],item[2]))
                        d.save() ; app.unset_watch_cursor = 1
                        app.todo.clear_text_boxes = 1
                    found = 1 ; break
            if not found:
                app.unset_watch_cursor = 1
                app.todo.alert=msg+" "+localise("Repeat count is 0, so we cannot reduce it for extra revision.")
        elif menu_response=="add":
            text1 = asUnicode(app.Text1.get()).encode('utf-8') ; text2 = asUnicode(app.Text2.get()).encode('utf-8')
            msg=generalCheck(text1,secondLanguage)
            if msg: app.todo.alert=ensure_unicode(msg)
            else:
                o=appendVocabFileInRightLanguages()
                if not o: continue # IOError
                writeB(o,text1+B("=")+text2+B("\n")) # was " = " but it slows down parseSynthVocab
                o.close()
                if paranoid_file_management:
                    if filelen(vocabFile)<filelen(vocabFile+"~") or chr(0) in readB(open(vocabFile,"rb"),1024): app.todo.alert="Vocab file corruption! You'd better restore the ~ backup."
                if hasattr(app,"vocabList"): app.vocabList.append((ensure_unicode(text1),ensure_unicode(text2)))
                app.todo.clear_text_boxes=app.wordsExist=1
        elif menu_response=="delete" or menu_response=="replace":
            app.set_watch_cursor = 1
            lang2,lang1 = app.toDelete
            t1,t2 = asUnicode(app.Text1.get()),asUnicode(app.Text2.get()) # take it now in case the following takes a long time and user tries to change
            if winCEsound: # hack because no watch cursor and can take time
                app.Text1.set("Please wait") ; app.Text2.set("wait...")
            found = delOrReplace(lang2,lang1,t1,t2,menu_response)
            if found and menu_response=="replace": # maybe hack progress.txt as well (taken out of the above loop for better failsafe)
                d = ProgressDatabase(0)
                lang2,lang1=lang2.lower(),lang1.lower() # because it's .lower()'d in progress.txt
                l1find = S(B("!synth:")+lang1.encode('utf-8')+B("_"+firstLanguage))
                for item in d.data:
                    if (item[1]==l1find or (type(item[1])==type([]) and checkIn(l1find,item[1]))) and item[2]==S(B("!synth:")+lang2.encode('utf-8')+B("_"+secondLanguage)) and item[0]:
                        app.unset_watch_cursor = 1
                        if not getYN(localise("You have repeated %s=%s %d times.  Do you want to pretend you already repeated %s=%s %d times?") % (S(lang2),S(lang1),item[0],S(t2),S(t1),item[0])):
                            app.set_watch_cursor = 1 ; break
                        d.data.remove(item)
                        l1replace = S(B("!synth:")+t2.encode('utf-8')+B("_"+firstLanguage))
                        if type(item[1])==type([]):
                            l = item[1]
                            l[l.index(l1find)] = l1replace
                        else: l=l1replace
                        item = (item[0],l,S(B("!synth:")+t1.encode('utf-8')+B("_"+secondLanguage)))
                        d.data.append(item)
                        app.set_watch_cursor = 1
                        for i2 in d.unavail:
                            if i2[1:]==item[1:]:
                                d.unavail.remove(i2) # because we updated the item above - don't want duplicates
                                break
                        d.save()
                        break
            del app.vocabList # re-read
            app.todo.clear_text_boxes=1
            app.unset_watch_cursor = 1
            if not found: app.todo.alert = "OOPS: Item to delete/replace was not found in "+vocabFile

def vocabLinesWithLangs(): # used for merging different users' vocab files
    langs = [secondLanguage,firstLanguage] ; ret = []
    try: v=u8strip(read(vocabFile)).replace(B("\r"),B("\n"))
    except IOError: v=B("")
    for l in v.split(B("\n")):
        l2=l.lower()
        if l2.startswith(B("set language ")) or l2.startswith(B("set languages ")): langs=map(S,l.split()[2:])
        elif l: ret.append((tuple(langs),l)) # TODO what about blank lines? (currently they'd be considered duplicates)
    return ret

def appendVocabFileInRightLanguages():
    # check if we need a SET LANGUAGE
    langs = [secondLanguage,firstLanguage]
    try: v=u8strip(read(vocabFile)).replace(B("\r"),B("\n"))
    except IOError: v=B("")
    for l in v.split(B("\n")):
        l2=l.lower()
        if l2.startswith(B("set language ")) or l2.startswith(B("set languages ")):
            langs=l.split()[2:]
            for i in range(len(langs)): langs[i]=S(langs[i])
    try: o=open(vocabFile,"ab") # (ensure binary on Python 3)
    except IOError:
        show_warning("Cannot write to "+vocabFile+" (current directory is "+os.getcwd()+")")
        return
    if not v.endswith(B("\n")): o.write(B("\n"))
    if not langs==[secondLanguage,firstLanguage]: o.write(B("SET LANGUAGES "+secondLanguage+" "+firstLanguage+"\n"))
    return o

def transliterates_differently(text,lang):
    global last_partials_transliteration ; last_partials_transliteration=None
    global partials_are_sporadic ; o=partials_are_sporadic ; partials_are_sporadic = None # don't want to touch the counters here
    if synthcache_lookup(B("!synth:")+B(text)+B("_")+B(lang)):
        partials_are_sporadic = o
        if last_partials_transliteration and not last_partials_transliteration==text: return last_partials_transliteration
        else: return # (don't try to translit. if was in synth cache - will have no idea which synth did it)
    partials_are_sporadic = o
    synth=get_synth_if_possible(lang,0) # not to_transliterate=True this time because we want the synth that actually synth'd it (may have done it differently from the transliterating synth)
    if not synth or not synth.can_transliterate(lang): return
    translit=synth.transliterate(lang,text,forPartials=0)
    if translit and not translit==text: return translit

def gui_outputTo_start():
    if hasattr(app,"outputTo") and app.outputTo.get() and not app.outputTo.get()=="0":
        global outputFile,gui_output_directory,oldGID ; outputFile=None
        if type(gui_output_directory)==type([]):
            oldGID = gui_output_directory
            for d in gui_output_directory:
                if d and d[-1]=="*" and len(os.listdir(d[:-1]))==1: d=d[:-1]+os.listdir(d[:-1])[0]
                if isDirectory(d):
                    gui_output_directory = d ; break
        if type(gui_output_directory)==type([]): gui_output_directory=gui_output_directory[-1]
        try: os.mkdir(gui_output_directory)
        except: pass
        gui_output_counter = 1 # now local because we also got prefix
        if justSynthesize:
            if B('#') in B(justSynthesize)[1:]: prefix=B("") # multiple languages
            else: # prefix the language that's being synth'd
                prefix=B(justSynthesize).split()[0]
                if prefix.startswith(B('#')): prefix=prefix[1:]
        else: prefix = B("lesson")
        while not outputFile or fileExists(outputFile):
            outputFile=gui_output_directory+os.sep+S(prefix)+str(gui_output_counter)+extsep+app.outputTo.get()
            gui_output_counter += 1
        global write_to_stdout ; write_to_stdout = 0
        global out_type ; out_type = app.outputTo.get()
        global need_run_media_encoder
        if out_type=="wma" or (out_type=="aac" and not (got_program("neroAacEnc") or got_program("faac"))):
            need_run_media_encoder = (out_type,outputFile)
            out_type="wav" ; outputFile=os.tempnam()+dotwav
        else: need_run_media_encoder = 0
        setSoundCollector(SoundCollector())
        global waitBeforeStart, waitBeforeStart_old
        waitBeforeStart_old = waitBeforeStart ; waitBeforeStart = 0
def gui_outputTo_end(openDir=True):
    global outputFile, waitBeforeStart, oldGID, gui_output_directory
    if outputFile:
        no_output = not soundCollector.tell() # probably 'no words to put in the lesson'
        setSoundCollector(None)
        if no_output: os.remove(outputFile)
        elif need_run_media_encoder:
            t,f = need_run_media_encoder
            oldF = f
            if cygwin:
                o=outputFile.replace("/","\\")
                if o.lower().startswith("\\cygdrive\\"): o=o[10]+":"+o[11:] # reverse \cygdrive paths back to DOS (in case used for temp dirs etc)
                if o.startswith("\\"): o="C:\\cygwin"+o # e.g. c:\cygwin\tmp
                f=f.replace("/","\\")
            else: o=outputFile
            if t=="wma":
                pFiles = programFiles
                if cygwin: pFiles=os.environ.get("ProgramFiles","C:\\Program Files") # re-generate it (don't want Cygwin path version)
                # NB we're passing this to cmd, NOT bash:
                cmd = "cscript \""+pFiles+"\\Windows Media Components\\Encoder\\WMCmd.vbs\" -input \""+o+"\" -output \""+f+"\" -profile a20_1 -a_content 1"
            elif t=="aac": cmd="afconvert \""+o+"\" -d aac \""+f+"\"" # could also use "afconvert file.wav -d samr file.amr", but amr is bigger than aac and not as good; don't know if anyone has a device that plays amr but not aac.
            # afconvert default is 64kbit AAC. if want 96+ for music, use -b 96000 after the -d aac (and if want iTunes to be able to accept it, specify extension mp4 instead of aac to afconvert; do not rename aac to mp4, but tell afconvert it's mp4)
            else: assert 0
            if cygwin:
                assert not "'" in cmd, "apostrophes in pathnames could cause trouble on cygwin"
                cmd="echo '"+cmd+" && exit' | cmd" # seems the only way to get it to work on cygwin
            system(cmd)
            os.remove(outputFile)
            if not fileExists(oldF):
                m = "This computer's "+t.upper()+" encoder failed to write any output.  Try a different format."
                if t=="wma": m += " (This condition can be caused by some program changing the registry entries for VBS scripts.)"
                app.todo.alert = m
                no_output = 1
        outputFile=None
        waitBeforeStart = waitBeforeStart_old
        if openDir and not no_output: openDirectory(gui_output_directory)
        try: gui_output_directory = oldGID
        except: pass

def main():
    global useTK,justSynthesize,waitBeforeStart,traceback,appTitle,app,warnings_toprint
    if useTK:
        if justSynthesize and not B(justSynthesize)[-1:]==B('*'): appTitle=cond(B('#') in B(justSynthesize),"Gradint","Reader") # not "language lesson"
        startTk()
    else:
        app = None # not False anymore
        if not appuifw and not android: # REALLY output them to stderr
            for w in warnings_toprint: show_warning(w)
        warnings_toprint = [] ; rest_of_main()
def rest_of_main():
    global useTK,justSynthesize,waitBeforeStart,traceback,appTitle,saveProgress,RM_running
    exitStatus = 0 ; RM_running = 1

    try:
        try: ceLowMemory
        except NameError: ceLowMemory=0
        if ceLowMemory and getYN("Low memory! Python may crash. Turn off progress saving for safety?"): saveProgress=0
        
        if B(justSynthesize)==B("-"): primitive_synthloop()
        elif justSynthesize and B(justSynthesize)[-1:]==B('*'):
            justSynthesize=justSynthesize[:-1]
            waitBeforeStart = 0
            just_synthesize() ; lesson_loop()
        elif justSynthesize: just_synthesize()
        elif app and waitBeforeStart: gui_event_loop()
        elif appuifw: s60_main_menu()
        elif android: android_main_menu()
        else: lesson_loop()
    except SystemExit:
        e = sys.exc_info()[1]
        exitStatus = e.code
    except KeyboardInterrupt: pass
    except PromptException:
        prEx = sys.exc_info()[1]
        waitOnMessage("\nProblem finding prompts:\n"+prEx.message+"\n")
        exitStatus = 1
    except MessageException:
        mEx = sys.exc_info()[1]
        waitOnMessage(mEx.message+"\n") ; exitStatus = 1
    except:
        w="\nSomething has gone wrong with my program.\nThis is not your fault.\nPlease let me know what it says.\nThanks.  Silas\n"+exc_info()
        try: import traceback
        except:
            w += "Cannot import traceback\n"
            traceback = None
        if traceback and useTK: traceback.print_exc() # BEFORE waitOnMessage, in case Tk is stuck (hopefully the terminal is visible)
        try: tracebackFile=open("last-gradint-error"+extsep+"txt","w")
        except: tracebackFile=None
        if tracebackFile:
            try:
                tracebackFile.write(time.asctime()+":\n"+w+"\n")
                if traceback: traceback.print_exc(None,tracebackFile)
                tracebackFile.close()
                if traceback: w += "Details have been written to "+os.getcwd()+os.sep+"last-gradint-error"+extsep+"txt" # do this only if there's a traceback, otherwise little point
            except: pass
        try: # audio warning in case was away from computer.  Do this last as it may overwrite the exception.
            global soundCollector
            if app: soundCollector=0
            if not soundCollector and get_synth_if_possible("en",0): synth_event("en","Error in graddint program.").play() # if possible, give some audio indication of the error (double D to try to force correct pronunciation if not eSpeak, e.g. S60)
        except: pass
        waitOnMessage(w.strip())
        if not useTK:
            if tracebackFile: writeB(sys.stderr,read("last-gradint-error"+extsep+"txt"))
            elif traceback: traceback.print_exc() # will be wrong if there was an error in speaking
        exitStatus = 1
        if appuifw: raw_input() # so traceback stays visible
    # It is not guaranteed that __del__() methods are called for objects that still exist when the interpreter exits.  So:
    global viable_synths,getsynth_cache,theMp3FileCache
    del viable_synths,getsynth_cache,theMp3FileCache
    if app:
        app.todo.exit_ASAP=1
        while app: time.sleep(0.2)
    elif not app==None: pass # (gets here if WAS 'app' but was closed - DON'T output anything to stderr in this case)
    elif appuifw: appuifw.app.set_exit()
    elif riscos_sound: show_info("You may now close this Task Window.\n")
    elif not android:
        try:
            doLabelLastLen ; show_info("\n") # if got any \r'd string there - don't want to confuse the next prompt
        except NameError: pass # no doLabelLastLen - no \r
    RM_running = 0
    if exitStatus: sys.exit(exitStatus)

if __name__=="__main__": main() # Note: calling main() is the ONLY control logic that can happen under the 'if __name__=="__main__"' block; everything else should be in main() itself.  This is because gradint-wrapper.exe under Windows calls main() from the exe and does not call this block

# This file is part of the source code of
# gradint v0.9961 (c) 2002-2010 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# This is the start of system.py - imports library modules, gets directory and extension separators, works out where temporary files go, etc.

macsound = (sys.platform.find("mac")>=0 or sys.platform.find("darwin")>=0)
cygwin = (sys.platform.find("cygwin")>=0)
mingw32 = sys.platform.find("mingw32")>=0
if not macsound and not cygwin and sys.platform.find("win")>=0: import winsound
else: winsound=None
riscos_sound = sys.platform.lower().find("riscos")>=0
try: import olpc # One Laptop Per Child module
except: olpc = 0

try: import appuifw # Symbian S60's GUI module
except: appuifw = 0
if appuifw:
    appuifw.app.body = appuifw.Text()
    appuifw.app.body.add(u""+program_name.replace("(c)","\n(c)")+"\n\nLoading, please wait...\n(Do NOT press OK or Cancel yet!)\n")
    import audio
    appuifw.app.title = u""+appTitle
    appuifw.app.screen='large' # lose Python banner
    import e32,time
    # S60 threads are awkward - callbacks run in a different thread and there's no way to interrupt main().  This is not as responsive as I'd like but it should do:
    def e32sleep(s):
        t=time.time()+s
        while time.time()<t:
            check_for_interrupts()
            e32.ao_sleep(min(1,t-time.time()))
    time.sleep = e32sleep
    def s60_interrupt():
        doLabel("Trying to interrupt main thread, please wait...")
        global need_to_interrupt
        need_to_interrupt = 1
    def s60_briefInt():
        global emergency_lessonHold_to
        if emergency_lessonHold_to:
            emergency_lessonHold_to = 0
            doLabel("Resuming...")
        else:
            emergency_lessonHold_to = time.time() + briefInterruptLength
            doLabel("Preparing to interrupt lesson... (select it again to resume)")
    appuifw.app.menu=[(u"Brief interrupt",s60_briefInt),(u"Cancel lesson",s60_interrupt)]
    appuifw.app.exit_key_handler = s60_interrupt

winCEsound = msvcrt = WMstandard = None
if winsound:
    try: import msvcrt
    except: msvcrt = None # missing
    if hasattr(os,"name") and os.name=="ce": # oops, this "Windows" is Windows CE
        winsound = None ; winCEsound = 1
        import ctypes # if that fails (pre-2.5, pre-Windows Mobile 2003) then we can't do much
        import ctypes.wintypes as wintypes
        class ShellExecuteInfo(ctypes.Structure): _fields_ = [("cbSize",wintypes.DWORD),("fMask",wintypes.ULONG),("hwnd",wintypes.HWND),("Verb",ctypes.c_wchar_p),("File",ctypes.c_wchar_p),("Parameters",ctypes.c_wchar_p),("Directory",ctypes.c_wchar_p),("nShow",ctypes.c_int),("hInstApp",wintypes.HINSTANCE),("IDList",ctypes.c_void_p),("Class",ctypes.c_wchar_p),("hkeyClass",wintypes.HKEY),("dwHotKey",wintypes.DWORD),("hIconOrMonitor",wintypes.HANDLE),("hProcess",wintypes.HANDLE)]
        try: ctypes.cdll.commdlg
        except: WMstandard = True

if macsound and __name__=="__main__": os.system("clear 1>&2") # so warnings etc start with a clear terminal (1>&2 just in case using stdout for something else)
if riscos_sound: sys.stderr.write("Loading Gradint...\n") # in case it takes a while

wsp = '\t\n\x0b\x0c\r ' # whitespace characters - ALWAYS use .strip(wsp) not .strip(), because someone added \xa0 (iso8859-1 no-break space) to string.whitespace on WinCE Python, and that can break processing of un-decoded UTF8 strings, e.g. a Chinese phrase ending "\xe5\x86\xa0"!  (and assign to string.whitespace does not work around this.)
# As .split() can't take alternative characters (and re-writing in Python is probably slow), just be careful with using it on un-decoded utf-8 stuff.  (split(None,1) is ok if 1st word won't end in an affected character)

warnings_printed = [] ; app = None
def show_warning(w):
    if not app and not appuifw:
        if winCEsound and len(w)>100: w=w[:100]+"..." # otherwise can hang winCEsound's console (e.g. a long "assuming that" message from justSynthesize)
        sys.stderr.write(w+"\n")
    warnings_printed.append(w+"\n")

def show_info(i,always_stderr=False):
    # == sys.stderr.write(i) with no \n and no error if closed (+ redirect to app or appuifw if exists)
    if (app or appuifw) and not always_stderr: return doLabel(i)
    if not always_stderr and hasattr(sys.stderr,"isatty") and not sys.stderr.isatty(): return # be quiet if o/p is being captured by cron etc
    if winCEsound and len(i)>101: i=i[:100]+"..."+i[-1] # otherwise can hang winCEsound's console (e.g. a long "Not in cache" message)
    if type(i)==type(u""): i=i.encode('utf-8')
    try: sys.stderr.write(i)
    except IOError: pass

# For pre-2.3 versions of Python (e.g. 2.2 on Symbian S60 and Mac OS 10.3):
try: True
except: exec("True = 1 ; False = 0")
# TODO make sure to avoid writing "string1 in string2" without thinking - if string1 is multiple characters it won't work on pre-2.3
# TODO check all lambda functions for Python2.2 compatibility
# (TODO: GUI_translations, if not set in advanced.txt, won't work properly on pre-2.3 - it'll take them as Latin-1)
# (TODO: and if it *IS* set in advanced.txt, will 2.2's exec() correctly exec a unicode string?)

# Check if we're on big-endian architecture (relevant to sox etc)
try: import struct
except: struct=0
if struct and struct.pack("h",1)[0]=='\x00': big_endian = 1
else: big_endian = 0

# RISC OS has a different extension separator because "." is used as a directory separator (from the original 1982 BBC Micro DFS with 1-character directories)
if hasattr(os,'extsep'): extsep = os.extsep
elif riscos_sound: extsep = "/"
else: extsep = "."
dotwav = extsep+"wav" ; dotmp3 = extsep+"mp3" ; dottxt = extsep+"txt"
# and Python for S60 2.2 appends os.sep to getcwd() and crashes if you add another, so check:
cwd_addSep = os.sep
if os.getcwd()[-1]==os.sep: cwd_addSep = ""

def list2dict(l):
  d = {}
  for i in l: d[i]=True
  return d
try: list2set = set
except NameError: list2set = list2dict

# settings.txt and advanced.txt
# (done here before the variables start to be used in
# defaults, top-level, etc)
# but check we're in the right directory (needed if launched
# via Mac OS Finder)
try:
    import os.path
    fileExists = os.path.isfile
    fileExists_stat = os.path.exists
    isDirectory = os.path.isdir
except: # os.path not included in the libraries - use this slower version:
    def fileExists(f):
        try:
            open(f)
            return 1
        except: return 0
    def fileExists_stat(f):
        try:
            os.stat(f)
            return 1
        except: return 0
    def isDirectory(directory):
        # or a symlink to a directory.  Do it this way to be safe:
        oldDir = os.getcwd()
        try:
            os.chdir(directory)
            ret = 1
        except: ret = 0 # was except OSError but some Python ports have been known to throw other things
        os.chdir(oldDir)
        return ret

use_unicode_filenames = winCEsound # needed to stop synth-cache being ??? (but do NOT use this on winsound, it's too unreliable)
if use_unicode_filenames:
    # pretend we still work in utf-8 for listdir etc (TODO this is not complete, but SampleEvent and PlayerInput will translate to Unicode also)
    oldOsListdir = os.listdir
    def listdir(d): return map(lambda x:x.encode('utf-8'),oldOsListdir(unicode(d,"utf-8")))
    os.listdir = listdir
    oldOsRename = os.rename
    def rename(o,n): return oldOsRename(unicode(o,"utf-8"),unicode(n,"utf-8"))
    os.rename = rename
    oldIsdir = isDirectory
    def isDirectory(d): return oldIsdir(unicode(d,"utf-8"))
    oldFileExistsStat = fileExists_stat
    def fileExists_stat(f): return oldFileExistsStat(unicode(f,"utf-8"))

def u8strip(d):
    global last_u8strip_found_BOM ; last_u8strip_found_BOM = 0
    if d.startswith('\xef\xbb\xbf'):
        last_u8strip_found_BOM = 1
        return d[3:] # ignore Notepad's UTF-8 BOM's
    else: return d
GUI_translations_old = GUI_translations
configFiles = map(lambda x:x+dottxt,["advanced","settings"]) # MUST have settings last so can have per-user override of scriptVariants
if not hasattr(sys,"argv"): sys.argv=" " # some Symbian versions
starting_directory = os.getcwd()
if not fileExists(configFiles[0]):
  if macsound and "_" in os.environ:
    s=os.environ["_"] ; s=s[:s.rfind(os.sep)]
    os.chdir(s)
    if not fileExists(configFiles[0]):
        # try up 1 more level (in case gradint.py has been hidden in start-gradint.app directory on Mac OS)
        s=s[:s.rfind(os.sep)]
        os.chdir(s)
  if not fileExists(configFiles[0]) and sys.argv and (os.sep in sys.argv[0] or (os.sep=='\\' and '/' in sys.argv[0])):
    # try the sys.argv[0] directory, in case THAT works
    if os.sep=="\\" and '/' in sys.argv[0] and fileExists(sys.argv[0].replace('/','\\')): sys.argv[0]=sys.argv[0].replace('/','\\') # hack for some Windows Python builds accepting / in command line but reporting os.sep as \
    os.chdir(starting_directory)
    os.chdir(sys.argv[0][:sys.argv[0].rfind(os.sep)])
  if not fileExists(configFiles[0]):
    # Finally, try the module pathname, in case some other Python program has imported us without changing directory.  Apparently we need to get this from an exception.
    try: raise 0
    except:
      tbObj = sys.exc_info()[2]
      while tbObj and hasattr(tbObj,"tb_next") and tbObj.tb_next: tbObj=tbObj.tb_next
      if tbObj and hasattr(tbObj,"tb_frame") and hasattr(tbObj.tb_frame,"f_code") and hasattr(tbObj.tb_frame.f_code,"co_filename") and os.sep in tbObj.tb_frame.f_code.co_filename:
        os.chdir(starting_directory)
        try: os.chdir(tbObj.tb_frame.f_code.co_filename[:tbObj.tb_frame.f_code.co_filename.rfind(os.sep)])
        except: pass

# directory should be OK by now
if sys.platform.find("ymbian")>-1: sys.path.insert(0,os.getcwd()+os.sep+"lib")
import time,sched,sndhdr,random,math,pprint,codecs

def readSettings(f):
   try: exec(unicode(u8strip(open(f,"rb").read()).replace("\r","\n"),"utf-8")) in globals()
   except: show_warning("Warning: Could not load "+f)
dir1 = list2set(dir()+["dir1","f","last_u8strip_found_BOM"])
for f in configFiles: readSettings(f)
for d in dir():
  if not d in dir1 and eval(d): # (ignore unrecognised options that evaluate false - these might be an OLD unused option with a newer gradint rather than vice versa)
    show_warning("Warning: Unrecognised option in config files: "+d)
del dir1
GUI_translations_old.update(GUI_translations) ; GUI_translations = GUI_translations_old # in case more have been added since advanced.txt last update

def cond(a,b,c):
    if a: return b
    else: return c

unix = not (winsound or mingw32 or riscos_sound or appuifw or winCEsound)
if unix: os.environ["PATH"] = os.environ.get("PATH","/usr/local/bin:/usr/bin:/bin")+cond(macsound,":"+os.getcwd()+"/start-gradint.app:",":")+os.getcwd() # for qtplay and sox, which may be in current directory or may be in start-gradint.app if it's been installed that way, and for lame etc.  Note we're specifying a default PATH because very occasionally it's not set at all when using 'ssh system command' (some versions of DropBear?)

# Any options in the environment?
env=os.environ.get("Gradint_Extra_Options","")
while env.endswith(";"): env=env[:-1]
while env.startswith(";"): env=env[1:]
if env: exec(env)
# and anything on the command line?
if len(sys.argv)>1:
    runInBackground=0 # NOT useTK=0 because there might not be a console on Win/GUI or Mac
    progressFileBackup=logFile=None
    exec(" ".join(sys.argv[1:]))

# Paranoid file management option.  Can't go any earlier than this because must parse advanced.txt first.  At least fileExists should call the new version of open() after this happens.
if paranoid_file_management:
  _old_open = open
  def open(file,mode="r"):
    # For ftpfs etc.  Retry on errno 13 (permission denied), and turn append into a copy.  Otherwise occasionally get vocab.txt truncated.
    if "a" in mode:
        try: dat = open(file,mode.replace("a","r")).read()
        except IOError,err:
            if err.errno==2: dat = "" # no such file or directory
            else: raise
        try: os.rename(file,file+"~") # just in case!
        except: pass
        o=open(file,mode.replace("a","w"))
        o.write(dat)
        return o
    for tries in range(10)+["last"]:
        try: return _old_open(file,mode)
        except IOError,err:
            if tries=="last" or not err.errno==13: raise
            time.sleep(0.5)

# Different extension separators again
if not extsep==".":
    # only do the below if defaults haven't been changed
    if progressFile=="progress.txt": progressFile=progressFile.replace(".",extsep)
    if vocabFile=="vocab.txt": vocabFile=vocabFile.replace(".",extsep)
    if progressFileBackup=="progress.bak": progressFileBackup=progressFileBackup.replace(".",extsep)
    if pickledProgressFile=="progress.bin": pickledProgressFile=pickledProgressFile.replace(".",extsep)
    if logFile=="log.txt": logFile=logFile.replace(".",extsep)
    if userNameFile=="username.txt": userNameFile=userNameFile.replace(".",extsep)
# End of extension-separator stuff

# Check for a script changing progressFile but forgetting to change pickledProgressFile to match
oldDir=None
for p in [progressFile,progressFileBackup,pickledProgressFile]:
    if not p: continue
    if os.sep in p: p=(p[:p.rfind(os.sep)+1],p[p.rfind(os.sep)+1:])
    else: p=("",p)
    if extsep in p[1]: p=(p[0],p[1][:p[1].rfind(extsep)]) # here rather than earlier to cover cases where extsep is in a directory name but not in the filename
    if oldDir==None: oldDir=p
    elif not oldDir==p:
        sys.stderr.write("ERROR: progressFile, progressFileBackup and pickledProgressFile, if not None, must have same directory and major part of filename.  Gradint will not run otherwise.  This sanity-check was added in case some script sets progressFile to something special but forgets to set the others.\n")
        sys.exit(1)

# Check for RISC OS pre-1970 clock problem (actually quite likely if testing on the rpcemu emulator without setting the clock)
if riscos_sound and hex(int(time.time())).find("0xFFFFFFFF")>-1 and not outputFile:
    sys.stderr.write("ERROR: time.time() is not usable - gradint cannot run interactively.\n")
    sys.stderr.write("This error can be caused by the RISC OS clock being at 1900 (the Unix time functions start at 1970).\nClose this task window, set the clock and try again.\n")
    sys.exit()

# Check for WinCE low memory (unless we're a library module in which case it's probably ok - reader etc)
# NB on some systems this has been known to false alarm (can't allocate 15M even when there's 70M+ of program memory ??) so set a flag and ask Y/N later when got Tk
if winCEsound and __name__=="__main__":
  m1=m2=m3=0
  try:
    m1=chr(0)*5000000
    m2=chr(0)*5000000
    m3=chr(0)*5000000
    del m1,m2,m3
  except MemoryError:
    del m1,m2,m3
    ceLowMemory=1

# Check for Mac OS Tk problem
Tk_might_display_wrong_hanzi = wrong_hanzi_message = "" ; forceRadio=0
if macsound:
  try: os.remove("_tkinter.so") # it might be an old patched version for the wrong OS version
  except: pass
  def tkpatch(): # patch Mac OS Tk to the included v8.6 (as v8.4 on OS10.5 has hanzi problem and v8.5 on 10.6 has fontsize problems etc)
    f="/System/Library/Frameworks/Python.framework/Versions/"+sys.version[:3]+"/lib/python"+sys.version[:3]+"/lib-dynload/_tkinter.so"
    if fileExists(f): # we might be able to patch this one up
     if not isDirectory("Frameworks") and fileExists("Frameworks.tbz"): os.system("tar -jxvf Frameworks.tbz && rm Frameworks.tbz && chmod -R +w Frameworks")
     if isDirectory("Frameworks"):
      if not fileExists("_tkinter.so"): open("_tkinter.so","w").write(open(f).read().replace("/System/Library/Frameworks/T","/tmp/gradint-Tk-Frameworks/T").replace("/Versions/8.4/","/Versions/8.6/").replace("/Versions/8.5/","/Versions/8.6/"))
      os.system('ln -fs "$(pwd)/Frameworks" /tmp/gradint-Tk-Frameworks') # must be same length as /System/Library/Frameworks
      sys.path.insert(0,os.getcwd()) ; import _tkinter ; del sys.path[0]
      _tkinter.TK_VERSION = _tkinter.TCL_VERSION = "8.6"
      return True
  if not os.environ.get("VERSIONER_PYTHON_PREFER_32_BIT","no")=="no": # needed at least on 10.6 (so if run from cmd line w/out this setting, don't try this patch)
    if sys.version.startswith("2.3.5"): Tk_might_display_wrong_hanzi="10.4"
    elif sys.version[:5] == "2.5.1": # 10.5
      if not tkpatch(): Tk_might_display_wrong_hanzi="10.5"
    elif sys.version[:5] == "2.6.1": tkpatch() # 10.6 (still has Tk8.5, hanzi ok but other problems)
  if Tk_might_display_wrong_hanzi: wrong_hanzi_message = "NB: In Mac OS "+Tk_might_display_wrong_hanzi+", Chinese\ncan display wrongly here." # so they don't panic when it does

# Handle keeping progress file and temp directories etc if we're running from a live CD
# (and if the live CD has just been copied to the hard disk, look in the old progress file locations also)

def progressFileOK():
    try:
        open(progressFile) ; return 1
    except IOError:
        try:
            open(progressFile,"w") ; os.unlink(progressFile)
            return 1
        except: return 0
if winsound:  # will try these dirs in reverse order:
    tryList = ["C:\\TEMP\\gradint-progress.txt", "C:\\gradint-progress.txt", "C:gradint-progress.txt"]
    if "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ: tryList.append(os.environ["HOMEDRIVE"]+os.environ["HOMEPATH"]+os.sep+"gradint-progress.txt")
elif "HOME" in os.environ: tryList=[os.environ["HOME"]+os.sep+"gradint-progress.txt"]
elif riscos_sound: tryList=["$.gradint-progress/txt"]
else: tryList = []
foundPF = okPF = 0 ; defaultProgFile = progressFile
while not foundPF:
    if fileExists(progressFile):
        foundPF = okPF = progressFile ; break
    elif (not okPF) and progressFileOK(): okPF = progressFile   # (but carry on looking for an existing one)
    if not tryList: break # (NOT elif!)
    progressFile = tryList.pop()
if foundPF: progressFile=foundPF
elif okPF: progressFile=okPF
else: show_warning("WARNING: Could not find a writable directory for progress.txt and temporary files\nExpect problems!")
need_say_where_put_progress = (not progressFile==defaultProgFile)
if need_say_where_put_progress:
    progressFileBackup = progressFile[:-3]+"bak"
    pickledProgressFile = progressFile[:-3]+"bin"
    logFile = None # for now
if winsound or winCEsound or mingw32 or riscos_sound or not hasattr(os,"tempnam"):
    tempnam_no = 0
    if os.sep in progressFile: tmpPrefix=progressFile[:progressFile.rindex(os.sep)+1]+"gradint-tempfile"
    else: tmpPrefix="gradint-tempfile"
    if winCEsound or ((winsound or mingw32) and not os.sep in tmpPrefix and not tmpPrefix.startswith("C:")):
        # put temp files in the current directory, EXCEPT if the current directory contains non-ASCII characters then check C:\TEMP and C:\ first (just in case the non-ASCII characters create problems for command lines etc; gradint *should* be able to cope but it's not possible to test in advance on *everybody's* localised system so best be on the safe side).  TODO check for quotes etc in pathnames too.
        def isAscii():
          for c in os.getcwd():
            if c<' ' or c>chr(127): return False
          return True
        tmpPrefix = None
        if winCEsound or not isAscii():
            # WinCE: If a \Ramdisk has been set up (e.g. with http://www.amv007.narod.ru/Ramdisk_WinCE.zip), try that first.  (Could next try storage card if on WM5+ to save hitting internal flash, but that would be counterproductive on WM2003, and anyway the space in the pathname would be awkward.)
            for t in cond(winCEsound,["\\Ramdisk\\","\\TEMP\\", "\\"],["C:\\TEMP\\", "C:\\"]):
                try:
                    open(t+"gradint-tempfile-test","w")
                    os.unlink(t+"gradint-tempfile-test")
                except: continue
                tmpPrefix = t ; break
        if not tmpPrefix: tmpPrefix = os.getcwd()+os.sep
        tmpPrefix += "gradint-tempfile"
    def tempnam():
        global tempnam_no ; tempnam_no += 1
        return tmpPrefix+str(tempnam_no)
    os.tempnam = os.tmpnam = tempnam

if once_per_day&2 and not hasattr(sys,"_gradint_innerImport"): # run every day
    currentDay = None
    # markerFile logic to avoid 2 background copies etc (can't rely on taskkill beyond WinXP)
    # (however this doesn't protect against uninstall + immediate reinstall)
    markerFile,toDel="background1"+dottxt,"background2"+dottxt
    if fileExists(markerFile): markerFile,toDel=toDel,markerFile
    try: os.remove(toDel)
    except OSError: pass
    open(markerFile,"w").write("(delete this file to make the background process quit on next check)")
    while fileExists(markerFile):
      need1adayMessage = (currentDay == time.localtime()[:3]) # (not 1st run of day, so if the run goes ahead then they quit earlier and we'd better explain why we came back)
      currentDay = time.localtime()[:3]
      if __name__=="__main__": # can do it by importing gradint
        sys._gradint_innerImport = 1
        try:
            try: reload(gradint)
            except NameError: import gradint
            gradint.need1adayMessage = need1adayMessage
            gradint.orig_onceperday = once_per_day
            gradint.main()
        except SystemExit: pass
      elif winsound and fileExists("gradint-wrapper.exe"): # in this setup we can do it by recursively calling gradint-wrapper.exe
        s=" ".join(sys.argv[1:])
        if s: s += ";"
        s += "once_per_day="+str(once_per_day-2)+";need1adayMessage="+str(need1adayMessage)+";orig_onceperday="+str(once_per_day)
        s="gradint-wrapper.exe "+s
        if fileExists_stat("tcl"): os.popen(s).read() # (looks like we're a GUI setup; start /wait will probably pop up an undesirable console if we're not already in one)
        else: os.system("start /wait "+s) # (NB with "start", can't have quotes around 1st part of the program, as XP 'start' will treat it as a title, but if add another title before it then Win9x will fail)
      else:
        show_warning("Not doing once_per_day&2 logic because not running as main program")
        # (DO need to be able to re-init the module - they might change advanced.txt etc)
        break
      time.sleep(3600) # delay 1 hour at a time (in case hibernated, + if quit without lesson come back in an hour) (NB if changing this, change the message below too)
if once_per_day&1 and fileExists(progressFile) and time.localtime(os.stat(progressFile).st_mtime)[:3]==time.localtime()[:3]: sys.exit() # already run today
try: need1adayMessage
except: need1adayMessage=0
try: orig_onceperday
except: orig_onceperday=0

if winsound:
    # check for users putting support files/folders in the desktop shortcuts folder and thinking it's the gradint folder
    # We can't do much about detecting users on non-English Windows who have heeded the warning about moving the "Desktop" folder to the real desktop but then mistook this for the gradint folder when adding flite (but hopefully they'll be using ptts/espeak anyway, and yali has an installer)
    if "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ: dr=os.environ["HOMEDRIVE"]+os.environ["HOMEPATH"]
    else: dr="C:\\Program Files" # as setup.bat (location for gradint on Win95 etc)
    if "USERPROFILE" in os.environ: dr=os.environ["USERPROFILE"]
    if not dr[-1]=="\\": dr += "\\"
    try: dirList = os.listdir(dr+"Desktop\\gradint\\") # trailing \ important, otherwise it can include gradint.zip etc on Desktop
    except: dirList = []
    for d in dirList:
        if not d.endswith(".bat"): show_warning("WARNING: The file or folder '%s'\nwas found in the desktop shortcuts folder,\nwhich is NOT the gradint folder.\nThe gradint folder is: %s\nIf you meant '%s' to be used by gradint,\nplease move it to %s\n" % (d,os.getcwd(),d,os.getcwd()))
elif macsound:
    # Handle Mac upgrades.  Windows upgrades are done by setup.bat, but on the Mac if the Finder unpacks a second gradint.tbz we will be in "Gradint 2.app" (which is why there's a "Gradint 2" script in Contents/MacOS).
    if os.getcwd().endswith("/Gradint 2.app") and fileExists_stat("../Gradint.app"):
       for toKeep in "vocab.txt settings.txt advanced.txt".split():
          if fileExists_stat(toKeep) and fileExists_stat("../Gradint.app/"+toKeep): os.remove(toKeep)
       os.system('cp -fpr * ../Gradint.app/')
       open("deleteme","w")
       os.system('open ../Gradint.app')
       sys.exit(0)
    elif fileExists_stat("../Gradint 2.app/deleteme"):
       import thread ; thread.start_new_thread(lambda *x:(time.sleep(2),os.system('rm -rf "../Gradint 2.app"')),())

def got_program(prog):
    # Test to see if the program 'prog' is on the system, as portable as possible.  NB some Unix 'which' output an error to stdout instead of stderr, so check the result exists.
    return (winsound and fileExists(prog+".exe")) or (unix and fileExists_stat(os.popen("which "+prog+" 2>/dev/null").read().strip(wsp)))

def win2cygwin(path): # convert Windows path to Cygwin path
    if path[1]==":": return "/cygdrive/"+path[0].lower()+path[2:].replace("\\","/")
    else: return path.replace("\\","/") # TODO what if it STARTS with a \ ?
if winsound or mingw32: programFiles = os.environ.get("ProgramFiles","C:\\Program Files")
elif cygwin: programFiles = win2cygwin(os.environ.get("PROGRAMFILES","C:\\Program Files"))

def mysleep(secs):
    # In some Python distributions, time.sleep() will sleep about 1.01% too long.
    # That's not normally a problem for lessons (the scheduler compensates afterwards), but it can be a problem if using gradint for reminders - 1% extra on a 9-hour delay could make a reminder 5 minutes late (this happens on an NSLU2 running Debian Etch for example)
    # Let's work around it by reducing long delays slightly (sched will call sleep again if necessary)
    if secs>60: secs *= 0.95
    if emulated_interruptMain or winCEsound:
        t=time.time()+secs
        while time.time()<t:
            if emulated_interruptMain: check_for_interrupts()
            if winCEsound: ctypes.cdll.coredll.SystemIdleTimerReset()
            time.sleep(max(0,min(1,t-time.time())))
    else: time.sleep(secs)

emulated_interruptMain = (appuifw or winCEsound) # for now (will add 1 if we import thread and find it doesn't have an interrupt_main)
# (OK so the "emulated_interruptMain or winCEsound" will be redundant above, but keep it anyway in case we ever get a real interrupt_main on WinCE)

need_to_interrupt = 0
def check_for_interrupts(): # used on platforms where thread.interrupt_main won't work
    global need_to_interrupt
    if need_to_interrupt:
        need_to_interrupt = 0
        raise KeyboardInterrupt

# If forking, need to do so BEFORE importing any Tk module (we can't even verify Tk exists 1st)
if outputFile or justSynthesize or appuifw or not (winsound or winCEsound or mingw32 or macsound or riscos_sound or cygwin or "DISPLAY" in os.environ): useTK = 0
if useTK and runInBackground and not (winsound or mingw32) and hasattr(os,"fork") and not "gradint_no_fork" in os.environ:
    import fcntl, termios
    if os.fork(): sys.exit()
    os.setpgid(0,0)
    if os.fork(): sys.exit()
    try: tty = os.open("/dev/tty", os.O_RDWR)
    except: tty = None
    if not tty==None:
        fcntl.ioctl(tty, termios.TIOCNOTTY, 0)
        os.close(tty)
    devnull = os.open("/dev/null", os.O_RDWR)
    for fd in range(3): os.dup2(devnull,fd)
else: runInBackground = 0

try: import readline # enable readline editing of raw_input()
except: pass

try: import cPickle as pickle
except:
  try: import pickle
  except: pickle = None
try: import re
except: re = None
try:
    import gc
    gc.disable() # slight speedup (assume gradint won't create reference loops)
except: pass

# make sure unusual locale settings don't make .lower() change utf-8 bytes by mistake:
try:
  import locale
  locale.setlocale(locale.LC_ALL, 'C')
except: pass

# -------------------------------------------------------

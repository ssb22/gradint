#!/usr/bin/env python
# -*- coding: utf-8 -*-

program_name = "gradint v0.99892 (c) 2002-2015 Silas S. Brown. GPL v3+."

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Note: To make Gradint easier to package on all the platforms, all the main parts are in a single Python file.  In development however several different python files are used, which are then concatenated together to make the one file.  Comments indicate the start of the various component files in the main file.

progressFileHeader = "# -*- mode: python -*-\n# Do not add more comments - this file will be overwritten\n"

appTitle = "Language lesson"

import sys,os

if not sys.version_info[0]==2: # oh panic, someone's probably trying to run us on Py3k
    sys.stderr.write("Sorry, Gradint cannot run on Python "+repr(sys.version_info[0])+"\nPlease install a 2.x version of Python (must be 2.2+).\n")
    sys.exit(1)

# --------------------------------------------------------
# This is the start of defaults.py - configuration defaults, automatically extracted from default settings.txt and advanced.txt, so user customisations don't have to be complete (helps with upgrades)
firstLanguage = "en"
secondLanguage = "zh"
otherLanguages = ["cant","ko","jp"]
possible_otherLanguages = ["cant","ko","jp","en","zh"]
otherFirstLanguages = []
prefer_espeak = "en"
sapiVoices = {
}
sapiSpeeds = {
}
macVoices = {
"en":"Emily Daniel Alex Vicki",
"zh":"Ting-Ting",
"cant":"Sin-Ji",
"jp":"Kyoko",
}
ekho_speed_delta = 0
extra_speech = []
extra_speech_tofile = []
synthCache = ""
synthCache_test_mode = 0
justSynthesize = ""
lily_file = "C:\\Program Files\\NeoSpeech\\Lily16\\data-common\\userdict\\userdict_chi.csv"
ptts_program = None
partialsDirectory = "partials"
betweenPhrasePause = 0.3
partials_are_sporadic = 0
voiceOption = ""
max_extra_buttons = 12
mp3web = ""
mp3webName = ""
downloadsDirs = ["../Downloads","..\\Desktop"]
outputFile = ""
compress_SH = False
outputFile_appendSilence = 0
if outputFile.endswith("cdr"): outputFile_appendSilence = 5
beepThreshold = 20
startAnnouncement = None
endAnnouncement = None
commentsToAdd = None
orderlessCommentsToAdd = None
maxLenOfLesson = 30*60
saveProgress = 1
ask_teacherMode = 0
maxNewWords = 5
maxReviseBeforeNewWords = 3
newInitialNumToTry = 5
recentInitialNumToTry = 3
newWordsTryAtLeast = 3
knownThreshold = 5
reallyKnownThreshold = 10
meaningTestThreshold = 20
randomDropThreshold = 14
randomDropLevel = 0.67
randomDropThreshold2 = 35
randomDropLevel2 = 0.97
shuffleConstant = 2.0
transitionPromptThreshold = 10
advancedPromptThreshold = 20
transitionPromptThreshold2 = 2
advancedPromptThreshold2 = 5
limit_words = max(1,int(maxNewWords * 0.4))
logFile = "log.txt"
briefInterruptLength = 10
vocabFile = "vocab.txt"
samplesDirectory = "samples"
promptsDirectory = "samples"+os.sep+"prompts"
progressFile = "progress.txt"
progressFileBackup = "progress.bak"
pickledProgressFile = "progress.bin"
gui_output_directory = "output"
limit_filename = "!limit"
intro_filename = "_intro"
poetry_filename = "!poetry"
variants_filename = "!variants"
exclude_from_scan = "_disabled"
exclude_from_coverage = "z_try_again"
userNameFile="username.txt"
import_recordings_from = [r"\My Documents", r"\Storage Card\My Documents", r"\Ramdisk\My Documents"]
GUI_translations={
"@variants-zh":[u"简体字",u"繁體字"],
"Word in %s":{"zh":u"%s"},
"Meaning in %s":{"zh":u"%s意思"},
"en":{"zh":u"英文"},
"zh":{"zh":u"中文"},
"Your first language":{"zh":u"母语","zh2":u"母語"},
"second":{"zh":u"学习的语言","zh2":u"學習的語言"},
"Change languages":{"zh":u"选择其他语言","zh2":u"選擇其他語言"},
"Cancel lesson":{"zh":u"退出"},
"Cancel selection":{"zh":u"取消"},
"Clear input boxes":{"zh":u"取消"},
"Manage word list":{"zh":u"管理词汇表","zh2":u"管理詞彙表"},
"Create word list":{"zh":u"创造词汇表","zh2":u"創造詞彙表"},
"words in":{"zh":u"词, 用","zh2":u"詞, 用"},
"new words in":{"zh":u"新词, 用","zh2":u"新詞, 用"},
"mins":{"zh":u"分钟","zh2":u"分鐘"},
"Start lesson":{"zh":u"开始","zh2":u"開始"},
"Quit":{"zh":u"关闭","zh2":"關閉"},
"Back to main menu":{"zh":u"回主选单","zh2":u"回主選單"},
"Delete non-hanzi":{"zh":u"除字非汉字","zh2":u"除字非漢字"},
"Speak":{"zh":u"发音","zh2":u"發音"},
"Add to %s":{"zh":u"添加到%s"},
"vocab.txt":{"zh":u"词汇表","zh2":u"詞彙表"},
"Recorded words":{"zh":u"录音词汇","zh2":u"錄音詞彙"},
"To":{"zh":u"转到","zh2":"轉到"},
"Make":{"zh":u"做"},
"Speaker":{"zh":u"扬声器","zh2":u"揚聲器"},
"Change or delete item":{"zh":u"更换/删除","zh2":u"更換/刪除"},
"You have not changed the test boxes.  Do you want to delete %s?":{"zh":u"你还没编辑了。你想删除%s吗?","zh2":u"你還沒編輯了。你想刪除%s嗎?"},
"Restore":{"zh":u"归还","zh2":u"歸還"},
"Hear this lesson again?":{"zh":u"再次听那个课吗?","zh2":u"再次聽那個課嗎?"},
"Start this lesson again?":{"zh":u"再次开始这个课吗?","zh2":u"再次開始這個課嗎?"},
"You have %d words in your collection":{"zh":u"你的汇编有%d词","zh2":u"你的彙編有%d詞"},
"%d new words + %d old words":{"zh":u"%d新词而%d旧词","zh2":u"%d新詞而%d舊詞"},
"minutes":{"zh":u"分钟","zh2":u"分鐘"},
"seconds":{"zh":u"秒"},
"Today's lesson teaches %d new words\nand revises %d old words\n\nPlaying time: %d %s %d %s":{"zh":u"今天我们学%d新词而复习%d旧词\n需要%d%s%d%s","zh2":u"今天我們學%d新詞而複習%d舊詞\n需要%d%s%d%s"},
"Today we will learn %d words\nThis will require %d %s %d %s\nFollow the spoken instructions carefully":{"zh":u"今天我们学%d新词, 需要%d%s%d%s\n请仔细听从口头指示","zh2":u"今天我們學%d新詞, 需要%d%s%d%s\n請仔細聽從口頭指示"},
"Family mode (multiple user)":{"zh":u"加别的学生(家人等)","zh2":u"加別的學生(家人等)"},
"Add new name":{"zh":u"加名字"},
"Students":{"zh":u"学生","zh2":u"學生"},
"Brief interrupt":{"zh":u"短时暂停","zh2":"短時暫停"},
"Resume":{"zh":u"恢复","zh2":u"恢復"},
"Emergency brief interrupt":{"zh":u"紧急的短打岔","zh2":u"緊急的短打岔"},
"Resuming...":{"zh":u"正在恢复...","zh2":u"正在恢復..."},
"Big print":{"zh":u"大号字体","zh2":u"大號字體"},
"Compressing, please wait":{"zh":u"正在压缩...","zh2":u"正在壓縮..."},
"All recordings have been compressed to MP3.  Do you also want to make a ZIP file for sending as email?":{"zh":u"所有录音都压缩成为MP3了。 你也想做一个ZIP文件所以能随email附上吗?","zh2":u"所有錄音都壓縮成為MP3了。 你也想做一個ZIP文件所以能隨email附上嗎?"},
"Compress all":{"zh":u"压缩这些文件","zh2":u"壓縮這些文件"},
"Play":{"zh":u"播放"},
"Synthesize":{"zh":u"用机器声音","zh2":u"用機器聲音"},
"(synth'd)":{"zh":u"(机器声音)","zh2":u"(機器聲音)"},
"Re-record":{"zh":u"重新录音","zh2":u"重新錄音"},
"(empty)":{"zh":u"(空白)"},
"Record":{"zh":u"录音","zh2":u"錄音"},
"Add more words":{"zh":u"添加词汇","zh2":u"添加詞彙"},
"New folder":{"zh":u"新文件夹","zh2":"新文件夾"},
"Stop":{"zh":u"停止"},
"Action of spacebar during recording":{"zh":u"空格键在录音的时候的功能","zh2":u"空格鍵在錄音的時候的功能"},
"move down":{"zh":u"进步下面"},
"move along":{"zh":u"进步右边","zh2":u"進步右邊"},
"stop":{"zh":u"停止"},
"(Up)":{"zh":u"(返回)"},
"Record from %s":{"zh":u"从%s做录音","zh2":u"從%s做錄音"},
"Record from file":{"zh":u"切已录音的文件","zh2":u"切已錄音的文件"},
"It has been %d days since your last Gradint lesson.  Please try to have one every day.":{"zh":u"你没做Gradint的课%d天了。请试试天天做。","zh2":u"你沒做Gradint的課%d天了。請試試天天做。"},
"It has been %d days since you installed Gradint and you haven't had a lesson yet.  Please try to have one every day.":{"zh":u"%d天前安装了Gradint但还没做课。请试试天天做。","zh2":u"%d天前安裝了Gradint但還沒做課。請試試天天做。"},
"Error: maximum number of new words must be an integer":{"zh":u"误差: 新词界限不是整数","zh2":u"誤差: 新詞界限不是整數"},
"Error: minutes must be a number":{"zh":u"误差: 分钟界限不是号码","zh2":"誤差: 分鐘界限不是號碼"},
"%s new words is a lot to remember at once.  Reduce to 5?":{"zh":u"一天记得%s新词是很多。我减少到5好吗?","zh2":"一天記得%s新詞是很多。我減少到5好嗎?"},
"More than 30 minutes is rarely more helpful.  Reduce to 30?":{"zh":u"超过30分钟很少有帮助。我减少到30好吗?","zh2":"超過30分鐘很少有幫助。我減少到30好嗎?"},
"Less than 20 minutes can be a rush.  Increase to 20?":{"zh":u"缺乏20分钟可以太赶紧了。我增长到20好吗?","zh2":"缺乏20分鐘可以太趕緊了。我增長到20好嗎?"},
"Proceed anyway?":{"zh":u"反正继续?","zh2":"反正繼續"},
    }
scriptVariants = {}
GUI_languages = { "cant":"zh", "zhy":"zh", "zh-yue":"zh" }
GUI_for_editing_only = 0
GUI_omit_settings = 0
GUI_omit_statusline = 0
GUI_always_big_print = 0
recorderMode = 0
runInBackground = 0
useTK = 1
waitBeforeStart = 1
startFunction = None
oss_sound_device = ""
soundVolume = 1
wavPlayer = ""
mp3Player = ""
saveLesson = ""
loadLesson = 0
justSaveLesson = 0
compress_progress_file = 0
paranoid_file_management = 0
once_per_day = 0
disable_once_per_day = 0

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

try: import androidhelper as android
except:
  try: import android
  except: android = 0
if android: android = android.Android()

wsp = '\t\n\x0b\x0c\r ' # whitespace characters - ALWAYS use .strip(wsp) not .strip(), because someone added \xa0 (iso8859-1 no-break space) to string.whitespace on WinCE Python, and that can break processing of un-decoded UTF8 strings, e.g. a Chinese phrase ending "\xe5\x86\xa0"!  (and assign to string.whitespace does not work around this.)
# As .split() can't take alternative characters (and re-writing in Python is probably slow), just be careful with using it on un-decoded utf-8 stuff.  (split(None,1) is ok if 1st word won't end in an affected character)

warnings_printed = [] ; app = False # False is a hack for "maybe later"
warnings_toprint = []
def show_warning(w):
    if not app and not app==False and not appuifw and not android:
        if winCEsound and len(w)>100: w=w[:100]+"..." # otherwise can hang winCEsound's console (e.g. a long "assuming that" message from justSynthesize)
        sys.stderr.write(w+"\n")
    warnings_printed.append(w+"\n")
    if app==False: warnings_toprint.append(w) # may need to output them if app/appuifw/android turns out not to be created

def show_info(i,always_stderr=False):
    # == sys.stderr.write(i) with no \n and no error if closed (+ redirect to app or appuifw if exists)
    if (app or appuifw or android) and not always_stderr: return doLabel(i)
    if not riscos_sound and not always_stderr and hasattr(sys.stderr,"isatty") and not sys.stderr.isatty(): return # be quiet if o/p is being captured by cron etc (but isatty() might always return false on RISC OS
    if winCEsound and len(i)>101: i=i[:100]+"..."+i[-1] # otherwise can hang winCEsound's console
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
    if os.sep=="\\" and '/' in sys.argv[0] and fileExists(sys.argv[0].replace('/','\\')): sys.argv[0]=sys.argv[0].replace('/','\\') # hack for some Windows Python builds accepting slash in command line but reporting os.sep as backslash
    os.chdir(starting_directory)
    os.chdir(sys.argv[0][:sys.argv[0].rfind(os.sep)])
  if not fileExists(configFiles[0]): # argv[0] might be a symlink
    os.chdir(starting_directory)
    try: rp = os.path.realpath(sys.argv[0])
    except: rp = 0 # e.g. no os.path, or no os.path.realpath
    if rp: os.chdir(rp[:rp.rfind(os.sep)])
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

def exc_info(inGradint=True):
    import sys # in case it's been gc'd
    w = str(sys.exc_info()[0])
    if "'" in w: w=w[w.index("'")+1:w.rindex("'")]
    if '.' in w: w=w[w.index(".")+1:]
    if sys.exc_info()[1]: w += (": "+str(sys.exc_info()[1]))
    tbObj = sys.exc_info()[2]
    while tbObj and hasattr(tbObj,"tb_next") and tbObj.tb_next: tbObj=tbObj.tb_next
    if tbObj and hasattr(tbObj,"tb_lineno"): w += (" at line "+str(tbObj.tb_lineno))
    if inGradint:
        if tbObj and hasattr(tbObj,"tb_frame") and hasattr(tbObj.tb_frame,"f_code") and hasattr(tbObj.tb_frame.f_code,"co_filename") and not tbObj.tb_frame.f_code.co_filename.find("gradint"+extsep+"py")>=0: w += (" in "+tbObj.tb_frame.f_code.co_filename+"\n")
        else: w += (" in "+program_name[:program_name.index("(c)")]+"\n")
    del tbObj
    return w

def read(fname): return open(fname,"rb").read()
def write(fname,data): open(fname,"wb").write(data)
def readSettings(f):
   try: fdat = u8strip(read(f)).replace("\r","\n")
   except: return show_warning("Warning: Could not load "+f)
   try: fdat = unicode(fdat,"utf-8")
   except: return show_warning("Problem decoding utf-8 in "+f)
   try: exec(fdat) in globals()
   except: show_warning("Error in "+f+" ("+exc_info(False)+")")
synth_priorities = "eSpeak MacOS SAPI Ekho" # old advanced.txt had this instead of prefer_espeak; we can still support it
dir1 = list2set(dir()+["dir1","f","last_u8strip_found_BOM"])
for f in configFiles: readSettings(f)
for d in dir():
  if not d in dir1 and eval(d) and not type(eval(d))==type(lambda *args:0): # (ignore unrecognised options that evaluate false - these might be an OLD unused option with a newer gradint rather than vice versa; also ignore functions as these could be used in command-line parameters)
    show_warning("Warning: Unrecognised option in config files: "+d)
del dir1
GUI_translations_old.update(GUI_translations) ; GUI_translations = GUI_translations_old # in case more have been added since advanced.txt last update

def cond(a,b,c):
    if a: return b
    else: return c

unix = not (winsound or mingw32 or riscos_sound or appuifw or android or winCEsound)
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

# Paranoid file management option.  Can't go any earlier than this because must parse advanced.txt first.
if paranoid_file_management:
  # For ftpfs etc.  Retry on errno 13 (permission denied), and turn append into a copy.  Otherwise occasionally get vocab.txt truncated.
  _old_open = open
  def tryIO(func):
    for tries in range(10)+["last"]:
        try: return func()
        except IOError,err:
            if tries=="last" or not err.errno in [5,13,None]: raise
            time.sleep(0.5)
  def read(file): return tryIO(lambda x=file:_old_open(x,"rb").read())
  def _write(fn,data):
    tryIO(lambda x=fn,y=data:_old_open(x,"wb").write(data))
    time.sleep(0.5)
    if not filelen(fn)==len(data):
      # might be a version of curlftpfs that can't shorten files - try delete and restart (although this can erase permissions info)
      os.remove(fn)
      tryIO(lambda x=fn,y=data:_old_open(x,"wb").write(data))
      if not filelen(fn)==len(data): raise IOError("wrong length")
    if not read(fn)==data: raise IOError("verification failure on "+repr(fn))
  def write(fn,data): return tryIO(lambda x=fn,y=data:_write(x,data))
  def open(file,mode="r",forAppend=0):
    if "a" in mode:
        try: dat = open(file,"rb").read()
        except IOError,err:
            if err.errno==2: dat = "" # no such file or directory
            else: raise
        if len(dat) < filelen(file): raise IOError("short read")
        try: os.rename(file,file+"~") # just in case!
        except: pass
        o=open(file,"wb",1)
        o.write(dat)
        return o
    r=tryIO(lambda x=file,m=mode:_old_open(x,m))
    if "w" in mode and not forAppend and filelen(file): # it's not truncating (see _write above)
        r.close()
        os.unlink(file)
        r=tryIO(lambda x=file,m=mode:_old_open(x,m))
    return r

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
if riscos_sound and hex(int(time.time())).find("0xFFFFFFFF")>=0 and not outputFile:
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
      if not fileExists("_tkinter.so"): open("_tkinter.so","w").write(read(f).replace("/System/Library/Frameworks/T","/tmp/gradint-Tk-Frameworks/T").replace("/Versions/8.4/","/Versions/8.6/").replace("/Versions/8.5/","/Versions/8.6/"))
      os.system('ln -fs "$(pwd)/Frameworks" /tmp/gradint-Tk-Frameworks') # must be same length as /System/Library/Frameworks
      sys.path.insert(0,os.getcwd()) ; import _tkinter ; del sys.path[0]
      _tkinter.TK_VERSION = _tkinter.TCL_VERSION = "8.6"
      return True
  if not os.environ.get("VERSIONER_PYTHON_PREFER_32_BIT","no")=="no": # needed at least on 10.6 (so if run from cmd line w/out this setting, don't try this patch)
    if sys.version.startswith("2.3.5"): Tk_might_display_wrong_hanzi="10.4"
    elif sys.version[:5] == "2.5.1": # 10.5
      if not tkpatch(): Tk_might_display_wrong_hanzi="10.5"
    elif sys.version[:5] == "2.6.1": tkpatch() # 10.6 (still has Tk8.5, hanzi ok but other problems)
    elif sys.version[:5] == "2.7.5": tkpatch() # 10.9 (problems with "big print" button if don't do this).  TODO: import platform and check platform.mac_ver()[0].startswith('10.9') first? as future releases might now have same Python version and we haven't tested them against this patch; also check 10.8 isn't Python 2.7.5 (10.7 is 2.7.1)
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
tempdir_is_curdir = False
if winsound or winCEsound or mingw32 or riscos_sound or not hasattr(os,"tempnam") or android:
    tempnam_no = 0
    if os.sep in progressFile: tmpPrefix=progressFile[:progressFile.rindex(os.sep)+1]+"gradint-tempfile"
    else: tmpPrefix,tempdir_is_curdir="gradint-tempfile",True
    if winCEsound or ((winsound or mingw32) and not os.sep in tmpPrefix and not tmpPrefix.startswith("C:")):
        # put temp files in the current directory, EXCEPT if the current directory contains non-ASCII characters then check C:\TEMP and C:\ first (just in case the non-ASCII characters create problems for command lines etc; gradint *should* be able to cope but it's not possible to test in advance on *everybody's* localised system so best be on the safe side).  TODO check for quotes etc in pathnames too.
        def isAscii():
          for c in os.getcwd():
            if c<' ' or c>chr(127): return False
          return True
        tmpPrefix = None
        if winCEsound or not isAscii():
            # WinCE: If a \Ramdisk has been set up, try that first.  (Could next try storage card if on WM5+ to save hitting internal flash, but that would be counterproductive on WM2003, and anyway the space in the pathname would be awkward.)
            for t in cond(winCEsound,["\\Ramdisk\\","\\TEMP\\", "\\"],["C:\\TEMP\\", "C:\\"]):
                try:
                    open(t+"gradint-tempfile-test","w")
                    os.unlink(t+"gradint-tempfile-test")
                except: continue
                tmpPrefix,tempdir_is_curdir = t,False ; break
        if not tmpPrefix: tmpPrefix = os.getcwd()+os.sep
        tmpPrefix += "gradint-tempfile"
    def tempnam():
        global tempnam_no ; tempnam_no += 1
        return tmpPrefix+str(tempnam_no)
    os.tempnam = os.tmpnam = tempnam

if disable_once_per_day==1:
  if once_per_day==3: sys.exit()
  else: once_per_day=0
if once_per_day&2 and not hasattr(sys,"_gradint_innerImport"): # run every day
    currentDay = None
    # markerFile logic to avoid 2+ background copies (can't rely on taskkill beyond WinXP)
    myID = str(time.time())
    try: myID += str(os.getpid())
    except: pass
    markerFile="background"+dottxt
    open(markerFile,"w").write(myID)
    def reador0(f):
        try: return read(f)
        except: return 0
    while reador0(markerFile)==myID:
     if not currentDay == time.localtime()[:3]: # first run of day
      currentDay = time.localtime()[:3]
      if __name__=="__main__": # can do it by importing gradint
        sys._gradint_innerImport = 1
        try: reload(gradint)
        except NameError: import gradint
        gradint.orig_onceperday = once_per_day
        try: gradint.main()
        except SystemExit: pass
      elif winsound and fileExists("gradint-wrapper.exe"): # in this setup we can do it by recursively calling gradint-wrapper.exe
        s=" ".join(sys.argv[1:])
        if s: s += ";"
        s += "once_per_day="+str(once_per_day-2)+";orig_onceperday="+str(once_per_day)
        s="gradint-wrapper.exe "+s
        if fileExists_stat("tcl"): os.popen(s).read() # (looks like we're a GUI setup; start /wait will probably pop up an undesirable console if we're not already in one)
        else: os.system("start /wait "+s) # (NB with "start", can't have quotes around 1st part of the program, as XP 'start' will treat it as a title, but if add another title before it then Win9x will fail)
      else:
        show_warning("Not doing once_per_day&2 logic because not running as main program")
        # (DO need to be able to re-init the module - they might change advanced.txt etc)
        break
      if len(sys.argv)>1: sys.argv.append(";")
      sys.argv.append("disable_once_per_day=0") # don't let a disable_once_per_day=2 in argv result in repeated questioning
     time.sleep(3600) # delay 1 hour at a time (in case hibernated)
if once_per_day&1 and fileExists(progressFile) and time.localtime(os.stat(progressFile).st_mtime)[:3]==time.localtime()[:3]: sys.exit() # already run today
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
    if winsound:
        return fileExists(prog+".exe")
    elif unix:
        try:
            import distutils.spawn
            if ":." in ":"+os.environ.get("PATH",""):
                prog = distutils.spawn.find_executable(prog)
            else: # at least some distutils assume that . is in the PATH even when it isn't, so
                oldCwd = os.getcwd()
                pList = os.environ.get("PATH","").split(':')
                if pList:
                  done=0
                  for p in pList:
                    try: os.chdir(p)
                    except: continue
                    done=1 ; break
                  if done:
                    prog = distutils.spawn.find_executable(prog)
                    os.chdir(oldCwd)
        except ImportError:
            # fall back to running 'which' in a shell (probably slower if got_program is called repeatedly)
            prog = os.popen("which "+prog+" 2>/dev/null").read().strip(wsp)
            if not fileExists_stat(prog): prog=None # some Unix 'which' output an error to stdout instead of stderr, so check the result exists
        return prog

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
    if os.fork(): sys.exit()
    os.setsid()
    if os.fork(): sys.exit()
    devnull = os.open("/dev/null", os.O_RDWR)
    for fd in range(3): os.dup2(devnull,fd)
else: runInBackground = 0

try: import readline # enable readline editing of raw_input()
except: readline=0

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
if not '\xc4'.lower()=='\xc4': # buggy setlocale (e.g. S60) can create portability issues with progress files
  lTrans="".join([chr(c) for c in range(ord('A'))]+[chr(c) for c in range(ord('a'),ord('z')+1)]+[chr(c) for c in range(ord('Z')+1,256)])
  def lower(s): return s.translate(lTrans) # (may crash if Unicode)
else:
  def lower(s): return s.lower()

# -------------------------------------------------------

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
            if self.didScan and maxNewWords: f.write("# collection=%d done=%d left=%d lessonsLeft=%d\n" % (len(self.data),len(data),len(self.data)-len(data),(len(self.data)-len(data)+maxNewWords-1)/maxNewWords))
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
    if zf>=0:
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
        disable_lid(0)
        try:
          # make the runner as late as possible
          if soundCollector: runner = sched.scheduler(collector_time,collector_sleep)
          else: runner = sched.scheduler(time.time,mysleep)
          for (t,event) in self.events: copy_of_runner_events.append((event,runner.enter(t,1,play,(event,)),t))
          # TODO what if Brief Interrupt appears during that events loop and someone presses it (will act as a Cancel and go back to main)
          try: runner.run()
          except KeyboardInterrupt: handleInterrupt()
        finally: disable_lid(1)
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
                    if (re and re.search(str,cache_fname)) or cache_fname.find(str)>=0:
                        found=1 ; break
                if found: continue
            lang = languageof(cache_fname)
            if get_synth_if_possible(lang) and decide_subst_synth(cache_fname): events[i] = (events[i][0],synth_event(lang,cache_fname[:cache_fname.rindex("_")]))

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
    def makesSenseToLog(self): return not self.file.startswith(promptsDirectory) # (NB "not prompts" doesn't necessarily mean it'll be a sample - may be a customised additional comment)
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
    o = open(fname) ; i = -1
    while i==-1:
      head=o.read(512)
      if len(head)==0: raise IndexError # read the whole file and not found a \xFF byte??
      i=head.find('\xFF')
    if i+2 < len(head): head += o.read(3)
    o.close()
    b=ord(head[i+1])
    layer = 4-((b&6)>>1)
    if b&24 == 24: # bits are 11 - MPEG version is 1
      column = layer-1 # MPEG 1 layer 1, 2 or 3
    elif layer==1: column = 3 # MPEG 2+ layer 1
    else: column = 4 # MPEG 2+ layer 2+
    bitrate = br_tab[ord(head[i+2])>>4][column]
    if bitrate==0: bitrate=48 # reasonable guess for speech
    return filelen(fname)*8.0/(bitrate*1000)
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
        elif out_type=="ogg": self.o=os.popen("oggenc -o \"%s\" -r -C 1 -q 0 -" % (cond(write_to_stdout,"-",outputFile),),"wb") # oggenc assumes little-endian, which is what we're going to give it
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
    elif madplay_path or got_program("mpg123"):
        oldDir = os.getcwd()
        if madplay_path: d=os.popen(madplay_path+cond(compress_SH," -R 16000 -b 8","")+" -q \""+changeToDirOf(file)+"\" -o wav:-","rb").read()
        else: d=os.popen("mpg123 -q -w - \""+changeToDirOf(file)+"\"","rb").read()
        os.chdir(oldDir)
        # fix length (especially if it's mpg123)
        wavLen = len(d)-8 ; datLen = wavLen-36 # assumes no other chunks
        if datLen<0: raise IOError("decode_mp3 got bad wav") # better than ValueError for the chr() in the following line
        return d[:4] + chr(wavLen&0xFF)+chr((wavLen>>8)&0xFF)+chr((wavLen>>16)&0xFF)+chr(wavLen>>24) + d[8:40] + chr(datLen&0xFF)+chr((datLen>>8)&0xFF)+chr((datLen>>16)&0xFF)+chr(datLen>>24) + d[44:]
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
    if unix and out_type in ["ogg","mp3"] and os.uname()[4].startswith("arm"): show_warning("Note: On armel, compile lame or oggenc with -fno-finite-math-only, or use lame -b 64 (or higher).  See http://martinwguy.co.uk/martin/debian/no-finite-math-only")
if not (soundCollector and out_type=="sh"): compress_SH = False # regardless of its initial setting (because it's used outside ShSoundCollector)
def collector_time(): return soundCollector.tell()
def collector_sleep(s): soundCollector.addSilence(s)

##########################################################

# Start of synth.py - drive various speech synthesizers

def quickGuess(letters,lettersPerSec): return math.ceil(letters*1.0/lettersPerSec)

class Synth(object):
    # Subclasses need to re-implement these:
    def supports_language(self,lang): return 0
    def not_so_good_at(self,lang): return 0
    def works_on_this_platform(self): return 0
    # def guess_length(self,lang,text) - MUST define this.
    # OPTIONAL def play(self,lang,text) play in realtime, returns a non-(False,0,None) value on error
    # OPTIONAL def makefile(self,lang,text) return unique filename (doesn't have to be ready yet) + finish_makefile(self) (ensure all files ready (may get more synth requests later))
    # (at least one of the above must be defined; if don't define the second then can't use this synth offline)
    # Remember to include it in all_synth_classes below
    ################## don't have to re-implement below
    def __init__(self): self.fileCache = {}
    def __del__(self):
        import os # as it might already have been gc'd
        for v in self.fileCache.values():
            try: os.remove(v)
            except: pass # someone may have removed it already, e.g. cache-synth.py's renaming
        self.fileCache = {} # essential for the globalEspeakSynth hack (or get crash when try to make multiple lessons to file)
    def makefile_cached(self,lang,text):
        if type(text)==type([]): textKey=repr(text)
        else: textKey=text
        if (lang,textKey) in self.fileCache: return self.fileCache[(lang,textKey)]
        t = self.makefile(lang,text)
        self.fileCache[(lang,textKey)] = t
        return t
    def finish_makefile(self): pass
    def transliterate(self,lang,text,forPartials=1): return None # could return a transliteration for the GUI if you want (forPartials is 1 if the translit. is for synth from partials, 0 if is for GUI - may not translit. quite so aggressively in the latter case - but NB if partials are used then the GUI will show them instead of calling with 0)
    def can_transliterate(self,lang): return 0

try:
    import warnings
    warnings.filterwarnings("ignore","tempnam is a potential security risk to your program")
except ImportError: pass

def unzip_and_delete(f,specificFiles="",ignore_fail=0):
    if ignore_fail:
        # we had better at least check that the unzip command exists
        if not got_program("unzip"):
            show_warning("Please unzip "+f+" (Gradint cannot unzip it for you as there's no 'unzip' program on this system)")
            return 1
    show_info("Attempting to extract %s, please wait\n" % (f,))
    if os.system("unzip -uo "+f+" "+specificFiles) and not ignore_fail:
        show_warning("Warning: Failed to unzip "+f)
        return 0
    else:
        # unzip seemed to work
        os.remove(f)
        show_info(f+" unpacked successfully\n")
        return 1

class OSXSynth_Say(Synth):
    def __init__(self): Synth.__init__(self)
    def works_on_this_platform(self):
        if not (macsound and fileExists("/usr/bin/say")): return False
        global osxSayVoicesScan
        try: osxSayVoicesScan # singleton
        except: osxSayVoicesScan = self.scanVoices()
        self.voices = osxSayVoicesScan ; return True
    def supports_language(self,lang): return lang in self.voices
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("say %s\"%s\"" % (self.voices[lang],self.transliterate(lang,text).replace('"','')))
    # TODO 10.7+ may also support -r rate (WPM), make that configurable in advanced.txt ?
    def makefile(self,lang,text):
        fname = os.tempnam()+extsep+"aiff"
        system("say %s-o %s \"%s\"" % (self.voices[lang],fname,self.transliterate(lang,text).replace('"','')))
        return aiff2wav(fname)
    def transliterate(self,lang,text,forPartials=0):
        if not self.voices[lang]=='-v "Ting-Ting" ': return text
        # The hanzi-to-pinyin conversion in the Ting-Ting voice is not always as good as eSpeak's, but it can be controlled with pinyin.
        ut = ensure_unicode(text)
        if u"\u513f" in ut or u"\u5152" in ut: return text # might be erhua - better pass to the synth as-is
        es = ESpeakSynth()
        if not es.works_on_this_platform() or not es.supports_language('zh'): return text
        return es.transliterate('zh',text,0)
    def can_transliterate(self,lang):
        if not self.voices.get(lang,0)=='-v "Ting-Ting" ': return 0
        es = ESpeakSynth()
        return es.works_on_this_platform() and es.supports_language('zh')
    def scanVoices(self):
        d = {}
        try: from AppKit import NSSpeechSynthesizer
        except: return {"en":""} # no -v parameter at all
        for vocId in NSSpeechSynthesizer.availableVoices():
            vocAttrib = NSSpeechSynthesizer.attributesForVoice_(vocId)
            if not 'VoiceName' in vocAttrib: continue
            if not 'VoiceLanguage' in vocAttrib:
                lang={"Damayanti":"id","Maged":"ar","Stine":"nb"}.get(vocAttrib['VoiceName'],None) # TODO: can sometimes use VoiceLocaleIdentifier instead, dropping the _ part (but can't even do that with Damayanti on 10.7)
                if not lang: continue # TODO: output VoiceName in a warning?
            else: lang = vocAttrib['VoiceLanguage']
            if '-' in lang: lang=lang[:lang.index("-")]
            if not lang in d: d[lang]=[]
            d[lang].append(vocAttrib['VoiceName'].encode('utf-8'))
        found=0 ; d2=d.copy()
        class BreakOut(Exception): pass
        # First, check for voice matches in same language beginning
        for k,v in d.items()[:]:
            if k in macVoices:
              try:
                for m in macVoices[k].split():
                  for vv in v:
                    if m.lower() == vv.lower():
                        d2[k] = [vv] ; found=1 ; del macVoices[k] ; raise BreakOut()
              except BreakOut: pass
            if len(d2[k])>1: d2[k]=[d2[k][0]]
        # Then check across languages (e.g. cant -> zh-...)
        for k,v in macVoices.items():
         try:
          for kk,vv in d.items():
            for m in v.split():
              for vvv in vv:
                if m.lower() == vvv.lower():
                  d2[k] = [vvv] ; found=1 ; raise BreakOut()
         except BreakOut: pass
        if d.keys()==['en'] and not found: return {"en":""} # just use the default
        for k,v in d2.items()[:]: d2[k]='-v "'+v[0]+'" '
        return d2

def aiff2wav(fname):
    if not system("sox \"%s\" \"%s\"" % (fname,fname[:-4]+"wav")):
        # good, we converted it to wav
        os.remove(fname)
        fname=fname[:-4]+"wav"
    # else just return aiff and hope for the best (TODO won't work with cache-synth; TODO can get here when 'say' gave empty output, e.g. just a dot, and the returned aiff might raise IOError when constructing a SampleEvent)
    return fname

class OSXSynth_OSAScript(Synth):
    # for old Macs that don't have a "say" command
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return macsound and fileExists("/usr/bin/osascript")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    # def play(self,lang,text): os.popen("osascript","w").write('say "%s"\n' % (text,)) # better not have the realtime one because osascript can introduce a 2-3second delay (and newer machines will not be using this class anyway; they'll be using OSXSynth_Say)
    def makefile(self,lang,text):
        fname = os.tempnam()+extsep+"aiff"
        os.popen("osascript","w").write('say "%s" saving to "%s"\n' % (text,fname))
        return aiff2wav(fname)

class OldRiscosSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return riscos_sound and not os.system("sayw .")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("sayw %s" % (text,))

class S60Synth(Synth): # TODO: figure out if S60 Python can call external programs; might be able to use eSpeak http://pvagner.webranet.sk/espeak/espeak.sisx
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en" # (audio.say always uses English even when other languages are installed on the device)
    def works_on_this_platform(self): return appuifw and hasattr(audio,"say")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text):
        if not text=="Error in graddint program.": # (just in case it's unclear)
          if text.endswith(';'): doLabel(text[:-1])
          else: doLabel(text)
        audio.say(text)

class AndroidSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en" # TODO others?
    def works_on_this_platform(self): return android
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): android.ttsSpeak(text)

if winsound or mingw32: toNull=" > nul"
else: toNull=" >/dev/null" # stdout only, not stderr, because we want to see any errors that happen

def ensure_unicode(text):
    if type(text)==type(u""): return text
    else:
        try: return unicode(text,"utf-8")
        except UnicodeDecodeError: raise Exception("problem decoding "+repr(text))

class PttsSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.program=None
        self.offlineOnly = False
        if ptts_program: self.program=ptts_program
        elif not winsound and not mingw32 and not cygwin: return
        # You can rename ptts.exe to ptts-offline.exe as a hack if you think your SAPI works only when generating words offline but not for actually playing them.  This is no longer documented in vocab.txt because usually if the system is that broken then it won't work offline either.
        if not self.program:
          for i in ["ptts.exe","ptts-offline.exe"]:
            if fileExists(i):
                # must keep the full path even on non-cygwin because we're adding ,1 to changeToDirOf (hope we don't hit a Windows version that doesn't like this).  But we can keep relative paths if tempdir_is_curdir. (TODO if this breaks when not tempdir_is_curdir, could try copying ptts.exe to temp, but would need to delete it afterwards)
                if cygwin or not tempdir_is_curdir: self.program='"'+os.getcwd()+cwd_addSep+i+'"'
                else: self.program = i
                self.offlineOnly = 'offline' in i
                break
        if not self.program:
            # (in case someone's running on Windows from source)
            show_warning("Warning: ptts.exe not found (required for SAPI 5 speech) - get it from the Windows gradint distribution (or elsewhere)")
        if cygwin: self.lily_file = win2cygwin(lily_file)
        else: self.lily_file = lily_file
        if fileExists(self.lily_file):
            self.old_lily_data=read(self.lily_file)
            if "zh" in sapiVoices and sapiVoices["zh"][0].lower()=="vw lily": del sapiVoices["zh"] # because we don't want to bypass our own interface to lily if a user set that without realising it's not needed
        else: self.lily_file = None
    def supports_language(self,lang): return lang in sapiVoices or lang=="en" or (self.lily_file and lang=="zh")
    # Voice list: os.popen("echo | "+self.program+" -vl").read().split("\n").  If any .lower() contain "espeak-" then after the "-" is an espeak language code see ESpeakSynth (it may not want unicode).  Other voices may also have support for specific languages - may sometimes be able to use <lang langid="locale-hex-code"/> (e.g. 809 UK, 804 Chinese (PRC) 404 Taiwan, 411 Japan) but no way for gradint to tell if successful
    def works_on_this_platform(self): return self.program
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate, especially if they're going to set the speed in the control panel!
    def play(self,lang,text):
        if self.offlineOnly: return SampleEvent(self.makefile_cached(lang,text)).play()
        if lang in sapiVoices:
            d=os.getcwd()
            ret=self.sapi_unicode(sapiVoices[lang][0],ensure_unicode(text),speed=sapiSpeeds.get(lang,None))
            os.chdir(d) ; return ret
        elif lang=='en':
            p=os.popen(self.program+self.speedParam(sapiSpeeds.get(lang,None))+toNull,"w")
            p.write(text+"\n")
            return p.close()
        elif lang=='zh':
            d=os.getcwd()
            ret=self.sapi_unicode("VW Lily",self.preparePinyinPhrase(text),speed=sapiSpeeds.get(lang,None))
            self.restore_lily_dict()
            os.chdir(d) ; return ret
    def sapi_unicode(self,voice,unicode_string,toFile=None,sampleRate=None,speed=None):
        # Speaks unicode_string in 'voice'.  toFile (if present) must be something that was returned by tempnam.  May change the current directory.
        if voice=="Ekho Cantonese": unicode_string = preprocess_chinese_numbers(fix_compatibility(unicode_string),isCant=2) # hack to duplicate the functionality of EkhoSynth
        unifile=os.tempnam() ; write(unifile,codecs.utf_16_encode(unicode_string)[0])
        if not toFile: extra=""
        else:
            extra=' -w '+changeToDirOf(toFile,1)+' -c 1'
            if sampleRate: extra += (' -s '+str(sampleRate))
        ret=system(self.program+' -u '+changeToDirOf(unifile,1)+' -voice "'+voice+'"'+extra+self.speedParam(speed)+toNull) # (both changeToDirOf will give same directory because both from tempnam)
        os.unlink(unifile) ; return ret
    def speedParam(self,speed):
        if speed: return " -r "+str(speed)
        else: return ""
    def makefile(self,lang,text):
        fname = os.tempnam()+dotwav
        oldcwd=os.getcwd()
        if lang in sapiVoices: r=self.sapi_unicode(sapiVoices[lang][0],ensure_unicode(text),fname,sapiVoices[lang][1],speed=sapiSpeeds.get(lang,None))
        elif lang=="en":
            p=os.popen(self.program+' -c 1 -w '+changeToDirOf(fname,1)+self.speedParam(sapiSpeeds.get(lang,None))+toNull,"w") # (can specify mono but can't specify sample rate if it wasn't mentioned in sapiVoices - might make en synth-cache bigger than necessary but otherwise no great problem)
            p.write(text+"\n")
            r=p.close()
        elif lang=='zh':
            r=self.sapi_unicode("VW Lily",self.preparePinyinPhrase(text),fname,16000,speed=sapiSpeeds.get(lang,None))
            self.restore_lily_dict()
        else: r=0 # shouldn't get here
        os.chdir(oldcwd)
        assert not r,"ptts.exe failed"
        d = sapi_sox_bug_workaround(read(fname)); write(fname,d)
        if cygwin: os.system("chmod -x '"+fname+"'")
        return fname
    def preparePinyinPhrase(self,pinyin):
        def stripPunc(p,even_full_stop=1): # because synth won't like punctuation in the dictionary entries
            toStrip=',?;":\'!' # (see note below re hyphens)
            if even_full_stop: toStrip+='.'
            for punc in toStrip: p=p.replace(punc,"")
            return p
        if __name__=="__main__": pinyin=stripPunc(pinyin,0) # (if not running as a library, strip ALL punctuation ANYWAY, because the voice can pause a bit long) (but don't strip full stops)
        # Split it into words to avoid it getting too long
        # (max 30 chars in a word, max 30 syllables & 240 bytes in its definition, no duplicate entries.  Splitting into words should be OK, but perhaps had better make sure the words on the left don't get too long in case the user omits spaces.)
        pinyin=ensure_unicode(pinyin) # allow existing hanzi as well (TODO also allow/convert unicode tone marks)
        # mark all existing hanzi with @ :
        i=0
        while i<len(pinyin):
            if ord(pinyin[i])>128:
                pinyin=pinyin[:i]+" @"+pinyin[i]+" "+pinyin[i+1:]
                i+=4
            else: i+=1
        pinyin=pinyin.replace("na4",u' @\u637a ').replace("yong4",u' @\u7528 ') # bug workarounds (sometimes na4 is pronounced as nei4 if left as pinyin, etc) (TODO it sometimes still is, whatever character we set it to, e.g. if 'na4 ge5 [cz..]' - it might be right; what are the rules anyway?)
        pinyin=pinyin.split()
        rVal=[]; dicWrite=[]; count=0
        for p in pinyin:
            if p.startswith('@') or (not '1' in p and not '2' in p and not '3' in p and not '4' in p and not '5' in p): # it's the hanzi we added, or it's not a pinyin word, so don't add it to the dictionary
                if not p.startswith('@'): # it's an english word
                    if True in map(lambda x: 'a'<=x<='z',list(p.lower())): show_warning("NOTE: Lily will synthesize '"+p+"' as English because there are no digits 1-5")
                    if rVal and not '_' in rVal[-1] and not rVal[-1].startswith('@'): rVal.append(' ') # 2 English words
                rVal.append(p)
                continue
            p2=stripPunc(p)
            kVal="_%d" % count ; count += 1 # better not make kVal too long otherwise the voice can insert awkward pauses
            dicWrite.append('"%s","%s","p"\r\n' % (kVal,p2))
            rVal.append(p.replace(p2,kVal)) # (leave in full stops etc; assumes p2 is a substring of p, which is why hyphens are taken out before stripPunc)
        write(self.lily_file,''.join(dicWrite))
        return ''.join(rVal).replace('@','') # (WITHOUT spaces, otherwise pauses far too much)
    def restore_lily_dict(self): write(self.lily_file,self.old_lily_data) # done ASAP rather than on finalise, because need to make sure it happens (don't leave the system in an inconsistent state for long)
def sapi_sox_bug_workaround(wavdata):
    # SAPI writes an 'EVNT' block after the sound data, and some versions of sox don't recognise this.  NB this hack is not very portable (relies on SAPI5 guaranteeing to write exactly one EVNT chunk and the bytes 'EVNT' never occur inside it, otherwise would need proper parsing)
    f=wavdata.rfind("EVNT")
    if f>-1: return wavdata[:f]
    else: return wavdata
py_final_letters="aeginouvrAEGINOUVR:" # (don't just pick up on tone numbers, but on numbers after finals, otherwise will have trouble if there's numeric input)
def sort_out_pinyin_3rd_tones(pinyin):
    # Tone sandhi blocking rules: Need to stop 3rd-tones sortout at end of any 2-syllable word + "gei3 ni3" + "wo3 xiang3".
    # Also need to stop at phrase breaks and any English word (or hanzi, although may get awkward cases with 3rd-tone hanzi mixed with pinyin, but that's no big worry as lily isn't too reliable anyway and with partials it'll be transliterated)
    segments = [] ; thisSeg = "" ; syls = 0
    def endsWithSpecialWordpair(segLower): return segLower.endswith("gei3 ni3") or segLower.endswith("gei3 wo3") or segLower.endswith("ni3 xiang3") or segLower.endswith("wo3 xiang3")
    for c in pinyin:
        if ord(c)>128 or c in ".,?;" or (c==" " and syls==2) or endsWithSpecialWordpair(thisSeg.lower()):
            segments.append(thisSeg) ; thisSeg="" ; syls = 0
        elif c==" ": syls = 0
        elif c in "12345": syls += 1
        thisSeg += c
    segments.append(thisSeg)
    # Now go for each segment
    ret = []
    for seg in segments:
      i=0
      while i<len(seg):
        while i<len(seg) and seg[i] not in '12345': i+=1
        if i<len(seg) and seg[i]=='3' and i and seg[i-1] in py_final_letters:
            toneToChange = i ; numThirdsAfter = 0
            j = i
            while True:
                j += 1
                while j<len(seg) and seg[j] not in '12345': j+=1
                if j<len(seg) and seg[j]=='3' and seg[j-1] in py_final_letters: numThirdsAfter+=1
                else: break
            if numThirdsAfter % 2: seg=seg[:toneToChange]+'2'+seg[toneToChange+1:]
        i += 1
      ret.append(seg)
    return "".join(ret)

class FliteSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): return got_program("flite")
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    def play(self,lang,text): return system("flite -t \"%s\"" % (text.replace('"',''),))
    def makefile(self,lang,text):
        fname = os.tempnam()+dotwav
        system("flite -t \"%s\" -o \"%s\"" % (text,fname))
        return fname
if winsound or mingw32 or cygwin: del FliteSynth.play # because on some (even high-spec) systems flite.exe gets intermittently stuck when playing in realtime.  Safer just to generate everything offline.

if macsound:
    # See if we need to unpack eSpeak and/or set the variables
    import commands
    f=commands.getoutput("echo espeak*-OSX.zip")
    if fileExists(f): unzip_and_delete(f)
    f=commands.getoutput("echo espeak*/speak")
    if fileExists(f) and fileExists(f[:-5]+"espeak-data/phontab"):
      os.environ["ESPEAK_DATA_PATH"]=os.getcwd()+cwd_addSep+f[:-6]
      os.environ["PATH"]=os.getcwd()+cwd_addSep+f[:-6]+":"+os.environ["PATH"]
elif winsound or mingw32 or cygwin:
    # See if we need to set the variables for eSpeak
    # (you can unpack it in the current directory or the espeak subdirectory, but not espeak-N.N )
    for dir in [".","espeak"]:
        if fileExists(dir+os.sep+"espeak-data"+os.sep+"phontab"):
            os.environ["ESPEAK_DATA_PATH"] = os.getcwd()+cwd_addSep+dir
            break

# If you are using the eSpeak speech synthesizer, you can
# optionally define a Python dictionary espeak_language_aliases
# that maps your language abbreviations onto eSpeak's, so
# that gradint will recognise yours as an alternative to eSpeak's.
# For example the following will cause "cant" to be a valid
# alternative to "zhy" when specifying a language for synthesized text
# in espeak (or when using synth partials).
espeak_language_aliases = { "cant":"zhy" }
# TODO does the above need to be moved to advanced.txt?
# (maybe not as 'cant' is probably the only example for now)

class SimpleZhTransliterator(object): # if not got eSpeak on system
    def can_transliterate(self,lang): return lang=="zh"
    def transliterate(self,lang,text,forPartials=1,from_espeak=0):
        if lang=="zh" and text.find("</")==-1: # (not </ - don't do this if got SSML)
            text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode("utf-8")
            found=0
            for t in text:
                if ord(t)>=128:
                    found=1 ; break
            if not found and text.lower()==fix_pinyin(text,[]): return text # don't need espeak
            elif from_espeak: return [text] # This transliterate() and ESpeakSynth's transliterate() work together - don't call espeak if there aren't any special characters (this saves launching a lot of espeak processes unnecessarily when synthing from partials), but DO proceed if fix_pinyin changes something, as in this case we need to check for embedded en words so fix_pinyin doesn't add spurious 5's, + embedded letters etc.
            elif not found: return fix_pinyin(text,[]) # No ESpeak on system and fix_pinyin needed to do something - best we can do is hope there aren't any embedded English words (because if there are, they'll have spurious 5's added)
simpleZhTransliterator = SimpleZhTransliterator()

def shell_escape(text):
    text = text.replace('\\','\\\\').replace('"','\\"')
    if unix: text=text.replace("$","\\$").replace("`","\\`").replace("!","! ")
    return '"'+text+'"'

espeakTranslitCacheFile = "espeak-translit-cache"+extsep+"bin" # TODO to advanced.txt?
class ESpeakSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.languages = {} ; self.program=""
        tryList = []
        if riscos_sound and 'eSpeak$dir' in os.environ: tryList=[os.environ['eSpeak$dir']+'.espeak-dat',os.environ['eSpeak$dir']+'.espeak-data']
        elif winsound or mingw32: tryList=[programFiles+"\\eSpeak\\espeak-data"]
        elif winCEsound: tryList=["\\espeak-data"] # Can't try \\Storage Card because our eSpeak compile can't cope with spaces (and quoting it does not work)
        else:
            tryList=[os.environ.get("HOME","")+"espeak-data","/usr/share/espeak-data","/usr/local/share/espeak-data"]
            if cygwin: tryList.append(programFiles+"/eSpeak/espeak-data")
        if os.environ.get("ESPEAK_DATA_PATH",""): tryList.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"espeak-data")
        langList = []
        for tryplace in tryList:
            try:
                self.place = tryplace
                langList = os.listdir(self.place+os.sep+"voices")
            except: self.place = None
            if langList: break
        if unix: # espeak might know where its data is
          if not self.place:
            import commands
            versionLine = (filter(lambda x:x.strip(),os.popen("(speak --help||espeak --help) 2>/dev/null").read().split("\n"))+[""])[0]
            if versionLine.find("Data at:")>=0:
              self.place = versionLine[versionLine.index("Data at:")+8:].strip()
              try: langList = os.listdir(self.place+os.sep+"voices")
              except: self.place = None
        for l in langList[:]:
            if l in ["default","!v","mb"]: langList.remove(l)
            elif isDirectory(self.place+os.sep+"voices"+os.sep+l):
                for ll in os.listdir(self.place+os.sep+"voices"+os.sep+l):
                    self._add_lang(ll,l+os.sep+ll)
            else: self._add_lang(l,l)
        self.theProcess = None
        self.translitCache = {}
        if self.place:
          if pickle and fileExists(espeakTranslitCacheFile):
            try: placeStat,tc = pickle.Unpickler(open(espeakTranslitCacheFile,"rb")).load()
            except: placeStat,tc = (),{}
            if placeStat==tuple(os.stat(self.place)): self.translitCache = tc # otherwise regenerate it because eSpeak installation has changed (TODO if you overwrite an existing _dict file in-place, it might not update the stat() of espeak-data and the cache might not be re-generated when it should; espeak's --compile seems ok though)
          self.place=self.place[:self.place.rindex(os.sep)] # drop the \espeak-data, so can be used in --path=
    def _add_lang(self,lang,fname):
        if "~" in lang: return # emacs backup files
        self.languages[lang]=fname
        for l in open(self.place+os.sep+"voices"+os.sep+fname).read(256).replace("\r","\n").split("\n"):
            if l.startswith("language "):
                l=l[9:].strip(wsp)
                if not l==lang:
                    if l in espeak_language_aliases.values(): # aliasing to an alias - update it
                        for k,v in espeak_language_aliases.items():
                            if v==l: espeak_language_aliases[k]=lang
                    espeak_language_aliases[l] = lang
    def describe_supported_languages(self):
        ret=[]
        items=self.languages.items() ; items.sort()
        for k,v in items:
            if "-" in k and not k=="zh-yue": continue # skip variants in the report (but do recognise them)
            o=open(self.place+os.sep+"espeak-data"+os.sep+"voices"+os.sep+v)
            line=""
            for t in range(10):
                line=o.readline()
                if line.find("name")>=0:
                    lname = line.split()[1].replace("_test","").replace("-test","").replace("-experimental","").replace("-expertimental","") # (delete the -test etc for more screen real-estate, as this is used only for explaining what the language abbreviations mean)
                    if not lname: continue
                    lname=lname[0].upper()+lname[1:]
                    ret.append(k+"="+lname)
                    break
        return " ".join(ret)
    def supports_language(self,lang): return espeak_language_aliases.get(lang,lang) in self.languages
    def not_so_good_at(self,lang): return lang not in prefer_espeak
    def works_on_this_platform(self):
        if len(self.languages.items())==0: return 0
        if winCEsound:
            for d in ["","\\Storage Card"]: # TODO check other language versions of Windows Mobile
                if fileExists(d+"\\bin\\speak"):
                    self.program = d+"\\bin\\speak" ; return True
            return False
        elif winsound or mingw32: toTry=[programFiles.replace("Program Files","progra~1")+"\\eSpeak\\command_line\\espeak.exe"] # progra~1 because "C:\Program Files" in os.system doesn't always work despite the quotes
        elif cygwin: toTry=[programFiles+"/eSpeak/command_line/espeak.exe"]
        else: toTry = []
        if toTry: # windows or cygwin
            if "ESPEAK_DATA_PATH" in os.environ:
                toTry.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"espeak.exe")
                toTry.insert(0,os.environ["ESPEAK_DATA_PATH"]+os.sep+"command_line"+os.sep+"espeak.exe")
            for t in toTry:
                if fileExists(t):
                    if " " in t: self.program='"'+t+'"'
                    else: self.program = t
                    return True
            return False
        else: # not windows or cygwin
            self.program="speak"
            if riscos_sound: return True # we've already confirmed <eSpeak$dir> works in the constructor
            import commands
            loc=commands.getoutput("locale -a|grep -i 'utf-*8$'|head -1").strip(wsp)
            if loc: loc="LC_CTYPE="+loc+" " # in case espeak can't find a utf-8 locale by itself
            self.program=loc+"speak"
            if got_program("speak"): return True
            # if 'speak' is not available then also check for 'espeak', because some packages install only that:
            self.program = loc+"espeak"
            return got_program("espeak")
    def guess_length(self,lang,text):
        if text.find("</")>=0: # might be SSML - don't count inside <...>
            l=inSsml=0
            for c in text:
                if c=="<": inSsml=1
                elif c==">": inSsml=0
                elif not inSsml: l += 1
        else: l=len(text)
        latency = 0
        if winCEsound: latency = 1.3 # TODO need a better estimate.  Overhead on 195MHz Vario (baseline?) >1sec (1.3 seems just about ok)
        elif unix:
          if espeak_pipe_through and not outputFile:
            if not hasattr(self,"latency"):
              t = time.time()
              self.play("en","")
              self.latency = time.time() - t # 2secs on eeePC Ubuntu 11.10, mostly AFTER the utterance
              if self.latency > 0.5: show_info("espeak_pipe_through latency is "+str(int(self.latency*10)/10.0)+"\n",True)
            latency = self.latency
        return quickGuess(l,12)+latency
    def can_transliterate(self,lang): return espeak_language_aliases.get(lang,lang) in ["zh","zhy","zh-yue"] and not riscos_sound # TODO it's OK on RISC OS if the eSpeak version is recent enough to do --phonout=filename; TODO aliases for zhy (but not usually a problem as can_transliterate is called only for preference)
    def winCE_run(self,parameters,expectedOutputFile,infileToDel=None):
        self.winCE_start(parameters)
        time.sleep(0.3) # 0.2 not always long enough for transliterations (get empty output file if try to read too soon, then loop waiting for it to have contents)
        return self.winCE_wait(expectedOutputFile,infileToDel)
    def winCE_start(self,parameters):
        s = ShellExecuteInfo(60,File=u""+self.program,Parameters=u"--path="+self.place+" "+parameters,fMask=0x40)
        ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(s))
        self.hProcess = s.hProcess # TODO check it's not NULL (failed to run)
    def winCE_wait(self,expectedOutputFile,infileToDel=None,needDat=1):
        # won't always work: if app and not app.Label["text"].strip(): app.setLabel("Waiting for eSpeak") # in case it doesn't produce output
        ctypes.cdll.coredll.WaitForSingleObject(self.hProcess,4294967295) # i.e. 0xFFFFFFFF but that throws up a warning on Python 2.3
        ctypes.cdll.coredll.CloseHandle(self.hProcess)
        # In some rare circumstances, that command won't wait (e.g. process hadn't started despite the fact we delayed), so check the output files also.
        # (Leave WaitForSingleObject in as it could save some CPU cycles / potential OS crashes on some WinCE versions)
        firstIter = 2
        while True:
            if firstIter: firstIter -= 1
            else: time.sleep(0.2),check_for_interrupts() # (latter needed in case it gets stuck)
            try:
              if needDat: dat=read(u""+expectedOutputFile)
              else: dat=open(u""+expectedOutputFile).read(8)
            except: continue # error on trying to read output
            if not dat: continue # output read as empty
            if expectedOutputFile.endswith(dotwav) and (len(dat)<8 or dat[6:8]=="\xff\x7f"): continue # length field not yet written
            # (TODO how could we make sure a long transliteration has finished, if the OS lets us open the file before done and if WaitForSingleObject doesn't work?)
            if not firstIter: time.sleep(0.2) # just in case
            if infileToDel:
                try: os.unlink(infileToDel)
                except: continue # still got the input file open
            return dat
    def update_translit_cache(self,lang,textList): # forPartials=1 assumed
        if not lang=="zh": return # TODO if expand 'transliterate' to do other languages, make sure to update this also, and the cache format
        if self.translitCache: textList=filter(lambda x:x not in self.translitCache, textList)
        step = 1000 # should be about right?
        for i in range(0,len(textList),step):
            tl = textList[i:i+step]
            tlr = self.transliterate_multiple(lang,tl,keepIndexList=1)
            if not tlr: return # espeak's not up to it
            for i in self.lastIndexList: self.translitCache[tl[i]]=tlr[i]
            if winCEsound: ctypes.cdll.coredll.SystemIdleTimerReset() # TODO here may not be often enough if auto-switchoff is an especially short time and/or CPU is especially slow (but then plugging it into external power would probably be best anyway)
        if textList:
            try: pickle.Pickler(open(espeakTranslitCacheFile,"wb"),-1).dump((tuple(os.stat(self.place+os.sep+"espeak-data")),self.translitCache))
            except IOError: pass # 'permission denied' is ok
    def transliterate(self,lang,text,forPartials=1):
        if lang=="zh" and text in self.translitCache: return self.translitCache[text] # (TODO add "and forPartials"? but don't need to bother with this extra condition on slow systems)
        return self.transliterate_multiple(lang,[text],forPartials)[0] # and don't cache it - could be experimental, and we don't want cache to grow indefinitely
    if unix:
        def check_dicts(self,lang):
            if not hasattr(self,"dictsChecked"): self.dictsChecked = {}
            if lang in self.dictsChecked or not lang in ["zh","zhy","ru"]: return
            if filelen(self.place+os.sep+"espeak-data"+os.sep+lang+"_dict")<100000: show_warning("Warning: the eSpeak on this system has only a short dictionary for language '"+lang+"' - please install eSpeak's additional data.")
            self.dictsChecked[lang]=1
    else:
        def check_dicts(self,lang): pass
    def transliterate_multiple(self,lang,textList,forPartials=1,keepIndexList=0):
      # Call eSpeak once for multiple transliterations, for greater efficiency (especially on systems where launching a process is expensive e.g. WinCE).
      # Note: Don't make textList TOO long, because the resulting data must fit on the (RAM)disk and in memory.
      retList = [] ; write_to_espeak = [] ; indexList = []
      split_token = "^^^" # must be something not defined in the _rules files
      self.check_dicts(lang)
      for text in textList: # DON'T escape_jyutping (treat as en words)
        if lang=="zh":
         if keepIndexList: # making the cache - can we go a bit faster?
           try: t = unicode(text,"ascii") # if no utf, know is OK (but ONLY if keepIndexList, as the result is imprecise)
           except UnicodeDecodeError: t = simpleZhTransliterator.transliterate(lang,text,from_espeak=1)
         else: t = simpleZhTransliterator.transliterate(lang,text,from_espeak=1)
        else: t=[fix_compatibility(ensure_unicode(text)).encode("utf-8")]
        if t and not riscos_sound: # same TODO as above re RISC OS
            if type(t)==type([]):
                indexList.append(len(retList))
                retList.append(None) # result not filled in yet
                if lang=="zh": tt=pinyin_uColon_to_V(t[0].replace("-","/")) # NB fix_compatibility has already been done (as has preprocess_chinese_numbers), by simpleZhTransliterator above
                else: tt=t[0]
                write_to_espeak.append(fix_commas(tt).replace(split_token," "))
                # (replacing - with / because espeak zh voice treats / as a silent word separator but - is ignored; - is used as a word separator in MeiLing etc.  so if you want to write the hanzi for wei2ren2 but you want it to be wei4+ren2, you can hack in this way.  TODO document?)
            else: retList.append(t)
        else: retList.append(None)
      if keepIndexList: self.lastIndexList = indexList
      if not indexList: return retList
      overruns = [] # elements that need to be merged with their following elements (duplicates allowed because indices change after each merge), used when we're transliterating very long texts (not usually as part of a lesson) because some versions of espeak truncate very long lines
      i = 0
      while i < len(write_to_espeak):
          if len(write_to_espeak[i]) > 500:
              x = write_to_espeak[i].decode('utf-8')
              write_to_espeak[i] = x[:150].encode('utf-8')
              write_to_espeak.insert(i+1,x[150:].encode('utf-8'))
              overruns.append(i-len(overruns))
          i += 1
      fname = os.tempnam()
      open(fname,"w").write((".\n"+split_token+" ").join(write_to_espeak))
      oldcwd=os.getcwd()
      if winCEsound:
          translit_out = os.tempnam()
          data=self.winCE_run(' -v%s -q -X -f %s --phonout=%s' % (espeak_language_aliases.get(lang,lang),fname,translit_out),translit_out)
          os.remove(translit_out)
      else: data=os.popen(self.program+' -v%s -q -X -f %s%s' % (espeak_language_aliases.get(lang,lang),changeToDirOf(fname,1),cond(unix," 2>&1","")),"rb").read() # popen2 might not work, so had better do it this way:
      os.chdir(oldcwd) ; os.remove(fname)
      data = data.replace("\r\n","\n").split("\nTranslate '"+split_token+"'\n")
      if len(data)==2*(len(indexList)+len(overruns))-1:
        # split points are doubled - better take every ODD item.  (NB the text in between is NOT necessarily blank - espeak can flush its sentence cache there)
        d2 = []
        for i in xrange(0,len(data),2): d2.append(data[i])
        data = d2
      for o in overruns:
          data[o] += data[o+1]
          del data[o+1]
      if not len(data)==len(indexList):
          if not (winsound or macsound): show_warning("Warning: eSpeak's transliterate returned wrong number of items (%d instead of %d).  Falling back to separate runs for each item (slower)." % (len(data),len(indexList)))
          return None
      for index,dat in zip(indexList,data):
          en_words={} # any en words that espeak found embedded in the text
          r=[] ; lastWasBlank=False
          delete_last_r_if_blank = 0
          thisgroup_max_priority,thisgroup_enWord_priority = 0.5,0
          for l in dat.strip(wsp).split("\n"):
              # print "Debugger:",l.strip()
              # get en_words for fix_pinyin (and for making sure we embed them in cant)
              lWords = l.split()
              if lWords: int0 = intor0(lWords[0])
              else: int0 = 0
              if int0:
                  if int0 > thisgroup_max_priority:
                      thisgroup_max_priority = int0
                      if lWords[-1]=="[_^_]": thisgroup_enWord_priority = int0 # so far it looks like this is going to be an English word
              else: # a split between the groups
                  if thisgroup_enWord_priority == thisgroup_max_priority: # the choice with the highest priority was the one containing the [_^_] to put the word into English
                      en_words[r[-1]]=1
                  thisgroup_max_priority,thisgroup_enWord_priority = 0.5,0
              # end of getting en_words
              if lang=="zh" and r and ((not lastWasBlank and (l.startswith("Replace") or l.startswith("Translate") or l.startswith("Found"))) or l.find("';'")>1 or l.find("','")>1): r[-1]+="," # (because not-blank is probably the line of phonemes)
              elif not lang=="zh" and l.startswith("_|") and r: r[-1] += "," # works for zh-yue
              if delete_last_r_if_blank and not l: r=r[:-1] # "Translate" followed by blank line is probably corner-brackets or something; don't want that confusing the transliteration (especially if it's for partials)
              delete_last_r_if_blank = 0
              foundLetter=0
              if l.startswith("Translate "):
                  toAppend=l[l.index("'")+1:-1].replace("\xc3\xbc","v")
                  if not (toAppend in en_words and r and toAppend==r[-1]):
                    # TODO what about partial English words? e.g. try "kao3 testing" - translate 'testing' results in a translate of 'test' also (which assumes it's already in en mode), resulting in a spurious word "test" added to the text box; not sure how to pick this up without parsing the original text and comparing with the Replace rules that occurred
                    r.append(toAppend)
                    delete_last_r_if_blank = 1
                  else: en_words[toAppend]=1
              else: # not Translate
                  if lang=="zh" and l.startswith("Found: ") and ((l[7]==l[9]=="'" and "a"<=l[8]<="z") or (l[8]==" " and "a"<=l[7]<="z")): # an alphabetical letter - we can say this as a Chinese letter and it should be compatible with more partials-based synths.  But DON'T do this if going to give it to a unit-selection synth - 'me1' and 'ne1' don't have hanzi and some synths will have difficulty saying them.
                      if l[8]==' ': letter=l[7]
                      else: letter=l[8]
                      if forPartials: r.append("a1 bo1 ci1 de1 e1 fou1 ge1 he1 yi1 ji1 ke1 le1 me1 ne1 wo1 po1 qi1 ri4 si1 te4 yu1 wei4 wu1 xi1 ye1 zi1".split()[ord(letter)-ord('a')])
                      else: # a letter in something we're transliterating for a pinyin-driven unit-selection synth
                          r.append(letter)
                          en_words[r[-1]]=1
                      foundLetter = 1
                  elif not lang=="zh" and l.startswith("Found: ") and (ord(l[7])>127 or (l[7]=="'" and ord(l[8])>127)): # (espeak 1.40 puts in l[7], 1.44 surrounds in quotes)
                      r.append(l[l.index("[")+1:l.index("]")])
              lastWasBlank=(l.startswith("Replace") or not l or foundLetter) # (take 'Replace' lines as blank, so 'Translate' doesn't add a second comma.  ditto letters thing.)
          while r and r[-1] and r[-1][-1]==',': r[-1]=r[-1][:-1] # strip any trailing commas
          if lang=="zh": retList[index]=fix_pinyin(" ".join(r),en_words)
          else: retList[index]=" ".join(r)
      return retList
    def escape_jyutping(self,text): return re.sub(r"([abcdefghjklmnopstuwz][a-z]*[1-7])",r"[[\1]]",text) # TODO what if user already escaped it?
    def play(self,lang,text):
        self.check_dicts(lang)
        if espeak_language_aliases.get(lang,lang) in ["zhy","zh-yue"]: text=self.escape_jyutping(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=1).encode("utf-8"))
        elif lang=="zh": text=fix_commas(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode('utf-8'))
        if winCEsound: # need to play via makefile, and careful not to leave too many tempfiles or take too long
            ret = 0
            if len(text)>15: # not a short phrase - let's split it up
                l = [] ; pos=0
                for i in xrange(len(text)-1):
                    if text[i] in ",.;!?" and text[i+1]==" " and i-pos>20: # (don't split TOO short)
                        l.append(text[pos:i+1])
                        pos = i+2
                if pos<len(text): l.append(text[pos:])
                text = l
            else: text=[text]
            try:
              for i in range(len(text)):
                f=self.makefile(lang,text[i])
                if len(text)>5: doLabel("("+str(int(100*i/len(text)))+"%)")
                if i<len(text)-1: self.makefile(lang,text[i+1],1) # give it a hint about the next phrase
                ret = SampleEvent(f,isTemp=1).play() # TODO ret is not checked unless it's the last one (but should be OK for short in-lesson phrases, and 'ret' might not show up the errors anyway)
                if emulated_interruptMain: check_for_interrupts()
                ctypes.cdll.coredll.SystemIdleTimerReset()
            finally:
              if hasattr(self,"winCEhint"): os.unlink(self.makefile(lang,"")) # make sure to clean up on interrupt
            return ret
        elif unix or winsound or mingw32 or cygwin:
            # Windows command line is not always 100% UTF-8 safe, so we'd better use a pipe.  Unix command line OK but some espeak versions have a length limit.  (No pipes on riscos.)
            p=os.popen(self.program+cond(text.find("</")>=0," -m","")+' -v%s -a%d %s' % (espeak_language_aliases.get(lang,lang),100*soundVolume,espeak_pipe_through),"wb")
            p.write(text.replace(". ",".\n")+"\n") ; return p.close() # (see comment below re adding newlines)
        else: return system(self.program+cond(text.find("</")>=0," -m","")+' -v%s -a%d %s %s' % (espeak_language_aliases.get(lang,lang),100*soundVolume,shell_escape(text),espeak_pipe_through)) # (-m so accepts SSML tags)
    def makefile(self,lang,text,is_winCEhint=0):
        self.check_dicts(lang)
        if espeak_language_aliases.get(lang,lang) in ["zhy","zh-yue"]: text=self.escape_jyutping(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=1).encode("utf-8"))
        elif lang=="zh": text=fix_commas(preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text))).encode('utf-8'))
        if hasattr(self,"winCEhint"): # waiting for a previous async one that was started with is_winCEhint=1
            fname,fnameIn = self.winCEhint
            del self.winCEhint
            self.winCE_wait(fname,fnameIn,needDat=0)
            return fname
        fname = os.tempnam()+dotwav
        oldcwd=os.getcwd()
        sysCommand = cond(winCEsound,"",self.program)+cond(text.find("</")>=0," -m","")+' -v%s -w %s%s' % (espeak_language_aliases.get(lang,lang),cond(unix,"/dev/stdout|cat>",""),changeToDirOf(fname,1))
        # (Unix use stdout and cat because some espeak versions truncate the output file mid-discourse)
        # (eSpeak wavs are 22.05k 16-bit mono; not much point down-sampling to 16k to save 30% storage at expense of CPU)
        if winsound or mingw32: os.popen(sysCommand,"w").write(text+"\n") # must pipe the text in
        elif riscos_sound: os.system(sysCommand+' '+shell_escape(text))
        elif winCEsound:
            fnameIn = os.tempnam() ; open(fnameIn,"w").write(text)
            if is_winCEhint:
                self.winCEhint = (fname,fnameIn)
                self.winCE_start(sysCommand+' -f '+fnameIn)
            else: self.winCE_run(sysCommand+' -f '+fnameIn,fname,fnameIn)
        else:
            # we can make it asynchronously (still need to pipe)
            # (add end-of-sentence newlines due to short line buffer in some versions of espeak)
            sysCommand='echo '+shell_escape(text.replace(". ",".\n"))+'|'+sysCommand
            if not self.theProcess: self.theProcess = os.popen("/bin/bash","w")
            self.theProcess.write('cd "'+os.getcwd()+'"\n'+sysCommand+"\n")
            self.theProcess.flush()
        os.chdir(oldcwd)
        return fname
    def finish_makefile(self):
        if self.theProcess: self.theProcess.close()
        self.theProcess = None

def fix_commas(text):
  # some versions of espeak won't honour ordinary commas in among Chinese text if the ordinary commas don't have spaces after
  # also put 2 spaces after full stop, and make sure capitalised
  i=0
  while i<len(text)-1:
    if text[i] in '.,?;!':
      tRest = text[i+1:].strip(wsp)
      if tRest and (ord(tRest[0])>=128 or 'a'<=tRest[0].lower()<='z'):
        text=text[:i+1]+cond(text[i] in ".?!","  "+tRest[0].upper()," "+tRest[0])+tRest[1:]
    i+=1
  return text

def fix_pinyin(pinyin,en_words):
  # fix pinyin numbers in 'wrong' place, e.g. ta4i to tai4 (which can result from espeak being given tone marks or from non-standard user input to the GUI), and add missing 5's
  if en_words:
    ret=[]
    def stripPunc(w):
      i=0 ; j=len(w) ; w=w.lower()
      while i<len(w) and not 'a'<=w[i]<='z': i+=1
      while j>1 and not ('a'<=w[j-1]<='z' or '1'<w[j-1]<='5'): j-=1
      return w[i:j]
    for w in pinyin.split():
      if stripPunc(w) in en_words: ret.append(w)
      else: ret.append(fix_pinyin(w,[]))
    return ' '.join(ret)
  i=0
  pinyin=pinyin_uColon_to_V(pinyin)+"@@@" # (includes .lower; @@@ for termination)
  while i<len(pinyin):
    if pinyin[i] in "12345":
      moveBy=0
      if pinyin[i+1] in "iuv": moveBy=1 # these are never initial letters
      elif pinyin[i+1]=="o" and not pinyin[i+2] in "u12345": moveBy=1 # "o" and "ou" are valid syllables, but a number before "o" is likely to be premature especially if the "o" is not itself followed by a number (or "u")
      elif pinyin[i+1:i+3]=="ng" and not pinyin[i+3] in "aeiouv": moveBy=2 # before an -ng, but NOT before a -n g-(vowel)
      elif pinyin[i+1] in "nr" and not pinyin[i+2] in "aeiouv" and not (pinyin[i+1]=="r" and i and not pinyin[i-1]=="e") and not pinyin[i+1:i+3]=="r5": moveBy=1 # before -n or -r (as final not as initial) (but NB -r is only on -er, otherwise it's an r5.  and if it already says r5, leave it.)
      if moveBy: pinyin=pinyin[:i]+pinyin[i+1:i+moveBy+1]+pinyin[i]+pinyin[i+moveBy+1:]
    i+=1
  i=0
  while i<len(pinyin): # check for missing 5's
    if (pinyin[i] in "aeiouvr" and pinyin[i+1] not in "aeiouv12345") or (ord('a')<=ord(pinyin[i])<=ord('z') and not (ord("a")<=ord(pinyin[i+1])<=ord("z") or pinyin[i+1] in "12345")): # ("alnum and next is not alnum" is not strictly necessary, but we do need to add 5's after en-like words due to 'fix_pinyin(t)==t' being used as a do-we-need-proper-translit. condition in SimpleZhTransliterator, otherwise get problems with things like "c diao4" going to eSpeak when it could go to partials-with-letter-substitutions)
      if pinyin[i+1:i+3]=="ng" and not pinyin[i+3] in "aeiouv":
        if pinyin[i+3] not in "12345": pinyin=pinyin[:i+3]+"5"+pinyin[i+3:]
      elif (pinyin[i+1]=="n" or pinyin[i:i+2]=="er") and not pinyin[i+2] in "aeiouv" and not pinyin[i]=="r":
        if pinyin[i+2] not in "12345": pinyin=pinyin[:i+2]+"5"+pinyin[i+2:]
      else: pinyin=pinyin[:i+1]+"5"+pinyin[i+1:]
    i+=1
  return pinyin[:-3] # remove the @@'s

def remove_tone_numbers(utext): # for hanzi_and_punc to take out numbers that can't be transliterated
    i=1
    while i<len(utext):
        if "1"<=utext[i]<="5" and "a"<=utext[i-1].lower()<="z" and (i==len(utext)-1 or not "0"<=utext[i+1]<="9"): utext=utext[:i]+utext[i+1:]
        i+=1
    return utext
def preprocess_chinese_numbers(utext,isCant=0): # isCant=1 for Cantonese, 2 for hanzi (and if 1 or 2, also assumes input may be jyutping not just pinyin)
    # Hack for reading years digit by digit:
    for year in ["nian2",u"\u5e74"]: # TODO also " nian2" to catch that? what of multiple spaces?
        while utext.find(year)>=4 and 1200 < intor0(utext[utext.index(year)-4:utext.index(year)]) < 2300: # TODO is that range right?
            yrStart = utext.index(year)-4
            utext = utext[:yrStart] + " ".join(list(utext[yrStart:yrStart+4]))+" "+utext[yrStart+4:]
    # End of hack for reading years
    i=0
    while i<len(utext):
        if "0"<=utext[i]<="9" and not ("1"<=utext[i]<=cond(isCant,"7","5") and i and "a"<=utext[i-1].lower()<="z" and (i==len(utext)-1 or not "0"<=utext[i+1]<="9")): # number that isn't a tone digit
            j=i
            while j<len(utext) and utext[j] in "0123456789.": j += 1
            while utext[j-1]==".": j -= 1 # exclude trailing point(s)
            num = read_chinese_number(utext[i:j])
            if isCant:
              for mand,cant in zip("ling2 yi1 er4 san1 si4 wu3 liu4 qi1 ba1 jiu3 dian3 yi4 qian1 bai3 shi2 wan4".split(),cond(isCant==2,u"\u96f6 \u4e00 \u4e8c \u4e09 \u56db \u4e94 \u516d \u4e03 \u516b \u4e5d \u70b9 \u4ebf \u5343 \u767e \u5341 \u4e07","ling4 jat1 ji6 saam7 sei3 ng5 luk6 cat7 baat3 gau2 dim2 jik1 cin7 baak3 sap6 maan6").split()): num=num.replace(mand,cant)
            utext=utext[:i]+num+utext[j:]
            i += len(num)
        else: i += 1
    return utext
def read_chinese_number(num):
    digits="ling2 yi1 er4 san1 si4 wu3 liu4 qi1 ba1 jiu3".split()
    nums=num.split(".")
    if len(nums)==1: # normal number
        columns=("yi4 qian1 bai3 shi2 wan4 qian1 bai3 shi2".split()+[""])
        has_wan = not ("00000000"+num)[-8:-4]=="0000"
        if len(num)>len(columns) or (num and num[0]=="0"): return "".join([digits[ord(d)-ord("0")] for d in num]) # far too many digits, or something starting with 0 - read one at a time
        r=[]
        for d,c,i in zip(list(num),columns[-len(num):],range(len(num))):
            if d=="0":
                if c=="wan4" and has_wan: r.append(c)
                elif c and not (r and r[-1]=="ling2"): r.append("ling2")
                # else nothing
            elif d=="1" and c=="shi2" and (i==0 or (r and r[-1]=="ling2")): r.append(c) # 10, 1010
            else: r.append(digits[ord(d)-ord("0")]+c)
        if len(r)>1 and r[-1]=="ling2": del r[-1] # e.g. 100
        return "".join(r)
    elif len(nums)==2: # read digits after the point one at a time
        rVal = [read_chinese_number(nums[0]),"dian3"]
        for d in nums[1]: rVal.append(digits[ord(d)-ord("0")])
        return "".join(rVal)
    else: return "dian3".join([read_chinese_number(n) for n in nums]) # probably a complex version number

def fix_compatibility(utext): # convert 'compatibility full-width' characters to ASCII, also simplify some quote marks etc
    r = []
    for c in utext:
        if 0xff01<=ord(c)<=0xff5e: r.append(unichr(ord(c)-0xfee0))
        elif 0x2010 <= ord(c) <= 0x2015: r.append("-")
        elif c==unichr(0x201a): r.append(",") # sometimes used as comma (incorrectly)
        elif 0x2018 <= ord(c) <= 0x201f: r.append('"')
        elif c==unichr(0xff61): r.append(".")
        else: r.append(c)
    return u"".join(r)

# Older versions of eSpeak output WAVs with 0 length and can't be piped through aplay
espeak_pipe_through = "" # or "--stdout|..." (NOT on Windows)
def espeak_stdout_works():
    assert unix, "espeak_stdout_works should be called only if unix"
    # recent enough for --stdout to work.  Don't be tempted to look for "zh" in languages
    # because espeak 1.31 shipped with zh (broken) and a broken --stdout (length marked as 0)
    versionLine = (filter(lambda x:x,os.popen("(speak --help||espeak --help) 2>/dev/null").read().split("\n"))+[""])[0]
    versionLine = versionLine[versionLine.find(":")+1:].strip()
    versionLine = versionLine[:versionLine.find(" ")]
    versionLine = (versionLine+".")[:versionLine.find(".",versionLine.find(".")+1)] # if x.y.z just have x.y
    try: return (float(versionLine)>=1.32)
    except ValueError: return False
def espeak_volume_ok():
    # if has "zh", should be recent enough
    return "zh" in ESpeakSynth().languages
if wavPlayer_override or (unix and not macsound and not (oss_sound_device=="/dev/sound/dsp" or oss_sound_device=="/dev/dsp")):
    if wavPlayer=="aplay" and espeak_stdout_works(): espeak_pipe_through="--stdout|aplay -q" # e.g. NSLU2
    else: del ESpeakSynth.play # because we have no way of sending it to the alternative device, so do it via a file
    if hasattr(FliteSynth,"play"): del FliteSynth.play
if hasattr(ESpeakSynth,"play") and (soundVolume<0.04 or (soundVolume<0.1 and not espeak_volume_ok()) or soundVolume>2): del ESpeakSynth.play # old versions of espeak are not very good at less than 10% volume, so generate offline and use sox

# ESpeakSynth's c'tor may modify espeak_language_aliases, and it has to be consistent at the time of partial scanning.  Plus c'tor called too often.  Hack for now:
globalEspeakSynth = ESpeakSynth()
class ESpeakSynth(ESpeakSynth):
    def __init__(self): self.__dict__ = globalEspeakSynth.__dict__

class EkhoSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        if ekho_speed_delta: self.prog="ekho -s %d" % ekho_speed_delta
        else: self.prog="ekho"
    def supports_language(self,lang): return lang in ["zhy","zh-yue","cant"] # not Mandarin unless we can check we have a version of ekho that does 3rd tones correctly
    def works_on_this_platform(self): return got_program("ekho")
    def guess_length(self,lang,text): return quickGuess(len(text),6) # TODO need a better estimate
    def play(self,lang,text):
        text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=2).encode("utf-8")
        infile = os.tempnam()+dottxt ; open(infile,"w").write(text) # Ekho 4.5 takes "-f -" for stdin, but 4.1 can't
        r = system(self.prog+" --voice=Cantonese -f \""+infile+"\"")
        os.remove(infile)
        return r
    def makefile(self,lang,text):
        text = preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=2).encode("utf-8")
        fname = os.tempnam()+dotwav # TODO can also have dotmp3 (with -t mp3 added), and the resulting mp3 can be smaller than gradint's
        infile = os.tempnam()+dottxt ; open(infile,"w").write(text)
        system(self.prog+" --voice=Cantonese -f \""+infile+"\" -o \""+fname+"\"")
        os.remove(infile)
        return fname

class FestivalSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def startProcess(self):
        self.theProcess = os.popen("festival -i >/dev/null 2>/dev/null","w")
        self.theProcess.write("(Parameter.set 'Audio_Required_Format 'riff)\n(Parameter.set 'Audio_Method 'Audio_Command)\n")
    def supports_language(self,lang): return lang=="en"
    def works_on_this_platform(self): # can *assume* this *will* be called, so put the startProcess check here (no need to call this in duplicate from init)
        r=(unix and not macsound and got_program("festival"))
        if r: self.startProcess()
        return r
    def guess_length(self,lang,text): return quickGuess(len(text),12) # TODO need a better estimate
    if oss_sound_device:
      def play(self,lang,text):
        if not self.theProcess: self.startProcess()
        self.theProcess.write("(Parameter.set 'Audio_Command \"play --device=%s \$FILE vol %.1f\")\n(tts_text \"%s\" nil)\n" % (oss_sound_device,5*soundVolume,text)) # (tts_text text nil) can be better than (SayText text) because it splits into multiple utterances if necessary
        self.theProcess.flush()
    # else send it via a file, because we haven't got code to give it to play to the other devices directly
    def makefile(self,lang,text):
        if not self.theProcess: self.startProcess()
        fname = os.tempnam()+dotwav
        self.theProcess.write("(Parameter.set 'Audio_Command \"sox \$FILE %s vol 5\")\n(SayText \"%s\")\n" % (fname,text))
        self.theProcess.flush()
        return fname
    def finish_makefile(self):
        if self.theProcess: self.theProcess.close()
        self.theProcess = None

class GeneralSynth(Synth):
    def __init__(self): Synth.__init__(self)
    def supports_language(self,lang):
        for l,c in extra_speech:
            if l==lang: return 1
        return 0
    def works_on_this_platform(self): return extra_speech
    def guess_length(self,lang,text): return quickGuess(len(text),10) # TODO need a better estimate
    def play(self,lang,text):
        for l,c in extra_speech:
            if l==lang: return system('%s %s' % (c,shell_escape(text)))

class GeneralFileSynth(Synth):
    def __init__(self):
        Synth.__init__(self)
        self.letters = {} ; self.duration = {}
    def supports_language(self,lang):
        for l,c,f in extra_speech_tofile:
            if l==lang: return 1
        return 0
    def works_on_this_platform(self): return extra_speech_tofile
    def guess_length(self,lang,text):
        if not lang in self.letters: self.letters[lang]=self.duration[lang]=0
        if self.letters[lang]<25:
            self.letters[lang] += len(text)
            self.duration[lang] += SampleEvent(self.makefile_cached(lang,text)).exactLen
            assert self.duration[lang], "GeneralFileSynth didn't put sound in file?"
        return quickGuess(len(text),self.letters[lang]/self.duration[lang]) # (doing it this way so don't synth the whole list, but do make sure got a big enough sample)
    # (note: above works only because finish_makefile() is not necessary in this class)
    def makefile(self,lang,text):
        for l,c,f in extra_speech_tofile:
            if l==lang:
                if os.system(c % shell_escape(text)): raise Exception("Your extra_speech_tofile command failed on "+repr(text))
                fname = os.tempnam()+extsep+soundFileType(f)
                if unix: os.system('mv "'+f+'" "'+fname+'"') # because os.rename() can throw an exception if renaming cross-device on some systems
                else: os.rename(f,fname)
                return fname

all_synth_classes = [GeneralSynth,GeneralFileSynth] # at the beginning so user can override
for s in synth_priorities.split(): # synth_priorities no longer in advanced.txt (see system.py above) but we can still support it
    if s.lower()=="ekho": all_synth_classes.append(EkhoSynth)
    elif s.lower()=="espeak": all_synth_classes.append(ESpeakSynth)
    elif s.lower()=="macos":
       all_synth_classes.append(OSXSynth_Say)
       all_synth_classes.append(OSXSynth_OSAScript) # (prefer _Say if >=10.3 because it's faster)
    elif s.lower()=="sapi": all_synth_classes.append(PttsSynth)
all_synth_classes = all_synth_classes + [FestivalSynth,FliteSynth,OldRiscosSynth,S60Synth,AndroidSynth]
prefer_espeak = prefer_espeak.split()

viable_synths = []
warned_about_nosynth = {}
getsynth_cache = {}
def setSoundCollector(sc):
    # for GUI etc - need to reset the available synths when changing it
    global soundCollector, viable_synths, getsynth_cache
    soundCollector,viable_synths,getsynth_cache = sc,[],{}
def get_synth_if_possible(language,warn=1,to_transliterate=False):
    if language in getsynth_cache and not to_transliterate: return getsynth_cache[language] # most common case (vocab.txt parse)
    if language==None:
        if not None in getsynth_cache: getsynth_cache[None]=Partials_Synth()
        return getsynth_cache[None]
    global viable_synths, warned_about_nosynth
    if not viable_synths:
        for C in all_synth_classes:
            instance = C()
            if instance.works_on_this_platform() and (not soundCollector or hasattr(instance,"makefile")): viable_synths.append(instance)  # TODO: what if soundCollector is later set in the GUI and there's an online-only synth?
    if to_transliterate: # for partials: return a synth that can transliterate the language, if possible
        for synth in viable_synths:
            if synth.supports_language(language) and synth.can_transliterate(language): return synth
        if language=="zh": return simpleZhTransliterator # in case haven't got eSpeak
    for synth in viable_synths:
        if synth.supports_language(language) and not synth.not_so_good_at(language):
            getsynth_cache[language]=synth ; return synth
    for synth in viable_synths:
        if synth.supports_language(language):
            getsynth_cache[language]=synth ; return synth
    if (not warn) or language not in [firstLanguage,secondLanguage]+possible_otherLanguages: return None # without printing a warning
    if not language in warned_about_nosynth:
        warned_about_nosynth[language] = 1
        canSay = []
        if language in synth_partials_voices: canSay.append("recorded syllables (partials)")
        if synthCache: canSay.append("recorded phrases (synthCache)")
        if canSay: canSay="\n  - can use only "+" and ".join(canSay)
        else: canSay="\n  (did you read ALL the comments in vocab.txt?)"
        show_warning(("Warning: No speech synthesizer installed for language '%s'"+cond(appuifw or winCEsound,"",canSay)) % (language,))
    return None # and do NOT set getsynth_cache (see parseSynthVocab)

def synth_event(language,text,is_prompt=0):
    synth = get_synth_if_possible(language) ; assert synth, "Cannot get synth for '%s'" % (language,)
    return SynthEvent(text,synth,language,is_prompt)

def pinyin_uColon_to_V(pinyin):
    pinyin = pinyin.lower()

    pristineU = unichr(0xfc).encode('utf-8')
    pinyin = pinyin.replace("j"+pristineU,"ju").replace("q"+pristineU,"qu").replace("x"+pristineU,"xu").replace(pristineU,"v").replace(unichr(0xea).encode('utf-8'),"e") # for pristine's pinyin
    
    return pinyin.replace("u:","v").replace("leu","lv").replace("neu","nv")

class SynthEvent(Event):
    def __init__(self,text,synthesizer,language,is_prompt=0):
        assert text,"Trying to speak zero-length text"
        self.text = text ; self.synthesizer = synthesizer
        self.modifiedText = self.text
        if language=="en":
            self.modifiedText = self.modifiedText.replace("\xE2\x80\xA7","").replace("\xE2\x80\xB2","") # remove syllable boundaries and primes (usually just confuse speech synths)
            if not self.text[-1] in ";.!?-" and not (';' in self.text and ';' in self.text[self.text.index(';')+1:]): self.modifiedText += ';' # prosody hack (some synths sound a bit too much like 'disjointed strict commands' without this)
        elif language=="zh":
            # normalise pinyin
            # (note - this code is NOT used for partials synth, only for passing to espeak etc.  see elsewhere for partials synth)
            self.modifiedText = pinyin_uColon_to_V(self.modifiedText) # includes .lower()
            # and put space between every syllable of w, if it's one word only (the Lily voice seems to stand a better chance of getting it right that way, and occasionally other voices do too, e.g. "chang2yuan3" in at least some versions of eSpeak, not to mention Loquendo Lisheng
            for t in ["1","2","3","4","5"]: self.modifiedText = self.modifiedText.replace(t+"-",t+" ") # for Lily, Lisheng etc.  NB replace hyphen with space not with "", otherwise can get problems with phrases like "wang4en1-fu4yi4".  DON'T do it except after tone marks, because for hanzi we might want to use hyphens for word-boundary disambiguation.
            if (not " " in self.modifiedText) and ("1" in self.modifiedText or "2" in self.modifiedText or "3" in self.modifiedText or "4" in self.modifiedText or "5" in self.modifiedText):
                self.modifiedText=fix_pinyin(self.modifiedText,[]) # better call that before doing the following (in case any digits in the wrong place)
                for f in py_final_letters:
                    for t in "12345": self.modifiedText=self.modifiedText.replace(f+t,f+t+" ")
            if synthesizer.__class__ in [GeneralSynth, GeneralFileSynth]:
                # some e.g. eSpeak use capitals to start a new sentence, so need to undo some of the .lower() that pinyin_uColon_to_V did.
                # (ESpeakSynth already calls fix_commas in play() and makefile() so don't need to do it here.)
                self.modifiedText=fix_commas(fix_compatibility(ensure_unicode(self.modifiedText)).encode('utf-8'))
            elif synthesizer.__class__ in [PttsSynth]: self.modifiedText = sort_out_pinyin_3rd_tones(self.modifiedText) # for Lily, and in some cases for Lisheng
        self.language = language
        self.is_prompt = is_prompt ; self.sound = None
        if soundCollector and lessonIsTight():
            # non-realtime and a tight-fitting lesson, so it's worth taking time to calculate length more accurately
            self.sound = synthesizer.makefile_cached(language,self.modifiedText) ; synthesizer.finish_makefile()
            length = SampleEvent(self.sound).length
        else: length = synthesizer.guess_length(language,self.modifiedText)
        Event.__init__(self,length)
    def __repr__(self):
        if not self.language: return eventList_repr(self.text) # partials-synth list
        return str(self.text)
    def __setstate__(self,state):
        synth = get_synth_if_possible(state['language'])
        assert synth, "Error: Trying to play a previously-stored lesson under conditions that prevent one of the speech synths from working as before (maybe trying to use an online-only synth offline?)"
        self.__init__(state['text'],synth,state['language'],state['is_prompt'])
    def __getstate__(self): return {"text":self.text,"language":self.language,"is_prompt":self.is_prompt}
    def makesSenseToLog(self): return not self.is_prompt
    def will_be_played(self):
        if not soundCollector and not hasattr(self.synthesizer,"play"):
            self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText) # don't need to do that here if soundCollector, do it on demand below (it might get partially cancelled anyway).  Only need to do it here if generating ahead of real-time.
        else: self.sound = None # in case restoring a lesson that was previously to file but now to speaker (TODO is this still necessary now got __setstate__ above?)
    def getSound(self): # used in caching
        if not self.sound: self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText)
        return self.sound
    def play(self):
        if soundCollector and not self.sound:
            self.sound = self.synthesizer.makefile_cached(self.language,self.modifiedText)
            self.synthesizer.finish_makefile()
        if sample_table_hack:
            if not self.sound in sample_table_hack_lengthDic: sample_table_hack_lengthDic[self.sound]=SampleEvent(self.sound).exactLen
            soundCollector.addFile(self.sound,sample_table_hack_lengthDic[self.sound])
            open(self.sound,"wb") # i.e. truncate at 0 bytes to save space (but keep around so no name clashes)
        elif self.sound:
            # If synthesizing asynchronously, hopefully self.sound will have been synthesized by now, but just in case, we'll have a loop
            for t in range(10):
                try: e = SampleEvent(self.sound)
                except IOError:
                    time.sleep(1) ; continue
                return e.play()
            raise IOError("IOError after 10 tries on "+repr(self.sound))
        else:
            assert (not soundCollector) and hasattr(self.synthesizer,"play"),"Should have called will_be_played before playing offline"
            return self.synthesizer.play(self.language,self.modifiedText)
sample_table_hack_lengthDic = {}

class ShellEvent(Event): # used in just_synthesize below, and in concatenative synth as an optimisation on some platforms
    def __init__(self,command,retryOnFail=False):
        Event.__init__(self,0)
        self.command = command
        self.retryOnFail = retryOnFail
    def play(self):
        if soundCollector and hasattr(self,"equivalent_event_list"):
            for e in self.equivalent_event_list:
                if type(e)==type([]): # we have a list of lists-separated-by-pauses
                    for ee in e: ee.play()
                elif e.__class__==Event: soundCollector.addSilence(e.length,False)
                else: e.play()
            return
        elif hasattr(self,"VolReplace"): r = system(self.command.replace("$Vol$",str(eval(self.VolReplace))))
        else: r = system(self.command)
        if self.retryOnFail: return r # else None
    def makesSenseToLog(self): return hasattr(self,"is_prompt") and not self.is_prompt
    def __repr__(self):
        if hasattr(self,"equivalent_event_list"): return eventList_repr(self.equivalent_event_list)
        else: return "ShellEvent: "+self.command

def eventList_repr(el):
    r=[]
    def fname(p):
        if os.sep in p: p=p[p.rindex(os.sep)+1:]
        if extsep in p: p=p[:p.rindex(extsep)]
        return p
    for e in el:
        if type(e)==type([]) or hasattr(e,"eventList"):
            if not type(e)==type([]): e=e.eventList
            for ee in e:
                if not ee.__class__==Event: r.append(fname(str(ee)))
            r.append(",")
        elif not e.__class__==Event: r.append(fname(str(e)))
    return " ".join(r)

def abspath_from_start(p): # for just_synthesize to check for paths relative to the original starting directory if this is different from the gradint directory (see system.py)
    d=os.getcwd()
    os.chdir(starting_directory)
    try: r=os.path.abspath(p)
    except: r="" # library problems on Windows?
    os.chdir(d)
    return r

def just_synthesize(callSanityCheck=0,lastLang_override=None):
    # Handle the justSynthesize setting (see advanced.txt)
    global startAnnouncement,endAnnouncement,logFile,synth_partials_cache
    synth_partials_cache = {} # to stop 'memory leak' when running from the GUI
    oldStart,oldEnd,oldLogfile = startAnnouncement,endAnnouncement,logFile
    startAnnouncement=endAnnouncement=logFile=None
    if app: app.setLabel("") # not "wait a moment"
    called_synth = 0
    # we re-generate the lesson on each repeat, so sporadic-synthcache stuff works
    global repeatMode ; repeatMode = 1
    while repeatMode and not repeatMode=="interrupted":
      repeatMode = 0
      less = Lesson()
      lastStartTime = lastEndTime = lastWasDelay = 0
      if lastLang_override: lastLanguage = lastLang_override
      else: lastLanguage = secondLanguage
      def checkCanSynth(fname):
          ret=can_be_synthesized(fname)
          if ret: return fileToEvent(fname)
          else: show_warning("Can't say "+repr(fname)) # previous warnings should have said why (e.g. partials-only language)
      for line in justSynthesize.split('#'):
        line = line.strip(wsp) ; l = line.split(None,1)
        if extsep in line and fileExists(line): event = fileToEvent(line,"")
        elif extsep in line and fileExists(abspath_from_start(line)): event = fileToEvent(abspath_from_start(line),"")
        elif line=='R':
            repeatMode=1 ; continue
        elif len(l)==1:
            try: delayVal = float(l[0])
            except ValueError: delayVal = None
            if delayVal==None:
                # no float value; assume it's a single word to synth in secondLanguage or whatever was the last language used
                show_warning("Assuming that %s is a word to synthesize in language '%s'" % (repr(l[0]),lastLanguage))
                if callSanityCheck and sanityCheck(l[0],lastLanguage,1): return
                event = checkCanSynth("!synth:"+l[0]+"_"+lastLanguage)
                if not event: continue # couldn't synth
                called_synth = 1
            else:
                lastWasDelay = 1
                if delayVal<0: lastEndTime = lastStartTime-delayVal
                else: lastEndTime += delayVal
                continue
        elif len(l)==2:
            lang, text = l
            if lang=="sh:": event = ShellEvent(text)
            else:
                fname = "!synth:"+text+"_"+lang
                if not can_be_synthesized(fname):
                    if lang in [firstLanguage,secondLanguage]+otherLanguages:
                        show_warning("Can't say %s in %s" % (repr(text),repr(lang)))
                        lastLanguage=lang ; continue
                    # otherwise, user might have omitted lang by mistake
                    show_warning("Assuming %s was meant to be synthesized in language '%s'" % (cond('#' in justSynthesize or len(repr(line))<10,"that '"+repr(line)+"'","this line"),lastLanguage))
                    if callSanityCheck and sanityCheck(line,lastLanguage,1): return
                    event = checkCanSynth("!synth:"+line+"_"+lastLanguage)
                else:
                    if callSanityCheck and sanityCheck(text,lang,1): return
                    event = checkCanSynth(fname)
                    lastLanguage = lang
                if not event: continue
                called_synth = 1
        else: continue # len(l)==0: ignore empty strings between #s
        event.addToEvents(less.events,lastEndTime)
        lastWasDelay = 0
        lastStartTime = lastEndTime
        lastEndTime += event.length
      if lastWasDelay: Event(0).addToEvents(less.events,lastEndTime)
      global dbase ; dbase = None # for handleInterrupt
      less.play()
    startAnnouncement,endAnnouncement,logFile = oldStart,oldEnd,oldLogfile
    if repeatMode=="interrupted": sys.exit(1) # better tell the calling script
    if not called_synth: return None
    return lastLanguage

# Start of makeevent.py - make events from recorded words,
# synthesized words, cached synthesized words, or partials

def filesToEvents(files,dirBase=None):
    # Normally will be one file, but might be a list
    # (e.g. when learning poetry, may have a composite
    # prompt)
    if not type(files)==type([]): files = [files]
    return CompositeEvent(map(lambda x:fileToEvent(x,dirBase),files))

class Partials_Synth(Synth):
    # text is really a list of lists of filenames
    # TODO if there's a SoundCollector, and if header.wav matches its desired parameters, we can feed bytes directly to it rather than making a temp file; could be useful in environments with Flash disks (NSLU2 etc). (Could have WAV partials there instead, but the resulting number of wav-to-raw sox conversions can slow down SoundCollector on large texts (TODO document this))
    def guess_length(self,lang,text):
        l=(len(text)-1)*0.3
        for phrase in text: l+=quickGuess(len(phrase),1.5) # TODO assumes average of 1.5 partials/sec; needs to be better than that
        return l
    def play(self,lang,text):
        if len(text)<=2 or self.guess_length(lang,text)<=10: return SampleEvent(self.makefile(lang,text),isTemp=1).play()
        # If it's big, it might be better to synth one phrase at a time.  (Unfortunately we can't pipeline this on all architectures.  Hopefully this synth-in-the-pauses is OK for now.)
        t=0
        for phrase in text:
            e=SampleEvent(self.makefile(lang,[phrase]),isTemp=1)
            time.sleep(max(0,betweenPhrasePause-(time.time()-t)))
            e.play()
            t=time.time()
    def makefile(self,lang,text):
        # text is a list of syllable-lists
        # the first syllable in 1st list can optionally be the header file to use
        fname = os.tempnam()+dotwav
        o=open(fname,"wb")
        if not (text and text[0] and text[0][0].endswith(dotwav)): o.write(read(partialsDirectory+os.sep+"header"+dotwav))
        for phrase in text:
            datFileInUse = 0 ; assert type(phrase)==type([])
            for f in phrase:
                if f in audioDataPartials:
                    datFile,offset,size = audioDataPartials[f]
                    if not datFileInUse: datFileInUse = open(partialsDirectory+os.sep+datFile,"rb")
                    datFileInUse.seek(offset) ; o.write(datFileInUse.read(size))
                else: o.write(read(partialsDirectory+os.sep+f))
            if not phrase==text[-1]: o.write(chr(0)*partials_raw_0bytes) # TODO what if there's a duplicate of text[-1]
        # MUST fix the length, for Windows etc:
        wavLen = o.tell()-8
        o.seek(4) ; o.write(chr(wavLen&0xFF)+chr((wavLen>>8)&0xFF)+chr((wavLen>>16)&0xFF)+chr(wavLen>>24))
        wavLen -= 36 ; o.seek(40) ; o.write(chr(wavLen&0xFF)+chr((wavLen>>8)&0xFF)+chr((wavLen>>16)&0xFF)+chr(wavLen>>24))
        return fname

def fileToEvent(fname,dirBase=None):
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    orig_fname = fname
    if os.sep in fname and fname.find("!synth:")==-1: dirBase,fname = dirBase+fname[:fname.rindex(os.sep)+1], fname[fname.rindex(os.sep)+1:]
    if "_" in fname: lang = languageof(fname)
    else: lang="-unknown-" # so can take a simple wav file, e.g. for endAnnouncement
    if dirBase+fname in variantFiles:
        variantFiles[dirBase+fname]=variantFiles[dirBase+fname][1:]+[variantFiles[dirBase+fname][0]] # cycle through the random order of variants
        fname=variantFiles[dirBase+fname][0]
    if fname.lower().endswith(dottxt) and "_" in fname: fname = "!synth:"+u8strip(read(dirBase+fname)).strip(wsp)+'_'+lang
    if fname.find("!synth:")>=0:
        s = synthcache_lookup(fname)
        if type(s)==type([]): # trying to synth from partials
            if filter(lambda x:not type(x)==type([]), s): # but not completely (switching between partials and synth in a long text), this is more tricky:
                eList = []
                for phrase in s:
                    if type(phrase)==type([]):
                      if partials_raw_mode: eList.append(synth_event(None,[phrase]))
                      else: eList.append(optimise_partial_playing(CompositeEvent(map(lambda x:SampleEvent(partialsDirectory+os.sep+x,useExactLen=True),phrase))))
                    else: eList.append(phrase) # it will be a SynthEvent
                    eList.append(Event(betweenPhrasePause))
                e = CompositeEvent(eList[:-1]) # omit trailing pause
            elif partials_raw_mode: e=synth_event(None,s)
            else: e=optimise_partial_playing_list([CompositeEvent(map(lambda x:SampleEvent(partialsDirectory+os.sep+x,useExactLen=True),phrase)) for phrase in s]) # (tell SampleEvent to useExactLen in this case - don't want ANY pause between them)
            if not e: # can't make a ShellEvent from the whole lot; try making individual ShellEvents:
                e=[]
                for phrase in s:
                    e.append(optimise_partial_playing(CompositeEvent(map(lambda x:SampleEvent(partialsDirectory+os.sep+x,useExactLen=True),phrase))))
                    e.append(Event(betweenPhrasePause))
                e=CompositeEvent(e[:-1]) # omit trailing pause
            if not lessonIsTight(): e.length=math.ceil(e.length) # (TODO slight duplication of logic from SampleEvent c'tor)
        elif s: e=SampleEvent(synthCache+os.sep+s) # single file in synth cache
        else: e=synth_event(languageof(fname),textof(fname))
        e.is_prompt=(dirBase==promptsDirectory+os.sep)
    else: e=SampleEvent(dirBase+fname)
    e.setOnLeaves('wordToCancel',orig_fname)
    return e

transTbl = "TRANS"+extsep+"TBL"
if mp3web: # synth-cache must exist
    if not synthCache: synthCache = "synth-cache"
    try: os.mkdir(synthCache)
    except: pass # already exists, temporarily-dangling symlink, etc

if synthCache:
    # this listdir() call can take ages on rpcemu if it's large
    if riscos_sound: show_info("Reading synthCache... ")
    try: synthCache_contents = os.listdir(synthCache)
    except: synthCache_contents = synthCache = []
    for i in synthCache_contents:
        if i.upper()==transTbl: # in case it's a different case
            transTbl=i ; break
    synthCache_contents = list2dict(synthCache_contents) # NOT 2set, as the GUI can delete things from it
    if riscos_sound: show_info("done\n")
synthCache_transtbl = {}
if synthCache and transTbl in synthCache_contents:
    ensure_nodups = {} # careful of duplicate filenames being appended to trans.tbl, make sure they override previous entries
    for l in open(synthCache+os.sep+transTbl).readlines():
        v,k = l.strip(wsp).split(None,1)
        if v in ensure_nodups: del synthCache_transtbl[ensure_nodups[v]]
        ensure_nodups[v]=k ; synthCache_transtbl[k]=v
    del ensure_nodups
def textof(fname): return fname[fname.find('!synth:')+7:fname.rfind('_')]
last_partials_transliteration = None
synth_partials_cache = {} ; scl_disable_recursion = 0
def synthcache_lookup(fname,dirBase=None,printErrors=0,justQueryCache=0,lang=None):
    # if justQueryCache (used by the GUI), return value is (synthCache_transtbl key, result if any).  If key starts with _, we got a sporadic one.  (If =2, query sporadic ones but also try partials, used for can_be_synthesized)
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    if not lang: lang = languageof(fname)
    if fname.lower().endswith(dottxt):
        try: fname = fname[:fname.rfind("_")]+"!synth:"+u8strip(read(dirBase+fname)).strip(wsp)+"_"+lang
        except IOError: return 0,0 # probably trying to synthcache_lookup a file with variants without first choosing a variant (e.g. in anticipation() to check for sporadic cache entries in old words) - just ignore this
    text = textof(fname)
    useSporadic = -1 # undecided (no point accumulating counters for potentially-unbounded input)
    if justQueryCache: useSporadic,tryHarder=1,0
    else: tryHarder = not get_synth_if_possible(lang,0) # (tryHarder = always use sporadic if can't synth from partials, because there's no other synth to fall back on)
    if synthCache:
      for init in "_","":
        for ext in "wav","mp3":
            k=init+text.lower()+"_"+lang+extsep+ext
            s=synthCache_transtbl.get(k,k)
            if s in synthCache_contents: ret=s
            elif s.lower().endswith(dotwav) and s[:-len(dotwav)]+dotmp3 in synthCache_contents: ret=s[:-len(dotwav)]+dotmp3
            else: ret=0
            if ret:
                if justQueryCache==1: ret=(k,ret)
                if init=="_":
                    if useSporadic==-1: useSporadic=decide_subst_synth(text)
                    if useSporadic: return ret
                    elif tryHarder: tryHarder=ret
                else: return ret
    if justQueryCache==1: return 0,0
    if lang not in synth_partials_voices: l,translit=None,None # don't bother trying to transliterate here if there aren't even any partials for that language
    elif (lang,text) not in synth_partials_cache:
        # See if we can transliterate the text first.
        synth,translit = get_synth_if_possible(lang,0,to_transliterate=True),None
        if espeak_language_aliases.get(lang,lang) in ["zhy","zh-yue"]:
          text2=preprocess_chinese_numbers(fix_compatibility(ensure_unicode(text)),isCant=1).encode('utf-8')
          if ekho_speed_delta and type(get_synth_if_possible(lang,0))==EkhoSynth: return # don't use partials at all if they've got ekho and have set a different speed (TODO unless they've also changed the speed of the partials? but that would impair the quality advantage of using partials anyway)
        else: text2=text
        if synth: translit=synth.transliterate(lang,text2)
        if translit: t2=translit
        else: t2=text2
        if lang=="zh": t2=sort_out_pinyin_3rd_tones(pinyin_uColon_to_V(t2)) # need to do this BEFORE stripPuncEtc, for correct sandhi blocking
        phraseList = stripPuncEtc(t2.lower())
        l = [synth_from_partials(phrase,lang) for phrase in phraseList] # TODO do we really want to be able to pick new voices at every phrase?  if not, would have to pass the pause points into synth_from_partials itself
        if None in l: # at least one of the partials-phrases failed
          global scl_disable_recursion
          if len(t2)<100 or not filter(lambda x:x,l) or scl_disable_recursion: l=None # don't mix partials and synth for different parts of a short phrase, it's too confusing (TODO make the 100 configurable?)
          elif type(get_synth_if_possible(lang,0))==EkhoSynth: l=None # some faulty versions of Ekho are more likely to segfault if called on fragments (e.g. if the fragment ends with some English), so don't do this with Ekho (unless can confirm it's at least ekho_4.5-2ubuntu10.04 .. not all versions of ekho can report their version no.)
          else: # longer text and SOME can be synth'd from partials: go through it more carefully
            t2=fix_compatibility(ensure_unicode(text2.replace(chr(0),"")).replace(u"\u3002",".").replace(u"\u3001",",")).encode('utf-8')
            for t in ".!?:;,": t2=t2.replace(t,t+chr(0))
            l=[]
            scl_disable_recursion = 1
            for phrase in filter(lambda x:x,t2.split(chr(0))):
              ll=synthcache_lookup("!synth:"+phrase+"_"+lang,dirBase,0,0,lang)
              if type(ll)==type([]): l += ll
              else: l.append(synth_event(lang,phrase,0))
            scl_disable_recursion = 0
        synth_partials_cache[(lang,text)]=(l,translit)
    else: l,translit=synth_partials_cache[(lang,text)]
    if l and partials_are_sporadic:
        if useSporadic==-1: useSporadic=decide_subst_synth(("partials",text))
        if not useSporadic: l=translit=None
    if l and translit: # record it for the GUI
        global last_partials_transliteration
        last_partials_transliteration=translit
    if l: return l
    if tryHarder and not tryHarder==True: return tryHarder
    if printErrors and synthCache and not (app and winsound):
        r = repr(text.lower()+"_"+lang)
        if len(r)>100: r=r[:100]+"..."
        global NICcount
        try: NICcount += 1
        except: NICcount=1
        if NICcount>20: pass
        elif NICcount==20: show_info("Further 'not in cache' warnings turned off\n",True) # (important on S60 etc; TODO configurable?)
        else: show_info("Not in cache: "+r+"\n",True)
def can_be_synthesized(fname,dirBase=None,lang=None):
    if dirBase==None: dirBase=samplesDirectory
    if dirBase: dirBase += os.sep
    if not lang: lang = languageof(fname)
    if get_synth_if_possible(lang,0): return True
    elif synthcache_lookup(fname,dirBase,1,2,lang): return True
    else: return get_synth_if_possible(lang) # and this time print the warning
def stripPuncEtc(text):
    # For sending text to synth_from_partials.  Removes spaces and punctuation from text, and returns a list of the text split into phrases.
    for t in " -_'\"()[]": text=text.replace(t,"")
    for t in ".!?:;": text=text.replace(t,",")
    return filter(lambda x:x,text.split(","))

for zipToCheck in ["yali-voice","yali-lower","cameron-voice"]:
    if riscos_sound:
        if fileExists(zipToCheck+"/exe") or fileExists(samplesDirectory+"."+zipToCheck+"/exe") or fileExists(os.getcwd()[:os.getcwd().rindex(".")]+"."+zipToCheck+"/exe"): show_warning("RISC OS users: Please rename the file "+zipToCheck+"/exe to "+zipToCheck+"/zip and unpack it into the gradint directory.")
    elif not winsound: # ok if mingw32, appuifw etc (unzip_and_delete will warn)
        for d in [os.getcwd()+cwd_addSep,".."+os.sep,samplesDirectory+os.sep]:
            f=d+zipToCheck+".exe"
            if fileExists(f): unzip_and_delete(f,ignore_fail=1) # ignore the error exit status from unzip, which will be because of extra bytes at the beginning

# Filename / Unicode translation - need some safety across filesystems.  synthCache(+utils) could be done this way also rather than having TRANS.TBL (however I'm not sure it would save that much code)
non_normal_filenames = {} ; using_unicode_filenames=0
def filename2unicode(f):
    if type(f)==type(u""):
        global using_unicode_filenames
        using_unicode_filenames = 1
        return f
    def u8_or_raw(s):
        try: return unicode(s,"utf-8")
        except UnicodeDecodeError: return unicode(s,"latin1") # (actually should try the local codepage on Windows for correct display, but at least this stops a crash)
    if f.find("_u")>=0 or f.find("_U")>=0:
        try: return unicode(f.replace("_u","\\u").replace("_U","\\u"),"unicode_escape")
        except UnicodeDecodeError: # oops, need to be more careful
            ret = []
            while True:
                i = f.lower().find("_u")
                if i==-1: break
                ret.append(u8_or_raw(f[:i]))
                f=f[i:]
                try:
                    r=unicode("\\u"+f[2:6],"unicode_escape")
                    f=f[6:]
                except UnicodeDecodeError:
                    r=f[:2] ; f=f[2:]
                ret.append(r)
            return u"".join(ret+[f])
    u=u8_or_raw(f)
    if filter(lambda x:ord(x)>=128, list(u)): non_normal_filenames[u] = f # make at least some attempt to keep the old one for GUI rename()s etc, TODO this might not always cope with directories in the path being non-normal, so let's hope they don't set that up manually and then expect the GUI to cope with it
    return u
def unicode2filename(u):
    if using_unicode_filenames: return u
    if u in non_normal_filenames: return non_normal_filenames[u]
    f=u.encode("unicode_escape").replace("\\u","_u")
    for unsafe_char in "?+*<=": f=f.replace(unsafe_char,"_u%04x" % ord(unsafe_char))
    return f

synth_partials_voices = {} # lang -> list of voices, each being a tuple of (directory,startDict,midDict,endDict,flags); see comments below for the dictionary format
partials_cache_file="partials-cache"+extsep+"bin"
partials_language_aliases = {}
if partialsDirectory and isDirectory(partialsDirectory):
  dirsToStat = []
  partialsCacheFormat="(partials_raw_mode,synth_partials_voices,guiVoiceOptions,audioDataPartials,dirsToStat,espeak_language_aliases,partials_language_aliases)"
  if pickle and fileExists(partials_cache_file):
    try:
        ela = espeak_language_aliases
        format,values = pickle.Unpickler(open(partials_cache_file,"rb")).load()
        if format==partialsCacheFormat: exec format+"=values"
        if not (ela==espeak_language_aliases and dirsToStat[0][0]==partialsDirectory): espeak_language_aliases,dirsToStat=ela,[]
        del ela,format,values
    except MemoryError: raise # has been known on winCEsound when we're a library module (so previous memory check didn't happen)
    except: dirsToStat = []
    for d,result in dirsToStat:
      if not tuple(os.stat(d))==result:
        dirsToStat=[] ; break
  if not dirsToStat: # need to re-scan
    if riscos_sound or winCEsound: show_info("Scanning partials... ")
    guiVoiceOptions = []
    langs = os.listdir(partialsDirectory)
    dirsToStat.append((partialsDirectory,os.stat(partialsDirectory)))
    audioDataPartials = {} ; synth_partials_voices = {}
    partials_raw_mode = "header"+dotwav in langs
    for l in langs:
        try: voices = os.listdir(partialsDirectory+os.sep+l)
        except: voices = []
        if voices: dirsToStat.append((partialsDirectory+os.sep+l,os.stat(partialsDirectory+os.sep+l)))
        thisLangVoices = [] ; voices.sort()
        for v in voices:
            if "-" in v and v[:v.index("-")] in voices:
              suffix=v[v.index("-"):]
              if not suffix in guiVoiceOptions: guiVoiceOptions.append(suffix)
            start,mid,end = [],[],[] ; flags=0
            try: files = os.listdir(partialsDirectory+os.sep+l+os.sep+v)
            except: files = []
            if files: dirsToStat.append((partialsDirectory+os.sep+l+os.sep+v,os.stat(partialsDirectory+os.sep+l+os.sep+v)))
            def addFile(f):
                global flags
                if riscos_sound and "." in f: f=f.replace(".",extsep) # in case made filelist on another system
                if f=="!calibrated":
                    flags|=1 # calibrated
                if partials_raw_mode and f=="header"+dotwav:
                    flags|=2 # has a separate header.wav
                if f=="audiodata"+extsep+"dat": # parse audiodata.dat
                    dirsToStat.append((partialsDirectory+os.sep+l+os.sep+v+os.sep+f,os.stat(partialsDirectory+os.sep+l+os.sep+v+os.sep+f)))
                    offset=0 ; f=l+os.sep+v+os.sep+f
                    ff=open(partialsDirectory+os.sep+f,"rb")
                    amend = []
                    while True:
                        fftell = ff.tell()
                        char = ff.read(1)
                        if not "0"<=char<="9": break
                        size,fname = (char+ff.readline(256)).strip(wsp).split(None,1)
                        try: size=int(size)
                        except: break # binary just happened to start with "0"-"9"
                        addFile(fname)
                        amend.append(l+os.sep+v+os.sep+fname)
                        audioDataPartials[l+os.sep+v+os.sep+fname] = (f,offset,size)
                        offset += size
                    for k in amend: audioDataPartials[k]=(audioDataPartials[k][0],audioDataPartials[k][1]+fftell,audioDataPartials[k][2])
                    del ff,amend,offset
                if partials_raw_mode:
                    if not f.endswith(extsep+"raw"): return
                elif not f.endswith(dotwav) or f.endswith(dotmp3): return
                if f.find("-s")>=0 or f.find("-i")>=0: start.append(f) # 'start' or 'initial'
                elif not "-" in f or f.find('-m')>=0: mid.append(f)
                elif f.find('-e')>=0 or f.find('-f')>=0: end.append(f) # 'end' or 'finish'
            for f in files: addFile(f)
            def byReverseLength(a,b): return len(b)-len(a)
            start.sort(byReverseLength) ; mid.sort(byReverseLength) ; end.sort(byReverseLength) # important if there are some files covering multiple syllables (and do it to start,mid,end not to files initially, so as to catch files within audiodata.dat also)
            def toDict(l): # make the list of filenames into a dict of short-key -> [(long-key, filename) list].  short-key is the shortest possible key.
                if not l: return {}
                l2 = [] ; kLen = len(l[0])
                for i in l:
                    if "-" in i: key=i[:i.index("-")]
                    else: key=i[:i.rindex(extsep)]
                    if key.find("_u")>=0 or key.find("_U")>=0: # a unicode partial with a portable filename?
                        key = filename2unicode(key).encode('utf-8')
                    l2.append((key,i))
                    kLen=min(kLen,len(key))
                l = {}
                for k,i in l2:
                    if not k[:kLen] in l: l[k[:kLen]]=[]
                    l[k[:kLen]].append((k,i))
                return l
            thisLangVoices.append((v,toDict(start),toDict(mid),toDict(end),flags))
        synth_partials_voices[l] = thisLangVoices
        if l in espeak_language_aliases: partials_language_aliases[espeak_language_aliases[l]]=l
    if riscos_sound or winCEsound: show_info("done\n")
    if pickle:
      try: pickle.Pickler(open(partials_cache_file,"wb"),-1).dump((partialsCacheFormat,eval(partialsCacheFormat)))
      except IOError: pass # ignore write errors as it's only a cache
      except OSError: pass
  if partials_raw_mode:
    (wtype,wrate,wchannels,wframes,wbits) = sndhdr.what(partialsDirectory+os.sep+"header"+dotwav)
    partials_raw_0bytes = int(betweenPhrasePause*wrate)*wchannels*(wbits/8)
else: synth_partials_voices,partials_raw_mode = {},None

if "cant" in synth_partials_voices: synth_partials_voices["zhy"]=synth_partials_voices["zh-yue"]=synth_partials_voices["cant"]

def partials_langname(lang):
    lang = espeak_language_aliases.get(lang,lang)
    lang = partials_language_aliases.get(lang,lang)
    return lang

def synth_from_partials(text,lang,voice=None,isStart=1):
    lang = partials_langname(lang)
    text=text.strip(wsp) # so whitespace between words is ignored on the recursive call
    if lang=="zh": # hack for Mandarin - higher tone 5 after a tone 3 (and ma5 after 4 or 5 also)
        lastNum = None
        for i in range(len(text)):
            if text[i] in "123456":
                if text[i]=="5" and (lastNum=="3" or (lastNum>"3" and i>2 and text[i-2:i+1]=="ma5")): # (TODO ne5 also? but only if followed by some form of question mark, and that might have been dropped)
                    # see if we got a "tone 6" (higher tone 5)
                    # don't worry too much if we haven't
                    r=synth_from_partials(text[:i]+"6"+text[i+1:],lang,voice,isStart)
                    if r: return r
                    else: break
                elif lastNum: break # don't look beyond 1st 2
                lastNum = text[i]
    if not voice: # try all voices for the language, see if we can find one that can say all the necessary parts
        if not lang in synth_partials_voices: return None
        needCalibrated=False
        if lang=="zh": # hack for Mandarin - avoid consecutive 1st tones on non-calibrated voices
            # (DON'T do 3rd tone sandhi here - that's the caller's responsibility and we don't want it done twice now there's sandhi-blocking rules)
            lastNum=None
            for c in text:
                if c=="1" and lastNum=="1":
                    needCalibrated=True ; break # TODO: unless this syllable is exactly the same as the last syllable (a repeated syllable is always ok to use even if uncalibrated)
                if c in "123456": lastNum=c
            # end of hack for Mandarin
        vTry = synth_partials_voices[lang]
        if voiceOption:
            vt1=[] ; vt2=[]
            for v in vTry:
              if v[0].endswith(voiceOption): vt1.append(v)
              else: vt2.append(v)
            vTry=vt1+vt2
        for v in vTry:
            if needCalibrated and not v[-1]&1: continue
            r = synth_from_partials(text,lang,v)
            if r:
                if partials_raw_mode and v[-1]&2: r.insert(0,"header"+dotwav)
                return map(lambda x:lang+os.sep+v[0]+os.sep+x,r)
        return None
    dir, start, mid, end, flags = voice
    def lookup_dic(text,dic):
        if dic:
            for k,v in dic.get(text[:len(dic.keys()[0])],[]):
                if text.startswith(k): return k,v
        return None,None
    if not text: return [] # (shouldn't happen)
    k,v = lookup_dic(text,end)
    if text==k: return [v] # whole of (rest of) text matches a 'final' sound
    if isStart: preferredOrder = [start, mid]
    else: preferredOrder = [mid, start] # (can usually get away with re-using a 'start' sound as a 'mid' or vice versa, but can't usually use an 'end' as anything else without it sounding too 'choppy')
    for l in preferredOrder:
        k,v = lookup_dic(text,l)
        if k: # matched a syllable or so - can we do the rest?
            if text==k: return [v] # finished.  (Comment out this line to use *only* 'end' sounds at the end.)
            rest = synth_from_partials(text[len(k):],lang,voice,0)
            if rest==None: return None # (could ignore this match and carry on searching, but it's unlikely)
            else: return [v]+rest
    # Got to a character we cannot synth - probably best to fall back to a non-partials synth, but try to keep going if that's not possible
    if not get_synth_if_possible(lang,0):
        global warned_missing_chars
        if not warned_missing_chars: show_warning("Warning: Partials synth is IGNORING unrecognised characters in the input, because there is no fallback synth")
        warned_missing_chars=1
        return synth_from_partials(text[1:],lang,voice)
warned_missing_chars=0

def optimise_partial_playing(ce):
    # ce is a CompositeEvent of SampleEvents.  See if we can change it to a ShellEvent that plays all partial-samples in a single command - this helps with continuity on some low-end platforms.
    if soundCollector and not saveLesson: return ce # no point doing this optimisation if won't ever play in real time
    fileType = soundFileType(ce.eventList[0].file)
    hasPauses = 0
    for e in ce.eventList[1:]:
        if not soundFileType(e.file)==fileType: return ce # must be all the same type for this optimisation
    s = None
    if fileType=="mp3" and madplay_path and mp3Player==madplay_path and not macsound and not cygwin: # (don't do this on cygwin because cygwin will require changeToDirOf and that could get awkward)
        # mp3 probably has encoding gaps etc, but we can try our best
        if wavPlayer=="aplay": s=ShellEvent(mp3Player+' -q -A $Vol$'+''.join(map(lambda x:' "'+x.file+'"', ce.eventList))+' -o wav:-|aplay -q',True) # (set retryOnFail=True)
        else: s=ShellEvent(mp3Player+' -q -A $Vol$'+''.join(map(lambda x:' "'+x.file+'"', ce.eventList)),True)
        s.VolReplace="soundVolume_dB"
    elif (not fileType=="mp3") and (wavPlayer in ["aplay","sox"] or wavPlayer.strip().endswith("<")):
        # if they're all the same format, we can use sox concatenation (raw, with an unspecified-length wav header at start)
        # (don't try to do that if different formats - the low-end hardware may not take the rate conversion)
        ok=gotSox
        if ok:
            format = simplified_header(ce.eventList[0].file)
            for e in ce.eventList[1:]:
                if not simplified_header(e.file)==format:
                    ok=False ; break
        if ok:
            if wavPlayer=="aplay": wpMod="aplay -q"
            elif wavPlayer.strip().endswith("<"): wpMod=wavPlayer.strip()[:-1] # nc etc
            else: wpMod='sox -t wav - '+sox_type+' '+oss_sound_device
            s=ShellEvent('set -o pipefail;('+'&&'.join(['cat "%s" | sox -t %s - -t wav - $Vol$ 2>/dev/null' % (ce.eventList[0].file,fileType)]+['cat "%s" | sox -t %s - -t raw - $Vol$'%(e.file,fileType) for e in ce.eventList[1:]])+')'+sox_ignoreLen+'|'+wpMod,True)
            s.VolReplace="sox_effect"
        elif wavPlayer=="aplay" and not sox_effect: s=ShellEvent('aplay -q '+''.join(map(lambda x:' "'+x.file+'"', ce.eventList)),True) # (which is not quite as good but is the next best thing) (and hope they don't then try to re-play a saved lesson with a volume adjustment)
    if s:
        s.length = ce.length
        s.equivalent_event_list = ce.eventList
        return s
    else: return ce # can't figure out an optimisation in these circumstances
def simplified_header(fname):
    h=sndhdr.what(fname)
    # ignore num frames i.e. h[3], just compare formats
    if h: return h[:3]+h[4:]
def optimise_partial_playing_list(ceList):
    # similar to above, but returns a ShellEvent for a list of ce's that are to be separated by short pauses, or None if can't do this optimisation.  This is because sox on NSLU2's etc has too much latency for the short pauses.
    if (soundCollector and not saveLesson) or not wavPlayer=="aplay" or not gotSox: return
    format = None ; l = [] ; theLen = 0
    for ce in ceList:
        for e in ce.eventList:
            if not soundFileType(e.file)=="wav": return
            if not format: format=simplified_header(e.file)
            elif not format==simplified_header(e.file): return
            if not l: l.append('sox "%s" -t wav - $Vol$ 2>/dev/null' % (e.file,))
            else: l.append('sox "%s" -t raw - $Vol$'%(e.file,))
            theLen += e.length
        if not ce==ceList[-1]:
            l.append('dd if=/dev/zero bs=%d count=1 2>/dev/null' % (int(betweenPhrasePause*format[1])*format[2]*(format[-1]/8)))
            theLen += betweenPhrasePause
    s=ShellEvent('('+';'.join(l)+')'+sox_ignoreLen+'|aplay -q',True) # sox_ignoreLen is needed for newer 'sox' versions which manage to write the 1st syllable's length no matter how we try to stop it
    s.length = theLen
    s.VolReplace="sox_effect"
    s.equivalent_event_list = []
    for ce in ceList[:-1]:
        # equivalent_event_list can be a list of 'lists with pauses in between'.
        # Event()s are interpreted correctly only if preceeded by lists.  (TODO this is getting hacky)
        s.equivalent_event_list.append(ce.eventList)
        s.equivalent_event_list.append(Event(betweenPhrasePause))
    s.equivalent_event_list.append(ceList[-1])
    return s


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
                    except: write(destDir+os.sep+f,read(importDir+os.sep+f))
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
        if has_variants and file.find("_",file.find("_")+1)>=0: languageOverride=file[file.find("_")+1:file.find("_",file.find("_")+1)]
        else: languageOverride=None
        if filelower.endswith(dottxt) and (file+extsep)[:file.rfind(extsep)] in lsDic: continue # don't let a .txt override a recording if both exist
        if (filelower.endswith(dottxt) and file.find("_")>=0 and can_be_synthesized(file,directory,languageOverride)) or filelower.endswith(dotwav) or filelower.endswith(dotmp3): val = file
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
            if not v or (not directory==promptsDirectory and v.find("_explain_")>=0): continue # don't get confused by that
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
        elif '#' in l and l.strip(wsp)[0]=='#': continue # guard condition "'#' in l" improves speed
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
auto_advancedPrompt=0 # used by gradint.cgi
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
            if (not self.user_is_advanced) and not auto_advancedPrompt and cond(language==secondLanguage,advancedPromptThreshold,advancedPromptThreshold2): raise PromptException("Prompt '%s' is too advanced; need '%s_%s' (unless you set %s=0 in advanced%stxt)" % (advancedPrompt,prefix,firstLanguage,cond(language==secondLanguage,"advancedPromptThreshold","advancedPromptThreshold2"),extsep))
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
        if rates:
          for rate in [22050, 16000, 24000, 44100]:
            if rate in rates:
                self.rate = rate ; return
          self.rate = max(rates)
        else: self.rate = None
    def startRec(self,outFile,lastStopRecVal=None):
        if not self.rate: return self.err("Cannot record on this system (try aoss?)")
        try: self.sound = tkSnack.Sound(file=outFile, rate=self.rate, channels=1, encoding="Lin16")
        except: return self.err("Cannot write to sound file '"+outFile+"' with tkSnack")
        try: self.sound.record()
        except: # e.g. waveInOpen failed on Windows 7 (driver problems?)
            self.err("sound.record() failed")
            try: self.sound.stop()
            except: pass
            try: os.remove(outFile)
            except: pass
            del self.sound
    def err(self,msg): app.todo.alert=msg
    def stopRec(self):
        if hasattr(self,"sound"): self.sound.stop()

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
                write(self.fileToDel,read(fileToPlay))
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
        try: self.sound.play(start=curSample)
        except: app.todo.alert="tkSnack problem playing sound: try running gradint under aoss"
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
                try: os.rename(MacRecordingFile,self.fileToWrite)
                except: write(self.fileToWrite,read(MacRecordingFile)), os.remove(MacRecordingFile) # because there's a cross-device link problem or something
        tkSnack = "MicOnly"
  elif unix and useTK and isDirectory("/dev/snd") and got_program("arecord"): # no tkSnack, but can record via ALSA (but no point doing the tests if not useTK)
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
    if baseDir==outDir or baseDir.endswith(extsep+"zip"): return zipNo # omit the output dir, plus any existing ZIP files
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

def getAmplify(directory):
    statfile = os.tempnam()
    tmplist = []
    if unix: out2nul="-t wav /dev/null" # sox bug workaround on some versions
    elif winsound: out2nul="-t wav nul" # sox bug workaround
    else: out2nul="-t nul nul"
    for f in os.listdir(directory):
        factor = None
        if f.endswith(dotwav) and not system("sox \""+directory+os.sep+f+"\" "+out2nul+" stat 2> \""+statfile+"\""):
            for l in read(statfile).replace("\r","\n").split("\n"):
                if l.startswith("Volume adjustment:"): factor=l.split()[2]
        if not factor: continue
        tmplist.append([float(factor),f,factor])
    try: os.remove(statfile)
    except: pass
    if not tmplist: return [],"",0
    tmplist.sort()
    minFactor = tmplist[-1][0]/2 # amplify softest by at least half its required amp (TODO parameterise that 2)
    i=len(tmplist)-1
    while i>=0:
        if tmplist[i][0]<minFactor: break
        i -= 1
    i += 1
    if not tmplist[i][2]==tmplist[0][2]: tmplist[i][2]="%.3f" % (tmplist[i][0]/tmplist[0][0]) # don't make the softest ones louder than the existing loudest one
    if tmplist[i][2].startswith("1.0"): return [],"",len(tmplist)
    else: return map(lambda x:x[1],tmplist[i:]),tmplist[i][2],i

def doAmplify(directory,fileList,factor):
    failures = 0
    for f in fileList:
        if system("sox \""+directory+os.sep+f+"\" -t wav \""+directory+os.sep+"tmp0\" vol "+factor): failures += 1
        else:
            os.remove(directory+os.sep+f)
            os.rename(directory+os.sep+"tmp0",directory+os.sep+f)
    return failures

class ButtonScrollingMixin(object):
    # expects self.ourCanvas
    def bindFocusIn(self,b):
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
    def scrollIntoView(self,button):
        if hasattr(app,"justGotFocusIn"): return # ignore double <FocusIn> event - allows switch out of app and back in again w/out scrolling back to the keyboard-focused button
        self.scrollingIntoView = button
        self.continueScrollIntoView(button)
    def continueScrollIntoView(self,button):
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

class RecorderControls(ButtonScrollingMixin):
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
        self.bindFocusIn(b)
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
        rc = self.coords2buttons[(row,col)] = self.makeLabel_lenLimit(utext)
        rc.grid(row=row,column=col,sticky="w")
        if col==0:
          rc.bind('<Button-1>',lambda *args:self.startRename(row,col,utext))
          if not winCEsound:
            def contextMenu(e): # TODO: document this?
                m=Tkinter.Menu(None, tearoff=0, takefocus=0)
                m.add_command(label="Rename",command=lambda *args:self.startRename(row,col,utext))
                if self.currentDir.startswith(samplesDirectory): m.add_command(label="Add extra revision",command=lambda *args:self.addRevision(utext))
                m.add_command(label="Delete",command=lambda *args:self.delete(utext))
                m.tk_popup(e.x_root-3, e.y_root+3,entry="0")
            rc.bind('<ButtonRelease-3>',contextMenu)
            if macsound:
                rc.bind('<Control-ButtonRelease-1>',contextMenu)
                rc.bind('<ButtonRelease-2>',contextMenu)
    if not winCEsound:
      def delete(self,filename):
        toDel = [] ; fs=filename.encode('utf-8')
        for f in os.listdir(self.currentDir):
            if f.startswith(fs): toDel.append(f)
        if not toDel: return tkMessageBox.showinfo(filename,"No files found") # shouldn't happen
        if tkMessageBox.askyesno(filename,"Really delete "+" ".join(toDel)+"?"):
            for d in toDel: os.remove(self.currentDir+os.sep+d)
            self.undraw() ; self.draw() # TODO incremental update? (need to check really does affect just that row; careful with variants, synth, etc)
      def addRevision(self,filename):
        # c.f. gui_event_loop menu_response=="add" when already in vocabList
        app.set_watch_cursor = 1
        d = ProgressDatabase(0)
        found = 0
        curDir = self.currentDir[len(samplesDirectory)+len(os.sep):]
        if curDir: curDir += os.sep
        for item in d.data: # TODO: don't run this loop in the GUI thread!
            if not item[2].startswith(curDir+filename.encode('utf-8')+"_"): continue
            if not item[0]: break # not done yet
            newItem0 = reviseCount(item[0])
            if tkMessageBox.askyesno(filename,localise("Repeat count is %d. Reduce this to %d for extra revision?" % (item[0],newItem0))):
                d.data.remove(item)
                d.data.append((newItem0,item[1],item[2]))
                d.save()
            found = 1 ; break
        if not found: tkMessageBox.showinfo(filename,localise("Repeat count is 0, so we cannot reduce it for extra revision."))
    def makeLabel_lenLimit(self,utext): return Tkinter.Label(self.grid,text=utext,wraplength=int(self.ourCanvas.winfo_screenwidth()/(1+len(self.languagesToDraw))))
    def addSynthLabel(self,filename,row,col):
        try: ftext = ensure_unicode(u8strip(read(filename).strip(wsp)))
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
        try: editText.set(ensure_unicode(u8strip(read(filename).strip(wsp))))
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
    def amplify(self,*args):
        self.AmplifyButton["text"] = localise("Please wait") # TODO not in the GUI thread !! (but lock our other buttons while it's doing it)
        toAmp,factor,numOutliers = getAmplify(self.currentDir)
        if not toAmp:
            if numOutliers>1: app.todo.alert=localise("Found %d files but they were too loud to amplify") % numOutliers
            elif numOutliers: app.todo.alert=localise("Found 1 file but it was too loud to amplify")
            else: app.todo.alert=localise("No WAV files found in this folder")
        elif tkMessageBox.askyesno(app.master.title(),localise("Amplify %d files by %s? (exceptions: %d)") % (len(toAmp),factor,numOutliers)):
            f=doAmplify(self.currentDir,toAmp,factor)
            if f: app.todo.alert="%d sox failures" % f
        self.AmplifyButton["text"] = localise("Amplify")
    def all2mp3_or_zip(self,*args):
        self.CompressButton["text"] = localise("Compressing, please wait")
        if got_program("lame"): wavToMp3(self.currentDir) # TODO not in the GUI thread !! (but lock our other buttons while it's doing it)
        if got_program("zip") and (explorerCommand or winCEsound) and (not got_program("lame") or tkMessageBox.askyesno(app.master.title(),localise("All recordings have been compressed to MP3.  Do you also want to make a ZIP file for sending as email?"))):
            try: os.mkdir(self.currentDir+os.sep+"zips")
            except: pass # already exists?
            numZips = makeMp3Zips(self.currentDir,self.currentDir+os.sep+"zips")
            if numZips:
                openDirectory(self.currentDir+os.sep+"zips",1)
                if numZips>1: app.todo.alert=localise("Please send the %d zip files as %d separate messages, in case one very large message doesn't get through.") % (numZips,numZips)
                else: app.todo.alert=localise("You may now send the zip file by email.")
            else: app.todo.alert=localise("No recordings found")
        self.undraw() ; self.draw()
    def startRename(self,row,col,filename):
        if hasattr(self,"renameToCancel"):
          rr,cc = self.renameToCancel
          self.cancelRename(rr,cc)
        if self.has_variants and filename.find(" (")>=0:
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
        if number and ("0"<=number[0]<="9" or (len(number)>=2 and number[0]=="_" and "0"<=number[1]<="9")): # the format of addMore method
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
        try: origName = self.coords2buttons[(row,col)].origName
        except AttributeError: return # event must have fired twice for some reason?
        newNames = filter(lambda x:x,asUnicode(self.coords2buttons[(row,col)].theText.get()).split("\n")) # multiline paste, ignore blank lines
        for newName in newNames:
            if not origName: # extra lines - need to get their origNames
                if row==self.addMoreRow: self.addMore()
                elif not (row,col) in self.coords2buttons: row += 1 # skip extra row if there are notes
                origName=self.coords2buttons[(row,col)]["text"]
            if self.has_variants and origName.find(" (")>=0:
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
                for lang in list2set([firstLanguage,secondLanguage]+otherLanguages+self.languagesToDraw): # not just self.languagesToDraw, as a student of more languages than these might not have them all showing and still expect renames to work
                    updated=False
                    for ext in [dottxt, dotwav, dotmp3]:
                      if fileExists_stat(unicode2filename(self.currentDir+os.sep+origName+"_"+lang+ext)):
                        try: os.rename(unicode2filename(self.currentDir+os.sep+origName+"_"+lang+ext),unicode2filename(self.currentDir+os.sep+newName+"_"+lang+ext))
                        except:
                            tkMessageBox.showinfo(app.master.title(),localise("Could not rename %s to %s") % (origName+"_"+lang+ext,newName+"_"+lang+ext)) # TODO undo any that did succeed first!  + check for destination-already-exists (OS may not catch it)
                            return
                        if not lang in self.languagesToDraw: continue
                        self.updateFile(unicode2filename(newName+"_"+lang+ext),row,self.languagesToDraw.index(lang),cond(ext==dottxt,0,2)) # TODO the 2 should be 1 if and only if we didn't just record it
                        updated=True
                    if not updated and lang in self.languagesToDraw: self.updateFile(unicode2filename(newName+"_"+lang+dotwav),row,self.languagesToDraw.index(lang),0)
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
            if not tkSnack or tkSnack=="MicOnly" or wavPlayer_override: self.addButton(row,2+3*languageNo,text=localise("Play"),command=(lambda e=None,f=filename:(self.doStop(),SampleEvent(f).play())))  # but if got full tkSnack, might as well use setInputSource instead to be consistent with the non-_ version:
            else: self.addButton(row,2+3*languageNo,text=localise("Play"),command=(lambda e=None,f=filename:(self.doStop(),theISM.setInputSource(PlayerInput(f,not self.syncFlag)),self.setSync(False))))
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
            else: prefix = "word_%04d" % self.maxPrefix # if changing this, change startRename and selectAllButNumber also, AND the code that works out maxPrefix (and NB legacy collections).  TODO use of _ may not suit variants if in same dir.
            self.addLabel(self.addMoreRow,0,utext=prefix)
            for lang in self.languagesToDraw:
                self.updateFile(unicode2filename(prefix+"_"+lang+dotwav),self.addMoreRow,self.languagesToDraw.index(lang),state=0)
                self.gridLabel(lang,self.addMoreRow)
            self.addMoreRow += 2 ; self.maxPrefix += 1
        self.add_addMore_button()
    def gridLabel(self,lang,row): Tkinter.Label(self.grid,text=" "+localise(cond(lang.find("-meaning_")>=0,"meaning",lang))+": ").grid(row=row,column=1+3*self.languagesToDraw.index(lang))
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
            fname = "folder%d" % count # DON'T default its name to today's date etc, as this may make it less obvious what the GUI's renaming step is
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
        l=os.listdir(self.currentDir) ; l.sort()
        openDirectory(self.currentDir,1)
        tkMessageBox.showinfo(app.master.title(),localise("Gradint has opened the current folder for you to work on.  When you press OK, Gradint will re-scan the folder for new files."))
        l2=os.listdir(self.currentDir) ; l2.sort()
        if l==l2: return # no change
        self.undraw() ; self.draw()
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
        if hasattr(app,"isBigPrint") and winsound:
            # Vista sometimes has window placement problems here
            try: app.master.geometry("+0+0")
            except: pass
        if not self.snack_initialized:
            if tkSnack and not tkSnack=="MicOnly":
                tkSnack.initializeSnack(app)
                if paranoid_file_management:
                    if tkSnack.audio.playLatency()<500: tkSnack.audio.playLatency(500) # at least 500ms latency if we're paranoid_file_management, just in case (since tkSnack.audio.elapsedTime does not account for hold-ups)
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
          if hasattr(app,"isBigPrint") and macsound:
              # Try to make up for the fact that we can't always increase the width of the scrollbar (and the keyboard often loses focus).  Add extra up/down buttons. (TODO: does any other platform need this?)
              r2 = Tkinter.Frame(r)
              r2.pack({"side":"right"})
              addButton(r2,unichr(8593),lambda *args:app.ScrollUpHandler(),"left")
              addButton(r2,unichr(8595),lambda *args:app.ScrollDownHandler(),"left")
              Tkinter.Label(r,text="    ").pack({"side":"right"}) # TODO: more flexible spacer
              r = Tkinter.Frame(r)
              r.pack({"side":"right"})
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
        allLangs = list2set([firstLanguage,secondLanguage]+possible_otherLanguages)
        hadDirectories = False
        for fname in l:
            flwr = fname.lower() ; isMeaning=0
            if firstLanguage==secondLanguage and firstLanguage+"-meaning_"+secondLanguage in fname: isMeaning,languageOverride = True, firstLanguage+"-meaning_"+secondLanguage # hack for re-loading a dir of word+meaning in same language.  TODO hope not combining -meaning_ with variants
            elif self.has_variants and fname.find("_",fname.find("_")+1)>=0 and not fname.find("_explain_")>=0: languageOverride=fname[fname.find("_")+1:fname.find("_",fname.find("_")+1)]
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
                    if fileExists(self.currentDir+os.sep+fname+os.sep+longDescriptionName): description=u8strip(read(self.currentDir+os.sep+fname+os.sep+longDescriptionName)).strip(wsp)
                    elif fileExists(self.currentDir+os.sep+fname+os.sep+shortDescriptionName): description=u8strip(read(self.currentDir+os.sep+fname+os.sep+shortDescriptionName)).strip(wsp)
                    else: description=None
                    if description:
                        try: sbarWidth = app.sbarWidth
                        except: sbarWidth = 16 # default
                        ll = Tkinter.Label(self.grid,text="     "+description,wraplength=self.ourCanvas.winfo_screenwidth()-sbarWidth-50) # allow for borders on Windows (TODO: is 50px always right?)
                        ll.grid(row=curRow,column=0,columnspan=1+3*len(self.languagesToDraw),sticky="w")
                        curRow += 1
                    if not flwr=="prompts": hadDirectories = True
            elif "_" in fname and (languageOverride in allLangs or languageof(fname) in allLangs): # something_lang where lang is a recognised language (don't just take "any _" because some podcasts etc will have _ in them)
              # TODO what about letting them record _explain_ files etc from the GUI (can be done but have to manually enter the _zh_explain bit), + toggling !poetry etc?
              afterLang = ""
              if languageOverride:
                  realPrefix = prefix = fname[:fname.index("_")]
                  if not isMeaning:
                      afterLang = (fname+extsep)[fname.find("_",fname.find("_")+1):fname.rfind(extsep)]
                      prefix += (" ("+afterLang[1:]+")")
              else:
                  realPrefix = prefix = fname[:fname.rindex("_")]
                  languageOverride = languageof(fname)
              wprefix = prefix
              for ww in ["word_","word","_"]:
                if wprefix.startswith(ww):
                  wprefix=wprefix[len(ww):] ; break
              ii=0
              while ii<len(wprefix) and "0"<=wprefix[ii]<="9": ii += 1
              try: iprefix = int(wprefix[:ii])
              except: iprefix = -1
              if iprefix>maxPrefix: maxPrefix=iprefix # max existing numerical prefix
              
              if (flwr.endswith(dotwav) or flwr.endswith(dotmp3) or flwr.endswith(dottxt)): # even if not languageOverride in self.languagesToDraw e.g. for prompts - helps setting up gradint in a language it doesn't have prompts for (creates blank rows for the prefixes that other languages use). TODO do we want to add 'and languageOverride in self.languagesToDraw' if NOT in prompts?
                if not prefix in prefix2row:
                    self.addLabel(curRow,0,utext=filename2unicode(prefix))
                    foundTxt = {}
                    for lang in self.languagesToDraw:
                        if realPrefix+"_"+lang+afterLang+dottxt in l: foundTxt[lang]=(self.currentDir+os.sep+realPrefix+"_"+lang+afterLang+dottxt,2+3*self.languagesToDraw.index(lang))
                    prefix2row[prefix] = curRow
                    for lang in self.languagesToDraw: # preserve tab order
                        if lang==languageOverride and not flwr.endswith(dottxt):
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
        r1=Tkinter.Frame(self.frame) ; r1.grid(columnspan=2) ; r1=Tkinter.Frame(r1) ; r1.pack()
        r2=Tkinter.Frame(self.frame) ; r2.grid(columnspan=2) ; r2=Tkinter.Frame(r2) ; r2.pack()
        # note: addButton NOT self.addButton :
        addButton(r1,localise("Advanced"),self.do_openInExplorer,"left")
        if gotSox: self.AmplifyButton=addButton(r1,localise("Amplify"),self.amplify,"left")
        if not self.always_enable_synth: addButton(r1,localise("Mix with computer voice"),self.enable_synth,"left")
        addButton(r2,localise("Record from file"),self.do_recordFromFile,"left")
        if got_program("lame"): self.CompressButton = addButton(r2,localise("Compress all"),self.all2mp3_or_zip,"left") # was "Compress all recordings" but it takes too much width
        # TODO else can we see if it's possible to get the encoder on the fly, like in the main screen? (would need some restructuring)
        elif got_program("zip") and (explorerCommand or winCEsound): self.CompressButton = addButton(r2,localise("Zip for email"),lambda *args:self.all2mp3_or_zip(),"left")
        addButton(r2,localise(cond(recorderMode,"Quit","Back to main menu")),self.finished,"left")
        
        if winCEsound and not tkSnack: msg="Click on filenames at left to rename; click synthesized text to edit it"
        else: msg="Choose a word and start recording. Then press space to advance (see control at top). You can also browse and manage previous recordings. Click on filenames at left to rename (multi-line pastes are allowed); click synthesized text to edit it."
        if olpc or winCEsound: labelwidth = self.ourCanvas.winfo_screenwidth()
        elif hasattr(app,"isBigPrint"): labelwidth = self.ourCanvas.winfo_screenwidth()-50 # allow for borders on Windows (TODO: is 50px always right?)
        else: labelwidth=min(int(self.ourCanvas.winfo_screenwidth()*.7),512) # (512-pixel max. so the column isn't too wide to read on wide screens, TODO increase if the font is large)
        Tkinter.Label(self.frame,text=msg,wraplength=labelwidth).grid(columnspan=2)
        # (Don't worry about making the text files editable - editable filenames should be enough + easier to browse the result outside Gradint; can include both languages in the filename if you like - hope the users figure this out as we don't want to make the instructions too complex)

def reviseCount(num):
    # suggested reduction for revision
    thresholds=[1,2,knownThreshold,reallyKnownThreshold,meaningTestThreshold,randomDropThreshold,randomDropThreshold2] ; thresholds.sort() ; thresholds.reverse()
    for i in range(len(thresholds)-1):
        if num>thresholds[i]: return thresholds[i+1]
    return 0

def doRecWords(): # called from GUI thread
    if hasattr(app,"LessonRow"): app.thin_down_for_lesson() # else recorderMode
    app.Label.pack_forget() ; app.CancelRow.pack_forget()
    global theRecorderControls
    try: theRecorderControls
    except: theRecorderControls=RecorderControls()
    theRecorderControls.draw()
    app.wordsExist = 1 # well not necessarily, but see comments re "Create word list"

# Functions for recording on Android and S60 phones:

def android_recordFile(language):
 fname = os.getcwd()+os.sep+"newfile_"+language+dotwav
 while True:
  android.recorderStartMicrophone(fname) # TODO: python-for-android's MediaRecorderFacade.java startAudioRecording uses default output format and encoder, which likely means that so-called .wav file is really a .3gp file.  Have worked around in pcmlen for now, but don't know if the assumptions made there are universal, plus we don't want to name these files .wav if they're not really .wav
  android.dialogCreateAlert("Recording",language)
  android.dialogSetPositiveButtonText("Stop")
  android.dialogShow() ; android.dialogGetResponse()
  android.recorderStop()
  android.mediaPlay("file://"+fname)
  if not getYN("Are you happy with this?"):
    os.remove(fname) ; continue
  return fname

def android_recordWord():
    if not getYN("Ready to record "+secondLanguage+" word?"): return
    def ipFunc(prompt,value=u""): return android.dialogGetInput("Gradint",prompt,value).result
    droidOrS60RecWord(android_recordFile,ipFunc)
def s60_recordWord():
    def ipFunc(prompt,value=u""): return appuifw.query(prompt,"text",value)
    droidOrS60RecWord(s60_recordFile,ipFunc)
def droidOrS60RecWord(recFunc,inputFunc):
 if secondLanguage==firstLanguage: l1Suffix, l1Display = firstLanguage+"-meaning_"+firstLanguage, "meaning"
 else: l1Suffix, l1Display = firstLanguage, firstLanguage
 while True:
  l2 = recFunc(secondLanguage)
  if not l2: return
  l1 = None
  while not l1:
    if (not maybeCanSynth(firstLanguage)) or getYN("Record "+l1Display+" too? (else computer voice)"): l1 = recFunc(l1Suffix) # (TODO what if maybeCanSynth(secondLanguage) but not first, and we want to combine 2nd-lang synth with 1st-lang recorded? low priority as if recording will prob want to rec L2)
    else:
       l1txt = inputFunc(u""+firstLanguage+" text:")
       if l1txt:
          l1 = "newfile_"+firstLanguage+dottxt
          open(l1,"w").write(l1txt.encode("utf-8"))
    if not l1 and getYN("Discard the "+secondLanguage+" recording?"):
       os.remove(l2) ; break
  if not l1: continue
  ls = list2set(os.listdir(samplesDirectory))
  def inLs(prefix):
    for l in ls:
        if l.startswith(prefix) and len(l) > len(prefix) and l[len(prefix)] not in "0123456789": return True
  global recCount
  try: recCount += 1
  except: recCount = 1
  while inLs("%02d" % recCount): recCount += 1
  origPrefix = prefix = u""+("%02d" % recCount)
  while True:
    prefix = inputFunc(u"Filename:",prefix)
    if not prefix: # pressed cancel ??
      if getYN("Discard this recording?"):
        recCount-=1;os.remove(l1);os.remove(l2);return
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

# Start of users.py - multiple users in the Tk interface

settingsFile = "settings"+dottxt
user0 = (samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile)

def addUserToFname(fname,userNo):
  if not userNo or not fname: return fname
  elif os.sep in fname: return fname+"-user"+str(userNo)
  else: return "user"+str(userNo)+"-"+fname

def select_userNumber(N,updateGUI=1):
  global samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile
  prevUser = samplesDirectory
  samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile = user0
  samplesDirectory=addUserToFname(samplesDirectory,N)
  vocabFile=addUserToFname(vocabFile,N)
  progressFile=addUserToFname(progressFile,N)
  pickledProgressFile=addUserToFname(pickledProgressFile,N)
  settingsFile = addUserToFname("settings"+dottxt,N)
  if prevUser == samplesDirectory: return # called twice with same number
  ofl = firstLanguage
  if fileExists(settingsFile): readSettings(settingsFile)
  else: readSettings("settings"+dottxt) # the default one
  if not firstLanguage==ofl and updateGUI: # need to update the UI
      app.thin_down_for_lesson()
      app.todo.set_main_menu="keep-outrow"
  if updateGUI and hasattr(app,"vocabList"): del app.vocabList # re-read
def select_userNumber2(N):
    select_userNumber(N) ; app.userNo.set(str(N))

def setup_samplesDir_ifNec(d=0): # if the user doesn't have a samples directory, create one, and copy in the README.txt if it exists
  if not d: d=samplesDirectory
  if not isDirectory(d):
    os.mkdir(d)
    if fileExists(user0[0]+os.sep+"README"+dottxt): write(d+os.sep+"README"+dottxt,read(user0[0]+os.sep+"README"+dottxt))

def get_userNames(): # list of unicode user names or []
  ret=[]
  u=userNameFile ; c=0
  while fileExists(u):
    ret.append(unicode(u8strip(read(u)).strip(wsp),'utf-8'))
    c += 1 ; u=addUserToFname(userNameFile,c)
  global lastUserNames ; lastUserNames = ret
  return ret

def set_userName(N,unicodeName): open(addUserToFname(userNameFile,N),"w").write(unicodeName.encode("utf-8")+"\n") # implicitly adds if N=num+1

def wrapped_set_userName(N,unicodeName):
  if unicodeName.strip(wsp): set_userName(N,unicodeName)
  else: app.todo.alert="You need to type the person's name in the box before you press "+localise("Add new name") # don't waitOnMessage because we're in the GUI thread

GUI_usersRow = lastUserNames = None

def updateUserRow(fromMainMenu=0):
  row=GUI_usersRow
  if not row: return
  if hasattr(row,"widgetsToDel"):
    for w in row.widgetsToDel: w.pack_forget()
  row.widgetsToDel=[]
  names = get_userNames()
  if fromMainMenu and names==[""]:
    # someone pressed "add other students" but didn't add any - better reset it this run
    os.remove(userNameFile) ; names=[]
  if names:
    names.append("") # ensure at least one blank
    if not hasattr(app,"userNo"):
        app.userNo = Tkinter.StringVar(app)
        app.userNo.set("0")
    row["borderwidth"]=1
    if hasattr(Tkinter,"LabelFrame") and not winCEsound: # new in Tk 8.4 and clearer (but takes up a bit more space, so not winCEsound)
        r=Tkinter.LabelFrame(row,text=localise("Students"),padx=5,pady=5)
    else:
        r=addRow(row,1) ; Tkinter.Label(r,text=localise("Students")+":").grid(row=0,column=0,columnspan=2)
    row.widgetsToDel.append(r) ; row=r
    if winCEsound: row.pack()
    else: row.pack(padx=10,pady=10)
    global userBSM
    if len(names)>4:
        row, c = setupScrollbar(row,1) # better have a scrollbar (will configure it after the loop below)
        userBSM = ButtonScrollingMixin() ; userBSM.ourCanvas = c
    else: userBSM = None
    for i in range(len(names)):
      if names[i].strip(wsp):
        r=Tkinter.Radiobutton(row, text=names[i], variable=app.userNo, value=str(i), takefocus=0)
        r.grid(row=i+1,column=0,sticky="w")
        r["command"]=cmd=lambda e=None,i=i: select_userNumber(i)
        if not forceRadio:
           r2=Tkinter.Radiobutton(row, text="Select", variable=app.userNo, value=str(i), indicatoron=0) ; bindUpDown(r2,True)
           r2.grid(row=i+1,column=1,sticky="e")
           r2["command"]=cmd
           r2.bind('<Return>',lambda e=None,i=i: select_userNumber2(i))
           if userBSM: userBSM.bindFocusIn(r2)
        addButton(row,"Rename",lambda e=None,i=i,r=r,row=row:renameUser(i,r,row),"nopack").grid(row=i+1,column=2,sticky="e")
        r=addButton(row,"Delete",lambda e=None,i=i:deleteUser(i),"nopack") ; r.grid(row=i+1,column=3,sticky="e")
      else:
        r=Tkinter.Frame(row) ; r.grid(row=i+1,column=0,columnspan=4)
        text,entry = addTextBox(r)
        if not fromMainMenu: entry.focus() # because user has just pressed the "add other students" button, or has just added a name and may want to add another
        l=lambda *args:(wrapped_set_userName(i,asUnicode(text.get())),updateUserRow())
        addButton(r,localise("Add new name"),l)
        entry.bind('<Return>',l)
        if not i: Tkinter.Label(row,text="The first name should be that of the\nEXISTING user (i.e. YOUR name).").grid(row=i+2,column=0,columnspan=4)
      if userBSM: userBSM.bindFocusIn(r) # for shift-tab from the bottom
      if hasattr(row,"widgetsToDel"): row.widgetsToDel.append(r)
      if not names[i]: break
    if userBSM: c.after(cond(winCEsound,1500,300),lambda *args:c.config(scrollregion=c.bbox(Tkinter.ALL),width=c.bbox(Tkinter.ALL)[2],height=min(c["height"],c.winfo_screenheight()/2,c.bbox(Tkinter.ALL)[3]))) # hacky (would be better if it could auto shrink on resize)
  else: row.widgetsToDel.append(addButton(row,localise("Family mode (multiple user)"),lambda *args:(set_userName(0,""),updateUserRow())))

def renameUser(i,radioButton,parent,cancel=0):
    if hasattr(radioButton,"in_renaming"):
        del radioButton.in_renaming
        n=asUnicode(radioButton.renameText.get())
        if cancel: pass
        elif not n.strip(wsp) and len(lastUserNames)>1: tkMessageBox.showinfo(app.master.title(),"You can't have blank user names unless there is only one user.  Keeping the original name instead.")
        else:
            set_userName(i,n)
            radioButton["text"]=n
        radioButton.renameEntry.grid_forget()
        radioButton.grid(row=i+1,column=0,sticky="w")
    else:
        radioButton.in_renaming = 1
        radioButton.grid_forget()
        radioButton.renameText,radioButton.renameEntry = addTextBox(parent,"nopack")
        radioButton.renameEntry.grid(row=i+1,column=0)
        radioButton.renameText.set(lastUserNames[i])
        radioButton.renameEntry.focus()
        radioButton.after(10,lambda *args:radioButton.renameEntry.event_generate('<End>'))
        radioButton.renameEntry.bind('<Return>',lambda *args:renameUser(i,radioButton,parent))
        radioButton.renameEntry.bind('<Escape>',lambda *args:renameUser(i,radioButton,parent,cancel=1))

def deleteUser(i):
    for n in ["Are you sure","Are you REALLY sure","This is your last chance: Are you REALLY SURE"]:
        if not tkMessageBox.askyesno(app.master.title(),u""+n+" you want to delete "+lastUserNames[i]+" permanently, including any vocabulary list and recordings?"): return
    numUsers=len(lastUserNames)
    for fileOrDir in user0+(userNameFile,):
        d=addUserToFname(fileOrDir,i)
        if not d: continue # ??
        if isDirectory(d):
            while True:
                try: import shutil
                except: shutil = 0
                if shutil: shutil.rmtree(d,1)
                else: system(cond(winsound or mingw32,"del /F /S /Q \"","rm -rf \"")+d+"\"")
                if not isDirectory(d): break
                tkMessageBox.showinfo(app.master.title(),"Directory removal failed - make sure to close all windows etc that are open on it.")
        elif fileExists(d): os.remove(d)
        for j in range(i+1,numUsers):
            d2=addUserToFname(fileOrDir,j)
            if fileExists_stat(d2): os.rename(d2,d)
            d=d2
    select_userNumber2(0) # save confusion
    updateUserRow()

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
    else: msg2=msg
    if appuifw:
        t=appuifw.Text() ; t.add(u"".join(warnings_printed)+msg) ; appuifw.app.body = t # in case won't fit in the query()  (and don't use note() because it doesn't wait)
        appuifw.query(u""+msg,'query')
    elif android:
        # android.notify("Gradint","".join(warnings_printed)+msg) # doesn't work?
        android.dialogCreateAlert("Gradint","".join(warnings_printed)+msg)
        android.dialogSetPositiveButtonText("OK")
        android.dialogShow() ; android.dialogGetResponse()
    elif app:
        if not (winsound or winCEsound or mingw32 or cygwin): show_info(msg2+"\n\nWaiting for you to press OK on the message box... ",True) # in case terminal is in front
        app.todo.alert = "".join(warnings_printed)+msg
        while True:
            try:
              if not hasattr(app.todo,"alert"): break
            except: break # app destroyed
            time.sleep(0.5)
        if not (winsound or winCEsound or mingw32 or cygwin): show_info("OK\n",True)
    else:
        if clearScreen(): msg2 = "This is "+program_name.replace("(c)","\n(c)")+"\n\n"+msg2 # clear screen is less confusing for beginners, but NB it may not happen if warnings etc
        show_info(msg2+"\n\n"+cond(winCEsound,"Press OK to continue\n","Press Enter to continue\n"))
        sys.stderr.flush() # hack because some systems don't do it (e.g. some mingw32 builds), and we don't want the user to fail to see why the program is waiting (especially when there's an error)
        try:
            raw_input(cond(winCEsound,"See message under this window.","")) # (WinCE uses boxes for raw_input so may need to repeat the message - but can't because the prompt is size-limited, so need to say look under the window)
            clearScreen() # less confusing for beginners
        except EOFError: show_info("EOF on input - continuing\n")
    warnings_printed = []

def getYN(msg,defaultIfEof="n"):
    if appuifw:
        appuifw.app.body = None
        return appuifw.query(u""+msg,'query')
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
                ans=defaultIfEof ; print ans
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
            justSynthesize=appuifw.query(u"Say:","text",u""+justSynthesize)
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
              if justSynthesize=="a": justSynthesize=old_js
        oldLang = lang
        if justSynthesize: lang = just_synthesize(interactive,lang)
        # and see if it transliterates:
        if justSynthesize and lang and not '#' in justSynthesize:
            if justSynthesize.startswith(lang+" "):
                t = transliterates_differently(justSynthesize[len(lang+" "):],lang)
                if t: t=lang+" "+t
            else: t = transliterates_differently(justSynthesize,lang)
            if t:
                if appuifw: justSynthesize = t
                else: show_info("Spoken as "+t+"\n")
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
      return g.open_new(url)
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
    widget.bind('<Enter>',lambda *args:app.set_statusline(status))
    widget.bind('<Leave>',app.restore_statusline)
    if not mouseOnly:
        widget.bind('<FocusIn>',lambda *args:app.set_statusline(status))
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
    for l,cmd in funclist: m.add_command(label=l,command=(lambda e=e,c=cmd: e.widget.after(10,evgen,e,c)))
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
        entry.bind('<Return>',lambda e:doRawInput(text,entry))
        if wide: # put help in 1st wide textbox
          global had_doRawInput
          try: had_doRawInput
          except:
            had_doRawInput=1
            text.set("(Push OK to type A-Z)") # (if changing this message, change it below too)
            class E: pass
            e=E() ; e.widget = entry
            entry.after(10,lambda *args:selectAll(e))
      else: # PocketPC: try to detect long clicks. This is awkward. time.time is probably 1sec resolution so will get false +ves if go by that only.
        def timeStamp(entry): entry.buttonPressTime=time.time()
        entry.bind('<ButtonPress-1>',lambda e:timeStamp(entry))
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
        entry.bind('<ButtonRelease-1>',lambda e:pasteInstructions(time.time()-getattr(entry,"buttonPressTime",time.time())))
        entry.bind('<Double-Button-1>',lambda e:doPaste(text,entry))
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
    def getRow(row):
      if not row:
        row = Tkinter.Frame(parent)
        row.pack(fill=Tkinter.X,expand=1)
      return row
    GUIlang = GUI_languages.get(firstLanguage,firstLanguage)
    if "@variants-"+GUIlang in GUI_translations: # the firstLanguage has script variants
        row=getRow(row)
        if not hasattr(app,"scriptVariant"): app.scriptVariant = Tkinter.StringVar(app)
        count = 0
        for variant in GUI_translations["@variants-"+GUIlang]:
            Tkinter.Radiobutton(row, text=u" "+variant+u" ", variable=app.scriptVariant, value=str(count), indicatoron=forceRadio).pack({"side":"left"})
            count += 1
        app.scriptVariant.set(str(scriptVariants.get(GUIlang,0)))
    if synth_partials_voices and guiVoiceOptions:
        row=getRow(row)
        if not hasattr(app,"voiceOption"): app.voiceOption = Tkinter.StringVar(app)
        Tkinter.Radiobutton(row, text=u" Normal ", variable=app.voiceOption, value="", indicatoron=forceRadio).pack({"side":"left"})
        for o in guiVoiceOptions: Tkinter.Radiobutton(row, text=u" "+o[1].upper()+o[2:]+u" ", variable=app.voiceOption, value=o, indicatoron=forceRadio).pack({"side":"left"})
        app.voiceOption.set(voiceOption)
    if not gotSox: return row # can't do any file output without sox
    if not hasattr(app,"outputTo"):
        app.outputTo = Tkinter.StringVar(app) # NB app not parent (as parent is no longer app)
        app.outputTo.set("0") # not "" or get tri-state boxes on OS X 10.6
    row=getRow(row)
    rightrow = addRightRow(row) # to show beginners this row probably isn't the most important thing despite being in a convenient place, we'll right-align
    def addFiletypeButton(fileType):
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
    if got_program("lame"): addFiletypeButton("mp3")
    if got_windows_encoder: addFiletypeButton("wma")
    if got_program("neroAacEnc") or got_program("faac") or got_program("afconvert"): addFiletypeButton("aac")
    if got_program("oggenc"): addFiletypeButton("ogg")
    if got_program("toolame"): addFiletypeButton("mp2")
    if got_program("speexenc"): addFiletypeButton("spx")
    addFiletypeButton("wav")
    # "Get MP3 encoder" and "Get WMA encoder" changed to "MP3..." and "WMA..." to save width (+ no localisation necessary)
    if unix and not got_program("lame") and got_program("make") and got_program("gcc") and (got_program("curl") or got_program("wget")): addButton(rightrow,"MP3...",app.getEncoder,status="Press this to compile an MP3 encoder\nso Gradint can output to MP3 files") # (checking gcc as well as make because some distros strangely have make but no compiler; TODO what if has a non-gcc compiler)
    # (no longer available) elif (winsound or mingw32) and not got_windows_encoder and not got_program("lame"): addButton(rightrow,"WMA...",app.getEncoder,status="Press this to download a WMA encoder\nso Gradint can output to WMA files")
    return row

def updateSettingsFile(fname,newVals):
    # leaves comments etc intact, but TODO does not cope with changing variables that have been split over multiple lines
    replacement_lines = []
    try: oldLines=u8strip(read(fname)).replace("\r\n","\n").split("\n")
    except IOError: oldLines=[]
    for l in oldLines:
        found=0
        for k in newVals.keys():
            if l.startswith(k):
                replacement_lines.append(k+"="+repr(newVals[k]))
                del newVals[k]
                found=1
        if not found: replacement_lines.append(l)
    for k,v in newVals.items(): replacement_lines.append(k+"="+repr(v))
    if replacement_lines and replacement_lines[-1]: replacement_lines.append("") # ensure blank line at end so there's a \n but we don't add 1 more with each save
    open(fname,"w").write("\n".join(replacement_lines))

def asUnicode(x): # for handling the return value of Tkinter entry.get()
    try: return u""+x # original behaviour
    except: # some localised versions of Windows e.g. German will return Latin1 instead of Unicode, so try interpreting it as utf-8 and Latin-1
        try: return x.decode("utf-8")
        except: return x.decode("iso-8859-1") # TODO can we get what it actually IS? (on German WinXP, sys.getdefaultencoding==ascii and locale==C but Tkinter still returns Latin1)

def setupScrollbar(parent,rowNo):
    onLeft = winCEsound or olpc
    s = Tkinter.Scrollbar(parent,takefocus=0)
    s.grid(row=rowNo,column=cond(onLeft,0,1),sticky="ns"+cond(onLeft,"w","e"))
    c=Tkinter.Canvas(parent,bd=0,width=200,height=100,yscrollcommand=s.set)
    c.grid(row=rowNo,column=cond(onLeft,1,0),sticky="nsw")
    s.config(command=c.yview)
    scrolledFrame=Tkinter.Frame(c) ; c.create_window(0,0,window=scrolledFrame,anchor="nw")
    # Mousewheel binding.  TODO the following bind_all assumes only one scrolledFrame on screen at once (redirect all mousewheel events to the frame; necessary as otherwise they'll go to buttons etc)
    app.ScrollUpHandler = lambda *args:c.yview("scroll","-1","units")
    app.ScrollDownHandler = lambda *args:c.yview("scroll","1","units")
    scrolledFrame.bind_all('<Button-4>',app.ScrollUpHandler)
    scrolledFrame.bind_all('<Button-5>',app.ScrollDownHandler)
    # DON'T bind <MouseWheel> on Windows - our version of Tk will segfault when it occurs. See http://mail.python.org/pipermail/python-bugs-list/2005-May/028768.html but we can't patch our library.zip's Tkinter anymore (TODO can we use newer Tk DLLs and ensure setup.bat updates them?)
    return scrolledFrame, c

# GUI presets buttons:
shortDescriptionName = "short-description"+dottxt
longDescriptionName = "long-description"+dottxt
class ExtraButton(object):
    def __init__(self,directory):
        self.shortDescription = u8strip(read(directory+os.sep+shortDescriptionName)).strip(wsp)
        if fileExists(directory+os.sep+longDescriptionName): self.longDescription = u8strip(read(directory+os.sep+longDescriptionName)).strip(wsp)
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
        while newName in ls: newName+="1"
        name2=newName
        newName = samplesDirectory+os.sep+newName
        os.rename(self.directory,newName)
        which_collection = localise(" has been added to your recorded words collection.")
        if fileExists(newName+os.sep+"add-to-vocab"+dottxt):
            which_collection = localise(" has been added to your collection.")
            o=open(vocabFile,"a")
            o.write("# --- BEGIN "+self.shortDescription+" ---\n")
            o.write(u8strip(read(newName+os.sep+"add-to-vocab"+dottxt)).strip(wsp)+"\n")
            o.write("# ----- END "+self.shortDescription+" ---\n")
            if hasattr(app,"vocabList"): del app.vocabList # so re-reads
            os.remove(newName+os.sep+"add-to-vocab"+dottxt)
        if fileExists(newName+os.sep+"add-to-languages"+dottxt):
            changed = 0
            for lang in u8strip(read(newName+os.sep+"add-to-languages"+dottxt)).strip(wsp).split():
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
          app.after(t,lambda *args:flashButton(button,"active"))
          app.after(t+150,lambda *args:flashButton(button,"normal"))
        # (Don't like flashing, but can't make it permanently active as it won't change when the focus does)

if WMstandard: GUI_omit_statusline = 1 # unlikely to be room (and can disrupt nav)

def startTk():
    class Application(Tkinter.Frame):
        def __init__(self, master=None):
            Tkinter.Frame.__init__(self, master)
            class EmptyClass: pass
            self.todo = EmptyClass() ; self.toRestore = []
            self.ScrollUpHandler = self.ScrollDownHandler = lambda *args:True
            global app ; app = self
            make_extra_buttons_waiting_list()
            if olpc: self.master.option_add('*font',cond(extra_buttons_waiting_list,'Helvetica 9','Helvetica 14'))
            elif macsound and Tkinter.TkVersion>=8.6: self.master.option_add('*font','System 13') # ok with magnification.  Note >13 causes square buttons.  (Including this line causes "Big print" to work)
            elif WMstandard: self.master.option_add('*font','Helvetica 7') # TODO on ALL WMstandard devices?
            if winsound or cygwin or macsound: self.master.resizable(1,0) # resizable in X direction but not Y (latter doesn't make sense, see below).  (Don't do this on X11 because on some distros it results in loss of automatic expansion as we pack more widgets.)
            elif unix:
                import commands
                if commands.getoutput("xlsatoms|grep COMPIZ_WINDOW").find("COMPIZ")>=0: # (not _COMPIZ_WM_WINDOW_BLUR, that's sometimes present outside Compiz)
                  # Compiz sometimes has trouble auto-resizing our window (e.g. on Ubuntu 11.10)
                  self.master.geometry("%dx%d" % (self.winfo_screenwidth(),self.winfo_screenheight()))
                  if not GUI_always_big_print: self.todo.alert = "Gradint had to maximize itself because your window manager is Compiz which sometimes has trouble handling Tkinter window sizes"
            self.extra_button_callables = []
            self.pack(fill=Tkinter.BOTH,expand=1)
            self.leftPanel = Tkinter.Frame(self)
            self.leftPanel.pack(side="left",fill=Tkinter.X,expand=1) # "fill" needed so listbox can fill later
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
                    f=str(self.tk.eval('set font [font actual '+' '.join(f)+']')).split()
                    upNext = 0
                    for i in range(len(f)):
                        if f[i]=="-size": upNext=1
                        elif upNext:
                            nominalSize=intor0(f[i])
                            if nominalSize<0: nominalSize,f[i] = -nominalSize,"-%d"
                            else: f[i]="%d"
                            break
                    f=" ".join(f)
                    if not "%d" in f: raise Exception("wrong format") # caught below
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
            self.copyright_string = u"This is "+(u""+program_name).replace("(c)",u"\n\u00a9").replace("-",u"\u2013")
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
                    self.BigPrintButton["font"]=self.bigPrintFont
                self.remake_cancel_button(localise("Quit"))
                if not GUI_omit_statusline: self.Version.pack(fill=Tkinter.X,expand=1)
                if olpc or self.todo.set_main_menu=="test" or GUI_for_editing_only: self.showtest() # olpc: otherwise will just get a couple of options at the top and a lot of blank space (no way to centre it)
                else: focusButton(self.TestButton)
                del self.todo.set_main_menu
                self.restore_copyright()
            if hasattr(self.todo,"alert"):
                # we have to do it on THIS thread (especially on Windows / Cygwin; Mac OS and Linux might get away with doing it from another thread)
                tkMessageBox.showinfo(self.master.title(),self.todo.alert)
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
            self.MakeLessonButton.bind('<FocusIn>',(lambda *args:app.after(10,lambda *args:app.MinsEntry.selection_clear())))
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
                    k,f = synthcache_lookup("!synth:"+t+"_"+l,justQueryCache=1)
                    if f:
                      if (partials_langname(l) in synth_partials_voices or get_synth_if_possible(l,0)): # (no point having these buttons if there's no chance we can synth it by any method OTHER than the cache)
                        if k in synthCache_transtbl and k[0]=="_": cacheManagementOptions.append(("Keep in "+l+" cache",k,k[1:],0,0))
                        elif k[0]=="_": cacheManagementOptions.append(("Keep in "+l+" cache",0,0,f,f[1:]))
                        if k in synthCache_transtbl: cacheManagementOptions.append(("Reject from "+l+" cache",k,"__rejected_"+k,0,0))
                        else: cacheManagementOptions.append(("Reject from "+l+" cache",0,0,f,"__rejected_"+f))
                    else:
                      k,f = synthcache_lookup("!synth:__rejected_"+t+"_"+l,justQueryCache=1)
                      if not f: k,f = synthcache_lookup("!synth:__rejected__"+t+"_"+l,justQueryCache=1)
                      if f:
                        if k in synthCache_transtbl: cacheManagementOptions.append(("Undo "+l+" cache reject",k,k[11:],0,0))
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
            l=map(lambda (x,y):x+"="+y, filter(lambda (x,y):text1 in x.lower().replace(" ","") and text2 in y.lower().replace(" ",""),self.vocabList)[-tkNumWordsToShow:])
            l.reverse() ; synchronizeListbox(self.ListBox,l) # show in reverse order, in case the bottom of the list box is off-screen
        def doSynthcacheManagement(self,oldKey,newKey,oldFname,newFname):
            # should be a quick operation - might as well do it in the GUI thread
            if (oldKey,oldFname) == (0,0): # special for mp3web
                self.menu_response="mp3web" ; return
            if oldKey in synthCache_transtbl:
                if newKey: synthCache_transtbl[newKey]=synthCache_transtbl[oldKey]
                else: del synthCache_transtbl[oldKey]
                open(synthCache+os.sep+transTbl,'w').write("".join([v+" "+k+"\n" for k,v in synthCache_transtbl.items()]))
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
        def stripText(self,*args): self.Text1.set(fix_commas(hanzi_and_punc(asUnicode(self.Text1.get()))))
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
            self.ChangeLanguageButton.bind('<FocusIn>',(lambda *args:app.after(10,lambda *args:app.L2Entry.selection_clear())))
            self.AddButton.bind('<FocusIn>',(lambda *args:app.after(10,lambda *args:app.L1Entry.selection_clear()))) # for backwards tabbing
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
                    if fileExists(addUserToFname(user0[1],i)): m.add_command(label=u"Copy vocab list from "+lastUserNames[i],command=(lambda e=None,i=i:self.copyVocabFrom(i)))
                    m.add_command(label=u"Copy recordings to/from "+lastUserNames[i],command=(lambda e=None,i=i:self.setToOpen((addUserToFname(user0[0],i),addUserToFname(user0[0],intor0(self.userNo.get()))))))
            m.tk_popup(self.CopyFromButton.winfo_rootx(),self.CopyFromButton.winfo_rooty(),entry="0")
        def setToOpen(self,toOpen): self.menu_response,self.toOpen = "samplesCopy",toOpen
        def copyVocabFrom(self,userNo):
            # Copy any NEW vocab lines (including comments).  TODO could also insert them in the right place (like 'diff' without the deletions)
            select_userNumber(userNo,updateGUI=0)
            vCopyFrom = vocabLinesWithLangs()
            select_userNumber(intor0(self.userNo.get()),updateGUI=0)
            vCurrent = list2set(vocabLinesWithLangs())
            o=appendVocabFileInRightLanguages()
            langs = (secondLanguage,firstLanguage)
            for newLangs,line in vCopyFrom:
                if (newLangs,line) in vCurrent: continue # already got it
                if not newLangs==langs: o.write("SET LANGUAGES "+" ".join(list(newLangs))+"\n")
                o.write(line+"\n")
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
            if (firstLanguage,secondLanguage) == (firstLanguage1,secondLanguage1): # they didn't change anything
                langs = ESpeakSynth().describe_supported_languages()
                msg = (localise("To change languages, edit the boxes that say '%s' and '%s', then press the '%s' button.") % (firstLanguage,secondLanguage,localise("Change languages")))+"\n\n"+localise("Recorded words may be in ANY languages, and you may choose your own abbreviations for them.  However if you want to use the computer voice for anything then please use standard abbreviations.")
                if langs:
                    if tkMessageBox.askyesno(self.master.title(),msg+"  "+localise("Would you like to see a list of the standard abbreviations for languages that can be computer voiced?")): self.todo.alert = localise("Languages with computer voices (some better than others):")+"\n"+langs
                else: self.todo.alert = msg+"  "+localise("(Sorry, a list of these is not available on this system - check eSpeak installation.)")
                return
            need_redisplay = "@variants-"+GUI_languages.get(firstLanguage,firstLanguage) in GUI_translations or "@variants-"+GUI_languages.get(firstLanguage1,firstLanguage1) in GUI_translations # if EITHER old or new lang has variants, MUST reconstruct that row.  (TODO also do it anyway to get the "Speaker" etc updated?  but may cause unnecessary flicker if that's no big problem)
            firstLanguage,secondLanguage = firstLanguage1,secondLanguage1
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
            t1,t2 = t1.strip(wsp), t2.strip(wsp)
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
        ret.append((unicode(c,"utf-8"),unicode(b,"utf-8")))
    return ret
def readText(l): # see utils/transliterate.py (running guiVocabList on txt files from scanSamples)
    l = samplesDirectory+os.sep+l
    if l in variantFiles: # oops. just read the 1st .txt variant
        if os.sep in l: lp=(l+os.sep)[:l.rfind(os.sep)]+os.sep
        else: lp = ""
        varList = filter(lambda x:x.endswith(dottxt),variantFiles[l])
        varList.sort() # so at least it consistently returns the same one.  TODO utils/ cache-synth.py list-synth.py synth-batchconvert-helper.py all use readText() now, can we get them to cache the other variants too?
        l = lp + varList[0]
    return u8strip(read(l)).strip(wsp)

def singular(number,s):
  s=localise(s)
  if firstLanguage=="en" and number==1 and s[-1]=="s": return s[:-1]
  return s
def localise(s):
  d = GUI_translations.get(s,{}) ; s2 = 0
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
        # Try Notepad++ first, otherwise plain notepad
        textEditorCommand = programFiles+os.sep+"Notepad++"+os.sep+"notepad++.exe"
        if fileExists(textEditorCommand): textEditorCommand='"'+textEditorCommand+'" -multiInst -notabbar -nosession'
        else: textEditorCommand="notepad"
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
        if "KDE_FULL_SESSION" is os.environ and got_program("kfmclient"):
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
        for editor in ["leafpad","gedit","nedit","kedit","xedit"]:
            if got_program(editor):
                textEditorName=textEditorCommand=editor
                textEditorWaits = 1
                if textEditorName.endswith("edit"):
                    textEditorName=textEditorName[:-4]+"-"+textEditorName[-4:]
                    textEditorName=textEditorName[0].upper()+textEditorName[1:]
                break
    # End of finding editor - now start GUI
    try:
        import thread,Tkinter,tkMessageBox
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
        ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(ShellExecuteInfo(60,File=u"\\Windows\\fexplore",Parameters=u""+dir)))
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

def sanityCheck(text,language,pauseOnError=0): # text is utf-8; returns error message if any
    if not text: return # always OK empty strings
    if pauseOnError:
        ret = sanityCheck(text,language)
        if ret: waitOnMessage(ret)
        return ret
    if language=="zh":
        allDigits = True
        for t in text:
            if ord(t)>127: return # got hanzi or tone marks
            if t in "12345": return # got tone numbers
            if t not in "0123456789. ": allDigits = False
        if allDigits: return
        return "Pinyin needs tones.  Please go back and add tone numbers to "+text+"."+cond(startBrowser("http://www.pristine.com.tw/lexicon.php?query="+fix_pinyin(text,[]).replace("1","1 ").replace("2","2 ").replace("3","3 ").replace("4","4 ").replace("5"," ").replace("  "," ").strip(wsp).replace(" ","+"))," Gradint has pointed your web browser at an online dictionary that might help.","")

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
  label1,label2 = u""+localise("Word in %s") % localise(secondLanguage),u""+localise("Meaning in %s") % localise(firstLanguage)
  while True:
    result = appuifw.multi_query(label1,label2) # unfortunately multi_query can't take default items (and sometimes no T9!), but Form is too awkward (can't see T9 mode + requires 2-button save via Options) and non-multi query would be even more modal
    if not result: return # cancelled
    l2,l1 = result # guaranteed to both be populated
    while sanityCheck(l2.encode('utf-8'),secondLanguage,1):
        l2=appuifw.query(label1,"text",u"")
        if not l2: return # cancelled
    # TODO detect duplicates like Tk GUI does?
    appuifw.note(u"Added "+l2+"="+l1,"conf")
    appendVocabFileInRightLanguages().write((l2+"="+l1+"\n").encode("utf-8"))
def s60_changeLang():
    global firstLanguage,secondLanguage
    result = appuifw.multi_query(u""+localise("Your first language")+" (e.g. "+firstLanguage+")",u""+localise("second")+" (e.g. "+secondLanguage+")")
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
    vList = map(lambda (l2,l1):l2+u"="+l1, guiVocabList(parseSynthVocab(vocabFile,1)))
    if not vList: return waitOnMessage("Your computer-voiced vocab list is empty.")
    while True:
      appuifw.app.body = None
      sel = appuifw.selection_list(vList,search_field=1)
      if sel==None: return
      l2,l1 = vList[sel].split("=",1)
      action = appuifw.popup_menu([u"Speak (just "+secondLanguage+")",u"Speak ("+secondLanguage+" and "+firstLanguage+")",u"Change "+secondLanguage,u"Change "+firstLanguage,u"Delete item",u"Cancel"], vList[sel])
      if action==0 or action==1:
        doLabel("Speaking...")
        justSynthesize = secondLanguage+" "+l2.encode('utf-8')
        if action==1: justSynthesize += ('#'+firstLanguage+" "+l1.encode('utf-8'))
        just_synthesize()
        justSynthesize = ""
      elif action==5: pass
      else:
          if action==4 and not getYN(u"Are you sure you want to delete "+vList[sel]+"?"): continue
          oldL1,oldL2 = l1,l2
          if action==2:
              first=1
              while first or (l2 and sanityCheck(l2.encode('utf-8'),secondLanguage,1)):
                  first=0 ; l2=appuifw.query(u""+secondLanguage,"text",l2)
              if not l2: continue
          elif action==3:
              l1 = appuifw.query(u""+firstLanguage,"text",l1)
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
    while not l2 or sanityCheck(l2.encode('utf-8'),secondLanguage,1):
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
    v=u8strip(read(vocabFile)).replace("\r\n","\n").replace("\r","\n")
    if paranoid_file_management:
        fname = os.tempnam()
        o = open(fname,"w")
    else: o=open(vocabFile,"w")
    found = 0
    if last_u8strip_found_BOM: o.write('\xef\xbb\xbf') # re-write it
    v=v.split("\n")
    if v and not v[-1]: v=v[:-1] # don't add an extra blank line at end
    for l in v:
        l2=l.lower()
        if l2.startswith("set language ") or l2.startswith("set languages "):
            langs=l.split()[2:] ; o.write(l+"\n") ; continue
        thisLine=map(lambda x:x.strip(wsp),l.split("=",len(langs)-1))
        if (langs==[secondLanguage,firstLanguage] and thisLine==[L2toDel.encode('utf-8'),L1toDel.encode('utf-8')]) or (langs==[firstLanguage,secondLanguage] and thisLine==[L1toDel.encode('utf-8'),L2toDel.encode('utf-8')]):
            # delete this line.  and maybe replace it
            found = 1
            if action=="replace":
                if langs==[secondLanguage,firstLanguage]: o.write(newL2.encode("utf-8")+"="+newL1.encode("utf-8")+"\n")
                else: o.write(newL1.encode("utf-8")+"="+newL2.encode("utf-8")+"\n")
        else: o.write(l+"\n")
    o.close()
    if paranoid_file_management:
        write(vocabFile,read(fname))
        os.remove(fname)
    return found

def maybeCanSynth(lang): return lang in synth_partials_voices or get_synth_if_possible(lang,0) or synthCache
def android_main_menu():
  while True:
    menu=[]
    if maybeCanSynth(secondLanguage):
        menu.append((u"Just speak a word",primitive_synthloop))
        doVocab = maybeCanSynth(firstLanguage)
        if doVocab: menu.append((u"Add word to my vocab",android_addVocab))
        menu.append((u"Make lesson from vocab",lesson_loop))
        # if doVocab: menu.append((u"View/change vocab",android_viewVocab)) # (TODO but lower priority because SL4A has an editor)
    else: menu.append((u"Make lesson",lesson_loop))
    menu += [(u"Record word(s) with mic",android_recordWord),(u"Change languages",android_changeLang)]
    menu.append((u"Quit",None))
    android.dialogCreateAlert("Gradint","Choose an action")
    android.dialogSetItems(map (lambda x:x[0], menu))
    android.dialogShow()
    try: function = menu[android.dialogGetResponse().result['item']][1]
    except KeyError: break # no 'item'
    if function: function()
    else: break
def s60_main_menu():
  while True:
    appuifw.app.body = None # NOT text saying version no etc - has distracting blinking cursor
    menu=[]
    if maybeCanSynth(secondLanguage):
        menu.append((u"Just speak a word",primitive_synthloop))
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
    return not system("""if which curl >/dev/null 2>/dev/null; then export Curl="curl -L"; else export Curl="wget -O -"; fi
if ! test -e lame*.tar.gz; then
  export Link="$($Curl "http://sourceforge.net/project/showfiles.php?group_id=290&package_id=309"|grep tar.gz|head -1)"
  echo "Got HTML: $Link" 1>&2
  export Link="$(echo "$Link"|sed -e 's,href="/,href="http://sourceforge.net/,' -e 's/.*http:/http:/' -e 's/.tar.gz.*/.tar.gz/')"
  echo "Following link to $Link" 1>&2
  if ! $Curl "$Link" > lame.tar.gz; then
    rm -f lame.tar.gz; exit 1
  fi
  if grep downloads.sourceforge lame.tar.gz 2>/dev/null; then
    export Link="$(cat lame.tar.gz|grep downloads.sourceforge|head -1)"
    echo "Got HTML 2: $Link" 1>&2
    export Link="$(echo "$Link"|sed -e 's/.*http/http/' -e 's,.*/projects,http://sourceforge.net/projects,' -e 's/".*//')"
    echo "Following link 2 to $Link" 1>&2
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
        if menu_response=="input": # WMstandard
            app.todo.input_response=raw_input()
        elif menu_response=="go":
            gui_outputTo_start()
            if not soundCollector: app.todo.add_briefinterrupt_button = 1
            try: lesson_loop()
            except PromptException,prEx: waitOnMessage("Problem finding prompts:\n"+prEx.message) # and don't quit, user may be able to fix
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
                    ctypes.cdll.coredll.ShellExecuteEx(ctypes.byref(ShellExecuteInfo(60,File=u""+app.fileToEdit)))
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
              if text1.startswith('#'): msg="" # see below
              else: msg=sanityCheck(text1,secondLanguage)
              if msg: app.todo.alert=u""+msg
              else:
                app.set_watch_cursor = 1 ; app.toRestore = []
                global justSynthesize ; justSynthesize = ""
                def doControl(text,lang,control):
                    global justSynthesize
                    restoreTo = asUnicode(control.get())
                    if text.startswith('#'): justSynthesize += text # hack for direct control of just_synthesize from the GUI (TODO document it in advanced.txt? NB we also bypass the GUI transliteration in the block below)
                    elif text:
                        if can_be_synthesized("!synth:"+text+"_"+lang): justSynthesize += ("#"+lang+" "+text)
                        else: app.todo.alert="Cannot find a synthesizer that can say '"+text+"' in language '"+lang+"' on this system"
                        t=transliterates_differently(text,lang)
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
                      if app: del app.menu_response
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
              if not f in oldLs and (f.lower().endswith(dotmp3) or f.lower().endswith(dotwav)) and getYN("Use "+f[f.rfind(os.sep)+1:]+"?"): # TODO don't ask this question too many times if there are many and they're all 'no'
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
                if system("""tar -zxvf lame*.tar.gz && cd lame-* && if ./configure && make; then ln -s $(pwd)/frontend/lame ../lame || true; else cd .. ; rm -rf lame*; exit 1; fi"""): app.todo.alert = "Compile failed"
          app.todo.set_main_menu = 1
        elif (menu_response=="add" or menu_response=="replace") and not (app.Text1.get() and app.Text2.get()): app.todo.alert="You need to type text in both boxes before adding the word/meaning pair to "+vocabFile
        elif menu_response=="add" and hasattr(app,"vocabList") and (asUnicode(app.Text1.get()),asUnicode(app.Text2.get())) in app.vocabList:
            # Trying to add a word that's already there - do we interpret this as a progress adjustment?
            app.set_watch_cursor = 1
            t1,t2 = asUnicode(app.Text1.get()),asUnicode(app.Text2.get())
            lang2,lang1=t1.lower(),t2.lower() # because it's .lower()'d in progress.txt
            d = ProgressDatabase(0)
            l1find = "!synth:"+lang1.encode('utf-8')+"_"+firstLanguage
            found = 0
            msg=(u""+localise("%s=%s is already in %s.")) % (t1,t2,vocabFile)
            for listToCheck in [d.data,d.unavail]:
              if found: break
              for item in listToCheck:
                if (item[1]==l1find or (type(item[1])==type([]) and l1find in item[1])) and item[2]=="!synth:"+lang2.encode('utf-8')+"_"+secondLanguage:
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
            msg=sanityCheck(text1,secondLanguage)
            if msg: app.todo.alert=u""+msg
            else:
                o=appendVocabFileInRightLanguages()
                o.write(text1+"="+text2+"\n") # was " = " but it slows down parseSynthVocab
                o.close()
                if paranoid_file_management:
                    if filelen(vocabFile)<filelen(vocabFile+"~") or chr(0) in open(vocabFile).read(1024): app.todo.alert="Vocab file corruption! You'd better restore the ~ backup."
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
                l1find = "!synth:"+lang1.encode('utf-8')+"_"+firstLanguage
                for item in d.data:
                    if (item[1]==l1find or (type(item[1])==type([]) and l1find in item[1])) and item[2]=="!synth:"+lang2.encode('utf-8')+"_"+secondLanguage and item[0]:
                        app.unset_watch_cursor = 1
                        if not getYN(localise("You have repeated %s=%s %d times.  Do you want to pretend you already repeated %s=%s %d times?") % (lang2,lang1,item[0],t2,t1,item[0])):
                            app.set_watch_cursor = 1 ; break
                        d.data.remove(item)
                        l1replace = "!synth:"+t2.encode('utf-8')+"_"+firstLanguage
                        if type(item[1])==type([]):
                            l = item[1]
                            l[l.index(l1find)] = l1replace
                        else: l=l1replace
                        item = (item[0],l,"!synth:"+t1.encode('utf-8')+"_"+secondLanguage)
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
        if app: del app.menu_response

def vocabLinesWithLangs(): # used for merging different users' vocab files
    langs = [secondLanguage,firstLanguage] ; ret = []
    try: v=u8strip(read(vocabFile)).replace("\r","\n")
    except IOError: v=""
    for l in v.split("\n"):
        l2=l.lower()
        if l2.startswith("set language ") or l2.startswith("set languages "): langs=l.split()[2:]
        elif l: ret.append((tuple(langs),l)) # TODO what about blank lines? (currently they'd be considered duplicates)
    return ret

def appendVocabFileInRightLanguages():
    # check if we need a SET LANGUAGE
    langs = [secondLanguage,firstLanguage]
    try: v=u8strip(read(vocabFile)).replace("\r","\n")
    except IOError: v=""
    for l in v.split("\n"):
        l2=l.lower()
        if l2.startswith("set language ") or l2.startswith("set languages "): langs=l.split()[2:]
    o=open(vocabFile,"a")
    if not v.endswith("\n"): o.write("\n")
    if not langs==[secondLanguage,firstLanguage]: o.write("SET LANGUAGES "+secondLanguage+" "+firstLanguage+"\n")
    return o

def transliterates_differently(text,lang):
    global last_partials_transliteration ; last_partials_transliteration=None
    global partials_are_sporadic ; o=partials_are_sporadic ; partials_are_sporadic = None # don't want to touch the counters here
    if synthcache_lookup("!synth:"+text+"_"+lang):
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
            if '#' in justSynthesize[1:]: prefix="" # multiple languages
            else: # prefix the language that's being synth'd
                prefix=justSynthesize.split()[0]
                if prefix.startswith('#'): prefix=prefix[1:]
        else: prefix = "lesson"
        while not outputFile or fileExists(outputFile):
            outputFile=gui_output_directory+os.sep+prefix+str(gui_output_counter)+extsep+app.outputTo.get()
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
        if justSynthesize and not justSynthesize[-1]=='*': appTitle=cond('#' in justSynthesize,"Gradint","Reader") # not "language lesson"
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
        
        if justSynthesize=="-": primitive_synthloop()
        elif justSynthesize and justSynthesize[-1]=='*':
            justSynthesize=justSynthesize[:-1]
            waitBeforeStart = 0
            just_synthesize() ; lesson_loop()
        elif justSynthesize: just_synthesize()
        elif app and waitBeforeStart: gui_event_loop()
        elif appuifw: s60_main_menu()
        elif android: android_main_menu()
        else: lesson_loop()
    except SystemExit,e: exitStatus = e.code
    except KeyboardInterrupt: pass
    except PromptException,prEx:
        waitOnMessage("\nProblem finding prompts:\n"+prEx.message+"\n")
        exitStatus = 1
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
            if tracebackFile: sys.stderr.write(read("last-gradint-error"+extsep+"txt"))
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

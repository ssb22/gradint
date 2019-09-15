# This file is part of the source code of
# gradint v0.999 (c) 2002-2019 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# program to "thin down" the gradint .py for low memory environments
# by taking out some of the code that's unused on that platform

import sys, re

tk_only = [ # we want these on WinCE but not S60:
# note: comments are stripped BEFORE checking against this list
"def words_exist():",
"def reviseCount(num):", # used only in Tk for now
"if mp3web:",
"class InputSourceManager(object):",
"class InputSource(object):",
"class MicInput(InputSource):",
"class PlayerInput(InputSource):",
"class ButtonScrollingMixin(object):",
"class RecorderControls(ButtonScrollingMixin):",
"def doRecWords():",
"if app:","elif app:",
"def addStatus(widget,status,mouseOnly=0):",
"def addButton(parent,text,command,packing=None,status=None):",
"def addLabel(row,label):",
"def CXVMenu(e):",
"def selectAll(e):",
"def selectAllButNumber(e):",
"def addTextBox(row,wide=0):",
"def addLabelledBox(row,wide=0,status=None):",
"def addRow(parent,wide=0):",
"def addRightRow(widerow):",
"def make_output_row(parent):",
"def select_userNumber(N,updateGUI=1):",
"def select_userNumber2(N):",
"def updateUserRow(fromMainMenu=0):","def get_userNames():",
"def set_userName(N,unicodeName):",
"def wrapped_set_userName(N,unicodeName):",
"def renameUser(i,radioButton,parent,cancel=0):",
"def deleteUser(i):",
"def addUserToFname(fname,userNo):",
"def setupScrollbar(parent,rowNo):",
"def focusButton(button):",
"def bindUpDown(o,alsoLeftRight=False):",
"class ExtraButton(object):",
"def make_extra_buttons_waiting_list():",
"def startTk():",
# "def guiVocabList(parsedVocab):", # now actually used on S60
"def synchronizeListbox(listbox,masterList):",
"if useTK:",
"if useTK and not tkSnack:",
"def openDirectory(dir,inGuiThread=0):",
"def gui_event_loop():",
"def makeButton(parent,text,command):",
"def vocabLinesWithLangs():",
"if Tk_might_display_wrong_hanzi:",
"def setup_samplesDir_ifNec(d=0):",
"def filename2unicode(f):",
"def unicode2filename(u):",
]

not_S60_or_android = [ # but may still need on winCE
"if winsound:",
"if winsound or mingw32:",
"class ESpeakSynth(Synth):","def espeak_volume_ok():",
'if winCEsound or ((winsound or mingw32) and not os.sep in tmpPrefix and not tmpPrefix.startswith("C:")):',
'def got_program(prog):', # as no non-winsound/unix
'if useTK and runInBackground and not (winsound or mingw32) and hasattr(os,"fork") and not "gradint_no_fork" in os.environ:',
'def maybe_warn_mp3():',
'elif (cygwin or ((winsound or mingw32) and winsound_also)) and os.sep in file:',
'elif (winsound and not (self.length>10 and wavPlayer)) or winCEsound:',
"elif wavPlayer.find('sndrec32')>=0:",
'elif wavPlayer:', # it'll take appuifw/android 1st
'if winsound or mingw32 or cygwin:',
'elif winsound or mingw32 or cygwin:',
'for s in synth_priorities.split():', # Ekho/eSpeak/MacOS/SAPI not available on S60/Android (well, not that we can yet call into)
'def import_recordings(destDir=None):', # TODO: document in advanced.txt that this option is non-functional on S60/Android?  (code WOULD work if suitably configured, but unlikely to be used and we need to save size)
"elif msvcrt:",
]

not_android = [
"if not app and not app==False and not appuifw and not android:",
"elif not android:",
"def fileExists(f):", # assume we got os.path
"def fileExists_stat(f):",
"def isDirectory(directory):",
"for p in [progressFile,progressFileBackup,pickledProgressFile]:", # this 'sanity check' is not likely to be a problem on Android, and we could do with saving the space
"if need_say_where_put_progress:", # ditto
'def check_for_interrupts():','if emulated_interruptMain:','if emulated_interruptMain or winCEsound:','def handleInterrupt():', # no current way to do this on Android (unlike S60/WinCE)
r"if not '\xc4'.lower()=='\xc4':", # this workaround is not needed on Android
r"if not fileExists(configFiles[0]) and sys.argv and (os.sep in sys.argv[0] or (os.sep=='\\' and '/' in sys.argv[0])):", # that logic not likely to work on Android (but we do need the rest of that block)
"def guiVocabList(parsedVocab):", # not yet available on Android (unlike S60, TODO?)
]

riscos_only = [
"if riscos_sound:",
"elif riscos_sound:",
'if riscos_sound and hex(int(time.time())).find("0xFFFFFFFF")>=0 and not outputFile:',
"class OldRiscosSynth(Synth):",
'if not extsep==".":', # RISC OS
]

mac_only = [
'if macsound and __name__=="__main__":',
'if macsound and "_" in os.environ:',
"if macsound:","elif macsound:",
'if hasattr(app,"isBigPrint") and macsound:',
'elif macsound and got_program("afconvert"):',
]

desktop_only = [ # Don't want these on either WinCE or S60:
'if hasattr(app,"isBigPrint") and winsound:',
"if unix:","elif unix:",
"def disable_lid(restore):",
'elif unix and useTK and isDirectory("/dev/snd") and got_program("arecord"):',
"if unix and (';' in cmd or '<' in cmd):",
'elif wavPlayer=="sox":',
'elif wavPlayer=="aplay" and ((not fileType=="mp3") or madplay_path or gotSox):',
"def simplified_header(fname):",
"def win2cygwin(path):","elif cygwin:",
"if paranoid_file_management:",
"elif unix and not macsound:",
"elif unix and hasattr(os,\"popen\"):",
"def wavToMp3(directory):",
"def makeMp3Zips(baseDir,outDir,zipNo=0,direc=None):",
"def check_for_slacking():",
"def checkAge(fname,message):",
"def downloadLAME():",
"def decode_mp3(file):",
"class Mp3FileCache(object):",
"class OSXSynth_Say(Synth):",
"def aiff2wav(fname):", # (used only on Mac)
"class OSXSynth_OSAScript(Synth):",
"class PttsSynth(Synth):",
"def sapi_sox_bug_workaround(wavdata):",
"class FliteSynth(Synth):",
"def espeak_stdout_works():", # called only if unix
# (keep ESpeakSynth for WinCE)
"class EkhoSynth(Synth):",
"class FestivalSynth(Synth):",
"class GeneralSynth(Synth):", # (needs os.system, so not S60/WinCE)
"class GeneralFileSynth(Synth):", # (ditto)
"class ShellEvent(Event):",
# And the following are desktop only because they need sox:
"if gotSox and unix:",
"class SoundCollector(object):","if soundCollector:",
"def oggenc():",
"def outfile_writeBytes(o,bytes):",
"def outfile_close(o):",
"def outfile_writeFile(o,handle,filename):",
"class ShSoundCollector(object):",
"def outfile_write_error():",
"def lame_quiet():",
"def beepCmd(soxParams,fname):",
"def collector_time():",
"def collector_sleep(s):",
"def dd_command(offset,length):",
"def lame_endian_parameters():",
"if outputFile:",
"def setSoundCollector(sc):",
"def getAmplify(directory):",
"def doAmplify(directory,fileList,factor):",
"def gui_outputTo_end(openDir=True):",
"def gui_outputTo_start():",
"def warn_sox_decode():",
'if disable_once_per_day==1:',
'if once_per_day&2 and not hasattr(sys,"_gradint_innerImport"):',
'if once_per_day&1 and fileExists(progressFile) and time.localtime(os.stat(progressFile).st_mtime)[:3]==time.localtime()[:3]:',
'def optimise_partial_playing(ce):',
'def optimise_partial_playing_list(ceList):',
]

winCE_only = [
"if use_unicode_filenames:",
"if winCEsound:",'elif winCEsound:',
'if winCEsound and __name__=="__main__":',
'elif winCEsound and fileType=="mp3":',
"if WMstandard:",
]

not_winCE = [
"if not winCEsound:",
]

S60_only = [
'if sys.platform.find("ymbian")>-1:',
"class S60Synth(Synth):",
"if appuifw:","elif appuifw:",
"def s60_recordWord():",
"def s60_recordFile(language):",
"def s60_addVocab():",
"def s60_changeLang():",
"def s60_runLesson():",
"def s60_viewVocab():",
"def s60_main_menu():",
]

android_only = [
"if android:",
"elif android:",
"class AndroidSynth(Synth):",
"def android_recordWord():",
"def android_recordFile(language):",
"def android_main_menu():",
"def android_addVocab():",
"def android_changeLang():",
]

android_or_S60 = [
"def droidOrS60RecWord(recFunc,inputFunc):",
]

if "s60" in sys.argv: # S60 version
  version = "S60"
  to_omit = tk_only + desktop_only + winCE_only + not_S60_or_android + android_only + riscos_only + mac_only
elif "android" in sys.argv: # Android version
  version = "Android"
  to_omit = tk_only + desktop_only + winCE_only + S60_only + not_S60_or_android + not_android + riscos_only + mac_only
elif "wince" in sys.argv: # Windows Mobile version
  version = "WinCE"
  to_omit = desktop_only + S60_only + android_only + android_or_S60 + not_winCE + riscos_only + mac_only
elif "core" in sys.argv: # experimental "core code only" for 'minimal embedded porting' starting point (no UI, no synth, limited file I/O; you'll probably have to load up the event data yourself)
  version = "core"
  to_omit = tk_only + not_S60_or_android + not_android + riscos_only + mac_only + desktop_only + winCE_only + S60_only + android_only + android_or_S60 + ["def main():","def rest_of_main():",'if __name__=="__main__":',"def transliterates_differently(text,lang):","def primitive_synthloop():","def appendVocabFileInRightLanguages():",'def delOrReplace(L2toDel,L1toDel,newL2,newL1,action="delete"):',"def sanityCheck(text,language,pauseOnError=0):","def localise(s):","def singular(number,s):","def readText(l):","def asUnicode(x):","def updateSettingsFile(fname,newVals):","def clearScreen():","def startBrowser(url):",'def getYN(msg,defaultIfEof="n"):',"def waitOnMessage(msg):","def interrupt_instructions():","def parseSynthVocab(fname,forGUI=0):","def scanSamples_inner(directory,retVal,doLimit):","def getLsDic(directory):","def check_has_variants(directory,ls):","def exec_in_a_func(x):","def scanSamples(directory=None):","def synth_from_partials(text,lang,voice=None,isStart=1):","def partials_langname(lang):","if partialsDirectory and isDirectory(partialsDirectory):",'for zipToCheck in ["yali-voice","yali-lower","cameron-voice"]:','def stripPuncEtc(text):','def can_be_synthesized(fname,dirBase=None,lang=None):','def synthcache_lookup(fname,dirBase=None,printErrors=0,justQueryCache=0,lang=None):','def textof(fname):','if synthCache and transTbl in synthCache_contents:','if synthCache:','class Partials_Synth(Synth):','def abspath_from_start(p):','class SynthEvent(Event):','def pinyin_uColon_to_V(pinyin):','def synth_event(language,text,is_prompt=0):','def get_synth_if_possible(language,warn=1,to_transliterate=False):','if wavPlayer_override or (unix and not macsound and not (oss_sound_device=="/dev/sound/dsp" or oss_sound_device=="/dev/dsp")):','def fix_compatibility(utext):','def read_chinese_number(num):','def preprocess_chinese_numbers(utext,isCant=0):','def intor0(v):','def fix_pinyin(pinyin,en_words):','def fix_commas(text):','def shell_escape(text):','class SimpleZhTransliterator(object):','def sort_out_pinyin_3rd_tones(pinyin):','def ensure_unicode(text):','def unzip_and_delete(f,specificFiles="",ignore_fail=0):','class Synth(object):','def quickGuess(letters,lettersPerSec):',"def changeToDirOf(file,winsound_also=0):",'if app or appuifw or android:','def subst_some_synth_for_synthcache(events):','def decide_subst_synth(cache_fname):','if winsound or winCEsound or mingw32 or riscos_sound or not hasattr(os,"tempnam") or android:','if len(sys.argv)>1:','def readSettings(f):','def exc_info(inGradint=True):','if not fileExists(configFiles[0]):','def u8strip(d):',]
else: assert 0, "Unrecognised version on command line"

revertToIndent = lastIndentLevel = indentLevel = -1
lCount = -1 ; inTripleQuotes=0 ; orig = []
for l in sys.stdin.xreadlines():
  orig.append(l)
  lCount += 1
  if lCount==2: print "\n# NOTE: this version has been automatically TRIMMED for "+version+" (some non-"+version+" code taken out)\n"
  l=l.rstrip()
  assert not "\t" in l, "can't cope with tabs"
  lastIndentLevel,indentLevel = indentLevel,-1
  for i in range(len(l)):
    if not l[i]==" ":
      indentLevel = i ; break
  was_inTripleQuotes = inTripleQuotes
  if (len(l.split('"""'))%2) == 0: inTripleQuotes = not inTripleQuotes
  if indentLevel<0 or indentLevel==len(l) or (revertToIndent>=0 and (indentLevel>revertToIndent or was_inTripleQuotes)): continue
  justRevertedI,revertToIndent = revertToIndent,-1
  code0 = (l+"#")[:l.find("#")].rstrip()
  code = code0.lstrip()
  if (code in to_omit or (':' in code and code[:code.index(':')+1] in to_omit)) and not was_inTripleQuotes:
    if ':' in code and code[:code.index(':')+1] in to_omit: code = code[:code.index(':')+1]
    if code.startswith("def "): code=re.sub(r"\([^)][^)][^)]+\)",r"(*_)",code)
    if code.startswith("elif "): pass # can always remove those lines completely, even if will be followed by an 'else' (and will never be the only thing in its block)
    else:
      if code.startswith("if "): code="if 0:"
      print " "*indentLevel+code+" pass # trimmed"
    revertToIndent = indentLevel
  elif not code:
    if "#    " in l or lCount < 2: print l # keep start and GPL comments
  elif ('"' in code and '"' in l[len(code):]) or ("'" in code and "'" in l[len(code):]): print l # perhaps # was in a string, keep it
  else: print code0
orig = "".join(orig)
for o in to_omit:
  if not o in orig: sys.stderr.write("Warning: line not matched: "+o)

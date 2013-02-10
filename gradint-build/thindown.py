# This file is part of the source code of
# gradint v0.99851 (c) 2002-2013 Silas S. Brown. GPL v3+.
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

import sys

tk_only = [ # we want these on WinCE but not S60:
# note: comments are stripped BEFORE checking against this list
"def words_exist():",
"def reviseCount(num):", # used only in Tk for now
"if mp3web:",
"class InputSourceManager(object):",
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
"def updateUserRow(fromMainMenu=0):",
"def renameUser(i,radioButton,parent,cancel=0):",
"def deleteUser(i):",
"def setupScrollbar(parent,rowNo):",
"def focusButton(button):",
"def bindUpDown(o,alsoLeftRight=False):",
"class ExtraButton(object):",
"def make_extra_buttons_waiting_list():",
"def startTk():",
# "def guiVocabList(parsedVocab):", # now actually used on S60
"def synchronizeListbox(listbox,masterList):",
"if useTK:",
"def openDirectory(dir,inGuiThread=0):",
"def gui_event_loop():",
]

not_S60 = [ # but may still need on winCE
"if winsound:",
"if winsound or mingw32:",
]

desktop_only = [ # Don't want these on either WinCE or S60:
'if not extsep==".":', # RISC OS
"if macsound:","elif macsound:",
'if hasattr(app,"isBigPrint") and macsound:',
"if unix:","elif unix:",
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
"def aiff2wav(fname):",
"class OSXSynth_OSAScript(Synth):",
"class OldRiscosSynth(Synth):",
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
"class SoundCollector(object):",
"class ShSoundCollector(object):",
"def dd_command(offset,length):",
"def lame_endian_parameters():",
"if outputFile:",
"def setSoundCollector(sc):",
"def getAmplify(directory):",
"def doAmplify(directory,fileList,factor):",
"def gui_outputTo_end(openDir=True):",
"def gui_outputTo_start():",
"def warn_sox_decode():",
]

winCE_only = [
"if use_unicode_filenames:",
"if winCEsound:",
]

not_winCE = [
"if not winCEsound:",
]

S60_only = [
"class S60Synth(Synth):",
"if appuifw:",
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
"def droidOrS60RecWord(s60_recordFile,inputFunc):",
]

if "s60" in sys.argv: # S60 version
  version = "S60"
  to_omit = tk_only + desktop_only + winCE_only + not_S60 + android_only
elif "android" in sys.argv: # Android version
  version = "Android"
  to_omit = tk_only + desktop_only + winCE_only + S60_only
elif "wince" in sys.argv: # Windows Mobile version
  version = "WinCE"
  to_omit = desktop_only + S60_only + android_only + android_or_S60 + not_winCE
else: assert 0, "Unrecognised version on command line"

revertToIndent = -1
lCount = -1
omitted = {} ; inTripleQuotes=0
for l in sys.stdin.xreadlines():
  lCount += 1
  if lCount==2: print "\n# NOTE: this version has been automatically TRIMMED for "+version+" (some non-"+version+" code taken out)\n"
  l=l.rstrip()
  assert not "\t" in l, "can't cope with tabs"
  indentLevel=-1
  for i in range(len(l)):
    if not l[i]==" ":
      indentLevel = i ; break
  was_inTripleQuotes = inTripleQuotes
  if (len(l.split('"""'))%2) == 0: inTripleQuotes = not inTripleQuotes
  if indentLevel<0 or indentLevel==len(l) or (revertToIndent>=0 and (indentLevel>revertToIndent or was_inTripleQuotes)): continue
  revertToIndent = -1
  code = (l+"#")[:l.find("#")].strip()
  if code in to_omit and not was_inTripleQuotes:
    print " "*indentLevel+code+" pass # trimmed"
    revertToIndent = indentLevel
    omitted[code]=1
  else: print l
for o in to_omit:
  if not o in omitted: sys.stderr.write("Warning: line not matched: "+o+"\n")

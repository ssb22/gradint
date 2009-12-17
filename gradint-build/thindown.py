# This file is part of the source code of
# gradint v0.9945 (c) 2002-2009 Silas S. Brown. GPL v3+.
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

if "s60" in sys.argv: # S60 version
  version = "S60"
  to_omit = [
"if use_unicode_filenames:", # WinCE
"if paranoid_file_management:",
'if not extsep==".":',
"if macsound:","elif macsound:",
"if winsound:",
"if unix:",
"if winsound or mingw32:",
"elif unix and not macsound:",
"if gotSox and unix:",
"class SoundCollector(object):",
"def lame_endian_parameters():",
"def soundfile_to_data(file,soxParams):",
# TODO SH sound collector will have problem with indentation due to """..""" strings
"def decode_mp3(file):",
"class Mp3FileCache(object):",
"if outputFile:",
"class InputSourceManager(object):",
"def wavToMp3(directory):",
"def makeMp3Zips(baseDir,outDir,zipNo,direc=None):",
"class RecorderControls:",
"def doRecWords():",
"if app:","elif app:",
"def addStatus(widget,status,mouseOnly=0):",
"def removeStatus(widget):",
"def addButton(parent,text,command,packing=None,status=None):",
"def addLabel(row,label):",
"def CXVMenu(e):",
"def selectAll(e):",
"def selectAllButNumber(e):",
"def addTextBox(row,wide=0):",
"def addLabelledBox(row,wide=0):",
"def addRow(parent,wide=0):",
"def addRightRow(widerow):",
"def make_output_row(parent):",
"def select_userNumber(N,updateGUI=1):",
"def updateUserRow(fromMainMenu=0):",
"def renameUser(i,radioButton,parent,cancel=0):",
"def deleteUser(i):",
"def setupScrollbar(parent,rowNo):",
"def focusButton(button):",
"class ExtraButton(object):",
"def make_extra_buttons_waiting_list():",
"def startTk():",
"def guiVocabList(parsedVocab):",
"def synchronizeListbox(listbox,masterList):",
"if useTK:",
"def openDirectory(dir):",
"if winCEsound:",
"def check_for_slacking():",
"def gui_outputTo_end():",
"def gui_outputTo_start():",
]
else: assert 0, "Unrecognised version on command line"

revertToIndent = -1
lCount = -1
for l in sys.stdin.xreadlines():
  lCount += 1
  if lCount==2: print "\n# NOTE: this version has been automatically TRIMMED for "+version+" (some non-"+version+" code taken out)\n"
  l=l.rstrip()
  assert not "\t" in l, "can't cope with tabs"
  indentLevel=-1
  for i in range(len(l)):
    if not l[i]==" ":
      indentLevel = i ; break
  if indentLevel<0 or indentLevel==len(l) or (revertToIndent>=0 and indentLevel>revertToIndent): continue
  revertToIndent = -1
  if (l+"#")[:l.find("#")].strip() in to_omit:
    print (l+"#")[:l.find("#")]+" pass # trimmed"
    revertToIndent = indentLevel
  else: print l

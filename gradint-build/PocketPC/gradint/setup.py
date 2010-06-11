# Gradint wrapper script for PocketPC

# shortcut
try:
  if "Storage Card" in os.getcwd():
    os.rename(os.getcwd()+"\\gradint-card.lnk","\\Windows\\Start Menu\\Programs\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-internal.lnk")
  else:
    os.rename(os.getcwd()+"\\gradint-internal.lnk","\\Windows\\Start Menu\\Programs\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-card.lnk")
except: pass
if not os.path.exists("\\Windows\\Start Menu\\Programs\\Gradint.lnk"):
  raw_input("Failed to write to \\Windows")
  raw_input("is Application Lock on? Remove and try again.")
  raise SystemExit
  # http://www.mobilejaw.com/articles/2009/09/removing-application-lock-on-windows-mobile-standard-devices/
  # -> http://www.mobilejaw.com/content/2009/09/MobileJaw-ClearSecurity-MobiControl.cab

# Pre-compile - helps when the device is short of RAM,
# since compiling and running at the same time
# can take more RAM than doing it separately.

import os, py_compile, sys
f=os.getcwd()+os.sep+"gradint.py"
a=0
try: a=open(f)
except: pass
if a:
  print "Compiling gradint..."
  del a
  try: py_compile.compile(f)
  except IOError: raw_input("Compile error")
  try: os.remove(f) # leave the .pyc only
  except: pass

def moveFiles(srcDir,destDir):
    try: os.mkdir(destDir)
    except: pass
    for f in os.listdir(srcDir):
        if not "." in f:
            c = os.getcwd() ; isDir=0
            try:
                os.chdir(srcDir+"\\"+f)
                isDir = 1
            except: pass
            os.chdir(c)
            if isDir:
                moveFiles(srcDir+"\\"+f, destDir+"\\"+f)
                continue
        if os.path.exists(destDir+"\\"+f): os.remove(srcDir+"\\"+f)
        else: os.rename(srcDir+"\\"+f,destDir+"\\"+f)
    os.rmdir(srcDir)

try: l=os.listdir(os.getcwd()+"\\espeak-data")
except: l=0
if l:
  print "Installing eSpeak..."
  moveFiles(os.getcwd()+"\\espeak-data","\\espeak-data")
  if "Storage Card" in os.getcwd(): moveFiles(os.getcwd()+"\\bin","\\Storage Card\\bin")
  else: moveFiles(os.getcwd()+"\\bin","\\bin")
try: l=os.listdir(os.getcwd()+"\\Program Files")
except: l=0
if l:
    print "Installing TkInter..."
    try: moveFiles("\\Storage Card\\Windows","\\Windows")
    except: pass
    try:
      if "Storage Card" in os.getcwd(): moveFiles(os.getcwd()+"\\Program Files","\\Storage Card\\Program Files")
      else: moveFiles(os.getcwd()+"\\Program Files","\\Program Files")
      # need to restart Python
      raw_input("Setup successful - now run Gradint")
    except:
      raw_input("Failed to move Program Files")
      raw_input("Please do it manually in Explorer")
    raise SystemExit

# can now run
del moveFiles,l
import gradint ; gradint.main()

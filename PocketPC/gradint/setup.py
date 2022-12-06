# Gradint wrapper script for Windows Mobile

import os, py_compile, sys

# Pre-compile - helps when the device is short of RAM,
# since compiling and running at the same time
# can take more RAM than doing it separately.

f=os.getcwd()+os.sep+"gradint.py"
try: a=open(f)
except: a=0
if a:
  print "Compiling gradint..."
  del a
  try: py_compile.compile(f)
  except IOError: raw_input("Compile error")
  try: os.remove(f) # leave the .pyc only
  except: pass

# shortcut
progs="\\Windows\\Start Menu\\Programs"
if not os.path.isdir(progs): progs="\\Windows\\Start Menu" # WM-Standard has no Programs subdir
try:
  if "Storage Card" in os.getcwd():
    os.rename(os.getcwd()+"\\gradint-card.lnk",progs+"\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-internal.lnk")
  else:
    os.rename(os.getcwd()+"\\gradint-internal.lnk",progs+"\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-card.lnk")
except: pass

fail={}
def moveFiles(srcDir,destDir):
    try: os.mkdir(destDir)
    except: pass
    for f in os.listdir(srcDir):
        if not "." in f and os.path.isdir(srcDir+"\\"+f):
            moveFiles(srcDir+"\\"+f, destDir+"\\"+f)
            continue
        try:
          if os.path.exists(destDir+"\\"+f): os.remove(srcDir+"\\"+f)
          os.rename(srcDir+"\\"+f,destDir+"\\"+f)
        except:
          if not destDir in fail:
            fail[destDir]=1
            raw_input("Problem writing to "+destDir)
            raw_input("from "+srcDir)
            raw_input("Please do it manually in Explorer")
            raw_input("or remove Application Lock if on")
    try: os.rmdir(srcDir)
    except: pass # follow-through
# http://www.mobilejaw.com/articles/2009/09/removing-application-lock-on-windows-mobile-standard-devices/
# -> http://www.mobilejaw.com/content/2009/09/MobileJaw-ClearSecurity-MobiControl.cab

if os.path.isdir(os.getcwd()+"\\espeak-data"):
  print "Installing eSpeak..."
  moveFiles(os.getcwd()+"\\espeak-data","\\espeak-data")
  if "Storage Card" in os.getcwd(): moveFiles(os.getcwd()+"\\bin","\\Storage Card\\bin")
  else: moveFiles(os.getcwd()+"\\bin","\\bin")
if os.path.isdir(os.getcwd()+"\\Program Files"):
    print "Installing TkInter..."
    if "Storage Card" in os.getcwd():
      if os.path.isdir("\\Storage Card\\Windows"):
        moveFiles("\\Storage Card\\Windows","\\Windows")
      moveFiles(os.getcwd()+"\\Program Files","\\Storage Card\\Program Files")
    else: moveFiles(os.getcwd()+"\\Program Files","\\Program Files")
    raw_input("Setup successful - now run Gradint")
    raise SystemExit

# can now run
del moveFiles,l
import gradint ; gradint.main()

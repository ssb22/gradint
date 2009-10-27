# Gradint wrapper script for PocketPC

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

# shortcut
try:
  if "Storage Card" in os.getcwd():
    os.rename(os.getcwd()+"\\gradint-card.lnk","\\Windows\\Start Menu\\Programs\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-internal.lnk")
  else:
    os.rename(os.getcwd()+"\\gradint-internal.lnk","\\Windows\\Start Menu\\Programs\\Gradint.lnk")
    os.remove(os.getcwd()+"\\gradint-card.lnk")
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
        os.rename(srcDir+"\\"+f,destDir+"\\"+f)
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
    if "Storage Card" in os.getcwd(): moveFiles(os.getcwd()+"\\Program Files","\\Storage Card\\Program Files")
    else: moveFiles(os.getcwd()+"\\Program Files","\\Program Files")
    # need to restart Python
    raw_input("Setup successful - now run Gradint")
    raise SystemExit

# can now run
del moveFiles,l
import gradint ; gradint.main()

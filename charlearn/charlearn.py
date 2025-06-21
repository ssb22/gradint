#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# Character-learning support program
# (C) 2006-2013, 2020 Silas S. Brown.  Version 0.3.

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Where to find history:
# on GitHub at https://github.com/ssb22/gradint
# and on GitLab at https://gitlab.com/ssb22/gradint
# and on BitBucket https://bitbucket.org/ssb22/gradint
# and at https://gitlab.developers.cam.ac.uk/ssb22/gradint
# and in China: https://gitee.com/ssb22/gradint

listenAddr='127.0.0.1'
firstPortNo=9876

tableFile = "characters.txt"  # for first-time setup
knownFile = "known-chars.txt" # ditto
dumpFile = "charlearn-data"   # for saving progress
reviseFile = "revise.txt"     # for requesting more revision next time (will be deleted after integration into progress)

import sys,os.path
if sys.argv[-1].startswith("--"): gradint = None # (don't need to speak if we're processing options, see at end)
elif os.path.isfile("gradint.py"): import gradint
else: gradint = None # won't speak characters

import random,os,time,socket
try: from subprocess import getoutput
except: from commands import getoutput
try: from cPickle import Pickler,Unpickler
except: from pickle import Pickler,Unpickler
try: from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except: from http.server import BaseHTTPRequestHandler, HTTPServer
try: import thread
except: import _thread as thread

def byPriority(a): return a.priority

priorityIfGotWrong = -10
priorityOfOtherCharWrong = -4
priorityOfGroupWrong = 0
maxShowInGroup = 5 ; priorityBreakGroup = 10
initSessionLen = sessionLen = 2 ; maxSessionLen = 10 ; sampleConst = 1.5

def updateSessionLen():
  global sessionLen
  sessionLen = min(max(sessionLen,int(thechars.countKnown()[1]+0.95)),maxSessionLen)
  # did have /sampleConst after countKnown()[1] but doesn't seem necessary

already_spoken = {}

gradint_busy = 0
def speak_bkg():
  gradint.just_synthesize()
  global gradint_busy
  gradint_busy = 0

class SingleChar:
  def __init__(self,hanzi,pinyin):
    self.hanzi = hanzi ; self.pinyin = pinyin
    self.priority = 0 ; self.similarityGroup = None
    self.supposedToKnow = 0
  def formatPinyin(self): return self.pinyin.replace("\n","<BR>") # (could make it into actual tone marks also)
  def htmlString(self,parent,step=1,left=0):
    self.supposedToKnow = 1
    r=u'<html><head><title>hanzi</title><meta http-equiv="Content-Type" content="text/html; charset=%s"></head><body><h1>%s</h1>' % (parent.charset,self.hanzi)
    if step==1: r+=self.yesno('Do you know what this is? (%d remaining)' % left,2,0)
    else:
      r += self.formatPinyin() + "<HR>"
      if step<=0:
        if self.similarityGroup:
          l = []
          for c in parent.chars:
            if c.similarityGroup == self.similarityGroup and not id(c)==id(self): l.append(c)
          l.sort(key=byPriority)
          r+="Not to be confused with:"
          for c in l[:maxShowInGroup-1]: r+='<h1>%s</h1>%s' % (c.hanzi,c.formatPinyin())
          r += '<hr>'
        if parent.thisSession:
          r+='<A HREF="/%s">Next character</A>' % str(random.random())
          if step==-1:
            # got it right - might as well take that link automatically
            r=parent.processRequest("/").decode(parent.charset).replace('</body></html>','')
        else:
          updateSessionLen()
          r+='<A HREF="/quit">Quit</A> | <A HREF="/%s">Another %d</A>' % (str(random.random()),sessionLen)
        if step==0:
          self.priority=priorityIfGotWrong
          self.speak(parent.charset)
        else:
          # knew it
          self.priority += 1
          if self.priority > 0:
            if self.priority < 25000: self.priority *= 2 # give new characters a chance
            else: self.priority = 50000 # level off
          else: self.priority /= 2 # TRY this for a while - will make chars got-wrong recover more quickly (again to give new chars a chance)
        parent.save()
      elif step==2:
        r+=self.yesno('Did you get it right?',-1,3)
        self.speak(parent.charset)
      elif step==3:
        r+='What did you think it was?<P>'
        toOut = [] # (pinyin,hanzi,id,is-in-same-group)
        for c in parent.chars:
          if c.similarityGroup and c.similarityGroup==self.similarityGroup: sameGrp=True
          else: sameGrp=False # need to do it this way because Python sometimes returns 'None' from that expression
          if c.supposedToKnow and not id(c)==id(self): toOut.append((c.pinyin,c.hanzi,id(c),sameGrp)) # NOT formatPinyin, because may want to i-search it
        toOut.sort()
        if len(toOut) > 20: r+="(Hint: On some browsers you can use find-as-you-type)<P>"
        for outSameGroup in [True,False]:
          oldL=len(r)
          for p,hanzi,val,sameGrp in toOut:
            if sameGrp==outSameGroup: r+='%s <A HREF="/%d_%d">%s</A><BR>' % (hanzi,id(self),val,p)
          if len(r)>oldL and outSameGroup: r += '<HR>' # between chars in same group and others
        r+='<A HREF="/%d=0">None of the above</A>' % id(self)
        if not parent.thisSession:
          global already_spoken ; already_spoken = {} # reset it so "Another N" does speak them
    return r + '</body></html>'
  def speak(self,charset):
    if self.hanzi in already_spoken: return
    already_spoken[self.hanzi] = 1 # don't set a self. attribute - it'll get pickled for next session
    if gradint:
      gradint.justSynthesize = self.hanzi.decode(charset).encode('utf-8')
      global gradint_busy
      while gradint_busy: time.sleep(0.5)
      gradint_busy = 1
      thread.start_new_thread(speak_bkg,())
  def yesno(self,question,ifyes,ifno): return question+'<P><A ID="y" HREF="/%d=%d">Yes</A><SCRIPT>document.getElementById("y").focus()</SCRIPT> | <A HREF="/%d=%d">No</A>' % (id(self),ifyes,id(self),ifno) # (don't use the js anywhere except yes/no, because 'next character' etc may have too much on the screen and we don't want the focus() to scroll)
the_speaker_process = None
def terminate_server():
  # portable signal.alarm(1)
  time.sleep(1); os.abort()
def B(s):
    if type(u"")==type(""): return s.encode('utf-8')
    else: return s
def S(s):
    if type(u"")==type("") and not type(s)==type(""): return s.decode('utf-8')
    else: return s
class CharDbase:
  def __init__(self):
    self.counter = 0 ; self.nextPriority = 0
    self.similarityGroups = 0
    self.chars = [] ; self.thisSession = []
    self.readTable() ; self.readKnown() ; self.readRevise()
  def debug_printKnown(self):
    print ("-*- coding: %s -*-" % (self.charset,))
    for c in self.chars:
      if c.supposedToKnow: print ("%s %s" % (c.priority,c.hanzi))
  def readTable(self):
    addingTo = 0
    if self.chars: addingTo = 1
    lines=open(tableFile,'rb').readlines()
    if lines[0].startswith(B("charset:")):
      self.charset = S(lines[0].split()[-1])
      lines = lines[1:]
    else: self.charset = "iso-8859-1"
    for line in lines: self.addCharFromFreqTable(line.decode(self.charset),addingTo)
  def readKnown(self):
    try:
      o=open(knownFile)
    except IOError: return
    for line in o.readlines(): self.makeCharKnown(line.split()[0])
  def readRevise(self):
    try:
      o=open(reviseFile)
    except IOError: return
    for line in o.readlines(): self.makeCharRevise(line.split()[0])
  def makeCharKnown(self,hanzi):
    if not hanzi: return # blank lines etc
    for c in self.chars:
      if c.hanzi==hanzi:
        if not c.supposedToKnow:
          c.supposedToKnow = 1
          c.priority = priorityOfGroupWrong # just to check
        return
    print ("WARNING: character '%s' in %s was not in %s - ignoring" % (repr(hanzi),knownFile,tableFile))
  def makeCharRevise(self,hanzi):
    if not hanzi: return # blank lines etc
    for c in self.chars:
      if c.hanzi==hanzi:
        c.supposedToKnow = 1
        c.priority = priorityIfGotWrong
        return
    print ("WARNING: character '%s' in %s was not in %s - ignoring" % (repr(hanzi),reviseFile,tableFile))
  def addCharFromFreqTable(self,line,checkAlreadyThere):
    hanzi,pinyin = line.split(None,1)
    c=SingleChar(hanzi,pinyin.replace("\\n","\n"))
    c.priority = self.nextPriority ; self.nextPriority += 1
    if checkAlreadyThere:
      for c2 in self.chars:
        if c2.hanzi == hanzi: return
    self.chars.append(c)
  def charIdToChar(self,charId):
    char = None
    for c in self.chars:
      if id(c)==charId:
        char = c ; break
    assert char ; return char
  def processRequest(self,path):
    if '=' in path:
      charId,step = map(lambda x:int(x),path[1:].split('='))
      char = self.charIdToChar(charId)
    elif '_' in path: # grouping
      char,char2 = map(lambda x:self.charIdToChar(int(x)),path[1:].split('_'))
      if not char.similarityGroup and not char2.similarityGroup: # new group:
        self.similarityGroups += 1
        char.similarityGroup = char2.similarityGroup = self.similarityGroups
      elif not char.similarityGroup: char.similarityGroup = char2.similarityGroup
      elif not char2.similarityGroup: char2.similarityGroup = char.similarityGroup
      elif not char.similarityGroup == char2.similarityGroup: # merge 2 different groups:
        for c in self.chars:
          if c.similarityGroup == char2.similarityGroup: c.similarityGroup = char.similarityGroup
      step = 0 # normal got-wrong for this character
      char.priority = priorityIfGotWrong # here also, for the loop below
      char2.priority = min(char2.priority,priorityOfOtherCharWrong)
      for c in self.chars:
        if c.similarityGroup == char.similarityGroup:
          if c.priority >= priorityBreakGroup: c.similarityGroup=None
          elif c.priority > priorityOfGroupWrong: c.priority = priorityOfGroupWrong
    elif path=="/status":
      self.chars.sort(key=byPriority)
      cp=self.chars[:] ; r='<html><head><title>Current Status</title><meta http-equiv="Content-Type" content="text/html; charset=%s"></head><body><h2>Current Status</h2>(score/priority number is shown to the left of each item)<br>' % (self.charset,)
      while cp:
        if not cp[0].supposedToKnow:
          del cp[0] ; continue
        if cp[0].priority >= priorityBreakGroup: thisGrp=[0]
        else: thisGrp=list(filter(lambda x:x==0 or (cp[x].similarityGroup and cp[x].similarityGroup==cp[0].similarityGroup and cp[x].priority < priorityBreakGroup),range(len(cp))))
        if len(thisGrp)>1 and not r.endswith("<hr>"): r+="<hr>"
        if len(thisGrp)>1: r+="<em>"+str(len(thisGrp))+" similar items:</em><br>"
        for g in thisGrp: r += str(cp[g].priority)+": "+cp[g].hanzi+" "+cp[g].pinyin+"<br>"
        if len(thisGrp)>1: r+="<hr>"
        thisGrp.reverse()
        for toDel in thisGrp: del cp[toDel]
      return (r+"</body></html>").encode(self.charset)
    else:
      if path=="/checkallknown": self.thisSession = list(filter(lambda x:x.supposedToKnow,self.chars)) # TODO: Document this URL
      char,step = self.chooseChar(),1
    return char.htmlString(self,step,len(self.thisSession)).encode(self.charset)
  def chooseChar(self):
    if not self.thisSession:
      self.chars.sort(key=byPriority)
      if sessionLen==initSessionLen:
        self.thisSession = self.chars[:sessionLen] # introduce in order the first time (especially if the second one is just a straight line ("yi1"), as one beginner thought the program had gone wrong when he saw this)
        self.thisSession.reverse() # because taken out by pop()
      else: self.thisSession = random.sample(self.chars[:int(sessionLen*sampleConst)],sessionLen) # TODO need a better way than that.  NB high priority should be VERY likely, but others should have a chance.  try as-is for now
    return self.thisSession.pop()
  def save(self): Pickler(open(dumpFile,"wb"),-1).dump(self)
  def countKnown(self):
    charsSeen = sessnLen = newChars = 0
    secure=[] ; insecure=[]
    self.chars.sort(key=byPriority)
    for c in self.chars:
      if c.supposedToKnow:
        charsSeen += 1
        if c.priority>0: secure.append(c.hanzi)
        else: insecure.append(c.hanzi)
      else: newChars += 1
      if newChars == 2: sessnLen = charsSeen
    return charsSeen,sessnLen,secure,insecure

try:
  dumped = open(dumpFile,"rb")
except IOError: dumped = None
if dumped:
  thechars = Unpickler(dumped).load()
  dumped.close()
  thechars.thisSession = []
  if os.stat(tableFile).st_mtime > os.stat(dumpFile).st_mtime: thechars.readTable()
  try:
    if os.stat(knownFile).st_mtime > os.stat(dumpFile).st_mtime: thechars.readKnown()
  except OSError: pass
  try:
    if os.stat(reviseFile).st_mtime > os.stat(dumpFile).st_mtime: thechars.readRevise()
  except OSError: pass
  updateSessionLen()
else:
  thechars=CharDbase()

class RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.startswith("/fav"):
      self.send_response(404) ; self.end_headers() ; return
    self.send_response(200)
    self.send_header("Content-type","text/html; charset="+thechars.charset)
    self.end_headers()
    if self.path.startswith("/quit"):
      r=thechars.processRequest("/status").decode(thechars.charset)
      r=r[:r.index("<body>")+6]+"Server terminating."+r[r.index("<body>")+6:]
      self.wfile.write(r.encode(thechars.charset))
      thread.start_new_thread(terminate_server,()) # can terminate the server after this request
    else: self.wfile.write(thechars.processRequest(self.path))
    self.wfile.close() # needed or will wait for bkg speaking processes etc
def do_session():
  portNo = firstPortNo ; server = None
  while portNo < firstPortNo+100:
    try:
      server = HTTPServer((listenAddr,portNo),RequestHandler)
      break
    except socket.error: portNo += 1
  assert server, "Couldn't find a port to run the server on"
  if ("win" not in sys.platform) and getoutput("which x-www-browser 2>/dev/null"): # (try to find x-www-browser, but not on windows/cygwin/darwin)
    os.system("x-www-browser http://localhost:%d/%s &" % (portNo,str(random.random()))) # shouldn't need a sleep as should take a while to start anyway
  else:
    try:
      import webbrowser
      webbrowser.open_new("http://localhost:%d/%s" % (portNo,str(random.random())))
    except ImportError: pass # fall through to command-line message
  # Do this as well, in case that command failed:
  print ("") ; print ("") ; print ("")
  print ("Server running.  If a web browser does not appear automatically,")
  print ("please start one yourself and go to")
  print ("http://localhost:%d/%d" % (portNo,random.randint(1,99999)))
  print ("") ; print ("") ; print ("")
  server.serve_forever()

if sys.argv[-1]=='--count':
  x,y,sec,insec=thechars.countKnown()
  print ("%d (of which %d seem secure)" % (x,len(sec)))
elif sys.argv[-1]=='--show-secure':
  x,y,sec,insec=thechars.countKnown()
  print (" ".join(sec))
elif sys.argv[-1]=='--show-wfx':
  # the result of this might need charset conversion
  # (and the conversion of charlearn scores to Wenlin histories is only approximate)
  print ("""<?xml version='1.0'?>
<!-- Wenlin Flashcard XML file -->
<stack owner='Anonymous' reward='points'>""")
  thechars.chars.sort(key=byPriority)
  for c in thechars.chars:
    print ("<card type='d'><question>"+c.hanzi+"</question>")
    trials = "" ; score = 0
    if c.supposedToKnow:
        if c.priority < 0:
            trials += "n"
            p = priorityIfGotWrong
            while p < c.priority:
                trials += "y" ; score += 1
                p /= 2
        p = 1
        while p < c.priority:
            trials += "y" ; score += 1
            p *= 2
    print ("<history score='%d' trials='%d' recent='%s'></history></card>" % (score,len(trials),trials))
  print ("</stack>")
else: do_session()

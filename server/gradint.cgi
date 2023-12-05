#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  (either Python 2 or Python 3)

program_name = "gradint.cgi v1.33 (c) 2011,2015,2017-23 Silas S. Brown.  GPL v3+"

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

gradint_dir = "$HOME/gradint" # include samples/prompts
path_add = "$HOME/gradint/bin" # include sox, lame, espeak, maybe oggenc
lib_path_add = "$HOME/gradint/lib"
espeak_data_path = "$HOME/gradint"

import os, os.path, sys, cgi, urllib, time
try: from commands import getoutput # Python 2
except: from subprocess import getoutput # Python 3
try: from urllib import quote,quote_plus,unquote # Python 2
except: from urllib.parse import quote,quote_plus,unquote # Python 3
home = os.environ.get("HOME","")
if not home:
  try:
    import pwd
    home = os.path.expanduser("~{0}".format(pwd.getpwuid(os.getuid())[0]))
  except: home=0
  if not home: home = ".." # assume we're in public_html
gradint_dir = gradint_dir.replace("$HOME",home)
path_add = path_add.replace("$HOME",home)
lib_path_add = lib_path_add.replace("$HOME",home)
espeak_data_path = espeak_data_path.replace("$HOME",home)
try: import Cookie # Python 2
except: import http.cookies as Cookie # Python 3
import random
if "QUERY_STRING" in os.environ and "&" in os.environ["QUERY_STRING"] and ";" in os.environ["QUERY_STRING"]: os.environ["QUERY_STRING"]=os.environ["QUERY_STRING"].replace(";","%3B") # for dictionary sites to add words that contain semicolon
try: query = cgi.FieldStorage(encoding="utf-8") # Python 3
except: query = cgi.FieldStorage() # Python 2
os.chdir(gradint_dir) ; sys.path.insert(0,os.getcwd())
os.environ["PATH"] = path_add+":"+os.environ["PATH"]
if "LD_LIBRARY_PATH" in os.environ: os.environ["LD_LIBRARY_PATH"] = lib_path_add+":"+os.environ["LD_LIBRARY_PATH"]
else: os.environ["LD_LIBRARY_PATH"] = lib_path_add
os.environ["ESPEAK_DATA_PATH"] = espeak_data_path

cginame = os.sep+sys.argv[0] ; cginame=cginame[cginame.rindex(os.sep)+1:]
sys.stderr=open("/dev/null","w") ; sys.argv = []
gradint = None
def reinit_gradint(): # if calling again, also redo setup_userID after
    global gradint,langFullName
    if gradint: gradint = reload(gradint)
    else: import gradint
    gradint.waitOnMessage = lambda *args:False
    langFullName = {}
    for l in gradint.ESpeakSynth().describe_supported_languages().split():
        abbr,name = gradint.S(l).split("=")
        langFullName[abbr]=name
    # Try to work out probable default language:
    lang = os.environ.get("HTTP_ACCEPT_LANGUAGE","")
    if lang:
        for c in [',',';','-']:
            if c in lang: lang=lang[:lang.index(c)]
        if not lang in langFullName: lang=""
    if lang:
        gradint.firstLanguage = lang
        if not lang=="en": gradint.secondLanguage="en"
    elif " zh-" in os.environ.get("HTTP_USER_AGENT",""): gradint.firstLanguage,gradint.secondLanguage = "zh","en" # Chinese iPhone

reinit_gradint()

def main():
  if "id" in query: # e.g. from redirectHomeKeepCookie
    os.environ["HTTP_COOKIE"]="id="+query.getfirst("id")
    print ('Set-Cookie: id=' + query.getfirst("id")+'; expires=Wed, 1 Dec 2036 23:59:59 GMT')
  if has_userID(): setup_userID() # always, even for justSynth, as it may include a voice selection (TODO consequently being called twice in many circumstances, could make this more efficient)
  filetype=""
  if "filetype" in query: filetype=query.getfirst("filetype")
  if not filetype in ["mp3","ogg","wav"]: filetype="mp3"
  for k in query.keys():
    if k.startswith("del-"):
     k=unquote(unquote(k)) # might be needed
     if '=' in k:
       l2,l1 = k[4:].split('=')
       setup_userID()
       gradint.delOrReplace(gradint.ensure_unicode(l2),gradint.ensure_unicode(l1),"","","delete")
       return listVocab(True)
  if "js" in query: # just synthesize (js=text jsl=language)
    if "jsl" in query: justSynth(query.getfirst("js"), query.getfirst("jsl"),filetype=filetype)
    else: justSynth(query.getfirst("js"),filetype=filetype)
  elif "spk" in query: # speak (l1,l2 the langs, l1w,l2w the words)
    gradint.justSynthesize="0"
    if "l2w" in query and query.getfirst("l2w"):
      gradint.startBrowser=lambda *args:0
      if query.getfirst("l2")=="zh" and gradint.sanityCheck(query.getfirst("l2w"),"zh"): gradint.justSynthesize += "#en Pinyin needs tones.  Please go back and add tone numbers." # speaking it because alert box might not work and we might be being called from HTML5 Audio stuff (TODO maybe duplicate sanityCheck in js, if so don't call HTML5 audio, then we can have an on-screen message here)
      else: gradint.justSynthesize += "#"+query.getfirst("l2").replace("#","").replace('"','')+" "+query.getfirst("l2w").replace("#","").replace('"','')
    if "l1w" in query and query.getfirst("l1w"): gradint.justSynthesize += "#"+query.getfirst("l1").replace("#","").replace('"','')+" "+query.getfirst("l1w").replace("#","").replace('"','')
    if gradint.justSynthesize=="0": return htmlOut('You must type a word in the box before pressing the Speak button.'+backLink) # TODO maybe add a Javascript test to the form also, IF can figure out if window.alert works
    serveAudio(stream = len(gradint.justSynthesize)>100, filetype=filetype)
  elif "add" in query: # add to vocab (l1,l2 the langs, l1w,l2w the words)
    if "l2w" in query and query.getfirst("l2w") and "l1w" in query and query.getfirst("l1w"):
      gradint.startBrowser=lambda *args:0
      if query.getfirst("l2")=="zh": scmsg=gradint.sanityCheck(query.getfirst("l2w"),"zh")
      else: scmsg=None
      if scmsg: htmlOut(gradint.B(scmsg)+gradint.B(backLink))
      else: addWord(query.getfirst("l1w"),query.getfirst("l2w"),query.getfirst("l1"),query.getfirst("l2"))
    else: htmlOut('You must type words in both boxes before pressing the Add button.'+backLink) # TODO maybe add a Javascript test to the form also, IF can figure out a way to tell whether window.alert() works or not
  elif "bulkadd" in query: # bulk adding, from authoring options
    dirID = setup_userID()
    def isOK(x):
      if x[0]=='W':
        try:
          int(x[1:])
          return True
        except: pass
    def mycmp(x,y): return cmp(int(x[1:]),int(y[1:]))
    keyList = sorted(filter(lambda x:isOK(x),query.keys()),mycmp)
    for k in keyList:
      l2w,l1w = query.getfirst(k).split('=',1)
      addWord(l1w,l2w,query.getfirst("l1"),query.getfirst("l2"),False)
    redirectHomeKeepCookie(dirID,"&dictionary=1") # '1' is special value for JS-only back link; don't try to link to referer as it might be a generated page
  elif "clang" in query: # change languages (l1,l2)
    dirID = setup_userID()
    if (gradint.firstLanguage,gradint.secondLanguage) == (query.getfirst("l1"),query.getfirst("l2")) and not query.getfirst("clang")=="ignore-unchanged": return htmlOut('You must change the settings before pressing the Change Languages button.'+backLink) # (external scripts can set clang=ignore-unchanged)
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": query.getfirst("l1"),"secondLanguage":query.getfirst("l2")})
    redirectHomeKeepCookie(dirID)
  elif "swaplang" in query: # swap languages
    dirID = setup_userID()
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": gradint.secondLanguage,"secondLanguage":gradint.firstLanguage})
    redirectHomeKeepCookie(dirID)
  elif "editsave" in query: # save 'vocab'
    dirID = setup_userID()
    if "vocab" in query: vocab=query.getfirst("vocab")
    else: vocab="" # user blanked it
    open(gradint.vocabFile,"w").write(vocab)
    redirectHomeKeepCookie(dirID)
  elif "edit" in query: # show the edit form
    dirID = setup_userID()
    try: v=open(gradint.vocabFile).read()
    except: v="" # (shouldn't get here unless they hack URLs)
    htmlOut('<form action="'+cginame+'" method="post"><textarea name="vocab" style="width:100%;height:80%" rows="15" cols="50">'+v+'</textarea><br><input type=submit name=editsave value="Save changes"> | <input type=submit name=placeholder value="Cancel"></form>',"Text edit your vocab list")
  elif "lesson" in query: # make lesson ("Start lesson" button)
    setup_userID()
    gradint.maxNewWords = int(query.getfirst("new")) # (shouldn't need sensible-range check here if got a dropdown; if they really want to hack the URL then ok...)
    gradint.maxLenOfLesson = int(float(query.getfirst("mins"))*60)
    # TODO save those settings for next time also?
    serveAudio(stream = True, inURL = False, filetype=filetype)
  elif "voNormal" in query: # voice option = normal
    setup_userID()
    gradint.voiceOption=""
    gradint.updateSettingsFile(gradint.settingsFile,{"voiceOption":""})
    listVocab(True)
  elif "vopt" in query: # set voice option
    setup_userID()
    for v in gradint.guiVoiceOptions:
      if v.lower()=="-"+query.getfirst("vopt").lower():
        gradint.voiceOption = v
        gradint.updateSettingsFile(gradint.settingsFile,{"voiceOption":v})
        break
    listVocab(True)
  elif "lFinish" in query:
    dirID = setup_userID()
    try: os.rename(gradint.progressFile+'-new',gradint.progressFile)
    except: pass # probably a duplicate GET
    try: os.remove(gradint.progressFile+'-ts') # the timestamp file
    except: pass
    redirectHomeKeepCookie(dirID)
  elif not isAuthoringOption(query): listVocab(has_userID()) # default screen

def U(x):
  try: return x.decode('utf-8')
  except: return x

def isAuthoringOption(query):
  # TODO document the ?author=1 option
  if "author" in query:
    htmlOut('<form action="'+cginame+'" method="post"><h2>Gradint word list authoring mode</h2>This can help you put word lists on your website. The words will be linked to this Gradint server so your visitors can choose which ones to hear and/or add to their personal lists.<p>Type any text in the box below; use blank lines to separate paragraphs. To embed a word list in your text, type:<br><em>phrase 1</em>=<em>meaning 1</em><br><em>phrase 2</em>=<em>meaning 2</em><br><em>phrase 3</em>=<em>meaning 3</em><br>etc, and <b>make sure there is a blank line before and after the list</b>. Then press <input type=submit name="generate" value="Generate HTML">.<p>Language for phrases: '+langSelect('l2',gradint.secondLanguage)+' and for meanings: '+langSelect('l1',gradint.firstLanguage)+'<p><textarea name="text" style="width:100%;height:80%" rows="15" cols="50"></textarea><br><input type=submit name="generate" value="Generate HTML"></form>',"Word list authoring",links=0)
    # TODO maybe langSelect for mand+cant together ? (but many wordlists wld be topolect-specific)
  elif "generate" in query:
    l1,l2,txt = query.getfirst("l1"),query.getfirst("l2"),query.getfirst("text")
    paras = "\n".join([l.strip() for l in U(txt).replace("\r\n","\n").replace("\r","\n").split("\n")]).split("\n\n")
    need_h5a = False
    for i in xrange(len(paras)):
        lines = filter(lambda x:x,paras[i].split("\n")) # filter needed for trailing newline on document
        if allLinesHaveEquals(lines):
            paras[i] = authorWordList(lines,l1,l2)
            need_h5a = True
        # TODO else some wiki markup for links etc ? (but you can alter the HTML after)
    if need_h5a: h5astr = h5a()
    else: h5astr = ""
    htmlOut(HTML_and_preview(h5astr+encodeAmp('<p>'.join(paras))),"HTML result",links=0)
  else: return False
  return True
def allLinesHaveEquals(lines):
    if not lines: return False
    for l in lines:
        if not '=' in l: return False
    return True
def authorWordList(lines,l1,l2):
    gradintUrl = os.environ["SCRIPT_URI"] # will be http:// or https:// as appropriate
    r=[] ; count = 0
    # could have target="gradint" in the following, but it may be in a background tab (target="_blank" not recommended as could accumulate many)
    r.append('<form action="%s" method="post" accept-charset="utf-8"><table style="margin-left:auto;margin-right:auto;border:thin solid blue"><tr><td colspan=3 style="text-align:center"><em>Click on each word for audio</em></td></tr>' % gradintUrl)
    for l in lines:
        l2w,l1w = l.split('=',1)
        r.append('<tr><td><input type="checkbox" name="W%d" value="%s=%s" checked></td><td>%s</td><td>%s</td></tr>' % (count,l2w,l1w,U(justsynthLink(l2w.encode('utf-8'),l2)).replace('HREF="'+cginame+'?','HREF="'+gradintUrl+'?'),U(justsynthLink(l1w.encode('utf-8'),l1)).replace('HREF="'+cginame+'?','HREF="'+gradintUrl+'?')))
        count += 1
    # could have target="gradint" in the following href, but see comment above
    r.append('<tr><td colspan=3><input type="submit" name="bulkadd" value="Add selected words"> to your <a href="%s">personal list</a></td></tr></table><input type="hidden" name="l1" value="%s"><input type="hidden" name="l2" value="%s"></form>' % (gradintUrl,l1,l2))
    return ''.join(r)
def encodeAmp(uniStr):
  # HTML-ampersand encode when we don't know if the server will be utf-8 after copy/paste
  r=[]
  for c in uniStr:
    if ord(c)>126: r.append("&#"+str(ord(c))+";")
    else: r.append(c)
  return ''.join(r)
def HTML_and_preview(code): return '<h2>HTML code</h2><textarea style="width:100%%;height:40%%" rows=7 cols=50>%s</textarea><h2>Preview</h2>%s' % (code.replace('&','&amp;').replace('<','&lt;'),code)

def justSynth(text,lang="",filetype=""):
  if lang: lang = lang.replace("#","").replace('"','')+" "
  gradint.justSynthesize=lang+text.replace("#","").replace('"','')
  if not filetype in ["mp3","ogg","wav"]: filetype="mp3"
  serveAudio(stream = len(text)>80, filetype=filetype)

def justsynthLink(text,lang=""): # assumes written function h5a
  if lang in gradint.synth_partials_voices and gradint.guiVoiceOptions: cacheInfo="&curVopt="+gradint.voiceOption
  else: cacheInfo=""
  return '<A HREF="'+cginame+'?js='+gradint.S(quote_plus(text))+'&jsl='+quote_plus(lang)+cacheInfo+'" onClick="return h5a(this);">'+gradint.S(text)+'</A>'
# TODO if h5a's canPlayType etc works, cld o/p a lesson as a JS web page that does its own 'take out of event stream' and 'progress write-back'.  wld need to code that HERE by inspecting the finished Lesson object, don't call play().

def htmlOut(body_u8,title_extra="",links=1):
    print ("Content-type: text/html; charset=utf-8\n")
    if title_extra: title_extra=": "+title_extra
    print ('<html lang="en"><head><title>Gradint Web edition'+title_extra+'</title>')
    print ('<meta name="mobileoptimized" content="0"><meta name="viewport" content="width=device-width">')
    print ('<script>if(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)document.write("<style>body,input,textarea { background-color: black; color: #c0c000; } select,input[type=submit],input[type=button] { background-color: #300020; color: #c0c000; } select[disabled],input[disabled] { background-color: #101010; color: #b0b000; } a:link { color: #00b000; } a:visited { color: #00c0c0; } a:hover { color: red; }</style>");</script>')
    print ('</head><body>')
    if type(body_u8)==type(u""): body_u8=body_u8.encode('utf-8')
    if hasattr(sys.stdout,'buffer'): # Python 3
      sys.stdout.flush()
      sys.stdout.buffer.write(body_u8)
      sys.stdout.flush()
    else: print(body_u8)
    print ('<HR>')
    if links:
        print ('This is Gradint Web edition.  If you need recorded words or additional functions, please <A HREF="http://ssb22.user.srcf.net/gradint/">download the full version of Gradint</A>.')
        # TODO @ low-priority: Android 3 <input type="file" accept="audio/*;capture=microphone"></input>
        if "iPhone" in os.environ.get("HTTP_USER_AGENT","") and gradint.secondLanguage=="zh": print ('<p>You can also try the Open University <A HREF="http://itunes.apple.com/gb/app/chinese-characters-first-steps/id441549197?mt=8#">Chinese Characters First Steps</A> iPhone application.')
    print ('<p>'+program_name[:program_name.index("(")]+"using "+gradint.program_name[:gradint.program_name.index("(")])
    print ("</body></html>")
backLink = ' <A HREF="'+cginame+'" onClick="history.go(-1);return false">Back</A>' # TODO may want to add a random= to the non-js HREF

def serveAudio(stream=0, filetype="mp3", inURL=1):
  # caller imports gradint (and sets justSynthesize or whatever) first
  if os.environ.get("HTTP_IF_MODIFIED_SINCE",""):
    print ("Status: 304 Not Modified\n\n") ; return
  if filetype=="mp3": print ("Content-type: audio/mpeg")
  else: print ("Content-type: audio/"+filetype) # ok for ogg, wav?
  if inURL:
    print ("Last-Modified: Sun, 06 Jul 2008 13:20:05 GMT")
    print ("Expires: Wed, 1 Dec 2036 23:59:59 GMT") # TODO: S2G
  gradint.out_type = filetype
  def mainOrSynth():
    oldProgress = None ; rollback = False
    if not gradint.justSynthesize and 'h5a' in query:
      # TODO: if os.environ.get('HTTP_RANGE','')=='bytes=0-1' then that'll be '\xff' for mp3 but would need to stop the web server from adding a Content-Length etc (flush stdout and wait indefinitely for server to terminate the cgi process??)
      try: oldProgress = open(gradint.progressFile).read()
      except: pass
      rollback = True
      if 'lesson' in query: random.seed(query.getfirst('lesson')) # so clients that re-GET same lesson from partway through can work
      if os.environ.get('HTTP_X_PLAYBACK_SESSION_ID',''): # seen on iOS: assumes the stream is a live broadcast and reconnecting to it continues where it left off.  TODO: cache the mp3 output? (but don't delay the initial response)  Recalculating for now with sox trim:
        if os.path.exists(gradint.progressFile+'-ts'):
         trimTo = time.time() - os.stat(gradint.progressFile+'-ts').st_mtime
         if trimTo < gradint.maxLenOfLesson:
          cin,cout = os.popen2("sox "+(gradint.soundCollector.soxParams()+' - ')*2+" trim "+str(int(trimTo)))
          gradint.soundCollector.o,copyTo = cin,gradint.soundCollector.o
          def copyStream(a,b):
            while True:
              try: x = a.read(1024)
              except EOFError: break
              b.write(x)
            b.close()
          import thread ; thread.start_new(copyStream,(cout,copyTo))
         else: open(gradint.progressFile+'-ts','w') # previous one was abandoned, restart
        else: open(gradint.progressFile+'-ts','w') # create 1st one
      # end of if HTTP_X_PLAYBACK_SESSION_ID
    try: gradint.main()
    except SystemExit:
      if not gradint.justSynthesize:
        o1,o2 = gradint.write_to_stdout,gradint.outputFile
        reinit_gradint() ; setup_userID()
        gradint.write_to_stdout,gradint.outputFile = o1,o2
        gradint.setSoundCollector(gradint.SoundCollector())
        gradint.justSynthesize = "en Problem generating the lesson. Check we have prompts for those languages." ; gradint.main() ; oldProgress = None
    if rollback: # roll back pending lFinish
      os.rename(gradint.progressFile,gradint.progressFile+'-new')
      if oldProgress: open(gradint.progressFile,'w').write(oldProgress)
  if stream:
    print ("Content-disposition: attachment; filename=gradint.mp3\n") # helps with some browsers that can't really do streaming
    sys.stdout.flush()
    gradint.write_to_stdout = 1
    gradint.outputFile="-."+filetype ; gradint.setSoundCollector(gradint.SoundCollector())
    mainOrSynth()
  else:
    tempdir = getoutput("mktemp -d")
    gradint.write_to_stdout = 0
    gradint.outputFile=tempdir+"/serveThis."+filetype ; gradint.setSoundCollector(gradint.SoundCollector())
    gradint.waitBeforeStart = 0
    mainOrSynth()
    print ("Content-Length: "+repr(os.stat(tempdir+"/serveThis."+filetype).st_size)+"\n")
    sys.stdout.flush()
    os.system("cat "+tempdir+"/serveThis."+filetype)
    os.system("rm -r "+tempdir)

def addWord(l1w,l2w,l1,l2,out=True):
    if out: dirID=setup_userID()
    if not (gradint.firstLanguage,gradint.secondLanguage) == (l1,l2):
      if not ((gradint.firstLanguage,gradint.secondLanguage) == (l2,l1) and "HTTP_REFERER" in os.environ and not cginame in os.environ["HTTP_REFERER"]): gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": l1,"secondLanguage":l2})
      gradint.firstLanguage,gradint.secondLanguage = l1,l2
    if (l1w+"_"+l1,l2w+"_"+l2) in map(lambda x:x[1:],gradint.parseSynthVocab(gradint.vocabFile,forGUI=1)):
      if out: htmlOut('This word is already in your list.'+backLink)
      return
    gradint.appendVocabFileInRightLanguages().write(gradint.B(l2w)+gradint.B("=")+gradint.B(l1w)+gradint.B("\n"))
    if not out: return
    if "HTTP_REFERER" in os.environ and not cginame in os.environ["HTTP_REFERER"]: extra="&dictionary="+quote(os.environ["HTTP_REFERER"])
    else: extra=""
    redirectHomeKeepCookie(dirID,extra)

def redirectHomeKeepCookie(dirID,extra=""):
    dirID = gradint.S(dirID) # just in case
    print ("Location: "+cginame+"?random="+str(random.random())+"&id="+dirID[dirID.rindex("/")+1:]+extra+"\n")

def langSelect(name,curLang):
    curLang = gradint.espeak_language_aliases.get(curLang,curLang)
    return '<select name="'+name+'">'+''.join(['<option value="'+abbr+'"'+gradint.cond(abbr==curLang," selected","")+'>'+localise(abbr)+' ('+abbr+')'+'</option>' for abbr in sorted(langFullName.keys())])+'</select>'

def numSelect(name,nums,curNum): return '<select name="'+name+'">'+''.join(['<option value="'+str(num)+'"'+gradint.cond(num==curNum," selected","")+'>'+str(num)+'</option>' for num in nums])+'</select>'

def localise(x,span=0):
    r=gradint.localise(x)
    if r==x: return langFullName.get(gradint.espeak_language_aliases.get(x,x),x)
    if span==1: r="<span lang=\""+gradint.firstLanguage+"\">"+r+"</span>"
    elif span==2: r+='" lang="'+gradint.firstLanguage
    if type(r)==type("")==type(u""): return r # Python 3
    else: return r.encode('utf-8') # Python 2
for k,v in {"Swap":{"zh":u"交换","zh2":u"交換"},
            "Text edit":{"zh":u"文本编辑"},
            "Delete":{"zh":u"删除","zh2":u"刪除"},
            "Really delete this word?":{"zh":u"真的删除这个词?","zh2":u"真的刪除這個詞?"},
            "Your word list":{"zh":u"你的词汇表","zh2":u"你的詞彙表"},
            "click for audio":{"zh":u"击某词就听声音","zh2":u"擊某詞就聽聲音"},
            "Repeats":{"zh":u"重复计数","zh2":u"重複計數"},
            "To edit this list on another computer, type":{"zh":u"要是想在其他的电脑或手机编辑这个词汇表，请在别的设备打","zh2":u"要是想在其他的電腦或手機編輯這個詞彙表，請在別的設備打"},
            "Your word list is empty.":{"zh":u"词汇表没有词汇，加一些吧","zh2":u"詞彙表沒有詞彙，加一些吧"}
            }.items():
  if not k in gradint.GUI_translations: gradint.GUI_translations[k]=v

def h5a():
    body = """<script><!--
function h5a(link,endFunc) { if (document.createElement) {
   var ae = document.createElement('audio');
   function cp(t,lAdd) { if(ae.canPlayType && function(s){return s!="" && s!="no"}(ae.canPlayType(t))) {
       if (link.href) ae.setAttribute('src', link.href+lAdd);
       else ae.setAttribute('src', link+lAdd);
       if (typeof endFunc !== 'undefined') ae.addEventListener("ended", endFunc, false);
       ae.play(); return true;
    } return false; }
   if (cp('audio/mpeg','')) return false;"""
    if gradint.got_program("oggenc"): body += """else if (cp('audio/ogg',"&filetype=ogg")) return false;"""
    body += """} return true; }
//--></script>"""
    return body
def hasVoiceOptions(l):
    if not l in gradint.synth_partials_voices: return False
    if not gradint.guiVoiceOptions: return False
    try: voices = os.listdir(gradint.partialsDirectory+os.sep+l)
    except: voices = []
    for v in voices:
        if "-" in v and v[:v.index("-")] in voices: return True
def listVocab(hasList): # main screen
    firstLanguage,secondLanguage = gradint.firstLanguage, gradint.secondLanguage
    # TODO button onClick: careful of zh w/out tones, wld need to JS this
    body = h5a() + '<center><form action="'+cginame+'">'
    gotVoiceOptions = (hasVoiceOptions(gradint.secondLanguage) or hasVoiceOptions(gradint.firstLanguage))
    if gotVoiceOptions:
      body += 'Voice option: <input type=submit name=voNormal value="Normal"'+gradint.cond(gradint.voiceOption=="",' disabled="disabled"',"")+'>'
      for v in gradint.guiVoiceOptions: body += ' | <input type=submit name=vopt value="'+v[1].upper()+v[2:]+'"'+gradint.cond(gradint.voiceOption==v,' disabled="disabled"',"")+'>'
      body += '<input type=hidden name=curVopt value="'+gradint.voiceOption+'">' # ignored by gradint.cgi but needed by browser cache to ensuer 'change voice option and press Speak again' works
      body += '<br>'
    # must have autocomplete=off if capturing keycode 13
    if gotVoiceOptions: cacheInfo="&curVopt="+gradint.voiceOption
    else: cacheInfo=""
    body += (localise("Word in %s",1) % localise(secondLanguage))+': <input type=text name=l2w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].spk.click();return false} else return true" onfocus="document.forms[0].onsubmit=\'document.forms[0].onsubmit=&quot;return true&quot;;document.forms[0].spk.click();return false\'" onblur="document.forms[0].onsubmit=\'return true\'"> <input type=submit name=spk value="'+localise("Speak",2)+'" onClick="if (!document.forms[0].l1w.value && !document.forms[0].l2w.value) return true; else return h5a(\''+cginame+'?spk=1&l1w=\'+document.forms[0].l1w.value+\'&l2w=\'+document.forms[0].l2w.value+\'&l1=\'+document.forms[0].l1.value+\'&l2=\'+document.forms[0].l2.value+\''+cacheInfo+'\');"><br>'+(localise("Meaning in %s",1) % localise(firstLanguage))+': <input type=text name=l1w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].add.click();return false} else return true" onfocus="document.forms[0].onsubmit=\'document.forms[0].onsubmit=&quot;return true&quot;;document.forms[0].add.click();return false\'" onblur="document.forms[0].onsubmit=\'return true\'"> <input type=submit name=add value="'+(localise("Add to %s",2) % localise("vocab.txt").replace(".txt",""))+'"><script><!--\nvar emptyString="";document.write(\' <input type=submit name=placeholder value="'+localise("Clear input boxes",2)+'" onClick="document.forms[0].l1w.value=document.forms[0].l2w.value=emptyString;document.forms[0].l2w.focus();return false">\')\n//--></script><p>'+localise("Your first language",1)+': '+langSelect('l1',firstLanguage)+' '+localise("second",1)+': '+langSelect('l2',secondLanguage)+' <nobr><input type=submit name=clang value="'+localise("Change languages",2)+'"><input type=submit name=swaplang value="'+localise("Swap",2)+'"></nobr>' # onfocus..onblur updating onsubmit is needed for iOS "Go" button
    def htmlize(l,lang):
       if type(l)==type([]) or type(l)==type(()): return htmlize(l[-1],lang)
       l = gradint.B(l)
       if gradint.B("!synth:") in l: return htmlize(l[l.index(gradint.B("!synth:"))+7:l.rfind(gradint.B("_"))],lang)
       return justsynthLink(l,lang)
    def deleteLink(l1,l2):
       r = []
       for l in [l2,l1]:
         if type(l)==type([]) or type(l)==type(()) or not gradint.B("!synth:") in l: return "" # Web-GUI delete in poetry etc not yet supported
         r.append(gradint.S(quote(l[l.index(gradint.B("!synth:"))+7:l.rfind(gradint.B("_"))])))
       r.append(localise("Delete",2))
       return ('<td><input type=submit name="del-%s%%3d%s" value="%s" onClick="return confirm(\''+localise("Really delete this word?")+'\');"></td>') % tuple(r)
    if hasList:
       gradint.availablePrompts = gradint.AvailablePrompts() # needed before ProgressDatabase()
       # gradint.cache_maintenance_mode=1 # don't transliterate on scan -> NO, including this scans promptsDirectory!
       gradint.ESpeakSynth.update_translit_cache=lambda *args:0 # do it this way instead
       data = gradint.ProgressDatabase().data ; data.reverse()
       if data: hasList = "<p><table style=\"border: thin solid green\"><caption><nobr>"+localise("Your word list",1)+"</nobr> <nobr>("+localise("click for audio",1)+")</nobr> <input type=submit name=edit value=\""+localise("Text edit",2)+"\"></caption><tr><th>"+localise("Repeats",1)+"</th><th>"+localise(gradint.secondLanguage,1)+"</th><th>"+localise(gradint.firstLanguage,1)+"</th></tr>"+"".join(["<tr><td>%d</td><td lang=\"%s\">%s</td><td lang=\"%s\">%s</td>%s" % (num,gradint.secondLanguage,htmlize(dest,gradint.secondLanguage),gradint.firstLanguage,htmlize(src,gradint.firstLanguage),deleteLink(src,dest)) for num,src,dest in data])+"</table>"
       else: hasList=""
    else: hasList=""
    if hasList: body += '<p><table style="border:thin solid blue"><tr><td>'+numSelect('new',range(2,10),gradint.maxNewWords)+' '+localise("new words in")+' '+numSelect('mins',[15,20,25,30],int(gradint.maxLenOfLesson/60))+' '+localise('mins')+""" <input type=submit name=lesson value="""+'"'+localise("Start lesson",2)+"""" onClick="document.forms[0].lesson.disabled=1; document.forms[0].lesson.value='Please wait while the lesson starts to play'; return h5a('"""+cginame+'?lesson='+str(random.random())+"""&h5a=1&new='+document.forms[0].new.value+'&mins='+document.forms[0].mins.value,function(){location.href='"""+cginame+'?lFinish='+str(random.random())+"""'})"></td></tr></table>"""
    if "dictionary" in query:
        if query.getfirst("dictionary")=="1": body += '<script><!--\ndocument.write(\'<p><a href="javascript:history.go(-1)">'+localise("Back to referring site",1)+'</a>\')\n//--></script>' # apparently it is -1, not -2; the redirect doesn't count as one (TODO are there any JS browsers that do count it as 2?)
        else: body += '<p><a href="'+query.getfirst("dictionary")+'">'+localise("Back to dictionary",1)+'</a>' # TODO check for cross-site scripting
    if hasList:
      if "SCRIPT_URI" in os.environ: hasList += "<p>"+localise("To edit this list on another computer, type",1)+" <kbd>"+os.environ["SCRIPT_URI"]+"?id="+getCookieId()+"</kbd>"
    else: hasList="<P>"+localise("Your word list is empty.",1)
    body += hasList
    htmlOut(body+'</form></center><script><!--\ndocument.forms[0].l2w.focus()\n//--></script>')

def has_userID(): # TODO: can just call getCookieId with not too much extra overhead
    cookie_string = os.environ.get('HTTP_COOKIE',"")
    if cookie_string:
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        return 'id' in cookie

def getCookieId():
    cookie_string = os.environ.get('HTTP_COOKIE',"")
    if not cookie_string: return
    cookie = Cookie.SimpleCookie()
    cookie.load(cookie_string)
    if 'id' in cookie: return cookie['id'].value.replace('"','').replace("'","").replace("\\","")

def setup_userID():
    # MUST call before outputting headers (may set cookie)
    # Use the return value of this with -settings.txt, -vocab.txt etc
    if cginame=="gradint.cgi": dirName = "cgi-gradint-users" # as previous versions
    else: dirName = cginame+"-users" # TODO document this feature (you can symlink something-else.cgi to gradint.cgi and it will have a separate user directory) (however it still reports gradint.cgi on the footer)
    if not os.path.exists(dirName): os.system("mkdir "+dirName)
    userID = getCookieId()
    need_write = (userID and not os.path.exists(dirName+'/'+userID+'-settings.txt')) # maybe it got cleaned up
    if not userID:
        while True:
            userID = str(random.random())[2:]
            if not os.path.exists(dirName+'/'+userID+'-settings.txt'): break
        open(dirName+'/'+userID+'-settings.txt','w') # TODO this could still be a race condition (but should be OK under normal circumstances)
        need_write = 1
        print ('Set-Cookie: id=' + userID+'; expires=Wed, 1 Dec 2036 23:59:59 GMT') # TODO: S2G
    userID = dirName+'/'+userID
    gradint.progressFileBackup=gradint.pickledProgressFile=None
    gradint.vocabFile = userID+"-vocab.txt"
    gradint.progressFile = userID+"-progress.txt"
    gradint.settingsFile = userID+"-settings.txt"
    if need_write: gradint.updateSettingsFile(gradint.settingsFile,{'firstLanguage':gradint.firstLanguage,'secondLanguage':gradint.secondLanguage})
    else: gradint.readSettings(gradint.settingsFile)
    gradint.auto_advancedPrompt=1 # prompt in L2 if we don't have L1 prompts on the server, what else can we do...
    return userID

try: main()
except Exception as e:
  print ("Content-type: text/plain; charset=utf-8\n")
  sys.stdout.flush()
  import traceback
  try: traceback.print_exc(file=sys.stdout)
  except: pass
  sys.stdout.flush()
  if hasattr(sys.stdout,"buffer"): buf = sys.stdout.buffer
  else: buf = sys.stdout
  buf.write(repr(e).encode("utf-8"))

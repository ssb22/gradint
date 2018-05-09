#!/usr/bin/env python
# -*- coding: utf-8 -*-

program_name = "gradint.cgi v1.077 (c) 2011,2015,2017-18 Silas S. Brown.  GPL v3+"

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

import os, os.path, sys, commands, cgi, cgitb, urllib, time ; cgitb.enable()
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
import Cookie, random
if "QUERY_STRING" in os.environ and "&" in os.environ["QUERY_STRING"] and ";" in os.environ["QUERY_STRING"]: os.environ["QUERY_STRING"]=os.environ["QUERY_STRING"].replace(";","%3B") # for dictionary sites to add words that contain semicolon
query = cgi.parse()
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
        abbr,name = l.split("=")
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
    os.environ["HTTP_COOKIE"]="id="+query["id"][0]
    print 'Set-Cookie: id=' + query["id"][0]+'; expires=Wed, 1 Dec 2036 23:59:59 GMT'
  if has_userID(): setup_userID() # always, even for justSynth, as it may include a voice selection (TODO consequently being called twice in many circumstances, could make this more efficient)
  filetype=""
  if "filetype" in query: filetype=query["filetype"][0]
  if not filetype in ["mp3","ogg","wav"]: filetype="mp3"
  for k in query.keys():
    if k.startswith("del-"):
     k=urllib.unquote(urllib.unquote(k)) # might be needed
     if '=' in k:
       l2,l1 = k[4:].split('=')
       setup_userID()
       gradint.delOrReplace(gradint.ensure_unicode(l2),gradint.ensure_unicode(l1),"","","delete")
       return listVocab(True)
  if "js" in query: # just synthesize (js=text jsl=language)
    if "jsl" in query: justSynth(query["js"][0], query["jsl"][0],filetype=filetype)
    else: justSynth(query["js"][0],filetype=filetype)
  elif "spk" in query: # speak (l1,l2 the langs, l1w,l2w the words)
    gradint.justSynthesize="0"
    if "l2w" in query and query["l2w"][0]:
      gradint.startBrowser=lambda *args:0
      if query["l2"][0]=="zh" and gradint.sanityCheck(query["l2w"][0],"zh"): gradint.justSynthesize += "#en Pinyin needs tones.  Please go back and add tone numbers." # speaking it because alert box might not work and we might be being called from HTML5 Audio stuff (TODO maybe duplicate sanityCheck in js, if so don't call HTML5 audio, then we can have an on-screen message here)
      else: gradint.justSynthesize += "#"+query["l2"][0].replace("#","").replace('"','')+" "+query["l2w"][0].replace("#","").replace('"','')
    if "l1w" in query and query["l1w"][0]: gradint.justSynthesize += "#"+query["l1"][0].replace("#","").replace('"','')+" "+query["l1w"][0].replace("#","").replace('"','')
    if gradint.justSynthesize=="0": return htmlOut('You must type a word in the box before pressing the Speak button.'+backLink) # TODO maybe add a Javascript test to the form also, IF can figure out if window.alert works
    serveAudio(stream = len(gradint.justSynthesize)>100, filetype=filetype)
  elif "add" in query: # add to vocab (l1,l2 the langs, l1w,l2w the words)
    if "l2w" in query and query["l2w"][0] and "l1w" in query and query["l1w"][0]:
      gradint.startBrowser=lambda *args:0
      if query["l2"][0]=="zh": scmsg=gradint.sanityCheck(query["l2w"][0],"zh")
      else: scmsg=None
      if scmsg: htmlOut(scmsg+''+backLink)
      else: addWord(query["l1w"][0],query["l2w"][0],query["l1"][0],query["l2"][0])
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
      l2w,l1w = query[k][0].split('=',1)
      addWord(l1w,l2w,query["l1"][0],query["l2"][0],False)
    redirectHomeKeepCookie(dirID,"&dictionary=1") # '1' is special value for JS-only back link; don't try to link to referer as it might be a generated page
  elif "clang" in query: # change languages (l1,l2)
    dirID = setup_userID()
    if (gradint.firstLanguage,gradint.secondLanguage) == (query["l1"][0],query["l2"][0]) and not query["clang"][0]=="ignore-unchanged": return htmlOut('You must change the settings before pressing the Change Languages button.'+backLink) # (external scripts can set clang=ignore-unchanged)
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": query["l1"][0],"secondLanguage":query["l2"][0]})
    redirectHomeKeepCookie(dirID)
  elif "swaplang" in query: # swap languages
    dirID = setup_userID()
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": gradint.secondLanguage,"secondLanguage":gradint.firstLanguage})
    redirectHomeKeepCookie(dirID)
  elif "editsave" in query: # save 'vocab'
    dirID = setup_userID()
    if "vocab" in query: vocab=query["vocab"][0]
    else: vocab="" # user blanked it
    open(gradint.vocabFile,"w").write(vocab)
    redirectHomeKeepCookie(dirID)
  elif "edit" in query: # show the edit form
    dirID = setup_userID()
    try: v=open(gradint.vocabFile).read()
    except: v="" # (shouldn't get here unless they hack URLs)
    htmlOut('<form action="'+cginame+'" method="post"><textarea name="vocab" style="width:100%;height:80%" rows="15" cols="50">'+v+'</textarea><br><input type=submit name=editsave value="Save changes"> | <input type=submit name=dummy value="Cancel"></form>',"Text edit your vocab list")
  elif "lesson" in query: # make lesson
    setup_userID()
    gradint.maxNewWords = int(query["new"][0]) # (shouldn't need sensible-range check here if got a dropdown; if they really want to hack the URL then ok...)
    gradint.maxLenOfLesson = int(float(query["mins"][0])*60)
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
      if v.lower()=="-"+query["vopt"][0].lower():
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

def isAuthoringOption(query):
  # TODO document the ?author=1 option
  if "author" in query:
    htmlOut('<form action="'+cginame+'" method="post"><h2>Gradint word list authoring mode</h2>This can help you put word lists on your website. The words will be linked to this Gradint server so your visitors can choose which ones to hear and/or add to their personal lists.<p>Type any text in the box below; use blank lines to separate paragraphs. To embed a word list in your text, type:<br><em>phrase 1</em>=<em>meaning 1</em><br><em>phrase 2</em>=<em>meaning 2</em><br><em>phrase 3</em>=<em>meaning 3</em><br>etc, and <b>make sure there is a blank line before and after the list</b>. Then press <input type=submit name="generate" value="Generate HTML">.<p>Language for phrases: '+langSelect('l2',gradint.secondLanguage)+' and for meanings: '+langSelect('l1',gradint.firstLanguage)+'<p><textarea name="text" style="width:100%;height:80%" rows="15" cols="50"></textarea><br><input type=submit name="generate" value="Generate HTML"></form>',"Word list authoring",links=0)
    # TODO maybe langSelect for mand+cant together ? (but many wordlists wld be topolect-specific)
  elif "generate" in query:
    l1,l2,txt = query["l1"][0],query["l2"][0],query["text"][0]
    paras = "\n".join([l.strip() for l in txt.replace("\r\n","\n").replace("\r","\n").decode('utf-8').split("\n")]).split("\n\n")
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
    gradintUrl = os.environ["SCRIPT_URI"]
    r=[] ; count = 0
    # could have target="gradint" in the following, but it may be in a background tab (target="_blank" not recommended as could accumulate many)
    r.append('<form action="%s" method="post" accept-charset="utf-8"><table style="margin-left:auto;margin-right:auto;border:thin solid blue"><tr><td colspan=3 style="text-align:center"><em>Click on each word for audio</em></td></tr>' % gradintUrl)
    for l in lines:
        l2w,l1w = l.split('=',1)
        r.append('<tr><td><input type="checkbox" name="W%d" value="%s=%s" checked></td><td>%s</td><td>%s</td></tr>' % (count,l2w,l1w,justsynthLink(l2w.encode('utf-8'),l2).replace('HREF="'+cginame+'?','HREF="'+gradintUrl+'?').decode('utf-8'),justsynthLink(l1w.encode('utf-8'),l1).replace('HREF="'+cginame+'?','HREF="'+gradintUrl+'?').decode('utf-8')))
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
  return '<A HREF="'+cginame+'?js='+urllib.quote_plus(text)+'&jsl='+urllib.quote_plus(lang)+cacheInfo+'" onClick="return h5a(this);">'+text+'</A>'
# TODO if h5a's canPlayType etc works, cld o/p a lesson as a JS web page that does its own 'take out of event stream' and 'progress write-back'.  wld need to code that HERE by inspecting the finished Lesson object, don't call play().

def htmlOut(body_u8,title_extra="",links=1):
    print "Content-type: text/html; charset=utf-8" ; print
    if title_extra: title_extra=": "+title_extra
    print '<html><head><title>Gradint Web edition'+title_extra+'</title>'
    print '<meta name="mobileoptimized" content="0"><meta name="viewport" content="width=device-width">'
    print '</head><body>'+body_u8
    print '<HR>'
    if links:
        print 'This is Gradint Web edition.  If you need recorded words or additional functions, please <A HREF="http://people.pwf.cam.ac.uk/ssb22/gradint/">download the full version of Gradint</A>.'
        # TODO @ low-priority: Android 3 <input type="file" accept="audio/*;capture=microphone"></input>
        if "iPhone" in os.environ.get("HTTP_USER_AGENT","") and gradint.secondLanguage=="zh": print '<p>You can also try the Open University <A HREF="http://itunes.apple.com/gb/app/chinese-characters-first-steps/id441549197?mt=8#">Chinese Characters First Steps</A> iPhone application.'
    print '<p>'+program_name[:program_name.index("(")]+"using "+gradint.program_name[:gradint.program_name.index("(")]
    print "</body></html>"
backLink = ' <A HREF="'+cginame+'" onClick="history.go(-1);return false">Back</A>' # TODO may want to add a random= to the non-js HREF

def serveAudio(stream=0, filetype="mp3", inURL=1):
  # caller imports gradint (and sets justSynthesize or whatever) first
  if filetype=="mp3": print "Content-type: audio/mpeg"
  else: print "Content-type: audio/"+filetype # ok for ogg, wav?
  if inURL:
    print "Last-Modified: Sun, 06 Jul 2008 13:20:05 GMT"
    print "Expires: Wed, 1 Dec 2036 23:59:59 GMT"
  gradint.out_type = filetype
  def mainOrSynth():
    oldProgress = None ; rollback = False
    if not gradint.justSynthesize and 'h5a' in query:
      # TODO: if os.environ.get('HTTP_RANGE','')=='bytes=0-1' then that'll be '\xff' for mp3 but would need to stop the web server from adding a Content-Length etc (flush stdout and wait indefinitely for server to terminate the cgi process??)
      try: oldProgress = open(gradint.progressFile).read()
      except: pass
      rollback = True
      if 'lesson' in query: random.seed(query['lesson'][0]) # so clients that re-GET same lesson from partway through can work
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
    print "Content-disposition: attachment; filename=gradint.mp3" # helps with some browsers that can't really do streaming
    print ; sys.stdout.flush()
    gradint.write_to_stdout = 1
    gradint.outputFile="-."+filetype ; gradint.setSoundCollector(gradint.SoundCollector())
    mainOrSynth()
  else:
    tempdir = commands.getoutput("mktemp -d")
    gradint.write_to_stdout = 0
    gradint.outputFile=tempdir+"/serveThis."+filetype ; gradint.setSoundCollector(gradint.SoundCollector())
    gradint.waitBeforeStart = 0
    mainOrSynth()
    print "Content-Length:",os.stat(tempdir+"/serveThis."+filetype).st_size
    print ; sys.stdout.flush()
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
    gradint.appendVocabFileInRightLanguages().write(l2w+"="+l1w+"\n")
    if not out: return
    if "HTTP_REFERER" in os.environ and not cginame in os.environ["HTTP_REFERER"]: extra="&dictionary="+urllib.quote(os.environ["HTTP_REFERER"])
    else: extra=""
    redirectHomeKeepCookie(dirID,extra)

def redirectHomeKeepCookie(dirID,extra=""):
    print "Location: "+cginame+"?random="+str(random.random())+"&id="+dirID[dirID.rindex("/")+1:]+extra ; print

def langSelect(name,curLang):
    curLang = gradint.espeak_language_aliases.get(curLang,curLang)
    return '<select name="'+name+'">'+''.join(['<option value="'+abbr+'"'+gradint.cond(abbr==curLang," selected","")+'>'+localise(abbr)+' ('+abbr+')'+'</option>' for abbr in sorted(langFullName.keys())])+'</select>'

def numSelect(name,nums,curNum): return '<select name="'+name+'">'+''.join(['<option value="'+str(num)+'"'+gradint.cond(num==curNum," selected","")+'>'+str(num)+'</option>' for num in nums])+'</select>'

def localise(x):
    r=gradint.localise(x)
    if r==x: return langFullName.get(gradint.espeak_language_aliases.get(x,x),x)
    else: return r.encode('utf-8')
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
    body += (localise("Word in %s") % localise(secondLanguage))+': <input type=text name=l2w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].spk.click();return false} else return true" onfocus="document.forms[0].onsubmit=\'document.forms[0].onsubmit=&quot;return true&quot;;document.forms[0].spk.click();return false\'" onblur="document.forms[0].onsubmit=\'return true\'"> <input type=submit name=spk value="'+localise("Speak")+'" onClick="if (!document.forms[0].l1w.value && !document.forms[0].l2w.value) return true; else return h5a(\''+cginame+'?spk=1&l1w=\'+document.forms[0].l1w.value+\'&l2w=\'+document.forms[0].l2w.value+\'&l1=\'+document.forms[0].l1.value+\'&l2=\'+document.forms[0].l2.value+\''+cacheInfo+'\');"><br>'+(localise("Meaning in %s") % localise(firstLanguage))+': <input type=text name=l1w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].add.click();return false} else return true" onfocus="document.forms[0].onsubmit=\'document.forms[0].onsubmit=&quot;return true&quot;;document.forms[0].add.click();return false\'" onblur="document.forms[0].onsubmit=\'return true\'"> <input type=submit name=add value="'+(localise("Add to %s") % localise("vocab.txt").replace(".txt",""))+'"><script><!--\nvar emptyString="";document.write(\' <input type=submit name=dummy value="'+localise("Clear input boxes")+'" onClick="document.forms[0].l1w.value=document.forms[0].l2w.value=emptyString;document.forms[0].l2w.focus();return false">\')\n//--></script><p>'+localise("Your first language")+': '+langSelect('l1',firstLanguage)+' '+localise("second")+': '+langSelect('l2',secondLanguage)+' <nobr><input type=submit name=clang value="'+localise("Change languages")+'"><input type=submit name=swaplang value="'+localise("Swap")+'"></nobr>' # onfocus..onblur updating onsubmit is needed for iOS "Go" button
    def htmlize(l,lang):
       if type(l)==type([]) or type(l)==type(()): return htmlize(l[-1],lang)
       if "!synth:" in l: return htmlize(l[l.index("!synth:")+7:l.rfind("_")],lang)
       return justsynthLink(l,lang)
    def deleteLink(l1,l2):
       r = []
       for l in [l2,l1]:
         if type(l)==type([]) or type(l)==type(()) or not "!synth:" in l: return "" # Web-GUI delete in poetry etc not yet supported
         r.append(urllib.quote(l[l.index("!synth:")+7:l.rfind("_")]))
       r.append(localise("Delete"))
       return ('<td><input type=submit name="del-%s%%3d%s" value="%s" onClick="return confirm(\''+localise("Really delete this word?")+'\');"></td>') % tuple(r)
    if hasList:
       gradint.availablePrompts = gradint.AvailablePrompts() # needed before ProgressDatabase()
       # gradint.cache_maintenance_mode=1 # don't transliterate on scan -> NO, including this scans promptsDirectory!
       gradint.ESpeakSynth.update_translit_cache=lambda *args:0 # do it this way instead
       data = gradint.ProgressDatabase().data ; data.reverse()
       if data: hasList = "<p><table style=\"border: thin solid green\"><caption><nobr>"+localise("Your word list")+"</nobr> <nobr>("+localise("click for audio")+")</nobr> <input type=submit name=edit value=\""+localise("Text edit")+"\"></caption><tr><th>"+localise("Repeats")+"</th><th>"+localise(gradint.secondLanguage)+"</th><th>"+localise(gradint.firstLanguage)+"</th></tr>"+"".join(["<tr><td>%d</td><td>%s</td><td>%s</td>%s" % (num,htmlize(dest,gradint.secondLanguage),htmlize(src,gradint.firstLanguage),deleteLink(src,dest)) for num,src,dest in data])+"</table>"
       else: hasList=""
    else: hasList=""
    if hasList: body += '<P><table style="border:thin solid blue"><tr><td>'+numSelect('new',range(2,10),gradint.maxNewWords)+' '+localise("new words in")+' '+numSelect('mins',[15,20,25,30],int(gradint.maxLenOfLesson/60))+' '+localise('mins')+""" <input type=submit name=lesson value="""+'"'+localise("Start lesson")+"""" onClick="if(h5a('"""+cginame+'?lesson='+str(random.random())+"""&h5a=1&new='+document.forms[0].new.value+'&mins='+document.forms[0].mins.value,function(){location.href='"""+cginame+'?lFinish='+str(random.random())+"""'})) return true; else { document.forms[0].lesson.value='Please wait while the lesson starts to play'; document.forms[0].lesson.disabled=1; return false}"></td></tr></table>"""
    if "dictionary" in query:
        if query["dictionary"][0]=="1": body += '<script><!--\ndocument.write(\'<p><a href="javascript:history.go(-1)">'+localise("Back to referring site")+'</a>\')\n//--></script>' # apparently it is -1, not -2; the redirect doesn't count as one (TODO are there any JS browsers that do count it as 2?)
        else: body += '<p><a href="'+query["dictionary"][0]+'">'+localise("Back to dictionary")+'</a>' # TODO check for cross-site scripting
    if hasList:
      if "SCRIPT_URI" in os.environ: hasList += "<p>"+localise("To edit this list on another computer, type")+" <kbd>"+os.environ["SCRIPT_URI"]+"?id="+getCookieId()+"</kbd>"
    else: hasList="<P>"+localise("Your word list is empty.")
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
        print 'Set-Cookie: id=' + userID+'; expires=Wed, 1 Dec 2036 23:59:59 GMT'
    userID = dirName+'/'+userID
    gradint.progressFileBackup=gradint.pickledProgressFile=None
    gradint.vocabFile = userID+"-vocab.txt"
    gradint.progressFile = userID+"-progress.txt"
    gradint.settingsFile = userID+"-settings.txt"
    if need_write: gradint.updateSettingsFile(gradint.settingsFile,{'firstLanguage':gradint.firstLanguage,'secondLanguage':gradint.secondLanguage})
    else: gradint.readSettings(gradint.settingsFile)
    gradint.auto_advancedPrompt=1 # prompt in L2 if we don't have L1 prompts on the server, what else can we do...
    return userID

main()

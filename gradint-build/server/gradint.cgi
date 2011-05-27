#!/usr/bin/env python

program_name = "gradint.cgi v1.03 (c) 2011 Silas S. Brown.  GPL v3+"

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

gradint_dir = "/home/ssb22/gradint" # include samples/prompts
path_add = "/home/ssb22/gradint/bin" # include sox, lame, espeak, maybe oggenc
lib_path_add = "/home/ssb22/gradint/lib"
espeak_data_path = "/home/ssb22/gradint"

import os, os.path, sys, commands, cgi, cgitb, urllib ; cgitb.enable()
import Cookie, random
if "QUERY_STRING" in os.environ and "&" in os.environ["QUERY_STRING"] and ";" in os.environ["QUERY_STRING"]: os.environ["QUERY_STRING"]=os.environ["QUERY_STRING"].replace(";","%3B") # for dictionary sites to add words that contain semicolon
query = cgi.parse()
os.chdir(gradint_dir) ; sys.path.insert(0,os.getcwd())
os.environ["PATH"] = path_add+":"+os.environ["PATH"]
if "LD_LIBRARY_PATH" in os.environ: os.environ["LD_LIBRARY_PATH"] = lib_path_add+":"+os.environ["LD_LIBRARY_PATH"]
else: os.environ["LD_LIBRARY_PATH"] = lib_path_add
os.environ["ESPEAK_DATA_PATH"] = espeak_data_path

sys.stderr=open("/dev/null","w") ; import gradint

lDic = {}
for l in gradint.ESpeakSynth().describe_supported_languages().split():
    abbr,name = l.split("=")
    lDic[abbr]=name

# Try to work out probable default language:
lang = os.environ.get("HTTP_ACCEPT_LANGUAGE","")
if lang:
 for c in [',',';','-']:
   if c in lang: lang=lang[:lang.index(c)]
 if not lang in lDic: lang=""
if lang:
 gradint.firstLanguage = lang
 if not lang=="en": gradint.secondLanguage="en"
elif " zh-" in os.environ.get("HTTP_USER_AGENT",""): gradint.firstLanguage,gradint.secondLanguage = "zh","en" # Chinese iPhone

def main():
  if has_userID(): setup_userID() # always, even for justSynth, as it may include a voice selection (TODO consequently being called twice in many circumstances, could make this more efficient)
  if "id" in query:
    os.environ["HTTP_COOKIE"]="id="+query["id"][0]
    print 'Set-Cookie: id=' + query["id"][0]+'; expires=Wed, 1 Dec 2036 23:59:59 GMT'
  filetype=""
  if "filetype" in query: filetype=query["filetype"][0]
  if not filetype in ["mp3","ogg","wav"]: filetype="mp3"
  if "js" in query:
    if "jsl" in query: justSynth(query["js"][0], query["jsl"][0],filetype=filetype)
    else: justSynth(query["js"][0],filetype=filetype)
  elif "spk" in query:
    gradint.justSynthesize="0"
    if "l2w" in query and query["l2w"][0]:
      gradint.startBrowser=lambda *args:0
      if query["l2"][0]=="zh" and gradint.sanityCheck(query["l2w"][0],"zh"): gradint.justSynthesize += "#en Pinyin needs tones.  Please go back and add tone numbers." # speaking it because alert box might not work and we might be being called from HTML5 Audio stuff (TODO maybe duplicate sanityCheck in js, if so don't call HTML5 audio, then we can have an on-screen message here)
      else: gradint.justSynthesize += "#"+query["l2"][0].replace("#","").replace('"','')+" "+query["l2w"][0].replace("#","").replace('"','')
    if "l1w" in query and query["l1w"][0]: gradint.justSynthesize += "#"+query["l1"][0].replace("#","").replace('"','')+" "+query["l1w"][0].replace("#","").replace('"','')
    if gradint.justSynthesize=="0": return htmlOut('You must type a word in the box before pressing the Speak button.'+backLink) # TODO maybe add a Javascript test to the form also, IF can figure out if window.alert works
    serveAudio(stream = len(gradint.justSynthesize)>100, filetype=filetype)
  elif "add" in query:
    if "l2w" in query and query["l2w"][0] and "l1w" in query and query["l1w"][0]:
      gradint.startBrowser=lambda *args:0
      if query["l2"][0]=="zh": scmsg=gradint.sanityCheck(query["l2w"][0],"zh")
      else: scmsg=None
      if scmsg: htmlOut(scmsg+''+backLink)
      else: addWord(query["l1w"][0],query["l2w"][0],query["l1"][0],query["l2"][0])
    else: htmlOut('You must type words in both boxes before pressing the Add button.'+backLink) # TODO maybe add a Javascript test to the form also, IF can figure out a way to tell whether window.alert() works or not
  elif "clang" in query: # change languages
    dirID = setup_userID()
    if (gradint.firstLanguage,gradint.secondLanguage) == (query["l1"][0],query["l2"][0]) and not query["clang"][0]=="ignore-unchanged": return htmlOut('You must change the settings before pressing the Change Languages button.'+backLink) # (external scripts can set clang=ignore-unchanged)
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": query["l1"][0],"secondLanguage":query["l2"][0]})
    redirectHomeKeepCookie(dirID)
  elif "swaplang" in query: # change languages
    dirID = setup_userID()
    gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": gradint.secondLanguage,"secondLanguage":gradint.firstLanguage})
    redirectHomeKeepCookie(dirID)
  elif "editsave" in query:
    dirID = setup_userID()
    if "vocab" in query: vocab=query["vocab"][0]
    else: vocab="" # user blanked it
    open(gradint.vocabFile,"w").write(vocab)
    redirectHomeKeepCookie(dirID)
  elif "edit" in query:
    dirID = setup_userID()
    try: v=open(gradint.vocabFile).read()
    except: v="" # (shouldn't get here unless they hack URLs)
    htmlOut('<form action="gradint.cgi" method="post"><textarea name="vocab" style="width:100%;height:80%" rows="15" cols="50">'+v+'</textarea><br><input type=submit name=editsave value="Save changes"> | <input type=submit name=dummy value="Cancel"></form>')
  elif "lesson" in query:
    setup_userID()
    gradint.maxNewWords = int(query["new"][0]) # (shouldn't need sensible-range check here if got a dropdown; if they really want to hack the URL then ok...)
    gradint.maxLenOfLesson = int(float(query["mins"][0])*60)
    # TODO save those settings for next time also?
    serveAudio(stream = True, inURL = False, filetype=filetype)
  elif "voNormal" in query:
    setup_userID()
    gradint.voiceOption=""
    gradint.updateSettingsFile(gradint.settingsFile,{"voiceOption":""})
    listVocab(True)
  elif "vopt" in query:
    setup_userID()
    for v in gradint.guiVoiceOptions:
      if v.lower()=="-"+query["vopt"][0].lower():
        gradint.voiceOption = v
        gradint.updateSettingsFile(gradint.settingsFile,{"voiceOption":v})
        break
    listVocab(True)
  else: listVocab(has_userID())

def justSynth(text,lang="",filetype=""):
  if lang: lang = lang.replace("#","").replace('"','')+" "
  gradint.justSynthesize=lang+text.replace("#","").replace('"','')
  if not filetype in ["mp3","ogg","wav"]: filetype="mp3"
  serveAudio(stream = len(text)>80, filetype=filetype)

def justsynthLink(text,lang=""): # assumes written function h5a
  if lang in gradint.synth_partials_voices and gradint.guiVoiceOptions: cacheInfo="&curVopt="+gradint.voiceOption
  else: cacheInfo=""
  return '<A HREF="gradint.cgi?js='+urllib.quote_plus(text)+'&jsl='+urllib.quote_plus(lang)+cacheInfo+'" onClick="javascript:return h5a(this);">'+text+'</A>'
# TODO if h5a's canPlayType etc works, cld o/p a lesson as a JS web page that does its own 'take out of event stream' and 'progress write-back'.  wld need to code that HERE by inspecting the finished Lesson object, don't call play().

def htmlOut(body_u8):
    print "Content-type: text/html; charset=utf-8" ; print
    print '<html><head><title>Gradint Web edition</title>'
    print '<meta name="viewport" content="width=device-width">'
    print a</head><body>'+body_u8
    print '<HR>This is Gradint Web edition.  If you need recorded words or additional functions, please <A HREF="http://people.pwf.cam.ac.uk/ssb22/gradint/">download the full version of Gradint</A>.<p>'+program_name[:program_name.index("(")]+"using "+gradint.program_name[:gradint.program_name.index("(")]
    # TODO @ low-priority: Android 3 <input type="file" accept="audio/*;capture=microphone"></input>
    print "</body></html>"
backLink = ' <A HREF="gradint.cgi" onClick="javascript:history.go(-1);return false">Back</A>' # TODO may want to add a random= to the non-js HREF

def serveAudio(stream=0, filetype="mp3", inURL=1):
  # caller imports gradint (and sets justSynthesize or whatever) first
  if filetype=="mp3": print "Content-type: audio/mpeg"
  else: print "Content-type: audio/"+filetype # ok for ogg, wav?
  if inURL:
    print "Last-Modified: Sun, 06 Jul 2008 13:20:05 GMT"
    print "Expires: Wed, 1 Dec 2036 23:59:59 GMT"
  gradint.out_type = filetype
  def mainOrSynth():
    try: gradint.main()
    except SystemExit:
      if not gradint.justSynthesize:
        gradint.justSynthesize = "en Problem generating the lesson. Check we have prompts for those languages." ; gradint.main()
  if stream:
    print "Content-Disposition: attachment; filename=gradint.mp3" # helps with some browsers that can't really do streaming
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

def addWord(l1w,l2w,l1,l2):
    dirID=setup_userID()
    if not (gradint.firstLanguage,gradint.secondLanguage) == (l1,l2):
      if not ((gradint.firstLanguage,gradint.secondLanguage) == (l2,l1) and "HTTP_REFERER" in os.environ and not "gradint.cgi" in os.environ["HTTP_REFERER"]): gradint.updateSettingsFile(gradint.settingsFile,{"firstLanguage": l1,"secondLanguage":l2})
      gradint.firstLanguage,gradint.secondLanguage = l1,l2
    if (l1w+"_"+l1,l2w+"_"+l2) in map(lambda x:x[1:],gradint.parseSynthVocab(gradint.vocabFile,forGUI=1)): return htmlOut('This word is already in your list.'+backLink)
    gradint.appendVocabFileInRightLanguages().write(l2w+"="+l1w+"\n")
    if "HTTP_REFERER" in os.environ and not "gradint.cgi" in os.environ["HTTP_REFERER"]: extra="&dictionary="+urllib.quote(os.environ["HTTP_REFERER"])
    else: extra=""
    redirectHomeKeepCookie(dirID,extra)

def redirectHomeKeepCookie(dirID,extra=""):
    print "Location: gradint.cgi?random="+str(random.random())+"&id="+dirID[dirID.rindex("/")+1:]+extra ; print

def langSelect(name,curLang):
    curLang = gradint.espeak_language_aliases.get(curLang,curLang)
    return '<select name="'+name+'">'+''.join(['<option value="'+abbr+'"'+gradint.cond(abbr==curLang," selected","")+'>'+localise(abbr)+' ('+abbr+')'+'</option>' for abbr in sorted(lDic.keys())])+'</select>'

def numSelect(name,nums,curNum): return '<select name="'+name+'">'+''.join(['<option value="'+str(num)+'"'+gradint.cond(num==curNum," selected","")+'>'+str(num)+'</option>' for num in nums])+'</select>'

def localise(x):
    r=gradint.localise(x)
    if r==x: return lDic.get(gradint.espeak_language_aliases.get(x,x),x)
    else: return r.encode('utf-8')

def listVocab(hasList): # main screen
    firstLanguage,secondLanguage = gradint.firstLanguage, gradint.secondLanguage
    # TODO button onClick: careful of zh w/out tones, wld need to JS this
    body = """<script language="Javascript"><!--
function h5a(link) { if (document.createElement) {
   var ae = document.createElement('audio');
   if (ae.canPlayType && function(s){return s!="" && s!="no"}(ae.canPlayType('audio/mpeg'))) {
     if (link.href) ae.setAttribute('src', link.href);
     else ae.setAttribute('src', link);
     ae.play();
     return false; }"""
    if gradint.got_program("oggenc"): body += """else if (ae.canPlayType && function(s){return s!="" && s!="no"}(ae.canPlayType('audio/ogg'))) {
     if (link.href) ae.setAttribute('src', link.href+"&filetype=ogg");
     else ae.setAttribute('src', link+"&filetype=ogg");
     ae.play();
     return false; }"""
    body += """} return true; }
//--></script>"""
    body += '<center><form action="gradint.cgi">'
    gotVoiceOptions = (gradint.secondLanguage in gradint.synth_partials_voices or gradint.firstLanguage in gradint.synth_partials_voices) and gradint.guiVoiceOptions
    if gotVoiceOptions:
      body += 'Voice option: <input type=submit name=voNormal value="Normal"'+gradint.cond(gradint.voiceOption=="",' disabled="disabled"',"")+'>'
      for v in gradint.guiVoiceOptions: body += ' | <input type=submit name=vopt value="'+v[1].upper()+v[2:]+'"'+gradint.cond(gradint.voiceOption==v,' disabled="disabled"',"")+'>'
      body += '<input type=hidden name=curVopt value="'+gradint.voiceOption+'">' # ignored by gradint.cgi but needed by browser cache to ensuer 'change voice option and press Speak again' works
      body += '<br>'
    # must have autocomplete=off if capturing keycode 13
    if gotVoiceOptions: cacheInfo="&curVopt="+gradint.voiceOption
    else: cacheInfo=""
    body += (localise("Word in %s") % localise(secondLanguage))+': <input type=text name=l2w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].spk.click();return false} else return true"> <input type=submit name=spk value="'+localise("Speak")+'" onClick="javascript: if (!document.forms[0].l1w.value && !document.forms[0].l2w.value) return true; else return h5a(\'gradint.cgi?spk=1&l1w=\'+document.forms[0].l1w.value+\'&l2w=\'+document.forms[0].l2w.value+\'&l1=\'+document.forms[0].l1.value+\'&l2=\'+document.forms[0].l2.value+\''+cacheInfo+'\');"><br>'+(localise("Meaning in %s") % localise(firstLanguage))+': <input type=text name=l1w autocomplete=off onkeydown="if(event.keyCode==13) {document.forms[0].add.click();return false} else return true"> <input type=submit name=add value="'+(localise("Add to %s") % localise("vocab.txt").replace(".txt",""))+'"><script language="Javascript"><!--\nvar emptyString="";document.write(\' <input type=submit name=dummy value="'+localise("Clear input boxes")+'" onClick="javascript:document.forms[0].l1w.value=document.forms[0].l2w.value=emptyString;document.forms[0].l2w.focus();return false">\')\n//--></script><p>'+localise("Your first language")+': '+langSelect('l1',firstLanguage)+' '+localise("second")+': '+langSelect('l2',secondLanguage)+' <nobr><input type=submit name=clang value="'+localise("Change languages")+'"><input type=submit name=swaplang value="Swap"></nobr>'
    def htmlize(l,lang):
       if type(l)==type([]) or type(l)==type(()): return htmlize(l[-1],lang)
       if "!synth:" in l: return htmlize(l[l.index("!synth:")+7:l.rfind("_")],lang)
       return justsynthLink(l,lang)
    if hasList:
       gradint.availablePrompts = gradint.AvailablePrompts() # needed before ProgressDatabase()
       # gradint.cache_maintenance_mode=1 # don't transliterate on scan -> NO, including this scans promptsDirectory!
       gradint.ESpeakSynth.update_translit_cache=lambda *args:0 # do it this way instead
       data = gradint.ProgressDatabase().data ; data.reverse()
       if data: hasList = "<p><TABLE style=\"border: thin solid green\"><caption><nobr>Your word list</NOBR> <NOBR>(click for audio)</NOBR> <input type=submit name=edit value=\"Text edit \""+localise("vocab.txt").replace(".txt","")+"\"></caption><TR><TH>Repeats</TH><TH>"+localise(gradint.secondLanguage)+"</TH><TH>"+localise(gradint.firstLanguage)+"</TH></TR>"+"".join(["<TR><TD>%d</TD><TD>%s</TD><TD>%s</TD>" % (num,htmlize(dest,gradint.secondLanguage),htmlize(src,gradint.firstLanguage)) for num,src,dest in data])+"</TABLE>"
       else: hasList=""
    else: hasList=""
    if hasList: body += '<P><table style="border:thin solid blue"><tr><td>'+numSelect('new',range(2,10),gradint.maxNewWords)+' '+localise("new words in")+' '+numSelect('mins',[15,20,25,30],int(gradint.maxLenOfLesson/60))+' '+localise('mins')+' <input type=submit name=lesson value="'+localise("Start lesson")+'"></td></tr></table>'
    if "dictionary" in query: body += '<p><a href="'+query["dictionary"][0]+'">Back to dictionary</a>' # TODO check for cross-site scripting
    if not hasList: hasList="<P>Your word list is empty."
    body += hasList
    htmlOut(body+'</form></center><script name="Javascript"><!--\ndocument.forms[0].l2w.focus()\n//--></script>')

def has_userID():
    cookie_string = os.environ.get('HTTP_COOKIE',"")
    if cookie_string:
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        return 'id' in cookie

def setup_userID():
    # MUST call before outputting headers (may set cookie)
    # Use the return value of this with -settings.txt, -vocab.txt etc
    dirName = "cgi-gradint-users"
    if not os.path.exists(dirName): os.system("mkdir "+dirName)
    userID = None
    cookie_string = os.environ.get('HTTP_COOKIE',"")
    if cookie_string:
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        if 'id' in cookie: userID = cookie['id'].value.replace('"','').replace("'","").replace("\\","")
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
    return userID

main()

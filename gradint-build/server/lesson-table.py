#!/usr/bin/env python
# (compatible with both Python 2 and Python 3)

# Script to generate an HTML table of the contents of a lesson
# for summarizing it to a teacher or native speaker.
# Reads from progressFile and progressFileBackup.

# Version 1.06 (c) 2011, 2020-21 Silas S. Brown.  License: GPL

# Example use:
# export samples_url=http://example.org/path/to/samples/ # or omit
# python lesson-table.py [gradint-params] | ssh some-server 'mutt -e "set record = \"\";" -e "set charset=\"utf-8\"; set send_charset=\"utf-8\"; set content_type=\"text/html\";" to-address -s "Gradint report"' || echo Send failed

import gradint, os
samples_url = os.getenv("samples_url","")

from gradint import B,S
newpf = gradint.progressFile
gradint.progressFile = gradint.progressFileBackup
gradint.pickledProgressFile=None

mergeIn = gradint.scanSamples()+gradint.parseSynthVocab(gradint.vocabFile)

oldProg = gradint.ProgressDatabase(alsoScan=0)
oldProg.data += oldProg.unavail # because it might be available in newProg
gradint.mergeProgress(oldProg.data,mergeIn)
opd = {}
for tries,l1,l2 in oldProg.data:
  key = gradint.norm_filelist(l1,l2)
  if tries: opd[key]=tries
del oldProg
gradint.progressFile = newpf
newProg = gradint.ProgressDatabase(alsoScan=0)
gradint.mergeProgress(newProg.data,mergeIn)
del mergeIn
changes = [] ; count=0
gradint.sort(newProg.data,gradint.cmpfunc)
for tries,l1,l2 in newProg.data:
  if not tries: continue
  key = gradint.norm_filelist(l1,l2)
  oldTries = opd.get(key,0)
  if not oldTries==tries: changes.append((oldTries,count,tries-oldTries,S(l1),S(l2)))
  count += 1
del newProg,opd
changes.sort()
print ('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Gradint lesson report</title><meta name="mobileoptimized" content="0"><meta name="viewport" content="width=device-width"><script>if(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)document.write("<style>body { background-color: black; color: #c0c000; } a:link { color: #00b000; } a:visited { color: #00c0c0; } a:hover { color: red; }</style>");</script></head><body><h2>Gradint lesson report</h2>')
if gradint.unix and gradint.got_program("zgrep"):
  print (os.popen("zgrep '^# collection=' \"%s\"" % gradint.progressFile).read()[2:].rstrip())
print ('<table border><tr><th>Repeats before</th><th>Repeats today</th><th>Question</th><th>Answer</th></tr>') # (have Question/Answer order rather than Word/Meaning, because if it's L2-only poetry then the question is the previous line, which is not exactly "meaning")
  
had_h5a = False
def h5aCode(filename):
  r = real_h5aCode(filename)
  if r:
    global had_h5a
    if not had_h5a:
      had_h5a = True
      print ("""<script language="Javascript"><!--
function h5a(link,type) { if (document.createElement) {
   var ae = document.createElement('audio');
   if (ae.canPlayType && function(s){return s!="" && s!="no"}(ae.canPlayType(type))) {
     if (link.href) ae.setAttribute('src', link.href);
     else ae.setAttribute('src', link);
     ae.play();
     return false; } } return true; }
//--></script>""")
  return r
def real_h5aCode(filename):
  if filename.endswith(gradint.dotmp3): return ' onClick="javascript:return h5a(this,\'audio/mpeg\')"'
  elif filename.endswith(gradint.dotwav): return ' onClick="javascript:return h5a(this,\'audio/wav\')"'
  else: return ""

def wrappable(f):
  z = u'\u200b' # zero-width space
  if not type(u"")==type(""): z=z.encode('utf-8') # Py2
  return f.replace(os.sep,os.sep+z).replace('_',z+'_')
def checkVariant(l,ensureTxt=0):
  l=S(l)
  if os.sep in l: fname=l[l.rindex(os.sep)+1:]
  else: fname=l
  variants = map(S,gradint.variantFiles.get(B(gradint.samplesDirectory+os.sep+l),[fname]))
  if fname in variants: return l # ok
  # else no default variant, need to pick one for the link
  for v in variants:
    if ensureTxt:
      if not v.endswith(gradint.dottxt): continue
    elif v.endswith(gradint.dottxt): continue
    if not os.sep in l: return v
    return l[:l.rindex(os.sep)+1]+v
def link(l):
  if type(l)==type([]): return link(l[-1])
  l = S(l)
  if l.lower().endswith(gradint.dottxt): l="!synth:"+S(gradint.u8strip(gradint.read(gradint.samplesDirectory+os.sep+checkVariant(l,1)))).strip(gradint.wsp)+"_"+gradint.languageof(l)
  if "!synth:" in l:
    if gradint.languageof(l) not in [gradint.firstLanguage,gradint.secondLanguage]: l=S(gradint.textof(l))+" ("+gradint.languageof(l)+")"
    else: l=S(gradint.textof(l))
    return l.replace('&','&amp;').replace('<','&lt;')
  if samples_url: return '<A HREF="'+samples_url+checkVariant(l)+'"'+h5aCode(checkVariant(l))+'>'+wrappable(l)+'</A>'
  return wrappable(l).replace('&','&amp;').replace('<','&lt;')
for b4,pos,today,l1,l2 in changes: print ('<tr><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>' % (b4,today,link(l1),link(l2)))
print ('</table></body></html>')

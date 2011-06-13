#!/usr/bin/env python

# vocab2html.py - converts vocab.txt to HTML,
# linking any vocab that is cached
# (resulting html file should be put in synthCache directory for the links to work)
# HTML markup in the comments is OK,
# e.g. to comment out a section, # <!-- ... # -->

# you can run vocab2html.py with command-line arguments
# - these will be passed to gradint

# if you have set the environment variable ESPEAK_CGI_URL, this will
# be used.  E.g.: export ESPEAK_CGI_URL="/~userID/espeak.cgi"
# (TODO: this script ignores the possibility of synthesizing phrases from partials)

# Version 1.1, (c) Silas S. Brown, License: GPL

from gradint import *
if not synthCache: synthCache_contents = []
langs=[secondLanguage,firstLanguage]
o=open(vocabFile,"rU")
justHadP=1
print '<html><HEAD><META HTTP-EQUIV=Content-type CONTENT="text/html; charset=utf-8"><meta name="viewport" content="width=device-width"></HEAD><body>' # (assume utf8 in case there's any hanzi, but TODO what if using another charset for another language?)
for l in o.readlines():
  l2=l.lower()
  if l2.startswith("set language ") or l2.startswith("set languages "): langs=l.split()[2:]
  if not l.strip():
    # blank line
    if not justHadP: print "<P>"
    justHadP=1 ; continue
  if not justHadP: print "<BR>"
  if l2.startswith("set language ") or l2.startswith("set languages ") or l2.startswith("limit on") or l2.startswith("limit off") or l2.startswith("begin poetry") or l2.startswith("end poetry"):
    print "<EM>%s</EM>" % (l,)
  elif l2.startswith("#"):
    # comment (and may be part of multi-line comment)
    if not l[1:].strip().startswith("<!--"): print "<small>#</small> "
    print l[1:]
  else:
    # vocab line
    langsAndWords=zip(langs,map(lambda x:x.strip(),l.split("=")))
    out = []
    for lang,word in langsAndWords:
      fname=synthCache_transtbl.get(word.lower()+"_"+lang+dotwav,word.lower()+"_"+lang+dotwav)
      found = 0
      for fn2 in [fname,fname.replace(dotwav,dotmp3)]:
          if fn2 in synthCache_contents:
              out.append("<A HREF=\""+fn2+"\">"+word+"</A>")
              found = 1 ; break
      if not found:
          if os.getenv("ESPEAK_CGI_URL"):
              import urllib
              out.append("<A HREF=\""+os.getenv("ESPEAK_CGI_URL")+"?"+urllib.urlencode({"t":word,"l":lang})+"\">"+word+"</A>")
          else: out.append(word)
    print " = ".join(out)
  justHadP=0
print "</body></html>"

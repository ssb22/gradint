#!/usr/bin/env python

# espeak.cgi - a CGI script for the eSpeak speech synthesizer

# (c) 2008,2011 Silas S. Brown, License: GPL
version="1.123"

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# With most webservers you should be able to put this
# in your public_html and do chmod +x.  You will also need to
# install eSpeak on the system (if you can't do it system-wide
# then add code here to modify PATH and ESPEAK_DATA_PATH, e.g.
# import os ; os.environ["PATH"]="/my/espeak/path:"+os.environ["PATH"]
# )

import cgi, cgitb ; cgitb.enable()
f = cgi.FieldStorage()

default_language = "en"
stream_if_input_bigger_than = 100
max_input_size = 1000

minSpeed, defaultSpeed, maxSpeed, speedStep = 80,170,370,30 # (NB check defaultSpeed=minSpeed+integer*speedStep)

import os,commands,re,sys
if commands.getoutput("which espeak 2>/dev/null"): prog="espeak"
elif commands.getoutput("which speak 2>/dev/null"): prog="speak"
else: raise Exception("Cannot find espeak")

lang = f.getfirst("l",default_language)
if len(lang)>10 or not re.match("^[a-z0-9-+]*$",lang): lang=default_language

voiceDir=os.environ.get("ESPEAK_DATA_PATH","/usr/share/espeak-data")+"/voices"

variants = os.listdir(voiceDir+"/!v")
if "whisper" in variants and "wisper" in variants: variants.remove("wisper")
variants.sort() ; variants.insert(0,"default")
if "+" in lang:
    variant=lang[lang.index("+")+1:]
    lang=lang[:lang.index("+")]
else: variant = f.getfirst("v",variants[0])
if not variant in variants: variant=variants[0]

speed = f.getfirst("s",str(defaultSpeed))
try: speed=int(speed)
except: speed=defaultSpeed
if speed<minSpeed or speed>maxSpeed: speed=defaultSpeed

t = f.getfirst("t","")
if len(t)>max_input_size: t=""
else:
    try: t.decode('utf-8')
    except: t="" # not valid utf-8
    if chr(0) in t: t="" # just in case

if len(t)>stream_if_input_bigger_than:
    # streaming - will need sox to convert
    if not commands.getoutput("which sox 2>/dev/null"): raise Exception("Cannot find sox")
    fname=None
else:
    # not streaming (so can fill in length etc) - will need a writable file in a private tmp directory, preferably in memory
    worked = 0
    for tmp in ["/dev/shm/",os.getenv("TMPDIR"),"/tmp/",""]:
        fname = tmp + "espeak-cgi." + str(os.getpid())
        try:
            os.mkdir(fname)
            worked = 1 ; break
        except: pass # INCLUDING if already exists - avoid symlink attacks
    if not worked: raise Exception("Can't find anywhere to put temp file")
    fname2=fname+"/"+str(os.getpid())+".wav"
    open(fname2,"w") # raising exception if it's unwritable (try changing to a suitable directory)

# in case espeak can't find a utf-8 locale
loc=commands.getoutput("locale -a|grep -i 'utf-*8$'|head -1").strip()
if loc: os.environ["LC_CTYPE"]=loc

def getName(f):
    o=open(f)
    line=""
    for t in range(10):
        line=o.readline()
        if "name" in line: return line.split()[1]
    return f[f.rindex("/")+1:] # assumes it'll be a full pathname
def isDirectory(directory):
    oldDir = os.getcwd()
    try:
        os.chdir(directory)
        ret = 1
    except: ret = 0 # was except OSError but some Python ports have been known to throw other things
    os.chdir(oldDir)
    return ret

if t and f.getfirst("qx",""):
    sys.stdout.write("Content-Type: text/plain; charset=utf-8\n\n")
    sys.stdout.flush() # help mathopd
    os.popen(prog+" -v "+lang+" -q -X -m 2>/dev/null","wb").write(t)
elif t:
    prog_with_params = prog+" -v "+lang+"+"+variant+" -s "+str(speed)+" -m"
    # TODO -p 0-99 default 50 (pitch adjustment)
    # TODO -g wordgap * 10mS
    if len(t)>stream_if_input_bigger_than:
        sys.stdout.write("Content-Type: audio/basic\nContent-Disposition: attachment; filename=\""+t+"_"+lang+".au\"\n\n") # using .au instead of .wav because Windows Media Player doesn't like incorrect length fields in wav.  And make sure it's attachment otherwise Mac OS QuickTime etc can have problems when server is slow
        # problem is, WILL NEED CONVERTING for gradint (unless want to use "sox" on the Windows version before playing via winsound) (but the espeak no-length wav files will probably be wrong on that anyway).  Should be OK because we're doing this only in the case of len(t)>stream_if_input_bigger_than.
        sys.stdout.flush() # help mathopd
        os.popen(prog_with_params+" --stdout 2>/dev/null | sox -t wav - -t au - 2>/dev/null","wb").write(t)
    else:
        os.popen(prog_with_params+" -w "+fname2+" 2>/dev/null","wb").write(t)
        sys.stdout.write("Content-Type: audio/wav\nContent-Disposition: attachment; filename=\""+t+"_"+lang+".wav\"\n\n")
        sys.stdout.write(open(fname2,"rb").read())
else:
    sys.stdout.write('Content-Type: text/html; charset=utf-8\n\n<HTML><head><meta name="viewport" content="width=device-width"></head><BODY>') # (specify utf-8 here in case accept-charset is not recognised, e.g. some versions of IE6)
    banner = commands.getoutput(prog+" --help|head -3").strip()
    sys.stdout.write("This is espeak.cgi version "+version+", using <A HREF=http://espeak.sourceforge.net/>eSpeak</A> "+" ".join(banner.split()[1:]))
    if not loc: sys.stdout.write("<br>Warning: could not find a UTF-8 locale; espeak may malfunction on some languages")
    warnings=commands.getoutput(prog+" -q -x .").strip() # make sure any warnings about locales are output
    if warnings: sys.stdout.write("<br>"+warnings)
    sys.stdout.write("<FORM method=post accept-charset=UTF-8>Text or SSML: <INPUT TYPE=text NAME=t STYLE='width:80%'><br>Language: <SELECT NAME=l>")
    ld=os.listdir(voiceDir)
    directories = {}
    for f in ld[:]:
        if f in ["!v","default","mb"]: ld.remove(f)
        elif isDirectory(voiceDir+"/"+f):
            ld.remove(f)
            for f2 in os.listdir(voiceDir+"/"+f):
                ld.append(f2)
                directories[f2]=f
    ld.sort()
    for f in ld:
        sys.stdout.write("<OPTION VALUE="+f)
        if f==lang: sys.stdout.write(" SELECTED")
        if f in directories: name=getName(voiceDir+"/"+directories[f]+"/"+f)
        else: name=getName(voiceDir+"/"+f)
        sys.stdout.write(">"+f+" ("+name+")</OPTION>")
    sys.stdout.write("</SELECT> Voice: <SELECT NAME=v>")
    for v in variants:
        if v=="default": name="default"
        else: name=getName(voiceDir+"/!v/"+v)
        sys.stdout.write("<OPTION VALUE="+v)
        if v==variant: sys.stdout.write(" SELECTED")
        sys.stdout.write(">"+name+"</OPTION>")
    sys.stdout.write("</SELECT> Speed: <SELECT NAME=s>")
    for ss in range(minSpeed,maxSpeed,speedStep)+[maxSpeed]:
        sys.stdout.write("<OPTION VALUE="+str(ss))
        if ss==speed: sys.stdout.write(" SELECTED")
        sys.stdout.write(">"+str(ss)+"</OPTION>")
    sys.stdout.write("</SELECT> <INPUT TYPE=submit NAME=qx VALUE=\"View phonemes\"><center><big><INPUT TYPE=submit VALUE=SPEAK></big></center></FORM></BODY></HTML>")
if fname: os.system("rm -rf \""+fname+"\"") # clean up temp dir

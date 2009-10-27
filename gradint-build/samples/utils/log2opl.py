# log2opl.py (c) 2008 Silas S. Brown.  License: GPL.
# This is a Python script to translate log.txt into an OPL
# program for a palmtop or smartphone running EPOC.  The
# resulting file lesson.opl needs to be imported into Program
# and translated.  The program will show the log of the lesson
# in real time, providing a countdown for each item.  This
# is for use as a speaker's cue when demonstrating the
# graduated-interval method in an extemporaneous talk (works
# best with a lesson 1 so there are plenty of gaps to speak in).
# Make sure you're using vocab.txt or meaningful filenames.
# It may also be useful to set partialsDirectory=None

# If you have a PDA that can run Gradint by itself, then
# see ask_teacherMode in advanced.txt for a more flexible approach.

o=open("lesson.opl","wb")
o.write("PROC m:\r\nfont 8,9\r\n")
curS = -5 # allow lead-in
for l in open("log.txt"):
  m,s = l.split()[0].split(":") ; m,s = int(m),int(s)
  s=s+60*m
  o.write("a:("+str(s-curS)+",\""+" ".join(l.split()[1:])+"\")\r\n")
  curS = s

o.write('PRINT "Finished.":GET\r\nENDP\r\nPROC a:(secs%,a$)\r\nLOCAL i%\r\nPRINT "   ";a$+chr$(13),\r\ni%=secs%\r\nWHILE i%\r\nprint CHR$(13)+GEN$(i%,2)+" ";\r\nPAUSE 20\r\ni%=i%-1\r\nENDWH\r\nPRINT CHR$(13)+" "\r\nENDP\r\n')

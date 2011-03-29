# safety-check-progressfile.py:
# The purpose of this script is to check
# progress.txt for safety.  Because it's
# possible to embed any Python command in
# progress.txt, in some situations you may want
# to make sure an untrusted progress.txt doesn't
# contain OS commands or the like.  To do this,
# run this script and check for error exit.

# The script works by running progress.txt in an
# environment with no modules loaded and no
# builtin functions available.  Additionally,
# search/replace operations are performed that
# will break code using various keywords etc.
# Since this includes "try"/"except", the
# resulting code cannot catch any errors it
# raises.  Attempts to do anything other than
# setting variables (and variables that don't
# have keywords etc in their names at that)
# should result in a harmless crash when run
# with this script.

# Note that it may still be possible for the
# code to set some of Gradint's variables to
# values that will crash Gradint.  But at least
# it shouldn't be able to delete files etc.

# Note also that you must make sure progress.txt
# cannot be changed between being validated by
# this script and being used by Gradint.

from gradint import ProgressDatabase, progressFile
from os import popen
try: f=popen("gzip -fdc \""+progressFile+"\"").read()
except: f=""
if not f: f=open(progressFile).read()
for wordToBreak in "try import def lambda if break continue class yield del exec while".split()+dir("__builtins__"): f=f.replace(wordToBreak," 0=0 ")
ProgressDatabase(0,f)

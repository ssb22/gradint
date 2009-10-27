Utilities
---------

The programs in this directory are small utililies that can
make it easier to work with gradint.

Most require sox (download from sox.sourceforge.net).
In Windows, put sox.exe in the same directory or in
C:\Windows\system32 or somewhere.

All require Python (from www.python.org).  All systems
except Windows have that anyway if you can run gradint.

SPLITTING SOUND FILES
---------------------

splitter.py - lets you split a long recording into
individual files while you listen to the recording.  Needs
fast reaction times.  Works best with recordings that are
not TOO big (max 5 to 10 minutes at a time).

autosplit.py - splits a long recording into individual files
completely automatically, but only if the recording has been
made in near-broadcasting-studio conditions.

strip0.py - strips absolute silence off the beginning and
end of audio files (only useful if you're dealing with files
from a textbook CD or something)

manual-splitter.py (Unix only but not too difficult to
modify for other systems) - a helper script so that you can
use Audacity (or another sound editor) to split the file.
Use the "export selection as wav" command (you can assign a
hot-key to it), and you don't have to type in a different
filename each time because this script can run in the
background renaming the file every time you export it.
Useful if the recording is so messy that nothing else works.

OTHER PROCESSING
----------------

equalise.py - adjusts the volume of all files to a similar
level (usually increasing it also).  Use this if the volume
of your recordings varies too much.

filemove.sh - a Unix script that can help you to re-organise
your directories while automatically reflecting those
changes in the gradint progress database, so the
re-organisation does not interfere with your progress so far

make-smaller - some brief notes on what to do in Unix if you
find that your collection of words is taking up too much
hard disk space (or too much space on the backup device)

email-lesson* - scripts that can help you to
automatically distribute daily lessons to students
using a web server with reminder emails

cache-synth.py and cleanup-cache.py - cache all words that
can be synthesized, and cleanup the cache (if you later
remove some words from the vocabulary).  Useful if you have
a synthesizer that cannot be installed on all the systems
you run your gradint on.

list-synth.py and list2cache.py - aids in adding words from
online synthesizers (or real people) to the synth cache

vocab2html.py - make an HTML index for the synth
cache, with the help of vocab.txt
(you can also use it with espeak.cgi)

transliterate.py - make a transliterated vocab report
(for use with grep or on PDAs or whatever)

diagram.py - make a diagram of a gradint lesson

log2opl.py - translate a lesson to speaker's notes on EPOC PDA

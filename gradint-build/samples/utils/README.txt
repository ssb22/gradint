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

autosplit.py - splits a long recording into individual files
completely automatically, but only if the recording has been
made in near-broadcasting-studio conditions.

manual-splitter.py (Unix only but not too difficult to
modify for other systems) - a helper script so that you can
use Audacity (or another sound editor) to split the file
in non-realtime.  (Realtime splitting can be done in Gradint.)
Use the "export selection as wav" command (you can assign a
hot-key to it), and you don't have to type in a different
filename each time because this script can run in the
background renaming the file every time you export it.
Useful if the recording is so messy that nothing else works.

OTHER PROCESSING
----------------

filemove.sh - a Unix script that can help you to re-organise
your directories while automatically reflecting those
changes in the gradint progress database, so the
re-organisation does not interfere with your progress so far

cache-synth.py and cleanup-cache.py - cache all words that
can be synthesized, and cleanup the cache (if you later
remove some words from the vocabulary).  Useful if you have
a synthesizer that cannot be installed on all the systems
you run your gradint on.

list-synth.py and list2cache.py - aids in adding words from
online synthesizers (or real people) to the synth cache

transliterate.py - make a transliterated vocab report
(for use with grep or on PDAs or whatever)

diagram.py - make a diagram of a gradint lesson

trace.py - make a raytraced animation of a lesson

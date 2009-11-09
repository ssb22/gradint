SAMPLES DIRECTORY
-----------------

This directory should contain any recorded words and phrases
you want to learn.  They can be WAV or MP3, and should be
named 'name_en.wav' and 'name_la.wav' (or .mp3), where
'en' and 'la' are the abbreviations you are using for the
languages (e.g. en=English, la=Latvian, zh=Zhongwen, etc)
and 'name' is any name you like but must be consistent
across abbreviations.  The abbreviations must be the same as
the ones that are used in settings.txt (and advanced.txt).
(RISC OS users should replace '.' with '/'.)

If you don't already have a tool for recording and editing
sound files, try Audacity at http://audacity.sourceforge.net/
- look for its "export selection as WAV" function.

If you want to keep your recordings as MP3 files instead of
WAV files, you MUST read the section "IMPORTANT NOTES ABOUT MP3"
at the bottom of this document, to get it to work properly.
You still need to split them up into words or phrases.

Every word or phrase must have a first-language version and
a foreign-language version (but see later in this file if
you want to use foreign-language prompts or if you are
learning a text).

Do not place more than 1 word or phrase in each file.  If
you have a long recording containing many words and phrases,
look in the 'utils' directory for some scripts that can help
you to divide your recording into individual files.  See the
file README.txt in the 'utils' directory for details.

You can put your recordings into subdirectories as deep as
you like.  The order in which they are introduced in the
course reflects the order in which the directories appear
(so you can choose names accordingly).  If you also have
words in vocab.txt then they will normally take priority
over the samples directory; if you need some samples to
take priority over vocab.txt then put them in a subdirectory
with a name that starts with 00000, or with a character that
comes before 0 in the ASCII set, such as # ( ) , .

If you need to re-organise your subdirectories after you've
started the course, or if you need to reduce the amount of
disk space taken up by the files, see the file README.txt in
the 'utils' directory.

LEARNING A TEXT:

If a file called !poetry or !poetry.txt is present in a directory, the
program will assume that all the samples in the directory
are part of a poem or other text that is to be memorised in
sequence (the sequence is given by the ordering of the
filenames).  In this case, first-language versions of each
line are optional (but still desirable).  If several
consecutive samples are very long then this may cause
scheduling problems.

FOREIGN LANGUAGE PROMPTS:

You may wish to have both the prompts and the words in your
foreign language, using words you already know to explain
words you don't know.  If this is the case, you can add the
text "-meaning" to the filename of the prompt, i.e.
someWord-meaning_zh.wav  and  someWord_zh.wav
gradint will then behave as though the -meaning file is in
your first language.

Doing it this way will prevent gradint from behaving
incorrectly when you swap the first and second languages
(for example in a language exchange your partner probably
won't want to learn your second-language prompts).  It is
essential when using speech synthesis (see instructions in
vocab.txt) as the language in the filename must then be
correct to ensure correct choice of synthesizer.

VERBAL ANNOTATIONS:

If there is a file called _intro_en.wav in a directory, then
that file will be played before anything else in that
directory is introduced.  (Replace "en" with your first
language.)  You can use this for annotating parts of your
sample collection (i.e. "The words you are about to learn
are taken from ..." messages).

You can also introduce individual words, by recording the
introduction into a file called
<word>_<second-language>_explain_<first-language>.wav
for example myword_zh_explain_en.wav
This will be played when that word is introduced.

BORING WORDS:

If a file called !limit or !limit.txt is present in a directory, the
program will try to limit how many new words it introduces
from that directory in any one lesson.  Useful for "boring"
directories where you don't want to spend weeks on end
taking all your new words from there before moving to other
directories.

TEMPORARILY DISABLING PARTS OF THE COLLECTION:

If you add _disabled to a directory name, gradint will not
look in that directory.  Can be useful for temporarily
disabling parts of your collection.

COMBINING RECORDED AND SYNTHESIZED WORDS:

If you have recordings in one language and you want the
equivalents in another language to be synthesized by
computer, see the instructions in vocab.txt.

VARIANTS:

If a file called !variants or !variants.txt exists
then samples are interpreted as word_language_variant.wav
for example word_en_speaker1.wav and if there are
several variants of a word they will be chosen from at random.
(This is on by default in the prompts directory.)

IMPORTANT NOTES ABOUT MP3
-------------------------

You can put MP3 files in the prompts and samples directories,
and in the synth cache.  HOWEVER: In order to schedule a lesson,
Gradint must be able to work out the duration of each MP3
file, and Gradint's code to do this is rather basic and gets
VBR files all wrong.  I suggest encoding at CBR 48-kbit
(should be adequate for speech if the encoder is good).
If you're using Lame, try these parameters: --cbr -b 48 -h -m m

Non-Windows users, please also read the notes below:

MAC OS: Mac OS gradint can play MP3s IN REAL TIME ONLY
without assistance, but if you want to output to a file then
you'll need to obtain madplay (as a command), or a version of
sox that has been compiled with MP3 support.

LINUX / UNIX / CYGWIN : You need to obtain either madplay or
a version of sox that has been compiled with MP3 support.
(For Cygwin, the madplay.exe in the Windows gradint will
work if you put it somewhere in the PATH.  Most Linux
distributions have a madplay package and/or a sox package
that understands MP3s.)

RISC OS: You need to obtain a version of sox that has been
compiled with MP3 support.

If you create .SH files to be run remotely, then the remote
sox doesn't have to have mp3 support, but you'll still need
the appropriate capability on the system where gradint is running.

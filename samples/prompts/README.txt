PROMPTS DIRECTORY
-----------------

This directory should contain recorded prompts like "say
again" and "now please say", ideally in all the languages
you want to learn as well as your first language.  Gradint
will try to gradually introduce foreign-language prompts
over time and eventually drop the first-language prompts
altogether, but it can do this only if appropriate prompts
are available.

Prompts should be named like this: sayAgain_en.wav

where sayAgain is the name of the prompt (see below) and en
is the abbreviation of the language of the prompt.

You can also use .mp3 format, but see the section "IMPORTANT
NOTES ABOUT MP3" in the samples directory's README file.

You can also have prompts like sayAgain_en.txt (a text file)
if you want it to be spoken by a speech synthesizer.  (But
see vocab.txt for notes on getting synthesizers set up if
you have not already done so.)

Names can be anything, but there are some special ones:

whatmean and meaningis - used in "what does that mean?" and
"it means" tests

repeatAfterMe - used when a word is first introduced

sayAgain - used the second time a word is introduced

longpause - used when there is a long pause in the first
lesson (can explain to new users that the pause is OK and
will go away in future lessons as more revision is available)

begin - used when learning poetry and other long texts, to
indicate that the beginning of the text is asked for

end - used at the end of the lesson

whatSay - any prompts called whatSay will be placed AFTER
the word instead of before it (this is a hack)

You can have multiple versions of a prompt if you want.  To
do this, name them thus: name_en_1.wav name_en_2.wav etc
(anything can be used after the second _, not just a number)

If you are learning several languages then you also need
prompts to identify the names of the languages.  See the
file 'advanced.txt' for details.

If you want to make your samples quieter to match the lower
volume of PythonS60's audio.say() command, you can do this
on Unix (it doesn't matter if this command is repeated) :

find synth-cache samples -name '*.mp3' -exec mp3gain -a -m -12 '{}' ';'

and for any partials voices (Yali etc) using audiodata.dat
(see advanced.txt) you can do something like this (once only) :

grep -a '^[0-9]\+ .*\.raw$' audiodata.dat > /tmp/audiodata.dat &&
grep -av '^[0-9]\+ .*\.raw$' audiodata.dat | sox -t raw -r 44100 -c 1 -s -2 - -t raw - vol 0.2 >> /tmp/audiodata.dat
ls -l audiodata.dat /tmp/audiodata.dat # check they're the same length
cp /tmp/audiodata.dat .

S60's English synth isn't always clear.  To help, the text
is also displayed on screen, but it's not very big.  If you
need to run Gradint without looking, it might be better if
you can generate the lessons on another machine (with a
clearer English synth), or pre-cache the English.

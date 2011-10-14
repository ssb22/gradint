There's an article explaining how to set up the Android emulator at
http://www.linuxjournal.com/article/10940

The Gradint files go into the device's sl4a/scripts directory.
On the emulator, you can use e.g.:
  platform-tools/adb push ~/gradint/gradint.py /sdcard/sl4a/scripts
  platform-tools/adb push ~/gradint/samples /sdcard/sl4a/scripts/samples
(the linuxjournal article said tools/ instead of platform-tools/
  - may depend on which version you have)
Does not work with very large files, so for partials do not use audiodata.dat
(use the individual syllable files instead)

TO-DO: Try making a .apk file using the instructions at
http://code.google.com/p/android-scripting/wiki/SharingScripts
  but this would complicate the process of releasing new Gradint versions

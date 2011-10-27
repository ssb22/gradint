There's an article explaining how to set up the Android emulator at
http://www.linuxjournal.com/article/10940
(on a real phone, need to go to Application settings and enable Unknown sources)

The Gradint files go into the device's sl4a/scripts directory.
On the emulator, you can use e.g.:
  platform-tools/adb push ~/gradint/gradint.py /sdcard/sl4a/scripts
  platform-tools/adb push ~/gradint/samples /sdcard/sl4a/scripts/samples
(the linuxjournal article said tools/ instead of platform-tools/
  - may depend on which version you have)
Does not work with very large files, so for partials do not use audiodata.dat
(use the individual syllable files instead)

------- Making Gradint into a self-contained .apk file -------

This might not work (the device might fail to accept the resulting .apk file)
so this is only for reference.  Requires an Android SDK installation.

cd /tmp
wget http://android-scripting.googlecode.com/hg/android/script_for_android_template.zip
wget http://people.pwf.cam.ac.uk/ssb22/gradint/gradint-android.zip
mkdir android
cd android
unzip ../gradint-android.zip
cd ..
mkdir apk
cd apk
unzip ../script_for_android_template.zip
export ANDROID_SDK=~/android-sdk-linux_x86/  # or wherever
sh configure_package.sh org.ucam.ssb22.gradint
leafpad build.xml # change project name to "Gradint"
mv ../android/gradint.py res/raw/script.py 
mv ../android/advanced.txt ../android/settings.txt ../android/samples ../android/vocab.txt res/raw/
ant debug
# now copy bin/Gradint-debug.apk to the device

# This file is part of the source code of Gradint
# (c) Silas S. Brown.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Stuff in Extra_Data does not have to be present,
# but if present will be included in all versions.
# Use this for bundling Gradint with partials-synths,
# preset-collections, encoders, whatever, into one
# installer for giving to someone.  Note that you can
# support both Windows and Linux using a single bundle
# with win2linux.sh (see comments at top of that script)
Extra_Data=partials *_disabled [^g]*.exe

All_Versions=gradint-build.7z gradint.exe gradint.tbz gradint.bgz gradint.zip gradintcab.zip gradint-S60.zip gradint-android.zip servertools.bgz
# dropping gradint-noGUI.exe and GUI.exe for now - probably don't need that separation anymore

SHELL=/bin/bash

EData := $(shell for N in $(Extra_Data); do if [ -e $$N ]; then echo $$N; fi; done)

Common_Files=vocab.txt settings.txt advanced.txt samples $(EData)
Most_Mac_Files=$(Common_Files) gradint.py
Mac_Files=$(Most_Mac_Files) mac/start-gradint.app
Linux_Files=$(Common_Files) gradint.py INSTALL.txt
Riscos_Files=$(Common_Files) gradint.py

CODE=src/lessonplan.py src/sequence.py src/loop.py src/booktime.py src/play.py src/synth.py src/makeevent.py src/filescan.py src/recording.py src/users.py
TOP=src/top.py
SETUP=src/defaults.py src/system.py
ENDING=src/frontend.py
SOURCES=$(SETUP) $(CODE) $(ENDING)

gradint.py: $(SOURCES) cleanup
	chmod +w gradint.py 2>/dev/null || true
	(cat $(TOP);for N in $(SOURCES); do awk 'BEGIN {p=1} /^# This file is part of the source code of Gradint/ {p=0} /^$$/ {p=1} // {if(p) print}' < $$N; done) > gradint.py
	chmod a-w gradint.py
	chmod +x gradint.py
	python2 -c "import gradint" && rm -f gradint.pyc # just to make sure it compiles in Python 2
	python3 -c "import gradint" && rm -f gradint.pyc # just to make sure it compiles in Python 3 as well

# Do NOT run with "make -j" or other parallelisations - some of these rules have conflicting tempfiles
.NOTPARALLEL:

src/defaults.py: settings.txt advanced.txt Makefile
	echo "# This is the start of defaults.py - configuration defaults, automatically extracted from default settings.txt and advanced.txt, so user customisations don't have to be complete (helps with upgrades)" > src/defaults.py
	cat settings.txt advanced.txt|grep -v "^#"|sed -e 's/  *# .*//'|grep '[^ ]' >> src/defaults.py

gradint.exe: $(Common_Files) gradint.py
	rm -rf windows0 ; cp -r windows windows0
	cd windows0 && 7za x gradint.7z && rm gradint.7z && cd ..
	cd windows0/gradint && 7za x ../espeak-windows.7z -aoa && rm ../espeak-windows.7z && cd ../.. # bundled copy of eSpeak that unpacks in espeak/
	cd windows0 && 7za x ../windowsGUI/gradint.7z -aoa && cd ..
	cp -r $(Common_Files) windows0/gradint/
	mv windows0/gradint/samples/utils "windows0/gradint/samples/advanced utilities"
	for N in hanzi-prompts/*.txt; do python2 -c "open('windows0/gradint/samples/prompts/$$(echo $$N|sed -e s,.*/,,)','w').write('\\xef\\xbb\\xbf'+open('$$N').read())"; done # overwriting the pinyin ones (as will bundle espeak so can translit.)
	zip -0 windows0/gradint/library.zip gradint.py # (important to have no compression)
	for N in windows0/gradint/*.txt windows0/gradint/*/*.txt windows0/gradint/*/*.txt windows0/*.bat windows0/*/*.bat windows0/7zip.conf; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	# add a utf-8 BOM to start of vocab.txt, to ensure Notepad saves it in utf-8
	cd windows0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("vocab.txt").read())' && mv v2 vocab.txt && cd ../..
	cd windows0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("advanced.txt").read())' && mv v2 advanced.txt && cd ../..
	# can trim down the shortcuts, as the GUI now gives access to them
	cd windows0/shortcuts; rm "advanced setup.bat" "advanced utilities.bat" "General setup.bat" "Prompts.bat" "Recorded words.bat" "Synthesized words.bat" ; mv "Main program.bat" Gradint.bat ; cd ../..
	# shortcuts: Don't use .lnk files, they are far too horrible (even if you put %HOMEDRIVE%%HOMEPATH% in the shortcut, it still stores the original location, and you can't reliably create them on the client without delving rediculously deep into Windows programming).  Perhaps could use .url files, but we just use small batch files.  Prepend a common header to each one.  (NB it won't work to try to force the sort order by calling things _uninstall, ~uninstall, etc, unless you want Z_uninstall, Z_advanced etc)
	cd windows0/shortcuts ; mv header.bat bat_header ; for N in *.bat ../startup/*.bat; do if ! test "$$N" == uninstall.bat; then cat bat_header "$$N" > n ; mv n "$$N"; fi; done ; rm bat_header ; cd ../..
	# now run 7zip (look in a few extra places for it, and give it its full path in argv[0])
	cd windows0 ; 7za a data.7z setup.bat gradint shortcuts startup ; cd ..
	cat windows0/7zS.sfx windows0/7zip.conf windows0/data.7z > gradint.exe
	rm -rf windows0

# recorder.exe utility for sending to native friends to ask them to record words
# e.g. make recorder.exe RecorderL1=ja  if their language is different from zh
RecorderL1=zh
RecorderL2=en
recorder.exe: $(Common_Files) gradint.py
	rm -rf windows0 ; cp -r windows windows0
	cd windows0 && 7za x gradint.7z && rm gradint.7z && cd ..
	rm windows0/espeak-windows.7z
	cd windows0 && 7za x ../windowsGUI/gradint.7z && cd ..
	cp -r $(Common_Files) windows0/gradint/
	rm -rf windows0/gradint/samples/utils windows0/gradint/samples/prompts windows0/gradint/samples/README.txt
	rm -f windows0/gradint/madplay.exe windows0/gradint/sox.exe windows0/gradint/ptts.exe
	zip -0 windows0/gradint/library.zip gradint.py
	cp extras/zip.exe windows0/gradint/ # 2017-05: moved lame.exe from extras/ to windows/gradint.7z as patents have expired
	mv windows0/gradint windows0/recorder
	echo $$'@echo off\ncd recorder\ngradint-wrapper.exe recorderMode=1\nif not exist ..\\recorder.bat copy runme.bat ..\\recorder.bat\nif exist ..\\recorder.exe del ..\\recorder.exe\nexit' > windows0/recorder/runme.bat
	# (replace the .exe with a .bat in case they try to open it again from desktop and get confused by unzip's "overwrite" prompt)
	# (NB must say 'start' below for the above del to work)
	echo 'firstLanguage="$(RecorderL1)";secondLanguage="$(RecorderL2)"' > windows0/recorder/settings.txt
	for N in windows0/recorder/*.bat windows0/recorder/*.txt; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	cd windows0; 7za a recorder.zip recorder/ ; cd ..
	echo '$$AUTORUN$$>start /min recorder\runme.bat' | zip -z windows0/recorder.zip
	cat yali-voice/unzipsfx.exe windows0/recorder.zip > recorder.exe
	zip -A recorder.exe
	rm -rf windows0

gradint.cab: $(Common_Files) gradint.py
	rm -rf PocketPC0 ; cp -r PocketPC PocketPC0
	cd PocketPC0 && 7za x espeak.7z && 7za x tkinter.7z && rm espeak.7z tkinter.7z pocketpc-cab && cd ..
	cp -r $(Common_Files) PocketPC0/gradint
	cd PocketPC0/gradint && python ../../thindown.py wince < ../../gradint.py > gradint.py && cd ../..
	# if using partials, must combine them for CAB:
	for Dir in PocketPC0/gradint/partials/*/*; do if cd $$Dir; then if wc -c *.raw | grep -v total$$ | sed -e 's/^ *//' > audiodata.dat ; then cat *.raw >> audiodata.dat ; rm *.raw; else rm -f audiodata.dat; fi; cd ../../../../..; else true; fi; done
	chmod +w PocketPC0/gradint/gradint.py # saves problems with pocketpc-cab
	rm -rf PocketPC0/gradint/samples/utils # no point having those on Windows Mobile
	for N in PocketPC0/gradint/*.txt; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	cd PocketPC0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("vocab.txt").read())' && mv v2 vocab.txt && cd ../..
	cd PocketPC0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("advanced.txt").read())' && mv v2 advanced.txt && cd ../..
	# PocketPC/espeak-data contains the altered phon* files in case the eSpeak version is slightly different, but we should be able to re-use the dictionaries etc
	7za x windows/espeak-windows.7z && mv PocketPC0/espeak-data/* espeak/espeak-data && rmdir PocketPC0/espeak-data && mv espeak/espeak-data PocketPC0 && rm -rf espeak PocketPC0/espeak-data/mbrola*
	# Problem: we MUST have everything in ONE directory if it is to go on the storage card, otherwise it will go on the internal disk (which is a shame because the uninstall won't track where we really put things) (and no putting a file at top-level of device does not work)
	cd PocketPC0 && mv bin Progra* espeak-data gradint && cd ..
	# compile PocketPC espeak:
	# (if compiling 1.04.03 remember the changes posted to espeak-general 2010-09-13)
	# make speak CXX=arm-wince-pe-g++ USE_AUDIO="-DNEED_GETOPT -DNEED_WCHAR_FUNCTIONS -DWINCE" LIB_AUDIO=
	# python2 -c 'd=open("speak","rb").read().replace("/temp/wcetrace.log","/notexist/tracelog") ; open("speak","wb").write(d)'
	# then add to PocketPC/espeak.7z in bin/
	cd PocketPC0 && find . -type f | sort -f | grep -v /mb | grep -v /files.list | sed -e 's,./\(.*\)$$,\1 /\1,' -e 's,/\([^/]*\)/\([^/]*\)$$,/\1,' -e 's, /[^/]*.py$$, /,' -e 's/Program Files/Program~Files/g' > files.list && cd ..
	cd PocketPC0 && export PATH="/other/downloads/7zip/bin/:$$HOME/bin/p7zip-for-gradint:$$PATH" && ../PocketPC/pocketpc-cab -p "" -a "Gradint $$(head gradint/gradint.py | grep program_name | sed -e 's/.*t v/v/' -e 's/(c).*//')" files.list ../gradint.cab && cd ..
	# (need pocketpc-cab and lcab binaries for that to work)
	[ -e gradint.cab ] # pocketpc-cab can fail silently if we add too many files, so check the output exists
	rm -rf PocketPC0

gradint-S60.zip: $(Common_Files) gradint.py README-S60.txt
	cp S60.zip gradint-S60.zip
	7za a gradint-S60.zip $(Common_Files) README-S60.txt
	zip -d gradint-S60.zip 'samples/utils*' # no point having those on S60
	mkdir gradint
	cd gradint && python ../thindown.py s60 < ../gradint.py > gradint.py && 7za a ../gradint-S60.zip gradint.py && cd ..
	rm -rf gradint

gradint-android.zip: $(Common_Files) gradint.py
	7za a gradint-android.zip $(Common_Files)
	zip -d gradint-android.zip 'samples/utils*'
	mkdir gradint
	echo 'import gradint0;gradint0.main()' > gradint/gradint.py # QPython tends to load faster if we have a simple wrapper script
	cd gradint && python ../thindown.py android < ../gradint.py > gradint0.py && 7za a ../gradint-android.zip gradint*.py && cd ..
	rm -rf gradint

gradintcab.zip: gradint.cab
	zip -9 gradintcab.zip gradint.cab
	rm gradint.cab

gradint-noGUI.exe: $(Common_Files) gradint.py
	rm -rf windows0 ; cp -r windows windows0
	cd windows0 && 7za x gradint.7z && rm gradint.bgz && cd ..
	cd windows0/gradint && 7za x ../espeak-windows.bgz && rm ../espeak-windows.bgz && cd ../.. # bundled copy of eSpeak that unpacks in espeak/
	cp -r $(Common_Files) windows0/gradint/
	mv windows0/gradint/samples/utils "windows0/gradint/samples/advanced utilities"
	zip -0 windows0/gradint/library.zip gradint.py # (important to have no compression)
	for N in windows0/gradint/*.txt windows0/gradint/*/*.txt windows0/gradint/*/*.txt windows0/*.bat windows0/*/*.bat windows0/7zip.conf; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	# add a utf-8 BOM to start of vocab.txt, to ensure Notepad saves it in utf-8
	cd windows0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("vocab.txt").read())' && mv v2 vocab.txt && cd ../..
	cd windows0/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("advanced.txt").read())' && mv v2 advanced.txt && cd ../..
	# shortcuts: Don't use .lnk files, they are far too horrible (even if you put %HOMEDRIVE%%HOMEPATH% in the shortcut, it still stores the original location, and you can't reliably create them on the client without delving rediculously deep into Windows programming).  Perhaps could use .url files, but we just use small batch files.  Prepend a common header to each one.  (NB it won't work to try to force the sort order by calling things _uninstall, ~uninstall, etc, unless you want Z_uninstall, Z_advanced etc)
	cd windows0/shortcuts ; mv header.bat bat_header ; for N in *.bat ../startup/*.bat; do if ! test "$$N" == uninstall.bat; then cat bat_header "$$N" > n ; mv n "$$N"; fi; done ; rm bat_header ; cd ../..
	# now run 7zip (look in a few extra places for it, and give it its full path in argv[0])
	cd windows0 ; 7za a data.7z setup.bat gradint shortcuts startup ; cd ..
	cat windows0/7zS.sfx windows0/7zip.conf windows0/data.7z > gradint-noGUI.exe
	rm -rf windows0

GUI.exe: gradint.py
	rm -rf windows0 ; cp -r windowsGUI windows0
	cd windows0 && 7za x gradint.bgz && rm gradint.bgz && cd ..
	for N in windows0/7zip.conf; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	zip -0 windows0/gradint/library.zip gradint.py # (important to have no compression)
	cd windows0 ; 7za a data.7z setup.bat gradint ; cd ..
	cat windows/7zS.sfx windows0/7zip.conf windows0/data.7z > GUI.exe
	rm -rf windows0

gradint.tbz: $(Mac_Files)
	mkdir gradint
	cp -r $(Mac_Files) gradint
	chmod +x gradint/start-gradint.app/sox gradint/start-gradint.app/sox-14.4.2 gradint/start-gradint.app/qtplay
	mv gradint/samples/utils "gradint/samples/advanced utilities"
	for N in hanzi-prompts/*.txt; do python2 -c "open('gradint/samples/prompts/$$(echo $$N|sed -e s,.*/,,)','w').write('\\xef\\xbb\\xbf'+open('$$N').read())"; done # overwriting the pinyin ones (as will bundle espeak so can translit.), and NB we *do* need the byte-order-mark on Mac OS 10.6 for TextEdit
	cd gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("vocab.txt").read())' && mv v2 vocab.txt && cd ..
	cd gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("advanced.txt").read())' && mv v2 advanced.txt && cd ..
	cd gradint ; mv $(Most_Mac_Files) start-gradint.app/ ; mv start-gradint.app Gradint.app ; cd Gradint.app/Contents/MacOS ; sed -e s/start-gradint/Gradint/g -e s,Gradint.app/Contents,Contents,g < start-gradint > Gradint ; cp Gradint "Gradint 2"; chmod +x Gradint "Gradint 2" ; rm start-gradint ; cd ../../../.. # hide it all inside the app (optional) ("Gradint 2" is for upgrades - see code for details)
	# tar -c gradint/ | bzip2 -9 > gradint.tbz
	# use this alternative version if hiding all inside the app:
	cd gradint ; tar -c Gradint.app | bzip2 -9 > ../gradint.tbz; cd ..
	rm -rf gradint

gradint-installer.command: gradint.tbz
	# Someone reported not being able to see Gradint.app after double-clicking on the tbz in her Safari downloads window.  It probably just unpacked to the downloads folder and didn't show it.  So let's make a wraper script which forces it to the desktop.
	# Update: This won't work, because there's no way to chmod +x it
	# (except by making a dmg file, which you need to be on a Mac to do)
	# (however, if you ARE on a mac you could still "make gradint.dmg" and send it to whoever's having problems)
	cat mac/install.sh gradint.tbz > gradint-installer.command
	chmod +x gradint-installer.command
gradint.dmg: gradint-installer.command
	if [ -d /Volumes/Gradint ]; then diskutil eject /Volumes/Gradint; fi
	if [ -e gradint.dmg ]; then rm gradint.dmg; fi
	hdiutil create -megabytes $$[$$(du -h gradint-installer.command | sed -e 's/\..*//')+1] -fs HFS+ -volname Gradint gradint
	open gradint.dmg
	while ! cp gradint-installer.command /Volumes/Gradint/; do echo Retrying ; sleep 1 ; done # 'open' might delay
	chmod +x /Volumes/Gradint/gradint-installer.command
	diskutil eject /Volumes/Gradint

gradint.bgz: $(Linux_Files)
	mkdir gradint
	cp -r $(Linux_Files) gradint
	tar -c gradint/ | bzip2 -9 > gradint.bgz
	rm -rf gradint

servertools.bgz: server
	rm -f server/*~ server/*.pyc
	tar -c server/ | bzip2 -9 > servertools.bgz

gradint.zip: $(Riscos_Files) riscos.zip
	mkdir \!gradint
	cp -r $(Riscos_Files) \!gradint
	cd \!gradint && for F in samples/README.txt samples/prompts/README.txt vocab.txt advanced.txt; do sed -e 's,\.wav,/wav,g' -e 's,\.mp3,/mp3,g' -e 's,\.txt,/txt,g' -e 's,\.py\.,/py.,g' -e 's,\.py$$,/py,g' -e 's,TRANS\.TBL,TRANS/TBL,g' -e 's,samples/utils/,samples.utils.,g' -e 's,samples/,samples.,g' < $$F > n && mv n $$F ; done && cd .. # TODO: even in the suggested bash command lines?  and what of .cdr .au (but be cautious about 'overzealous' search/replace)
	cp riscos.zip gradint.zip # the existing zip file has the right RISC OS filetype for the Obey file (difficult to do on non-RISCOS systems)
	zip -9 -r gradint.zip \!gradint/* # update with gradint sources
	rm -rf \!gradint

publish: $(All_Versions) gradint.py
	scp -C gradint.py srcf:gradint/
	scp -C server/gradint.cgi srcf:public_html/
	mv $(All_Versions) ~/homepage/public/gradint/
	cp vocab.txt advanced.txt ~/homepage/public/gradint/
	cp samples/README.txt ~/homepage/public/gradint/samples-readme.txt
	cp samples/prompts/README.txt ~/homepage/public/gradint/prompts-readme.txt
	grep ^program_name < src/top.py|head -1|sed -e 's/.*radint v/v/' -e 's/ .*/./' > ~/homepage/public/gradint/latest-version.txt
	make clean
	~/homepage/update

gradint-build.7z:
	mkdir /tmp/gradint-build00
	cp -r * /tmp/gradint-build00
	rm -r /tmp/gradint-build00/LICENSE /tmp/gradint-build00/README.md /tmp/gradint-build00/charlearn
	mv /tmp/gradint-build00 gradint
	make -C gradint clean
	rm -rf gradint/extras
	7za a gradint-build.7z gradint/
	rm -rf gradint

# "make CD" to make a CD/ directory with all versions, for a live CD
CD: $(Mac_Files) gradint.zip
	rm -rf CD ; mkdir CD
	cd CD && 7za x ../windows/gradint.7z && 7za x ../windowsGUI/gradint.7z && cd ..
	cp -r $(Mac_Files) CD/gradint
	cp windows/setup.bat CD
	cp -r windows/shortcuts windows/startup CD/gradint/
	cd CD/gradint/shortcuts ; mv header.bat bat_header ; for N in *.bat ../startup/*.bat; do if ! test "$$N" == uninstall.bat; then cat bat_header "$$N" > n ; mv n "$$N"; fi; done ; rm bat_header ; cd ../../..
	mv CD/gradint/start-gradint.app CD/gradint/MacOS-version.app
	echo "@start gradint-wrapper.exe" > CD/gradint/Windows-version.bat # as can't rename the .exe
	echo '#!/bin/bash'>CD/gradint/Linux-version.sh; echo python gradint.py>>CD/gradint/Linux-version.sh # don't rename gradint.py because it's used by Mac version also
	mv gradint.zip CD/gradint/RiscOS-version.zip
	zip -0 CD/gradint/library.zip gradint.py # (important to have no compression)
	for N in CD/gradint/*.txt CD/gradint/*/*.txt CD/gradint/*/*/*.txt CD/setup.bat CD/gradint/*.bat CD/gradint/*/*.bat; do python2 -c "import sys; sys.stdout.write(sys.stdin.read().replace('\r','').replace('\n','\r\n'))" < "$$N" > n && mv n "$$N"; done
	cd CD/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("vocab.txt").read())' && mv v2 vocab.txt && cd ../..
	cd CD/gradint && python2 -c 'open("v2","w").write("\xef\xbb\xbf"+open("advanced.txt").read())' && mv v2 advanced.txt && cd ../..
	echo "<html><body><h1>Gradint Live CD" > CD/Read_Me.html
	grep ^program_name < src/top.py|head -1|sed -e 's/.*radint v/v/' -e 's/ .*/./' >> CD/Read_Me.html
	echo "</h1><h2>In the 'gradint' folder on this CD:</h2><ul><li>Recorded words are in <tt>samples</tt> folder<li>Synthesized words are in <tt>vocab.txt</tt> (and take priority over recorded words)<li>Run the program by choosing 'Windows-version', 'MacOS-version', 'Linux-version' or 'RiscOS-version' as appropriate<li>Don't worry about the many other files (they are supporting components)<li>Run it once per day if possible<li>You can change <tt>settings.txt</tt> and <tt>advanced.txt</tt> (e.g. set it to output to disk for listening later, or change the length of lesson), and you can manage the recorded and synthesized words, but you need to copy the 'gradint' folder to your hard disk (or use the 'setup' .bat file in Windows) before making changes, otherwise you can only run it the way it's set up at the moment because CDs are read-only.</ul></body></html>" >> CD/Read_Me.html
	chmod -R +x CD # needed if you're going to copy it using Cygwin
	echo;echo;echo "Made CD directory.  Can add gradint/samples, gradint/vocab.txt, gradint/espeak for Windows, gradint/espeak-.. for OSX, sox Win/Mac binaries, oggenc or whatever for Windows, etc."

cleanup:
	find . -type f '(' -name '*~' -o -name '*.pyc' -o -name DEADJOE ')' -exec rm -vf '{}' ';'
	rm -rvf __pycache__ # must be separate from find, as some find implementations exec before trying to descend and then error
clean: cleanup
	rm -rf gradint.py $(All_Versions) src/defaults.py gradint-installer.command gradint.dmg

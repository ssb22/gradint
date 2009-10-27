gradint build instructions
--------------------------

See Makefile for what you can do.

As a GPL program, gradint can include parts of other GPL programs.

You will need 7-Zip for making the Windows version
(so you'll need to be running on x86 Linux or Cygwin).
windows/7zS.sfx is the stub for 7-zip self-extracting files
(you might want to update this from www.7-zip.org as long as
updated versions still work with gradint's 7zip setup file).  7zip is LGPL.

windows/gradint contains quite a few files that were output by compiling an
earlier version of gradint on py2exe under python2.3 (both of which are GPL)
on a Windows box.  Those files are: datetime.pyd _sre.pyd w9xpopen.exe
winsound.pyd library.zip gradint-wrapper.exe python23.dll.  In order to
avoid having to use a Windows box with py2exe every time (and note py2exe
with Python 2.5 requires Administrator access to the Windows system to
install, so it's no good running that in an average university login
environment), all we have to do is update library.zip with the latest
gradint.py using 0 compression (Makefile does this).  gradint-wrapper.exe
then simply imports gradint and runs its main().

As it's not particularly easy to add new libraries to library.zip now I
don't have a proper py2exe installation, and as it's best to keep the
Windows size down, gradint MUST ensure that it can work within Python 2.3
and using only the libraries provided in that library.zip file.  (It can
attempt to import other libraries, but it must have a fall-back mechanism if
they're not there, as they almost certainly won't be there on Windows.)

windows/ also contains a copy of ptts.exe (extracted from Jampal from
jampal.sourceforge.net with is GPL) and madplay.exe (I can't remember how I
got this binary but I know madplay is GPL).

The Windows setup will install to Program Files\gradint on Windows 9x and
%HomePath%\gradint on later versions.  The start menu and desktop
"shortcuts" are all batch-file hacks because I haven't made a "real" Windows
%installer, but it should be OK on most systems.

start-gradint.app contains the Mac files.  It has a binary of qtplay which
is redistributable (see qtplay.copyright), and also a Finder script that
starts gradint.py in a Terminal.

(qtplay is compiled for PowerPC; Intel macs should automatically use the
emulator.)

riscos.zip contains a copy of !PlayIt (which is re-distributable) and a
compiled version of the Wenhua binary (which is GPL and related to gradint -
see vocab.txt).  It's important not to re-create riscos.zip except by using
a RISCOS-aware zip program (such as on RISC OS itself) otherwise the RISC OS
file types will be corrupted (especially that of the Obey file).  However,
the Makefile can and does add the current gradint version to riscos.zip as
it doesn't matter that this filetype is not set correctly.

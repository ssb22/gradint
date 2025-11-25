# Graduated Interval Recall tool
from https://ssb22.user.srcf.net/gradint
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint) just in case)

Gradint is a program that can be used to make your own self-study audio tapes for learning foreign-language vocabulary.  You can use it to help with a course, to prepare for speaking assignments, or just to keep track of the vocabulary you come across.

Gradint uses a variant of the “graduated-interval recall” method published by Pimsleur in 1967.  It’s like audio flashcards that appear in a special pattern designed to help you remember.  The Pimsleur accelerated language courses use several techniques (they say some are patented), and Gradint does not imitate all that, but this particular 1967 idea is now in the public domain so Gradint can use it to help you learn your own choice of vocabulary.

Gradint gives only audio, so you concentrate on pronunciation. (And so you can listen during daily routines e.g. washing etc, since you don’t have to look or press buttons during a lesson.) Gradint can write its lessons to MP3 or similar files for you to hear later, or it can play them itself and try to adapt to emergency interruptions.  The words it uses can be taken from real sound recordings or they can be synthesized by computer.  You can add words to your collection at any time, and Gradint can manage collections of thousands of words (and supports batch entry).  It can also help you rehearse longer texts such as poems.

Gradint is Free/Libre and Open Source Software distributed under the GNU General Public License (GPL v3).

## Setup instructions
1. Download the appropriate version.
   * **Windows:** download the [Windows installer](https://ssb22.user.srcf.net/gradint/gradint.exe) and run it.  (You do not need Administrator rights.)
     * On Windows 7+ click the small “More options” link to reveal the “Run anyway” option (I haven’t paid Microsoft to make me a “known publisher”).
     * There are incorrect reports that Gradint is a virus or a trojan.  See my [discussion of Gradint’s supposedly-malicious behaviour](README-wrapper.md).
   * **Mac:** download the [Mac version](https://ssb22.user.srcf.net/gradint/gradint.tbz), unpack it, and open Gradint.  Should work with versions of OS X from 10.0 through 10.14, but on 10.15 it might need permission to run from the Security settings.
   * For **GNU/Linux and other Unix systems** (including OLPC laptops, NAS devices and the Raspberry Pi), download the [GNU/Linux version](https://ssb22.user.srcf.net/gradint/gradint.bgz), do `tar -jxf gradint.bgz` and run using `gradint/gradint.py` (compatible with both Python 2 and Python 3). Also install `espeak` and `python-tk` packages if possible.
   * For **Windows Mobile** (6.0 or earlier) install [PythonCE](https://ssb22.user.srcf.net/wm/PythonCE.WM.CAB), install [gradint.cab](https://ssb22.user.srcf.net/gradint/gradintcab.zip) **and run Setup in the gradint folder.**  (This will also install eSpeak, and some scripts to read the clipboard.  It will run faster if you have a RAMdisk.)
   * For **Nokia/Symbian S60 phones** (e.g. E63, N71, N86, N97, 6120), install [PyS60](https://web.archive.org/web/20110727070040/https://garage.maemo.org/frs/download.php/5952/Python_1.9.4.sis) and [ScriptShell](https://web.archive.org/web/20110727070117/https://garage.maemo.org/frs/download.php/5910/PythonScriptShell_1.9.4_3rdEd.sis) (those links are for 3rd edition phones; for other editions google it), unpack gradint-S60.zip into the phone’s `data\python` or `python` folder, open Python and run script `gradint.py`.
   * For **Android** phones (including very old ones), install the old version 1.2.5 of QPython and disable Play Store updates on it (as version 3.0 is broken, especially on Android 4.x). Unpack [gradint-android.zip](https://ssb22.user.srcf.net/gradint/gradint-android.zip) into `qpython/scripts` (or `com.hipipal.qpyplus/scripts` on older versions), and optionally set QPython’s “default program” to `gradint.py` (or if you have SL4A+Python, use `/sdcard/sl4a/scripts`)
   * **RISC OS:** For RISC OS 4, download [RISC OS Python 2.3](http://web.archive.org/web/20070315150725/python.acorn.de/Python-2.3-runtime-2003-08-03.zip) (via Internet Archive), [gradint.zip](https://ssb22.user.srcf.net/gradint/gradint.zip) and PlayIt; shift-click to open `!gradint` or click to run.  For RISC OS 5 on ARM7+ use Python 3.8, edit `!Run` to say Python3, and use MP3s not WAVs; install AMPlayer, and eSpeak if possible.
   * **Online:** You can use [Gradint Web edition](https://ssb22.user.srcf.net/gradint.cgi) with any browser.  You can set up your own server with the Unix version and the [server scripts](server/README.txt) (also includes scripts for email-based service).

**Additional downloads for Chinese:** [Yali Cheng’s Mandarin voice](https://ssb22.user.srcf.net/gradint/yali-voice.exe) ([hear a sample](https://ssb22.user.srcf.net/gradint/yali.mp3)); a [lower-pitch version of Yali’s voice](https://ssb22.user.srcf.net/gradint/yali-lower.exe); [Cameron Wong’s Cantonese voice](https://ssb22.user.srcf.net/gradint/cameron-voice.exe).  These are larger downloads but less “robotic” than the voice that comes with Gradint.  On Windows just open them; on other systems put them in the same folder as you put Gradint.  Source is in my separate Git repositories `yali-voice`, `yali-lower` and `cameron-voice`.

2. Tell the program which language you want to learn.  On most systems, Gradint will show a GUI which lets you do this.  A more technical way to do it is to edit the file settings.txt.
3. Give the program some words and phrases to teach.  This can be any combination of real recordings and computer-synthesized words, and you can always add more later.  You can use the graphical interface (on supported systems), or you can:
  * place real recordings in the samples directory and its sub­directories (see [the file README.txt in the samples directory](samples/README.txt))
  * add words that you want synthesized by computer to vocab.txt (see [the instructions in vocab.txt](vocab.txt))
4. If possible, prepare some audio prompts such as “say again” and “do you remember how to say”.  These can be real recordings or synthesized text.  Some text for English and Chinese is already provided, but if you won’t be using a speech synthesizer you can download [sampled English prompts](https://ssb22.user.srcf.net/gradint/en-prompts.zip).  For any other language you should ideally add your own; for details of how to do this, see [the file README.txt in the prompts subdirectory](samples/prompts/README.txt) of the samples directory.

You should then be able to run the program every time you want a lesson.

You can do more advanced things if you are able to edit configuration files.  For details see the file [advanced.txt](advanced.txt) (to make changes you will need to open the copy in your gradint installation). 

## Building

This repository contains the Gradint build environment, including a `Makefile` that can create these installers by packaging up versions of the Python script for various environments (Windows, Mac, Linux, Windows Mobile, S60, Android, RISC OS) plus utilities for running Gradint on a server.  Not all of Gradint's functions are available in all environments.

A separate program [charlearn](charlearn/README.md) can help you learn to recognise foreign characters.  If you are learning Chinese, [be careful of commercial computer voices](voice-mistakes.md).

## Citation
Silas S. Brown and Peter Robinson.  Addressing Print Disabilities in Adult Foreign-language Acquisition.  In: Proceedings of the 10th International Conference on Human-Computer Interaction (HCII 2003, Crete, Greece), Vol.4: Universal Access in HCI, pp 38-42.

## Copyright and Trademarks
All material © Silas S. Brown unless otherwise stated.
Android is a trademark of Google LLC.
ARM is a registered trademark of Advanced RISC Machines, Ltd or its subsidiaries.
GitHub is a trademark of GitHub Inc.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Microsoft is a registered trademark of Microsoft Corp.
MP3 is a trademark that was registered in Europe to Hypermedia GmbH Webcasting but I was unable to confirm its current holder.
Pimsleur is a registered trademark of Beverly Pimsleur exclusively licensed to Simon & Schuster.
Python is a trademark of the Python Software Foundation.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
RISC OS is a trademark of Pace Micro Technology Plc which might now have passed to RISC OS Ltd but I was unable to find definitive documentation.
Symbian was a trademark of the Symbian Foundation until its insolvency in 2022 and I was unable to find what happened to the trademark after that.
Unix is a trademark of The Open Group.
Windows is a registered trademark of Microsoft Corp.
Any other trademarks I mentioned without realising are trademarks of their respective holders. 

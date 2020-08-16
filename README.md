# gradint
Graduated Interval Recall program from http://ssb22.user.srcf.net/gradint

(also mirrored at http://ssb22.gitlab.io/gradint just in case)

Gradint is a program that can be used to make your own self-study audio tapes for learning foreign-language vocabulary. You can use it to help with a course, to prepare for speaking assignments, or just to keep track of the vocabulary you come across.

Gradint uses a variant of the “graduated-interval recall” method published by Pimsleur in 1967.  It’s like audio flashcards that appear in a special pattern designed to help you remember. The Pimsleur accelerated language courses use several techniques (they say some are patented), and Gradint does not imitate all that, but this particular 1967 idea is now in the public domain so Gradint can use it to help you learn your own choice of vocabulary.

Gradint gives only audio, so you concentrate on pronunciation. (And so you can listen during daily routines e.g. washing etc, since you don’t have to look or press buttons during a lesson.) Gradint can write its lessons to MP3 or similar files for you to hear later, or it can play them itself and try to adapt to emergency interruptions. The words it uses can be taken from real sound recordings or they can be synthesized by computer. You can add words to your collection at any time, and Gradint can manage collections of thousands of words (and supports batch entry).  It can also help you rehearse longer texts such as poems.

Gradint is Free/Libre and Open Source Software distributed under the GNU General Public License (GPL v3).

The Gradint home page (linked above) contains installers for various platforms and details of how to run them.  This repository contains the Gradint build environment, including a `Makefile` that can create these installers by packaging up versions of the Python script for various environments (Windows, Mac, Linux, Windows Mobile, S60, Android, RISC OS) plus utilities for running Gradint on a server.  Not all of Gradint's functions are available in all environments.

If you are learning Chinese, you might also want Yali Cheng’s Mandarin voice or Cameron Wong’s Cantonese voice.  Installers for these may also be found on the Gradint home page, and source in my separate Git repositories `yali-voice`, `yali-lower` and `cameron-voice`.  They are larger downloads but less "robotic" than the eSpeak voice.

Once you have installed Gradint, you must tell the program which language(s) you want to learn.  On most systems, Gradint will show a GUI which lets you do this.  You can also edit the file `settings.txt`.

Then you can give the program some words and phrases to teach.  This can be any combination of real recordings and computer-synthesized words, and you can always add more later. You can use the graphical interface (on supported systems), or you can place real recordings in the samples directory and its subdirectories (see the file `README.txt` in the `samples` directory), and add words that you want synthesized by computer to vocab.txt (see the instructions in `vocab.txt`).

If possible, prepare some audio prompts such as “say again” and “do you remember how to say”.  These can be real recordings or synthesized text. Some text for English and Chinese is already provided.  For any other language you should ideally add your own; for details of how to do this, see the file README.txt in the prompts subdirectory of the samples directory.

You should then be able to run the program every time you want a lesson.  For more advanced things, see the settings in the file advanced.txt.

Citation: Silas S. Brown and Peter Robinson. Addressing Print Disabilities in Adult Foreign-language Acquisition. In: Proceedings of the 10th International Conference on Human-Computer Interaction (HCII 2003, Crete, Greece), Vol.4: Universal Access in HCI, pp 38-42.

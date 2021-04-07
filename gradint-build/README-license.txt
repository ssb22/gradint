Licensing notes
---------------

As a GPL program, Gradint can include parts of other GPL programs.

It is possible that many of these programs could be included anyway
even if Gradint were not GPL, since they are optional and are run as
system commands independently of the Gradint process: this seems to
fit the "mere aggregation" clause of the GPL.  However, Gradint's use
of eSpeak may be a 'borderline' case, as may be the Windows version's
use of py2exe, so I feel the safest thing is to make Gradint GPL too.

I could make a more liberally licensed version of the Gradint core
code without the parts that drive eSpeak etc.  This liberally-licensed
core code would then be includeable in the whole GPL version and also
in other non-GPL projects.  To keep things simple, I have not made
such a division by default (the Gradint GUI displays "GPL" because
it's usually associated with eSpeak, and to save screen space I don't
want to change that to "whole thing's GPL but some parts are Apache"),
but contact me if you need me to make or approve a cut-down version of
the code containing just the parts that don't have to be GPL, probably
as a separate project.

The GPL allows commercial use, and it does not allow the removal of
any permissions it grants, including the permission for commercial
use.  Therefore, it is NOT allowed to take a GPL program together with
a program that's distributed under a "non-commercial use only" license
and distribute the combined version, unless it falls under the GPL's
provision of "mere aggregation".  (I could give special permission,
but my permission would not be valid if the above "borderline" cases
really do mean that Gradint must be GPL with no extra permissions.)

The RISC OS distribution of Gradint includes PlayIt, which is licensed
for non-commercial use only.  Since Gradint's use of PlayIt is
optional, and it is run as an independent system command with a very
simple command line (no complex exchange of data structures etc), I
believe this should qualify as "mere aggregation".

The Windows and Mac versions of Gradint include not only eSpeak but
also some customised dictionary files, one of which contains
pronunciation data derived from the OALD with a "non-commercial only"
license.  Since eSpeak's dictionary is a user-customisable file loaded
at runtime, and does not make up part of eSpeak's code proper, it is
arguable that making a non-commercial download of eSpeak + OALD is
"mere aggregation" allowed by the GPL.  However, there is also the
issue that this modified dictionary was derived not only from the OALD
but also from eSpeak's original data files, including en_rules which
is explicitly GPL, so I would need special permission to combine this
with OALD in a non-commercial binary (otherwise I would have to ship
the files separately and have eSpeak combine them at runtime).
Thankfully though, I do indeed have special permission, because I
collaborated with eSpeak's original author Jonathan Duddington (to
help improve eSpeak's English, Mandarin and Ancient Greek voices and
port it to Mac and PocketPC), and he was happy for my pre-compiled
"non-commercial only" combination to go into Gradint's downloads.

This does however mean these Mac and Windows bundles cannot be
upgraded to eSpeak-NG, since the special permission I received from
Jonathan to make a "non-commercial" OALD-integrated download applies
only to my use of his original eSpeak data: the eSpeak-NG contributors
were not informed.  Anyway, my process for adding OALD entries to the
eSpeak data has not been as thoroughly tested on recent versions of
the eSpeak-NG data.  Gradint can however work with eSpeak-NG if you
supply it separately, and it is possible that eSpeak-NG's improvements
in its default data have reduced the need for OALD data anyway,
although I'm still choosing to ship old-eSpeak plus OALD in my
Mac and Windows 'bundle' downloads.

windows/ contains a copy of ptts.exe extracted from Jampal from
jampal.sourceforge.net with is GPL, and madplay.exe (I can't remember
how I got this binary but I know madplay is GPL), and now LAME.

qtplay is used by Gradint on OS X 10.4, which lacks afplay.
We bundle qtplay with the Mac version, and it has a BSD-like license
(see qtplay.copyright for details).

Mac and Windows additionally ship SOX which is GPL.

To save on server space, I have not included the source code to the
third-party free software binaries I ship.  This is possible because
I am performing an unmodified non-commercial distribution of binaries
whose source is widely available and can easily be found on the
Internet, which is something explicitly allowed by the GPL
(GPLv2 section 3c, GPLv3 section 6d).  If anyone has difficulty
obtaining source code for any of these binaries then please let me know.

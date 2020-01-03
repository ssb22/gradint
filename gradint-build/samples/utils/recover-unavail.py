#!/usr/bin/env python2

# Script to recover vocabulary from the "unavailable"
# entries in Gradint's progress file.  Use if for some
# reason the vocab file has been truncated (e.g. filesystem
# problems) and this propagated to your backup system before
# you noticed.

# v1.0 (c) 2012 Silas S. Brown.  License: GPL

ignore_words_that_are_also_in_backup_unavail = True # if the fault just happened

import gradint, time
gradint.availablePrompts = gradint.AvailablePrompts()
d = gradint.ProgressDatabase()

if ignore_words_that_are_also_in_backup_unavail:
    gradint.progressFile = gradint.progressFileBackup
    gradint.pickledProgressFile = None
    d2 = gradint.ProgressDatabase(alsoScan=0)
    for x in d2.unavail: d.unavail.remove(x)

print "# Words recovered %d-%02d-%02d" % time.localtime()[:3]
print "# - capitalisation and comments are missing; order may be approximate"

gradint.reallyKnownThreshold = 0
poems,line2index = gradint.find_known_poems(d.unavail)
output = [] ; doneAlready = {}
for pLines in poems:
    if filter(lambda x:not x.startswith("!synth:") or not gradint.languageof(x)==gradint.secondLanguage, pLines): continue
    plines2 = []
    for p in pLines:
        idx = line2index[p] ; doneAlready[idx] = 1
        prompt = d.unavail[idx][1]
        equals = ""
        if type(prompt)==type([]):
            if len(prompt)==3: equals = prompt[1]
        elif not plines2 and not prompt==p: equals=prompt # if 1st line
        if equals:
            assert equals.startswith("!synth:") and gradint.languageof(equals)==gradint.firstLanguage, "recovery of poems with non-L1 secondary prompts not yet supported"
            equals = "="+gradint.textof(equals)
        plines2.append(gradint.textof(p)+equals)
    output.append((d.unavail[line2index[pLines[0]]][0], gradint.secondLanguage, gradint.firstLanguage, "\n".join(["begin poetry"]+plines2+["end poetry"])))

for count,(num,L1,L2) in zip(xrange(len(d.unavail)),d.unavail):
    if count in doneAlready: continue
    if type(L1)==type(L2)==type("") and L1.startswith("!synth:") and L2.startswith("!synth:"):
        lang1,lang2 = gradint.languageof(L1),gradint.languageof(L2)
        output.append((num,lang2,lang1,"%s=%s" % (gradint.textof(L2),gradint.textof(L1))))

output.sort() ; output.reverse()
curL2,curL1 = None,None
for num,lang2,lang1,text in output:
    if not (lang2,lang1) == (curL2,curL1):
        curL2,curL1 = lang2,lang1
        print "SET LANGUAGES %s %s" % (curL2,curL1)
    print text

#!/bin/bash
# Sync gradint build environment to SVN
wget -N http://people.ds.cam.ac.uk/ssb22/gradint/gradint-build.7z || exit 1
rm -rf gradint # (any leftover ../gradint/gradint directory)
7z x gradint-build.7z || exit 1
diff -r gradint-build gradint|grep "^Only in gradint-build"|grep -v \\.svn|sed -e 's,Only in ,svn del ",' -e 's,: ,/,' -e 's/$/"/'|bash
cp -pur gradint/* gradint-build/
find gradint|grep -v \\.svn|sed -e 's/gradint/gradint-build/' -e 's/^/svn add "/' -e 's/$/"/'|bash
rm -rf gradint gradint-build.7z # if need to save space
if test "a$Msg" == a; then export Msg="Gradint update"; fi
svn commit -m "$Msg"

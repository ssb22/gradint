#!/bin/bash
# Sync gradint build environment to Git
git pull --no-edit
wget -N http://people.ds.cam.ac.uk/ssb22/gradint/gradint-build.7z || exit 1
rm -rf gradint # (any leftover ../gradint/gradint directory)
7z x gradint-build.7z || exit 1
diff -r gradint-build gradint|grep "^Only in gradint-build"|grep -v \\.git|sed -e 's,Only in ,git rm ",' -e 's,: ,/,' -e 's/$/"/'|bash
cp -pur gradint/* gradint-build/
find gradint|grep -v \\.git|sed -e 's/gradint/gradint-build/' -e 's/^/git add "/' -e 's/$/"/'|bash
rm -rf gradint gradint-build.7z # if need to save space
if test "a$Msg" == a; then export Msg="Gradint update"; fi
git commit -am "$Msg" && git push

#!/bin/bash
wget -N http://people.pwf.cam.ac.uk/ssb22/gradint/gradint-build.bgz
rm -rf gradint
tar -jxvf gradint-build.bgz
rm -rf gradint/extras # TODO shouldn't be in gradint-build.bgz anyway
diff -r gradint-build gradint|grep "^Only in gradint-build"|grep -v \\.svn|sed -e 's,Only in ,svn del ,' -e 's,: ,/,'
cp -pur gradint/* gradint-build/
find gradint-build -not -regex \\.svn -exec svn add '{}' ';'
if test "a$Msg" == a; then export Msg="Gradint update"; fi
svn commit -m "$Msg"

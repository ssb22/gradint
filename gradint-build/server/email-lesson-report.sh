#!/bin/bash

# email-lesson-report.sh - produces an HTML fragment
# showing a brief status report of the users of email-lesson.sh
# (can be used to check nobody's running out of vocab)
# - report is written to standard output so you can include
# it in a script that makes some larger HTML page

# v1.12 (C) 2007, 2009. 2021-22 Silas S. Brown, License: GPL

if ! pwd|grep email_lesson_users >/dev/null; then
  echo "This script should be run from an email_lesson_users directory (see email-lesson.sh)"
  exit
fi
echo '<TABLE>'
touch -d 0:00 /dev/shm/.midnight 2>/dev/null || touch -d 0:00 /tmp/.midnight
if [ -e /dev/shm/.midnight ]; then Midnight=/dev/shm/.midnight; else Midnight=/tmp/.midnight; fi
for P in $(ls --color=none -t -- */progress.txt */podcasts-to-send 2>/dev/null); do
  if test "$P" -nt $Midnight; then Em="*";else unset Em; fi
  if echo "$P" | grep podcasts-to-send$ >/dev/null; then
    zgrep -H -m 1 . "$P"|grep -v ^user\.|sed -e 's,/.*:,</TD><TD COLSPAN=4>,' -e "s/^/<TR><TD>$Em/" -e "s,$,</TD></TR>,"
  else
    zgrep -H -m 1 lessonsLeft "$P"|grep -v user\.|sed -e 's,/.*#,,' -e "s/^/<TR><TD>$Em/" -e "s, ,</TD><TD>,g" -e "s,$,</TD></TR>," -e "s/=/: /g"
  fi
done
rm $Midnight
echo '</TABLE>'

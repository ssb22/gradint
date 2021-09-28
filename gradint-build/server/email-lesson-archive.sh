#!/bin/bash

# email-lesson-archive.sh - archive an old email-lesson user
# (C) 2008,2021 Silas S. Brown, License: GPL

if ! pwd|grep email_lesson_users >/dev/null; then
  echo "This script should be run from an email_lesson_users directory (see email-lesson.sh)"
  exit 1
fi
if test "a$1" == a; then
  echo "Syntax: email-lesson-archive.sh userName (...)"
  exit 1
fi
. config
while ! test "a$1" == a; do
  if test -e "$1"; then
    unset U; unset Links
    if echo "$1"|grep "^user.0*" >/dev/null; then
      # specifying by user.0* id
      export U=$1
      export Links=$(find . -maxdepth 1 -lname "$U")
    elif find "$1" -maxdepth 0 -type l|grep . >/dev/null; then
      # specifying by symlink
      export Links=$1
      export U=$(ls -l --color=none "$1"|sed -e 's/.* -> //')
    else echo "Warning: can't make sense of username $1"; fi
    if ! test "a$U" == a; then
      if test -e "$U/lastdate"; then
        if test "a$Links" == a; then export Shortname=$U; else export Shortname=$Links; fi
        if echo "$PUBLIC_HTML" | grep : >/dev/null; then
        ssh $PUBLIC_HTML_EXTRA_SSH_OPTIONS "$(echo "$PUBLIC_HTML"|sed -e 's/:.*//')" rm -v "$(echo "$PUBLIC_HTML"|sed -e 's/[^:]*://')/$U-$(cat $U/lastdate).*"
        else rm -v "$PUBLIC_HTML/$U-$(cat "$U/lastdate")".*
        fi
      fi
      tar -jcvf "$Shortname.tbz" "$U" $Links
      mkdir -p old
      mv -v --backup=numbered "$Shortname.tbz" old/
      rm -rf "$U" $Links
    fi
  else echo "Warning: User $1 does not exist"; fi
shift; done

#!/bin/bash

# email-lesson.sh: a script that can help you to
# automatically distribute daily Gradint lessons
# to students using a web server with reminder
# emails.  Version 1.15

# (C) 2007-2010,2020-2022 Silas S. Brown, License: GPL

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

DEFAULT_SUBJECT_LINE="Vocabulary practice (automatic message from gradint)"
DEFAULT_FORGOT_YESTERDAY="You forgot your lesson yesterday.
Please remember to download your lesson from"
# (NB include the words "you forgot" so that it's obvious this is a reminder not an additional lesson)
DEFAULT_EXPLAIN_FORGOT="Please try to hear one lesson every day.  If you download that lesson today,
this program will make the next one for tomorrow."
DEFAULT_NEW_LESSON="Your lesson for today is at"
DEFAULT_LISTEN_TODAY="Please download and listen to it today."
DEFAULT_AUTO_MESSAGE="This is an automatic message from the gradint program.
Any problems, requests, or if you no longer wish to receive these emails,
let me know."

if ! [ -e gradint.py ]; then
  echo "Error: This script should ALWAYS be run in the gradint directory."
  exit 1
fi

if which mail >/dev/null 2>/dev/null; then DefaultMailProg=mail
elif which mutt >/dev/null 2>/dev/null; then DefaultMailProg="mutt -x"
else DefaultMailProg="ssh example.org mail"
fi

if test "a$1" == "a--run"; then
  set -o pipefail # make sure errors in pipes are reported
  if ! [ -d email_lesson_users ]; then
    echo "Error: script does not seem to have been set up yet"
    exit 1
  fi
  Gradint_Dir=$(pwd)
  cd email_lesson_users || exit
  . config
  if [ -e "$Gradint_Dir/.email-lesson-running" ]; then
    Msg="Another email-lesson.sh --run is running - exitting.  (Remove $Gradint_Dir/.email-lesson-running if this isn't the case.)"
    echo "$Msg"
    echo "$Msg"|$MailProg -s email-lesson-not-running $ADMIN_EMAIL # don't worry about retrying that
    exit 1
  fi
  touch "$Gradint_Dir/.email-lesson-running"
  if echo "$PUBLIC_HTML" | grep : >/dev/null && man ssh 2>/dev/null | grep ControlMaster >/dev/null; then
    # this version of ssh is new enough to support ControlPath, and PUBLIC_HTML indicates a remote host, so let's do it all through one connection
    ControlPath="-o ControlPath=$TMPDIR/__gradint_ctrl"
    while true; do ssh -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS -n -o ControlMaster=yes $ControlPath $(echo "$PUBLIC_HTML"|sed -e 's/:.*//') sleep 86400; sleep 10; done & MasterPid=$!
  else unset MasterPid
  fi
  (while ! bash -c "$CAT_LOGS_COMMAND"; do echo "cat-logs failed, re-trying in 61 seconds" 1>&2;sleep 61; done) | grep '/user\.' > "$TMPDIR/._email_lesson_logs"
  # (note: sleeping odd numbers of seconds so we can tell where it is if it gets stuck in one of these loops)
  Users="$(echo user.*)"
  cd ..
  unset NeedRunMirror
  for U in $Users; do
    . email_lesson_users/config
    if ! test "a$GLOBAL_GRADINT_OPTIONS" == a; then GLOBAL_GRADINT_OPTIONS="$GLOBAL_GRADINT_OPTIONS ;"; fi
    # set some (but not all!) variables to defaults in case not set in profile
    SUBJECT_LINE="$DEFAULT_SUBJECT_LINE"
    FORGOT_YESTERDAY="$DEFAULT_FORGOT_YESTERDAY"
    LISTEN_TODAY="$DEFAULT_LISTEN_TODAY"
    NEW_LESSON="$DEFAULT_NEW_LESSON"
    EXPLAIN_FORGOT="$DEFAULT_EXPLAIN_FORGOT"
    AUTO_MESSAGE="$DEFAULT_AUTO_MESSAGE"
    unset Extra_Mailprog_Params1 Extra_Mailprog_Params2 GRADINT_OPTIONS
    Use_M3U=no
    FILE_TYPE=mp3
    if grep $'\r' "email_lesson_users/$U/profile" >/dev/null; then
      # Oops, someone edited profile in a DOS line-endings editor (e.g. Wenlin on WINE for CJK stuff).  DOS line endings can mess up Extra_Mailprog_Params settings.
      tr -d $'\r' < "email_lesson_users/$U/profile" > email_lesson_users/$U/profile.removeCR
      mv "email_lesson_users/$U/profile.removeCR" "email_lesson_users/$U/profile"
    fi
    . "email_lesson_users/$U/profile"
    if test "a$Use_M3U" == ayes; then FILE_TYPE_2=m3u
    else FILE_TYPE_2=$FILE_TYPE; fi
    if echo "$MailProg" | grep ssh >/dev/null; then
      # ssh discards a level of quoting, so we need to be more careful
      SUBJECT_LINE="\"$SUBJECT_LINE\""
      Extra_Mailprog_Params1="\"$Extra_Mailprog_Params1\""
      Extra_Mailprog_Params2="\"$Extra_Mailprog_Params2\""
    fi
    if [ -e "email_lesson_users/$U/lastdate" ]; then
      if test "$(cat "email_lesson_users/$U/lastdate")" == "$(date +%Y%m%d)"; then
        # still on same day - do nothing with this user this time
	continue
      fi
      if ! grep "$U-$(cat email_lesson_users/$U/lastdate)"\. "$TMPDIR/._email_lesson_logs" >/dev/null
      # (don't add $FILE_TYPE after \. in case it has been changed)
      then
        Did_Download=0
        if [ -e "email_lesson_users/$U/rollback" ]; then
          if [ -e "email_lesson_users/$U/progress.bak" ]; then
            mv "email_lesson_users/$U/progress.bak" "email_lesson_users/$U/progress.txt"
            rm -f "email_lesson_users/$U/progress.bin"
            Did_Download=1 # (well actually they didn't, but we're rolling back)
          fi # else can't rollback, as no progress.bak
          if [ -e "email_lesson_users/$U/podcasts-to-send.old" ]; then
            mv "email_lesson_users/$U/podcasts-to-send.old" "email_lesson_users/$U/podcasts-to-send"
          fi
        fi
      else Did_Download=1; fi
      rm -f "email_lesson_users/$U/rollback"
      if test $Did_Download == 0; then
        # send a reminder
        DaysOld="$(python -c "import os,time;print(int((time.time()-os.stat('email_lesson_users/$U/lastdate').st_mtime)/3600/24))")"
        if test $DaysOld -lt 5 || test $(date +%u) == 1; then # (remind only on Mondays if not checked for 5 days, to avoid filling up inboxes when people are away and can't get to email)
        while ! $MailProg -s "$SUBJECT_LINE" "$STUDENT_EMAIL" "$Extra_Mailprog_Params1" "$Extra_Mailprog_Params2" <<EOF
$FORGOT_YESTERDAY
$OUTSIDE_LOCATION/$U-$(cat "email_lesson_users/$U/lastdate").$FILE_TYPE_2
$EXPLAIN_FORGOT

$AUTO_MESSAGE
EOF
do echo "mail sending failed; retrying in 62 seconds"; sleep 62; done; fi
        continue
      else
        # delete the previous lesson
        if echo "$PUBLIC_HTML" | grep : >/dev/null; then ssh -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS $ControlPath $(echo "$PUBLIC_HTML"|sed -e 's/:.*//') rm "$(echo "$PUBLIC_HTML"|sed -e 's/[^:]*://')/$U-$(cat "email_lesson_users/$U/lastdate").*"
        else rm $PUBLIC_HTML/$U-$(cat "email_lesson_users/$U/lastdate").*; fi
	# (.* because .$FILE_TYPE and possibly .m3u as well)
      fi
    fi
    CurDate=$(date +%Y%m%d)
    if ! test "a$GRADINT_OPTIONS" == a; then GRADINT_OPTIONS="$GRADINT_OPTIONS ;"; fi
    if echo "$PUBLIC_HTML" | grep : >/dev/null; then OUTDIR=$TMPDIR
    else OUTDIR=$PUBLIC_HTML; fi
    USER_GRADINT_OPTIONS="$GLOBAL_GRADINT_OPTIONS $GRADINT_OPTIONS samplesDirectory='email_lesson_users/$U/samples'; progressFile='email_lesson_users/$U/progress.txt'; pickledProgressFile='email_lesson_users/$U/progress.bin'; vocabFile='email_lesson_users/$U/vocab.txt';saveLesson='';loadLesson=0;progressFileBackup='email_lesson_users/$U/progress.bak';outputFile="
    # (note: we DO keep progressFileBackup, because it can be useful if the server goes down and the MP3's need to be re-generated or something)
    unset Send_Podcast_Instead
    if [ -s "email_lesson_users/$U/podcasts-to-send" ]; then
      Send_Podcast_Instead="$(head -1 email_lesson_users/$U/podcasts-to-send)"
      NumLines=$[$(cat "email_lesson_users/$U/podcasts-to-send"|wc -l)-1]
      tail -$NumLines "email_lesson_users/$U/podcasts-to-send" > "email_lesson_users/$U/podcasts-to-send2"
      mv "email_lesson_users/$U/podcasts-to-send" "email_lesson_users/$U/podcasts-to-send.old"
      mv "email_lesson_users/$U/podcasts-to-send2" "email_lesson_users/$U/podcasts-to-send"
      if test $NumLines == 0; then
        echo "$U" | $MailProg -s Warning:email-lesson-run-out-of-podcasts $ADMIN_EMAIL
      fi
    else rm -f "email_lesson_users/$U/podcasts-to-send.old" # won't be a rollback after this
    fi
    if test "$ENCODE_ON_REMOTE_HOST" == 1; then
      ToSleep=123
      while ! if test "a$Send_Podcast_Instead" == a; then
        python gradint.py "$USER_GRADINT_OPTIONS '-.sh'" </dev/null 2>"$TMPDIR/__stderr" | ssh -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS $ControlPath $(echo "$PUBLIC_HTML"|sed -e 's/:.*//') "mkdir -p $REMOTE_WORKING_DIR; cd $REMOTE_WORKING_DIR; cat > __gradint.sh;chmod +x __gradint.sh;PATH=$SOX_PATH ./__gradint.sh|$ENCODING_COMMAND $(echo $PUBLIC_HTML|sed -e 's/[^:]*://')/$U-$CurDate.$FILE_TYPE;rm -f __gradint.sh";
      else
        cd "email_lesson_users/$U" ; cat "$Send_Podcast_Instead" | ssh -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS $ControlPath $(echo "$PUBLIC_HTML"|sed -e 's/:.*//') "cat > $(echo $PUBLIC_HTML|sed -e 's/[^:]*://')/$U-$CurDate.$FILE_TYPE"; cd ../..;
      fi; do
        # (</dev/null so exceptions don't get stuck on 'press enter to continue' to a temp stderr if running from a terminal)
        $MailProg -s gradint-to-ssh-failed,-will-retry $ADMIN_EMAIL < "$TMPDIR/__stderr"
        # (no spaces in subj so no need to decide whether to single or double quote)
        # (don't worry about mail errors - if net is totally down that's ok, admin needs to know if it's a gradint bug causing infinite loop)
        sleep $ToSleep ; ToSleep=$[$ToSleep*1.5] # (increasing-time retries)
      done
      rm "$TMPDIR/__stderr"
      if test "a$Use_M3U" == ayes; then
        while ! ssh -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS $ControlPath $(echo "$PUBLIC_HTML"|sed -e 's/:.*//') "echo $OUTSIDE_LOCATION/$U-$CurDate.$FILE_TYPE > $(echo $PUBLIC_HTML|sed -e 's/[^:]*://')/$U-$CurDate.m3u"; do sleep 63; done
      fi
    else # not ENCODE_ON_REMOTE_HOST
      if ! test "a$Send_Podcast_Instead" == a; then
        (cd "email_lesson_users/$U" ; cat "$Send_Podcast_Instead") > "$OUTDIR/$U-$CurDate.$FILE_TYPE"
      elif ! python gradint.py "$USER_GRADINT_OPTIONS '$OUTDIR/$U-$CurDate.$FILE_TYPE'" </dev/null; then
        echo "Errors from gradint itself (not ssh/network); skipping this user."
        echo "Failed on $U, check output " | $MailProg -s gradint-failed $ADMIN_EMAIL
        continue
      fi
      if test "a$Use_M3U" == ayes; then
        echo "$OUTSIDE_LOCATION/$U-$CurDate.$FILE_TYPE" > "$OUTDIR/$U-$CurDate.m3u"
      fi
      if echo "$PUBLIC_HTML" | grep : >/dev/null; then
        while ! scp $ControlPath -C $PUBLIC_HTML_EXTRA_SSH_OPTIONS $OUTDIR/$U-$CurDate.* "$PUBLIC_HTML/"; do
          echo "scp failed; re-trying in 60 seconds"
  	sleep 64
        done
        rm "$OUTDIR/$U-$CurDate".*
      fi
    fi
    NeedRunMirror=1
    if ! [ -e "email_lesson_users/$U/progress.bak" ]; then touch "email_lesson_users/$U/progress.bak"; fi # so rollback works after 1st lesson
    while ! $MailProg -s "$SUBJECT_LINE" "$STUDENT_EMAIL" "$Extra_Mailprog_Params1" "$Extra_Mailprog_Params2" <<EOF
$NEW_LESSON
$OUTSIDE_LOCATION/$U-$CurDate.$FILE_TYPE_2
$LISTEN_TODAY

$AUTO_MESSAGE
EOF
do echo "mail sending failed; retrying in 65 seconds"; sleep 65; done
    echo "$CurDate" > "email_lesson_users/$U/lastdate"
    unset AdminNote
    if test "a$Send_Podcast_Instead" == a; then
      if test "$(zgrep -H -m 1 lessonsLeft "email_lesson_users/$U/progress.txt"|sed -e 's/.*=//')" == 0; then AdminNote="Note: $U has run out of new words"; fi
    elif ! [ -e "email_lesson_users/$U/podcasts-to-send" ]; then AdminNote="Note: $U has run out of podcasts"; fi
    if ! test "a$AdminNote" == a; then
      while ! echo "$AdminNote"|$MailProg -s gradint-user-ran-out "$ADMIN_EMAIL"; do echo "Mail sending failed; retrying in 67 seconds"; sleep 67; done
    fi
  done # end of per-user loop
  if test "a$NeedRunMirror" == "a1" && ! test "a$PUBLIC_HTML_MIRROR_COMMAND" == a; then
    while ! $PUBLIC_HTML_MIRROR_COMMAND; do
      echo "PUBLIC_HTML_MIRROR_COMMAND failed; retrying in 79 seconds"
      echo As subject | $MailProg -s "PUBLIC_HTML_MIRROR_COMMAND failed, will retry" "$ADMIN_EMAIL" || true # ignore errors
      sleep 79
    done
  fi
  rm -f "$TMPDIR/._email_lesson_logs"
  if ! test a$MasterPid == a; then
    kill $MasterPid
    kill $(ps axwww|grep "$TMPDIR/__gradint_ctrl"|sed -e 's/^ *//' -e 's/ .*//') 2>/dev/null
    rm -f "$TMPDIR/__gradint_ctrl" # in case ssh doesn't
  fi
  rm -f "$Gradint_Dir/.email-lesson-running"
  exit 0
fi

echo "After setting up users, run this script daily with --run on the command line."
echo "As --run was not specified, it will now go into setup mode."
# Setup:
if test "a$EDITOR" == a; then
  echo "Error: No EDITOR environment variable set"; exit 1
fi
if ! [ -e email_lesson_users/config ]; then
 echo "It seems the email_lesson_users directory is not set up"
 echo "Press Enter to create a new one,
 or Ctrl-C to quit if you're in the wrong directory"
 read
 mkdir email_lesson_users || exit 1
 cat > email_lesson_users/config <<EOF
# You need to edit this file.
GLOBAL_GRADINT_OPTIONS="" # if set, will be added to all gradint command lines (e.g. to set synthCache if it's not in advanced.txt)
MailProg="$DefaultMailProg" # mail, or mutt -x, or ssh some.host mail, or whatever
PUBLIC_HTML=~/public_html # where to put files on the WWW.  If it contains a : then scp will be used to copy them there.
OUTSIDE_LOCATION=http://$(hostname -f)/~$(whoami) # where they appear from outside
CAT_LOGS_COMMAND="false" # Please change this to a command that cats the
# server logs for at least the last 48 hours.  (On some systems you may need
# to make the script suid root.)  It is used to check that the users have
# downloads their lessons and remind them if not.

# If PUBLIC_HTML specifies a remote host and
# CAT_LOGS_COMMAND involves ssh-ing to that same remote
# host, you can include \$ControlPath
# for the ssh command to go through the already-open
# control connection (\$ControlPath will expand to
# nothing on systems with old ssh's that don't support this)

PUBLIC_HTML_EXTRA_SSH_OPTIONS="" # if set and PUBLIC_HTML is on a remote host, these options will be added to all ssh and scp commands to that host - use this for things like specifying an alternative identity file with -i

PUBLIC_HTML_MIRROR_COMMAND="" # if set, will be run after any new lessons are written to PUBLIC_HTML.
# This is for unusual setups where PUBLIC_HTML is not the real public_html directory but some command can be run to mirror its contents to the real one (perhaps on a remote server that cannot take passwordless SSH from here; of course you'd need to set up an alternative way of getting the files across and the log entries back).
# Note: Do not add >/dev/null or similar redirects to PUBLIC_HTML_MIRROR_COMMAND as some versions of bash will give an error.

export TMPDIR=/tmp # or /dev/shm or whatever

ENCODE_ON_REMOTE_HOST=0  # if 1, will ssh to the remote host
# that's specified in PUBLIC_HTML (which *must* be host:path in this case)
# and will run an encoding command *there*, instead of encoding
# locally and copying up.  This is useful if the local machine is the
# only place gradint can run but it can't encode (e.g. Linux server running on NAS device).
# If you set the above to 1 then you also need to set these options:
REMOTE_WORKING_DIR=. # directory to change to on remote host e.g. /tmp/gradint (will create with mkdir -p if does not exist)
# (make sure $PUBLIC_HTML etc is absolute or is relative to $REMOTE_WORKING_DIR) (don't use spaces in these pathnames)
SOX_PATH=$PATH
# make sure the above includes the remote host's "sox" as well as basic commands
ENCODING_COMMAND="lame --vbr-new -V 9 -"
# (used only if ENCODE_ON_REMOTE_HOST is set)
# (include the full path for that if necessary; SOX_PATH will NOT be searched)
# (set options for encode wav from stdin & output to the file specified on nxt parameter.  No shell quoting.)
ADMIN_EMAIL=admin@example.com # to report errors
EOF
 cd email_lesson_users; $EDITOR config; cd ..
 echo "Created email_lesson_users/config"
fi
cd email_lesson_users
while true; do
  echo "Type a user alias (or just press Enter) to add a new user, or Ctrl-C to quit"
  read Alias
  ID=$(mktemp -d user.$(python -c 'import random; print(random.random())')XXXXXX) # (newer versions of mktemp allow more than 6 X's so the python step isn't necessary, but just in case we want to make sure that it's hard to guess the ID)
  if ! test "a$Alias" == a; then ln -s "$ID" "$Alias"; fi
  cd "$ID" || exit 1
  cat > profile <<EOF
# You need to edit the settings in this file.
STUDENT_EMAIL=student@example.org  # change to student's email address
export GRADINT_OPTIONS="" # extra gradint command-line options, for example to
                          # specify a different first and second language
FILE_TYPE=mp3 # change to something else if you want
Use_M3U=no # if yes, sends a .m3u link to the student
# instead of sending the file link directly.  Use this if
# the student needs to stream over a slow link, but note
# that it makes offline listening one step more complicated.

# IMPORTANT: the student's vocab.txt and samples/ should also be placed or
# symlinked into the user's directory $(pwd)
# (It has a shorter symlink if you provided one,
# but the ID has to be long to make private URLs hard to guess.)
# (If on any given day the user has not downloaded a lesson
# and you change the vocab.txt or samples, the change
# will not take effect until they download the pending lesson,
# UNLESS you create a file called rollback in the user's directory
# in which case the pending lesson will be discarded on the next run
# and another created from the previous progress data.)
# You may also create a file in the user's directory called
# podcasts-to-send containing pathnames of "podcasts" (must be
# in same format as the user takes, will not be recoded)
# and the first of these will be sent INSTEAD OF a Gradint
# lesson until there are no more left.  Note however that
# touching rollback will overwrite podcasts-to-send with the
# previous version (podcasts-to-send.old).

# IMPORTANT: If the script is not using your normal email address,
# ensure the student knows how to check the junk / spam folder for them
# and mark the address as safe (e.g. Hotmail junk "Mark as Safe").
# If you have to move to a different server, you may need to warn all
# students that the lessons will now come from a different address.

# Optional settings for customising the text of the message:
SUBJECT_LINE="$DEFAULT_SUBJECT_LINE"
FORGOT_YESTERDAY="$DEFAULT_FORGOT_YESTERDAY"
LISTEN_TODAY="$DEFAULT_LISTEN_TODAY"
NEW_LESSON="$DEFAULT_NEW_LESSON"
EXPLAIN_FORGOT="$DEFAULT_EXPLAIN_FORGOT"
AUTO_MESSAGE="$DEFAULT_AUTO_MESSAGE"
Extra_Mailprog_Params1=""
Extra_Mailprog_Params2=""
# You may need to set Extra_Mailprog_Params to extra parameters
# if the subject or text includes characters that need to be sent
# in a specific charset.  For example, to send Chinese (Simplified)
# in UTF-8 with Mutt, you can do this:
# export GRADINT_OPTIONS="firstLanguage='zh'; secondLanguage='en'; otherLanguages=[]"
# export LANG=C
# Extra_Mailprog_Params1="-e"
# Extra_Mailprog_Params2="set charset='utf-8'; set send_charset='utf-8'"
# SUBJECT_LINE="英文词汇练习 (English vocabulary practice)"
# FORGOT_YESTERDAY="你忘记了昨天的课 (you forgot your lesson yesterday).
# 请记得下载 (please remember to download) :"
# EXPLAIN_FORGOT="请试图天天听一课 (please try to hear one lesson every day)
# 如果你今天下载, 这个软件要明天给你另一个课.
# (If you download that lesson today,
# this program will make the next one for tomorrow.)"
# NEW_LESSON="今天的课在以下的网址 (your lesson for today is at)"
# LISTEN_TODAY="请你今天下载而听 (please download and listen to it today)."
# AUTO_MESSAGE="这个电邮是软件写的 (this is an automatic message from the gradint program).
# 假如你有问题, 请告诉我 (any problems, let me know)."

# You can also override *some* of the email_lesson_users/config
# options on a per-user basis by putting them here,
# e.g. OUTSIDE_LOCATION, ENCODING_COMMAND, MailProg.
# (overriding OUTSIDE_LOCATION is useful if you need to supply the IP address to a user with DNS lookup problems)

EOF
  $EDITOR profile
  cd ..
done

#!/bin/bash

SamplesDir="samples/" # Must include trailing /
ProgressFile="progress.txt"
if ! [ -e $SamplesDir ]; then echo "Error: $SamplesDir does not exist (are you in the right directory?)"; exit 1; fi
if ! [ -e $ProgressFile ]; then echo "Error: $ProgressFile does not exist (are you in the right directory?)";exit 1;fi

if test "a$1" == a; then
  echo "Usage: $0 oldname newname"
  echo "oldname and newname are relative to $SamplesDir, and can be prefixes of several files/directories"
  echo "Moves files from one samples directory to another, keeping $ProgressFile adjusted.  Make sure gradint is not running (including waiting for start) when in use."
  exit 1
fi

Src=$1
Dest=$2

find "$SamplesDir" -follow -type f | grep "^$SamplesDir$Src" | \
while true; do read || break;
  SrcFile=$REPLY
  DestFile=$(echo "$SrcFile"|sed -e "s|^$SamplesDir$Src|$SamplesDir$Dest|")
  mkdir -p "$DestFile" ; rmdir "$DestFile" # ensure parent dirs exist before moving file across
  mv -b "$SrcFile" "$DestFile"
  SrcFile=$(echo "$SrcFile"|sed -e "s|$SamplesDir||")
  DestFile=$(echo "$DestFile"|sed -e "s|$SamplesDir||")
  gzip -fdc "$ProgressFile" | sed -e "s|$SrcFile|$DestFile|g" > /tmp/newprog ; mv /tmp/newprog "$ProgressFile" # (ideally should re-write to batch these changes, but leave like this for now in case need to recover from unfinished operation)
done

rmdir "$SamplesDir$Src" 2>/dev/null >/dev/null # IF it's a directory

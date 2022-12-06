@echo off
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEDRIVE=C:
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEPATH="\Program Files"
cd /D "%HOMEDRIVE%%HOMEPATH%\gradint"

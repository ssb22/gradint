@echo off

rem find where gradint is
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEDRIVE=C:
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEPATH="\Program Files"
if not exist "%USERPROFILE%" set USERPROFILE="C:\WINDOWS"

if exist "%HOMEDRIVE%%HOMEPATH%\gradint" goto ok

echo ERROR: Cannot find the Gradint installation
echo You should install this AFTER installing gradint
pause
goto end

:ok
xcopy gradint "%HOMEDRIVE%%HOMEPATH%\gradint" /S /Y

rem Open the desktop folder
cd /D "%USERPROFILE%\Desktop"
explorer gradint

:end

@echo off
echo This will completely remove gradint from your system
echo INCLUDING ANY WORDS YOU HAVE ADDED.
echo.
echo If that is not what you want, close this window NOW.
echo Otherwise press any key.
pause >nul

echo Some people run this by mistake.
echo Are you REALLY SURE you want to delete all your words?
pause >nul

echo Absolutely?
pause >nul

echo Positively?
pause >nul

echo Really really really, you are not just pressing buttons at random?
pause >nul

echo.
echo LAST CHANCE - REALLY DELETE EVERYTHING?
pause >nul

if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEDRIVE=C:
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEPATH="\Program Files"
if not exist "%USERPROFILE%" set USERPROFILE="C:\WINDOWS"

tskill gradint-wrapper 2>nul
taskkill /f /im gradint-wrapper.exe 2>nul >nul
cd /D "%HOMEDRIVE%%HOMEPATH%"
rmdir /S /Q gradint
cd /D "%USERPROFILE%"
del "Start Menu\Programs\Startup\Run gradint once per day.bat"
rmdir /S /Q "Start Menu\Programs\gradint" "Desktop\gradint"
rem (TODO - Chinese Windows shortcuts also - see setup.bat)

@echo off

rem Find a good place to put Gradint.  On Windows 9x this can be C:\Program Files.  On XP/NT/etc we'd better check for different home directories.  Also check where the profile is.

if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEDRIVE=C:
if not exist "%HOMEDRIVE%%HOMEPATH%" set HOMEPATH="\Program Files"
if not exist "%USERPROFILE%" set USERPROFILE="C:\WINDOWS"
if exist "%HOMEDRIVE%%HOMEPATH%\gradint" goto doneAlready
move gradint "%HOMEDRIVE%%HOMEPATH%\gradint"
if errorlevel 1 goto copy
goto tryZh
:copy
mkdir "%HOMEDRIVE%%HOMEPATH%\gradint"
xcopy gradint "%HOMEDRIVE%%HOMEPATH%\gradint" /S
:tryZh
if not exist "%USERPROFILE%\「开始」菜单" goto nextBit
rem Detected Chinese(Simplified) Windows with PRC legacy locale
rem (see comments below "goto PRC" for more explanation)
rem - let's assume their first language is "zh" for the GUI
echo firstLanguage="zh" > "%HOMEDRIVE%%HOMEPATH%\gradint\settings.txt"
echo secondLanguage="en" >> "%HOMEDRIVE%%HOMEPATH%\gradint\settings.txt"
goto nextBit

:doneAlready
if not exist "%HOMEDRIVE%%HOMEPATH%\gradint\gradint-wrapper.exe" goto silentRepair
echo It seems that gradint was already installed on your system.
echo The installer will replace the program files but not the data.
echo Your vocab.txt and recorded words will not be changed,
echo and any new options will not be added to your advanced.txt
echo (see the advanced.txt on the website if you want to set them).
echo.
echo If you wanted a fresh install, stop now and uninstall first.
echo.
pause
:silentRepair
rem copy all program files, even the ones that have never been changed, in case it was a manual or python-only install
tskill gradint-wrapper 2>nul
taskkill /f /im gradint-wrapper.exe 2>nul >nul
cd gradint
rem support users who install yali BEFORE gradint
rem (don't worry about trying move and catching problems with Vista etc - just use copy)
if not exist "%HOMEDRIVE%%HOMEPATH%\gradint\settings.txt" copy settings.txt "%HOMEDRIVE%%HOMEPATH%\gradint"
if not exist "%HOMEDRIVE%%HOMEPATH%\gradint\advanced.txt" copy advanced.txt "%HOMEDRIVE%%HOMEPATH%\gradint"
if not exist "%HOMEDRIVE%%HOMEPATH%\gradint\vocab.txt" copy vocab.txt "%HOMEDRIVE%%HOMEPATH%\gradint"
if exist "%HOMEDRIVE%%HOMEPATH%\gradint\samples" goto gotSamples
mkdir "%HOMEDRIVE%%HOMEPATH%\gradint\samples"
xcopy samples "%HOMEDRIVE%%HOMEPATH%\gradint\samples" /S
goto afterGotSamples
:gotSamples
rem Update the previously-buggy whatSay_zh.txt prompt
if exist "%HOMEDRIVE%%HOMEPATH%\gradint\samples\prompts\whatSay_zh.txt" copy /Y samples\prompts\whatSay_zh.txt "%HOMEDRIVE%%HOMEPATH%\gradint\samples\prompts"
:afterGotSamples
mkdir "%HOMEDRIVE%%HOMEPATH%\gradint\tcl" >nul 2>nul
xcopy /D /Y /S tcl "%HOMEDRIVE%%HOMEPATH%\gradint\tcl"
copy /Y library.zip "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y datetime.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y gradint-wrapper.exe "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y ptts.exe "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y madplay.exe "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y python23.dll "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y _sre.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y _tkinter.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y tcl84.dll "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y tk84.dll "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y unicodedata.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y zlib.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y w9xpopen.exe "%HOMEDRIVE%%HOMEPATH%\gradint"
copy /Y winsound.pyd "%HOMEDRIVE%%HOMEPATH%\gradint"
mkdir "%HOMEDRIVE%%HOMEPATH%\gradint\espeak" >nul 2>nul
xcopy /D /Y /S espeak "%HOMEDRIVE%%HOMEPATH%\gradint\espeak"
copy /Y sox.exe "%HOMEDRIVE%%HOMEPATH%\gradint"
cd ..

:nextBit

rem Some old versions of gradint tried to use schtasks
rem instead of once_per_day|2.  This didn't really work.
rem If we're upgrading from one of those, we want to remove the task.
schtasks /delete /tn gradint /f 2>nul

rem Make desktop and start menu shortcuts
if not exist startup cd gradint
rem (if running from the live CD)

if exist "%USERPROFILE%\「开始」菜单" goto PRC
if exist "%USERPROFILE%\Desktop" goto noWarning
cls
echo === BIG FAT WARNING !!! ===
echo.
echo It seems you are running a non-English version of Windows.
echo This simple batch file knows that your profile is located at
echo %USERPROFILE%
echo but it can only assume that your desktop is
echo %USERPROFILE%\Desktop
echo and your start menu is
echo %USERPROFILE%\Start Menu
echo.
echo NON-ENGLISH VERSIONS OF WINDOWS USE DIFFERENT NAMES FOR THESE FOLDERS.
echo This simple batch file has no way of knowing where your desktop and start
echo menu really are.  It will therefore create folders called 'Desktop' and
echo 'Start Menu' in your profile folder %USERPROFILE%.
echo YOU WILL NEED TO MANUALLY GO INTO THAT FOLDER AND MOVE THE CONTENTS OF
echo Desktop AND Start Menu TO YOUR REAL DESKTOP AND START MENU, otherwise
echo your gradint will NOT be easily accessible.
echo If you do not know what this means, FIND SOMEONE TO HELP YOU.
echo Press any key to continue.
pause >nul
rem (deliberately saying "press any key" ourselves not from 'pause', otherwise that part will be in their own language and they might not try to read the English message before it)
:noWarning

mkdir "%USERPROFILE%\Desktop\gradint"
copy /Y shortcuts\*.* "%USERPROFILE%\Desktop\gradint"
mkdir "%USERPROFILE%\Start Menu\Programs\gradint"
copy /Y shortcuts\*.* "%USERPROFILE%\Start Menu\Programs\gradint"

rem Install startup once-per-day thing
mkdir "%USERPROFILE%\Start Menu\Programs\Startup"
copy /Y startup\*.* "%USERPROFILE%\Start Menu\Programs\Startup"

cd /D "%USERPROFILE%\Desktop"
goto end
:PRC
rem This is a special case for Chinese (Simplified) Windows, configured to use the "Chinese (PRC)" locale for legacy apps (which means these strings should be gb2312 coded).
rem (You can get the names of Start Menu etc folders coded in the current locale by doing dir > file.txt at a command prompt and inspecting file.txt)
mkdir "%USERPROFILE%\桌面\gradint"
ren shortcuts\uninstall.bat "shortcuts\排除.bat"
copy /Y shortcuts\*.* "%USERPROFILE%\桌面\gradint"
mkdir "%USERPROFILE%\「开始」菜单\程序\gradint"
copy /Y shortcuts\*.* "%USERPROFILE%\「开始」菜单\程序\gradint"
mkdir "%USERPROFILE%\「开始」菜单\程序\启动"
copy /Y startup\*.* "%USERPROFILE%\「开始」菜单\程序\启动"
cd /D "%USERPROFILE%\桌面"

:end
rem Open the Gradint desktop folder
rem start explorer gradint

rem (actually, since there's only 1 shortcut now,
rem we might as well just launch it directly)
cd /D "%HOMEDRIVE%%HOMEPATH%\gradint"
start gradint-wrapper.exe once_per_day=2

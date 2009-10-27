# This file is part of the source code of
program_name = "gradint v0.9927 (c) 2002-2009 Silas S. Brown. GPL v3+."
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# This is the start of defaults.py - configuration defaults, automatically extracted from default settings.txt and advanced.txt, so user customisations don't have to be complete (helps with upgrades)
firstLanguage = "en"
secondLanguage = "zh"
outputFile = ""
compress_SH = False
outputFile_appendSilence = 0
if outputFile.endswith("cdr"): outputFile_appendSilence = 5
beepThreshold = 20
startAnnouncement = None
endAnnouncement = None
commentsToAdd = None
orderlessCommentsToAdd = None
otherLanguages = ["cant","ko","jp"]
possible_otherLanguages = ["cant","ko","jp","en","zh"]
maxLenOfLesson = 30*60
saveProgress = 1
ask_teacherMode = 0
maxNewWords = 5
maxReviseBeforeNewWords = 3
newInitialNumToTry = 5
recentInitialNumToTry = 3
newWordsTryAtLeast = 3
knownThreshold = 5
reallyKnownThreshold = 10
meaningTestThreshold = 20
randomDropThreshold = 14
randomDropLevel = 0.67
randomDropThreshold2 = 35
randomDropLevel2 = 0.97
shuffleConstant = 2.0
transitionPromptThreshold = 10
advancedPromptThreshold = 20
transitionPromptThreshold2 = 2
advancedPromptThreshold2 = 5
limit_words = max(1,int(maxNewWords * 0.4))
logFile = "log.txt"
briefInterruptLength = 10
synth_priorities = "eSpeak MacOS SAPI"
extra_speech = []
extra_speech_tofile = []
sapiVoices = {
}
synthCache = ""
synthCache_test_mode = 0
justSynthesize = ""
lily_file = "C:\\Program Files\\NeoSpeech\\Lily16\\data-common\\userdict\\userdict_chi.csv"
ptts_program = None
partialsDirectory = "partials"
betweenPhrasePause = 0.3
partials_are_sporadic = 0
partials_cache_file = ""
vocabFile = "vocab.txt"
samplesDirectory = "samples"
promptsDirectory = "samples"+os.sep+"prompts"
progressFile = "progress.txt"
progressFileBackup = "progress.bak"
pickledProgressFile = "progress.bin"
gui_output_directory = "output"
limit_filename = "!limit"
intro_filename = "_intro"
poetry_filename = "!poetry"
exclude_from_scan = "_disabled"
exclude_from_coverage = "z_try_again"
userNameFile="username.txt"
import_recordings_from = r"\My Documents"
max_extra_buttons = 12
GUI_translations={
"@variants-zh":[u"简体字",u"繁體字"],
"Word in %s":{"zh":u"%s词语","zh2":u"%s詞語"},
"Meaning in %s":{"zh":u"%s意思"},
"en":{"zh":u"英文"},
"zh":{"zh":u"中文"},
"press Control-V to paste":{"zh":u"剪贴: 打Ctrl+V","zh2":u"剪貼: 打Ctrl+V"},
"press Apple-V to paste":{"zh":u"剪贴: 打苹果+V","zh2":u"剪貼: 打蘋果+V"},
"Your first language":{"zh":u"你的语言","zh2":u"你的語言"},
"second":{"zh":u"学习","zh2":u"學習"},
"Change languages":{"zh":u"改变语言选择","zh2":u"改變語言選擇"},
"Cancel lesson":{"zh":u"退出课","zh2":u"退出課"},
"Manage word list":{"zh":u"管理词汇","zh2":u"管理詞匯"},
"words in":{"zh":u"词, 用","zh2":u"詞, 用"},
"new words in":{"zh":u"新词, 用","zh2":u"新詞, 用"},
"mins":{"zh":u"分钟","zh2":u"分鐘"},
"Start lesson":{"zh":u"开始课","zh2":u"開始課"},
"Clear test boxes":{"zh":u"扫清输入地方","zh2":u"掃清輸入地方"},
"Quit":{"zh":u"放弃","zh2":u"放棄"},
"Back to main menu":{"zh":u"回去主要项目表","zh2":u"回去主要項目表"},
"Delete non-hanzi":{"zh":u"除字非汉字","zh2":u"除字非漢字"},
"Speak":{"zh":u"发音","zh2":u"發音"},
"Add to %s":{"zh":u"加到词汇(%s)","zh2":u"加到詞匯(%s)"},
"Recorded words":{"zh":u"录音词语","zh2":u"錄音詞語"},
"To":{"zh":u"到"},
"Make":{"zh":u"做"},
"Speaker":{"zh":u"扬声器","zh2":u"揚聲器"},
"Change or delete item":{"zh":u"更换/删除","zh2":u"更換/刪除"},
"You have not changed the test boxes.  Do you want to delete %s?":{"zh":u"你还没编辑了。你想删除%s吗?","zh2":u"你還沒編輯了。你想刪除%s嗎?"},
"Restore":{"zh":u"归还","zh2":u"歸還"},
"Hear this lesson again?":{"zh":u"再次听那个课吗?","zh2":u"再次聽那個課嗎?"},
"Start this lesson again?":{"zh":u"再次开始这个课吗?","zh2":u"再次開始這個課嗎?"},
"You have %d words in your collection":{"zh":u"你的汇编有%d词","zh2":u"你的彙編有%d詞"},
"%d new words + %d old words":{"zh":u"%d新词而%d旧词","zh2":u"%d新詞而%d舊詞"},
"minutes":{"zh":u"分钟","zh2":u"分鐘"},
"seconds":{"zh":u"秒"},
"Today's lesson teaches %d new words\nand revises %d old words\n\nPlaying time: %d %s %d %s":{"zh":u"今天我们学%d新词而复习%d旧词\n需要%d%s%d%s","zh2":u"今天我們學%d新詞而複習%d舊詞\n需要%d%s%d%s"},
"Today we will learn %d words\nThis will require %d %s %d %s\nFollow the spoken instructions carefully":{"zh":u"今天我们学%d新词, 需要%d%s%d%s\n请仔细听从口头指示","zh2":u"今天我們學%d新詞, 需要%d%s%d%s\n請仔細聽從口頭指示"},
"Family mode (multiple user)":{"zh":u"加别的学生(家人等)","zh2":u"加別的學生(家人等)"},
"Add new name":{"zh":u"加名字"},
"Students":{"zh":u"学生","zh2":u"學生"},
"Brief interrupt":{"zh":u"短打岔"},
"Resume":{"zh":u"恢复","zh2":u"恢復"},
"Emergency brief interrupt":{"zh":u"紧急的短打岔","zh2":u"緊急的短打岔"},
"Resuming...":{"zh":u"正在恢复...","zh2":u"正在恢復..."},
"Big print":{"zh":u"大号字体","zh2":u"大號字體"},
"Compressing, please wait":{"zh":u"正在压缩...","zh2":u"正在壓縮..."},
"All recordings have been compressed to MP3.  Do you also want to make a ZIP file for sending as email?":{"zh":u"所有录音都压缩成为MP3了。 你也想做一个ZIP文件所以能随email附上吗?","zh2":u"所有錄音都壓縮成為MP3了。 你也想做一個ZIP文件所以能隨email附上嗎?"},
"Compress all recordings":{"zh":u"压缩一切录音","zh2":u"壓縮一切錄音"},
"Play":{"zh":u"演"},
"Re-record":{"zh":u"从新录音","zh2":u"從新錄音"},
"(empty)":{"zh":u"(空虚)","zh2":u"(空虛)"},
"Record":{"zh":u"录音","zh2":u"錄音"},
"Add more words":{"zh":u"加多词","zh2":u"加多詞"},
"New folder":{"zh":u"新卷宗"},
"Stop":{"zh":u"停止"},
"Action of spacebar during recording:":{"zh":u"空格键在录音的时候的功能:","zh2":u"空格鍵在錄音的時候的功能:"},
"move down":{"zh":u"进步下面"},
"move along":{"zh":u"进步右边","zh2":u"進步右邊"},
"stop":{"zh":u"停止"},
"(Up)":{"zh":u"(上面)"},
"Record from %s":{"zh":u"从%s做录音","zh2":u"從%s做錄音"},
"Record from file":{"zh":u"从文件做录音","zh2":u"從文件做錄音"},
"Manage recorded words using Gradint":{"zh":u"用这个软件管理录音","zh2":u"用這個軟件管理錄音"},
"Open the recorded words folder":{"zh":u"打开录音的卷宗","zh2":u"打開錄音的卷宗"},
    }
scriptVariants = {}
GUI_for_editing_only = 0
GUI_omit_settings = 0
GUI_omit_statusline = 0
recorderMode = 0
runInBackground = 0
useTK = 1
waitBeforeStart = 1
startFunction = None
oss_sound_device = ""
soundVolume = 1
saveLesson = ""
loadLesson = 0
justSaveLesson = 0
compress_progress_file = 0
paranoid_file_management = 0
once_per_day = 0

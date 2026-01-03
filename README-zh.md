
from https://ssb22.user.srcf.net/gradint/index-zh.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/index-zh.html) just in case)

简体字 | [繁體字](README-zhf.md)

# Gradint自己学外语软件

![screenshot-zh-winCE.png](https://ssb22.user.srcf.net/gradint/screenshot-zh-winCE.png)

跳到: 如何安装 | 学术引用

Gradint软件能帮你准备自学录音带练习外语词汇。 它能补充别的课程，帮你准备发表演讲，或者记录你所遇见的词汇。

**该软件的理论：** Gradint用皮姆斯勒(Pimsleur)1967年所出版的“分级间歇回想”法的变体。好像声音抽认卡, 采用一个特别顺序帮你记忆。 Pimsleur课程 ([听演示](https://ssb22.user.srcf.net/pims-lrnEn-demo.mp3)) 声称有专利的技巧, *Gradint并不违反*, 但1967年的“分级间歇回想”主意现在公有領域所以Gradint能用帮你学你自所选的词汇。

视窗操作系统:

Animation (“memory balls” reinforcement)

技术性的图表一课, 有许多分级间歇 (**grad** uated-**int** erval) 顺序。 短顺序回想旧词; 粉红顺序教新词; 簧显示顺序 能适应。

![diagram.jpg](https://ssb22.user.srcf.net/gradint/diagram.jpg)

(If you have an SVG viewer, you can [download a clearer version](https://ssb22.user.srcf.net/gradint/diagram.svg))

**Gradint *只* 用声音, 所以你能集中发音。** (也意味你能一面梳洗一面听, 因为不需要盯着显示器看。) Gradint 或者做MP3(或其他声音文件格式)让你以后听, 或者直接播放而试试适应你的紧急打断。 所用的词语或者是真正录音或者是机器声音。 你可以随时把词语加到你的目录。 Gradint 能管理一万多词语的积攒。也能帮你排练诗歌等。

Gradint 是免费的自由开源软件。 The latest release is v3.11.

## 如何安装
1. 下载合适的译本。

   如果你学习中文, 请也下载

    [Cheng Yali 的华语声音](https://ssb22.user.srcf.net/gradint/yali-voice.exe) ([听示范](https://ssb22.user.srcf.net/gradint/yali.mp3)) (也有[低音版](https://ssb22.user.srcf.net/gradint/yali-lower.exe)) 或 [黄冠能的粤语声音](https://ssb22.user.srcf.net/gradint/cameron-voice.exe), 比较大的下载但是没有比Gradint所包括的声音那么机器性。 视窗能打开; 别的作业系统把它放在Gradint 的卷宗。

   视窗操作系统

    (不需要管理人员) 下载[视窗 (Windows) 本](https://ssb22.user.srcf.net/gradint/gradint.exe)而打开。
   * On Windows 7+ click the **small “More options” link** to reveal the “Run anyway” option (I haven’t paid Microsoft to make me a “known publisher”).
   * There are incorrect reports that Gradint is a virus or a trojan. See my [discussion of Gradint’s supposedly-malicious behaviour](README-wrapper.md).

   苹果机 (Mac)

    下载 [苹果机本](https://ssb22.user.srcf.net/gradint/gradint.tbz), 打开包裹, 打开`Gradint`. (所有OS X版本10.0到10.14都该运转，但10.15可能需要安全许可)

   GNU/Linux等等

    包括每个孩子一台笔记型电脑(OLPC)、网络储存设备(NAS)和树莓派(Raspberry Pi), 下载 [GNU/Linux译本](https://ssb22.user.srcf.net/gradint/gradint.bgz), 做 `tar -jxf gradint.bgz` 然后 `gradint/gradint.py`. 推荐你也安装 `espeak` 和 `python-tk` 包裹。

   Windows Mobile:

    [Windows Mobile](https://ssb22.user.srcf.net/wm/) 手机6.0或更旧 安装 [PythonCE](https://ssb22.user.srcf.net/wm/PythonCE.WM.CAB), 安装[gradint.cab](https://ssb22.user.srcf.net/gradint/gradintcab.zip) **然后在gradint文件夹打开Setup** 。 (这也安装eSpeak而一些读出剪贴板的脚本。要是您的手机有RAMdisk，Gradint运转的比较快。

   S60:

    Nokia/Symbian S60 手机 安装 [PyS60](https://web.archive.org/web/20110727070040/https://garage.maemo.org/frs/download.php/5952/Python_1.9.4.sis) 和 [ScriptShell](https://web.archive.org/web/20110727070117/https://garage.maemo.org/frs/download.php/5910/PythonScriptShell_1.9.4_3rdEd.sis) (這些連接是S60第三版本的用途，其他版本請用搜索引擎找到合適的PyS60與ScriptShell)，打開[gradint-S60.zip](https://ssb22.user.srcf.net/gradint/gradint-S60.zip)到手機的`data\python`或`python`文件夹, 打开Python然后run script `gradint.py`.

   Android:

    [安卓 (Android)](https://ssb22.user.srcf.net/setup/android.html) 手机 安装 QPython1.2.5的APK, 打开[gradint-android.zip](https://ssb22.user.srcf.net/gradint/gradint-android.zip) 到 `qpython/scripts` (或旧版本的`com.hipipal.qpyplus/scripts`), 然后你可以把QPython的”default program”变成`gradint.py`

   RISC OS:

    RISC OS 4 下载 [RISC OS Python 2.3](http://web.archive.org/web/20070315150725/python.acorn.de/Python-2.3-runtime-2003-08-03.zip), [gradint.zip](https://ssb22.user.srcf.net/gradint/gradint.zip) and PlayIt; shift-click to open `!gradint` or click to run. For RISC OS 5 on ARM7+ use Python 3.8, edit `!Run` to say `Python3`, and use MP3s not WAVs; install AMPlayer, and eSpeak if possible.

   网站版本:

    使用[Gradint网站版本](https://ssb22.user.srcf.net/gradint.cgi)，能用任何浏览器。 为了设定自己的服务器，你可以用上面的Unix版本与这个[服务器脚本](https://ssb22.user.srcf.net/gradint/servertools.bgz) (存档也包括电子邮件服务的脚本)。

2. **告诉软件你要学什么语言。** 在大多数系统, Gradint 能显示一个视窗让你做这样。 或者你可以edit the file `settings.txt`.
3. **给软件词语和短语教。 **   你可以混合真正录音和机器声音。你可以随时把词语加到你的积攒。 在大多数系统, Gradint 能显示一个视窗让你做这样。 或者你可以:

   ![screenshot2.png](https://ssb22.user.srcf.net/gradint/screenshot2.png)

   * 把真正的录音文件放在`samples`文件夹和子目录 (请读英文的`samples`文件夹的`README.txt`)
   * 把你要机器声音读出的词汇加到`vocab.txt`文件 (请读英文的[`vocab.txt`指南](vocab.txt))
4. **如果可能, 准备提示声音 ** 比如 “请跟着说”, “在说一次”等。 英文和中文的机器声音课文已经提供了, 但如果你不想用机器声音或用别的语言, 请自己提供。 关于提供别的提示声音请看 [the file `README.txt` in the `prompts` subdirectory](samples/prompts/README.txt) of the `samples` directory. 我也有 [sampled English prompts](https://ssb22.user.srcf.net/gradint/en-prompts.zip).

然后, 你每当想一课, 能打开这个软件。

如果你的电脑技巧很高, 你也能看[ `advanced.txt`](advanced.txt) (这是参考连接而已。为了做改版，请打开您所安装的Gradint的拷贝。)

程序员: 源代码在所有下载里的`gradint.py`，或者欢迎下载[Gradint build environment](https://ssb22.user.srcf.net/gradint/gradint-build.7z)(看看里面的README.txt)。还有黄冠能所提供的SVN仓储: `svn co http://svn.code.sf.net/p/e-guidedog/code/ssb22`

还有GitHub的仓储: `git clone https://github.com/ssb22/gradint.git`

还有GitLab的仓储: `git clone https://gitlab.com/ssb22/gradint.git`

还有Bitbucket的仓储: `git clone https://bitbucket.org/ssb22/gradint.git`

## 学术引用

Silas S. Brown and Peter Robinson. Addressing Print Disabilities in Adult Foreign-language Acquisition. In: Proceedings of the 10th International Conference on Human-Computer Interaction (HCII 2003, Crete, Greece), Vol.4: Universal Access in HCI, pp 38-42. [PDF](https://ssb22.user.srcf.net/papers/hcii.pdf)

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Android is a trademark of Google LLC.
ARM is a registered trademark of Advanced RISC Machines, Ltd or its subsidiaries.
GitHub is a trademark of GitHub Inc.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Microsoft is a registered trademark of Microsoft Corp.
MP3 is a trademark that was registered in Europe to Hypermedia GmbH Webcasting but I was unable to confirm its current holder.
Pimsleur is a registered trademark of Beverly Pimsleur exclusively licensed to Simon & Schuster.
Python is a trademark of the Python Software Foundation.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
RISC OS is a trademark of Pace Micro Technology Plc which might now have passed to RISC OS Ltd but I was unable to find definitive documentation.
Symbian was a trademark of the Symbian Foundation until its insolvency in 2022 and I was unable to find what happened to the trademark after that.
Unix is a trademark of The Open Group.
Windows is a registered trademark of Microsoft Corp.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.

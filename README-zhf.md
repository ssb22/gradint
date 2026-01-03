
from https://ssb22.user.srcf.net/gradint/index-zhf.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/index-zhf.html) just in case)

[简体字](README-zh.md) | 繁體字

# Gradint自己學外語軟件

![screenshot-zh-winCE.png](https://ssb22.user.srcf.net/gradint/screenshot-zh-winCE.png)

跳到: 如何安裝 | 學術引用

Gradint軟件能幫你準備自學錄音帶練習外語詞彙。 它能補充別的課程，幫你準備發表演講，或者記錄你所遇見的詞彙。

**該軟件的理論：** Gradint用皮姆斯勒(Pimsleur)1967年所出版的“分級間歇回想”法的變體。好像聲音抽認卡, 採用一個特別順序幫你記憶。 Pimsleur課程聲稱有專利的技巧, *Gradint並不違反*, 但1967年的“分級間歇回想”主意現在公有領域所以Gradint能用幫你學你自所選的詞彙。

視窗操作系統:

Animation (“memory balls” reinforcement)

技術性的圖表一課, 有許多分級間歇 (**grad** uated-**int** erval) 順序。 短順序回想舊詞; 粉紅順序教新詞; 簧顯示順序 能適應。

![diagram.jpg](https://ssb22.user.srcf.net/gradint/diagram.jpg)

(If you have an SVG viewer, you can [download a clearer version](https://ssb22.user.srcf.net/gradint/diagram.svg))

**Gradint *只* 用聲音, 所以你能集中發音。** (也意味你能一面梳洗一面聽, 因為不需要盯著顯示器看。) Gradint 或者做MP3(或其他聲音文件格式)讓你以後聽, 或者直接播放而試試適應你的緊急打斷。 所用的詞語或者是真正錄音或者是機器聲音。 你可以隨時把詞語加到你的目錄。 Gradint 能管理一萬多詞語的積攢。也能幫你排練詩歌等。

Gradint 是免費的自由開源軟件。 The latest release is v3.11.

## 如何安裝
1. 下載合適的譯本。

   如果你學習中文, 請也下載

    [Cheng Yali 的華語聲音](https://ssb22.user.srcf.net/gradint/yali-voice.exe) ([聽示範](https://ssb22.user.srcf.net/gradint/yali.mp3)) (也有[低音版](https://ssb22.user.srcf.net/gradint/yali-lower.exe)) 或 [黃冠能的粵語聲音](https://ssb22.user.srcf.net/gradint/cameron-voice.exe), 比較大的下載但是沒有比Gradint所包括的聲音那麼機器性。 視窗能打開; 別的作業系統把它放在Gradint 的卷宗。

   視窗操作系統

    (不需要管理人員) 下載[視窗 (Windows) 本](https://ssb22.user.srcf.net/gradint/gradint.exe)而打開。
   * On Windows 7+ click the **small “More options” link** to reveal the “Run anyway” option (I haven’t paid Microsoft to make me a “known publisher”).
   * There are incorrect reports that Gradint is a virus or a trojan. See my [discussion of Gradint’s supposedly-malicious behaviour](README-wrapper.md).

   蘋果機 (Mac)

    下載 [蘋果機本](https://ssb22.user.srcf.net/gradint/gradint.tbz), 打開包裹, 打開`Gradint`. (所有OS X版本10.0到10.14都該運轉，但10.15可能需要安全許可)

   GNU/Linux等等

    包括每個孩子一檯筆記型電腦(OLPC)、網路儲存設備(NAS)和樹莓派(Raspberry Pi), 下載 [GNU/Linux譯本](https://ssb22.user.srcf.net/gradint/gradint.bgz), 做 `tar -jxf gradint.bgz` 然後 `gradint/gradint.py`. 推薦你也安裝 `espeak` 和 `python-tk` 包裹。

   Windows Mobile:

    [Windows Mobile](https://ssb22.user.srcf.net/wm/) 手機6.0或更舊 安裝 [PythonCE](https://ssb22.user.srcf.net/wm/PythonCE.WM.CAB), 安裝 [gradint.cab](https://ssb22.user.srcf.net/gradint/gradintcab.zip) **然後在gradint文件夾打開Setup** 。 (這也安裝eSpeak而一些讀出剪貼板的腳本。要是您的手機有RAMdisk，Gradint運轉的比較快。

   S60:

    Nokia/Symbian S60 手機 安裝 [PyS60](https://web.archive.org/web/20110727070040/https://garage.maemo.org/frs/download.php/5952/Python_1.9.4.sis) 和 [ScriptShell](https://web.archive.org/web/20110727070117/https://garage.maemo.org/frs/download.php/5910/PythonScriptShell_1.9.4_3rdEd.sis) (这些连接是S60第三版本的用途，其他版本请用搜索引擎找到合适的PyS60与ScriptShell)，打开[gradint-S60.zip](https://ssb22.user.srcf.net/gradint/gradint-S60.zip)到手机的`data\python`或`python`文件夾, 打開Python然後run script `gradint.py`.

   Android:

    [安卓 (Android)](https://ssb22.user.srcf.net/setup/android.html) 手機 安裝 QPython1.2.5的APK, 打開[gradint-android.zip](https://ssb22.user.srcf.net/gradint/gradint-android.zip) 到 `qpython/scripts` (或舊版本的`com.hipipal.qpyplus/scripts`), 然後你可以把QPython的”default program”變成`gradint.py`

   RISC OS:

    RISC OS 4 下載 [RISC OS Python 2.3](http://web.archive.org/web/20070315150725/python.acorn.de/Python-2.3-runtime-2003-08-03.zip), [gradint.zip](https://ssb22.user.srcf.net/gradint/gradint.zip) and PlayIt; shift-click to open `!gradint` or click to run. For RISC OS 5 on ARM7+ use Python 3.8, edit `!Run` to say `Python3`, and use MP3s not WAVs; install AMPlayer, and eSpeak if possible.

   網站版本:

    使用[Gradint網站版本](https://ssb22.user.srcf.net/gradint.cgi)，能用任何瀏覽器。 為了設定自己的服務器，你可以用上面的Unix版本與這個[服務器腳本](https://ssb22.user.srcf.net/gradint/servertools.bgz) (存檔也包括電子郵件服務的腳本)。

2. **告訴軟件你要學什麼語言。** 在大多數系統, Gradint 能顯示一個視窗讓你做這樣。 或者你可以edit the file `settings.txt`.
3. **給軟件詞語和短語教。 **   你可以混合真正錄音和機器聲音。你可以隨時把詞語加到你的積攢。 在大多數系統, Gradint 能顯示一個視窗讓你做這樣。 或者你可以:

   ![screenshot2.png](https://ssb22.user.srcf.net/gradint/screenshot2.png)

   * 把真正的錄音文件放在`samples`文件夾和子目錄 (請讀英文的`samples`文件夾的`README.txt`)
   * 把你要機器聲音讀出的詞彙加到`vocab.txt`文件 (請讀英文的[`vocab.txt`指南](vocab.txt))
4. **如果可能, 準備提示聲音 ** 比如 “請跟著說”, “在說一次”等。 英文和中文的機器聲音課文已經提供了, 但如果你不想用機器聲音或用別的語言, 請自己提供。 關於提供別的提示聲音請看 [the file `README.txt` in the `prompts` subdirectory](samples/prompts/README.txt) of the `samples` directory. 我也有 [sampled English prompts](https://ssb22.user.srcf.net/gradint/en-prompts.zip).

然後, 你每當想一課, 能打開這個軟件。

如果你的電腦技巧很高, 你也能看[ `advanced.txt`](advanced.txt) (這是參考連接而已。為了做改版，請打開您所安裝的Gradint的拷貝。)

程序員: 源代碼在所有下載裡的`gradint.py`，或者歡迎下載[Gradint build environment](https://ssb22.user.srcf.net/gradint/gradint-build.7z)(看看裡面的README.txt)。還有黃冠能所提供的SVN倉儲: `svn co http://svn.code.sf.net/p/e-guidedog/code/ssb22`

還有GitHub的倉儲: `git clone https://github.com/ssb22/gradint.git`

還有GitLab的倉儲: `git clone https://gitlab.com/ssb22/gradint.git`

還有Bitbucket的倉儲: `git clone https://bitbucket.org/ssb22/gradint.git`

## 學術引用

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

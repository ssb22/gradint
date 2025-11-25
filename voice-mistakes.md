# Chinese mistakes in commercial speech synthesizers
From https://ssb22.user.srcf.net/gradint/mistakes.html
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/mistakes.html) just in case)

Commercial unit-selection voices may sound pleasant, but they do make mistakes.  If you use one for language learning, be sure that it is not your only source.  For example [Gradint](README.md) has a function to alternate between different synthesizers on different repeats (it also has a syllable-based voice which should at least be predictable).

To demonstrate the trouble with unit-selection voices for language learning, below are some example Chinese mistakes that I found, usually after just a few minutes of experimenting with each voice.

## Google Translate
(2011-05, using SVOX Yun which is also used by Android)
* 继续学院: The 学 is only half-pronounced.  It seems like they had a recording of a whole 学 but some program played only half of it.  You can’t really hear the ‘-ue’ of the ‘xue’.
* 糖尿病: ‘n’ of 尿 unclear
* 深省: Google correctly says this is “shēn xǐng”, but its voice incorrectly says “shēn shěng” (the voice must be using a smaller dictionary than the transcriber)
* 绝: somewhat unclear when spoken in isolation
## Beijing Infoquick SinoVoice
(2011-05; online trial no longer available)
* 用出来: The main word 用 could be clearer; at least 来 (and possibly 出) should be neutral tone (轻声) but isn’t
## iFlyTek InterPhonic / Bider SpeechPlus
(free trial no longer available)
* bao3zheng4, bian4ming2, fou3ren4, jia3ru2, mei3zhou1, mu4du3, many others (via CSSML pinyin markup): Incorrect syllables spoken (I’d have thought pinyin gives better control but it doesn’t)
## Neospeech Hui
(2011-05, rebranded as ReadSpeaker Mandarin Female in 2019 then back to Hui end-2024)
* 糖尿病: ‘n’ of 尿 unclear
* 奉公守法: first syllable unclear
## ScanSoft (Nuance) MeiLing
(also used by Nokia)
* 深省: 省 spoken as shěng instead of xǐng; no way to add a dictionary entry to override it
* 地, 行 and many other ambiguous hanzi: Engine often gets the wrong reading (e.g. dì instead of de in many adverbs, xíng instead of háng in 十四行诗), no way to override (except sometimes by writing wrong hanzi)
* 邮编: 编 pitch too low for the context
* 切合实际，对: 际 in 切合实际 by itself is correctly pronounced jì, but when followed by ”，对” the 际 seems to pronounced more like jiè (although not so when the hanzi after the comma is different, or when there is no pause before the 对)
* 絶 (variant of 絕/绝), 説 (variant of 說/说) and others: completely skipped, with no indication that there is a missing character in the text
* 用户界面: 界 sounds too much like 3rd tone instead of 4th tone
* 齁声: Pitch falls from B to E-flat.  Some drop in pitch of tone 1 at the end of a phrase is acceptable, but an augmented fifth?  (Compare 中东, 拼车, 伸开, etc)
* 人文学: Faults on 文 (but not in 人文 by itself).  Sounds better if incorrectly written as 人闻学.
* 撞击: 击 sounds like a truncated neutral tone instead of tone 1
* 电脑及资讯科技: something like half a 个 is inserted before the 及
* 劫难: sounds more like jián’àn than jiénàn (it must be a coded exception to 难’s usual nán pronunciation but it seems the syllable boundary is wrong)
* 没有论文登出就垮台: 文 truncated
* 耳闻: ěr sounds like èr
## Microsoft Lili
(couldn’t test but heard a demo)
* 才: spoken as an unclear cǎi instead of cái (the old “MS Simplified Chinese” voice actually gets this one right but gets 央行 wrong)
## Neospeech Lily
(no longer sold separately but used by NextSpeak and ImTranslator 2011-05 without the lexicon access)
* 糖尿病: ‘n’ of 尿 very unclear
* yong4chu5lai5, zhuan3lai2zhuan3qu4 (via pinyin lexicon): Incorrectly read as yòngchūlai, zhuǎilái... but OK if input as hanzi 用出来, 转来转去
* chan3chu2 or 铲除: says chù instead of chú
* shan4yong4 or 善用: shèn instead of shàn in pinyin; “n”s clipped in hanzi
* li4bi4 or 利弊: sounds like bībì
* you2bian1 or 邮编: biān pitch too low for the context
* jia1de5fu1: spoken as jiādìfū (maybe it’s being treated as 加的夫, which might be right but a pinyin override shouldn’t try to guess what the pinyin should have been; what if it came from 家的夫?)
## Loquendo Lisheng
(2011; interactive demo no longer available)
* mu4du3, mu4du4.: both words seem to end in dù (the du3 sounds OK if it’s the last thing in the sentence)
## Apple Ting-ting
(in OS 10.7, retested in 11 and 12)
* 乐: always spoken as yuè even in words like 快乐 and 乐意 when it should be lè (fixed before macOS 11.4; these and other dictionary mistakes—pó instead of fán in 繁体字, etc—are forgivable because the voice can work reasonably well from pinyin)
* mu4du3, mu4du4: Both “du” sounds seem incomplete
* yue4du2: dú fails to rise in pitch
* zhi1 di4: dì sounds too neutral (“fa2 zhi1 di4” is worse as this zhī is high by comparison)
* jing4qi2li3: q sounds like x in this context
* ming2 que4: què glitches in mid-syllable (it’s OK when said in isolation)
* jing1juan4: juan sounds like a garbled jue (can also sound like jue in contexts e.g. jing1juan4ming2)
* chang3kai1: chǎng sounds like a tone 1 higher than the kāi; if doubled to 敞开敞开, the second chǎng is better but is almost a full third tone instead of a half
* kou3 zheng1guo1: guo sounds almost like gua (zheng1guo1 by itself is better except the pitch falls nearly a major sixth)
* cheng2qiang2 tan1ta1: q becomes like x + pitch drop at end
* qu3dai4: tones not clear
* ying3 pian4: n dropped (better in context)

Apple’s Ting-ting was supplied by Nuance (it says so in the PCMWave file) and it sounds like Loquendo Lisheng with different prosody, although Lion’s mid-2011 release was 2 months before Nuance finished taking over Loquendo.  (Pre-releases reportedly used MeiLing instead of Ting-ting.)  Baidu’s 2017 voice sounds identical to Ting-ting.  I can probably claim some minor input to these voices, because in 2008 Loquendo lent me copies of Lisheng and Lingling so I could raise bug reports, which they fixed, but time was limited so we couldn’t catch everything and they didn’t release the voice to consumers.  I don’t know what has happened to it since then.  (Ting-ting’s PCMWave file also contains the string “SCANSOFT” which merged with Nuance in 2005, but it additionally has English rewrite rules that are provably unused by the engine, so perhaps they just tried to merge the codebases.)

## Copyright and Trademarks
All material © Silas S. Brown unless otherwise stated.
Android is a trademark of Google LLC.
Apple is a trademark of Apple Inc.
Baidu is a trademark of Baidu Online Network Technology (Beijing) Co. Ltd.
Google is a trademark of Google LLC.
Loquendo is a trademark of Loquendo S.p.A.
Microsoft is a registered trademark of Microsoft Corp.
ScanSoft and Nuance are trademarks of Nuance Communications, Inc.
Any other trademarks I mentioned without realising are trademarks of their respective holders. 

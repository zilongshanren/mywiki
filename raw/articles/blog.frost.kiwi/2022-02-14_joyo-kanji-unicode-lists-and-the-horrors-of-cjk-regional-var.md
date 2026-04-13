---
title: Jōyō kanji Unicode lists and the horrors of CJK regional variants
url: https://blog.frost.kiwi/joyo-kanji-unicode/
published: '2022-02-14'
source_blog: FrostKiwi's Secrets
source_site: https://blog.frost.kiwi
category: graphics
fetched: '2026-04-13'
---

These files allow you to select or subset just the 2136 [Jōyō kanji](https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji) Unicode codepoints for Japanese. It’s a good middle ground between having only Kana and including the all 21000 characters of the complete [CJK block](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)) for embedded use-cases. How to use these files and how to subset fonts is [covered here](https://github.com/Immediate-Mode-UI/Nuklear/wiki/Complete-font-guide#subsetting-compressing-appending-to-the-binary). Note, that not all HEX codes are 4 digit / within 16-bit, the last one 𠮟 is HEX `20B9F`

. Eyes open, in case your program you use these HEX values in is picky about formatting. It’s a late edition to the Unicode standard [because reasons (article “𠮟る” と “叱る” by @hydrocul)](https://hydrocul.github.io/wiki/blog/2014/1201-shikaru.html) and is thus the only 5 digit HEX Jōyō kanji. The variant 叱 `53F1`

is also listed, since it’s usually the assumed default. ([Archive link in case that article goes down](https://web.archive.org/web/20210405065949/https://hydrocul.github.io/wiki/blog/2014/1201-shikaru.html)).

[Nuklear](https://github.com/Immediate-Mode-UI/Nuklear)Codepoints:[joyo-kanji-unicode-nuklear.c](https://blog.frost.kiwi/joyo-kanji-unicode-nuklear.c)[PyFTsubset](https://fonttools.readthedocs.io/en/latest/subset/index.html)Codepoints:[joyo-kanji-unicode-pyftsubset.txt](https://blog.frost.kiwi/joyo-kanji-unicode-pyftsubset.txt)- Raw-Hex Codepoints:
[joyo-kanji-unicode-unformatted-hex.txt](https://blog.frost.kiwi/joyo-kanji-unicode-unformatted-hex.txt)

## Regional variants [#](https://blog.frost.kiwi#regional-variants)

Finally, the usual applies if your are working with CJK fonts: Double, triple and quadruple check the font’s intended region or in rare cases, how the font file organizes those regions internally. Eg. Google’s Noto [offers their CJK fonts](https://github.com/googlefonts/noto-cjk) in `CJK SC (Simplified Chinese)`

, `CJK TC (Traditional Chinese)`

, `CJK JP (Japanese)`

, etc. Thanks to Unicode’s aweful decision of [Han unification](https://en.wikipedia.org/wiki/Han_unification), regional Sinograph variants are mapped to the same Unicode code point.

When my smartphone didn’t have Japanese set as an optional language, the OS assumed the Chinese variants by default and I was suddenly confused as to why I could not read some “Japanese” words in some apps. Such presumed defaults create issues in many [other](https://community.wanikani.com/t/userscript-anime-context-sentences/54003/83?u=frostkiwi) circumstances as well. Here is the difference with my Anki decks.

![](../../assets/df2915c5b682ee01.png)


Ironically enough, even apple manages to screw this up!

Their Apple calendar app displays Chinese Hanzu, even though the keyboard writes in Japanese Kanji. iOS does not have a secondary language like Android, but both Region is set to Japan and the Keyboard types in Japanese. Having the thing you type change right in front of your eyes is very annoying.

![image](../../assets/76043405f23c22f7.png)


Also same deal with Microsoft teams.![MicrosoftTeams-image (48)](../../assets/db88803479d9cbca.png)
---
title: Common Kanji Character Ranges for XNA SpriteFont Rendering
url: https://theinstructionlimit.com/common-kanji-character-ranges-for-xna-spritefont-rendering
author: Author Renaud Bédard
published: '2010-02-17'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

*Note : This sample is practically useless, because the XNA Localization sample has a much better alternative using the Content Pipeline and character detection from resource files, which works for any language (Chinese, Korean, Japanese…). But I guess if you wanted to get the ranges of common Kanji, here’s how.*

While working on Japanese language support in XNA, I realized a couple of things about Japanese writing (some of which may seem obvious, but wasn’t for me) :

- There’s two broad character sets :
[Kana](http://en.wikipedia.org/wiki/Kana)(syllabic) and[Kanji](http://en.wikipedia.org/wiki/Kanji)(logographic) - Kana has two modern subsystems or components,
[Hiragana](http://en.wikipedia.org/wiki/Hiragana)and[Katakana](http://en.wikipedia.org/wiki/Katakana), each with two distinct Unicode regions of respectively 92 and 95 different glyphs (187 total) - Kanji originate from
[Chinese “Han” characters](http://en.wikipedia.org/wiki/Chinese_character), and are stored within the[CJK](http://en.wikipedia.org/wiki/CJK_characters)(Chinese, Japanese, Korean) portion of Unicode. But CJK characters don’t uniquely reference Japanese logographs, and it contains over 20000 glyphs! - There’s over 10000 actual Japanese kanji, but only about 2000 of which every high-school grade Japanese person should know

In XNA, the [SpriteFont](http://msdn.microsoft.com/en-us/library/microsoft.xna.framework.graphics.spritefont.aspx) class and its associated content pipeline use bitmap fonts internally to cache and render text strings. It becomes obvious that generating a bitmap font with 20000 Han characters would take a very long time, and is also very irresponsible memory usage. Even 10000 characters seems ridiculous.

I wanted to keep using SpriteFonts, so switching to a realtime font rendering option like [FreeType](http://www.freetype.org/) was out of question. So how does one make bitmap fonts usable in Japanese?

While researching the subject, I stumbled upon a whitepaper called “[Unicode and Japanese Kanji](http://www.tonypottier.info/Unicode_And_Japanese_Kanji/)” by [Tony Pottier](http://www.tonypottier.info/), in which he discusses how to isolate Japanese Kanji from the CJK characters, and even dresses a list of all 1946 unique characters that are learned in Japanese education up to grade 7 (sorted [by Unicode point](http://www.tonypottier.info/Unicode_And_Japanese_Kanji/Appendix1.html), or [by learning grade](http://www.tonypottier.info/Unicode_And_Japanese_Kanji/Appendix2.html)). Even if it’s a large amount of glyphs, it’s a lot more reasonable than 10k.

So the only remaining step is to make this table into a a list of XML CharacterRegion elements so that we can use them in an XNA SpriteFont declaration.

I made a little C#3 program that takes a list of Kanji, one per line, and blurts out the expected XML; it also joins the succeeding characters into regions to save space.

using System; using System.IO; namespace KanjiFinder { static class Program { static void Main() { var output = new StreamWriter("regions.xml"); var input = File.ReadAllLines("kanjis.txt"); var writeCount = 0; var intervalsCount = 0; var start = (int)char.Parse(input[0]); var end = start; foreach (var line in input) { var cur = (int)char.Parse(line); if (cur - start > 1) { output.WriteLine(string.Format("<CharacterRegion><Start>&#x{0:X4};</Start><End>&#x{1:X4};</End></CharacterRegion>", start, end)); writeCount += end - start + 1; start = cur; intervalsCount++; } end = cur; } output.WriteLine(string.Format("<CharacterRegion><Start>&#x{0:X4};</Start><End>&#x{1:X4};</End></CharacterRegion>", start, end)); writeCount += end - start + 1; output.Close(); if (writeCount != input.Length) throw new InvalidOperationException(); Console.WriteLine(intervalsCount); } } }

Here’s its input [kanjis.txt](http://theinstructionlimit.com/wp-content/uploads/2010/02/kanjis.txt) (in Unicode format), and its result is ** regions.xml**.

I chose to go up to Grade 7, but one may choose to ignore Grade 7 characters and just do 1-6. I don’t know whether Grade 7 characters are useful in game menus and usual dialogue.

All that’s left is to put those regions in a <`CharacterRegions`> tag inside a .spritefont file, and supply a valid Japanese font! Thankfully, Windows 7 comes with a bundle of these (MS Gothic, Kozuka, Mieryo and Mincho) and the [M+ Fonts](http://en.wikipedia.org/wiki/M%2B_Fonts) offer a public domain alternative.

Apart from the Kanji regions list, a couple more regions you’ll probably need :

<!-- Ideographic Symbols and Punctuation --> <CharacterRegion><Start>　</Start><End>〿</End></CharacterRegion> <!-- Hiragana --> <CharacterRegion><Start>぀</Start><End>ゟ</End></CharacterRegion> <!-- Katakana --> <CharacterRegion><Start>゠</Start><End>ヿ</End></CharacterRegion> <!-- Fullwidth Latin --> <CharacterRegion><Start>！</Start><End>￦</End></CharacterRegion> <!-- and/or the standard Latin set... --> <CharacterRegion><Start> </Start><End>~</End></CharacterRegion>

That’s it! Hope it helped.

I’m currently building an XNA app for a Japanese company and was wondering how I could display error messages on screen in Japanese.

Your method works perfectly and saved me an enormous amount of time. Thank you very very much!

On a side note for anybody wanting to try this: Once all the XML is in the spritefont file the app will take a while to build the first time. Be patient and have fait, this works.

Glad to hear it :)

Thank you very much.

This helped me a lot.

no matter how outdated, it seems to work. the building is taking a while just like mr. allgayer mentioned.

Great! Thanks for help! im building game that shows online high score and i had lot of errors when trying show Japanese language but You helped me ! :)

Does anybody knows how to create spritefont for ALL languages?

Best practice?

I mean there is only 1 font file(.ttf) for 1 language (max is cjk)

but i want to make a full unicode .xnb (for only the string in my app of course) for all languages i support (Arabic, Hebrew, Latin, CJK etc)

so how can i merge all those to one .xnb?

(i thought maybe to add another FontName in the xna xml ) but it’s not working.

also to merge different .ttf to one- but it’s complicated.

so how can i make best practice ONE .xnb for all languages?

thanks.
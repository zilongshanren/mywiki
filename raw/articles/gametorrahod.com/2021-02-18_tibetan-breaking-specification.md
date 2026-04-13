---
title: '"Tibetan Breaking" Specification'
url: https://gametorrahod.com/tibetan-breaking-specification/
author: Sirawat Pitaksarit
published: '2021-02-18'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/34e43b3f4908bf30.png)

Tibetan Breaking is a convention to encode **line breaking opportunities** inside the string data itself, using a [Tibetan](https://en.wikipedia.org/wiki/Standard_Tibetan) interpunct ⟨་⟩ character, called ཙེག་ (*tsek*). ([Tibetan Script](https://en.wikipedia.org/wiki/Tibetan_script)) From now on I will also call ⟨་⟩ the "Tsek".

All strings that does not have white space or similar to hint line breaking should have Tsek and parser should be prepared to remove them from display if they are not intended to print them out, or even better, converts them into real line breaking opportunities that enhances reading experience.

Note that line breaking **opportunity **does not mean it must break at that position like `<br>`

, but it **could.** Presence of this character **also** means it should not break at any other places between characters, save for some punctuations that has language-specific rules.

## Example

`ทุกวันนี้་จ่ายภาษี་ไปเท่าไหร่་ก็ไม่เห็นว่า་ประเทศชาติ་จะพัฒนา་เท่าที่จ่ายไปเลย`

`赤い་甲殻に་身を་包む、火竜とも་呼ばれる་飛竜་リオスの雄。`


## Why should we use this character

- It is inlined with the text. Line breaking opportunities being a single entity (as opposed to range surrounders like
`**`

in Markdown), can be encoded as an accompanying array of integer offsets to the text, so the "clean" text is perfectly readable and editable. But it is now difficult to update the array after modifying the text. Having an actual character in the string is better. Also pairing different data to the string might be difficult to manage. - Almost invisible when you don't want to see, but at the same time visible when you want to edit them. This is better than thin character like a pipe
`|`

where it may not take much space, it is obtrusive to read. And better than a completely invisible character like the[Line Separator](https://www.compart.com/en/unicode/U+2028)(Sometimes that even show up as a tofu box.) where it is difficult to notice that you are editing over them. (e.g. Pressing backspace and nothing happen, so that means you are deleting this invisible character.) [Middle dot](https://www.compart.com/en/unicode/U+00B7)`·`

character is almost as good, but Tsek has an advantage that it is usually not present in most monospace fonts. It then falls back to a font that is not monospace, making it ideal in code editor because it stays small.- In online Localization collaboration platform, you don't need any special features to manage the line breaking opportunities. You may add a tag that Tsek is present to save processing cost for strings that does not have them at the destination.

## Disadvantages

- You likely cannot type from keyboard, but having to copy paste it.
- If you are making a string of an actual Tibetan language, then the parser needs to know to print them literally rather than process them...

## Relationship with other markup languages

[Markdown](https://en.wikipedia.org/wiki/Markdown)'s success came from it using a very humane markup format. We can both encode different highlighting that make different on the destination media, and also can read it aloud and feels like it has the same "highlighting" effect.

Tibetan Breaking is the same as Markdown that we are directly encoding more information inside the text. However for presentation, line breaking is naturally invisible so it make sense that this encoded information is the most invisible as possible when we read it in plain text editor. You can have Tibetan Breaking and Markdown together.

Tibetan Breaking is different that it use a single character Tsek, not surrounders like most of Markdown's syntax.

HTML-like "enriched text" format can sometimes encode a single entity (e.g. `<br>`

) or surrounders (e.g. `<strong>asdf</strong>`

) but neither are pleasant to read.

## The need for explicit line breaking opportunity

[Google's Budou](https://github.com/google/budou) documentation explained this very nicely.

English text has many clues, like spacing and hyphenation, that enable beautiful and legible line breaks. Some CJK languages lack these clues, and so are notoriously more difficult to process. Without a more careful approach, breaks can occur randomly and usually in the middle of a word. This is a long-standing issue with typography on the web and results in a degradation of readability.


In many places like website, text processor, game engine, etc. the "breakable at white space but not in between other characters" are **hard coded**. In east Asian characters, there are [more characters](https://en.wikipedia.org/wiki/Line_breaking_rules_in_East_Asian_languages) hard coded to be breakable. They can also be limited to not be able to use at the start/end of line, so it works together with line breaking code.

One more hard-coded behaviour is that if CJK language is found, suddenly it is breakable at **all **characters. You absolutely don't want to allow this for English. But in CJK if you don't allow this, strings of character without any hints of space can easily exceed the line. They can't break intelligently semantically like human do either, so they must settle for this simple but not optimal break at all characters.

Other than this, many languages wants to break mid-strings but of course **not anywhere**. In Japanese, a string of kanjis can be broken into words with different meaning than intended, sometimes even 1 kanji is readable. In Thai, there are more chance to create a word that is readable cross-line but is not optimal as there is a long pause before your eye scan to the beginning of the next line.

### Critical for responsive media

Unlike physical media like signs, strings can used in dynamic media. Line breaking tied with the width of that media. Nowadays websites could be viewed on mobile device. Even a smartphone games can be responsive to the device's screen and provide longer or shorter line depending on device, or even orientation you play on.

Here is an example from Budou's project page. モバイル (Mobile) and チーム (Team) should absolutely not be broken, but the algorithm is set to "breakable at every character" by default for Asian language. At the same time, we can't sneak in white spaces in Japanese language to hint the browser. Without manually marking line breaking **opportunity **you don't know at which width it will gives the reader sub-optimal experience.

![](../../assets/444e09f286ec2338.jpg)

[google/budou: Budou is an automatic organizer tool for beautiful line breaking in CJK (Chinese, Japanese, and Korean). (github.com)](https://github.com/google/budou)

Even the text above of this very blog broke in an unfortunate place at a certain screen size! Look at that unfortunate `ーム`

at new line that is not even readable...

![](../../assets/d54b3b5f7ec0eed0.png)

Here is an example from Unity game engine, the default behavior which is the same as website. Each character is completely independent and breakable. Imagine the changing boundary as various phone size.

![](../../assets/78bfe323c7e37127.gif)

An ideal result :

![](../../assets/fbfcee32e1bcc9ba.gif)

### Technical fixes is possible after having Tsek

This goes a bit beyond the purpose of this article but just for completeness. Supposed we had encoded Tsek in the text. How to decode them to use in the destination media?

On website, if you use Budou's way you can wrap each "chunk" in `<span>`

with a class `display: inline-block;`

, then all chunks inside an another empty `<span>`

. (Though, Budou tries to use machine learning to automatically place breaking opportunity. Tsek has real human place them manually.)

An another way is to have the parent with

to cancel out the built-in "break anywhere" of Asian language then place [white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space): nowrap

inside the HTML. Be careful if you use [<wbr>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/wbr)`white-space: no-wrap`

with English it will cancel out the already great white space breaking. So you need to be selective of languages. With this convention, you can check existence of Tsek character to activate `white-space: nowrap`

without knowing what language it is.

Also, `<wbr>`

simplify processing since you just replace Tsek with it. If you use `<span>`

wrapping, it could be a problem when you have Tsek in the middle of interleaving surrounders that also needs to be processed.

In other system like game engine that supports "rich text" like Unity, you may wrap each chunk in something like `<nobr>...</nobr>`

(non-breaking text) to counter the breakable anywhere rule of CJK language. Then in-between, ensure it is breakable with `<zwsp>`

(zero-width space) to silently add hints to CJK language which has no hint before.

In summary, all these technical fixes while usable, are absolutely not ideal to be encoded directly in the text as they are horrible to read and edit, and interferes with good encoding like Markdown.
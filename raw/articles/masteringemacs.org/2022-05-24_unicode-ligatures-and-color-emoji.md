---
title: Unicode, Ligatures and Color Emoji
url: https://www.masteringemacs.org/article/unicode-ligatures-color-emoji
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Emacs 27 adds a lot of interesting [new features](https://www.masteringemacs.org/article/whats-new-in-emacs-27-1), yet few people paid much attention to the introduction of Harfbuzz, a text shaping engine, as the subject is, well… a bit dull. And yet it’s one of the more expansive new additions for two simple reasons: color emoji and ligatures.

I suspect that you’re either very interested at this point or maybe a bit puzzled why this matters at all. I think both viewpoints are fair: it’s hard to get excited about color emoji in your text editor unless you’re a Javascript developer. And yet the change presages more than just color *emoji*. Indeed the change obviously works with any glyph you can represent in a font, and that means you can now render colorful graphical glyphs and icons from fonts instead of relying on bitmaps and other nasty hacks in Emacs. That itself is a good thing.

The other benefit is typographic ligatures — and not just the classic ones you see in [high-quality, typeset books](https://www.masteringemacs.org/book). As it happens, there’s a growing trend in modern programming fonts to add ligatures for common programming constructs such as symbols, operators and so on that render in more – though debatable – aesthetically pleasing ways.

Here’s an example from [Cascadia Code](https://github.com/microsoft/cascadia-code):

Pay close attention to `www`

, the comment and the closing title element. Using Emacs’s new ligature support they are now rendered with special glyphs present in the font.

It’s a nice feature. I do find that some of the symbols that (Cascadia Code, in this case) use hinder readability rather than aiding it. But that’s entirely about taste. Other, modern, editors have had this for a while as their display engines are newer than Emacs’ engine.

If you’ve been around Emacs for a while you are probably thinking: “Hey wait a minute. We can already compose characters!” And you’re not wrong. More than a decade ago I pinched a snippet of code from Emacswiki that composed the word `lambda`

into `λ`

and I’ve been lugging that snippet around ever since. In recent Emacsen it was formalized as `M-x prettify-symbols-mode`

to aid with just such a thing, and it uses a similar technique: composing one or more characters into another.

So what’s the difference?

I’m definitely missing a few nuances here (and I’m sure Eli Zaretskii is busy heaving old Unicode consortium references into his trebuchet for not getting the details exactly right!) but the gist is that with ligatures the text shaping engine works *with* the font to ligate clusters of graphemes (or “characters”), and that means that as you compose more and more characters the text shaper adapts the preceding characters to match whatever the font wants that stream of characters to look like.

Contrast it with `M-x prettify-symbols-mode`

(or the preceding snippet I and many others still use) that simply looks at a stream and replaces it with a Unicode code point that may or may not use the same font. Yeah - not the same font, that’s right. If your current font is unable to display a Unicode code point Emacs’ll try to find another font that will (and more on optimizing that later.)

So one question remains: why is it a checkbox in other editors and a major *tour de force* of elisp code in Emacs to make it work?

The reason for the need to specify individual ligatures in Emacs is a curious one, and I am at this point not entirely sure why nobody made it easier to do so out of the box in Emacs 27. Fonts that support ligatures come with detailed metadata describing – to all who may care – how to ligate text; use swash or small caps; old-style numerals, you name it.

In Emacs you would typically use really obscure functions like `set-fontset-font`

, `font-spec`

, etc. to define how Emacs displays character ranges and which font to use. That means you can tell Emacs to render Latin characters with your default workhorse font, and use your artisan font for domino tiles and musical notation.

## ligature.el

So how do you activate ligatures in your code, then? If you’re using VSCode or another editor then you click a button and hey presto – ligatures! Yeah, well.. that’s VSCode. We don’t work that way in Emacs land.

Currently there are only a few scattered snippets of code that turn this feature on, but each of them come with a number of usability issues that I think would annoy people. So I sat down and wrote a package that does it all for you.

For now I’ve added support for one font, but adding more – as you’ll see – is easy. You just need a list of the ligatures you want to use and the modes you want to use them in and you’re ready to go.

The package, [ligature.el](https://github.com/mickeynp/ligature.el), comes with pictures and installation instructions. One word of warning, though: you’ll need Emacs 28 to truly use it, due to a couple of gnarly issues in Emacs 27. So that *Matlock* stageplay you’re working on? Save it first before you proceed.

So yeah, anyway. The package lets you pick which ligatures to use where; unlike other editors, you can pick when you want to ligate a buffer or a major mode. That may not sound important, but some fonts come with a large amount of ligatures, and not all of them are easy to read or even desirable. You would likely find them unwanted in `M-x shell`

, for instance, but appropriate in your favorite programming modes.

If you like the package, then leave feedback, please. I intend to collate all the various ligature modes and configurations into a wiki and maybe even into the package at some point.

## Rendering Color Emoji

Finally, there is the issue of color emoji. Emacs has always had stellar unicode support out of the box, but if you ever want to *change* those configurations, you’ll find yourself staring into the Abyss. It’s a dark art.

For instance, with a Harfbuzz and Cairo builds of Emacs 27 (and that should be the norm for most) you won’t get color emoji (or any other symbol that has a color palette) because your default font probably doesn’t come with that. You may also prefer the emoji styles from a particular font. There are endless tables of Unicode blocks that Emacs maps to fonts to maximize readability and correctness, but if you want to *change* them, well.. that’s where things get tricky.

Luckily, the hard work is mostly done for you. Enter `unicode-fonts`

, a package that rejigs the internal tables Emacs uses to pick better fonts for unicode codepoint ranges.

To install it is easy:

```
(use-package unicode-fonts
:ensure t
:config
(unicode-fonts-setup))
```


**NOTE**: I’m experiencing some issues with this package in Emacs 28. We may have to wait for someone to take up the mantle and update it.

The package will then compile the right settings given your fonts. It may take a little while. I highly recommend you read the documentation, though. There’s a lot of useful information.

By default it’ll set dingbats and emoticons to use a variety of common emoji fonts. And because the package is well-made, it’s trivially easy to configure to your liking by typing `M-x customize-variable RET unicode-fonts-block-font-mapping RET`

. You can scroll down to emoticons – or any other category – and control the fonts Emacs must use for that particular Unicode block.

If you’ve ever had issues with Emacs rendering some unicode characters with the wrong font, this is a good package to use. It’s easy to configure and set up, and its defaults are sensible. And if you dislike what it does, simply disable all or parts of it.

## Conclusion

Improved text shaping and rendering is going to make a big difference going forward, but I really wish they made it easier to enable OTF styles. Despite my best efforts, I was not able to convince Emacs to use style sets or substitutions – that predefine things like ligatures – so instead I had to resort to a method that is some ways better (more flexibility) and yet it requires more effort to work. But that’s Emacs for you. Unparalleled flexibility and power.

Finally, I want to say that the color glyph support is a useful addition. There’s a growing contingent of Emacs users that find it empowering to build functional, but visually attractive, packages and themes in Emacs and this change is a good step in the right direction in the age of high dpi screens. As text permeate everything we do in Emacs, textual vectorized color glyphs will soon replace the rather awful bitmaps that lurk in Emacs’s many dusty corners. It’ll improve readability and, perhaps more importantly, signal to future Emacs users that Emacs does move with the times. I’m very happy the maintainers took the time to integrate such a feature and I commend them for staying on top of the text editing zeitgeist.
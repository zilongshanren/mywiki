---
title: Inserting Emoji with Input Methods
url: https://www.masteringemacs.org/article/inserting-emoji-input-methods
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Although Emacs 28 is out now, there’s a few interesting emoji additions in the upcoming Emacs 29 that I want to talk about now. You see, Emacs 29 adds builtin support for inserting emoji. Now, if you’re familiar with `C-x 8`

and friends as a way of inserting infrequently used symbols then it’s basically adding on to that. There’s also a Magit-style interface to insert emoji. It’s all pretty cool, but it got me thinking…

Way back in the day I wrote about [Input Methods](https://masteringemacs.org/article/diacritics-in-emacs) as it’s a really, really cool way of modifying your keyboard input to support languages that you wouldn’t ordinarily be able to type with your keyboard layout.

For instance, if you’re an occasional German speaker, you can type `C-u C-\`

and then pick `german`

from the list.

If you’re a LaTeX user I recommend you play around with the `TeX`

input method. You can use LaTeX commands to insert the equivalent symbol in non-LaTeX buffers. Try `C-h I TeX`

and you’ll get a really nice table of key sequences you can type and the symbol it’ll output.

Anyway. Input methods use a simple chord system to map a set of keys to a character. But it’s flexible, and you can do just about anything with it. Even emoji.

```
(quail-define-package
"Emoji" "UTF-8" "😎" t
"Emoji input mode for people that really, really like Emoji"
'(("\t" . quail-completion))
t t nil nil nil nil nil nil nil t)
(quail-define-rules
(":)" ?😀)
(":P" ?😋)
(":D" ?😂)
(":thumb:" ?👍))
```


Here’s a simple example. When you’ve [evaluated the elisp](https://www.masteringemacs.org/article/evaluating-elisp-emacs) you can enable it with `C-u C-\`

and then pick `Emoji`

. Feel free to change the source locale from `UTF-8`

to whatever you prefer. You can also pick your own mappings, and you’re not limited to `:`

as the start symbol either.

Now you can type `:`

and either `TAB`

to get a list of known completions or `C-h I Emoji RET`

to see a full list. You’re also presented with a little auto complete dialog in the echo area. Typing `:)`

thus yields 😀. You can toggle the input method on or off with `C-\`

— it’ll remember your last selection.

Pretty nifty! And if you’re a frequent user of emoji, possibly an easier way of inserting them. And, I hasten to add, you’re not limited to emoji. You can map just about anything.
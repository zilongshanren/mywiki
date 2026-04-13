---
title: Text Expansion with Hippie Expand
url: https://www.masteringemacs.org/article/text-expansion-hippie-expand
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Let’s talk about dynamic text expansion, but not the kind you may already know about. Dynamic text expansion is something Emacs does well, and you may have heard about two of Emacs’s builtin ones: *Skeletons* and *Tempo*. A common third-party tool is *Yasnippet*. The third (but very useful) *abbrev* is much simpler than either of those, preferring to silently replace one word with another, making it a useful tool for auto-correction and fixing typos. I use *abbrev* heavily; and so should you.

*But*, that’s not what I’m going to talk about. I’m here to talk about *Dynamic Abbrev* – zero relation to my good friend *abbrev* – and its talented cousin, *Hippie Expand*.

*Dynamic abbrev* is bound to `M-/`

and `C-M-/`

. When you call `M-/`

, it will expand your word at point to one of a number of different expansions sourced from either your current buffer, or all buffers. Its job is to help with repetitious data entry, or to jog your mind if you forgot the exact name of something. Unfortunately, it’s rather bad at its job: it can ably complete words found in your buffers, but not much more than that.

You see, for nearly 30 years, Emacs has had a well-kept secret. It’s called *Hippie Expand*. It’s everything *Dynamic Abbrev* should’ve been, if only the latter had tried harder in school. It’s surely also a better default than the current one, but I won’t hold out hopes of the default changing. It’s been this way for decades; it’s unlikely to change now.

So let’s right this injustice:

`(global-set-key [remap dabbrev-expand] 'hippie-expand)`


And now you can press `M-/`

and invoke `hippie-expand`

instead. Feel free to pick a key binding of your choosing if you don’t like the default.

So what’s different about it? Well, you can have a look at `C-h v hippie-expand-try-functions-list`

to see a list of completers it’ll use. `M-x apropos-function RET ^try- RET`

will show you a reasonable guess of all available completers.

As you cycle through matches with `M-/`

, hippie expand tells you where it’s drawing its matches from in the echo area.

But how about a few examples?

- File Names and File Paths
The first is its uncanny ability to complete filenames and file paths. Simply start typing a path in your buffer – any buffer will do – and type

`M-/`

. Hippie will attempt to either partially complete a filename or path, or walk through all possible matches with successive calls to`M-/`

.This alone makes it great. If you ever find yourself wanting to insert a filename or path you can use hippie to help you.

- Expanding a whole line
This may not seem useful, but if you ever find yourself having to repeat a line from earlier, you can ask hippie to auto complete it. Just start typing the beginning of the line, and let hippie take care of the rest.

- Completing “lists”
This one’s a bit nebulous and hard to explain, but hippie’s capable of ‘detecting’ lists and list-like entries. Consider:

`int foo(int a, int b) { } int bar(-!-`

With point at

`-!-`

, hippie’ll expand to`(int a, int b)`

when you type`M-/`

. That makes it really useful for, say, repeating function arguments or other bracketed structures. Try successive expands to cycle through the options.- Switches and Keywords in
`M-x shell`

or`M-x eshell`

Not really a completer

*per se*, but more of a benefit of its word completers (drawn from*Dynamic Abbrev*). But I find it useful to expand`--some-long-argument`

simply by typing in parts of it. Great if you can’t quite remember the name of a switch in a mile-long shell buffer of output. Because hippie will only expand things it’s actually seen, it’s also a pretty iron clad way of testing if you fumbled the name completely and it doesn’t know what you’re on about.- Elisp Symbols
Unsurprisingly, it can also do this. Start typing a symbol and it’ll auto complete it. It, again, works everywhere. Like in the minibuffer or in a complex form you’re writing in

`M-:`

.It’s so ingrained in my workflow that I completely forget I’m using it.

- From your Kill Ring
So you can recall stuff from your kill ring if you have previously killed something into it.


Now a lot of people will go, but yeah, OK, I’m using Company mode and/or LSP — and yeah, the former can draw from the same sources of information (and indeed does to an extent.) But LSP won’t save your bacon when you’re trying to complete something in a README file. Hippie will, though.

So the next time you’re trying to write out a filepath in a string or shell script, give Hippie Expand a try. You’ll quickly end up using it for lots of things once you’ve picked up on the cues you need to give it to tease out the completion you want.
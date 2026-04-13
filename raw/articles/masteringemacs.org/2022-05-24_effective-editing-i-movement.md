---
title: 'Effective Editing I: Movement'
url: https://www.masteringemacs.org/article/effective-editing-movement
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you can master movement and editing in Emacs, you have effectively conquered two of the biggest productivity boosters available to you. Emacs has unrivaled movement and editing capabilities. Few other things in Emacs will, pound-for-pound, give you a bigger productivity boost.

## Overview

Emacs has grown organically – some might say uncontrollably like kudzu – over its more than 40 year history, and in that time it has been honed and sharpened as a tool for effective text and source code editing. I’ve met lots of IDE users who use the mouse to edit text or access menu options, even though – and they realize this – it is very ineffective. But old habits die hard, and when your IDE’s most advanced text editing capability is a poorly-emulated *Brief* mode it’s no wonder people can’t be bothered.

The best way to maximize your productivity is to eliminate common bottlenecks like learning how to touch type and, of course, mastering Emacs. Editing text effectively can take a while to learn, as there are many specialized tools available to you to make your life easier. I’ve been using Emacs for a long time and I still learn new ways of doing things faster; but ultimately it is tenacity and persistence that will pay off in the long run.

Included in this series will be code snippets, suggestions for rebinding keys and other tips and tricks I’ve picked up over the years. You may not want to use all of them – which is fine – but I will try to highlight the importance of switching or changing something to give you an idea of how much of an improvement it is.

## Command Arguments

### Universal Argument

This concept deserves a mention as it will invoke an extended, and typically more complex, version of a command *or* it will default to the numeric argument `4`

, meaning it essentially does the same as though you had typed `C-u 4`

. The *universal argument* (also known as *prefix argument*) is multiplicative when invoked repeatedly.

### Numeric Argument

The *numeric argument* is so called because it lets you pass a numeric constant to a command. What the number is for used for depends entirely on the command you use it on. For `C-p`

it moves up *n* lines, for other commands it does nothing. It all depends. Most commands do what you would expect.

Because numeric arguments are so useful they are bound to a multitude of keys: `M-0`

to `M-9`

; `C-0`

to `C-9`

; `C-M-0`

to `C-M-9`

and `C-u <num>`

.

By duplicating the same command multiple times, you don’t have to move your fingers to execute a command that uses `C-`

, `M-`

or `C-M-`

. So to run the command `forward-word`

, bound to `M-f`

, 10 times you’d type `M-1 M-0 M-f`

.

Simple things like duplicate keybindings cut down on finger-straining typing and it increases the likelihood of people actually *using* numeric arguments in the first place. Odd or hard to reach keys are used less – empirically, it is not a difficult conclusion to reach.

### Negative Argument

When used with the numeric argument, the *negative argument* inverts the operation the command would otherwise carry out.

Like numeric arguments, the negative argument is bound to multiple keys to minimize unnecessary finger movement. It is bound to `M--`

(that’s meta followed by a dash); `C--`

; and `C-M--`

.

Negative arguments are very useful, for they can let you operate on words, lines or phrases you have just finished typing. If you want to capitalize the last word you just typed, type `M-- M-c`

. Not all commands have an inverse, or they do unexpected things – particularly if it is a third-party command – but almost all the keys I’ll be talking about in this series will work with a negative argument.

## Basic Movement

If you’re an experienced Emacs user, all of this should be muscle memory by now, but I have to start somewhere and the beginning is the best place.

Emacs does support the navigation keys (arrow keys and pg up/down and so on) but it’s better to learn the real Emacs keys. Every time you take your hand off the “home row” to use the navigation keys you are wasting time – time that adds up, considering how often you move around in code or text. A good Emacs hacker constantly moves and edits, and in rapid succession: it is folly to stop, start, stop, start every time you navigate the buffer.

### Fundamental Movement Keys

The four fundamental movement keys are `C-n`

, for next logical line; `C-p`

, for previous logical line; `C-f`

for move forward by character; and `C-b`

for move backward by character.

I recommend adding this to your .emacs, as it makes `C-n`

insert newlines if the point is at the end of the buffer. Useful, as it means you won’t have to reach for the return key to add newlines!

`(setq next-line-add-newlines t)`


The move to beginning and end of line commands bear mentioning as well, as they are also a crucial part of movement. To move to the beginning of a line, type `C-a`

; to move to the end, type `C-e`

.

## Extended Movement

It is rarely efficient to use the fundamental movement keys if you are moving the point more than a few characters. It is at this stage that you will have to make a judgment call and decide what the *fastest* way of getting to where you are going is.

### Movement by Word

The keybindings for movement by word in Emacs is almost the same as that of movement by character, but instead of the prefix `C-`

it is `M-`

. To move forward one word use `M-f`

; and to move backward one word use `M-b`

.

Movement by word will make up the bulk of your intra-line movement. It pays to understand why it works the way it does, and to understand that, you must know what a *word* is.

#### Definition of a Word

What a word is is governed by the *syntax table*, an altogether fascinating topic that deserves its own article at some point. But keeping it simple, the syntax table governs how Emacs treats almost every character – Unicode as well – and what its role is when a function like `forward-word`

is run.

For most things – particularly source code – a word is almost always alphanumeric, possibly with a few other characters like underscore. It may seem counterintuitive to have a fluid definition for what a word is, but if you think about it, it makes perfect sense: what you consider a word when you’re writing text may not be the same as when you are writing code, and the definition of, say, a variable may also differ between languages.

### Movement by Paragraph, Sentence

Movement in Emacs is not limited to just characters and words. If you are frequently writing text, the `forward/backward-paragraph`

and `forward/backward-sentence`

will come in handy. To move by sentence use the handy keybinds `M-e`

and `M-a`

. The paragraph keys are bound to the less-than-helpful `C-down/up`

navigation keys.

What is considered a *paragraph* is governed by variables like `paragraph-start`

and `paragraph-separate`

. The same holds true for a *sentence*, but it uses `sentence-end`

(a function *and* a variable) to determine what a sentence boundary is; the boundary is usually a full stop followed by one or two whitespaces.

### Scrolling

You can also scroll by “page” (and what that means deserves its own article) with `C-v`

to scroll down, and `M-v`

to scroll up. I use the word *scroll* here because the concept of a *page* in Emacs is not what it is in other editors. But I doubt anybody cares if you refer to it as page up or down, something I often catch myself doing.

The command `C-M-v`

also bears mention, as it scrolls the *other* window; what *other* is depends on how many split windows you have open (if you do) or frames (if you don’t). This key is very, very useful if you are reading documentation in another window or frame and you want to scroll it without the hassle of switching to that other window. Incidentally, there is only one command to scroll the other window, and that is the one I mentioned before; to scroll backwards, use the *negative argument* first.

### Move to Beginning/End of Buffer

Use `M-<`

to move to the beginning of the buffer, and `M->`

to move to the end. The buffer jump commands are useful for they leave the mark at the originating position, meaning you can jump back to where you came from with `C-u C-SPC`

. I recommend [reading my article on the mark commands](https://www.masteringemacs.org/articles/2010/12/22/fixing-mark-commands-transient-mark-mode/) as it will show you how to make the mark commands more useful.

## Advanced Movement

Advanced movement commands are meant to augment the basic commands I described above. What makes them advanced is that they require a bit more forethought before use as their functionality is *context-aware*. The movement keys described here are what makes Emacs stand out from most other editors; it is most important that you work the commands into your daily work-pattern as it will greatly speed up movement and, thus, editing.

### Movement by s-expression

Moving by s-expression is a little misleading (unless you edit *Lisp* in which case the name is apt) as what it *really* means is *movement by balanced expression*. A balanced expression is, like moving by word, subject to the syntax table, but common examples are quotes (`' '`

, `" "`

) and brackets (`[ ]`

, `( )`

, `{ }`

, `< >`

).

Movement by s-expression is similar to movement by character and word, only the prefix is `C-M-`

. So move forward is `C-M-f`

and backward is `C-M-b`

.

Moving by s-expression will take a bit of getting used to, but you will quickly find that it is a more effective means of navigating source code than by word or character. A lot of the things we do in development is deal with quoted strings; expressions in parentheses; and even regular text and code. Ignoring quotes and parentheses, moving by s-exp is still useful for everyday navigation as `forward/backward-sexp`

will treat a larger swath of characters as part of one “unit”. So what that basically boils down to is that it is more *intelligent* in grouping the letters together into meaningful chunks for you to move around by. Use it for a while – replace movement by word for a while if you have to to learn how to properly navigate by s-exp. You’ll thank me for it. I promise. Really.

### Moving In and Out of Lists

Like the commands to move *past* a balanced expression, Emacs also lets you move *into* one. The list commands were obviously meant, again, for Lisp-likes but they serve their purpose well in other languages.

To move into (down) a list type `C-M-d`

; to move out (up) a list type `C-M-u`

. When you move down Emacs will pick the nearest group of balanced parenthesis and move into those; if you wish to move into, say, a neighboring pair you must use…

If you get a scan error it is because you are in a position where Emacs cannot determine how to carry out what you are trying to do.

### Moving Forward and Backward in Lists

Moving forward and backward are niche-level commands indeed, unless you write a lot of Lisp. They work in much the same manner as moving in and out of lists, although they move forward or backward to a neighboring pair of parentheses that share the same depth.

## ISearch

Learn to move around the buffer with isearch (`C-s`

or `C-r`

; `C-M-s`

for regexp-aware isearch); it’s an incremental search engine in Emacs that looks as you type. It has myriad features (type `C-s`

followed by `C-h C-h`

to see them all) but the most important ones in isearch mode are `C-w`

(to add the word after point to); `M-y`

to yank the text; `C-r`

to reverse the search direction; `M-c`

to toggle case sensitivity folding and `M-n`

/`<-p`

to go through the history of past searches.

Isearch is a superfast way to get around in the code, and if you are often looking for words in source code, I would recommend the ever-useful `isearch-forward-word`

(`M-s w`

) to “fuzzy-find” matches in the code. It cleverly ignores things like punctuation as it looks for *whole words* instead. Super-duper Useful.

Oh, one more tip: if you type `C-s C-s`

it will repeat the last searched query.

## Back to Indentation

If you’ve ever typed `C-a M-f`

or something to that effect to move the point past the whitespace on a line then good news! There’s a better way. In Emacs the command `back-to-indentation`

moves point to the beginning of the line and moves forward past all the indentation. The command is bound to the easy-to-reach key `M-m`

.

## Registers / Bookmarks

You can use Emacs registers (and the bookmark functionality) to store the location of the point. If you only care about transient storage (that gets lost on Emacs exit) you should use registers; should you desire something more permanent then perhaps bookmarks are what you want. Bookmarks and registers both introduce a myriad features that I’ll introduce in a later article, but the commands that affect movement are `C-x r SPC`

to store point in a register and `C-x r j`

to jump to a point stored in a register.

The bookmark functionality in Emacs is very flexible and lets you do much more than simply storing and retrieving a point location. To use the bookmark functionality to store, retrieve and list bookmarks type `C-x r m`

to save a named bookmark; type `C-x r b`

to jump to a named bookmark; and `C-x r l`

to list all bookmarks.

## The Mark

The mark commands in Emacs are used to not only define one part of a region (the other being the point) but they are also used as a form of *transient beacon* that you can recall the point to. This functionality is very useful, as there are several movement commands in Emacs that set the mark, like moving to the beginning or end of a buffer, say.

My [article on the mark commands](https://www.masteringemacs.org/articles/2010/12/22/fixing-mark-commands-transient-mark-mode/) will tell you how to optimize the use of the mark commands if you use transient mark mode, as sometimes *tmm* will get in the way of using the mark as a *transient beacon*, and not just as a boundary for the region.

The commands that most interest you as far as movement is concerned is `C-x C-x`

to toggle between the point and the mark in the buffer. If you yank text, you can exchange the point and mark to jump between the beginning and end of the yanked text.

Another useful command is the command to jump to the head of the mark ring (subsequent calls will cycle through the other marks in the buffer’s mark ring) and that command is `C-u C-SPC`

. It bears mention that my aforementioned article suggests binding this useful command to `M-`

.
Jumping to the mark is useful, but explicitly setting it is just as useful, and this is where *tmm* can get in the way: the command to set the mark is C-SPC` (note that there is no universal argument here) but that will also activate the region – very annoying. Again, my article above has custom code that will set the mark but not activate the region.

The mark is invisible by default, but I use a cool module called *visiblemark.el* that makes, well, [the mark visible](http://www.emacswiki.org/emacs/VisibleMark).

## Repositioning Point

You can move the point between the top, center and bottom (by default) of the visible window but without actually scrolling up or down. The command is sometimes useful if you want to reach text in one of the previous three areas, although you can configure the variable `recenter-positions`

to change that. The command is bound to `M-r`

which makes it very easy to reach and thus use.

## Imenu

Imenu is a useful and extensible tool in Emacs that lets you jump to key areas of your buffer, most usually functions definitions in source code. Unfortunately, the imenu is marred somewhat by no default key binding (`M-x imenu`

to invoke) making it less known than it should be; another negative is that it uses the standard completion mechanism which is terrible for quickly navigating by “feel”.

I use [a super-charged ido version of imenu](http://www.emacswiki.org/emacs/ImenuMode#toc10) and bind it to the `M-i`

key:

`(global-set-key (kbd "M-i") 'ido-goto-symbol)`


## TAGS and Cross-Referencing

Nowadays, you’re better off outsourcing TAGS interaction to `xref`

, Emacs’s unified cross-referencing system. It’s a generic interface that can plug into a number of backends. By default it’s bound a number of common keys that used to be the preserve of just TAGS. The key bindings include: `M-?`

, `C-M-.`

, `M-,`

and `M-.`

.

A full list of these commands can be found with apropos: `C-h a ^xref-`

.

If you’re looking for a tool that can cross-reference and find definitions across your source files, you should consider LSP (either EGlot or LSP-Mode), and/or combine it with a tool like [dumb-jump](https://github.com/jacktasia/dumb-jump) that attempts to find the definition of something using external tools like `grep`

(though I strongly encourage you download `ripgrep`

as it’s much faster.)

## Goal Column

If you find yourself editing multiple lines in a row – perhaps in a macro – you may want to change the default column the point moves to when you change lines; naturally it will only do so if it is possible. This functionality is called *goal column* and it’s bound to `C-x C-n`

(`C-u C-x C-n`

to disable).

## Subword Mode

Editing code `WithCamelCaseWritingLikeThis`

is frustrating in part because Emacs treats a camelcased identifier as a single word. The good news is, though, that Emacs has something called `subword-mode`

(called `c-subword-mode`

in earlier Emacsen) that rewires the movement and edit commands to work on CapitalizedWords.

## Smart Scan

A long time ago I used an IDE feature that let you quickly search up or down for whatever identifier the point was on, and I decided I wanted something like it in Emacs so I wrote the code snippet you see below. Now, it’s perfectly possible to do what it does with isearch but I use the code as it avoids the hassle of fidgeting with isearch to get the term under point into the search field.

In the code below the commands are bound to `M-p`

and `M-n`

.

Smart Scan’s main advantage over isearch is that all you need to do is move the point to whatever identifier you wish to search for and then press `M-n`

to find the next match in the buffer. The main use is not that you go “looking” for the identifier you wish to search for first: you are probably better off using isearch then; no, the main advantage is when you’re already writing code – or stepping through it with a debugger – then smart scan will beat out isearch.

Smart Scan is also clever enough to ignore comments and strings containing the identifier you are looking for.

You can download [Smart-Scan from Github](https://github.com/mickeynp/smart-scan).

## Goto Line

Emacs does, of course, support jumping to a specific line, and it is bound to two commands: `M-g g`

(that everybody seems to use), and the easier-to-type `M-g M-g`

. The goto command is smart enough to default to whatever number point is on when the command is invoked, which will come in handy if you combine it with the command `C-u M-g M-g`

, which executes `goto-line`

in the *previous* buffer – that is, the buffer you just came from. The use case is if you switch to a buffer – say, a shell or output window – and you want to jump to a line in the buffer you just came from.

One important thing to note when using `goto-line`

is that, if the buffer is narrowed the goto line command still counts from the first line of the buffer, rather than the first line of the *narrowed* buffer.

## Next / Prev Error

If you use the compile mode (compile mode is also used for things like `grep`

and `occur`

) in Emacs you will, for free, gain the ability to jump to the next/prev error in that compile buffer by invoking `M-g M-n`

and `M-g M-p`

for next and previous error, respectively.

## Beginning / End of Defun

Despite the cryptic Lisp name for a function, the functions `beginning-of-defun`

and `end-of-defun`

works great with most programming modes in Emacs, by jumping to the beginning (duh) and end of the function/class definition point is contained in.

The commands are bound to `C-M-a`

and `C-M-e`

making them very easy to reach and use, and they will definitely make editing your code easier.

## Conclusion and Next Steps

Emacs has a staggering array of commands that makes moving around your buffer much, much easier; of course it’s easier said than done to learn all of them and make them part of your day-to-day life, but if you start slow and incorporate one command at a time then before long you will be speeding through text and code.

But this article’s really just a small sample of what you can do with Emacs — and it does not even cover editing! If you want to learn more, and with more in-depth instructions, then I recommend you check out [my book](https://www.masteringemacs.org/book).
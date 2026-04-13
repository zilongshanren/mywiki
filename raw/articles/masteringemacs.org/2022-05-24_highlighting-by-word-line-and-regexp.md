---
title: Highlighting by Word, Line and Regexp
url: https://www.masteringemacs.org/article/highlighting-by-word-line-regexp
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

With Emacs’s Hi-Lock mode you can highlight by word, line or regular expression with ease. The highlighter functionality in Emacs is particularly helpful when if you are trying to do complex code refactoring or if you are fixing data or text by hand.

The Emacs Hi-Lock facility is obviously – and this should come as no surprise to you if you have used Emacs for a while – very complex with lots of whiz-bang features. I’ll concern myself with the most common use-cases for Hi-Lock and leave the more advanced concepts for another time.

## Global Hi-Lock Key bindings

As luck would have it, the highlighter commands are bound to easy-to-reach key bindings.

`M-s h .`

or`highlight-symbol-at-point`

Grabs the symbol at point and highlights it with a highlighter of your choice.

What’s a symbol? That depends on your buffer’s syntax table. It’s usually set up grab the right thing in most programming modes, but if you’re poring over log files, beware that

`text-mode`

and so on may not have a syntax table amenable to that.`M-s h l`

or`highlight-lines-matching-regexp`

Highlights all

*lines*matching a regular expression`M-s h p`

or`highlight-phrase`

Highlights everything matching a phrase

`M-s h r`

or`highlight-regexp`

Highlights everything matching a regular expression.

If you use subexpressions – like this

`\(...\)`

– then, as of Emacs 27, you can give`highlight-regexp`

a numeric prefix argument to indicate the subexpression you wish to highlight.`M-s h u`

or`unhighlight-regexp`

Deletes the highlighter under point

`M-s h w`

or`hi-lock-write-interactive-patterns`

Inserts a list of Hi-Lock patterns into the buffer

`M-s h f`

or`hi-lock-find-patterns`

Searches for Hi-Lock patterns in the buffer to use.


**NOTE:**All of the highlight-xxxx commands are actually just aliases for the hi-lock-xxxx commands.

### Whitespace and Casing

In Emacs 28, matching is now case sensitive if – much like case folding in things like ISearch – you use an uppercase letter. So, if you want case *insensitive* highlighting, you should only use lower case!

Another new feature in Emacs 28 is that `highlight-phrase`

now uses a little-known feature of (again) ISearch: `search-whitespace-regexp`

. Emacs will automatically ‘fold’ several types of whitespace characters and treat them as though they were a regular whitespace. In other words, when you use whitespace, Emacs will automatically match for other whitespace-alike characters.

### Customizing Hi-Lock

If you don’t like the Hi-Lock colors they can be customized easily with `M-x customize-group RET hi-lock-faces`

. You can of course alter the variable `hi-lock-face-defaults`

and add your own faces.

## Persisting Highlighters

There is a mechanism for storing and restoring the Hi-Locks you’ve created. If you create highlights interactively you can tell Emacs to insert those patterns into the active buffer by running `M-s h w`

. Emacs will wrap the elisp patterns in the comment format used by the buffer (if one is defined) or ask if you no comment format is defined.

The patterns should be added to the top of the file, as Emacs will only search the first 10,000 characters (customize `hi-lock-file-patterns-range`

to change that amount) for the patterns before giving up.

Emacs will not highlight patterns found in a file automatically. You must explicitly tell it to do so by manually invoking `M-x hi-lock-mode`

or globally with `global-hi-lock-mode`

.

You can also add it to your init file:

`(global-hi-lock-mode 1)`


Emacs may ask you if you want to load the patterns if it finds any. If you find that as annoying as I do, you can add this to have Emacs always highlight any Hi-Lock patterns it finds in the file:

`(setq hi-lock-file-patterns-policy #'(lambda (dummy) t)) `
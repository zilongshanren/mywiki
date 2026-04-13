---
title: 'Spotlight: Flycheck, a Flymake replacement'
url: https://www.masteringemacs.org/article/spotlight-flycheck-a-flymake-replacement
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Today’s spotlight is *Flycheck*, an excellent drop-in replacement for *Flymake*.

If you’re a regular Emacs user you may have heard of *Flymake*, a built-in package in Emacs that adds you as-you-type syntax checking and error highlighting. It’s been a part of Emacs for a long time (around twenty years.) But there is also a drop-in replacement called [Flycheck](http://www.flycheck.org/). It’s a third-party package, and you can find it on MELPA.

Both Flymake and Flycheck use the same, simple, principle of calling out to an external tool – be it a linter, compiler or interpreter – with a file copy of the active buffer you’re editing, parsing the resulting errors and warnings, and highlighting them in your buffer.

So why switch away from Flymake? Well, before the advent of Emacs 27 and the renewed interest in Flymake, I’d argue because Flymake had atrophied for a long time. Nowadays the distinction is less clear. If running `M-x flymake-mode`

works as you expect – this is doubly true if you’re using a Language Server client like eglot or LSP-mode – then you can just stick with Flymake. It works well. But, if you’re using an older version of Emacs, or if you want a package with nearly a decade’s worth of attention lavished on it, you may want to give Flycheck a shot.

Flycheck works with most major and minor programming languages and environments – both C and C++, with or without Clang, for instance – out-of-the-box. For most Emacs users it’s easy to download and install and have it up and running in minutes. You simply invoke `M-x flycheck-mode`

in a buffer, or globally with `M-x global-flycheck-mode`

. Another benefit of Flycheck is a wider array of third-party plugins to Flycheck – available on your local Emacs package repository – if your favorite language is not supported out of the box. As Flycheck’s an established package with a large body of third-party packages, it’s easy to find a package that works well with obscure languages or tools.

Flycheck also has its own keybinding, `C-c !`

by default, with a handful of utility commands you may find useful:

| Key | Binding |
|---|---|
`C-c ! ?` | Describe a Flycheck Checker |
`C-c ! C-c` | Compile using checker |
`C-c ! C-w` | Copy error point is on to kill ring |
`C-c ! C` | Clear all highlights from buffer |
`C-c ! V` | Report Flycheck version |
`C-c ! c` | Start syntax checking current buffer |
`C-c ! e` | Change Flycheck executable |
`C-c ! i` | Open Flycheck info manual |
`C-c ! l` | List all Flycheck errors |
`C-c ! n` | Jump to next error |
`C-c ! p` | Jump to previous error |
`C-c ! s` | Change Flycheck checker |
`C-c ! v` | Verifies the Flycheck checker works |
`C-c ! x` | Disable Flycheck checker in buffer |

Of particular note is `C-c ! v`

as a diagnostic tool. When you run the command Flycheck will display diagnostic information about the active checker in your current buffer. Useful if you have `$PATH`

issues or are missing the checker entirely on your system.

The command `C-c ! C-c`

is also handy. Instead of checking the buffer source code you can also instruct Flycheck to *compile* the file; whether that works or not depends entirely on your programming language and the checker used.

Another major benefit is the ease of which you can add your own checkers. Using an elisp macro called `flycheck-define-checker`

you can construct a checker with just a few arguments and Flycheck will handle the rest. I particularly like the use of LISP macros’ pattern matching and `rx`

instead of the far more unreadable and brittle string-based regular expressions Flymake used.

Take a look at the XML linter. It’s very easy to understand and modify:

```
(flycheck-define-checker xml-xmllint
"A XML syntax checker and validator using the xmllint utility.
The xmllint is part of libxml2, see URL
`http://www.xmlsoft.org/'."
:command ("xmllint" "--noout" source)
:error-patterns
((error line-start (file-name) ":" line ": " (message) line-end))
:modes (xml-mode nxml-mode))
```


So, if you’re using a newer version of Emacs, and if the default Flymake doesn’t tick all the boxes, you should give Flycheck a shot.

There are no comments. Why not write one?
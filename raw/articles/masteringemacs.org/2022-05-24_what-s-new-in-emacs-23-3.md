---
title: What's New in Emacs 23.3
url: https://www.masteringemacs.org/article/whats-new-emacs-23-3
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

**Update 10/3/11: Emacs 23.3 is officially out**

Emacs 23.3 is out now. Get the source archives [here](ftp://ftp.gnu.org/gnu/emacs/) or the compiled Windows binaries [here](ftp://ftp.gnu.org/gnu/emacs/windows/).

## What’s New in Emacs 23.3

Here’s a few interesting changes. The full set can be read by typing `C-h n`

.

You can allow inferior Python processes to load modules from the current directory by setting

`python-remove-cwd-from-path`

to nil.

This is very useful if you work with Python. If you set that variable to `nil`

you can force Emacs to add the current directory to `sys.path`

, meaning you can import the modules in that path without having to add it manually. The docstring correctly points out that this is a potential security risk, so do keep that in mind.

New VC command

`vc-log-incoming`

, bound to`C-x v I`

. This shows a log of changes to be received with a pull operation. For Git, this runs “git fetch” to make the necessary data available locally; this requires version 1.7 or newer.New VC command

`vc-log-outgoing`

, bound to`C-x v O`

. This shows a log of changes to be sent in the next commit.

Good news for DVCS users.

The

`g`

key in VC diff, log, log-incoming and log-outgoing buffers reruns the corresponding VC command to compute an up to date version of the buffer.

A useful update; now we don’t have to (kill) the buffer and re-run the command in the original buffer.

Special markup can be added to log-edit buffers. You can add headers specifying additional information to be supplied to the version control system. For example:

Author: J. R. Hacker

Fixes: 4204

Actual text of log entry…

Bazaar recognizes the headers “Author”, “Date” and “Fixes”. Git, Mercurial, and Monotone recognize “Author” and “Date”. Any unknown header is left as is in the message, so it is not lost.


Again, very useful if you use Emacs’s own VC facility to commit files.

smie.el is a generic navigation and indentation engine. It takes a simple BNF description of the grammar, and provides both sexp-style navigation (jumping over begin..end pairs) as well as indentation, which can be adjusted via ad-hoc indentation rules.


Now this is very interesting. A generic indentation and navigation module is a most useful addition to Emacs. Currently, as far as “generic” goes, I suppose we were limited to abusing syntax tables and complex functions like `parse-partial-sexp`

and the other helper functions in the `syntax.el`

library. But now we can write a more generic navigation/indentation engine and possibly gain other benefits from using it as well.

How this fits in with Emacs’s long-term plan of integrating [CEDET](http://cedet.sourceforge.net/) and the *Semantic Bovinator* lexer/parser/parser-generator remains to be seen.

The SMIE (*Simple-Minded Indentation Engine*) will no doubt be a useful tool for elisp hackers and I wonder if it is powerful enough to indent things like Python (or, ugh, all the many flavors of C styles) without resorting to nasty hacks.

You can read more about it in the file itself – see `M-x find-library smie`

– or its newly-minted info manual at `M-: (info "(elisp) SMIE")`

.
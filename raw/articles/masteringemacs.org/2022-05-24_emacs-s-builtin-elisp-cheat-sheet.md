---
title: Emacs's Builtin Elisp Cheat Sheet
url: https://www.masteringemacs.org/article/emacs-builtin-elisp-cheat-sheet
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Learning Emacs lisp is as much about taming the language as it is the ecosystem of functions and variables that you need to get the job done. The lack of namespaces (notwithstanding [shorthands in Emacs 28](https://www.gnu.org/software/emacs/manual/html_node/elisp/Shorthands.html)) and inconsistent naming due to 40+ years of organic growth doesn’t help.

But good news. Emacs 28 adds a cheat sheet / reference card feature called *shortdoc*. Invoke `M-x shortdoc-display-group`

and pick a category of elisp functions you want a cheat sheet for, and Emacs abides.

What I especially like about it is that it leverages all the things that I love about lisp and Emacs. Although Emacs is eminently self-documenting, it has sorely needed a feature like this.

When you open a *shortdoc* group you’ll see example code for each listed function, along with the output of said function, and hyperlinks to the Info manual entry (if there is such an entry.) If there’s no manual entry, Emacs will instead describe the function.

To top it off, it’s really easy to extend:

```
(require 'shortdoc)
(define-short-documentation-group list
"Making Lists"
(make-list
:eval (make-list 5 'a))
(cons
:eval (cons 1 '(2 3 4))))
```


You can add your own collection of reference entries: the existing cheat sheet definitions in `M-x find-library shortdoc`

and `C-h f define-short-documentation-group`

is enough to get you started. It’s straightforward and a perfect way to familiarize yourself with elisp if you’re new to it.

There’s also a couple of key bindings: `n`

and `p`

to move up or down, and `C-c C-p`

and `C-c C-n`

to move between sections. That’s in addition to the `RET`

or left mouse click for the hyperlinked function names.
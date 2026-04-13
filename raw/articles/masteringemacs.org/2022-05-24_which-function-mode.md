---
title: Which Function Mode
url: https://www.masteringemacs.org/article/which-function-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Here’s another useful feature in Emacs that lurks in the back of the cupboard, rarely seeing the light of day.

There’s a minor mode, `which-function-mode`

, that shows the current *defun* – Lisp lingo for a function, but Emacs-speak for anything that would count as one – in your modeline by looking at where your point is.

The mode is global and it works in most major modes that implement `M-x imenu`

support. If you have never used imenu, you should read my article on [effective movement](https://www.masteringemacs.org/article/effective-editing-movement).

Nevertheless, to err on the side of caution, the `which-function-mode`

only activates if the major mode is in the `which-func-modes`

list.

To add or remove items you can use the customize interface: `M-x customize-option RET which-func-modes RET`

and alter the list of major modes you want it to use. Note that not all major modes work with it, of course. If you’re unsure of the exact name of a major mode, type `M-: major-mode`

— note the lack of parentheses!

To turn the mode on automatically you can enable it in the `which-func`

group: `M-x customize-group RET which-func RET`

.
---
title: Hiding and replacing modeline strings with clean-mode-line
url: https://www.masteringemacs.org/article/hiding-replacing-modeline-strings
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you are like me, you are probably using one or more minor modes, and most of them add their own *lighter* to the modeline to tell you that they are running. Common examples include “Abbrev” for *Abbrev mode*; “yas” for *Yasnippet mode* and so on. Unfortunately, modeline real estate is expensive, and if you are stuck on a small screen – or if you split your Emacs windows a lot – you will find that it is often truncated, possibly hiding useful information that you *actually* care about, such as [Which Function Mode](https://www.masteringemacs.org/article/which-function-mode).

There is no feature in Emacs to selectively hide or compress modeline flotsam, so I have hacked together some code to do the job for you.

**NOTE: If you use use-package you can use :diminish along with the diminish.el package to accomplish this**



For instance, in my Emacs I can collapse the following modeline string:

`(Python Hi AC yas Eldoc Abbrev)`


Into:

`(Py α υ)`


I’ve chosen to completely obscure `hi-lock-mode`

, `abbrev-mode`

, and `eldoc-mode`

but “compress” `auto-complete-mode`

, `yas/minor-mode`

, and `python-mode`

.

I used Greek characters (How? `C-u C-\ greek RET`

then `C-\`

to write Greek characters; see [Diacritics in Emacs](https://www.masteringemacs.org/article/diacritics-in-emacs)) but you can use Emoji or any other code point you want.

Here’s the code. Stick it in your emacs file, evaluate it, and you’re done. You can also force a refresh by running `M-x clean-mode-line`

. Flymake will have to be turned off and back on for the changes to take effect in a buffer!

```
(defvar mode-line-cleaner-alist
`((auto-complete-mode . " α")
(yas/minor-mode . " υ")
(paredit-mode . " π"))
"Alist for `clean-mode-line'.
When you add a new element to the alist, keep in mind that you
must pass the correct minor/major mode symbol and a string you
want to use in the modeline *in lieu of* the original.")
(defun clean-mode-line ()
(interactive)
(loop for cleaner in mode-line-cleaner-alist
do (let* ((mode (car cleaner))
(mode-str (cdr cleaner))
(old-mode-str (cdr (assq mode minor-mode-alist))))
(when old-mode-str
(setcar old-mode-str mode-str))
;; major mode
(when (eq mode major-mode)
(setq mode-name mode-str)))))
(add-hook 'after-change-major-mode-hook 'clean-mode-line)
```
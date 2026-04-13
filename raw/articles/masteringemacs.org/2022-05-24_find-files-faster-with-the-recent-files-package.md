---
title: Find files faster with the recent files package
url: https://www.masteringemacs.org/article/find-files-faster-recent-files-package
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I bet the majority of files you edit on a day-to-day basis are the same ones over, and over again. For that reason I recommend you use Emacs’s `recentf`

package, it is a great – and very sophisticated, like all things Emacs – utility that keeps track of recently used files.

I supercharge `recentf`

by adding Ido mode support (if you don’t know what Ido is, read [Introduction to IDO Mode](https://www.masteringemacs.org/article/introduction-to-ido-mode)); and by overriding `C-x C-r`

, bound to `find-file-read-only`

, a useless feature I never use.

**NOTE**: If you’re using newer versions of Emacs you may find that you prefer the default completer you use. That is doubly true if you’re using `M-x fido-mode`

as it supercedes IDO mode in many respects. I’ve written extensively about [Understanding Minibuffer Completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion), so if you’re interested in knowing more about completion mechanisms in Emacs, that’s a good place to start.

Note that unlike `find-file`

I’ve opted to display the entire filepath in Ido’s completion engine as I often find that a directory or remote host is the only disambiguator if there are multiple files with the same name.

Here’s what you need to add to your init file:

```
(require 'recentf)
;; get rid of `find-file-read-only' and replace it with something
;; more useful.
(global-set-key (kbd "C-x C-r") 'ido-recentf-open)
;; enable recent files mode.
(recentf-mode t)
; 50 files ought to be enough.
(setq recentf-max-saved-items 50)
(defun ido-recentf-open ()
"Use `ido-completing-read' to \\[find-file] a recent file"
(interactive)
(if (find-file (ido-completing-read "Find recent file: " recentf-list))
(message "Opening file...")
(message "Aborting")))
```
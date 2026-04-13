---
title: Fixing the mark commands in transient mark mode
url: https://www.masteringemacs.org/article/fixing-mark-commands-transient-mark-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Most people, myself included, use `transient-mark-mode`

(or just *tmm*), a great piece of kit that makes Emacs behave sanely by using visible regions like other editors. But *tmm* can get in the way of Emacs’s point and mark system, as [the mark](http://www.gnu.org/software/emacs/manual/html_node/emacs/Mark.html) also serves as a handy beacon that you can set with `C-SPC`

and jump to with `C-u C-SPC`

.

Sadly, most of the point and mark commands generally go unnoticed by people who never used Emacs without *tmm*. That’s a shame, because mastering the mark commands will greatly speed up movement and editing.

In *tmm* the command `C-SPC`

activates the region and lets you select text as you see fit. That means if you want to set the mark (and nothing else) you have to follow up the preceding command with another `C-SPC`

(or `C-g`

) to abort the active region “selection.” That’s too much typing for something that should be second nature.

I use the following snippet below to explicitly set the mark. I bind it to `C-``

, an unused key.

```
(defun push-mark-no-activate ()
"Pushes `point' to `mark-ring' and does not activate the region
Equivalent to \\[set-mark-command] when \\[transient-mark-mode] is disabled"
(interactive)
(push-mark (point) t nil)
(message "Pushed mark to ring"))
(global-set-key (kbd "C-`") 'push-mark-no-activate)
```


The `C-u C-SPC`

command is trickier, as the functionality in *tmm* can be very useful for precision work not served by specialist commands like `mark-defun`

or `kill-sexp`

. To jump to the mark I replace the binding on `M-``

– a command that opens a terminal-friendly menu bar in the minibuffer – with a dedicated “jump to mark” command.

```
(defun jump-to-mark ()
"Jumps to the local mark, respecting the `mark-ring' order.
This is the same as using \\[set-mark-command] with the prefix argument."
(interactive)
(set-mark-command 1))
(global-set-key (kbd "M-`") 'jump-to-mark)
```


The `exchange-point-and-mark`

, bound to `C-x C-x`

, will by default activate the region when it is invoked. You must use the prefix argument to suppress the activation, but I find that to be too cumbersome for day-to-day use so I disable it outright. The snippet below will do this, so if you don’t want that to happen don’t use the snippet below!

```
(defun exchange-point-and-mark-no-activate ()
"Identical to \\[exchange-point-and-mark] but will not activate the region."
(interactive)
(exchange-point-and-mark)
(deactivate-mark nil))
(define-key global-map [remap exchange-point-and-mark] 'exchange-point-and-mark-no-activate)
```


And there you have it. Mark commands without the interloping *tmm* to spoil the fun.
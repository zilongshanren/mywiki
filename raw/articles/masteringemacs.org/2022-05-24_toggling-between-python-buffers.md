---
title: Toggling between Python buffers
url: https://www.masteringemacs.org/article/toggling-python-buffers
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I work with Python a lot, and as any swashbuckling Pythoneer knows, using the Python REPL is a big part of the day-to-day routine.

I often find myself switching from one python buffer to the shell (also known in Emacs lingo as the *inferior python process*) and back again. That means copious use of `C-x b`

or `winner-mode`

yet.. it just doesn’t feel *right*. Sure, I could use `C-c C-z`

(in Emacs’ own Python mode) but to me that’s a different use case.

I wanted something easier, so I wrote this a while back to toggle from a Python buffer to the shell, and from the shell you can go back to the last buffer you toggled from. In effect, it works like a very localized “alt-tab”.

Now I can quickly toggle between buffer and shell with a keypress. I’ve set it up so it won’t split windows but will instead switch the active buffer – like when you use `C-x b`

.

I bind the toggle command to `F12`

in all Python buffers and in the shell, so it’s easy to reach. Feel free to change the keybind if you like (read Mastering Key Bindings in Emacs to learn how.)

*Note: I can’t promise it’ll work in the non-Emacs Python mode!*

```
(require 'python)
(defvar python-last-buffer nil
"Name of the Python buffer that last invoked `toggle-between-python-buffers'")
(make-variable-buffer-local 'python-last-buffer)
(defun toggle-between-python-buffers ()
"Toggles between a `python-mode' buffer and its inferior Python process
When invoked from a `python-mode' buffer it will switch the
active buffer to its associated Python process. If the command is
invoked from a Python process, it will switch back to the `python-mode' buffer."
(interactive)
;; check if `major-mode' is `python-mode' and if it is, we check if
;; the process referenced in `python-buffer' is running
(if (and (eq major-mode 'python-mode)
(processp (get-buffer-process python-buffer)))
(progn
;; store a reference to the current *other* buffer; relying
;; on `other-buffer' alone wouldn't be wise as it would never work
;; if a user were to switch away from the inferior Python
;; process to a buffer that isn't our current one.
(switch-to-buffer python-buffer)
(setq python-last-buffer (other-buffer)))
;; switch back to the last `python-mode' buffer, but only if it
;; still exists.
(when (eq major-mode 'inferior-python-mode)
(if (buffer-live-p python-last-buffer)
(switch-to-buffer python-last-buffer)
;; buffer's dead; clear the variable.
(setq python-last-buffer nil)))))
(define-key inferior-python-mode-map (kbd "<f12>") 'toggle-between-python-buffers)
(define-key python-mode-map (kbd "<f12>") 'toggle-between-python-buffers)
```
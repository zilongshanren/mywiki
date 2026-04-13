---
title: Maximizing Emacs on startup
url: https://www.masteringemacs.org/article/maximizing-emacs-startup
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Until recently it was impossible to start Emacs in maximized mode in X, but that changed with the release of Emacs 23.2. Now you can force Emacs to start in maximized mode with the command line switch `--maximized`

or `-mm`

.

In Windows you have to use a bit of elisp and Win32 magic to get it to work.

Add this to your .emacs file to make Emacs start in maximized mode in Windows:

```
(defun maximize-frame ()
"Maximizes the active frame in Windows"
(interactive)
;; Send a `WM_SYSCOMMAND' message to the active frame with the
;; `SC_MAXIMIZE' parameter.
(when (eq system-type 'windows-nt)
(w32-send-sys-command 61488)))
(add-hook 'window-setup-hook 'maximize-frame t)
```


The code will only execute on Windows, and it works by sending a `WM_SYSCOMMAND`

window message to itself, telling it to maximize. The magic number `61488`

is a constant declared as `SC_MAXIMIZED`

.
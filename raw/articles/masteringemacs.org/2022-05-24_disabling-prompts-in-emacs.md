---
title: Disabling Prompts in Emacs
url: https://www.masteringemacs.org/article/disabling-prompts-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I find prompts in Emacs very annoying and in-my-face, so I have gone out of my way to remove or minimize any interaction I have with them.

Let’s start out by getting rid of the “yes or no” prompt and replace it with “y or n”.

If you’re using Emacs 28 you can use the customizable option `use-short-answers`

:

`(setq use-short-answers t)`


For Emacs versions prior to 28, you must use `fset`

:

`(fset 'yes-or-no-p 'y-or-n-p)`


Next up is the annoying confirmation if a file or buffer does not exist when you use `C-x C-f`

or `C-x b`

.

`(setq confirm-nonexistent-file-or-buffer nil)`


If [you use ido-mode](https://www.masteringemacs.org/articles/2010/10/10/introduction-to-ido-mode/) I recommend disabling the prompt that asks you if you want to create a new buffer if you enter a non-existent buffer in `C-x b`

. You can replace `always`

with `never`

which does the opposite: disables new buffer creation in ido’s switch buffer routine. Setting it to `never`

is an exceptionally bad idea as creating buffers on-the-fly is a *very* useful thing to do if you want a quick throw-away buffer.

`(setq ido-create-new-buffer 'always)`


You can also rid yourself of the splash screen and the echo area message:

```
(setq inhibit-startup-message t
inhibit-startup-echo-area-message t)
```


And finally, the prompt that asks you if you want to kill a buffer with a live process attached to it:

```
(setq kill-buffer-query-functions
(remq 'process-kill-buffer-query-function
kill-buffer-query-functions))
```
---
title: Compiling and running scripts in Emacs
url: https://www.masteringemacs.org/article/compiling-running-scripts-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I’ve talked about [running shells and terminal emulators](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) and [executing shell commands](https://www.masteringemacs.org/article/executing-shell-commands-emacs) in Emacs before, but that’s mostly used for *ad hoc* commands or command line spelunking.

What if you want to compile or run your scripts, code or unit tests and have the errors and warnings highlighted?

## There’s a command for that…

Not surprisingly, Emacs has its own compilation feature, complete with an error message parser that adds syntax highlighting and “go to next/prev error” so you can walk up and down a traceback in Python; jump to a syntax error, warning or hint in GCC; or interact with any one of several hundreds of known patterns.

The simplest way to compile something is `M-x compile`

. However, in my experience, a lot of people are put off by the default input of `make -k`

. It leads people to think that it requires, or depends on, a Makefile somehow. That is *not* the case.

Simply erase the text and replace it with a command of your own.

So if you want to execute Python’s `pytest`

you can type `M-x compile RET pytest test_something.py RET`

and a new `*compilation*`

buffer will appear with the output of the command.

Emacs will parse the output and look for certain patterns – stored in the variables `compilation-error-regexp-alist[-alist]`

– and then highlight the output in the compilation buffer with “hyperlinks” that jump to the file and line (and column, if the tool outputs it) where the error occurred.

If compilation is successful – and like most things in the UNIX world, this is governed by the exit code of the program you ran – the modeline and compilation buffer will say so; likewise, if an error occurred, this is also displayed.

You can jump to the next or previous error (`M-x [next/previous]-error`

) with `M-g M-n`

and `M-g M-p`

– they’re bound to more keys, but I think those are the easiest ones to use. Similarly, in the compilation buffer itself (only), you can go to the next/previous file (`M-x compilation-[next/previous]-file`

) with `M-g M-}`

and `M-g M-{`

, respectively, and `RET`

jumps to the location of the error point is on.

There is an undocumented convention in Emacs that commands like `dired`

, `grep`

, and `compile`

can be rerun, reverted or redisplayed by typing `g`

in the buffer.

You can also type `M-x recompile`

to rerun the same `compile`

invocation again. I encourage you to memorize that command or, better still, [bind it to a key](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) as it’s such a frequent task.

By default the compilation buffer is just a dumb display and you cannot communicate with the background process. If you pass the universal argument (`C-u`

) you can; the buffer is switched to comint mode, and you can converse with the process as though you were running it in the shell.

I generally prefer it to be interactive by default but for some inexplicable reason, that is not customizable.

Instead I use this advice to toggle the comint flag on:

```
(defadvice compile (before ad-compile-smart activate)
"Advises `compile' so it sets the argument COMINT to t."
(ad-set-arg 1 t))
```


## Multiple `*Compilation*`

Buffers

Emacs recycles the compilation buffer if it’s already present. So if you want multiple, simultaneous, `M-x compile`

instances then I recommend you rename the buffer with `C-x x r`

(or `M-x rename-buffer`

.)

## Project-Based Compilation

If you use Emacs’s project features (see `C-x p C-h`

) then you’ll be happy to know that there’s a dedicated compile command for this use case. It’s bound to `C-x p c`

.

## There’s a Minor Mode for that…

The `compile`

workflow isn’t for everyone; some people want everything in one place: their shell. Well, good news then – you can have your cake and eat it. The minor mode `M-x compilation-shell-minor-mode`

is designed for comint buffers of all sizes and works well with `M-x shell`

and most modes that use comint. You get the same benefits offered by `compile`

without altering your workflow. If you compile or run interpreted stuff in your Emacs shell you’ll feel like a modern-day Prometheus with this minor mode enabled!

Add this to your init file and the compilation minor mode will start when `shell`

does.

`(add-hook 'shell-mode-hook 'compilation-shell-minor-mode)`
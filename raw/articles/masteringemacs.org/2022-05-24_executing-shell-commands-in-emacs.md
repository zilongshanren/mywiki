---
title: Executing Shell Commands in Emacs
url: https://www.masteringemacs.org/article/executing-shell-commands-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

A common workflow is saving a file; modifying all or parts of it, somehow, on the command line; and then re-opening it in your favorite editor. But why not let Emacs do all the heavy lifting?

I have previously talked about [running shells and terminal emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview). But this time I want to talk about the other use case: executing shell commands against a region of text, and capturing the output for further editing in Emacs.

## Executing Shell Commands

There’s a number of different shell commands – not to be confused with `M-x shell`

, the Emacs inferior shell – and they are tightly integrated with Emacs’s buffer system.

### The Basics

The simplest way to invoke something is to run the command `shell-command`

, bound to the handy shortcut `M-!`

. Any command you give it fed through an actual shell – so you gain the benefit of shell globbing with `*`

and `?`

– and its output returned to you. If the output exceeds a certain size it’s sent to a separate buffer called `*Shell Command Output*`

. Otherwise it’ll appear in the echo area.

Emacs displays the exit code of the finished command in the mode line if it is non-zero. Emacs does not distinguish between output from standard error or standard output: they’ll appear as it’s emitted by the underlying command. If you want standard error sent to its own buffer you must set `shell-command-default-error-buffer`

to the name of a buffer you want it sent to.

By default Emacs executes the command *synchronously*. That is, the command blocks Emacs until the command has run its course. That’s probably not what you want for longer-running commands.

Instead you can append an ampersand (`&`

) if your underlying shell supports job control. Alternatively you can use the dedicated command `async-shell-command`

, bound to `M-&`

,. The asynchronous version uses the buffer `*Async Shell Command*`

for its output.

If you prefix the command with the universal argument, `C-u`

, Emacs will insert the output of the shell command into the current buffer at point.

### Shell Commands on Regions

Unlike the “normal” shell commands I explained before, this command works on regions of text. The region is sent via standard input to the command you give it, so you must ensure the command is capable of reading from standard input.

To use it, you can invoke either `shell-command-on-region`

or its shortcut `M-|`

. If you want Emacs to replace the region with the output returned from the command, you can again use the universal argument `C-u`

.

Feeding a region into a command and inserting the output of that command back into a buffer is a nifty thing indeed. But if all you’re doing is, say, sorting text with `sort`

then you should give Emacs’s own [sort command a try](https://www.masteringemacs.org/article/sorting-text-line-field-regexp-emacs).

### Coding Systems and Unicode

One issue – it does not happen so frequently any more as everyone (in the west, anyway) is using UTF-8 – but if you get garbled characters or errors about the encoding or locale, you should read my article on [working with coding systems and unicode in Emacs](https://www.masteringemacs.org/article/working-coding-systems-unicode-emacs).

### Invoking Shell Commands from Elisp

You can use the same commands you used in interactive mode in your elisp code, with the only catch that you have to fill out a few more parameters.

Here’s a commented example I wrote that marks the entire buffer and feeds it to `tidy`

, a useful utility for cleaning up and formatting HTML and XML:

```
(defun tidy-html ()
"Tidies the HTML content in the buffer using `tidy'"
(interactive)
(shell-command-on-region
;; beginning and end of buffer
(point-min)
(point-max)
;; command and parameters
"tidy -i -w 120 -q"
;; output buffer
(current-buffer)
;; replace?
t
;; name of the error buffer
"*Tidy Error Buffer*"
;; show error buffer?
t))
```


As you can see, it’s a simple thing indeed to build your own function to do this. Instead of manually figuring out how to do this – if you’re new to elisp, it’s not always super obvious – I recommend you learn how you can [repeat complex commands in Emacs](https://www.masteringemacs.org/article/repeating-commands-emacs). It’s a genial way of learning elisp.

Or if you prefer a no-code approach, then I [recommend you try a keyboard macro](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) instead. Keyboard macros can play back nearly everything.
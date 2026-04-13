---
title: My Emacs keybindings
url: https://www.masteringemacs.org/article/my-emacs-keybindings
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I figured I’d write a blog post about the keys I’ve bound but also rebound in Emacs. I think rebinding keys in Emacs – even though, in essence, the editor is built around the idea of customization – is a perilous thing to do if you are not careful: people do it without knowing *why* the key is bound to what it is. This is particularly true of the “core” bindings in Emacs. Rebinding keys is something you should do as a last resort: if you’re new to Emacs and your first impulse is to rebind everything – stop! Learn Emacs first and *then* decide.

Consider `C-f`

. It moves forward by the character, but `M-f`

moves forward by word, and `C-M-f`

moves forward by an s-expression. See the similarities? The `C-`

for character, `M-`

for word and `C-M-`

for s-exp is a recurring pattern in Emacs.

Having said that… there are keys I rebind and commands I explicitly bind to keys. Most of them are quality of life improvements: I want to make it easier to type things I do frequently.

`M-o`


The command `other-window`

is normally bound to `C-x o`

but I find that way too cumbersome for what is such a frequent operation. `M-o`

is normally bound to some rich text formatting nobody cares about.

`C-<return>`


This I bind to a custom Helm command that calls up some of my more frequent things. This key is surprisingly unbound in most modes.

`M-`

`

This is taken from my article on [fixing the mark commands](https://www.masteringemacs.org/articles/2010/12/22/fixing-mark-commands-transient-mark-mode/). When pressed it’ll jump around in the mark ring. Very useful, but Ubuntu and Unity (in their wisdom) have decided that I am not allowed to rebind this key…. so I cannot use it any more.

`C-x C-k`


I kill buffers all the time, and the idea of killing a buffer that is *not* active is just not part of my workflow at all. This key will kill the active buffer without any prompting whatsoever.

`Read my article on repeating commands for more info.`


`C-=`


This I bind to CSSH’s `cssh-term-remote-open`

. It prompts me for a remote host to SSH to using an `M-x ansi-term`

session. It’s great.

`C-x C-r`


By default this will run `find-file-read-only`

, a command that finds a file but opens it as read only. Meh. That’s all I have to say about that. The few occasions I need to do this I just set it as read only. Instead I bind it to a custom command that, using IDO, [gives me a list of recent files I’ve opened.](https://www.masteringemacs.org/articles/2011/01/27/find-files-faster-recent-files-package/)

`M-n / M-p`


I bind these to my smart scan next/previous commands. They’re part of my [Smart Scan package](https://www.masteringemacs.org/articles/2013/10/31/smart-scan-jump-symbols-buffer/).

`S-C-<left/right/down/up>`


This calls `shrink/enlarge-window-horizontally`

and `enlarge/shrink-window`

respectively. I don’t often resize my windows any more (my high monitor resolution means I don’t have to) but it’s occasionally useful, and definitely more useful than the useless and impossibly-hard-to-type `C-x ^`

, et al. they’re bound to by default.

`F1`


This runs `M-x shell`

, my preferred one of the terminal/shell wrappers in Emacs. If you don’t know the difference, read [Running shells in Emacs: an overview](https://www.masteringemacs.org/articles/2010/11/01/running-shells-in-emacs-overview/). It’s such a handy keybinding, too. Yes, you override the help, but it’s bound to `C-h`

also.

`F2`


Runs `M-x rgrep`

. Indispensable. I grep a lot and the key is very accessible. By default it’s bound to the 2-column commands but they’re also bound to `C-x 6 ...`

.

`C-<f2>`


This runs my own command, `multi-occur-in-this-mode`

. This will run `M-x occur`

but against *all buffers* of the same major mode as the one point is in. Very useful. [Searching buffers with occur mode](https://www.masteringemacs.org/articles/2011/07/20/searching-buffers-occur-mode/) will tell you all you want to know.

`F6`


This calls another custom command of mine, `revert-this-buffer`

. It does exactly what the name implies: it reverts (reloads from file) the current buffer without asking any questions. It will notify you in the minibuffer area that it did it.

```
(defun revert-this-buffer ()
(interactive)
(revert-buffer nil t t)
(message (concat "Reverted buffer " (buffer-name))))
```


`F10`


This calls `magit-status`

. That will open up Magit, [a great Git client for Emacs](https://www.masteringemacs.org/articles/2013/12/06/introduction-magit-emacs-mode-git/). Simple, but I use it 100s of times a day.

`C-x C-b`


This is simply bound to `M-x ibuffer`

. Terrific feature; ibuffer’s great.

And that’s pretty much it. Not a whole lot, really. I do repurpose quite a few of the aforementioned keys as there is, to me, a lot of useless cruft I’d never use, but apart from that very few of them are remapped.

Still, there’s always room for improvement. If you have any suggestions or handy snippets – post below or e-mail me.
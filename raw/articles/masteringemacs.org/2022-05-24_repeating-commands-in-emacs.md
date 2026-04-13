---
title: Repeating Commands in Emacs
url: https://www.masteringemacs.org/article/repeating-commands-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Repeating a command you just carried out is useful thing to know about, and yet because it’s bound to `C-x z`

it’s unknown to most.

Like the `.`

command in vi, the `M-x repeat`

command will repeat the last action, but it does ignore input events, like moving around.

To save you from press the rather awkward keybind every time you want to repeat something, you can repeatedly press `z`

after your first invocation to call `repeat`

. Of course, you can also use the universal argument to repeat the command *N* number of times.

Although the repeat feature is useful, it’s best used for simple things. If you want to do complex chains of tasks, you should read why I think [keyboard macros are misunderstood](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood). It’s a deep dive into keyboard macros in Emacs and why they are so powerful. And no, they’re not just for munging text!

In a similar vein, you can exploit Emacs’s ability to turn any command you just executed into elisp. That elisp you can then invoke at will [by evaluting it any way you see fit](https://www.masteringemacs.org/article/evaluating-elisp-emacs). You can also [create a key binding for it](https://www.masteringemacs.org/article/mastering-key-bindings-emacs).

The choices in Emacs are endless.
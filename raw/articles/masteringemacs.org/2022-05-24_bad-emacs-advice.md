---
title: Bad Emacs Advice
url: https://www.masteringemacs.org/article/bad-emacs-advice
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I have been using Emacs since 2004 which, measured in Emacs-ontological terms, barely counts as much experience at all. But since I started using Emacs I have spent a large part of that time learning, just like everyone else, and helping others do the same — and perhaps more to the point: watching other people dispense advice on *how* to learn Emacs or get started with it.

We’ve all spent a large amount of time learning, and reaching proficiency in, Emacs. So, the sage advice that most people dispense to new Emacs users is usually just that: sage advice. But just like pizza with pineapple, people do occasionally give out downright *bad advice*.

A lot of the bad advice – and it’s really just a few things that crop up again and again – that I see repeated all over the place seems to stem from the idea that Emacs’s own builtin facilities are immovable barriers, or cumbersome impediments, to achieving True Enlightenment, and that you can only achieve this Zen of Emacs through self-flagellation.

So I’m quickly going to go over the things that I really wish people wouldn’t tell new users, even though they do so with an abundance of good faith.

## Disabling the Menu Bar

This is perhaps the most common “advice” of all: that you must disable the menu bar, tool bar, and scroll bar. In the case of the menu bar, you stand to gain 1 row of text in console Emacs, and a handful of pixels in GUI Emacs, at the cost of hiding the first thing any computer user would look to for help, features and guidance: a menu bar full of curated, context-sensitive menu options.

The menu bar is contextual: it will change depending on the major, and sometimes minor, modes you have enabled in the active buffer. And the selection of default menu bar features is *vast*. You can do an awful lot of Emacs work with nothing but the menu bar; better still, it’s got a human-friendly name for each option, and the keyboard shortcut (if any) next to it, as well. When I was learning Emacs (XEmacs, actually!) I found it invaluable myself.

And if you type `M-``

you get a keyboard-friendly version in the minibuffer that works in Terminals (and in the GUI) without the need for a mouse.

So it’s got features and it’s contextually aware of what you’re doing. That makes it an easy place to point beginners at if they want to do any number of common activities, like: customizing Emacs’s many features; changing the default font; or learning more about a major mode they frequently use. It’s also got a list of buffers and frames; you can access the package manager; the calculator; spell checker; search and replace; enable CUA mode; and much, much more.

But most importantly of all: it has the “Help” menu! Why someone would encourage newbies to disable something that can credibly *help* them learn Emacs is a mystery to me.

(Oh, and, by the way, you can type `C-h k`

and click on a menu bar item to get its function description. I bet you didn’t know that!)

## Not directing users to the Emacs Manual

Emacs is very well documented. It’s got the self-documenting parts, thanks to elisp and all that machinery, and a set of hand-curated manuals that ship with it. I find it surprising when people remark not to bother with it; it should be the first port of call for most people. I use it frequently to find commands and functions adjacent to what I am doing, or to learn about complex internals in Emacs.

I would encourage *everyone*, regardless of skill level, to sit down and read the Emacs manual in `C-h i`

from start to finish. You’ll learn a lot, and gain a much greater appreciation for what Emacs is capable of, and how much care and attention is lavished on an area that most consider unsexy.

Not sure how to find things in the manual? Use [the apropos tool](https://www.masteringemacs.org/article/full-text-searching-info-mode-apropos).

## Turning people away from the Tutorial

In a similar vein to the above, the builtin tutorial is short, simple, and to the point: but it’s there for a reason! It helps new users get acquainted with Emacs terminology and concepts — and they’ll need it, especially when you told them to turn off the menu bar so they can’t find things.

## The Customize Interface

I use it, it’s useful, and it has its place. *Especially* if you’re new to Emacs. You can configure large swathes of Emacs core to your liking (and many third-party packages), and you can temporarily enable your changes for the current session only, ensuring you’ll never break something permanently.

It should again be the first port of call for people to configure their Emacs, if they are not yet comfortable with elisp. And they may not be for years, if at all.

Customize has its place, and so does configuring stuff with elisp. You can do infinitely more with the latter, but you can still accomplish a large amount with the former.

So here’s a challenge to people who say the Customize interface is useless: try launching a blank-slate Emacs and manually set up your font faces with pure elisp the way you like them without `M-x customize-face`

and themes to guide you.

## Conclusion

Telling beginners to disable helpful features in Emacs is not good advice. The confluence of customizing Emacs with Customize; discovering features with the menu bar; and knowing how to learn and get help is foundational stuff in Emacs. And it’s something everyone needs to know to get ahead in Emacs, even if you’re an expert.
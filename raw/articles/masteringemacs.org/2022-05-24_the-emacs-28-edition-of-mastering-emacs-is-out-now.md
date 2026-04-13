---
title: The Emacs 28 Edition of Mastering Emacs is out now
url: https://www.masteringemacs.org/article/the-emacs-28-edition-of-mastering-emacs-out-now
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

After several weeks of tweaking and editing, the [ Mastering Emacs book](https://www.masteringemacs.org/book) is now current with Emacs 28. Although Emacs 28 is mostly an incremental upgrade, introducing a large swathe of changes and improvements touching on many parts of Emacs, I think the hallmark feature (as I allude to below in the excerpt from the 2022 update from the book) is

*native compilation*. I first wrote about it

[some years ago](https://www.masteringemacs.org/article/speed-up-emacs-libjansson-native-elisp-compilation)now, and I think native compilation is one of very few features in Emacs that pushed people to build Emacs from source just to try it out.

I’ve been using it daily for years and it’s rock solid. It’s a major engineering triumph. My personal thanks to [Andrea Corallo](https://akrl.sdf.org/gccemacs.html) for his incredible and steadfast work on this: it took him *years*!

## 2022 Edition Update

Emacs 28 is the newest version available and a significant upgrade over Emacs 27, as it introduces the long-awaited *native compilation* feature. With the size – and ambition – of third-party packages growing every year, so must Emacs’s performance.

*Native compilation* greatly improves Emacs’s performance across the board by compiling elisp into native code suitable for your platform and system architecture. It was a herculean effort by mostly one person, *Andrea Corallo*, that took several years of hard work before it made it into Emacs 28.

Aside from that major feature, the vast majority of changes in Emacs 28 are incremental, and I’ve updated the book accordingly, when I feel the new commands or customizations are worth knowing about.

However, there are a couple of larger features that I want to highlight here:

- Project Management Improvements
Some of them made it into Emacs 27, but it’s been greatly enhanced in Emacs 28. A dedicated project management keymap makes it more accessible and easy to use, and it enhances a lot of features already present in Emacs.

- Friendlier Help and Description Commands
Emacs is self-documenting, but it did have a few blind spots that I think this release helps address. The Help system is updated slightly with additional key bindings and better descriptions.

The

*describe*system is the primary way of looking up symbols in Emacs, and Emacs 28 adds a couple of new commands that helps with that.- Better Discoverability
Finding useful commands related to a minor or major mode is not always that easy. A mode may introduce many commands, of which only a handful are likely of interest to the average user. Emacs now lets you ask it to execute a command pertinent to the modes active in your current buffer. It greatly improves discoverability.


As for the book itself, I’ve also gone through and removed most version markers – some dating back to Emacs 24 – as they’re not going to make a material difference to readers today. As part of that process, I’ve reworded and clarified things that I felt weren’t as obvious or clear as I wanted them to be.

### Emacs in the Future

What’s in store for Emacs in the coming years, then? One tantalizing possibility is recognizing that regular expressions – the preferred tool of most editors to syntax highlight and extract semantic information – peaked decades ago, and if we want more intelligent tooling, we need to smarten up how we parse source code. That’s not a new or novel idea, but one that is hard to achieve at scale — a fact that held back intelligent code completion until *Language Servers* democratized it with a standardized protocol anyone could tap into and build on.

Emacs does have a few major modes that use language parsers for syntax and semantic enrichment, like `js2-mode`

and `nxml-mode`

. CEDET, a sprawling polyglot IDE with its own language parsers and semantic tooling, was merged into Emacs’s core about a decade ago, but it never caught on.

I believe *tree sitter*, a general-purpose incremental language parsing library that has seen significant adoption in other editors already, is the right tool for the job. It will not replace regular expressions completely, and nor should it: regular expressions have their place. But, *tree sitter* works with dozens of languages already and, rather propitiously, uses an s-expression-based query language. That makes it a perfect fit for Emacs and elisp. It’s also fast, and it can handle broken source code, so it’ll still work properly when you’re writing code. If you’re keen on experimenting, you can use tree sitter in Emacs right now for a much-improved syntax highlighting experience.
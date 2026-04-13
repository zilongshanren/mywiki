---
title: 'Jedi: A completion library for Python'
url: https://www.masteringemacs.org/article/jedi-completion-library-python
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re using Python with Emacs (using one of several competing, incompatible, and slightly different modes) you are used to a pretty… bare-bones experience: no completion; semi-functional dynamic docstring support; and little in the way of two-way communication between Python and Emacs.

**NOTE: I recommend you use a Language Server Protocol (“LSP”) tool like Eglot or lsp-mode nowadays.**

Enter [Jedi, a completion library](https://github.com/davidhalter/jedi). Yes, *Jedi*, an editor-agnostic library that publishes auto completion, docstring support, and more. Excellent.

I’ve experimented with Pymacs – an interesting science project that adds “Python-like” support Emacs, so you can avoid interacting with Elisp, except not really – rope, and ropemacs and they were… disappointing. Slow, crash-prone, obtuse and impossible to extend. So I never really used them, and lived without completion or, well, much of anything beyond the REPL and my own handcrafted modifications.

The other alternative is the 600 lbs gorilla, CEDET, and its incomplete Python support, but that’s no good either.

Imagine my surprise, after fidgeting with the dependencies for both Jedi and [Jedi.el, the Emacs library for Jedi](https://github.com/tkf/emacs-jedi), that it… works! And it’s good! It’s up-and-coming, I should say, but perfectly usable; it doesn’t get in my way, it’s got some crazy deferreds library it depends on for asynchronous, non-blocking querying of Jedi, but that bit works great – no input lag at all.

It seems to resolve, simplistically (which is good), as many assignments and method calls as one can reasonably expect from a non-evaluating, statically analyzing Python completion library.

![Functioning Auto Complete in a Python buffer](../../assets/5c0800d555fe6d1a.png)


The Jedi.el module also Just Works with the excellent [auto-complete](https://github.com/auto-complete/auto-complete) library, as you can see in the picture above.

Aside from completion, it also offers “find symbol definition at point” (a la *TAGS*, but not crap) and Jedi.el sensibly binds it to `C-.`

by default. It also has a “related names” functionality, tracking down same-named identifiers in other modules; it uses *Anything* (now *Helm*) to display the results, and it is bound to `C-c r`

. And finally, it can show the documentation for the identifier at point (be it a class or function) with `C-c d`

. Useful.

I haven’t used Jedi and Jedi.el long enough to really get to know it, but I’m probably going to extend Jedi.el so it uses `eldoc-mode`

for displaying the function parameters; it’s also a bit rough around the edges, and I may want to tweak certain things to my liking, but overall: huge success!

I highly recommend you give Jedi and Jedi.el a try!
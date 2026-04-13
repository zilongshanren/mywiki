---
title: The Emacs 29 Edition of Mastering Emacs is out now
url: https://www.masteringemacs.org/article/the-emacs-29-edition-of-mastering-emacs-out-now
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

It’s taken a little bit longer than I would have liked to get the next edition out the door. I also felt the site needed a lick of paint which, if you’re a regular and astute reader, you may have noticed already.

But as I explain in the book update below, the two headline features are tree-sitter support and Eglot. To say nothing of the [million other new Emacs 29.1 features](https://www.masteringemacs.org/article/whats-new-in-emacs-29-1) that were added.

A couple of years ago, I wrote about [Tree Sitter and the Complications of Parsing Languages](https://www.masteringemacs.org/article/tree-sitter-complications-of-parsing-languages). In it, I talk about the immense difficulties around parsing languages in a way that is both useful and consistent for a wide range of programming languages and structured texts. Tree-sitter is one of the few that have managed to cross that chasm; no small feat, in my opinion.

The other major inclusion is Eglot. It’s another smart and sensible addition to Emacs core. Combined with tree-sitter, you now have access to top-notch syntax highlighting and IDE-like features right out of the box.

## 2024 Edition Update

*This is 2024 Edition update the excerpt from the book.*

Emacs 29 continues the long-running trend of keeping up with advances in technology. That is commendable. Emacs is an old piece of software, and yet it is continuously improving.

One of the hardest things to get right in a text editor is syntax highlighting (*font locking* in Emacs parlance) and writing a robust indentation engine. You see, when Emacs – and many other editors, old and new – syntax highlight your source code, they do so using *regular expressions*, a terse method for matching text using pattern matching. Regular expressions are great; they’re a succinct way of matching and extracting important information from text. They are the backbone of syntax highlighters nearly everywhere, but they also have a flaw: they can be imprecise, and can impede performance if they are poorly written.

A regular expression also cannot contextualize what it is matching: just that it did (or did not) match something. For a wide range of granular tasks, it is simply not possible to rely on regular expressions. That is a problem as you want as much precision as you can get. Yet it’s often impossible to tell some things apart with a regular expression, such as whether a series of characters is a variable or a function call. The same series of characters may have one meaning in one context, and an altogether different one in another. Regular expressions are rarely powerful enough to capture that nuance. And so most text editors build their syntax highlighting and indentation engines with a medley of regular expressions and hand-tuned, imperative code to try to work around the limitations of the former.

Good news, then, as Emacs 29 adds optional support for [tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter), a parser library with an exacting eye for source code parsing that constructs a *Concrete Syntax Tree* from any text for which it has a valid grammar. Such a tree is the perfect medium for a computer (or willing user) to query. It makes correct syntax highlighting possible with little more than a few dozen lines of code. It also adds the tantalizing promise of *structured editing and movement*, a sprawling concept that reuses the tree-like structure tree-sitter yields to offer unparalleled editing and movement in your code base.

Tree-sitter’s not the only game in town. What it *does* bring to the table, and what has eluded most other attempts (in Emacs and beyond), is that is has the largest repository of parsers for both common and uncommon languages and structured text files. Tree-sitter is thus capable *and* popular. It helps that it is quite straightforward to write your own parser using tree-sitter’s tooling. The cherry on top is a query language to quickly find and match segments of the parsed *tree* that it emits. That is perhaps its ace in the hole: being able to ask it to show you (for example) all the functions that contain one or more variables with a given name is a powerful feature indeed. Modeled on LISP’s S-expressions, the query language also feels right at home in an Emacs ecosystem.

Presently, the feature is optional, as you must compile Emacs with tree-sitter support. So it is unlikely to replace, wholesale, the existing major modes and the old way of doing things. But it’s a large step forward for Emacs, as it makes writing syntax highlighting and indentation code [downright easy](https://www.masteringemacs.org/article/lets-write-a-treesitter-major-mode). Its adoption into Emacs core is a positive development, and a repudiation against the entrenched belief that Emacs can never fundamentally change. *Font locking* in Emacs was first introduced around 35 years ago, and now there is a new way – and often much better way – than the old regular expressions. Its successful integration into Emacs is also reflected in the wider Emacs community where it has proven to be a popular feature, despite the fact that tree-sitter is, being new to Emacs, cumbersome to set up and use.

The other major inclusion is Eglot, a client that understands the language server protocol (LSP). Eglot adds IDE-like features to any buffer for which there is a language server available. It’s designed to work with nothing more than base Emacs and the requisite language server. Provided you’ve got your language server set up, all you need to type is `M-x eglot`

(or select `Tools -> Language Server Support`

) to get started. Eglot’s been around for a long time on [ELPA](http://elpa.gnu.org/), an Emacs package repository. Now it’s built into Emacs.

Both capabilities are capstones in an otherwise packed release full of exciting improvements and fixes. If you’re not using Emacs 29 already, you should definitely upgrade.
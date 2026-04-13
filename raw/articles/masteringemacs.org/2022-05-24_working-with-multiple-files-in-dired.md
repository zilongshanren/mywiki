---
title: Working with multiple files in dired
url: https://www.masteringemacs.org/article/working-multiple-files-dired
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

It’s all too common: you have a large swathe of files and you want to do something to them. Unfortunately, they’re not in the same directory. If you’re a command line superstar you’re going to reach for `find`

and maybe a little `xargs`

.

But what if you want to use Emacs?

The simplest solution, when the files are all in the same directory, is to use `M-x dired`

(`C-x d`

) and mark the files you want to work on. Job done.

But what about the too-common case when they’re not.

Surprisingly, it is actually simple. Dired works by querying `ls`

(or an emulated equivalent if it is not available) and formatting the printed output from `ls`

. In fact, the GNU version of `ls`

comes with a switch `-D`

specifically designed to format the output to suit dired (though it’s not used in newer Emacsen.)

Emacs is a *text* editor, so it’s not surprise at all that Emacs would co-opt the output from a command line `ls`

; enrich it with hyperlinks and colors; and then call it a day. In fact, it’s such a fundamental part of Emacs that I’ve written about [why Emacs has buffers](https://www.masteringemacs.org/article/why-emacs-has-buffers).

Dired’s nothing more than `ls`

and a large corpus of commands that operate on that output. But if that’s the case, then surely it’d work just fine if you fed it output that looks like `ls`

but actually contains nested or relative paths, right? Right!

And don’t forget that Emacs and dired is a capable [find & xargs replacement](https://www.masteringemacs.org/article/dired-shell-commands-find-xargs-replacement) also. To say nothing of using [editable dired buffers](https://www.masteringemacs.org/article/wdired-editable-dired-buffers)!

## The Find Dired library

The command `find-dired`

calls `find`

to find and match files and `ls`

to format them so dired can understand it. It’s pretty bare-bones and it’s aimed at people who want to tweak every parameter that goes into those commands.

Generally, though, I find `find-name-dired`

to be more useful for day-to-day use when all I want is to feed it a single string to match against. `find`

is by its nature recursive, so I don’t have to do much more than point it at a base directory.

You can control how Emacs finds matches by customizing `find-ls-option`

. You may want to do that if you have strong opinions about the ordering or the results.

Here’s an example that uses human-readable file sizes instead of the default.

```
(require 'find-dired)
(setq find-ls-option '("-exec ls -ldh {} +" . "-ldh"))
```


Modern versions of `find`

support the `-ls`

argument. There’s no need to specifically invoke `-exec ls`

if you don’t want to.

## The Find Lisp library

The *Find Lisp* library is similar to the *Find Dired* library, but instead of calling out to `find`

, the *find lisp* library emulates a basic version of `find`

in elisp.

The *find lisp* library uses Emacs’s regular expression engine and that means you cannot use wildcards like `*.foo`

. Instead, you have to write `\.foo$`

. That may or may not be an issue for you, but it is worth keeping in mind.

One advantage the *find lisp* library *does* have is that it is usually very fast, and it does not require the presence of tools like `find`

. That’s mostly of note to Windows users or if you’re on minimalist platforms that may lack `find`

.

To find stuff with *find lisp* type `find-lisp-find-dired`

. To see *only* directories use `find-lisp-find-dired-subdirectories`

.

## Virtual Dired

Now I know what you’re thinking: can’t I just… stuff the output of `ls -l`

in a buffer and run `M-x dired-mode`

on it?

No.

I wish you could, but annoyingly you can’t. You have to use another command called `dired-virtual`

and for it to work, you have to import a library that is not normally loaded in Emacs:

`(require 'dired-x)`


It’s called `dired-x`

. It’s got a number of other surprises in it, but `dired-virtual`

is one of the more important ones.

To use it, insert a long listing from `ls`

into a buffer and type `M-x dired-virtual`

. It’ll ask you for a base directory, so make sure it reflects the relative paths of the files you’re inserting!

## Inserting Sub-Directories

Another approach is typing `i`

on a directory in dired. It’s a neat feature, but of course a bit manual.

## Final Thoughts

Combining `find`

& friends to turn a glob-style query into a full-fledged dired buffer is a bit of a super power. It’s therefore a viable alternative to using the command line directly, as you can unleash the full power of Emacs and dired.

And if that fails, you can always use `M-x virtual-dired`

or simply insert the sub directories manually with `i`

.
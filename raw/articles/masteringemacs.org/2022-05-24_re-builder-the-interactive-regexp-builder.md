---
title: 're-builder: the Interactive regexp builder'
url: https://www.masteringemacs.org/article/re-builder-interactive-regexp-builder
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I doubt it’s a well-kept secret that Emacs has a regexp “helper” called `M-x re-builder`

. But if you haven’t heard about it before, Emacs’s re-builder lets you interactively build a regular expression and see what it matches on the screen. It’ll even uniquely color capturing groups so you can tell them apart.

## Syntax

What most people *don’t* know is re-builder’s support for different syntax; but, sadly, not *PCRE* – sorry!

There are five different syntax choices (see table below). You can either use customize (`M-x customize-variable RET reb-re-syntax RET`

) or set the variable (`reb-re-syntax`

) directly.

`read`

**Default**. Similar to`string`

but requires “double escaping” of backslashes like you would be required to do in elisp. Example:`\\\\(foo\\\\\|bar\\\\)`

`string`

**Recommended**. Similar to`read`

but you**don’t**have the issue of backslash plague that haunts the default settings. Example:`\\(foo\\\|bar\\)`

`sregex`

**Deprecated**. A symbolic regular expression engine that uses s-expressions instead of strings.`lisp-re`

**Deprecated**. Yet*another*regular expression engine that uses s-expressions`rx`

**Recommended**. A*third*, and far more advanced, s-expression regexp engine. Use this and not`sregex`

or`lisp-re`

if you want to use a lisp-style regexp engine.

## The backslash madness

I recommend you switch to `string`

right away; there’s little reason to use `read`

, and the extra escaping will drive you insane unless you’re used to writing regexp in elisp.

Add this to your .emacs to switch the default syntax to `string`

:

```
(require 're-builder)
(setq reb-re-syntax 'string)
```


## Useful Keybinds

If you do write a lot of elisp, you probably use (or should use!) `rx`

to make your regexp experience in Emacs a bit more pleasant. Unfortunately, you can only have one default setting at a time so you have to switch manually with `C-c TAB`

in re-builder.

You can enter the sub-expression mode with `C-c C-e`

to only highlight capturing groups; you can toggle the case sensitivity with `C-c C-i`

; and you can move between matches with `C-c C-s`

and `C-c C-r`

.

The re-builder keybind `C-c C-w`

bears mention as well: it will copy (and convert, where applicable) the expression to a string format suitable for use in elisp.
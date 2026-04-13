---
title: Making CamelCase Readable with Glasses-Mode
url: https://www.masteringemacs.org/article/making-camelcase-readable-glasses-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re working on a codebase that makes use of CamelCase identifiers `LikeThis`

or `evenWorseLikeThisAbstractFactoryFactory`

you can make them readable by splitting up the words with `M-x glasses-mode`

. `glasses-mode`

will insert a virtual *underscore* separator between the conjoined words, so `fooBarBaz`

will look like `foo_Bar_Baz`

.

The changes are not permanent and Emacs will keep track of the virtual separators and ensure they are never accidentally saved to disk.

When `glasses-mode`

is enabled, you should continue following the CamelCase style as Emacs will automagically insert the virtual separator, as needed, when you type a capitalized character.

There’s a handful of configurable options you can tweak to personalize `glasses-mode`

. To access them, type `M-x customize-group RET glasses`

.
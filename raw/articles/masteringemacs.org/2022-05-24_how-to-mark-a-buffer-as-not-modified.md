---
title: How to mark a buffer as "not modified"
url: https://www.masteringemacs.org/article/mark-buffer-not-modified
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

You can tell Emacs to set a buffer as not modified (even though it may well be) by pressing `M-~`

, also bound to `M-x not-modified`

. This will obviously suppress any save prompts for that file – at least until you do something that makes it become modified again – so do be careful.

There are no comments. Why not write one?
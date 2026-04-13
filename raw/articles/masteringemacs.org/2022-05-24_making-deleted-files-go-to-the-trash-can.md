---
title: Making deleted files go to the trash can
url: https://www.masteringemacs.org/article/making-deleted-files-trash-can
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

In Emacs 23.1 support for your operating system’s *trash can* (or recycle bin, or whatever) was added. File deletions in Emacs now uses your system’s trash can and the deleted files will be put there instead. The feature must be enabled manually by adding this to your .emacs:

`(setq delete-by-moving-to-trash t)`


The delete to trash functionality will obviously behave differently depending on your operating system. On Windows the special function `system-move-file-to-trash`

is defined because Windows exposes its own API for handling files sent to the recycle bin. On other operating systems that function will be nil, and the default behavior provided by `move-file-to-trash`

is used instead.

In Emacs 23.2 new functionality was added to ensure Emacs conforms to the *freedesktop.org specification* used by all major, free desktop environments. The new variable is `trash-directory`

and determines where Emacs will put the deleted files. If the variable is `nil`

the *freedesktop.org* trash can default is used, otherwise the variable must contain a path string to where the files are to be put.
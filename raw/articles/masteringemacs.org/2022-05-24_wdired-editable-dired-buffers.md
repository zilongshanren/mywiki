---
title: 'WDired: Editable Dired Buffers'
url: https://www.masteringemacs.org/article/wdired-editable-dired-buffers
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

A while ago I wrote an article about [Working with multiple files in dired](https://www.masteringemacs.org/article/working-multiple-files-dired). In the article I describe how you can work with files across multiple directories – for instance all the matches from a `find`

call – in a `dired`

buffer.

But wouldn’t it be great if you can combine the text editing capabilities of Emacs *on* the files themselves? Well, if you’re a long-time reader of this blog, you will recognize the rhetorical nature of the question and know instinctively that, yes, it is indeed possible.

## WDired

WDired – meaning writable dired – has been part of Emacs for a long time now. This feature is another hidden gem of Emacs, only briefly mentioned in a sub node in the `dired`

info manual.

Its mode of operation is simple: if any `dired`

or dired-derived buffer is switched to writable from read-only with the globally-recognized binding `C-x C-q`

, you can edit the dired buffer as though it were an ordinary buffer. If you are in editable dired mode the modeline for the dired buffer will say `Editable`

.

Any change you make to the buffer will remain unchanged until you commit them by typing `C-c C-c`

. To cancel the changes and revert to the original state you can type `C-c ESC`

.

## Configuring WDired

By default only the filename is editable, and for most that is good enough. There are, however, a couple of switches that let you change more than just the filename. If you set `wdired-allow-to-change-permissions`

to `t`

you can also edit the permission bits directly, although wdired will ensure you can only enter valid permission bits. If you want a free-form permission field without the system handholding, you can set it to `advanced`

.

Another feature of wdired is its ability to rewrite symlinks. By default `wdired-allow-to-redirect-links`

is set to `t`

, meaning you can by default change the symlinks in Editable mode.

Two useful “safety” variables are `wdired-use-interactive-rename`

which if set to `t`

will prompt for every filename change you have made you when you commit the changes with `C-c C-c`

, and `wdired-confirm-overwrite`

asks if you want to overwrite files if your altered filenames conflict with existing files.

If you are a keen user of Emacs macros you may want to configure `wdired-use-dired-vertical-movement`

as it governs how where the point is put when you navigate up and down the dired list. You can set it to one of three switches: `nil`

, meaning it will not do anything out of the ordinary; `sometimes`

, meaning Emacs will move the point to the beginning of filename if the point is *before* it; and `t`

, meaning Emacs will always, unequivocally move the point to the beginning of the filename, mirroring the behavior in normal dired mode.

## Using WDired

Probably the most useful part of WDired is the ability to edit filenames as though they were ordinary lines of text in a buffer. Most commands work as you would expect, including rectangle functions! Only the filename portion of text killed with the rectangle kill command `C-x r k`

are killed. WDired is fairly intelligent and will only let you edit portions that make sense: you cannot change the file size, for instance, as that portion of the buffer is set to read only.

Replace regexp works well, but don’t expect `^foo`

to work as the filename is not actually at the beginning of file. Provided you express your regexp so it only affects the filename-portion of the dired buffer, you’re golden. This is a slightly annoying limitation but one worth living with. The functionality afforded by WDired is amazing: regexp replace, `[upcase/capitalize]-word`

; elaborate macros – they all work.
---
title: Searching and Editing in Buffers with Occur Mode
url: https://www.masteringemacs.org/article/searching-buffers-occur-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

The Emacs `M-x occur`

command (also bound to `M-s o`

) is a useful replacement for GNU `grep`

when your only requirement is searching open buffers in Emacs. Like `grep`

, Occur filters lines using regular expressions. And much like `M-x grep`

the matching lines are hyperlinked so you can jump to the location of the match.

`M-x occur`

filtering a buffer. Pressing

`e`

makes it editable; type `C-c C-c`

to commit the changes you have made back to the source buffer.Because Occur is so useful, it’s the first thing I reach for when I:

- Don’t want to iterate my way through the matches with Isearch (
`C-s`

); - Need or desire an overview of all the matches;
- Want to step through the matches with
`M-g M-n`

or`M-g M-p`

.

The Achilles’ heel is that it only works on a single buffer. If you want to match against multiple buffers you must use the sibling commands `M-x multi-occur`

or `M-x multi-occur-in-matching-buffers`

. Both work well for that purpose, but they do require that you specify what you want Occur to search for.

When you do use Occur, you can tell it to rename the buffer (if you desire more than one open Occur buffer) by pressing `r`

. You can also re-run the occur command by pressing `g`

in the output buffer. The latter is useful if you combine it with `M-x auto-revert-tail-mode`

in the buffer(s) that you’re searching.

Another useful feature is its support for the compilation mode commands `next/previous-error`

(`M-g M-n`

and `M-g M-p`

, respectively), as you can step through the matches one by one. [Combine it with keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) and you can build a sophisticated tool capable of processing an arbitrary amount of data, provided you source your matches for the keyboard macro by jumping to the next or previous match.

In a similar vein, you can enable follow mode in the `*Occur*`

buffer by pressing `C-c C-f`

, and future calls to `M-n`

and `M-p`

in the `*Occur*`

buffer will automatically jump to the correct match in the source buffer.

## Displaying Context Lines

If you customize `list-matching-lines-default-context-lines`

you can tell Emacs to show contextual lines around the match. Set it to `2`

, and you’ll see the preceding and following two lines of each match Occur finds.

## Editing Matches in an Occur Buffer

One blow-your-mind feature is editable Occur! `M-x occur-edit-mode`

(also bound to `e`

) engages the edit mode in Occur. You’re free to make what ever changes you like, Emacs will reflect the changes you’ve made back into the source buffer when you type `C-c C-c`

.

Exceptionally powerful, and works well with [keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) or [advanced search and replace](https://www.masteringemacs.org/article/evaluating-lisp-forms-regular-expressions).

Combine with `M-x multi-occur-in-matching-buffers`

for bulk editing across a range of buffers.

## Making Occur a little more useful

My only complaint about occur is that it does not let you quickly search a set of buffers that match a specific major mode – arguably a common use case if you’re a programmer. The code seen below will search all open buffers that share the same mode as the active buffer.

```
(eval-when-compile
(require 'cl))
(defun get-buffers-matching-mode (mode)
"Returns a list of buffers where their major-mode is equal to MODE"
(let ((buffer-mode-matches '()))
(dolist (buf (buffer-list))
(with-current-buffer buf
(when (eq mode major-mode)
(push buf buffer-mode-matches))))
buffer-mode-matches))
(defun multi-occur-in-this-mode ()
"Show all lines matching REGEXP in buffers with this major mode."
(interactive)
(multi-occur
(get-buffers-matching-mode major-mode)
(car (occur-read-primary-args))))
;; global key for `multi-occur-in-this-mode' - you should change this.
(global-set-key (kbd "C-<f2>") 'multi-occur-in-this-mode)
```
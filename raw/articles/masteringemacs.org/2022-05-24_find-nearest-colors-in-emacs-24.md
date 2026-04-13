---
title: Find nearest colors in Emacs 24
url: https://www.masteringemacs.org/article/find-nearest-colors-emacs-24
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

As I mentioned in my *What’s New In Emacs 24* series ([part one](https://www.masteringemacs.org/articles/2011/12/06/what-is-new-in-emacs-24-part-1/), [part two](https://www.masteringemacs.org/articles/2011/12/12/what-is-new-in-emacs-24-part-2/)) Emacs 24 can now sort the colors in `M-x list-colors-display`

based on the RGB or HSV *distance* to another color. This is perhaps of most interest to web designers or color theme creators, but it’s still a fun little addition.

Unfortunately, this functionality is only available through the customize interface, and that means most people will never bother with it at all. Hence, I’ve written two helper commands below to make this neat addition to Emacs 24 easier to use.

If you’re looking up a named color (like `red`

) then it must exist in `M-x list-colors-display`

; if it’s an HTML color then as long as it is valid it will work.

To use it, you must invoke `M-x find-nearest-color`

and enter the name of a color. The other command, `find-nearest-color-at-point`

does just that: it looks at what your point is on and tries to look it up.

```
(defun find-nearest-color (color &optional use-hsv)
"Finds the nearest color by RGB distance to COLOR.
If called with a universal argument (or if USE-HSV is set) use HSV instead of RGB.
Runs \\[list-colors-display] after setting `list-colors-sort'"
(interactive "sColor: \nP")
(let ((list-colors-sort `(,(if (or use-hsv current-prefix-arg)
'hsv-dist
'rgb-dist) . ,color)))
(if (color-defined-p color)
(list-colors-display)
(error "The color \"%s\" does not exist." color))))
(defun find-nearest-color-at-point (pt)
"Finds the nearest color at point PT.
If called interactively, PT is the value immediately under `point'."
(interactive "d")
(find-nearest-color (with-syntax-table (copy-syntax-table (syntax-table))
;; turn `#' into a word constituent to help
;; `thing-at-point' find HTML color codes.
(modify-syntax-entry ?# "w")
(thing-at-point 'word))))
```


If you hack a lot of elisp you will notice that I’ve chosen to hack the syntax table (temporarily) to make `thing-at-point`

play nice with the HTML color syntax (`#ABCDEF`

) as the character – and this will depend on your mode and thus your syntax table, of course – `#`

is rarely a “word” constituent. I think this is a much cleaner way of “getting” things at point than messing with regular expressions as you will inevitably end up reinventing most of `thing-at-point`

doing so.
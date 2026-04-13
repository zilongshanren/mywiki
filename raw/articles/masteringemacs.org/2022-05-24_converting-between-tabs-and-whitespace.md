---
title: Converting between tabs and whitespace
url: https://www.masteringemacs.org/article/converting-tabs-whitespace
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

It’s not an uncommon occurrence to find yourself editing a file that uses tabs instead of whitespaces, or vice versa. Thankfully, Emacs has facilities in place that make it possible to easily convert between tabs and spaces.

The commands `tabify`

and `untabify`

do just that; they convert the region to tabs or whitespaces. When you `untabify`

or `tabify`

, Emacs is smart enough to realign your code, so it should look the same after the replacement has taken place. When you use either command, the variable `tab-width`

is also used to determine the indentation level.

One important point, though, is that `tabify`

and `untabify`

**does not discriminate** when it replaces tabs with spaces and vice versa, so that means tabs or whitespaces in strings may suffer. Be careful.

It’s easy to miss tabs or mistake them for whitespace, so I recommend you give `M-x whitespace-mode`

a try also. It has a large number of highlighters to detect errant tabs; trailing whitespaces; and much more!

There are no comments. Why not write one?
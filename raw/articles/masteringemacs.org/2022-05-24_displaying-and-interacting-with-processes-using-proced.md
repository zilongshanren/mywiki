---
title: Displaying and Interacting with processes using Proced
url: https://www.masteringemacs.org/article/displaying-interacting-processes-proced
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re a regular user of the commandline tools `top`

or `ps`

then I have good news for you: there’s an Emacs command that does that and *it works on Windows too!*

The command is `M-x proced`

and it is modelled on `M-x dired`

(but it is not built on top of dired) and it does shadow most of the common navigational aids: `n`

and `p`

move down and up and `g`

refreshes the buffer, for instance.

It’s also feature rich; by combining the utility of `ps`

with the sortable, columnized and interactive system of `top`

you get the best of both worlds.

What I like about it is that it’s a buffer like any other in Emacs. So if you’re keeping your eye on a handful of processes you can use `highlight-phrase`

to highlight the strings you want to visually separate from the rest. It is also, in true Emacs tradition, very customizable – but I’ll get to that a bit later.

## Marking, Sorting, Filtering and Formatting Columns

By default you will be given the `short`

formatting but you can change the number of displayed columns by typing `F`

. You’ll be shown a prompt where you can select from `short`

, `medium`

, `long`

and `verbose`

.

You can also change the filtering – which defaults to `all`

– by pressing `f`

. Like the formatting key above you are given a list of common filter types. Furthermore you can filter by any of the visible columns by moving your point to it and pressing `RET`

. It will incrementally filter so you can repeatedly filter as much as you like – this is a very handy feature. Refreshing the buffer with `g`

does *not* reset it: you must change your filter with `f`

.

Like dired you can mark processes with both `d`

and `m`

(they do the same thing) and unmark with `backspace`

and `u`

. You can mark and unmark all processes with `M`

and `U`

. And finally you can then filter the marked processes with `o`

.

There are some specialty mark commands as well. The command `t`

will invert your marks and `C`

and `P`

will mark the children or parents of the process point is on.

Finally you can sort by columns as well. All the sort commands are bound to `M-x proced-sort-xxx`

and to the prefix menu `s`

:

| Command | Description |
|---|---|
`s c` | Sort by CPU % |
`s m` | Sort by Memory % |
`s p` | Sort by PID |
`s s` | Sort by Start Time |
`s t` | Sort by CPU Time |
`s u` | Sort by User |
`s S` | Sort by other column |

If you want to sort by a column not bound to a key you must use `s S`

where you are then prompted for the name of a column to sort by.

## Sending Signals and Interacting with processes

Unsurprisingly sending POSIX signals is fully supported by Emacs. This is done using the Elisp function `signal-process`

. Because of that all signals are sent using the uid of the Emacs process proced is running in. Conceivably proced could be changed to call out to userland command `kill`

(using an external command **is** supported) and, by combining it with TRAMP for sudo elevation it could kill processes owned by other users. Sadly that functionality does not currently exist but abusing the `default-directory`

variable might work.

To send a signal mark the processes you want to signal, or alternatively put your point on the target process, and press `k`

or `x`

. You will be shown a list of target processes and you can optionally change the default suggestion of `TERM`

to something else.

When the signal(s) have been sent you can review the log by pressing `?`

.

## Understanding & Customizing Proced’s Internals

Proced is very flexible and it also supports the customize interface. You can access this inferface by typing `M-x customize-group proced RET`

.

Proced will use the Elisp function `list-system-processes`

to retrieve all the known PIDs and then call `process-attributes`

on each one of them to fetch the process details. The good news is that Proced does not parse the output of `ps`

or `/proc`

directly but relies on Emacs’s compatibility layer to make sense of everything: this also means it works rather well on Windows.

Proced can auto update the display and you can enable this for a Proced buffer by running the command `proced-toggle-auto-update`

and it will update every `proced-auto-update-interval`

which is by default 5 seconds.

To make Proced auto update by default you must add a hook:

```
(defun proced-settings ()
(proced-toggle-auto-update))
(add-hook 'proced-mode-hook 'proced-settings)
```


You are free to customize other settings in this mode hook in much the same way you would other mode hook functions.

If you’re really serious about tweaking the way the columns are displayed you can try your hand at editing the alist variable `proced-grammar-alist`

. It controls how sorting, justification and string formatting works for each of the process attributes returned by `process-attributes`

.

You can also alter the default Proced filter by changing `proced-filter`

from `user`

to something else. Creating your own filter is also possible by adding to the `proced-filter-alist`

; in fact this functionality lets you do rather complex things such as calling a custom function for every process attribute.

The default sort and sort order (descending or ascending) is governed by `proced-sort`

and `proced-descent`

respectively.

There are many more customizable options and the author of Proced, Roland Winkler, has done a great job ensuring they’re accessible from Emacs’s customize interface.

It goes without saying that Proced is a both feature rich and customizable. I think it’s a very capable replacement for most `ps`

and `top`

use cases, but like so features in Emacs almost nobody has heard of it.
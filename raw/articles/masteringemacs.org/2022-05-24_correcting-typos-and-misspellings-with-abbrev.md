---
title: Correcting Typos and Misspellings with Abbrev
url: https://www.masteringemacs.org/article/correcting-typos-misspellings-abbrev
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I’ve previously talked about [using Hippie Expand](https://www.masteringemacs.org/article/text-expansion-hippie-expand) to expand text. It’s great; if you’ve not used it, you should give it a try. But it’s just one of many different ways of expanding the text at point and turning it into something else.

The most basic of these systems in Emacs is *abbrev*. *Abbrev* is, as its name may slyly allude to, intended for abbreviations or unconditional text replacements. It works as you type: you don’t need to do anything to trigger it, provided you’ve told *abbrev* to replace one word with another, either globally or locally to a particular major mode. Because *abbrev* silently expands stuff with no fanfare, that makes it great for auto-corrections.

Many moons ago, I borrowed Wikipedia’s [list of most common misspellings](https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines) and turned them into *abbrev* entries. It’s a total game changer. And the best thing about it is that it silently replaces the matches. Sure, it’s no replacement for a spell checker, but it’s good enough to catch a lot of common keyboard fumbles.

There are two ways of creating *abbrev* entries, and two ways of defining where they trigger. *Abbrev* entries trigger either in the major mode you define the *abbrev* in, or globally in all major modes.

In order to add *abbrev* entries you need to decide if you want to do it the *inverted* way – where you place point at the end of the word you want to *replace* – or the other way around.

Key Bind | Purpose |
`C-x a g` | Define an abbrev globally |
`C-x a l` | Define an abbrev locally |
`C-x a i g` | Define an inverted abbrev globally |
`C-x a i l` | Define an inverted abbrev locally |

You also need to enable it, as it’s not by default:

`(setq-default abbrev-mode t)`


I prefer the *inverted* approach as I’m more likely to catch the mistake in the buffer and then use `C-x a i g`

to enter the correct word. Emacs commits the new *abbrev* and fixes your word at point. This workflow works well for fix-as-you-go typos.

If you find yourself wanting to prevent *abbrev* from expanding the word at point, you can insert a literal space with `C-q SPC`

. That circumvents the *abbrev* trigger mechanism that one time.

Emacs will ask you when you exit if you want to save your abbrevs. But you can call `M-x abbrev-edit-save-buffer`

to explicitly save it, and `M-x edit-abbrevs`

to open the file directly for editing. I recommend you `M-x customize-group abbrev`

as there’s a number of interesting settings you can tweak, like the filename for the abbrevs, and whether you want it to handle word casing.

As it’s designed for whole-word expansions, *abbrev* is therefore not able to expand your *abbrev* entries if they’re part of a larger word. There *is* a way to do this – using `M-'`

as a marker to indicate that *abbrev* should expand anyway – but I find it more trouble than it’s worth.

Let’s quickly go over one (of many) ways you can import Wikipedia’s word list.

## Importing the Common Misspellings Word List

As the link above shows, the word list looks like this:

```
...
countrie's->countries, countries', country's
...
manoeuverability->maneuverability
manouver->maneuver, manoeuvre
...
```


As you can see, the word list may offer up alternatives. Some of them with grammatical inflections or regional spelling variations.

If you don’t want to manually sift through which ones you prefer, I recommend you just delete the ones with multiple matches:

`C-x h`

to mark the whole buffer.`M-x flush-lines RET , RET`

to flush anything with a`,`

on the line.

And… done.

To load the remaining entries into your *abbrev* table, I would recommend a keyboard macro:

- Place point at the beginning of the buffer with
`M-<`

. `F3`

to start macro recording.- Search for
`->`

with isearch (`C-s`

) and press`RET`

at the first match. - Your point is now after
`->`

, so`<backspace>`

twice to delete it. - Type
`C-k`

to kill to the end of the line. (This obviously needs tweaking if you have`kill-whole-line`

set… but this is yet another reason why you should never do that.) - Type
`C-x a i g`

to correct the preceding word. At the prompt, press`C-y`

to yank the previously-killed word into the buffer. Press`RET`

to accept. - Stop macro recording with
`F4`

. - Type
`C-0 C-x e`

to execute the macro forever, until it reaches the end of the buffer. It might take 5-10 seconds.

You’re done. Don’t forget to save the changes and enable `M-x abbrev-mode`

to test that it works.
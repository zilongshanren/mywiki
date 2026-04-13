---
title: 'discover.el: discover more of Emacs using context menus'
url: https://www.masteringemacs.org/article/discoverel-discover-emacs-context-menus
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

![ISearch context menu](../../assets/88402eb7b273d472.png)


## On Discoverability

Over the years I have written tens of thousands of words encouraging Emacs users of all skill levels to learn more about Emacs: either adopting work flows I personally find useful, or by covering in great detail a particular feature or package in Emacs.

What’s interesting to me, looking back, is that despite all the detailed manuals that ship with Emacs and the self-documenting nature of Emacs – most of Emacs is just not that discoverable. It takes time and patience. Even if you use a feature often (and I think `dired`

is a perfect example here) there are just so many overlooked nooks and crannies. For instance, did you know that there’s a command called `M-x repunctuate-sentences`

? It puts two spaces at the end of each sentence. Useful, if you believe in that style (your author does not) – but hidden.

I am entirely self-taught in Emacs and never had the requisite “graybeard” to teach me Emacs. It took a concentrated effort to educate myself. You have to read the manual, yes, but that’s often not enough; you have to read the source, experiment with elisp, and then read the source some more. Now, don’t get me wrong: that’s fun and all, but you don’t always have time for that.

Emacs suffers from the classical case of hiding things behind other things. How do you discover stuff about `dired`

? Why you just `C-h m`

to describe the active modes in the buffer, and in there, hopefully, is an unabridged list of relevant key bindings to the mode you’re using. Or maybe you try your luck with the info manual; perhaps you just read the source. Yet… if it’s that “simple”, how come so few people move beyond the basics? Clearly the tools we provide aren’t working well enough. There are few things in Emacs that are truly difficult to *grok*. The undo ring confuses people until they “get” it; recursive editing might be another; but there’s generally not that many things – it’s just muscle memory, practice, and awareness.

Taking a brief step back. There’s a game out there called *Dwarf Fortress* (you may have heard of it.) It’s an awesome game: eschewing the modernity of graphics and, ahem, good usability design, for a complex menu-riddled interface and colorful ASCII symbols. Does that ring a bell? Most people try and fail to learn *Dwarf Fortress* for the same reason people fail to learn Emacs. And they fail because Dwarf Fortress does a poor job aiding discoverability. It’s a very rewarding and deep game that’s *oh so close* to attracting a much larger audience – much like Emacs.

So I’ve been thinking long and hard about this problem for a considerable while and what *I* can do to try and improve it, beyond just writing articles. My vision (or call it a moment of clarity) for what Emacs needs to do to improve its discoverability. That’s why I sat down and wrote a proof-of-concept prototype that captures what I think Emacs needs to do to make its myriad commands more accessible and open. I’ve built this prototype on top of the popup system used in Magit.

When I first started using Magit, [a Git mode for Emacs](https://www.masteringemacs.org/articles/2013/12/06/introduction-magit-emacs-mode-git/), about a year ago I was enthralled by the clean and simple popup windows it used for actions, switches and arguments. I saw opportunities well beyond Magit; indeed, the lead maintainer of Magit, Jonas, is busy unstitching and rewriting it as we speak, having realized that many people find it useful.

Independently of him, I did the same work but rewrote parts of it to handle a different use case: Emacs itself. Instead of constructing command line arguments to git, why not build on the idea but use it for Emacs? So that’s exactly what I’ve done.

I call it discover.el - because that’s what I hope it’ll do; help you discover things.

## discover.el

### Overview

For now discover.el only supports a couple of key groups and one mode. I’ve decided to tackle `dired`

, as it’s a complex key-based mode; the register keys in `C-x r`

, as they’re hard for people to grasp and remember; and the Isearch keys in `M-s`

, because they are more common. All three cover a cross section of common to uncommon; large to small. The ultimate goal is to blanket Emacs with these *context menus*. Now, I don’t imagine it as a set of training wheels for beginners but a tool for expert Emacs users as well. I have altered the code I inherited from Magits’ popup system so you can set related lisp variables through the minibuffer and toggle boolean variables through the interface. Doing that without context menus is a *major* pain in the neck. This system encourages the use of the more esoteric variables and hidden switches, and it’s all done through `let`

-binding – so once the command’s run its course the values will revert to the old settings.

Now, as dired maps most of its commonly used keys to a single character, I have opted to rebind `?`

, an anaemic and unhelpful “help” system, to the new context menu.

For register & friends, I have opted to replace the key group wholesale. `C-x r`

is now a bound key and will display the context menu when you type it.

For isearch, I also replace the key group. I have decided to take it one step further and expose a lisp variable `case-fold-search`

. Toggle it if searches and matches should ignore case.

So far it works great. In fact, it works really well. There are no immediate disadvantages that I can see. It even works with macros.

It *is* a bit unpolished (as you’d expect from a prototype), and for now the commands and the descriptions mirror those of the original bindings, so I may end up tweaking the descriptions. Another is the ordering; for now, it’s loosely grouped together, but there’s a lot of scope for improvement. It’s my goal to start adding unbound commands to their respective areas to encourage their use.

So how is it like using it then? I also think it feels very natural. It’s an immense aid for things like dired. Once you get used to having it, it’s as though it’s always been there. The added bonus is, if you’re ever good enough to not need the popups, you can stop using discover.el. But you may not want to. I have several ideas I want to implement, such as:

**Save/restore toggles and arguments**By letting you tie save points to various things you do, you can create multiple roles depending on what you need them for. The added benefit is that it shouldn’t be too hard a thing to add.

**At-a-glance consoles**Use the context menus to display information in addition to actions, switches and arguments. Why not manage your debugging through a context menu? Make it persist between actions and you can show/hide it whenever you need it. Or why not let you step through, over, or edit each action in an Emacs macro?

**Custom context menus for your most-used comands**Use discover to create your own context menus for your own commands

**Interact with external command line tools**Like Magit, but for other external commands. Plenty of opportunity to do something really cool.


So it’s a prototype. I need more people to help test it and help with bug fixes and feature additions.

Even if you’re an expert Emacs user I still think there’s a lot of value to be had from using this tool; there’s bound to be features you didn’t know about, and the ability to toggle variable and set variables outright is extremely useful, as the changes you make are let-bound and will only affect the next action you call.

### The Future of discover.el

Aside from fulfilling the ideas I mentioned earlier, and fixing outstanding bugs, the biggest task is to migrate existing key groups and mode-specific keys to improve discoverability. The good news is this isn’t too difficult. Most of it can be done with `C-h m`

and a macro; or even better, a bit of elisp magic to generate what we need.

But the big one is people using it. I think this has a real potential to greatly improve the user interaction in Emacs, for beginners and experts alike. Regardless of whether you’re using it or not – tell your coworkers and friends. Tweet about it, too, if you use that. If you’re old fashioned and prefer to use a bugle – that’s fine too.

### How do I get it ?

**UPDATE:** Discover is now available in MELPA!

You can get it from the [discover.el github page](http://www.github.com/mickeynp/discover.el). For now there are no fancy packages - sorry. I’ll need to get it added to el-get.

The discover.el package [also requires makey.el](http://www.github.com/mickeynp/makey), the bastard child of Magit’s key popup system.

To install it, clone both packages and add them to your load path, then add this to your init file:

```
(require 'discover)
(global-discover-mode 1)
```


And you’re done. Use the isearch or register keys as you normally would. You can access the new dired context menu by pressing `?`

in dired.

Go forth and discover :)
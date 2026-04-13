---
title: What is new in Magit 2.x
url: https://www.masteringemacs.org/article/what-new-in-magit-2x
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Like it or not, Git is here to stay, and for many Emacs hackers the best interface to Git is not *Git Porcelain* – the byzantine commandline interface that we all love to hate – but *Magit*, a much-improved Git interface for Emacs.

**NOTE**: If you are looking for a Magit tutorial, then I recommend you read [my introduction to Magit](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git).

## Installing Magit 2.x

*Check your current Magit and Git version by running M-x magit-version*

The biggest change is the updated Git requirement. You now need **Git 1.9.4 or later**. If you’re using a recent-ish version of Ubuntu (or its derivatives) then bad luck: the antediluvian version available from its package manager is too old.

To upgrade Git itself to 2.x you can run these commands:

```
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git
```


Next, confirm on the commandline that you are using the newer version:

```
$ git --version
git version 2.4.6
```


### Upgrading Magit in Emacs

The first (and only) source of truth is the official manual: [Updating from an older release](http://magit.vc/manual/magit/Updating-from-an-older-release.html#Updating-from-an-older-release). But the instructions boil down to simply removing all traces of the old `magit`

, `git-commit-mode`

and `git-rebase-mode`

packages. Delete the directories from your `elpa/`

directory and then – the horror – exit and restart your Emacs. And no, you cannot avoid this step. You really have to restart Emacs.

### Fresh Magit Install

Simply install Magit from your local package manager in Emacs.

## What’s new in Magit 2.x

The first thing you’ll notice when you run `magit-status`

(I bind it to `F10`

) is how fast it is. A lot of work has gone into making Magit a lot quicker, and the effort has paid off handsomely.

The look and feel has changed slightly as well. The colors are different, and Magit now lets you change the look and feel by customizing additional faces. Type `M-x customize-group magit-faces`

to see all the faces.

Another new feature is that Magit will now tell you about unsaved buffers. That’s an important change as you sometimes forget to save things (meaning Git doesn’t know about them, and therefore Magit doesn’t either) and you end up only committing some of your work instead of all of it. All in all, a really handy addition.

The biggest change is the altered workflow. Magit 2.x deviates sufficiently from its predecessor that it will take you a while to re-train your muscle memory.

### A Manual

Magit 1.x had a fine info manual but a lot of people found it hard to get up to speed simply by reading it. But, in all honesty, considering the excellent engineering effort, I never had a problem with the community (myself included) providing blog posts, tips and additional information on how to use Magit.

Magit 2.x has a far more in-depth manual, covering all key bindings and popups available.

You can [find it here](http://magit.vc/manual/magit/index.html#SEC_Contents) or in `C-h i`

as a separate info manual.

### Rebasing

Rebasing is now bound to `r`

. To do an interactive rebase you’d type `r e`

, but its default mode is to ask you to rebase against your current branch. Useful if you want to manicure your own branch, but not useful if you usually do it as part of a rebase onto another branch (say `master`

) as that behavior is now (seemingly) gone. So, you now have to `r e`

*first*, and *then* `r r`

onto another branch. Not a big deal.

One advantage of the new `r e`

system is that you are given a list of commits in your current branch to rebase *from*, instead of the older system where you had to enter a commit to rebase from (like `HEAD~5`

) — so for interactive rebasing your current branch, the newer system is better.

Another new feature is the ability to edit (`r s`

) and reword (`r w`

) commits using the rebase system. Useful, as you can select a commit from the same list as before to alter and Magit will automatically interactively rebase just that one commit.

Dealing with merge issues during rebase is common, and Magit will now show you how far along in the process you are, along with a list of the rebased commits. Very useful.

### Cherry Picking

Magit’s always had a neat cherry picking functionality, letting you cherry pick arbitrary commits from the commit log. I use it frequently by combining it with range logs to look at commits in other branches.

The cherry pick interface is available on `A`

, and you can use it in more places. Practically anything the point is on that is a commit is cherry pick-able in the UI now.

### Per-repository settings

You can now control Magit with per-repository settings. What that actually means is that in addition to Git repository-specific configuration you can now do the same for Magit by using Emacs’s *directory local variables*. See the info manual entry `(emacs)Directory Variables`

.

### Changing popup defaults

Personally, this is one of my favourite features. Every Magit popup now lets you set the default switches and arguments Magit should use. `C-c C-c`

and `C-x C-s`

now set and save the defaults, exactly like Emacs’s *Customize* interface.

### Git Blame

Magit 1.x had a useful in-buffer blame interface called `M-x magit-blame-mode`

. It had its limitations, and Magit 2.x fixed most of them.

First and foremost, the interface is different. For one thing, the command is now `M-x magit-blame`

.

| Command | Description |
|---|---|
`RET` | Shows commit at point |
`SPC` | “DWIM”. Show commit or scroll down |
`DEL` | As above, but scroll up |
`n` | Move to next chunk |
`p` | Move to previous chunk |
`N` | Move to next chunk of the same commit |
`P` | Move to prev. chunk of the same commit |
`t` | Toggles showing commit headings |
`b` | Opens Blame popup |
`b b` | Blame commit at point |

All in all, the commands above work as you would expect. `b b`

deserves a special mention as it will pick the commit at point and show it to you — useful if you’re trawling through the history of a file.

Your typical workflow would be `M-x magit-blame`

then `n`

and `p`

to move around (or your usual movement commands) and `RET`

to view the commit and its diff, and `b b`

to view the file’s revision.

### The Branch Manager

Also known as “Ref Manager”, as that is technically what it shows — anything in Git that is a ref. That includes local branches, remote branches, tags, and so forth.

It switched keys and it’s now bound to `y`

.

### Previewing Merges

You can preview a merge now with `m p`

. If you’re afraid of merges, or if you don’t want the hassle of undoing it after the fact, you can get a diff view of what’ll change and if there are any potential merge conflicts. Very Useful.

### Checkout

Checking out is a smoother, more improved experience. You can now set and unset the upstream instead of relying on the push command to do it for you. I always thought this was the weakest part of Magit 1.x but I am glad it has been rectified.

## In Conclusion

Magit 2.x is excellent, and it basically builds on what made Magit 1.x fantastic, too. Yes, things have moved around a bit, but it’s a much better experience all around. It’s hard to capture all the things that makes Magit 2.x greater – the sum of its parts, I suppose. The unified approach to “Do What I Mean” when you highlight a commit with point is one of them; the updated rebase and commit interface is another. The new Ref Manager (`y`

) is also much improved.

All in all, a solid upgrade, and an incredible multi-year development effort.
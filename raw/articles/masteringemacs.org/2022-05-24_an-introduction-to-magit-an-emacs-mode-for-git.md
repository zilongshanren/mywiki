---
title: An introduction to Magit, an Emacs mode for Git
url: https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Magit is the sweetener that masks the bitter taste you get when you have to commune through algebraic brevity with git. Magit – unlike other user interfaces bolted on top of a command line version control system – is faithful in its adherence to git’s vocabulary and capabilities.

Although Magit is now firmly entrenched in Emacs canon, it’s still a complex piece of software because, well, so is git. And so this tutorial sets out to help you make the transition from command line – or Emacs’s builtin VC – to Magit.

## Getting Started

To use Magit, type `M-x magit-status`

or `C-x M-g j`

. You can also type `C-x p m`

to open a Magit status buffer in your project root, if you use that functionality in Emacs.

The status window is the most common entryway into Magit, but it is not the only one.

If you’re a user of Emacs’s *VC* – a wonderful one-size-fits-all version control abstraction layer built into Emacs – then you’ll have to learn how to operate Magit as there is little overlap in key bindings. Having said that, I happily mix-and-match both; there are some commands I find more ergonomic.

## Magit Status Window

The first thing you’ll notice about the Magit status window is that it plays nice with your window configuration when you open it, and when you close it with `q`

.

Magit works in much the same way as `M-x dired`

(or indeed `C-x v d`

, the VC Directory status window) as it prefers single-character key bindings. That’s a smart decision, as you’ll often find yourself repeating the same commands over and over; and like dired, you wouldn’t ordinarily *edit* anything in Magit’s many buffers anyway.

The status window is similar to `git status`

as it offers an overview of your repository. But unlike `git status`

Magit summarizes more than just the staged and unstaged changes. You can also see unpulled/unpushed commits and your stashes. There is a header containing: local and optional remote; the latest tag, if any; and what HEAD points at.

### Staging and Unstaging

One major benefit of using a UI to manage your git interactions is the ability to quickly browse staged and unstaged changes. Not only can you stage or unstage whole files, but you can also do so with the individual hunks in a diff – even regions of text, if a hunk is not granular enough.

Using a simple system of tree-like sections, you can expand or collapse sections, files, or hunks. For more granular control, you can use `M-1`

through to `M-4`

for all the files; and `1`

to `4`

for the selected section; and `TAB`

and `S-TAB`

to cycle the current section or all sections. Most tree-like sections of Magit behave this way; not just on the status window.

- Basic Navigation
Being Emacs,

`n`

and`p`

moves between logical entries in all parts of Magit. That’s your bread-and-butter navigational aid; the usual movement keys in Emacs still work:`C-n`

and`C-p`

, and so forth.There’s also

`M-n`

and`M-p`

that move between sibling sections, such as between each file or between each section (like staged or unstaged).- Staging and Unstaging, and Working with Hunks
You can use

`+`

and`-`

to enlarge or shrink each hunk and`0`

to reset to the default. You can also type`H`

to refine the hunk for additional diff highlighting.Pressing

`RET`

will go to the file where the change is made. It works on both hunks and files.To stage or unstage you can type

`s`

or`u`

to stage/unstage the item (be it a whole file, or just a hunk).I frequently find that a hunk is not granular enough if I want to manicure what goes into my commits. To work around that, you can navigate into a hunk and stage (or unstage) line by line.

If you select a region, you can instead stage or unstage just that region.

- Discarding Changes
If you want to discard something you can do so with

`k`

. It works on staged or unstaged files, hunks and untracked files.

### Committing Changes

To begin committing changes in Magit, type `c`

. You’ll see a window pop up – that popup window is the main way you interface, and amend, the parameters Magit must pass to git. Note that Magit may add actions that don’t exist as a singular command or concept in git. Instead they exist only in Magit and serve as a shortcut to save you time.

Part of the appeal of Magit is that you can tailor each command with ease. But if you don’t need that, just tap `c`

again to open the commit message buffer.

The commit message buffer appears when you’re ready to finalize the commit with a message. There’s a number of handy key bindings you should know about:

`M-n`

and`M-p`

They cycle through the commit message history ring. So if you write a long commit message but realize you need to amend some of the staged changes before you commit it, you can recover your draft commit message by tapping

`M-p`

.`C-c C-c`

Commits the changes with the message you’ve written.

Magit checks if your message is too long and warns you if you breach the ‘unwritten’ rule that the first line of a git commit message is self-contained and no longer than around 70 characters. (That way, it won’t get truncated when you use

`git log --one-line`

.)This limitation does not apply to subsequent lines or paragraphs you write. (But I recommend you adopt that rule if you don’t follow it already.)

`C-c C-k`

Cancels the commit. You’re returned to the Magit window and you can resume the commit if you like by repeating the

`c c`

key combo.

### The Commit and Reference Log

#### Filtering and Searching the Commit Log

Git on the command line is frustrating because you spend so much of your time trying to feed information from one part of it into another. Doubly so if you frequently browse or filter git’s commit log.

Magit automatically enriches and displays any query it gets back from `git log`

, no matter how gnarly.

I particularly like `-G`

as a means of tracking down the history of changes made in git. But `-F`

is equally useful is you know that the things you are looking for exist in a commit message.

And although `l l`

is the most common way of browing the commit log, I also like `l o`

as you can query any revision and most refspecs. For instance, `master..development`

is a valid input here. Magit will, if your [minibuffer completion is up to the task](https://www.masteringemacs.org/article/understanding-minibuffer-completion), let you auto complete ranges.

#### Browsing the Commit Log

`git log`

. It's got a number of tricks up its sleeve in addition to pretty printing the output of your commit log history.I think one of the areas where Magit really shines is its multitude of switches to filter, sort and search your git history. Not only does it render the logs in beautiful technicolor, but it’s interactive and it has a large number of nifty integrations with other parts of Magit.

The first handy shortcut you should know is `l l`

. That opens the “short log”. In it, you will see a one-line commit message; the name of author; how long ago the commit happened; the tree structure of the git log; and various labels, like where HEAD is and where the branch markers are.

The log view is probably the most frequently used view for a lot of git users, as it’s an essential aid if you want to keep up with changes in a fast-moving code base.

Here’s a handful of keys I find useful:

`C-w`

copies the commit hash of the selected commit. If you select multiple commits you will*not*get multiple commit hashes!`x`

prompts you to reset your HEAD and index to a particular commit. When you execute it with a selected log entry, Emacs defaults to the commit hash of the selected entry.`v`

will revert to the commit.`d`

opens the diff view.`d d`

tries to DWIM: Do What I Mean. An Emacs term for guessing your intent.I recommend you select the range of commits you want to

`d d`

, as it’ll otherwise use`<commit>^..<commit>`

which is just the changes made in the selected commit against its parent.`d s`

diffs the commit against your staged changes;`d u`

against your unstaged changes.`a`

applies a patch of the commit(s) to your files / index.`A`

cherry picks the commit on top of your working tree.

For history rewriting this is perhaps the best entry point for it. You can also use it to quickly collect commits for squashes, fixups and commit message amendments.`r`

opens the rebase interface.`RET`

pops open the full commit log entry. You’ll see the diff, author, etc.If you switch back to the log and navigate up or down, the commit log entry follows the selected commit.


## Branches

Type `b`

to enter the branch view. Of note is `b b`

that checks out a different branch. That’s a common activity, so it has an easy mnemonic.

I also like `b l`

as it creates a local branch of a remote branch and ensures it tracks the remote.

Another life saver is `b s`

: it creates a *spin-off* branch. It’s a Magit concept, and it’s useful when you end up creating one or more unpushed commits that you’d rather spin off into a separate feature branch. Magit creates a branch of your choosing and moves the unpushed commits to the new branch.

The similarly-named *spin-out* `b S`

works much the same but it does not change your current branch to the new branch after completing the transfer.

## Pushing and Pulling

You can push to remotes with `P`

and pull from remotes with `F`

.

You’ll want `P p`

or `P u`

depending on how you configure your default upstream remote. For pulling it is much the same with `F p`

and `F u`

.

Because fast-forwarding and rebasing on pulling is so common, you can instruct Magit to default to this by typing `F C-x C-s`

after changing the settings.

## Dispatching from Anywhere

You jump straight into a log view from any git-enabled buffer with `C-x M-g`

. It works in much the same way as though you’d invoked the action from inside `M-x magit-status`

.

You can also access `M-x magit-status`

through Emacs’s builtin project management suite with `C-x p m`

.

## Dispatching Actions on Individual Buffers

Although it’s not immediately obvious, bound to `C-c M-g`

is Magit’s action dispatcher. *Note:* do not confuse it with the similarly bound `C-x M-g`

.

Unlike the regular Magit interface, this command works on the current buffer. For instance, `C-c M-g l`

opens the commit log history for just that file.

Every command you’d reasonably want to invoke against the current buffer is found in that dispatcher.

`C-c M-g t`

. A powerful feature.One command that you must experiment with is `C-c M-g t`

. It shows the historical logs that changed the function point is in. (So it’ll only work well if Emacs can infer the function point is in.) So if you want to trace changes made to a particular function in your git history, that’s the command to use.

It derives the nearest function using `magit-which-function`

, a derived version of `which-function`

. The latter is a mechanism Emacs uses in [Which Function Mode](https://www.masteringemacs.org/article/which-function-mode) to display the function point is in, in your modeline.

## Blaming / Annotate

You can enable interactive blame mode with `M-x magit-blame`

or `C-c M-g b`

. Having said that, this is one area where I prefer `C-x v a`

, the default VC annotation system.

## Reviewing & Manually Executing Git Commands

Type `!`

to open the command line invocation view. The `! !`

chord invokes a `git`

command at the root of your git repository. If you want to circumvent Magit’s interface, that is the command you should use.

If you want to review the actions it took, then type `$`

in the status window to reveal the commands Magit executed on your behalf.

## Get Help

If you’re lost, you can type `?`

to see an overview of action dispatchers available in that view.

You can type `C-h`

in a magit popup followed by a key binding to see the underlying elisp function it invokes. Useful if you want to read up on what a command does.

Magit also ships with an excellent Info manual: `M-x magit-info`

.

## Conclusion

Magit’s a great tool for both beginners and experts. Magit does not *hide* anything; instead, it surfaces capabilities only the most ardent and serious git experts know about. Git is obtuse and hard to use, and that is especially true once you delve into its more esoteric features, like pickaxing through commits with the log viewer, bisecting a range of commits, or interactively rebasing.

In fact, I’ve barely scratched the surface. But I think you know enough now to start using Magit as your daily driver.
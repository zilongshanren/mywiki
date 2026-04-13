---
title: 'PComplete: Context-Sensitive Completion in Emacs'
url: https://www.masteringemacs.org/article/pcomplete-context-sensitive-completion-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

When you [run a shell in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) you’re ceding control of most of that shell’s capabilities to Emacs itself. For the likes of `bash`

and `zsh`

that means you lose its native `TAB`

completion. In return you gain the many benefits and hand-tooled features that enrich your shell experience.

But `TAB`

completion is an essential aid when you’re hacking away at the command line, whether you do so inside or outside of Emacs. That’s why there’s a dedicated library in Emacs that auto-completes prompts: PComplete.

PComplete is the default handler for command line-style `TAB`

completion. That means when you’re completing at point in `M-x shell`

and [Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell) you’re using PComplete.

It’s a neat package, and in addition to the many completers already present, it’s easy to add your own, should the need arise.

## Programmable, Context-Sensitive Completion

To use pcomplete you won’t have to do anything. It’s beavers away in the background, and Emacs decides which of its many completion backends to use. Emacs does come with a decent list of completers for common Linux tools.

The following table lists the commands supported by shell mode (or indeed any mode that supports pcomplete, including Eshell.)

`bzip2`

Completes arguments and lists only bzipped files.

`cd`

Completes directories.

`chgrp`

Completes list of known groups on the system.

`chown`

Completes user and group perms, but only if you use

`user.group`

.`gdb`

Completes only directories or files with eXecute permission.

`gzip`

Completes arguments and lists only gzipped files.

`kill`

Lists signals if completed with just a

`-`

, otherwise it completes all system PIDs.`make`

Completes arguments and valid Makefiles in the directory. If you use the

`-f`

argument, such as`make -f FILE`

, it’ll switch to file completion instead.`mount`

Completes arguments and valid filesystem types if completed with

`mount -t TYPE`

.`pushd`

Identical to

`cd`

.`rm`

Completes arguments and filenames and directories.

`rmdir`

Completes directories.

`rpm`

Very sophisticated completion mechanism for most of rpm, the Redhat Package Manager. Context-sensitive completion for almost all commands, including package lookup.

`scp`

Completes arguments, SSH known hosts and remote file lookup (using TRAMP) if the format is

`scp host:/`

.`ssh`

Completes arguments and SSH known hosts.

`tar`

Completes arguments, including context-sensitive completion for POSIX arguments, and file name completion.

`time`

Completes directories and files with eXecutable permission.

`umount`

Completes arguments, mounted directories and filesystem types (like

`mount`

)`xargs`

Completes directories and files with eXecutable permission.


## Custom Completion

It goes without saying that a completion library called *programmable completion* is, well, programmable.

Adding simple parameter completion is easy. But if you want complex completion, you’ll have to read up on PComplete’s internals.

I’ll demonstrate how to add rudimentary support for `git`

.

The first thing we need to do is establish the order in which parameters must be given. For git, it’s somewhat consistent: `git [options] <command> [<args>]`


For now I’ll stick to the commands as that’s what people use the most anyway. The commands, in list form, are:

```
(defconst pcmpl-git-commands
'("add" "bisect" "branch" "checkout" "clone"
"commit" "diff" "fetch" "grep"
"init" "log" "merge" "mv" "pull" "push" "rebase"
"reset" "rm" "show" "status" "tag" )
"List of `git' commands.")
```


The syntax for Pcomplete is rather clever: it uses dynamic dispatch to resolve the elisp function provided it you follow the right naming scheme. You must name your functions `pcomplete/COMMAND`

or `pcomplete/MAJOR-MODE/COMMAND`

.

For command completion to work we’ll need a list of valid `git`

commands – in this case the ones in `pcmpl-git-commands`

– to pass to the command `pcomplete-here*`

.

```
(defun pcomplete/git ()
"Completion for `git'."
(pcomplete-here* pcmpl-git-commands))
```


Now when you try to tab-complete the first argument to `git`

it will list our commands. Sweet.

Let’s extend it further by adding support for the `add`

and `rm`

commands. I want the aforementioned commands to provide the standard filename/filepath completion if, and only if, the command is `add`

or `rm`

.

That is surprisingly easy to do with `pcomplete-match`

, a function that asserts a certain regexp matches a particular function argument index. Note that the call to `pcomplete-here`

is in a while loop. This is so you can complete as many files as you like, one after another. One advantage of `pcomplete-here`

is that it won’t display files you have already completed earlier in the argument trail – that’s very useful for a command like `add`

.

```
(defun pcomplete/git ()
"Completion for `git'."
;; Completion for the command argument.
(pcomplete-here* pcmpl-git-commands)
;; complete files/dirs forever if the command is `add' or `rm'.
(when (pcomplete-match (regexp-opt '("add" "rm")) 1)
(while (pcomplete-here (pcomplete-entries)))))
```


Ok, that was easy. Now let’s make it a bit more dynamic by extending our code to support the git `checkout`

command so it will complete the list of branches available to us locally.

To do this we need a helper function that takes the output of a call to `shell-command`

(more on [Executing Shell Commands in Emacs](https://www.masteringemacs.org/article/executing-shell-commands-emacs)) and maps it to an internal elisp list. This is easily done.

The variable `pcmpl-git-ref-list-cmd`

holds the shell command we want Emacs to run for us. It gets every ref there is and we then filter by sub-type (heads, tags, etc.) later. The function `pcmpl-git-get-refs`

takes one argument, `type`

, which is the ref type to filter by.

```
(defvar pcmpl-git-ref-list-cmd "git for-each-ref refs/ --format='%(refname)'"
"The `git' command to run to get a list of refs.")
(defun pcmpl-git-get-refs (type)
"Return a list of `git' refs filtered by TYPE."
(with-temp-buffer
(insert (shell-command-to-string pcmpl-git-ref-list-cmd))
(goto-char (point-min))
(let ((ref-list))
(while (re-search-forward (concat "^refs/" type "/\\(.+\\)$") nil t)
(add-to-list 'ref-list (match-string 1)))
ref-list)))
```


And finally, we put it all together. To keep the code clean I’ve switched to using a cond form for readability.

```
(defconst pcmpl-git-commands
'("add" "bisect" "branch" "checkout" "clone"
"commit" "diff" "fetch" "grep"
"init" "log" "merge" "mv" "pull" "push" "rebase"
"reset" "rm" "show" "status" "tag" )
"List of `git' commands.")
(defvar pcmpl-git-ref-list-cmd "git for-each-ref refs/ --format='%(refname)'"
"The `git' command to run to get a list of refs.")
(defun pcmpl-git-get-refs (type)
"Return a list of `git' refs filtered by TYPE."
(with-temp-buffer
(insert (shell-command-to-string pcmpl-git-ref-list-cmd))
(goto-char (point-min))
(let ((ref-list))
(while (re-search-forward (concat "^refs/" type "/\\(.+\\)$") nil t)
(add-to-list 'ref-list (match-string 1)))
ref-list)))
(defun pcomplete/git ()
"Completion for `git'."
;; Completion for the command argument.
(pcomplete-here* pcmpl-git-commands)
;; complete files/dirs forever if the command is `add' or `rm'
(cond
((pcomplete-match (regexp-opt '("add" "rm")) 1)
(while (pcomplete-here (pcomplete-entries))))
;; provide branch completion for the command `checkout'.
((pcomplete-match "checkout" 1)
(pcomplete-here* (pcmpl-git-get-refs "heads")))))
```


And that’s that. A simple completion mechanism for git. Put this in your init file and you’re done.
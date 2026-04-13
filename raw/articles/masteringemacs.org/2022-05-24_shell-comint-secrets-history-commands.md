---
title: 'Shell & Comint Secrets: History commands'
url: https://www.masteringemacs.org/article/shell-comint-secrets-history-commands
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I am *super* fond of using Emacs for shells. It’s a topic I’ve written about before – like [Running Shells in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) or the [Complete Guide to Mastering EShell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell) – but today the focus is razor sharp: it’s about command history, and how you can use it in Emacs’s Shell mode and elsewhere — in fact, they’ll even work with programs like the Python and Ruby shells.

Now, before I go any further, it pays to mention this again if you are not familiar: Emacs’s shell mode is not like `M-x ansi-term`

, an actual terminal *emulator*; instead, `M-x shell`

just re-directs the pipes (well, it actually tries to use pseudoterminals…) so the program talks straight to Emacs. No fancy emulation here. That’s why – as you will see below – Emacs has to re-invent everything itself. The downside is it’s never quite 100%, but the upshot is you get to benefit from this generic functionality in programs that may not have it. I use `M-x shell`

for *everything*, and even though it is not perfect, I consider it full-featured and usable.

So most commands in Emacs that talk to the outside world, with EShell being a notable exception, are based on *Comint*. That’s a generic framework, if you like, for out-of-Emacs process communication. What it gives you as an elisp hacker is a bunch of helpful commands that kinda-sorta just work for most things that involve a standard commandline application: history, prompt detection, highlighting, sending and receiving stuff, and much more.

`M-x shell`

is based on Comint and so are most common third-party integrations like the Python shell and so on. That gives you consistency across applications which, I feel, is one of the hallmark features of using Emacs for everything.

## History

Briefly, Comint gives you both `M-p`

and `M-n`

for walking through the history ring in a comint-based buffer in much the same way the up and down arrow works if you ran them in a GNU Readline-enabled program through a normal terminal (Bash is one such example that uses GNU readline.) In Emacs those two keys move the point up or down, so comint has to use a different set of key bindings. So far, so simple.

*Note: GNU Readline also has a Vi emulation mode, which I assume you are not using here, and instead the Emacs-like commands that Readline normally uses…*

What a lot of people *don’t* know is the default GNU Readline command for interactive reverse search (called `reverse-i-search`

), bound to `Ctrl+r`

, is also available in Emacs as `M-r`

. If you knew about the former, but not the latter, you are no doubt a happy person right now as you will agree that it’s a productivity booster if you’re a regular command line user. You can reverse the search direction with `C-s`

.

### Re-running Commands

Another useful command to know about is `C-c C-x`

. It repeats the order of the history commands that come after the one you last ran. To explain in detail, consider this set of commands I ran in a Shell mode buffer:

```
$ echo foo
foo
$ echo bar
bar
$ echo baz
baz
```


Pretty simple: I ran three commands, and when I type `M-p`

(to recall the commands I sent through the history ring) I am given, in order, `echo baz`

, `echo bar`

, and `echo foo`

. Say I pick `echo bar`

and hit `RET`

and resend it:

```
$ echo bar
bar
```


Now, when I type `C-c C-x`

Emacs will insert the `echo baz`

command into the prompt area, as it follows on immediately from `echo bar`

in the history ring. Pretty neat, huh? So it’s great for repeating commands, in-order, as they appeared in the history ring. There are some limitations: you have to accept its suggestion to re-run the next command in the sequence before you can repeat the call to `C-c C-x`

. As long as you do that, Emacs will keep serving up the next logical command in a row.

### Inserting History Arguments

The GNU Readline key `Alt+.`

inserts the N’th argument of the last command, with an optional argument passed in with `Alt-<N>`

where `N`

is a digit – which is exactly the same way Emacs works – and in Emacs it is almost the same: `C-c .`

inserts the N’th argument and, like GNU Readline, it defaults to the last one if no argument is given. This is another useful time saver to know about if you frequently repeat arguments across commands. I find myself doing that more frequently than I think: calling various commands on a docker container id or a Kubernetes pod name being two good examples of such a use case.

### Displaying the History

All that history’s collected somewhere, so of course you can browse Comint’s history of all inputted commands with `C-c C-l`

. It’s a completion buffer, meaning normal keys like `TAB`

to navigate and `RET`

to select work: you can pick a history item and it’ll appear in your prompt for further editing. The command history is buffer-local meaning you don’t have to worry about contaminating one shell buffer with the history of another. Because Comint’s used widely in Emacs you can assume it will work for most other programs (like Python.)

### Nifty Command substitution

One of the more unexpected comint features is Emacs’s ability to expand bash-style history substitution commands *inline*. You can do subsitutions like `!!`

, that expands to the last command; `^a^b`

, that replaces `a`

with `b`

; and more.

To test it out, consider the following bash command:

```
$ echo Hello, World!
Hello, World!
```


If you type `!!`

into a shell mode buffer and then run `M-x comint-replace-by-expanded-history`

then Emacs will expand `!!`

into the `echo`

command above. Simultaneously, if you instead wrote `^Hello^Goodbye^`

and *then* typed that long-winded command, you’d end up with `echo Goodbye, World!`

.

Now, remembering that command is not exactly practical, so to enable it permanently, you must bind `comint-magic-space`

to `SPC`

. Its behavior depends entirely on the underlying program so don’t go enabling it for things you haven’t tested:

`(define-key shell-mode-map (kbd "SPC") 'comint-magic-space)`


In the above line, I’ve enabled it for only Shell mode. That’s a safe place to start. I also assume you’re not running Emacs on OS/2 Warp or something equally crazy, as it’ll probably not work right there. I mention this, as I am fairly certain it’s capable of reaching out and calling out to `history`

(or similar) which will obviously *not* work well if you use it in a comint buffer that does not use that particular history program. As far as I know it will default to the internal history ring that you can display with `C-c C-l`

.

Having said that, I have had good luck with it in Python also, crazily, as Emacs is clever enough to look in its own private history first. Yep, that means you can use `^a^b`

substitution in inferior Python processes and no doubt many other places!

If you weren’t already using Emacs to run most of your external command line programs, then I hope this article’s given you the encouragement to go out and try. I warmly recommend `M-x shell`

for command line excursions that’re not easily done with `M-x dired`

. Even if you are not ready to make the jump, but you use Emacs for programs like the Python or Ruby shells and what not, then you are not exactly left behind either as most of the history commands work everywhere. And if you really want to use Comint for a program that Emacs does not support, then head over and see how I write a basic [Comint mode for Cassandra](https://www.masteringemacs.org/article/comint-writing-command-interpreter). Happy recalling!
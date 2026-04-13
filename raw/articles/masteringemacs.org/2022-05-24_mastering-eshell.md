---
title: Mastering Eshell
url: https://www.masteringemacs.org/article/complete-guide-mastering-eshell
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

You can run [Run Shells and Terminal Emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview), but none can match the versatility and integration with Emacs like Eshell.

Eshell is a shell written entirely in Emacs Lisp, and it replicates most of the features and commands from GNU CoreUtils and the Bourne-like shells. So by re-writing common commands like `ls`

and `cp`

in Emacs-Lisp, Eshell will function identically on any environment Emacs itself runs on.

Unlike a terminal emulator, Eshell is more like `bash`

, `zsh`

or the `python`

shells. That means it has its own idiosyncrasies, rules, modes of operation, advantages and disadvantages.

`cd`

into remote systems. Here it's a docker container running locally.The main advantage is that you’re just talking to Emacs. The downside, of course, is that it’s not a shell you’re probably familiar with: it’ll bear many similarities to the likes of `bash`

or `zsh`

, but it’s distinctly *none* of those things also.

So why use it? Well…

- Native Tramp Support
So you can

`cd`

into docker containers; remote SSH servers; Android phones using the Android Debug Bridge; talk to anything[rclone](https://www.rclone.org)works with, like S3;`su`

and`sudo`

; and much more. And you can combine them all – SSH to this host, then`sudo`

to this user – all from within Emacs and Eshell.All of this, of course, is also available to Emacs writ large.

- Write Elisp instead of
`sh`

It’s got the full power of Emacs behind it.

- Want to open a file? Type
`find-file`

and Emacs opens it. - Need a
`M-x dired`

buffer? Just type`dired .`

. - Worried about the next full moon? Try
`lunar-phases`

.

- Want to open a file? Type
- Piping and Redirection is through Emacs
So you can redirect the output of a command straight into an Emacs buffer or its kill ring.

- It’s all Emacs
For better or worse! You gain tight integration with your Emacs environment, and extending Eshell is relatively easy, as it’s all elisp.

- Command Interception
Type

`grep`

and instead of printing out the results like a normal shell would, Emacs instead refers the query to its own grep machinery, as if you’d called`M-x grep`

.- Plan9 Smart Display
Instead of your screen tailing the output of a command, you can tell Eshell to page top-to-bottom automatically when the output exceeds what fits on your screen.

Excellent when you want to digest the output one page at a time.


… and much more!

Alas, there is also a small problem: Eshell is only partially documented – a rare sight in GNU Emacs – so I’ve compiled this guide to help people make full use of what Eshell has to offer. The [documentation](https://www.gnu.org/software/emacs/manual/eshell.html) is better today than it’s been before, but there’s still a lot of “tribal knowledge” out there you should know about.

## Overview

Unlike the other shells in Emacs, Eshell does not inherit from `comint-mode`

, the default mode for interacting with inferior processes in Emacs. But because Eshell is not an inferior process, it does not have to use comint; but while that may seem like a good thing, it does mean that hooks and routines written for *comint-mode* won’t work with Eshell. That also means any key bindings and commands you may know and use elsewhere may not work well in Eshell, or at all.

Nevertheless, Eshell does reproduce a selection of key bindings you might know from `comint-mode`

, and it does a reasonable job of mirroring the semantics of some of the commands. One example of where Eshell lags behind is that its history search, `M-r`

in `comint-mode`

derivatives and Eshell, does not search-as-you-type.

Eshell works well on any platform Emacs itself runs on, as Eshell interacts with a common middleware (namely Emacs, and Emacs in turn talks to your operating system) and that opens up a number of benefits if you’re stuck running Emacs on a platform that does not support common Linux paradigms. So you’re likely to get a consistent user experience when you use Eshell, and that’s one of its strengths. Another is that you get to benefit from native Tramp support, which is another feather in its cap.

In fact, Eshell also works well with Windows-specific concepts, like disk drives. So it’s easy-peasy to just `cd D:`

to change drives in Windows. No need for any POSIX-style abstractions, like `/cygdrive/c`

in Cygwin.

Despite all the advantages offered by Eshell, there are some disadvantages or gotchas you should keep in mind:

- It’s still not a terminal emulator
As I mentioned earlier, Eshell is not a terminal emulator. It is, in actual fact, utterly incapable of handling anything but line-based programs. Instead, it’ll outsource the running of interactive –

*visual*in Eshell terminology – programs to a dedicated terminal emulator, like`M-x ansi-term`

or VTerm.- Eshell is Emacs
That means you’re hidebound by the limitations of Emacs. You’re not farming out the work of running programs to an external tool like

`bash`

. So if Eshell hangs, your Emacs hangs.Emacs is also responsible for reading and writing from programs. That means it has to buffer text, and that is generally slower than a program written in plain C.

[Native elisp compilation](https://www.masteringemacs.org/article/speed-up-emacs-libjansson-native-elisp-compilation)definitely helps though.- Eshell is not <insert your favorite shell here>
Although it is a reasonable facsimile of particularly

`bash`

and`zsh`

, it does not implement their scripting languages or all the piping and redirection concepts you may know and love from`bash`

.In fact, unless you’re really talented at distinguishing GNU Coreutils from

`bash`

, you’re likely to assume Eshell can (or cannot) do something simply because that distinction is blurred to most users.

## Commands

Eshell is Emacs. And the command line is wired to talk directly to the large library of Elisp commands at your disposal. That means it’s not only easy to write your own commands – just write a normal elisp function and call it – but Eshell is also able to call them, with or without arguments.

You’re therefore free to type `find-file hello.txt`

and have Emacs open up `hello.txt`

. No need to call `emacsclient`

; though of course that also works!

It’s a cool feature and highlights the benefits of tightly coupling a shell to Emacs.

### Technical Details

All commands evaluated by Eshell have an *evaluation order*, which is an ordered list your command must pass through to determine what part of Eshell handles it. If there is nothing on the list that wants to evaluate your command, then Eshell will reject it.

Assuming you want to execute the command `cp`

, the evaluation order is:

- Look for a shell-defined alias (
`alias`

command) - A full filepath (e.g.
`/bin/cp`

) runs`cp`

in`/bin`

- Look for the command prefix,
`eshell-explicit-command-char`

(default is`*`

), and if it is found then look for the command in the search path. - Look for
`cp`

in the search path,`$PATH`

(or`eshell-path-env`

) - Look for a Lisp function named
`cp`

or the elisp function`eshell/cp`


The variable `eshell-prefer-lisp-functions`

alters the evaluation order. What that means is when it’s set to `t`

Eshell swaps the search order of #4 and #5. If the command prefix is specified, though, this directive is ignored.

### Built-In Commands

Eshell has a handful of commands written in elisp that closely emulate a large subset of GNU Coreutils. Those commands are called “Alias functions.”

Eshell only implements a subset of the functionality provided by the real commands, but if you pass an unknown argument to Eshell it will defer to the *real* commandline tool (if it is installed) automatically.

Here’s what Eshell currently re-implements in elisp:

`cat`

, `cp`

, `ls`

, `cd`

, `export`

, `dirs`

, `du`

, `echo`

, `env`

, `kill`

, `ln`

, `mkdir`

, `mv`

, `alias`

, `popd`

, `pushd`

, `pwd`

, `rm`

, `rmdir`

, `time`

, `umask`

.

There is a big emphasis on adhering to the original GNU functionality, so the fact they are emulated is only a problem if you don’t have the underlying tool installed on your system.

### Command Interception

Eshell has a cool mechanism where certain commands are *intercepted* and passed on to Emacs proper. It’s a bit like the ability to call elisp directly in Eshell, but instead of just doing that, the command is instead reinterpreted as the equivalent feature in Emacs.

For instance, Emacs has a large selection of `grep`

-style commands (like `M-x grep`

) that it can run internally and enrich with clickable hyperlinks to each match. Instead of typing `M-x grep`

you can type `grep`

in Eshell and Emacs takes it from there.

Here’s a selection of the supported commands:


`agrep`

,`diff`

,`egrep`

,`fgrep`

,`glimpse`

,`grep`

,`info`

,`jobs`

,`locate`

,`man`

,`occur`

,`su`

,`sudo`

,`whoami`

.

But you can see a full list with `C-u C-h a ^eshell/`

.

The commands `su`

, `sudo`

and `whoami`

are Tramp-aware commands, so if you are connected to a remote shell they work as expected.

### Subshells

There are two types of Emacs subshells. The first one is `$( ... )`

(also `( ... )`

) that evaluates Lisp.

You can use `$()`

to in-line an elisp form and use its output in much the same way as you would in bash:

```
$ echo $(+ 1 2 3)
6
```


The only caveat here is you cannot use the backquote (backtick) to spawn a subshell, but that syntax was never universally supported anyway.

It’s also possible (though I would not recommend it, for there are cases where it does not work) to use a standard elisp form like this:

```
$ echo (+ 1 2 3)
6
```


But it does not work everywhere, so exercise caution.

The other is more like an *actual* subshell: `${ ... }`

. Note that it’s not as versatile as a regular subshell that you may know from `bash`

and the like.

```
$ echo ${echo $(+ 1 2 3)}
6
```


### Useful Elisp Commands

There are a number of useful Eshell commands that you should know about. You’re of course not limited to these commands, but they’re either really useful and general, or made specifically to plug a hole in Eshell’s feature set.

`listify ARGS`

Parses an argument string into elisp list notation and prints it to the screen. It’s clever enough to handle both MS-DOS/Windows and POSIX-style argument syntax.

`$ listify 1 2 3 (1 2 3)`

`addpath PATH`

Adds the argument, which must be a path, to the

`$PATH`

environment variable. If no argument is specified the existing paths are pretty-printed to the screen.`$ addpath /usr/local/sbin/ /usr/local/bin/ [ ... ] $ addpath /opt/mypath/ /usr/local/sbin:...:/opt/mypath/`

`unset ENV-VAR`

Unsets an existing environment variable

`find-file FILE`

Finds the file FILE and opens it in Emacs. This function is Tramp aware and will therefore work remotely.

`dired DIRECTORY`

Opens a dired buffer in DIRECTORY.

`calc-eval EXPR`

Runs EXPR through the Emacs calculator.

`$ calc-eval (+ 1 2) 3`

Note that it does not use Emacs’s hyper-advanced symbolic, reverse-polish notation calculator (bound to

`M-x calc`

or`C-x * *`

)`upcase STR`

/`downcase STR`

Converts STR to upper- or lowercase.

`vc-dir DIRECTORY`

Reports the status of a version controlled directory (equivalent to the

`status`

command in most VCS)`magit`

Activates

`M-x magit`

’s status page for current working directory. (If you have Magit installed, that is!)If you have not used Magit for all your git needs, check out

[An introduction to Magit, an Emacs mode for Git](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git).`ediff-files FILE1 FILE2`

Diffs FILE1 and FILE2 using ediff, one of Emacs’s diff engines.

`find-name-dired DIR PATTERN`

Calls out to the external program

`find`

and asks it to find all`PATTERN`

in`DIR`

.Don’t forget to escape the glob patterns you pass to

`PATTERN`

. Single quotes work well.

Note that most commands work well over Tramp (more on that below) so you can definitely `cd`

to a remote Tramp directory; invoke `magit`

and get a magit status screen for a remote directory.

### Aliasing


`alias ALIAS-NAME DEFINITION`


Aliasing in Eshell works in much the same way as it does in other mainstream shells, except you can freely mix elisp and Eshell commands. The command `alias`

takes an `ALIAS-NAME`

and a `DEFINITION`

. You must enclose `DEFINITION`

with single quotes.

You can environment variable-style notation known from other shells: `$1`

for the first argument, `$2`

for the second, and so on. You can also use `$*`

to use all arguments, or omit them entirely as Eshell will magically append them on to the end of a command if they weren’t referenced in the definition.

To delete an alias, simply leave out the `DEFINITION`

argument. To list all the aliases, leave out both arguments.

Eshell will write the alias definitions to `eshell-aliases-file`

, which in turn is governed by the `eshell-directory-name`


By default that location is `~/.emacs.d/.eshell/alias`

. Emacs commits all alias changes to that file immediately.

Another useful thing to know is the *auto-correcting aliasing*. If you repeatedly fumble the spelling of a command (governed by `eshell-bad-command-tolerance`

, which is 3 by default) Eshell pops up a prompt asking you to alias it to another command.

If you don’t like that, you can bump up the aforementioned variable to a large number.

#### Useful Examples

Let’s map the cumbersome command `find-file`

to the more manageable `ff`

:

`alias ff 'find-file $1'`


And let’s map `dired`

to `d`

:

`alias d 'dired $1'`


This calls `find`

without arguments on the present working directory. Great for getting a recursive listing of all files and directories in your current buffer in a `M-x dired`

buffer.

`alias fd 'find-dired $PWD ""'`


### Visual Commands

Some commands are too complex to be displayed by Eshell directly, and require special handling. To most programs, tools like `M-x shell`

and `M-x eshell`

are *dumb* terminals: they are not capable of advanced cursor movement required for programs like `emacs`

or `top`

to work.

Eshell works well with line-based programs but not interactive programs. For the latter you need a proper terminal emulator. Because interactive (visual in Eshell speak) programs are common, you can tell Eshell to open up visual commands in a dedicated terminal emulator.

To modify the list of visual commands, you can alter `eshell-visual-commands`

. You can even put in commands that work fine in Eshell if you’d rather they run from a dedicated terminal emulator.

If a program requires a full-blown terminal emulator for only some of its subcommands – `git`

being one such example – you can customize `eshell-visual-subcommands`

and `eshell-visual-options`

and selectively enable visual command support:

```
(add-to-list 'eshell-visual-options '("git" "--help" "--paginate"))
(add-to-list 'eshell-visual-subcommands '("git" "log" "diff" "show"))
```


Invocations to `git`

that include either one of `--help`

or `--paginate`

as an option, or `log`

, `diff`

or `show`

as a subcommand, are now invoked through a terminal emulator.

## Command History and Prompt Key Bindings

Eshell comes with a feature-rich command history facility. Because Eshell does not use `comint-mode`

it does not have *all* the history features available to it, but most of the common ones do exist.

`M-r / M-s`

Search backwards or forwards for a command by regexp

`M-p / M-n`

Goes backwards or forwards in the command history list

`C-c C-p / C-c C-n`

Jump to the previous or next command prompt in Eshell

`C-c M-r / C-c M-s`

Jumps to the previous or next command that shares the command currently used as input. So it jumps to other instances of the command

`foo`

if that is the current input.`C-c C-o`

Kills the output of the previous command.

`C-a / C-e`

Move to the beginning or end of line.


Unfortunately, the search-as-you-type history search in `M-x shell`

(bound to `M-r`

) is not implemented in Eshell.

Because I program a lot, I tend to use `M-m`

instead of `C-a`

to move to the beginning of the line. `M-m`

skips indentation and moves to the first non-whitespace char, unlike `C-a`

.

That command does not work in Eshell, for obvious reasons, but you can rebind it to the same key as `C-a`

:

`(define-key eshell-mode-map (kbd "M-m") 'eshell-bol)`


### History Interaction

You can rewrite previous commands found in Eshell’s history. The syntax is similar to what you find in `bash`

, but it’s just a subset of the most common features. It’s probably easier to refer you to the `bash`

info manual for detailed information on how the history interaction works. I’ve included a small table below that describes most of the history syntax Eshell supports.

You may also want to read my article on [Shell & Comint Secrets: History commands](https://www.masteringemacs.org/article/shell-comint-secrets-history-commands). Although it concerns `comint-mode`

-derived things, it’s useful to know about anyway.

`!!`

Repeats the last command

`!ls`

Repeats the last command

**beginning**with`ls`

`!?ls`

Repeats the last command

**containing**`ls`

`!ls:n`

Extract the

*nth*argument from the last command**beginning**with`ls`

`!ls<tab>`

Using

*pcomplete*, show completion results matches`ls`

`^old^new`

Quick substitution. Using the last command, replace

`old`

with`new`

and run it again. Appears to be buggy.`$_`

Returns the last parameter in the last executed command.


Eshell also has some support for bash history modifiers (like `!!:s/old/new/`

) and [the bash reference on history interaction](http://www.gnu.org/software/bash/manual/bash.html#History-Interaction) would be a good place to brush up on that.

## Commandline Interaction

### The Eshell Prompt

You can customize the Eshell prompt by modifying `eshell-prompt-function`

, a variable that takes a function that defines what the prompt should contain. By relegating prompt configuration to elisp you can do just about anything you like with it. The only problem is, of course, that Eshell will need to be told *what* the prompt “looks” like, so you must also edit the variable `eshell-prompt-regexp`

so Eshell knows what the prompt is.

Instead of going to the trouble of changing it yourself, you can give the package [Eshell prompt extras](https://github.com/zwild/eshell-prompt-extras) a try.

### The Command Line

You can use `\`

to escape newlines and it supports rudimentary multi-line input that way.

Another way of doing multi-line *literal strings* is with single quotes: begin a single quote and hit enter, and you are free to enter text until the closing quote delimiter is encountered. If you use double quotes Eshell will expand subshell commands and do variable expansion. In this sense it’s quite similar to `bash`

, though without the support for `bash`

*heredocs*.

Due to the way Eshell works, you can even go back and modify the text you entered, in quotes.

### Useful Keybindings

Eshell comes equipped with a couple of quality-of-life improvements that make interacting with Emacs and Eshell a lot easier.

`C-c M-b`

Inserts the printed buffer name at point

`C-c M-i`

Inserts the printed process name at point

`C-c M-v`

Inserts an environment variable name at point

`C-c M-d`

Toggles between direct input and delayed input (send on RET).

Useful for some programs that don’t work correctly with buffered input.


## Argument Predicates

Argument predicates are a cool way of quickly filtering lists of files or even elisp lists. The predicate syntax is based on the one used in `zsh`

.

Unlike most other areas of Eshell, argument predicates are documented in Eshell itself.

You can access the help files by typing `eshell-display-predicate-help`

or `eshell-display-modifier-help`

in Eshell or `M-x`

. If you frequently use them, you should consider creating an Eshell `alias`

.

Filtering globbed lists of files is very useful, as it saves you the hassle of using tools like `find`

to cut down on matches.

The help file is fairly spartan and only serves as a simple reference, so I’ve included a small guide here. But actually, the only real way to learn something as flexible as argument predication istrial and error.

### Syntax Reference

I’ve opted not to reprint the sizeable list of predicates and modifiers, as the Eshell popup help (see the commands above) do a good enough job of explaining how they work.

### Globbing

Globbing in Eshell follow the same rules as it does in most other common shells: it is the shell that does the expansion of globs and *it* passes the expanded list of matches on to commands like `ls`

. That’s why when you use `find`

and `xargs`

together it’s critical that you pass `-print0`

to `find`

, and `-0`

to `xargs`

. If you don’t, filenames with obscure characters or spaces in them may trip up xargs. Using the NUL character as a separator ensures tokenization takes place correctly.

### Elisp Lists

Eshell’s “lists” are actually elisp lists in their printed form as well as internally. That makes life a lot simpler if you think about it, as Eshell can paw off list handling to elisp, which is something Lisp does well.

Here is a common example

```
$ echo *
("bar" "bin/" "dev/" "etc/" "foo" "home/" "lib/" "tmp/" "usr/" "var/")
```


Like most shells everywhere, `*`

is a wildcard glob pattern. Because – as I just mentioned above – wildcard expansion takes place *inline*, I can modify the output of a glob pattern like `*`

.

Let’s uppercase the globbed result set:

```
$ echo *(:U)
("BAR" "BIN/" "DEV/" "ETC/" "FOO" "HOME/" "LIB/" "TMP/" "USR/" "VAR/")
```


Notice how I used `()`

immediately following the glob pattern. Modifiers are things that *modify* (big surprise!) the resulting list. Modifier commands always begin with `:`

, and filtering predicates do not.

Another example, but this time I filter directories using a predicate:

```
$ echo *(^/)
("bar" "foo")
```


The circumflex, `^`

, in this case, like in regular expressions, is negation. The `/`

means “directories” only.

But I don’t have to use globs to apply modifiers or predicates to lists:

```
$ echo ("foo" "bar" "baz" "foo")(:gs/foo/blarg/)
("blarg" "bar" "baz" "blarg")
```


This time I replaced all occurrences of *foo* with *blarg*. Observe that the syntax is identical, except instead of using globs to get a list of files, I used a list of my own choosing.

The advantages provided by argument predicates and modifiers will greatly reduce commandline clutter as the predicates cover permissions, ownership, file attributes, and much more.

### Adding New Modifiers and Predicates

You can even add your own predicates (`eshell-predicate-alist`

) or modifiers (`eshell-modifier-alist`

):

`(add-to-list 'eshell-modifier-alist '(?X . (lambda (lst) (mapcar 'rot13 lst))))`


Here I’ve bound `X`

to `rot13`

, the substitution cipher:

```
$ echo ("foo" "bar" "baz")(:X)
("sbb" "one" "onm")
```


## Plan 9 Smart Shell

Eshell comes with a pared-down facsimile of Plan 9’s terminal, called *the Eshell smart display*. The smart display is meant to improve the write-run-revise cycle all command line hackers suffer through. It works by not letting the point follow the output of a command you execute, like a normal shell would. Instead, the point is kept on the line of the command you executed, letting you revise it easily without having to use `M-p`

and `M-n`

or the history modification commands.

Additionally, you can ‘peek’ at long-running commands using `SPC`

to move down a page and `BACKSPACE`

to move up a page while you wait for the command to finish. Any other key press jumps to the end of the buffer.

Essentially, if Eshell detects that you want to *review* the last executed command, it will help you do so; if, on the other hand, you do not then Eshell will jump to the end of the buffer instead. It’s pretty clever about it, and there are switches you can toggle to fine-tune the behavior.

Where the smart display really shines is that it lets you modify the command you just executed by using the movement keys – like you normally would – to change the command, say to fix a typo or tweak an argument.

You can also disable smart display so it won’t activate if the command you executed exited with code 0 (indicating success) and if it finished without emitting any output.

To enable it put this in your init file:

```
(require 'eshell)
(require 'em-smart)
(setq eshell-where-to-jump 'begin)
(setq eshell-review-quick-commands nil)
(setq eshell-smart-space-goes-to-end t)
;; If the above does not work, try uncommenting this.
;; (add-to-list 'eshell-modules-list 'eshell-smart)
```


If Eshell is already initialized (that is, you’ve already launched an instance of Eshell in Emacs) then evaluating the changes above will not work. You must switch to the Eshell buffer and type `M-: (eshell-smart-initialize)`

(or restart Emacs.) You might see some garbled output appear in your echo area. Just ignore it.

Some report that they must

So remember: `SPC`

to page through the output; `BACKSPACE`

to move back a page; and any other keys jumps to the end of the buffer.

## Redirection

Redirection in Eshell works in much the same way as it does in other shells. The key difference is that Eshell has to emulate the pseudo-devices as they may not be present (or may not be present in the same form) on platforms such as Windows where `/dev/null`

is actually `NUL`

.

Another caveat is that Eshell does not support *input* redirection, though it does support output redirection. To skirt around the lack of input redirection you should use pipes instead.

Redirection to stdout, stdin and stderr work as you would expect, and you can send things to multiple targets as well, which is very nice.

### Redirecting Pipes to a Buffer

Because Eshell has to reimplement pseudo-devices internally it is not at the mercy of dealing with just UNIX device files – it is actually capable of implementing its own pseudo-devices.

A good example would be redirection to a buffer of your choosing, and that can be done with the following syntax:

`$ cat mylog.log >> #<buffer *scratch*>`


This is where the ability to insert the printed format of a buffer comes in handy. The command `C-c M-b`

from before does the job. There is another shorthand: `#<*scratch*>`

that achieves the same outcome.

You can also output straight to an elisp variable (but be careful you don’t fry the wrong settings):

```
$ echo foo bar baz > #'myvar
$ echo $(cadr myvar)
bar
```


If you set `eshell-buffer-shorthand`

to `t`

you can use the shorthand `#'*scratch*`

instead, but it means you will not be able to redirect straight to elisp symbols. I recommend you use `C-c M-b`

and `#<buffer-name-here>`

instead.

### To Pseudo-Devices

Eshell reimplements the following pseudo-devices:

`/dev/eshell`

Prints the output interactively to Eshell.

`/dev/null`

Sends the output to the NULL device.

`/dev/clip`

Sends the output to the clipboard.

`/dev/kill`

Sends the output to the kill ring.


The usual redirection rules like overwrite (`>`

) and append (`>>`

) apply here.

### To Custom Virtual Targets

You can design your own virtual targets by modifying `eshell-virtual-targets`

, an alist that takes the name of the pseudo-device you want to create, and a function that takes one parameter, `mode`

, that determines if it’s `overwrite`

, `append`

or `insert`

.

## Remote Access with Tramp

Tramp (Transparent Remote Access, Multiple Protocol) is a framework for communicating across different user accounts, servers, docker containers, and much more.

It’s handy, and works well. Tramp works – keeping it simple, here – by intercepting how Emacs interacts with files, directories and processes. Because it’s generic, it works with a huge range of Emacs’s features — features that are almost never coded explicitly with Tramp in mind.

Eshell works well with Tramp. Provided you follow Tramp’s connection notation, you can connect to any backend Tramp supports and interface with it using Eshell.

Here’s an example that changes directory to a remote server using SSH:

`cd /ssh:bob@initech:/srv/tps-reports/`


That incantation connects as user `bob`

to the server `initech`

and switches to its `/srv/tps-reports/`

directory. From that moment on, all interactions in Eshell take place through the lens of the remote connection you established through Tramp.

Tramp is not perfect; nor is Eshell. But a wide range of commands work beautifully well remotely. Note that unlike an ordinary SSH connection Tramp does, in actual fact, make distinct calls via SSH every time you carry out an action.

It’s not a longer-running session like you might expect, and although you can configure all of this, it’s worth bearing in mind that you’re reaching out and executing standalone actions, one at a time.

If you install the third-party package `docker-tramp`

you can also `cd`

straight into docker containers and act on them.

Using that method, you can combine it with multi-hopping, so you can SSH to a remote server then `su`

to a different user; connect with `docker`

; or something else entirely:

`$ cd /ssh:initech|su:root@localhost:/`


## Startup Scripts

Like most shells, Eshell supports both login and profile/rc shell scripts. The full filepaths for both are stored in the variables `eshell-login-script`

and `eshell-rc-script`

, but by default the files `login`

and `profile`

are stored in `~/.emacs.d/.eshell/`

.

The comment syntax is `#`

.

## More Customization…

Eshell has hundreds of options you can tweak to your liking. To configure Eshell, type `M-x customize-group RET eshell RET`

.

## Third-Party Extensions

There’s a large body of third-party packages and snippets of code available. Check your local package manager with `M-x list-packages`

. Use `M-s o`

or `/ n`

to filter by package name.

## Bookmarks & Project Integration

Emacs’s extensive bookmarking facility also works with Eshell as of Emacs 28. Create a bookmark with `C-x r m`

and you can recall it at will with `C-x r l`

and friends.

I like this feature because you can bookmark directories and Emacs can open up an Eshell at the exact place you bookmarked.

Likewise, Emacs’s project management facility `C-x p`

can open an Eshell in your project root with `C-x p e`

.

## TAB Completion

Eshell has its own completion system called `pcomplete`

. Although newer versions of Emacs invoke the generic `completion-at-point`

command, it internally still uses pcomplete for much of the command completion.

I have an article where I talk about [PComplete: Context-Sensitive Completion in Emacs](https://www.masteringemacs.org/article/pcomplete-context-sensitive-completion-emacs). If you ever want to extend Emacs’s shell completion – in newer Emacsen `shell-mode`

also uses `pcomplete`

behind the scenes – or understand how it works, then that article’s a good place to start.

The completion system is not fool-proof, and unlike your favorite external shell it does not come with an abundance of completion libraries for every conceivable binary.

Nevertheless, both `TAB`

and `C-M-i`

offer completion at point.

And don’t forget, Emacs has both `M-x man`

and `M-x woman`

for manual page lookup.

## Conclusion

I think I’ve covered all major areas of Eshell, and I hope it paints it in a good light. Eshell is a versatile shell replacement thanks to its tight integration with Emacs. It’s not a drop-in replacement for `bash`

and your favorite terminal emulator, but it’ll do most of the command line stuff we all inevitably end up doing.

Eshell has Tramp support; custom pseudo-devices; a pocket-sized elisp REPL; lots of useful utility commands like being able to `find-file`

or `dired`

any directory or file you’re in; and the ability to redirect output from commands straight into a buffer.

All in all, it’s a clever take on shells, and a tool I would encourage you to experiment with.
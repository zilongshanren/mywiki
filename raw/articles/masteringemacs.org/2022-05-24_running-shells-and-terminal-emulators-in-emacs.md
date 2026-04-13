---
title: Running Shells and Terminal Emulators in Emacs
url: https://www.masteringemacs.org/article/running-shells-in-emacs-overview
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

To use Emacs effectively, you must learn to use all that Emacs has to offer. One of Emacs’s strongest selling-points is its shell integration and terminal emulation. If you come from other editors or IDEs you’re probably using an external terminal window (like xterm), a terminal multiplexer (like GNU Screen or tmux) or console window (in Windows) and switching back and forth. But there’s a better way…

If you use Emacs as your shell you will have all the functionality that Emacs provides *plus* you get almost all of the advantages provided by the shell itself, but built into Emacs. This article is only a quick overview, but it’s enough to get an understanding of Emacs’s capabilities.

All external, interactive shells in Emacs are derived from something called `comint-mode`

. `comint-mode`

introduces low-level functions for dealing with interactive shells that require user input, a history ring, and so on. Shells like `M-x shell`

and `M-x run-python`

inherit from comint mode. Comint mode also has the unfortunate job of having to work with a baroque set of systems, devices and rules that are old and arcane.

But an important note before I begin: a terminal emulator is not the same as a shell. The terminal emulator reads control codes and updates a grid of characters split into columns and rows. That, in a nutshell, is all it does. A shell is something like `bash`

, or `cmd.exe`

, or `python`

.

Emacs can do both. But first, it’s worth talking about how Emacs interacts with external programs.

## How Emacs talks to External Processes

Emacs runs on many platforms. The maintainers of Emacs go to great lengths to ensure a uniform experience — where possible, anyway. That includes native Emacs implementations for features that may not be present on certain platforms, or outright workarounds if certain features don’t work well or at all.

When you “run” a program in your terminal, you’re effectively communicating with that program using bidirectional “channels”. They’re usually called standard input, output and error — though not all platforms have a dedicated error channel, and some may have even *more* channels than those three. If you’re on Linux, your Emacs is *probably* using pseudo-terminals (called a “pty”) to achieve this. The fallback, and this is true of Windows especially, is to simply redirect the channels – pipes, really – to achieve a broadly similar effect.

That’s basically how Emacs works: it taps into those channels and communicates through them. It’s also how shell piping works when you do `cat myfile.txt | ...`

.

But talking to external processes is fraught with inconsistencies: bad decisions made in the 1980s that linger on today; platform discrepancies; having to emulate how a teletype or teleprinter device from the late 70s would literally write out characters on paper or screen; and the list goes on.

That’s why, if you ever find yourself in the unfortunate position of having to muck around with commandline tools like `stty`

, that you’ll come to appreciate just how much work Emacs has put into this over the last four decades.

When you type `M-x comint-run`

and you give it a program to run, it’ll… probably work fine. At least on 21st century platforms. There are a couple of things that may lessen your experience:

- Input echoes when you send text.
- ANSI / Terminal escape codes don’t render or work well.
- Emacs does not understand the prompt, and won’t provide history or completion.
- Line endings aren’t stripped properly.
- The prompt may not appear at all!

Luckily, these things are fixable. And usually, if you’re running specialized commands – like `M-x run-python`

– then it’s most likely set up correctly already.

In Emacs parlance, when you run a process it’s usually called *inferior*.

## The Inferior Shell (“Shell Mode”)

Type `M-x shell`

and Emacs spawns a shell using your platform’s default shell. On Windows that’s usually `cmd.exe`

, and on Linux it’s often `bash`

. `M-x shell`

is not a terminal, as I explained earlier. That means it’s not meant to be used with interactive terminal programs like `top`

.

But that’s not a bad thing. Instead, it’s a trade-off. You see, `M-x shell`

is a fantastic terminal *replacement* — you replace the terminal with common Emacs primitives. You can move around and edit and search and use any features you like. Already here, in my opinion, does it greatly exceed the utility of your typical terminal emulator. It works like any other buffer.

That also means you don’t have to fight with it to mark text and copy it; that can be done with any number of common Emacs commands. And because it’s an Emacs buffer, you gain a large number of useful additions:

- Builtin Completion
Emacs emulates the

`TAB`

-completion you find in tools like`bash`

. It’s not as expansive as`bash`

, and extending it isn’t that easy, but it’s generally good enough for a large swathe of things.The primary completer for commands is

`pcomplete`

, a completion tool originally built for Eshell. But more Eshell later.If you want to see what Emacs is capable of completing in

`shell-mode`

, you should look at the variable`C-h v shell-dynamic-complete-functions`

. To see all the pcompleters you system uses, look at`C-u C-h a pcomplete/`

.- History Ring
Emacs’s history tool is much better than the simplistic one you get in GNU readline (the tool most shells use for history completion and such like.)

To get an idea of what the differences are, you can read about the

[Shell and Comint History Commands](https://www.masteringemacs.org/article/shell-comint-secrets-history-commands).- Specialized Movement and Editing
Like

`C-c C-p`

and`C-c C-n`

to move between prompts. Or`C-c C-o`

to delete the output of the last command, and`C-c C-r`

to jump to the beginning of the command’s output.You’ve got

`M-r`

to isearch through your command history;`C-c C-l`

to show the history; and`M-p`

and`M-n`

to cycle through it.And, of course, you can apply the entire arsenal of Emacs keys and commands as it’s a plain old buffer.


A common complaint about `shell-mode`

is the anemic support for ANSI/Terminal control codes. Emacs’s builtin `ansi-color`

library is serviceable but basic.

If you want better control code emulation you can give [xterm-color](https://github.com/atomontage/xterm-color) a try instead. It does come with a number of trade-offs, but if you want better color emulation then it’s worth trying out.

### Changing the shell program

You can change the default program `shell-mode`

uses. But note, if you’re doing something esoteric, you’re going to have to change quite a few variables as every shell has its own unique set of challenges to deal with.

Here’s a *simple* example that uses `zsh`

:

```
(setq explicit-shell-file-name "/usr/bin/zsh")
(setq shell-file-name "zsh")
(setq explicit-zsh-args '("--login" "--interactive"))
(defun zsh-shell-mode-setup ()
(setq-local comint-process-echoes t))
(add-hook 'shell-mode-hook #'zsh-shell-mode-setup)
```


This setup makes a number of assumptions. Like that Emacs knows about the prompt — and if it’s the default `zsh`

prompt, it probably will. Otherwise you’ll have to change `shell-prompt-regexp`

so it’s correct.

Next, it adds a mode hook that “processes” echoes. This stops duplicate input from appearing.

Now note the variable `explicit-zsh-args`

; it’s not a builtin variable! The file name portion in `explicit-shell-file-name`

is extracted and checked against a variable named `explicit-<filename>-args`

. I have set it to call `zsh`

with `--login`

and `--interactive`

. The latter may, or may not, be a requirement. Some programs, when they detect the output and input is redirected, disable the prompt. So if the prompt is missing, you’ll want to ensure the shell runs interactively.

And that’s it. That’s the bare-bones setup for another shell. This setup leverages a number of hardcoded assumptions that `shell-mode`

sets if it detects the shell is `zsh`

.

If you want to fine tune things, and if you know a little elisp, just read the docstring in `C-h v shell-mode`

. It’ll list most of the variables you’d want to configure. If you’re running into issues, you should instrument and step through the `shell-mode`

function (or at least read its code) to see where things are going wrong.

### Directory Tracking

One common problem is Emacs losing track of the underlying directory your shell is visiting. That can happen easily if a command changes your working directory and Emacs is not told that it took place.

Emacs 28 adds support for OSC (“Operating System Command”) information. Namely OSC 7 which governs the current working directory. How that’s implemented is down to the individual tool. Emacs has opted for a URI-style notation, which I think is quite sensible and compatible with the hyperlink OSC notation that it also now supports.

Getting it to work requires a little bit of work and some fiddling, but I strongly recommend you go to the trouble of getting it to work. Directory tracking is notoriously unreliable and hard to get right without embedding the full filepath in your prompt. With this method you don’t need the directory at all; it’s silently fed to Emacs thanks to OSC.

For older Emacsen, use `M-x shell-dirtrack-mode`

or `M-x dirtrack-mode`

instead. **Make sure your prompt regexp is understood by dirtrack**!

**NOTE:** The library, `xterm-color`

, strips out OSC information and won’t work well with this option.

Here’s a `bash`

example. Put it in your `.bashrc`

file:

```
# .bashrc
function myprompt () {
printf "\e]7;file://%s%s\e\\" "$HOSTNAME" "$PWD"
}
PROMPT_COMMAND=myprompt
```


Feel free to use your own prompt setup here. If you use another shell you may need to change how the prompt is set. The money shot’s the `printf`

statement. Using `PROMPT_COMMAND`

with `bash`

has the advantage of calling the function whenever a prompt is printed and so it shouldn’t interfere with your existing prompt.

Now update `comint-output-filter-functions`

:

`(add-hook 'comint-output-filter-functions #'comint-osc-process-output)`


Don’t forget to disable `M-x shell-dirtrack-mode`

or `M-x dirtrack-mode`

so they don’t interfere with the OSC tracker.

At this point it should now work. You can test if it does by checking if the variable `default-directory`

is correct when you change paths.

## Terminal Emulator

**MS Windows**: The terminal emulator won’t work on Windows out of the box.

The Emacs terminal emulator is exactly that; it emulates the VT100-style ANSI escape codes, just like *xterm* or *rxvt*. Emacs’s emulator isn’t complete or perfect, so some interactive programs won’t work properly, but most things like `top`

or even `vi`

will. To run the terminal emulator, type `M-x term`

or `M-x ansi-term`

(for full ANSI support). I recommend the latter.

Due to the way terminal emulators work, most of Emacs’s common keybindings are reserved for the subshell itself; to get around this you can switch between *line mode* and *char mode*. In *line mode* the terminal buffer will behave much like *shell mode* and normal Emacs buffers. In *char mode* each character is sent directly to the underlying inferior shell without preprocessing by Emacs.

To switch between the two modes type `C-c C-j`

to switch to line mode, and `C-c C-k`

to switch to char mode. To save you from having to switch between modes for one-off commands you can use the alias `C-c char`

which translates into `C-x char`

.

I have a small amount of customizations I use to make the experience less jarring. Mostly to make it behave a little bit more like `shell-mode`

and my normal Emacs experience:

```
(defun mp-term-custom-settings ()
(local-set-key (kbd "M-p") 'term-send-up)
(local-set-key (kbd "M-n") 'term-send-down))
(add-hook 'term-load-hook #'mp-term-custom-settings)
(define-key term-raw-map (kbd "M-o") 'other-window)
(define-key term-raw-map (kbd "M-p") 'term-send-up)
(define-key term-raw-map (kbd "M-n") 'term-send-down)
```


I use `M-o`

to cycle through windows, and `M-p/n`

should behave as they do in `shell-mode`

. That’s it really.

## Serial Terminal

Doing embedded programming? Good news. Emacs has a serial terminal capable of talking to most devices connected to your machine. It works on Windows also – so if you have something connected to `COM1`

or `/dev/ttyS3`

, then you can use `M-x serial-term`

to talk to it.

It’s actually quite handy even if it’s a niche use case for most. You may want to adjust the speed and various serial terminal settings like parity, baud or flow control.

Here’s an example:

`(serial-process-configure :process "/dev/ttyS0" :speed 1200)`


The docstring for `serial-process-configure`

has all the gory details.

## VTerm in Emacs

`M-x ansi-term`

is slow and not as advanced as it could be. It’s nice knowing it’s there, but if you don’t mind installing third-party modules and code, you should give `libvterm`

, a standalone library for terminal emulation, a try. It uses Emacs’s dynamic module system, and that means your Emacs must be compiled with dynamic module support!

The library itself is written in C and it is fast – pretty much as fast as an external terminal emulator. It does of course not have any of the frills you get with `shell-mode`

, but if you don’t care about that you should use the [Emacs libvterm](https://github.com/akermu/emacs-libvterm) package.

It works a bit like `ansi-term`

in that you can switch between “line” mode and “copy” mode which – much like old-school terminal flow control – stops printing if you engage it. Copy mode acts like a normal Emacs buffer until you go back to line mode.

I use it for things where speed and emulation quality is essential, which is not that often. I prefer `eshell`

or `shell`

as it’s basically just Emacs.

## Maybe you don’t need a Shell or Terminal Emulator…

Hear me out. Emacs is capable of almost everything you’d want a terminal for:

- Files and Directory Manipulation
Use dired:

`C-x d`

(`M-x dired`

). It’s infinitely better than slumming it with the likes of`cp`

,`ls`

and friends. Dired’s ridiculously advanced and yet super easy to get started with.Here’s a couple of workflows to get you started:

- Specialized tools like
`git`

Just use Magit. Job done. Here’s how:

[Using Git in Emacs with Magit](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git)- Common System Administration Tools
You don’t need

`kill`

,`ps`

or`top`

when you can[Replace ps and top with Emacs’s proced](https://www.masteringemacs.org/article/displaying-interacting-processes-proced)Emacs is also able to abstract common network tools. See:

[Interacting with network utilities like ping and dig](https://www.masteringemacs.org/article/network-utilities-emacs)- Piping buffer text in and out of Emacs
You can have Emacs feed a buffer or a region into a command and insert the output back into your Buffer.

- Running Commands with Error and Warning Highlighting
The

`M-x compile`

tool is designed to run commands that spit out structured errors like that you get from a compiler or a unit test harness. See how[you can compile scripts from Emacs](https://www.masteringemacs.org/article/compiling-running-scripts-emacs)- Writing your own Emacs Inferior Shell
If you find yourself interacting with interactive command line tools then why not bring them into the fold by

[writing your own comint interpreter](https://www.masteringemacs.org/article/comint-writing-command-interpreter)? With a little bit of work you’ll have command history, syntax highlighting, and more.

## EShell, The Emacs Shell

Emacs comes with its own shell (as in, like `bash`

or `zsh`

) written in entirely in Emacs-Lisp. The shell, named Eshell, is a feature-rich replacement for your standard-fare shells like `bash`

with the added bonus of working on any platform Emacs runs on. This is especially useful if you’re on Windows but crave a Linux-like environment. It’s heavily inspired by the likes of `bash`

and Plan9, a defunct operating system from Bell Labs.

To start Eshell, run `M-x eshell`

.

As the shell is written entirely in elisp, that means you can also *extend* it with elisp; and the shell has provisions for inlining elisp and using the results as part of your commands. EShell is clever enough to detect commands like `man`

that Emacs itself is capable of doing. Very useful.

You can also `cd`

straight into remote TRAMP directories — which is really, really cool.

EShell is a great shell but woefully underdocumented; therefore, I’ve written [a guide to mastering Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell).

Despite the many advantages Eshell brings to the table, it is *not* a shoe-in replacement for a terminal emulator running bash.

## Conclusion

Several terminal emulators and two shells. Not bad. They all serve an important purpose, but only *you* can decide which one is right for your workflow. If you’re looking for a faithful emulator, then `vterm`

is the choice for you, with `ansi-term`

a distant second; if you are more interested in a dumb terminal that behaves like an Emacs buffer then use `shell`

; if you want something fancier than `shell`

that you can tweak and customize like Emacs itself, `eshell`

may be the right shell for you.

Whatever the case, the shells alone should eliminate almost all external terminal emulators for all but the most complex interactive programs out there. And if that’s not enough, Emacs itself is no slouch: use it instead of command line tools where you can. And for everything else, you have `ansi-term`

or `vterm`

.
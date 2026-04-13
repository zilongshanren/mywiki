---
title: Introduction to Ido Mode
url: https://www.masteringemacs.org/article/introduction-to-ido-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

There are many ways of improving your productivity when you use Emacs, and Ido (or “Interactively DO things”) is one of those packages that you enable and then never, ever turn off again. Although it’s got a lot of competition today, it’s still a useful package because it hand crafts the completion experience for files and buffers. That’s something most modern completion frameworks *don’t* do.

By super-charging Emacs’s completion engine and improving the speed at which you open files and buffers, you will cut down on the time spent doing these menial tasks. Think about how often you switch buffers, open files or navigate directories in Emacs.

Because Ido predates the liberalization of Emacs’s builtin completion backend – I recommend you read [Understanding Minibuffer Completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion) – it works by wedging itself into Emacs’s internal machinery. That means you don’t get to benefit from some of the advances in completion customization that other, more modern, frameworks make use of.

Ido adds flex matching. It’s a particular type of matching that wildcard matches characters even though they’re not next to one another in the list of candidates. So `bk`

matches `book`

. That means if you were to search for the buffer “*Customize Group: Foobar*” without Ido you’d have to contort your fingers and type the *, then TAB (and hope it completes) and if not, type in some more; then rinse and repeat.

With Ido you’d type a few characters until you find the match, or until you narrow down your list of matches to a manageable subset, and then press RET. So the above buffer name could be found by typing “cgf” – c for Customize, g for Group and f for Foobar. Magic.

Because Ido asserts its presence in your Emacs rather forcefully, it won’t work well with some completion prompts. Instead Emacs will default to the normal completion system you use. If you want Ido-style completion literally everywhere – ignore that Ido has an option called *Ido Everywhere* that isn’t really everywhere! – then you should give [Fido Mode](https://www.masteringemacs.org/article/understanding-minibuffer-completion) a try. It’s an Ido-like facsimile built on top of Emacs’s Icomplete engine. It’s built into newer Emacsen.

## Enable Ido Everywhere

To enable Ido, you should customize it using the Customize interface. `M-x customize-group ido`

is a good place to start. That’ll enable basic Ido support for files and buffers and the useful “flex matching” as well.

I recommend you enable `Ido Enable Flex Matching`

(`M-x customize-option RET ido-enable-flex-matching`

) and Ido Everywhere `ido-everywhere`

.

Here’s how you do it without Customize:

```
(setq ido-enable-flex-matching t)
(setq ido-everywhere t)
(ido-mode 1)
```


There’s a boatload more you can tweak, but that’s a good place to start.

### My Customizations

There’s more to Ido than just enabling it. I’ve compiled a list of interesting settings you can change and I have thrown in some of my preferences for good measure.

#### Find File At Point

Find File At Point, also known generally as “ffap”, is an intelligent (well, when I say that, I mean it uses simple heuristics to infer the context at point) system for opening files, and URLs.

Some people hate it, and personally I tolerate it. It gets in the way sometimes and when it does it’s really annoying, but mostly it helps me so it gets to stay. It works in surprisingly many contexts like inferring the filepath of a library in an elisp `(require 'foobar)`

form.

This will make Ido guess the context, which is what I use.

`(setq ido-use-filename-at-point 'guess)`


You can disable URL ffap support by toggling `ido-use-url-at-point`

. I recommend you do so, as Emacs may mistake something for an URL that isn’t.

#### Eliminating Obstacles

If you create a ton of throw-away buffers like I do, this setting will force Ido to always create a new buffer (in `C-x b`

) if the name does not exist. I create throw-away buffers all the time and the last thing I need is Ido asking my permission to create one. Other choices are `prompt`

and `never`

.

```
(setq ido-create-new-buffer 'always)
(setq-default confirm-nonexistent-file-or-buffer nil)
```


You can customize the order in which files are sorted when Ido displays them in the minibuffer. There are certain file extensions I use more than others, so I tell Ido to emphasize those.

`(setq ido-file-extensions-order '(".org" ".txt" ".py" ".emacs" ".xml" ".el" ".ini" ".cfg" ".cnf"))`


#### Ignorance is Bliss

Ido is capable of ignoring (that is, by omission) buffers, directories, files and extensions using regexp.

| Variable Name | Description |
|---|---|
`ido-ignore-buffers` | Takes a list of buffers to ignore in `C-x b` |
`ido-ignore-directories` | Takes a list of directories to ignore in `C-x d` and `C-x C-f` |
`ido-ignore-files` | Takes a list of files to ignore in `C-x C-f` |

I would recommend using `M-x customize-option RET variable-name-here`

to customize them unless you are comfortabe editing Emacs lisp directly. I don’t ignore anything in Ido beyond the defaults, as I prefer to use the more general `completion-ignored-extensions`

as it works with and without Ido.

To make Ido use `completion-ignored-extensions`

you need to enable it if it is not enabled in your Emacs already:

`(setq ido-ignore-extensions t)`


Now you can customize that variable as well: `M-x customize-option RET completion-ignored-extensions`

. Go ahead and add all the useless object files, backup, autosave and other computing flotsam you don’t want Ido to show.

**NOTE:** Ido will *still* complete the ignored elements if Ido would otherwise not show any other matches. So if you type out the name of an ignored file Ido will still let you open it just fine.

## Ido Cheatsheet

Here’s a quick cheatsheet of all the interesting Ido commands.

The “Available In” column indicates where the keybinding is available. “All” means that it is a feature inherent to `ido-completing-read`

and as such is available in all the completion engines. “Files”, “Dirs” and “Buffers” means it is only available in one of those.

### General-purpose Commands

`C-b`

Reverts to the old `switch-buffer`

completion engine. *Available in Buffers*.

`C-f`

Reverts to the old `find-file`

completion engine. *Available in Files*.

`C-d`

Opens a dired buffer in the current directory. *Available in Dirs / Files*.

`C-a`

Toggles showing ignored files (see `ido-ignore-files`

). *Available in Files / Buffers*.

`C-c`

Toggles if searching of buffer and file names should ignore case. (see `ido-case-fold`

). *Available in Dirs / Files / Buffers*.

`TAB`

Attempt to complete the input like the normal completing read functionality. *Available in Dirs / Files / Buffers*.

`C-p`

Toggles prefix matching; when it’s on the input will only match the beginning of a filename instead of any part of it.

`C-s / C-r`

Moves to the next and previous match, respectively. *Available everywhere*.

`C-t`

Toggles matching by Emacs regular expression.. *Available everywhere*.

`Backspace`

Deletes characters as usual or goes up one directory if it makes sense to do so.. *Available everywhere*.

`C-SPC / C-@`

Restricts the completion list to anything that matches your current input. *Available everywhere*.

`//`

Like most Linux shells two forward slashes in a path means “ignore the preceding path, and go back to the top-most directory”. Works the same in Ido but it’s more interactive: it will go to the root `/`

(or the root of the current drive in Windows) *Available in Files*.

`~/`

Jumps to the home directory. On Windows this would be typically be `%USERPROFILE%`

or `%HOME%`

, if it is defined. *Available in Files / Dirs*.

`M-d`

Searches for the input in all sub-directories to the directory you’re in.. *Available in Files*.

`C-k`

Kills the currently focused buffer or **deletes the file** depending on the mode.. *Available in Files / Buffers*.

`M-m`

Creates a new sub-directory to the directory you’re in. *Available in Files*.

OK, so you probably won’t get in the habit of using *all* the commands. That’s fine, but some are more important to remember than others, like: `Backspace`

; `C-s`

and `C-r`

; `//`

and `~/`

; and `C-d`

.

If Ido is getting in your way, remember the fallback commands: `C-f`

for files; `C-b`

for buffers.

### Work Directory Commands

Work directories are recently used directories that Ido caches so the files and directories in them can be quickly recalled. Work directory commands only function in `find-file`

routines, but that goes without saying.

You change the cached directory list by manipulating the variable `ido-work-directory-list`

. If you’re tired of Ido caching slow, transient or generally unwanted directories you can add regular expressions to the list in `ido-work-directory-list-ignore-regexps`

to keep Ido from caching them.

Similarly, when you go to the next or previous work directory you can force Ido to disregard directories that do not match your current input. To change this behavior, set `ido-work-directory-match-only`

.

| Keybinding | Description |
|---|---|
`M-n` , `M-p` | Cycles through the next or previous work directories. |
`M-k` | Kills (removes) the active work directory from the list. |
`M-s` | M-s forces ido to search the list of work directories for the current input. |

Using `M-s`

is an excellent way to quickly scan recently used directories for files. You do not have to explicitly type `M-s`

as Ido will automagically start searching after a few seconds of idle time.

You can change the work directory merge delay by modifying the `ido-auto-merge-delay-time`

variable.
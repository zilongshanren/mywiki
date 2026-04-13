---
title: Mastering Key Bindings in Emacs
url: https://www.masteringemacs.org/article/mastering-key-bindings-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Altering the key bindings in Emacs should not, on the face of it, be a difficult task. But there’s a reason why the Emacs manual has dedicated 30-odd pages to describing, in great detail, all the subtleties and nuances of how to bind keys.

To save you the time of reading all of that, I’ve written a guide that covers what you need to know to bind keys to even complex commands, and a set of templates you can use in your own code. And the best thing about this guide is that you don’t need to know any elisp to get started!

I’ve included a selection of handy templates near the end that you can customize and put in your init file.

## What makes up a key bind?

Emacs is “self-hosting” and, depending on who you ask, close to achieving sentience. Almost all of Emacs is written in Emacs Lisp. Every function in Emacs in turn builds on smaller functions, and so on, right through all the strata of elisp until you reach the C core.

Emacs’s key engine works in much the same way. Layer upon layer — or keymap upon keymap!

Even elementary things like inserting characters – called self-insertion – is amenable to change. For instance, the key `f`

is bound to `self-insert-command`

, a special command that repeats the last typed key *N* times. So if you type `C-u 10 f`

you will see `ffffffffff`

printed on your screen. As you can see, every keypress – even basic ones like typing a character on the screen – has an associated key binding that you can modify or even remove.

### What is a Keymap?

A *keymap* is an internal data structure used by Emacs to store keys and their associated actions. Keymaps are rarely modified directly; instead, you modify them through a set of functions that manipulate the data structure for you. Most Emacs users will never interact with keymaps aside from indirectly assigning keys to them.

Every buffer and most major and minor modes have a keymap, and that keymap defines what the keys do when key sequences are sent to that buffer. Keys can be divided into three categories: *undefined*, *prefix key*, or *complete key*.

*Undefined*is self-explanatory: it does no operation when it is invoked.*Prefix keys*are keys like`C-x`

and`C-c`

. They are make up part of a*complete key*, and each constituent part of a*prefix key*has its own keymap.- A
*complete key*is a key combination that resolves to a valid command. Like the key`g`

,`C-x C-f`

, or`<mouse-1>`

.

In Emacs, a key is not limited to just your plain-as-day keys on a keyboard. Anything that can generate an input event is fair game: two-factor authentication USB sticks, as they just ‘type’ stuff like keyboard would; that Hammond organ you’re eyeing as a replacement for your regular keyboard; and of course your mouse.

It is possible for Emacs to enumerate all the active minor and major mode key bindings in a buffer by typing `C-h m`

. That command is essential if you want to learn more about what a major or minor mode can do. Likewise, you can type out parts of a complete key (say `M-s`

) and then type `C-h`

to get a list of all keys that belong to that prefix.

If you know the name of a keymap, you can use `M-x describe-keymap`

in Emacs 28.

### Key Bind Commands

There are several ways you can define (or undefine) keys, as the table below shows, but in reality there are dozens of ways you can hack the keymaps.

I recommend you familiarize yourself with these, as they’re the ones you’re more likely to encounter:

`(define-key KEYMAP KEY DEF)`

Defines a key against a keyboard map. Use this if you want to change a keymap that isn’t the current buffer map.

`(local-set-key KEY COMMAND)`

Binds a key to the local keymap used by the active buffer, unlike

`define-key`

which takes an explicit keymap to bind a key against.`(global-set-key KEY COMMAND)`

Binds a key to the global keymap, making it available in all buffers (with a caveat – see below.)

`(global-unset-key KEY)`

Removes KEY from the global keymap

`(local-unset-key KEY)`

Removes KEY from the active, local keymap.

`(use-package :bind ( ... ))`

If you use

[use-package, a declarative configuration tool](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool)then you may prefer to bind your keys using its declarative notation. It’s similar to how the other commands work.

### Representing Keys in Code

In order to actually bind a key you must first tell Emacs what key you intend to use. Unfortunately there’s more than one way of representing keys in Emacs: as a *string*, or as a *vector*. We won’t concern ourselves with either, as we will use a handy macro built in to Emacs called `kbd`

. The `kbd`

macro translates a human-readable key into a format Emacs can understand.

One important point to note is that you **must** surround *function* and *navigation* keys with `<`

and `>`

:

That includes F-keys, arrow keys and home row keys, like so: `<home>`

, `<f8>`

and `<down>`

.

```
(kbd "<home>") ;; OK
(kbd "tab") ;; Wrong, but valid -- missing < and >
(kbd "<tab>") ;; OK
(kbd "C-c p") ;; OK
```


#### Remapping Commands

You can tell Emacs that you want to *replace* all keys pointing to a certain command with one of your own choosing by using the `remap`

notation.

You must do this instead of passing a key to the key bind function you are using. This is the best way of replacing existing commands with your own, as Emacs does the hard work of figuring out all the keys it needs to rebind.

Example:

`(define-key (current-global-map) [remap kill-line] 'my-homemade-kill-line)`


Here I globally remap all keys that point to `kill-line`

to `my-homemade-kill-line`

.

For a practical example of remapping in use, see [fixing the mark commands in transient mark mode](https://www.masteringemacs.org/article/fixing-mark-commands-transient-mark-mode).

### Reserved Keys

You can pick any keyboard combination you desire – even if that key bind is already taken, so be careful – but Emacs has set aside certain keys for use by users. Generally, all keys prefixed with `C-c ?`

(where *?* is a single character) are reserved for you, and you alone. In practice most third-party packages don’t care about the key bindings they occupy. So keep that in mind.

The other set of reserved keys are the F-keys from `F5`

and onwards. The other two prefix keys reserved to you are *hyper* and *super*. They are remnants from ancient keyboards used in the 80s, but live on today in Emacs. Most PC-compatible keyboards won’t have a *super* or *hyper* key so some people rebind the *Windows key* and the *Application Context* key to be *hyper* and *super* instead.

If you’re fortunate enough to have spent a large sum of money on a fancy mechanical keyboard, you may have keys to spare, and the firmware to rebind them as you see fit. I recommend you look into dedicated *hyper* or *super* keys; but don’t forget, you can also tell your firmware to bind a key to, say, `C-M-`

or even a prefix key, like `C-x`

. Be creative.

Anyway. Because of Emacs’s roots, it understands these keys natively, and they have their own modifier keys: `H-`

(e.g., `H-q`

) for *hyper*; and `s-`

for *super*. Note that `s`

is super and `S`

is shift.

In Windows you can add this to your init file to enable *hyper* and *super*:

```
(setq w32-apps-modifier 'hyper)
(setq w32-lwindow-modifier 'super)
(setq w32-rwindow-modifier 'hyper)
```


In X you’ll have to play around with *xmodmap* or your own tool of choice.

#### Keymap Lookup Order

Emacs will look for keys in a certain order, and that order I have described below. Keep in mind that only *active* keymaps are used, and that the order is top-to-bottom. The first “match” is the keymap Emacs uses.

`overriding-terminal-local-map`

for terminal-specific key binds.`overriding-local-map`

for keys that should override all other local keymaps. Be VERY careful if you use this!

Common use cases include in-buffer fields, like the ones you find in*Keymap char property at point*for keymaps that are local to the character point is at.`M-x customize`

.`emulation-mode-map-alists`

for advanced multi-mode keymap management`minor-mode-overriding-map-alist`

for overriding the keymaps used by minor modes in major modes.`minor-mode-map-alist`

is exactly like the*overriding*version above, but the preferred means of specifying the keymaps for minor modes.*Keymap text property at point*is like the one above for char properties but this is for text properties only.`current-local-map`

for keymaps defined in the buffers’ current local map`current-global-map`

is the last place Emacs looks. It hosts keys that are global.

But I can summarize these rules in a way that accounts for 99% of all key bindings you’re likely to care about:

- First, Emacs checks if there’s a minor mode key binding;
If there isn’t, then Emacs checks if there are any local keys set.

Typically this local map is shared by the major mode of the current buffer. So if you want to add a key binding to`python-mode`

, you can use`local-set-key`

to do this.- And finally global keys are checked.

This order confuses many new users! Most people think that a global key trumps all other keys, but that is not so.

#### Global vs Local

A global key is functionally identical to that of a local one, except it is declared in a “global” keymap, governed by the `current-global-map`

function (but usually it points to the default, the `global-map`

variable.) Therefore, you can define a global key simply by passing the `current-global-map`

function to `define-key`

. The other – often better – alternative is to use the designated function, `global-set-key`

.

In a similar vein, to bind a local key you can use the “designated” function `local-set-key`

or the more general `define-key`

. Like the global map, there exists an equivalent function `current-local-map`

that returns the keymap local to the buffer.

If you want to change major mode key bindings, you’re going to have to choose between explicitly updating its keymap with `define-key`

, or calling it from within the major mode’s buffer with `local-set-key`

. You can’t always interchange the two, although they’re supposed to yield the same outcome. The reason is that some major modes regenerate keymaps or outright reset them. When that happens you may have to choose one or the other.

## Defining your Command

If you thought the mechanics of keymaps and keys were difficult, think again! Deciding on what you want to bind to those keys is even harder – especially so if you want the command to do very specific things, like switching to a specific buffer name. But I’ve got a few tricks up my sleeve to help you cut out most of the elisp writing by letting Emacs do all the heavy lifting.

### Invoking a command

Before I talk about the how and why of Emacs commands it is important that I mention how Emacs handles *interactive functions* — commonly known as *commands*. An Emacs *command* has an `(interactive ...)`

form at the top of its function body. The `(interactive ...)`

form controls how the function must respond to user input when it’s invoked interactively. For instance, a command that prompts a user for a string must tell Emacs – using the `(interactive ...)`

form – how to do this.

All commands are executable through `M-x`

and can therefore be bound to a key.

When you bind a function to a key it is important that you keep the above in mind, as you **cannot** invoke a non-interactive function through a key binding — it must be a *command*.

If it is your intent – as it so often is – to call a function, but with explicit parameter values, you must wrap it in a little helper function, like a `lambda`

expression or even a standard `defun`

. I have prepared templates (see below) that show you how to do this.

### Describing the command

There are two ways of describing a command in elisp: the *manual* way, and the *smart* way. Let’s start out with the manual way.

The manual way is to use `C-h k KEY`

to describe what `KEY`

is bound to; the other way is to describe a function, `FUNCTION`

, with `C-h f FUNCTION`

.

Because Emacs is a self-documenting editor all functions, variables, keys, etc. known to Emacs are accessible through the `describe-xxx`

commands. Type `C-h C-h`

to see them all.

With the name of the command, you can now begin the process of reading the documentation string and call it with the requisite arguments it needs to work.

If you’re unsure how to do that, but you do know what you want, then you may want to give the *smart* way a go.

### Capturing Complex Commands

The smart way has a name, or rather a command: `repeat-complex-command`

, and it is conveniently bound to the key `C-x ESC ESC`

and `C-x M-:`

.

Because Emacs and elisp are, in effect, one and the same, it’s no surprise that Emacs keeps a running tally of the commands you’re executing, and when. That’s why `M-x repeat-complex-command`

is able to represent the Lisp form of the last command you executed. When you invoke `C-x ESC ESC`

you’re given the equivalent form in Elisp with the function arguments (if any) filled out for you. Emacs knows which arguments go where because of the `(interactive ...)`

form: it knows which function argument belongs to which interactive user-facing prompt.

Here’s a practical example: `C-M-% foo RET bar RET`

– which does a `query-replace-regexp`

replacing *foo* with *bar*. Now, if you type `C-x ESC ESC`

you should see something similar to this (reformatted for clarity):

```
(query-replace-regexp "foo" "bar" nil
(if (and transient-mark-mode mark-active)
(region-beginning))
(if (and transient-mark-mode mark-active)
(region-end)))
```


Observe how Emacs has kindly filled in all the function arguments to `query-replace-regexp`

, including the optional parameters. If you were to run that command again (by say pasting it into the prompt in `M-:`

) it’ll execute it in the exact same way as when you ran it interactively.

Here’s another one, this time I type `C-x b *scratch*`

to switch to the `*scratch*`

buffer:

`(switch-to-buffer "*scratch*")`


And there you have it. Obviously the commands seen here are the *interactive* commands. Stuff like replacing strings in a buffer is normally done with specialist elisp functions that don’t require user input, but that may not be a big deal if you are writing your own quick-and-dirty key binds.

### Keyboard Macros

I’ve talked about the smart way above, but there’s an even *smarter* way: Keyboard macros. If you have a series of actions you want to perform, then record it in a keyboard macro!

Emacs can record, and play back, almost everything. You’re not limited to shoveling text; stuff like moving files in dired, or splitting your windows and opening the right buffers in them is not only possible, but easy.

I recommend you read about Emacs’s [keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) to see what I mean.

## Putting it all together

We’re nearly done. I just need to explain a few more important concepts that confuse a lot of newbies: mode hooks and mode-specific keymaps, and then it’s on to the templates.

Most major and minor modes will *usually* set their keys once, when the module is first loaded; that’s good news for us. That means you can use `define-key`

to add key definitions straight into a mode’s key map. Some modes are very advanced, and have several key maps – `M-x isearch`

is a good example – and for those you will have to mess around with the source code or info manual to find out how to add keys.

Another option is `M-x describe-keymap`

(Emacs 28+) that shows all known key maps. You can probably narrow down the ones you want that way.

It’s the modes that force you to use a *mode hook* that’s the problem: for that you must set your keys when the mode is activated, and that takes a little bit more work.

It is a convention in Emacs that all major and minor mode functions (the ones that activate the mode) end in `-mode`

(e.g., `python-mode`

), and it is also expected that its *mode map* follows a common naming scheme: `xxxx-mode-map`

for the key map; and `xxxx-mode-hook`

for the mode’s hook.

With those mode hooks in mind, you can add a `local-set-key`

call and, hopefully, that’s all you need to override or add keys to the right mode’s key map.

### Keymaps

Modifying a keymap is dirt simple, you use `define-key`

as I’ve mentioned before. What’s not so easy is determining what keymap to modify in the first place.

#### Listing all the Mode Maps

If you type this Emacs will give you an apropos buffer with all the known mode maps that follow the major mode naming scheme:

`C-u M-x apropos-variable RET -mode-map$ RET`


You can also use `M-x describe-keymap`

and then pick the mode map you want from the candidate list.

#### Quick Keymap Example

Let’s say I want to extend `python-mode`

by adding a key, I’ll use `F12`

, that switches to the python process buffer. Currently, that’s bound to `C-c C-z`

and `M-x python-shell-switch-to-shell`

.

`(define-key python-mode-map (kbd "<f12>") 'python-shell-switch-to-shell)`


In order to get the command belonging to the key, I used `C-h k C-c C-z`

.

### Creating New Keymaps

If you want your own blank key maps, particularly if you want to build your own complex web of prefix keys and such, you’ll need to learn how to make your own.

Luckily it’s not too hard.

```
(defvar my-special-map
(let ((map (make-sparse-keymap)))
(define-key map "s" 'shell)
(define-key map "g" 'rgrep)
map)
"My special key map.")
```


First things first. We’ll need a variable, declared with `defvar`

so it won’t get reevaluated by accident. Not sure what I mean by that? Read my article on [evaluating elisp](https://www.masteringemacs.org/article/evaluating-elisp-emacs).

Next, we use a `let`

form to bind the variable `map`

to a *sparse* keymap created with `make-sparse-keymap`

. Sparse in this case means “empty”. Inside the `let`

form you can call `define-key`

and assign commands to keys.

There is also `copy-keymap`

if you want to copy another keymap and modify its copy instead. In fact, there’s a whole host of functions that deal with this. But I think these two are the ones worth knowing about if you’re building your own stuff.

Either way, you get a key map ready to go.

### Repeating Keys with repeat-mode

Emacs 28 formalizes – the code that does it has existed in Emacs for eons – a method of making *repeating key maps*. If you find yourself typing `C-x o`

over and over again to switch windows, then as of Emacs 28 you can type `C-x o o o o ...`

*ad infinitum* if you enable `M-x repeat-mode`

.

The new mode is easy to retrofit onto existing Emacs key map machinery if you know how.

#### Repeating Keys Example

**NOTE**: Make sure you enable `M-x repeat-mode`

.

Consider the keys `C-M-u`

and `C-M-d`

. They move out or into balanced expressions, like `( ... )`

, `[ ... ]`

, and so on. Perfect for most programming languages.

For this to work, you have to define the repeatable keys: the one-letter chords that take effect after you’ve invoked the primary key.

```
(defvar balanced-repeat-map
(let ((map (make-sparse-keymap)))
(define-key map "u" 'backward-up-list)
(define-key map "d" 'down-list)
map)
"Repeating map for balanced expressions.")
```


Next, we attach a property name and value to the commands that enable the repeating keys we defined in `balanced-repeat-map`

:

```
(put 'backward-up-list 'repeat-map 'balanced-repeat-map)
(put 'down-list 'repeat-map 'balanced-repeat-map)
```


And that’s it! When you next type `C-M-u`

or `C-M-d`

you’re given the option to type `u`

or `d`

instead.

### Hooks

A *mode hook* has zero-or-more functions that are called when its mode is activated. Mode-specific hooks are run when you activate that mode. That happens automatically when you open a file, or manually call `M-x some-mode`

.

#### Altering Mode Hooks

- Adding Hooks
You can add a mode hook using the special function

`add-hook`

that takes the name of a hook (say`python-mode-hook`

) and the name of a function to call.- Removing Hooks
You can remove functions from a hook variable with

`remove-hook`

. If you are experimenting you may want to remove hooks as part of your testing.In newer Emacsen you can call it interactively, select a mode hook, and then pick the one you want to remove. That is good to know when you inevitably add

`lambda`

functions to a mode hook and now struggle with duplicate hooks!

#### Listing all the Mode Hooks

If you are unsure of the exact name of the mode hook, you can use this handy trick to list the ones Emacs can see:

`M-x apropos-variable RET -mode-hook$ RET`


That will show **all** mode hooks known to Emacs, including their docstring description. If you don’t see your mode it may be because Emacs hasn’t loaded it outright. You can try `M-x load-library`

and see if you can load the package or library that way first.

#### Quick Hook Example

Let’s add a key (`C-c q`

to run `M-x shell`

) local to `python-mode`

using a hook. For that to work we will need our special hook function, I’ve named it `mp-add-python-keys`

, and in it we need `local-set-key`

, the function that adds a key to the active buffer’s local map. Remember that `local-set-key`

uses the local mode map.

Next is the command that tells Emacs that we want to add a mode hook to Python.

```
(defun mp-add-python-keys ()
(local-set-key (kbd "C-c q") 'shell))
(add-hook 'python-mode-hook #'mp-add-python-keys)
```


#### Setting Key Bindings with use-package

If you use [use-package](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool) then you can leverage its key binding facilities.

Let’s say you like the package `M-x winner-mode`

, a minor mode that records your window configurations and lets you undo and redo changes made to it, by you or by commands you execute.

```
(use-package winner
:config
(winner-mode 1)
:bind (("M-[" . winner-undo)
("M-]" . winner-redo)))
```


The `:bind`

property is there to do just that. Here I’ve bound `M-[`

and `M-]`

to two commands. Note the structure!

Another thing to keep in mind is that, unless you tell it otherwise, `use-package`

defaults to **global** key bindings.

If, on the other hand, you want to insert the keys into a *specific* key map, you need to tell `use-package`

the map to use:

```
(use-package eshell
:bind (("C-c e" . eshell)
:map eshell-mode-map
("M-m" . eshell-bol)))
```


Here I’ve chosen to bind `C-c e`

to `M-x eshell`

globally, as I have not specified a particular key map yet.

Next, I declare `:map eshell-mode-map`

and from that point on, that is the keymap `use-package`

uses when I ask it to bind `M-m`

to `eshell-bol`

.

So as you can see, it’s easy to bind to a variety of both global and keymap-specific maps.

## Templates

Here’s a bunch of templates for various use-cases that you can cut’n’paste and use in your own code. I recommend naming things sensibly, and giving them a docstring (in-code documentation that explains what the code does) as well. The best way to avoid accidentally overriding another function with the same name, I would suggest you use a moniker or prefix. I use `mp-`

for all of my own functions.

I also urge you to avoid the temptation of plastering your code with `lambda`

functions. They’re great, sure; but if you ever need to update or change them during your development and testing cycle, you may end up with duplicate functions in your mode hooks playing havoc.

If you are unsure how to evaluate elisp, then read my article on [evaluating elisp in Emacs](https://www.masteringemacs.org/article/evaluating-elisp-emacs).

### Basic Global Key Binding

Binds a command to a global key binding.

#### Definition

`(global-set-key (kbd "key-bind-here") 'interactive-command-here)`


#### Example

Binds `F1`

to `M-x shell`


`(global-set-key (kbd "<f1>") 'shell)`


### Add or Remove a Key to or from a Keymap

Adds or removes a key and its associated command to/from an explicit keymap. Use this if you know the name of the keymap and you want to add a key to it.

#### Definition

Add a key to a keymap:

`(define-key KEYMAP (kbd "key-bind-here") 'interactive-command-here)`


Remove a key from a keymap:

`(define-key KEYMAP (kbd "key-bind-here") nil)`


#### Example

Binds `C-c p`

to `python-switch-to-python`


`(define-key python-mode-map (kbd "C-c p") 'python-shell-switch-to-shell)`


### Complex Command Key Bind

Creates a global key bind that invokes multiple commands in a row. Use this to create compound keys or invoke commands that take parameters. Uses code from the *Function Template*.

#### Definition

```
(defun name-of-interactive-command-here ()
(interactive)
;;; Insert your compound commands below
)
(global-set-key (kbd "key-bind-here") 'name-of-interactive-command-here)
```


#### Example

Switches to the *scratch* buffer and inserts “Hello, World” where point is, and switches back to where it came from.

```
(defun switch-to-scratch-and-insert-text ()
(interactive)
(save-excursion
(set-buffer "*scratch*")
(insert "Hello, World")))
(global-set-key (kbd "C-c i") 'switch-to-scratch-and-insert-text)
```


### Binding keys with a mode hook

Use this mode hook template to bind keys that won’t work with a standard `define-key`

template, or if the key map is reset in when the mode is initialized.

If you have other, mode-specific changes, you want to apply at the same time, then this is the perfect place for you to do so.

#### Definition

```
(defun my-hook-function ()
;; add your code here. it will be called every
;; time the major mode is run.
)
(add-hook 'my-mode-hook #'my-hook-function)
```


#### Example

Here I change the python indentation offset to 4 and make it local to that buffer with `setq-local`

. Next, I disable `eldoc-mode`

and I locally bind a key with `local-set-key`

.

```
(defun mp-my-hook-settings ()
(setq-local python-indent-offset 4)
(eldoc-mode -1)
(local-set-key (kbd "C-c p" 'python-shell-switch-to-shell)))
(add-hook 'python-mode-hook #'mp-my-hook-settings)
```


As you can see, this is a good place to put all your other tweaks that relate to a specific mode.

### Remapping a command

This template will remap all keys that *point* to a specific command. Say you want to rebind `kill-line`

, bound to `C-k`

, but you want your code to only override the key binds that `kill-line`

is *actually* bound to. Use this template to replace existing commands with those of your own, without worrying about explicitly rebinding each key.

#### Definition

Note: to replace a global key, you must use `global-map`

or call `current-global-map`

.

`(define-key keymap [remap original-function] 'my-own-function)`


#### Example

Example here is taken from my article on [fixing the mark commands in transient mark mode](https://www.masteringemacs.org/article/fixing-mark-commands-transient-mark-mode).

I remap the keys that point to `exchange-point-and-mark`

to my own function `exchange-point-and-mark-no-activate`

.

```
(defun exchange-point-and-mark-no-activate ()
"Identical to \\[exchange-point-and-mark] but will not activate the region."
(interactive)
(exchange-point-and-mark)
(deactivate-mark nil))
(define-key global-map [remap exchange-point-and-mark] 'exchange-point-and-mark-no-activate)
```


### Custom Prefixes

Creating a prefix is easy nowadays as you don’t have to explicitly create your own prefix keymaps, provided you use `local-set-key`

or `global-set-key`

. Use custom prefixes to group or categorize your commands.

#### Definition

```
(global-set-key (kbd "subkey_1 ... endkey_1") 'my-command-1)
(global-set-key (kbd "subkey_1 ... endkey_2") 'my-command-2)
```


#### Example

Global keys that will insert either the time of the day, or the current date. Type `C-c i d`

to insert the date; and `C-c i t`

to insert the time. Type `C-c i C-h`

to list all bound keys under the `C-c i`

prefix.

```
(defun mp-insert-date ()
(interactive)
(insert (format-time-string "%x")))
(defun mp-insert-time ()
(interactive)
(insert (format-time-string "%X")))
(global-set-key (kbd "C-c i d") 'mp-insert-date)
(global-set-key (kbd "C-c i t") 'mp-insert-time)
```


### Repeating Key Maps with repeat-mode

This feature requires Emacs 28 and that you have turned on `M-x repeat-mode`

.

Repeating keys allow you to tap one or more single keys to repeat a command once you have engaged repeat mode by first typing a key that supports repeating keys.

Adding this functionality to existing commands in Emacs is easy.

#### Definition

For changes relating to a specific package, use this format:

```
(defvar my-repeat-map
(let ((map (make-sparse-keymap)))
(define-key map "a" 'some-command)
;; ...
(define-key map "z" 'another-command)
map)
"Repeating map example.")
```


Next, we attach a property name and value to the commands that should trigger `my-repeat-map`

:

```
(put 'some-command 'repeat-map 'my-repeat-map)
(put 'another-command 'repeat-map 'my-repeat-map)
```


#### Example

Activate this repeat map with `C-M-u`

or `C-M-d`

, then type `d`

or `u`

to move down or up.

```
(defvar balanced-repeat-map
(let ((map (make-sparse-keymap)))
(define-key map "u" 'backward-up-list)
(define-key map "d" 'down-list)
map)
"Repeating map for balanced expressions.")
(put 'backward-up-list 'repeat-map 'balanced-repeat-map)
(put 'down-list 'repeat-map 'balanced-repeat-map)
```


### Binding keys with use-package

If you are already using [use-package](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool) then you may as well use it to bind your keys also.

You can define global and local keys this way.

#### Definition

For changes relating to a specific package, use this format:

```
(use-package package-name-here
:bind (("kbd-here" . command-here)
:map some-map
("kbd-here" . another-command-here)
:map yet-another-map
("kbd-here" . some-command-here)))
```


But if you want a place to store global keys that don’t relate to any one package, use the package name `emacs`

instead.

#### Example

Here I bind `C-c e`

to `eshell`

globally, and `M-m`

to `eshell-bol`

locally.

```
(use-package eshell
:bind (("C-c e" . eshell)
:map eshell-mode-map
("M-m" . eshell-bol)))
```


## Conclusion

I have covered almost every facet of key binding that most Emacs users would care to know about. If you use `use-package`

, then it can definitely cut down on some of the tedium and help centralize your bindings with your other settings.

I recommend you read why I think [keyboard macros are misunderstood](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) as it’ll further cement just how much “no-code” Emacs you can accomplish with keyboard macros and key bindings.
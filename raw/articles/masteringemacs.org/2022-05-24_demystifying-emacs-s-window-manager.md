---
title: Demystifying Emacs's Window Manager
url: https://www.masteringemacs.org/article/demystifying-emacs-window-manager
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Emacs is a fantastic tiling window manager, and not enough people know that. There, it’s out now; I said it; now everybody knows. And thanks to a number of consolidations and improvements, it’s no longer the indomitable black box it once was.

At some point in the distant past, Emacs got into the business of handling frames. I’m sure you, like me, eschew frames in favor of windows. Frames are just that much harder to deal with — unless you’re using an actual tiling window manager, of course. But few do, and the baleful support for frames in regular window managers nix any temptation to make it work.

Later on, tabs also joined the family business. `M-x tab-bar-mode`

adds tab-style window configurations to Emacs, and `M-x tab-line-mode`

a way of browsing visible buffers.

Back to windows. They’re one of Emacs’s greatest assets, and they’re highly configurable. Historically it was a rather difficult affair to control window and buffer placement as you’d have to rein in a cavalcade of variables and functions and hope they did what you wanted. But not any more.

Modern Emacs is now able to mirror the paneling so beloved of IDE users, and without the tears! And you can easily control how or where buffers and windows must go, giving you even more control over your Emacs experience. That means you may not need a third-party window management library – if you ever tried to use one, that is – for most things.

So here’s a snapshot of what is possible today:

- Grouping Windows
You can now group windows so certain commands that affect one now affect all of them. They’re given the cryptic name

*atomic*.When you call

`C-x 0`

and delete an atomic (ugh) window, all other windows that belong to that cohort also disappear. It does come with a couple of limitations, but it’s still a great feature.- Dedicating Windows
You can dedicate a window to a buffer. Dedicated windows are locked to the buffer it was dedicated to, and so any attempt to switch its buffer will merely display that buffer in another window. And if you switch to a buffer that belongs to a dedicated window, Emacs selects the dedicated window instead.

This feature solves another common complaint: that it’s easy to screw up a perfectly manicured window layout – like

`gdb`

’s debug view,`M-x calc`

, your fancy Org agenda setup, and so on – because you accidentally switched buffers in one of them.- Sidebars
You can now attach a window to one of the four sides of a frame: left, right, top or bottom. Sidebars are like their kin in other IDEs: they are a full-length (or full-width) windows that resist switching and splitting.

With a sidebar you can finally dedicate sides of a frame to specialized buffers, like the Calendar, Org Agenda, Compilation Output, GDB, you name it. And thanks to a handy command, you can toggle the sidebars to hide or show them all at once.

- Override window and buffer placement
Almost all window customization now involve one – albeit elephantine – variable that controls all of it.

Much like Emacs’s reformed

[minibuffer completion system](https://www.masteringemacs.org/article/understanding-minibuffer-completion)you’re able to precisely control how Emacs creates and shapes windows using a tiered system of overrides. And package authors can still suggest a preferred layout that you can override if you want to.Using a regular expression you can command all python buffers to appear only in open windows that already have python mode buffers; you can order

`M-x eshell`

to always pop up a new window, no matter what; or insist that`M-x compile`

buffers appear as a side bar on the right-hand side of your screen, and that it must never change your selected window’s buffer.You can also dictate if you can switch to windows with

`C-x o`

, or even prevent Emacs from deleting a window, and thus preserve your layout, even if you use`C-x 1`

.

These four concepts give you near-complete control of all aspects of Emacs’s window management, and that’s not even everything. Yet they’re enough to put you firmly in the driver’s seat.

And the best thing about it all? Experimenting with it is easy and interactive. If you use my snippets of [templates and examples](https://www.masteringemacs.org#templates-examples) you can use them as a starting point for your own window excursions.

## Important Terminology and Concepts

### Switching Buffers

There is a subtle but important distinction between displaying a buffer and switching to it. Switching is done with `C-x b`

(or its sibling commands, like `C-x 4 b`

) and it is the default user-facing key binding for switching a window’s buffer.

By default Emacs distinguishes between automatic and manual window switching. If you effect a window switch yourself with `C-x b`

, it’s manual — and exempt from any display action rules you create yourself.

**You probably don’t want that**. I recommend you set this:

```
;; Requires Emacs 27+
(setq switch-to-buffer-obey-display-actions t)
```


Now Emacs treats manual buffer switching the same as programmatic switching.

However, it also guards against (some) misbehaving commands you may encounter: those that call out to `switch-to-buffer`

programmatically. That is “against the rules”, as `switch-to-buffer`

is a *user-facing* command.

### Picking the Right Window

Thanks to a concerted cleanup, `display-buffer`

is now the ultimate arbiter of where your buffer and/or window goes. And that’s a good thing indeed, as the previous system required a mish-mash of `let`

-bound variables and mystery functions to do what you wanted.

`M-x display-buffer`

is both a command and an important internal function. It’s called in one of several ways. Here are two common scenarios:

- A function somewhere wants to compel Emacs to display a buffer in a frame, like
`M-x calendar`

. - You have manually switched buffers with
`C-x b`

,`C-x 4 b`

,`M-x ibuffer`

or some other means.

Eventually they – if they’re programmed right – call, either directly or indirectly, `display-buffer`

to do this. By centralizing the display of buffers you can more easily control how it happens.

Programmatically, `display-buffer`

takes an optional `ACTION`

argument with a *suggested* display action. At this point in time, the `ACTION`

is a *guideline*. Emacs may, or may not, follow it; that’s important, because `display-buffer`

decides where things go, and it does so by consulting this list:

- First it checks
`display-buffer-overriding-action`

, but that is for Lisp use only, so we won’t talk about it again. - Then it checks
`display-buffer-alist`

, which we very much*will*talk about, as it’s the most important variable in Emacs’s window management system. - Then it checks the
`ACTION`

argument. Then it checks

`display-buffer-base-action`

, which is a catch-all default.It’s a user-facing variable you can configure, and unlike

Although we won’t talk about it much, it’s mostly there so you can build a catch-all rule for windows that don’t fall under rules 1, 2 or 3.`display-buffer-alist`

it can only hold one`ACTION`

.At last it checks

`display-buffer-fallback-action`

, but that is also for Lisp only.The variable is only consulted last, and it’s the variable of last resort if there are no other actions that match.


Although the term `ACTION`

is thrown around a lot, it’s a bit of a misnomer, I think. It’s really a *constraint*. It is a mixture of “do *that*” along with “but only if *these facts hold true*”.

You see, when you ask Emacs to display a buffer it checks the aforementioned list. Each variable in that list may hold – particularly in the case of `display-buffer-alist`

– rules that Emacs must check before it decides on the next course of action.

The first set of constraints – actions – that satisfy Emacs, wins. It’s perfectly fine to have more than one set of constraints that match a given buffer; just know that the first one Emacs encounters is the one it picks.

So as you can see, the `ACTION`

argument in #3 is really more of a guideline, even though the package author had a particular layout in mind when they wrote it. That means elisp hackers can’t know for sure if Emacs will *actually* display a buffer the way they intended — good!

Look no further than `M-x speedbar`

for a disastrously bad example of curtailing choice. Speedbar only works in a standalone frame, and it’s impossible, without a third-party hack, to get it to display in a window.

#### Predicated Actions

The `display-buffer`

function checks a list of variables (and its own `ACTION`

argument) to determine what it needs to do. They’re all, in one way or another, made up of `ACTIONS`

.

Here’s the name of a function, and one part of, an action: `display-buffer-same-window`

. As its name alludes to, it’ll display a buffer in the same window (same refers to the *selected* window.) Its definition looks like this:

```
(defun display-buffer-same-window (buffer alist)
(unless (or (cdr (assq 'inhibit-same-window alist))
(window-minibuffer-p)
(window-dedicated-p))
(window--display-buffer buffer (selected-window) 'reuse alist)))
```


Asking Emacs to put something in the same window is only possible if:


This flag – more on it later – instructs Emacs to never put something in the same window. Which, of course, in the case of`inhibit-same-window`

is not`t`

in`ALIST`

.`display-buffer-same-window`

defeats the point of the display function!The window is not the minibuffer.

We can’t use that, for obvious reasons.The window is not dedicated.

Dedicated windows resist attempts to change their current buffer.


If it’s none of those things, then the predicate succeeds and the buffer is displayed in the selected window. The search is over, and `display-buffer`

has done its job.

Note that there’s a mixture of both predicates and logic to carry out the work and that’s because – back to my argument about *constraints* – that in order for Emacs to put a buffer somewhere it must first ascertain whether it’s even possible.

In the unlikely event that Emacs is *not* able to place a buffer, it’ll eventually consult `display-buffer-fallback-action`

and pick an option from that list.

### Constraint Satisfaction

Consider this. If you split your frame into a kaleidoscope of windows, each doing their own thing, and you then add a bunch of custom rules, like:

`*info*`

and`*Help*`

windows go in a sidebar on the left;- All Python buffers recycle existing Python windows;
`*Compilation*`

mode buffers always pop up in a new window, split along the top, with a height of 10 lines.`*EShell*`

buffers, once shown, are marked dedicated.

You’re giving Emacs a large number of rules it must abide whenever you display a buffer. Not only must Emacs respect the rules you’ve defined in `display-buffer-alist`

, but it must also contend with the *existing* windows and their buffers in your frame.

Now where should the next buffer you want to display go?

That is the dilemma Emacs faces when it must place both a buffer and maybe create a window. For every rule you add, you are constraining Emacs’s ability to pick (what it thinks) is the best place for a window or a buffer.

Dedicated windows, sidebars, forcing Emacs to re-use a window, or enforcing a minimum height or width for a window — they all add up to to a laundry list of *constraints*.

Emacs is not always able to do what you tell it to. Given a sufficiently complex web of rules, it’s possible those rules conflict with one another (and your current window layout) and so Emacs is unable to follow those rules.

That is why Emacs has a “safety valve”, of sorts. It’ll do its darnedest to respect the rules you set, and if it can’t, it’ll turn maverick and just display it somewhere. That’s why, despite Emacs’s best intentions, it may switch a buffer in a window you told it not to touch, or even – as the *last* resort – create a brand-new frame.

It’s rare, but it can happen.

### Trees, Windows and Internal Windows

Emacs tracks your current window layout in a tree structure called the window tree. The window tree represents the dimensions and location of every window in your current frame. A tree structure is ideally suited to this task, as subdivisions are either horizontal or vertical, which Emacs represents as nodes in the tree. The tree also knows where your minibuffer is, but that is not very interesting to us, although it *has* a window also.

You can browse your current window tree [by evaluating](https://www.masteringemacs.org/article/evaluating-elisp-emacs) `(window-tree)`

.

When you split a window, Emacs creates a new node in the tree that holds the *live windows* (the ones with buffers in them.) But as you successively split windows, you’ll end up with nodes in the tree that aren’t *actual* windows in your frame. Those nodes are called internal windows.

Internal windows aren’t terribly interesting to us, so I won’t belabor their role in Emacs’s window tree much. The only thing you need to know is that whenever you split a window, Emacs needs to keep track of each distinct, *live*, window you see on the screen. It does so with ‘invisible’ windows called internal windows.

Consider this:

```
+----------+-----+-----+
| | | |
| R1 | R2 | R3 |
| | | |
+----------+-----+-----+
```


If `R1`

is the selected window and you want to split below, then all you need to do is call `C-x 2`

. But if you want to split *across* `R1`

through `R3`

you can’t — not with `C-x 2`

anyway.

But it *is* possible: but you must split from the shared parent of `R1`

, `R2`

and `R3`

— an internal window.

Without an internal window, or some other structure that can represent the relationship between windows, you wouldn’t be able to split across those three windows.

Although it’s not super-duper important to know about, internal windows play an important role when you want to carry out actions that involve the parent, children or siblings of windows.

## Splitting Windows

*Note: Emacs 29 adds native support for this. See M-x split-root-window-<right/below>.*

The default split commands – `C-x 2`

and `C-x 3`

– split below or to the right of the selected window. Sometimes, though, you may want to split from the *root* of the tree. So if you want a full-length window below or to the right of all your other windows, you can, with a little bit of elisp:

```
(defun mp-split-below (arg)
"Split window below from the parent or from root with ARG."
(interactive "P")
(split-window (if arg (frame-root-window)
(window-parent (selected-window)))
nil 'below nil))
```


You’re free to replace `below`

with `right`

if you want it to split to the right instead, or swap the order of the `if`

statement if you’d rather invert the operation.

If you want to bind it to a key, check out my article on [binding keys in Emacs](https://www.masteringemacs.org/article/mastering-key-bindings-emacs).

This command works well when you want to split against the parent of the selected window, or from the root with `C-u`

.

Indeed, `split-window`

is the function that all the other ones call when they want to split a window. The distinguishing factor is the `WINDOW`

argument, as it controls the window you want to split from.

Splitting from `RT1`

with `M-x mp-split-below`

yields:

```
+----------+-----+-----+
| | RT1 | RT2 |
| +-----+-----+
| | RB2 |
| L1 +-----+-----+
| | |
| | RB1 |
| | |
+----------+-----------+
```


And with `C-u M-x mp-split-below`

:

```
+----------+-----+-----+
| | | |
| | RT1 | RT2 |
| L1 | | |
| +-----+-----+
| | RB1 |
+----------+-----------+
| B1 |
+----------+-----------+
```


This concept plays a role in a few of the display `ACTION`

functions we’ll look at later.

## Dedicating Windows

When you dedicate a window, you’re effectively saying that you would *prefer* that Emacs does not switch the buffer in that window for another. It’s not an ironclad guarantee; there are instances where Emacs is up against the wall and has to put something *somewhere*.

Having said that, window dedication works well, and you should definitely use it.

A dedicated window confers the following benefits:

Switching buffers manually with

`C-x b`

fails with an error.You can customize

`switch-to-buffer-in-dedicated-window`

and control how it behaves.I set it to

`pop`

, because I want it to open the buffer somewhere else instead. But there’s also`ignore`

, and it’ll ignore your switch;`nil`

, which raises an error and stops the switch; and`t`

, that undedicates the window and switches.Note that if you use custom completion frameworks that circumvent

`C-x b`

(`switch-to-buffer`

) like[Ido Mode](https://www.masteringemacs.org/article/introduction-to-ido-mode)it may not behave exactly this way.- Splitting a dedicated window with
`C-x 2`

and`C-x 3`

fails with an error. - Emacs will not switch buffers in dedicated windows.

However, dedicated windows are not immovable objects. You can still delete the windows with `C-x 0`

or `C-x 1`

; kill the buffers they belong to; or resize them.

The function `set-window-dedicated-p`

handles the dedicating. Unfortunately it’s not exposed to users by default, so let’s fix that by making a little elisp helper that toggles dedication in the selected window:

```
(defun mp-toggle-window-dedication ()
"Toggles window dedication in the selected window."
(interactive)
(set-window-dedicated-p (selected-window)
(not (window-dedicated-p (selected-window)))))
```


Note that the documentation is quite diffuse about the flag you can set. Here I toggle between `t`

or `nil`

, but it accepts a range of non-`nil`

values. Values like `side`

is not as *strong* a dedication as setting it to `t`

is.

But yeah. Just toggle between `t`

and `nil`

and it’ll generally behave the way you want.

Another approach is setting `dedicated`

flag directly in `display-buffers-alist`

, but more on that later.

The command is still useful, though: you can set and unset it as part of your window layout workflow, by [using a keyboard macro](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood).

## Side Windows

Side windows are full-length windows attached to either the `left`

, `top`

, `bottom`

or `right`

-hand side of a frame. You can have more than one side window attached to the same side of the frame, and you can have sidebars on more than one side at a time.

A side window and a dedicated window go hand-in-hand, and they share many similarities. Side windows are also dedicated, but they set `dedicated`

to `side`

, which is not as strong a promise as setting it to `t`

.

Every side in a frame has a number of slots, controlled by the `window-sides-slots`

variable. If you want to use side windows, then I strongly recommend that you customize it and set limits on how many you’ll allow on each side. Once you exceed the number of slots, Emacs will instead cycle the buffers in the existing side bar windows.

Side windows are special because you can order them relative to one another using their `slot`

, an integer position.

They also benefit from a really neat command that toggles side windows visible or invisible: `M-x window-toggle-side-window`

. Really useful command to know about if you’re flanked on all sides and want to briefly toggle them off.

One thing to be aware of is that, if you’re experimenting with windows, that the frame’s *window state* can get out of whack. The fix is to [evaluate this form](https://www.masteringemacs.org/article/evaluating-lisp-forms-regular-expressions):

`(set-frame-parameter (selected-frame) 'window-state nil)`


## Controlling Buffer and Window Display

If you want to control where a buffer or window must appear, you must customize `display-buffer-alist`

.

It’s a little… complex. Well, actually, once I explain how it all fits together, you’ll see that it is not.

The first thing you should do is customize it with `M-x customize-option`

. Insert an entry and click around a bit to get a feel for what it’s about. Don’t worry too much about making sense of the component parts of it yet. I’ll explain that in a moment.

### Recommended Settings

First things first though. I want you to consider customizing these, and at least consider why I want you to change them:

`switch-to-buffer-in-dedicated-window`

Controls what happens if you, as a user, attempt to switch buffers in a dedicated window. (Remember, sidebars are also a form of dedicated window.)

I prefer

`pop`

to the default, as I’d rather have it pop up the buffer somewhere else than simply error out. That then goes hand-in-hand with the next variable.`switch-to-buffer-obey-display-actions`

If

`nil`

, the default, user-switched buffers are exempt from display buffer actions set in`display-buffer-alist`

& friends. Requires Emacs 27.You probably want those rules to affect your interactive buffer switching, as it makes for a consistent buffer switching experience. I set it to

`t`

myself.I find that some packages and functions disregard all rhyme and reason and use

`switch-to-buffer`

instead of`display-buffer`

when they want to show a buffer to the user.**This is wrong**. And the net result is that your display rules won’t apply if this variable is not set to`t`

.

### Testing and Experimenting

If you’re not an elisp expert I recommend you use the *Customize* interface.

You can use it to browse and tweak `display-buffer-alist`

, even though my examples below use elisp. So my suggested workflow is:

[Evaluate](https://www.masteringemacs.org/article/evaluating-elisp-emacs)the elisp you want to test.`M-x customize-option`

on`display-buffer-alist`

.You’ll see the newly-added entry, and you can modify it in-situ.

(If it’s already open,`M-x revert-buffer`

reloads the Customize interface.)- Apply changes with
`C-c C-c`

to test them.

### Creating a `display-buffer-alist`

entry

A `display-buffer-alist`

entry consists of:

- A
`CONDITION`

, which is either a string or a function - An
`ACTION`

, which is either a function or a list of functions - An optional
`ALIST`

of flags and settings

#### Defining a `CONDITION`


Every entry must have a `CONDITION`

, which is either a regular expression matched against the buffer name, or a function that returns `t`

if a buffer name is a valid match or `nil`

if it is not.

Practically speaking you are limited to searches by buffer name with regular expressions. That’s *almost* always enough. If it is not, you have to use a function (and I’ll show you how to make one later on.)

Common reasons for needing a function include wanting a condition that triggers if a buffer belongs to a derived mode, for instance.

If you need help writing your regular expressions, then I recommend you use Emacs’s [interactive regexp builder](https://www.masteringemacs.org/article/re-builder-interactive-regexp-builder).

#### Choosing the Predicated `ACTION`

s

When you have defined your `CONDITION`

, you can give it *either* a singular `ACTION`

or a `(ACTION_1 ... ACTION_N)`

list of actions.

But what’s an `ACTION`

? Well, the description for `display-buffer`

does proffer a list of suggested `ACTION`

functions, **but this is not the complete list**.

To get the complete list you… well, you have to hope they’re sensibly named.

This is one way to find the builtin ones:

`C-u C-h a ^display-buffer-[^-]`


Note that you may find a few stray functions that have nothing to do with windows. But as you scan the list, you’ll see a pattern:

```
display-buffer-below-selected
display-buffer-at-bottom
...
```


They’re `ACTION`

entries. Or as I prefer to think of them: predicated actions.

Recall that they not only determine where something goes, but also check if they’re able to carry out the action in the first place!

Whether you specify a single `ACTION`

or a list of `ACTION`

s, the outcome is the same:

Emacs cycles through one of more `ACTIONS`

and it stops **when it receives the window the buffer was displayed in**.

That means you can order your preferred display methods in the order you want Emacs to try them. It also means that a sneaky display action can change stuff and *not* return a window — necessitating more work by Emacs. That is, as far as I know, only used in one place (so far.)

For instance, you can declare that `*Help*`

windows must:

- First
`display-buffer-reuse-window`

, which tells Emacs to find an existing`*Help*`

window and re-use that one. - Next, try
`display-buffer-pop-up-window`

and pop up a new window with the buffer. - And if that fails, the entire display entry is skipped and Emacs continues with the next one in
`display-buffer-alist`

.

That example works like this:

```
(add-to-list 'display-buffer-alist
'("\\*Help\\*"
(display-buffer-reuse-window display-buffer-pop-up-window)))
```


##### Useful `ACTION`

Functions

Here’s a list of some of the more useful display buffer functions you can use. As always I encourage you to use apropos to find the complete list yourself.

**NOTE**: If you use the customize interface, know that not all the functions below appear in the dropdown. You may have to select `Other Functions`

and type in the name below for this to work.

Some of the `ACTION`

functions require additional setttings to work. More on how to set them below. I recommend you `C-h f`

the functions you want to use.

`display-buffer-below-selected`

Attempts to display the buffer immediately below the selected window.

This is useful for contextual popups that you want near the selected window that triggered the buffer display.

You can optionally specify a setting of

`window-min-height`

that governs the required minimum size of the new window.`display-buffer-in-atom-window`

Marks the window as atomic when it is displayed somewhere. It will ‘stick’ to nearby atomic windows, if such windows exist.

You can control where it is displayed relative to an existing window by setting

`window`

.You must also specify a

`side`

where the new window is created, relative to`window`

.Useful for “shared” windows that must only exist as long as the other, related, windows exist.

One example is

`M-x calc`

and its calculation window and history window.`display-buffer-in-child-frame`

Really intriguing option that pops up an internal child frame, as opposed to a top-level frame. So it’s more like an in-frame popup window than a standalone window.

You can control its frame parameters with

`child-frame-parameters`

.`display-buffer-in-direction`

Displays a buffer in a window in an absolute direction from a window.

The default

`window`

is the selected window, and so it’s a generalized version of`display-buffer-below-selected`

, but capable of displaying the buffer in any`direction`

.If you set

`window`

to root you can split across the height or width of the entire frame.`display-buffer-in-tab`

/`display-buffer-in-new-tab`

**NOTE:**These display actions only return a valid window – thus ending the search –*after*initializing the tab, and*only*if the buffer is already present in a window. That means you can use these actions to initialize the tab and*another*action to refine what happens after that has taken place.Places a buffer in a (new) tab. Note that this refers to

`M-x tab-bar-mode`

and not the tab*line*mode.Tab bars are effectively tabbed window configurations, and a great addition to Emacs.

`display-buffer-in-tab`

pops a buffer in a tab named`tab-name`

(and optionally part of a`tab-group`

.)If the tab does not exist, it is first created. If you use

`display-buffer-in-new-tab`

then a new tab is always created, and existing ones are never reused.Tab groups are collections of tabs; they are not displayed by default, so customize

`M-x customize-option tab-bar-format`

first.`display-buffer-no-window`

Do not display the buffer in a window at all.

Useful if you want to suppress a buffer from showing. Great for throw-away buffer windows that insist on appearing even if you do not want them to.

`display-buffer-pop-up-window`

Pops a buffer in a new window. If you want Emacs to always requisition a new window for a buffer, use this.

`display-buffer-reuse-mode-window`

Force Emacs to reuse a window that has a buffer with

`mode`

major mode.Great if you have either a selection of major modes that you want a buffer to reuse. Use it to instruct Emacs to always open, say, Javascript files in existing

`js-mode`

windows.The

`mode`

setting also works with a list of major modes. It also uses`derived-mode-p`

to check if a buffer’s major mode qualifies: that means you can type`prog-mode`

to catch all the many programming modes.`display-buffer-reuse-window`

Reuse a window if it is already displaying that buffer.

So if you want Emacs to reuse the window that is already displaying the buffer, then use this. Note that you can force Emacs to disregard the window if it is the

*same*window you’re in. Set`inhibit-same-window`

to`t`

.`display-buffer-other-frame`

/`display-buffer-pop-up-frame`

/`display-buffer-use-some-frame`

Much like their window cousins, you can instruct Emacs to pop up a buffer in another frame if is already displaying the buffer.

You can also tell it to always pop up a new frame, or simply use any frame it likes.

`display-buffer-same-window`

Forces Emacs to display a buffer in the currently selected window.

Note that it respects window dedication (including sidebars), so it will not work there.

`display-buffer-use-least-recent-window`

Instructs Emacs to prefer the LRU (least recently used) window.

How it determines that is how often you (or Emacs) has interacted with a window.

`display-buffer-use-some-window`

Displays the buffer in some window in your frame. If you don’t care where a buffer is put, you can use this.

It also supports

`inhibit-same-window`

, so if you want it to display anywhere but your current window, set that flag.

`ACTION`

Settings

In addition to one or more `ACTION`

entries, you can – sometimes must – specify *settings* that fine tune how Emacs places a buffer or window.

I call them *settings* but they don’t have, as far as I can tell, a formal name beyond `ALIST`

in the description for `display-buffer-alist`

. `ALIST`

is just a generic word for association list, so I’ll refer to them as settings from now on.

You can find a list of settings in `C-h f display-buffer`

but it is, yet again, not a complete list. (But you should read the list of settings, nonetheless.)

Some `ACTION`

functions have their own requirements. They are usually listed in that function’s docstring. An example is `display-buffer-in-side-window`

:

```
The following two symbols, when used in ALIST, have a special meaning:
‘side’ denotes the side of the frame where the new window shall be located. Valid values are ‘bottom’, ‘right’, ‘top’ and ‘left’. The default is ‘bottom’.
‘slot’ if non-nil, specifies the window slot where to display BUFFER. A value of zero or nil means use the middle slot on the specified side. A negative value means use a slot preceding (that is, above or on the left of) the middle slot. A positive value means use a slot following (that is, below or on the right of) the middle slot. The default is zero.
```


The manual is also a good choice if you want further information. (Press `i`

in the Help buffer.)

##### Useful `ALIST`

Settings

I’ve included some of the more interesting `ALIST`

settings here that I think most people would find useful:

`inhibit-same-window`

It defaults to

`nil`

, but if you set it to`t`

then Emacs will ignore any desire to place a buffer in your same (selected) window.Use

`inhibit-same-window`

to force Emacs to place a window in a different window from your current one, even if the function would prefer to use your current one.This setting is used by

`display-buffer-in-previous-window`

,`display-buffer-use-least-recent-window`

,`display-buffer-use-some-window`

, etc.`window-height`

,`window-min-height`

and`window-width`

Controls the ultimate window size. Great if you know roughly how big you want the window to be, in height or width.

If you specify an integer then it’s a constant-sized window.

If you use a floating point number you can instead make it scale to the size of the frame.

`0.25`

is 1/4th the frame size, for instance.You can also give it a function and Emacs will attempt to use that function to size the window. Try

`fit-window-to-buffer`

. Note that it may not be able to fit the window to the buffer!The width and size settings only apply to some functions.

`window-min-height`

in particular only works with`display-buffer-below-selected`

.`preserve-size`

Orders Emacs to preserve (or not) the height and/or width of a window. It’s a cons form with the following format:

`(WIDTH . HEIGHT)`

.Replace

`WIDTH`

or`HEIGHT`

with`t`

or`nil`

to preserve or not preserve the size in that direction.`dedicated`

Marks the window dedicated if

`t`

. You can also set it to`side`

, but I don’t recommend that. Stick to`t`

and`nil`

.`side`

Used by

`display-buffer-in-side-window`

and`display-buffer-in-atom-window`

.Set

`side`

(`bottom`

,`left`

,`top`

,`right`

) to determine the direction you want the window to be.`slot`

Controls the integer

`slot`

where the window must go. Used by`display-buffer-in-side-window`

.`direction`

Used by

`display-buffer-in-direction`

and it places the window in`direction`

of the selected window.`direction`

must be one of`left`

,`up`

,`right`

,`bottom`

.Great if you prefer your

`M-x calendar`

or`M-x calc`

windows to always appear at the top or bottom.`mode`

Reuses an existing window provided it has one of

`mode`

major modes.This is used by

`display-buffer-reuse-mode-window`

and it’s great if you want to reuse windows based on a major mode.You can combine ‘similar’ major modes, like

`Info-mode`

and`help-mode`

and Emacs will dutifully put a buffer in any one of those.`window-parameters`

Very useful, but requires that you know the names of useful window parameters.

There are many, and I recommend you explore a window of your choosing by evaluating this:

`M-: (window-parameters (selected-window))`

Of

*particular*interest, I think, are the following:`no-delete-other-windows`

If

`t`

, the window is not deleted when you call`C-x 1`

.Great for side bars and other important windows.

`no-other-window`

If

`t`

, the window is unselectable with`C-x o`

.Great for windows where you want to look, but not interact with, the contents of the buffer in that window.

You can still click-select the window or

`C-x b`

to it. It’s only removed from the`other-window`

(`C-x o`

) cycle.

The

`window-parameters`

setting is itself an alist.

#### Putting it all together

Now that you know how each component part of a display entry works, let’s look at a few different ways of constructing them.

I still recommend you use the *Customize* interface if you’re not interested in hacking around with elisp.

The most basic of display entries looks like this:

```
(add-to-list 'display-buffer-alist
'("\\*Compilation\\*"
display-buffer-reuse-window))
```


We match against one buffer name, `*Compilation*`

; with one `ACTION`

, `display-buffer-reuse-window`

; and no `ALIST`

settings, so it’s not listed.

A more complicated example might look like this:

```
(add-to-list 'display-buffer-alist
'("\\*info\\*"
(display-buffer-in-side-window)
(side . right)
(slot . 0)
(window-width . 80)
(window-parameters
(no-delete-other-windows . t))))
```


There’s a bit more going on here. I want `*info*`

windows in a side bar window; it must be on the right-hand `side`

and in `slot`

0; the `window-width`

must be 80; and Emacs must set the window `no-delete-other-windows`

window parameter to `t`

.

```
(add-to-list 'display-buffer-alist
'("\\*Help\\*"
(display-buffer-reuse-window display-buffer-pop-up-window)
(inhibit-same-window . t)))
```


Here I insist that `*Help*`

buffers reuse any existing `*Help*`

window if such a window exists. And if that is not possible, it must pop up a new window. Furthermore, Emacs cannot use the same (selected) window, and it must use another.

## Limitations

Let’s talk limitations. There’s a large corpus of third-party packages – and a number of internal ones in Emacs – that don’t know or care about cooperating with you or your window configuration. More often than not it’s because they believe their settings are the best; they may well be right, but it’s still wrong. And older packages are at least partially excused, as they predate the modernization efforts. But there’s a large body of up-to-date packages that don’t create or manage windows correctly even when it’s most likely easier to do so.

If you encounter such a package – they are more common than you think – you have little in the way of recourse beyond working around the code, or raising an issue with the maintainer(s).

In particular, package authors must use `display-buffer`

(or `pop-to-buffer`

) and avoid the temptation to write long tracts of elisp that manicure a window immediately after displaying a buffer. Calling out to `display-buffer-xxxx`

actions is also not allowed.

## Moving Around & Undoing Window Changes

If you’re not already aware, `M-x winner-mode`

is a builtin minor mode that lets you undo (and redo) window configuration changes. They’re bound to `C-c <left>`

and `C-c <right>`

, respectively, by default.

There’s also a near-equivalent for tab bar window configurations called `M-x tab-bar-history-mode`

. You can now run `M-x tab-bar-history-forward`

and `M-x tab-bar-history-backward`

to cycle through changes made in the active tab’s window layout.

I also want to quickly mention `windmove`

. It’s a package that makes it possible to move (switch to a buffer) in all four cardinal directions using – by default – `S-<left/right/up/down>`

. It notably got an upgrade in Emacs 28 to let you delete or create windows in a direction also.

You may prefer `windmove`

to `C-x o`

. I prefer `M-o`

though as the default is awful. [More about my personalized key bindings here](https://www.masteringemacs.org/article/my-emacs-keybindings).

## Templates & Examples

Here’s a selection of templates that demonstrate all the concepts you’ve read so far. They’re designed to selectively override how Emacs displays buffers and windows.

I recommend, as always, that you experiment thoroughly. That is easiest if you don’t `add-to-list`

(it’s all too easy to end up with near-duplicated entries) but instead `setq`

or the *Customize* interface.

One common theme that I see a lot of newer users ask for is a way of *repeating* their favorite layouts, particularly between restarts or if the layout is changed. So I recommend [you record a keyboard macro](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood). Keyboard macros are more than capable of not only opening files, splitting windows or switching buffers, they can do nearly everything you can do. So give them a try. No elisp required.

Another suggestion is to use `tab-bar-mode`

. A tab is merely a window configuration — nothing more, nothing less.

### Handy Helpers

You don’t have to use a regular expression to match buffer names. There’s a little mini-language you can use instead; it’s usually enough for most things.

Instead of the `car`

of your `display-buffer-alist`

entry containing a string, you can use a form that is interpreted by Emacs’s display mechanism.

The docstring for `buffer-match-p`

explains it all, but I’ll throw in a few examples.

#### Matching with the buffer matching language

```
(add-to-list 'display-buffer-alist
'((or (major-mode . Info-mode)
(major-mode . help-mode))
(display-buffer-reuse-window
display-buffer-in-side-window)
(reusable-frames . visible)
(side . right)
(window-width . 0.33)))
```


Instead of a complex regex that may fail to match every possible name that use either `help-mode`

or `Info-mode`

, I’ve instead opted for the form `(or (major-mode . Info-mode) (major-mode . help-mode))`

that will match if the major mode is either of those two.

The docstring starts bloviating about `cadr`

this and `cdr`

that to describe what you can put where; but I think it’s easier to just think of it as:

- Either a cons cell with an explicit rule in the shape of
`(A . B)`

. Where`A`

is something like`major-mode`

, or`derived-mode`

and`B`

is the value it must match; - A (nested) bool form of
`(BOOL REST)`

where`BOOL`

is`or`

,`and`

, etc. and`REST`

is any number of cons cells or more BOOL values.

There are other things you can put in there, like a string, which is what most people think of when they use `display-buffer-alist`

. So you can indeed use the boolean system to test multiple regexes; or a combination of calling a function, checking the `major-mode`

, and so on.

#### Only match buffers that have a project

```
(defun mp-buffer-has-project-p (buffer action)
(with-current-buffer buffer (project-current nil)))
```


Returns non-`nil`

if a buffer belongs to a project – i.e., `C-x p p`

– and it is another way to match buffers.

You can use this inside the matcher code

### Frustration-Free Window Recycling

This setup tames all those annoying windows that keep popping up when you run a command, even if there’s already a window with a similar buffer. [VTerm](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) is one such culprit.

**NOTE**: As I explained earlier, you can only modify well-behaving windows. Some packages – even some of the ones *in* Emacs – are not, and they may ignore your attempts to tame them.

#### Example 1: Preventing Popups & Reusing a Window

This snippet instructs any buffer named `*vterm*`

to reuse a window with a major mode of `vterm-mode`

or `vterm-copy-mode`

. Changing `inhibit-same-window`

to `t`

prevents Emacs from reusing the selected window if it’s a `vterm`

window (you’ll instead get a new window.)

```
(add-to-list 'display-buffer-alist
'("\\*vterm\\*" display-buffer-reuse-mode-window
;; change to `t' to not reuse same window
(inhibit-same-window . nil)
(mode vterm-mode vterm-copy-mode)))
```


#### Example 2: Reusing Windows

Here I collect a bunch of buffer names and ask that they share their *respective* buffers’ windows. That is, `*xref*`

always reuses an `*xref*`

window; a `*grep*`

buffer a `*grep*`

window, etc.

```
(add-to-list 'display-buffer-alist
`(,(rx (| "*xref*"
"*grep*"
"*Occur*"))
display-buffer-reuse-window
(inhibit-same-window . nil)))
```


Here I default to `display-buffer-reuse-window`

.

If you have a random selection of buffers that pop up here and there, you can collect them all in one rule that forces them to reuse an existing window if such a window exists.

#### Example 3: Matching by major mode

One common problem is matching against one or more major modes. Sometimes, it’s simply not possible to match against the buffer name.

Consider [Magit](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git) that has a large range of buffer names and major modes.

```
;; Required. But note that this _does_ change Magit's default buffer display behavior.
(setq magit-display-buffer-function #'display-buffer)
(add-to-list 'display-buffer-alist
`((derived-mode . magit-mode)
(display-buffer-reuse-mode-window
display-buffer-in-direction)
(mode magit-mode)
(window . root)
(window-width . 0.15)
(direction . left)))
```


This snippet forces magit to reuse *any* `magit-mode`

-derived buffer window already present.

If there is no such buffer, Emacs will instead create a window in the `left`

-most direction with a width of 15% of the frame for all `magit-mode`

-derived modes.

### Hiding Buffers

You can also instruct Emacs to not show a window at all if it matches a buffer pattern.

#### Example

This hides `*compilation*`

buffers. You can still *switch* to them, but their display is inhibited when created.

```
(add-to-list 'display-buffer-alist
'("\\*compilation\\*" display-buffer-no-window
(allow-no-window . t)))
```


Great for all those annoying popups where you only care about the contents when something goes wrong.

### IDE-style Windows

This setup emulates the paneling you often find in commercial IDEs. They are more often than not attached to the sides.

- The bottom of the screen is used for ephemeral
[Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell)or`Shell`

mode buffers, for command line shell access. The right-hand side is a side bar

[for compiling and running scripts](https://www.masteringemacs.org/article/compiling-running-scripts-emacs)with`M-x compile`

or the output from`*Grep*`

.The sidebar is sacrosanct, so it prevents deletion with

`C-x 1`

. It is also marked dedicated, so you cannot`C-x b`

inside it by accident. This also stops Emacs from reusing it for other things.- Any buffer named
`test_`

is opened to the immediate right of the selected window.

#### Example

This first part controls the shells. It will force Emacs to place them at the bottom, with a window height of no more than 30% of the size of the frame.

```
(add-to-list 'display-buffer-alist
'("\\*e?shell\\*" display-buffer-in-direction
(direction . bottom)
(window . root)
(window-height . 0.3)))
```


Controlling side windows is equally straight forward. I recommend you limit the number of side window slots – `nil`

means infinite, and a positive number the maximum you’ll allow – as that means Emacs swaps out the buffer in that `slot`

instead of creating a new entry. Great for situations where you have a handful of ephemeral things – compilation, test output, shell command output, etc. – that you want to share windows.

I also set a window parameter, `no-delete-other-windows`

, that prevents Emacs from destroying the side window when you type `C-x 1`

. It also has a fixed size of 80.

```
;; left, top, right, bottom
(setq window-sides-slots '(0 0 1 0))
(add-to-list 'display-buffer-alist
`(,(rx (| "*compilation*" "*grep*"))
display-buffer-in-side-window
(side . right)
(slot . 0)
(window-parameters . ((no-delete-other-windows . t)))
(window-width . 80)))
```


And don’t forget: you can type `M-x window-toggle-side-windows`

to toggle them visible or hidden.

This snippet places a buffer to the immediate right of the current window if the buffer name starts with `test_`

or `test-`

.

```
(add-to-list 'display-buffer-alist
`("^test[-_]"
display-buffer-in-direction
(direction . right)))
```


Tweak it to use something else, of course. Maybe header files if you’re hacking on C or C++.

### Tab-Based Workflows

**NOTE**: This makes use of Emacs’s `M-x tab-bar-mode`

.

Also, I recommend you customize `tab-bar-format`

and change it so that you show formatted groups.

#### Grouping Buffers into a Named Tab

Let’s say you frequently work with Org mode files, and you want them to appear in a separate tab. That tab is your dedicated Org mode tab; only org-related stuff should appear in it.

```
(add-to-list 'display-buffer-alist
`((or (derived-mode . org-mode)
(derived-mode . org-agenda-mode))
(display-buffer-in-tab display-buffer-in-direction)
(ignore-current-tab . t)
(direction . bottom)
(window-height . .2)
(tab-name . "🚀 My ORG Mode Files")
;; Optional
(tab-group . "Org")))
```


This creates a display entry that routes `org-agenda-mode`

and `org-mode`

major modes to:

A tab called

If you leave out`🚀 My Org Mode Files`

. If the tab does not exist, it is first created.`tab-name`

Emacs will instead auto-generate it. That’ll generate lots of new tabs. So beware.- The tab-group
`Org`

is also set up if it does not exist. The group is optional and is not a requirement. If the buffer Emacs is displaying is already visible in a window in that tab bar, then Emacs stops the search.

*However*, if it is not, Emacs will**continue with the search**and apply`display-buffer-in-direction`

in that tab.The newly-minted window is given a height of 20%.


As you can see, `display-buffer-in-tab`

is special: it’s capable of creating a tab and handing over the window display to a subordinate display routine.

#### Tabs for Elfeed

![Tabbed Elfeed Example](../../assets/9e42f78c42654d61.png)

[Elfeed](https://github.com/skeeto/elfeed) is an Atom/RSS newsreader. It’s an excellent package, and you can read [Mastering Emacs](https://www.masteringemacs.org/feed/) in it.

Here I force Elfeed to use unique buffers for each elfeed article. I then match both the generic search buffer and the entry pages and show them in a dedicated tab group called `📻 Elfeed`

. The tab name is auto-generated and sourced from the feed title.

```
(setq elfeed-show-entry-switch #'pop-to-buffer
elfeed-show-unique-buffers t)
(add-to-list 'display-buffer-alist
`("^\\*elfeed-entry-"
(display-buffer-in-tab)
(dedicated . t)
(tab-name . (lambda (buffer alist)
(with-current-buffer buffer
(concat "🚀 " (elfeed-feed-title (elfeed-entry-feed elfeed-show-entry))))))
(tab-group . "📻 Elfeed")))
(add-to-list 'display-buffer-alist
`("\\*elfeed-search\\*"
(display-buffer-in-tab)
(dedicated . t)
(tab-name . "📣 Entries")
(tab-group . "📻 Elfeed")))
```


#### Project Tabs

This creates a tab group for each project – as defined by `C-x p p`

and Emacs’s project management implementation – and with each buffer getting its own tab. Buffers without projects are ignored.

**NOTE:** This is more of a demonstration; you’d probably want to tweak this quite heavily to match your workflow which does, unfortunately, require some elisp skills. It’s also not 100% free of bugs or quirks either!

```
(defun mp-buffer-has-project-p (buffer action)
(with-current-buffer buffer (project-current nil)))
(defun mp-tab-group-name (buffer alist)
(with-current-buffer buffer (concat "🗃 " (or (cdr (project-current nil)) "🛡 Ungrouped"))))
(defun mp-tab-tab-name (buffer alist)
(with-current-buffer buffer
(buffer-name)))
(add-to-list 'display-buffer-alist
'(mp-buffer-has-project-p
(display-buffer-in-tab display-buffer-reuse-window)
(tab-name . mp-tab-tab-name)
(tab-group . mp-tab-group-name)))
;;; OPTIONAL, but probably required for everything to work 100%
(defun tab-bar-tabs-set (tabs &optional frame)
"Set a list of TABS on the FRAME."
(set-frame-parameter frame 'tabs (seq-sort-by (lambda (el) (alist-get 'group el nil))
#'string-lessp
tabs)))
(defun mp-reload-tab-bars (&optional dummy)
"Reload the tab bars... because they're buggy."
(interactive)
(tab-bar-tabs-set (frame-parameter nil 'tabs)))
(add-hook 'kill-buffer-hook #'mp-reload-tab-bars)
(add-hook 'window-selection-change-functions #'mp-reload-tab-bars)
```


The optional code at the end is there to, ah… fix a few ‘quirks’ in tab bar’s implementation. Basically the tab groups (as you seem them in the tab bar) don’t sort by the tab group, so you end up with duplicates, which is weird. The hooks are there to try and rein in consistency bugs where the tab bar’s not updated as frequently as it should be.

## Conclusion

With a little bit of work you can (probably!) coax Emacs to do what you want it to do. The window manager is not perfect by any means, but I think it’s good enough to accommodate a large range of workflows.

If you build something nifty, by all means let me know.
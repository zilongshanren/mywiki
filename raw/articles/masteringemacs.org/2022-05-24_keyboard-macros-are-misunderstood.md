---
title: Keyboard Macros are Misunderstood
url: https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

What would Emacs be without Emacs Lisp? Elisp is there to help you with the bugbears that bedevil your daily life.

And I think that’s great! Knowing elisp greatly expands your capabilities in Emacs. But, *but*, maybe you don’t know it — it’s yet another thing to learn. You may not have the time or the inclination. That’s especially true if you just want to customize or automate simple tasks.

Not everyone who uses Emacs is a programmer. It has a wide audience, and that’s a really good thing, too. But that also ratchets up the difficulty if you have to pick up a programming language – possibly your first ever – to get simple things done. It’d be nice if you didn’t *have* to do that for simpler tasks. That’s where keyboard macros enter the frame. In Emacs they are very powerful, and as I’ll show you in a moment, more than capable of great feats of automation.

Keyboard macros are misunderstood, and they can do an awful lot more than most people *think* they can do. They’re amazing for text editing. But they can do so much more than that. And the reason for this knowledge gap – even in people possessing much Emacs-fu – is that it’s hiding its capabilities in plain sight. That, and the siren song of elisp: it calls out to all of us, but you need not heed its call if you just want to do simple automation!

Emacs’s keyboard macros can do pretty much everything *you* can do, except make human decisions about what to do next – but even here Emacs’s macro system has a few tricks up its sleeve.

*Because* Emacs is able to record and play back nearly anything in a keyboard macro, you can leverage that to do things you wouldn’t normally think a keyboard macro *should* do, like:

- Modifying your window layout
Like your windows split a certain way, with certain buffers in certain places? Why not record a macro to do it for you. You can make it resize the windows, too.

And if you need it, you can create several macros. Each one turns your window layout into something specialized and specific to your immediate needs. You can mix in some frame and tab action, too!

Just make sure you start with a call to

`C-x 1`

to reset the windows back to one when you start the recording.Heck, you can even tell your macro to store the idealized window configuration in a register before it stops, if you’d rather recall your setup from one of those. (Window configurations are registers and they don’t persist between Emacs sessions.)

- Visit files and Special Buffers
Combined with custom window layouts, you can have Emacs open a particular file in each window. Open up a magit buffer, maybe

`M-x calendar`

, or something else entirely.- Speed up interactions with Org mode
Do you regularly open up the Org mode agenda, only to apply filters and settings? Sure, you can

*customize*it, but maybe you can get by with a macro.- Call up a Shell and execute commands in it
Make it run

`C-u M-x shell`

(or[Eshell](https://masteringemacs.org/article/complete-guide-mastering-eshell), or Vterm, or…) and run some commands that you frequently need to do.Or just call out to

`M-x comint-run`

or`M-x compile`

for those one-off programs that you want to run. The possibilities are endless.- Search & replace common terms
If you find yourself having to bulk edit buffers, you can record a macro to do this for you. Maybe you have to make multiple passes, or you

*actually*have to do some text editing with a macro. (Yes, it’s obviously great at that too.)Why not combine it with tools like

`M-x rgrep`

or Xref to find text matches across a large swathe of files, and use`M-g M-n`

in a keyboard macro to bulk edit? Record the macro so it does one file, and then play it back and watch as it churns its way through the list of matches in your`*Grep*`

buffer.

OK, so those are just some of the things you can do with keyboard macros. And you know what, this approach will solve 80% of those annoying “I wish I knew elisp so I could solve this one problem” questions that frequently dog newer Emacs users. Window management is especially hard for beginners, particularly for those who come from IDEs with fixed layouts.

What keeps people from using macros for serious work is the mistaken impression that macros are impermanent and go away when Emacs does. By default they *are* impermanent, but you can tell Emacs to persist them with a couple of commands. More on that in a second. That makes ’em far more useful for repeat use.

But let me just quickly get the macro basics out of the way if you’re new to them.

## Keyboard Macro Basics

If you’re new to them, here’s a very quick table to get you started. I’m just scratching the surface here. You can do a lot of crazy stuff with them. Just know that keyboard macro commands are named either `kmacro-`

or they *contain* the word `kbd`

. Many `kmacro-`

commands are bound to the prefix key map `C-x C-k`

. Explore it with `C-x C-k C-h`

.

| Key Binding | Description |
|---|---|
`F3` | Starts macro recording, or inserts counter value |
`F4` | Stops macro recording or plays last macro |
`C-x (` and `C-x )` | Starts and stops macro recording |
`C-x e` | Plays last macro. Give prefix arg to repeat arg times |

You can optionally give a prefix argument to `C-x e`

or `F4`

to make it repeat the macro that many times. Use `0`

to tell Emacs to run the macro until it gets an error signal. A macro plays back until it encounters an error (end of buffer, end of matches in `*Grep*`

if you advance with `M-g M-n`

, and so on.) Watch out if you’re waving `C-g`

around in a macro — it terminates the recording!

If you call `F3`

when you’re recording, it’ll insert a number from a counter and increment it. Use a universal arg (`C-u`

) and it’ll repeat the last number without incrementing it. You can pass a numeric arg to `F3`

to start the recording with a different number.

This feature’s obviously great for numerating lists.

But call `F3`

with `C-u`

twice and you’ll instead append to your last macro.

You can do *way* more than this, but that’s the gist of it.

## Naming and Saving Keyboard Macros

In order to persist a macro you have to name it first. You do that with `C-x C-k n`

, or `M-x kmacro-name-last-macro`

. Recorded macros enter a macro ring – much like the kill, history or undo rings – but I recommend you name them if you think you’ll use them again later. Much easier than trying to find it again with `C-x C-k C-n`

and `C-x C-k C-p`

. Try running a named macro by invoking it with `M-x`

.

I strongly urge you to name your macros sensibly – ideally with a prefix. I use `mp-`

.

To persist it, you can ask Emacs to spit out an interactive function (a command) that is a like-for-like Elisp representation of the macro. To do this call `M-x insert-kbd-macro`

. Emacs will ask for a named macro and insert a code-generated, interactive function at point. I recommend you insert it in your `init.el`

file. It’s already named and evaluated at this point.

One thing that annoys me, and maybe it annoys you too, is the inconsistent command naming. The logical answer is because the `kbd`

-named commands predate the `kmacro-`

ones by many years.

The naming scheme is inconsistent and it lacks a key binding. So let’s fix that:

```
(require 'kmacro)
(defalias 'kmacro-insert-macro 'insert-kbd-macro)
(define-key kmacro-keymap (kbd "I") #'kmacro-insert-macro)
```


Much better. Now you can find it again easily under `kmacro-`

and it also has as its own key: `C-x C-k I`

.

There’s also a way to bind macros to keys (with `C-x C-k b`

) or registers (with `C-x C-k x`

) but they won’t persist. I recommend that you instead just call `M-x global-set-key`

or `M-x local-set-key`

if you want commands temporarily bound to keys, notwithstanding the register stuff, which is a great feature, if you are already familiar with it. But the global/local set key commands have the added advantage that you can bind keys to any command you like, and not just keyboard macro commands.

## Interactive Keyboard Macros

One neat, little feature is the ability to insert a *macro query* flag when you are recording a macro. A *macro query* is only triggered when you play it back. Emacs detects the query and pauses execution and cedes control back to you. To use it, type `C-x q`

when you’re recording. There is no visual indicator when you type it, though.

On playback you are then asked to pick from one of these options when the macro reaches the query flag:

| Query Key Binding | Description |
|---|---|
`y` | Continues as normal |
`n` , `DEL` | Skips the rest of the macro |
`RET` | Stops the macro entirely |
`C-l` | Recenters the screen |
`C-r` | Enters recursive edit |
`C-M-c` | Exits recursive edit |

That makes it excellent for what I call *interactive* macros that require user input. You can place the *macro query* anywhere you like — even in a prompt, like query replace regexp with `C-M-%`

. You can even prefill the prompt; Emacs will remember that also.

As the table shows, you’ve a number of options when control is ceded to you. I like `C-r`

as it breaks out of the macro into a recursive edit session. Recursive editing is Emacs’s way of letting you pause something mid-way through, only to resume it later as though you were never gone. You can nest recursive editing levels more or less as much as you’d reasonably like.

You can even run a whole new macro *inside* a recursive editing step. You can even run *the same one*! It’s macros all the way down.

Emacs takes you back from whence you came when you back out of a recursive edit level with `C-M-c`

. It’ll pick up where you left off when you entered it. You can tell you’re in a recurive editing step if you see `[ ]`

in your mode line. `ESC ESC ESC`

breaks out of all of them, if you just want to bail out now.

## Lossage & Step-Editing Macros

When you type stuff Emacs keeps a record of it. Check it out: `C-h l`

. You can turn parts of your *lossage* into a keyboard macro also with `C-x C-k l`

. You can edit the buffer and use `C-c C-c`

to commit the contents to a macro that you can then play back.

You can also edit the last macro you have set with `C-x C-k C-e`

. Occasionally useful if you’re doing something complex and you made a slight mistake. It works the same as the lossage interface. Heck, you can create brand new macros this way also, if you’re crazy enough.

The *pièce de résistance* is the ability to step-wise edit a macro with `C-x C-k SPC`

. Much like a debugger, you step through each playback step and you can decide what you want to do each step of the way.

The step editor is loosely modeled on the *query replace* interfaces (like `M-%`

and `C-M-%`

) so if you have some familiarity with that, your knowledge applies here too.

| Step Edit Key | Description |
|---|---|
`C-h` | Show inline help |
`SPC` , `y` | Act (apply) current command |
`n` , `d` , `C-d` | Skip and delete current command |
`TAB` | Repeatedly act (apply) this command and all similar ones |
`!` , `c` | Continue playing back the macro |
`C-k` | Skip and delete rest of macro |
`q` , `C-g` | Cancel step editing |
`u` , `U` | Undo once / Undo all |
`i` , `r` | Inserts / Replaces a series of commands until you enter `C-j` |
`I` , `R` | Inserts / Replaces a single command |

Stepping and editing is a supremely powerful feature that you should at least know about, even if you never use it. I find buffer editing a macro a bit easier to do as it’s easy to make a mistake step editing your macro, and before you know it you’re step editing your step edited macros. But the power of being able to step through and correct errors and insert or replace missing commands is undeniably powerful, and I’ve not even included all the commands you can use!

## Conclusion

Macros are great. And you don’t need elisp to get started either. Being able to configure your window layout with a quick keyboard macro is actually a bit of a super power. If you want to do that in a way that is persistent and stable and *easily interchangeable* you don’t have many options beyond elisp; maybe the `frameset`

library; and third-party packages.

And that’s to say nothing, of course, of the ability of keyboard macros to edit text. They’re definitely amazing at that also. But I think it’s all too easy to *only* look at them in that light. And if you’re new or unfamiliar with Elisp then it’s an easy way to supercharge your Emacs by *recording how you want it done*.

Oh, and believe me, I haven’t even *scratched* the surface of what you can do with keyboard macros in Emacs. So, if you do something cool with macros, I’d love to hear about it!
---
title: Switching from Vim to Emacs
url: https://www.masteringemacs.org/article/switching-from-vim-to-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If Dante Alighieri, author of the poem *The Divine Comedy*, had written it today, he would surely have versified about one of his layers of hell freezing over when someone switches between Vim and Emacs. Well, it’s frigid somewhere today, and you’ve decided to take the plunge!

Welcome to Emacs. You’ll find that it’s a welcoming community, with a large number of Vim users who use it daily, with or without Vim key bindings.

I’ve written this article to help you with *some* of the things you should know about Emacs and your move from Vim (or be it Vi or Neovim) to Emacs.

I can’t promise I’ll cover every question you may have, but this should serve as a guide for Vim users switching to Emacs. There are far too many workflows for me to possibly cover all of them, so what I am trying to do is capture a representative sample of the many Vim users I have worked with or helped over the years, and the most common criticisms (many of them legitimate) and observations they had.

If you have only barely opened Emacs, you should first start by running through the builtin tutorial (see `Help -> Emacs Tutorial`

or type `Control + h`

then `t`

.) The tutorial does not take long to complete, and it covers the absolute basics. I then recommend you read *my* [Emacs tutorial](https://www.masteringemacs.org/article/beginners-guide-to-emacs). In the tutorial I talk a little bit about some of the ‘softer’ things you should know. I really do recommend you read both, even if you’re convinced you are going to use a Vim emulation layer in Emacs.

And speaking of Vim emulation in Emacs. Let’s start with that.

## Vim Keybindings in Emacs

A lot of Vim users who switch to Emacs use the third-party package *Evil mode*, a feature rich Vim emulation layer in Emacs. There is also *Viper*, which is built into Emacs, but it is not as complete in its emulation as Evil, and it only emulates *Vi* and not Vim. One advantage of Viper is that it was built around the idea of Vi users starting out with a near-complete Vi emulator and then gradually disabling Vi features, with native Emacs features taking their place. It also means you can use it in places where you may not have access to *Evil mode*.

Which one you prefer is up to you, but most people use Evil mode as it’s actively maintained.

You can of course immediately turn on a Vim emulation layer, and it’ll work well in many instances, but Viper/Evil mode do not work well everywhere. There are features in Emacs with poor or no Vim emulation at all. Particularly in more complex packages (often third-party, but not always), and outside of regular text editing especially, where the package authors have – as you might expect – built things around the assumption that you are using Emacs key bindings. Usually it’s just a case of manually rebinding the keys to suit the temperament and expectation of Vim users. But not always.

Another problem you’re going to face is that literally everything you read about Emacs, especially in its documentation and docstrings, assume Emacs key bindings. You’re going to have to face up to the challenge of actually understanding how Emacs works, even though you can get by without for a long while.

This ‘fish out of water’ situation is a common one you see when people move abroad to a country where they do not speak the language. You can often get by with English for a good long time, but eventually you’re going to have to learn the local language. Vim in Emacs is much the same thing, even if you never end up actually using Emacs’s own key bindings. You would do well to dip your toes and learn how things work underneath your Vim emulation layer.

Vim users who come to Emacs fall into two, broad categories:

- Those looking for Vim but in Emacs, because they want things you can do in Emacs that they cannot do with Vim alone, but they also want to keep their preferred key bindings;
- And those open to using the default key bindings, or at least with the intent of doing so, once they have settled in.

Both are fine. For it is ultimately a personal choice. But heed my advice about learning how Emacs works, regardless of the category you most closely align with.

## Emacs is different

Emacs is just… different. I don’t mean it like you have a kooky uncle who mows his lawn at night and collects Albanian pottery. No, Emacs is simply a completely different tool with its own ways and means of doing things.

I’ve spoken to a lot of Vim users (or VSCode, or Atom, or…) who come to Emacs and expect it to accommodate every minor feature they had in their old editor. It’s possible that Emacs can – perhaps with the aid of a third-party package – do exactly that, but chances are Emacs does its own thing. Sometimes that *thing* is better than what you had before, and you just have to adapt your workflow and keep an open mind; perhaps it’s worse.

So I recommend you keep an open mind. And if you’re still not happy, you can always invest some time in trying to bend something that kinda-sorta does what you want to your will. That’s the power of Emacs and Lisp. I recommend the builtin manual *Introduction to Emacs Lisp*. See `Help -> More Manuals -> Introduction to Emacs Lisp`

.

## Asking for Help

You must learn to ask Emacs for help. It has an incredibly detailed manual, so make sure you read it. Additionally, because Emacs is a living and breathing computing environment powered by Lisp, every: key binding, function, variable, mode, and face is automatically documented and searchable in real time, so it always matches what ever your current Emacs setup is. I recommend you check out the `Help`

menu bar entry. Of note is the ability to find out what a key binding does. That system is called the *Describe* help system, and it can answer many questions related to your Emacs environment. Try it: `Help -> Describe -> Describe Key or Mouse Binding`

(or type `C-h k`

) and then type a key. It’s contextual, so you get an answer from the point of view of the buffer you entered it in.

Forget what a command does? Not sure what that flashy, new programming mode can do? Having a hard time discovering all the customizable whirligigs and doodads you can play with in Org mode?

Ask Emacs. It should be the second resource you check (after the manual, provided there is one!)

Learning how to ask Emacs the right questions is a key thing to Emacs mastery. It’s a topic I dedicate a lot of time to in my book, [Mastering Emacs](https://www.masteringemacs.org/book).

## Modal Editing in Emacs vs Vim

Here’s a common trope: Vim is a modal editor and Emacs is not. Someone’s probably told you this; maybe you have read it somewhere; or perhaps you objectively believe it is so. The thing is… it’s not really true. Emacs is also a modal editor. And I don’t mean “hey you can emulate Vi or Vim, ergo Emacs is modal.” No, I emphatically mean that vanilla Emacs is also a modal editor.

Let me explain.

In Vi and friends, you switch explicitly between modes in order to do different things. From insert back to normal mode, for example. In Emacs, you actually do much of the same, but actively entering and leaving a mode is not the only type of ‘modal switching’ employed in Emacs.

For example:

- If you type
`n`

in a buffer named`notes.txt`

, you’ll type the letter`n`

on the screen, because`notes.txt`

uses a specialized*major mode*for text editing called`text-mode`

. - If you
*hold*the`Control`

key and type`n`

, you’ll instead move your point (cursor) down one line. - Press
`n`

in a*dired*buffer (Emacs’s file manager accessible with`C-x d`

) and you’ll instead move the point down to the next file (provided there is one, of course.)

Three different things, and all involve the letter `n`

. But they are three different modalities of operation. You can think of `Control`

as a mode much like, say, *insert* is a mode in Vim. But instead of being something you switch to with a keystroke, in Emacs you’re expected to hold down the key: it is momentary.

Back to dired. In dired, `n`

is a shorthand to move to the next file or directory. It then positions your point (cursor) so it is at the beginning of the file or directory, because that is a sensible thing to do in a file manager where you act on files using the location of your point.

It also retains the same mnemonic that `C-n`

does, but with the added benefit of being even easier to type as you don’t have to hold down `Control`

. But because people are so used to typing `C-n`

, that key binding *still* works (but instead of running the underlying command `next-line`

, it instead calls `dired-next-line`

.)

You cannot *type* the letter `n`

because that is not a useful thing to do, really, in dired, by default. However, just to highlight the shifting sands that is modality in Emacs, you can alter dired by putting it into a specialized ‘writable dired’ mode by typing `C-x C-w`

. Now you *can* edit the dired buffer directly: instead of moving to the next line, `n`

now inserts that character (provided your point is inside a filename in the dired buffer) so it’s a good thing indeed that `C-n`

still moves to the next line, or you’d have no way of moving to the next file without resorting to the arrow keys or the mouse.

So as you can see, the marriage of all these keys and modes is complex – my article on [Mastering Key Bindings in Emacs](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) is a good overview once you’re a bit more familiar with Emacs – but it boils down to the basic idea that in Emacs it is not just about being in a singular mode (Insert, normal, etc.) as it so often is in Vim, but that Emacs’s modes come and go depending on what you are trying to do, and there may well be more than one mode active at the same time. Some commands only trigger when you press and hold certain modifiers keys (such as `Meta`

or `Alt`

, `Control`

, `Shift`

, etc.) and therefore your *keyboard’s* modifiers are modal. Other commands make themselves known to you, in turn, only when you invoke certain commands or key bindings. Yet more depend on where your point (cursor) is in the buffer.

Most (but not all) key bindings follow a simple set of rules. Because every buffer must have a major mode – the most basic is called *fundamental mode* – and because every major mode must declare the keys it accepts, that means the major mode is often the determinant in what you can and cannot do in a buffer in Emacs.

But key bindings are also layered in Emacs, and one layer can override another, as I showed when you enable writable dired. Global keys – such as `C-n`

to move to the next line – are available everywhere by default. It is considered so fundamental to Emacs that it is enabled everywhere by default. You can explore the globally set keys (or indeed any other keymap!) by typing `M-x describe-keymap RET global-map RET`

. Major mode keys override global keys. Dired overwriting `n`

*and* `C-n`

to move to the next filename is one such example. That’s really neat and useful in dired, and obviously not applicable in most other places. Minor modes, as you can probably guess, add another layer. They override major mode key bindings.

So it’s worth remembering that in Emacs you have, as a package author, a lot more fine-grained control over what happens and where. For example, you can type `M-x view-mode`

to enable a special read-only minor mode that disables all text editing and rebinds a large number of common alphabetic keys that help with searching and reading. For example, `/`

searches forward instead of typing the character on your screen, but outside of `view-mode`

the `/`

key binding would instead get handed over to other minor modes, then the major mode, and then the global key map.

Observe that `M-x view-mode`

preserves your *major mode*. That is because a buffer can have exactly one major mode, but many minor modes (type `C-h m`

to describe all the active modes.) That is advantageous because it means you can engage `M-x view-mode`

in a code buffer if you’re reviewing code and preserve all the features of the code buffer’s major mode, such as syntax highlighting. You could even enable it in *dired*. That is another example of Emacs’s modality at work. Layer upon layer.

That is also how Viper and Evil are implemented in Emacs, in broad strokes, and they work by introducing their own minor modes that change the default key bindings in Emacs so they are more natural to a Vim user.

What does that mean for you? It means that you can, with grit and a little bit of perseverance, create your own key system in Emacs. Perhaps you’re a fan of the 1980s Borland BRIEF editor and want to recreate its key system in Emacs (but don’t, there are several packages that do this already.)

Maybe you want generic Emacs keys for most things, and a specialized mode for the select Vim commands you *do* want to keep. Or you just want to make up your own custom key binding scheme from scratch.

Emacs is really quite powerful and flexible like that.

### CAPS Lock as Control

Some people get what’s known as “Emacs pinky” from overreaching with their pinky to press the (usually awkwardly placed) control keys on boring, old standard keyboards. It’s definitely a thing, but in the way that tennis elbow is a thing: not every tennis player gets it, but some do. Still, you should be aware of it.

I recommend rebinding your caps lock key to control. Or, better still, invest in a fancy mechanical keyboard with thumb keys you can bind to control, alt, and shift. That is much better, ergonomically speaking, for your hands.

You don’t need caps lock. There are better ways of yelling at people nowadays.

## How Movement and Editing differs in Emacs and Vim

Emacs’s notion of text editing and movement is similar in some ways to Vims’ in that both editors are finely honed for text editing, and aimed squarely at people who want to go through the motions of mastering them to really appreciate all they can do.

How these two editors go about doing this is vastly different, however.

You’re generally expected (as you obviously know!) to move around in normal mode, but in Emacs the movement keys are available nearly everywhere. (The few places that disable movement key bindings only do so because there is a legitimately good reason to do so.)

Emacs’s keys strive to be somewhat mnemonic; with limitations, of course, as there are only 26 letters in the English alphabet and a handful of symbols.

As you can see in the table below, `f`

is for forward; `b`

for backward; `<`

to go to the beginning; `n`

for next line; and on and on.

Emacs Key Binding |
Vim Insert |
Description |
`C-b` |
`h` |
Move cursor left |
`C-n` |
`j` |
Move cursor down |
`C-p` |
`k` |
Move cursor up |
`C-f` |
`l` |
Move cursor right |
`C-d` |
`x` |
Kill/Delete next char |
`M-<` |
`gg` |
Move to the first line in the file |
`M->` |
`G` |
Move to the last line in the file |

*Not listed are the arrow keys and control keys like pg. up/down, which behave as you’d expect in Emacs.*

Most Vim users find Emacs’s base cursor movement cumbersome as they are not next to each other on a normal, Western QWERTY keyboard. That is usually not the problem it is made out to be, for although moving one character at a time is useful, it is also the most *inefficient* way of moving around in Emacs — they are precision movement keys, used to finesse your point to the right place, and should be treated as such.

Having said that, if you’re used to `hjkl`

, then it *is* a jarring and annoying experience having to unlearn that! This is a common source of friction for Vim users switching to Emacs, and I cannot fault them. Muscle memory is a powerful thing.

For common movement commands, Emacs instead ‘layers’ them so you can quickly switch between them by holding down different modifiers.

Emacs Key Binding |
Vim Insert Key |
Description |
`M-f` |
`w` |
Forward word |
`M-b` |
`b` |
Backward word |
`C-a` |
`0` |
Move to beginning of line |
`C-e` |
`$` |
Move to end of line |
`M-<` |
`gg` |
Move to start of file/buffer |
`M->` |
`G` |
Move to end of file/buffer |
`M-d` |
`dw` |
Kill/delete forward word |

Here the mnemonics remain the same in Emacs for elemental movement (`M-f`

vs `C-f`

) but changes the type of operation. There’s a handful of keys that behave like this, and they synergize with Emacs’s *kill ring* for killing text.

For example, to delete forward one word you can type `M-d`

, or `C-d`

to delete just the character. Moving forward by word is `M-f`

, so it’s easy to hold down `Meta`

(`Alt`

) and tap `fffd`

to move forward three words and then delete one word. You can also type `3fd`

to leverage Emacs’s *numeric prefix argument* to compel a command to repeat itself a certain number of times. In Emacs, most modifiers + a number engage the digit prefix argument, in this case `M-3`

prefixes the next command with `3`

.

As you can see, you only have to hold down one modifier key to execute three forwards and a delete. That’s pretty efficient, and up there with Vims’. Having said that, Emacs will never, in a straight contest, beat Vim at brevity, but it usually comes close.

However, compositing like you do in Vim with `d?`

(where `?`

is a follow-up key like `w`

for word) is not so easy to do in Emacs once you get beyond the basics.

You’re instead expected to type the key bindings in the order you wish to carry them out. In vim the notion of “delete inside parens” (`di(`

) is programmed into Vim; it’s just a whole thing to be able to do this, and similar things.

In Emacs, you’d type something akin to:

`C-M-u`

, to move up out of an*s-expression*, which may be a string or a pair of parentheses;`C-M-k`

, to kill the next*s-expression*;`(`

to type a pair of matching parentheses (or`"`

if it’s a string, etc.);

A different way of approaching the same problem, though it does take a little longer to type. Most Emacs hackers hold down the two modifiers and execute `uk`

in one stroke, so it’s not too cumbersome, despite the fact that it may look that way.

There’s an awful lot more to movement and editing in Emacs, and if you were at all worried about its text editing capabilities, then you shouldn’t. Most Emacs wizards move and edit at lightning speed, just like you do in Vim. I highly recommend [you check out my book on Emacs](https://www.masteringemacs.org/book) as it covers, in great detail, how to master Emacs’s movement and editing.

### Emacs outside Emacs

You may have recognized `C-a`

and `C-e`

, and perhaps `M-f`

and `M-b`

, if you use a shell like `bash`

. That is because by default GNU readline – which is the library `bash`

, `psql`

, `python`

, and so forth use for line editing in the terminal – has a large array of builtin Emacs key bindings and features inspired by those found in Emacs. Did you know you can record keyboard macros and play them back in bash, *and* persist them between sessions? I betcha didn’t.

What I find most fascinating is that most grizzled command line hackers – many of whom know Vi or Vim – know a few Emacs incantations, possibly even without know they’re Emacs keys. I’ve worked with people who knew about `C-a`

but not `C-e`

. So I find it useful to teach junior and seasoned hackers alike a key binding or two as it can seriously ramp up their productivity.

My article on [Keyboard Shortcuts every Command Line Hacker should know about GNU Readline](https://www.masteringemacs.org/article/keyboard-shortcuts-every-command-line-hacker-should-know-about-gnu-readline) has a lot more detail on GNU readline. Worth a read if you do a lot of command line-fu.

Serious Emacs users, of course, prefer to use Emacs itself as [the shell or terminal emulator](https://www.masteringemacs.org/article/running-shells-in-emacs-overview). That is another powerful reason to consider Emacs.

## Emacs’s Client-Server Architecture

A lot of Vim users jump into Vim, do some light hacking, wrap up their work, and exit Vim. It’s a common pattern for Vim users (but not all, of course), particularly sysadmins and devops types, who administer servers. In and out; quick and easy.

In Emacs, that’s not really how it’s done, even if you are a sysadmin prone to jittery Vim usage. You *can* do it, and Emacs accommodates it as well as Vim does, if that is what you want. But. There are better ways. Emacs has a client-server architecture, and you can tell it to start as a server and use `emacsclient`

as your `$EDITOR`

.

That avoids slow Emacs startup times, as most Emacs users are hoarders and tend to keep a large array of junk around in their personalized configuration that slows down their startup time. But that’s never a problem if you use the client-server architecture.

Now, having said that: vanilla Emacs unencumbered by junk starts in milliseconds just like Vim.

Speed is not the only reason to consider using the client-server system. By launching `emacsclient`

instances instead of `emacs`

, you re-use your existing, running Emacs session. `emacsclient`

will, by default, block and wait until you are finished editing the file you asked it to open. That means you can use `emacsclient`

for git commit messages (if you do not use the far superior [Magit, an Emacs mode for Git](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git)); editing crontabs or sudoers the file, which require that an editor block for the duration of the edit session so that it can verify the changes made are safe to apply; or indeed anything you like. You can also tell `emacsclient`

to open a file and return immediately, which is great if you’re rooting around for lots of things to edit out of turn.

So. That’s in Emacs the preferred method is to keep one instance running at all times, and feed it files via `emacsclient`

. But you do not have to do this if you do not want to.

`vi`

is usually installed on all Linux machines, so it makes sense that sysadmins have historically preferred `vi`

for quick config file edits on remote serves that may not have Emacs or another preferred tool installed.

Most Emacs users, however, use *tramp*, Transparent Remote Access Method Protocol, to connect to remote systems directly from inside Emacs. It supports a bewildering array of protocols, from Docker and SSH, to Android Debug Bridge. Using *tramp* you can edit remote files (inside a docker container, or via SSH and then into a docker container, or…) as though they were local files. I recommend you explore tramp as an alternative to ssh’ing to boxes. It is very powerful.

## Maybe you don’t need fzf…?

I know, I know. How profane to even suggest it. You’ll still use it, as it’s a nice piece of kit, and you no doubt have a workflow that leverages it well.

But, believe it or not, Emacs can filter much better than `fzf`

. Filtering, searching, completing, call it what you like, is a topic that Emacs users endlessly fawn over – witness the doorstop I wrote on [Understanding Minibuffer Completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion) to see what I mean – because it does it so well. So well, in fact, that I wrote a simple bash script + some a bit of Emacs glue code so you can use your *Emacs client* to do the [Fuzzy Finding with Emacs instead of fzf](https://www.masteringemacs.org/article/fuzzy-finding-emacs-instead-of-fzf). It works *really well*. Standard out is ducted into Emacs (instead of `fzf`

) and it does the filtering and returns the results you pick. Is it better? That’s for you to decide — but look at what you can do with a handful of lines of code.

## And you probably don’t need `tmux`

either…

Emacs can trivially replace every single major feature in your favorite terminal multiplexer, whether that is `tmux`

or the classic GNU `screen`

tool, including the terminal interaction and much more. Not convinced? Check out my article on [replacing tmux and GNU screen with Emacs](https://www.masteringemacs.org/article/replacing-tmux-gnu-screen-emacs).

## The Tinkerer’s Editor: Personalizing Emacs

If you don’t like how a thing works in Emacs, then you can simply change it. And I do mean that *you* can change it. It is not a fantasy nor out of reach of even beginner Emacs users to do this!

And if your problem is somewhat common, chances are someone’s already made a package or written a snippet of code to fix it. If not, and if you’re crafty, you can hack together some elisp to do it. Don’t forget to share it — others may have the same problem as you.

For a wide range of paper-cut-sized tasks – be it editing, moving or something else – give [keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) a try. They’re capable of recording and replaying nearly everything you are capable of doing. No elisp required. Oh, and you can save them and bind them to a key, so they can become part of your permanent Emacs workflow if you so desire.

That brings me to my next point. Emacs is for tinkerers. If you do not want to customize your Emacs, if you expect everything to work perfectly and smoothly, then… Emacs may disappoint you sometimes. Sorry.

You need to think of Emacs as an Austin-Healey (the vintage car, not the rugby player.) It needs regular maintenance. It may backfire occasionally. It uses leaded fuel (Lisp) and servicing is hands-on and requires work. You’re expected to get your hands dirty, and when it’s a sunny spring day and you want to take your editor out for a spin, it might not start because you YOLO’d a package upgrade the night before. That’s just how it is.

On the other hand, it’s been around for 40+ years and show no signs of slowing. Emacs is quite probably older than you are. It’s also free software. I find comfort in that. You should, too.

A beat-up, ramshackle Emacs configuration that is truly yours is the end goal. Mine is, oh, 23 years old? It also looks like a pigpen. Configuring Emacs is why many of us *use* it to begin with. It’s empowering to know that if I do not like the ergonomics of a feature in Emacs that I can change it. Sure, most software lets you rebind their keys here and there. Right up until you want to do it in the “Search and Replace” dialog box in that one piece of dilapidated software you’re forced to use. But Emacs really, truly, is modifiable and malleable, and not just in some high-minded theoretical sense of the word. I mean, you’re contemplating whether to use a completely orthogonal editing system native to another text editor!

So that’s why Emacs’s gravitational pull is so strong. That is why people manage their lives with org mode; [build complex code navigation and editing tools](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter); write emails (and combine it with org mode); [run shells and terminal emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview); [play games](https://www.masteringemacs.org/article/fun-games-in-emacs) and so much more.

But maybe save it for tomorrow? You can skip a lot of the front-loaded work of customizing your Emacs by using someone else’s work. My [tutorial](https://www.masteringemacs.org/article/beginners-guide-to-emacs) mentions a few starter packs you can try if you want something to help you get started, though.

## Conclusion

Emacs is not Vim, and nor is Vim the same as Emacs. But they have a lot more in common than you may think. Emacs and Vim both assume you’re willing to put in the work to master them. I do not have to tell you how fast and efficient a skilled Vim user is. You’ll find it is the same when you have mastered Emacs. Both editors feature powerful editing, but they do work quite differently. Both have extensive plugin ecosystems (especially Neovim), and both editors come with trade-offs. The choice is yours. And you can always flip between them if you like.

Welcome aboard :)
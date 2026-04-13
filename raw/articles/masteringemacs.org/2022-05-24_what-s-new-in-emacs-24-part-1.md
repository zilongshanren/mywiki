---
title: What's New In Emacs 24 (part 1)
url: https://www.masteringemacs.org/article/what-is-new-in-emacs-24-part-1
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

With Emacs 24 looming around the corner I figured it was time I took a close look at all the new features and changes. As it’s not *officially* out yet I will settle for the pretest build (get it [here](http://alpha.gnu.org/gnu/emacs/pretest/).) With that said, there’s little difference (in my experience anyway) between the pretest versions of Emacs and the real mccoy. They’re usually rock-solid and won’t crash on you, but the featureset is, of course, still subject to change.

I’ve annotated most changes and given my view of how useful each change is to most people. Obviously I do not speak for all of us, so don’t neglect to read the NEWS file in its entirety yourself (`C-h n`

.)

## Installation Changes in Emacs 24.1

** By default, the installed Info and man pages are compressed.

You can disable this by configuring –without-compress-info.


Useful configure flag for people who value time over space; of course, most of us use a package manager and thus we have no say in how our software is built.

Emacs can be compiled with ImageMagick support.

Emacs links to ImageMagick if version 6.2.8 or newer of the library is

present at build time. To inhibit ImageMagick, use the configure

option `–without-imagemagick’ .


Neat. Imagemagick is a set of tools for manipulating, viewing and converting images and other media files like PDF and PS. With any luck we might get “native” PDF/PS support in Emacs. DocView (the Emacs document viewer) converts each PDF/PS page to PNG and displays *that* on your screen. Hardly ideal.

## Startup Changes in Emacs 24.1

On Windows, Emacs now warns when the obsolete _emacs init file is used,

and also when HOME is set to C:\ by default.


Warning when the HOME directory is unset (or set to `C:\`

)

will aid new Emacs users greatly as it is a rather obscure requirement

that you have to set the `HOME`

environment variable to

control where Emacs will read the init.el or .emacs file from.

## Changes in Emacs 24.1

auto-mode-case-fold is now enabled by default.


The `auto-mode-alist`

variable is an association list (hence the `-alist`

bit) of key-value pairs that define what major mode Emacs should set when you open a certain file type. By setting the case fold flag to `t`

Emacs will search the list twice: first time around it will use case *sensitive* matching and, if no matches were found, it will try again but with *insensitive* matching. This switch has no effect on Windows.

### Completion

shell-mode uses pcomplete rules, with the standard completion UI.


Yowzah! There’s a lot of cool, new functionality hidden away in this gem of a change. The author of pcomplete is *John Wiegley* – the same guy who wrote [EShell](https://www.masteringemacs.org/articles/2010/12/13/complete-guide-mastering-eshell/) – and in Eshell you can complete commandline arguments for things like `kill`

, `rmdir`

, etc. in the same way `zsh`

(or newer versions of `bash`

) does it: by writing your own “programmable” (that’s the *p* in pcomplete) completion engines for individual commands. Nifty. Of course, this concept is not limited to just shells. You could write completion libraries for programing modes and what have you as well.

This feature is a Big Deal to people (like me) who use `M-x shell`

*all the time* for day-to-day work. If you’re using Emacs 24 right now try this on for size (Linux, et al only): `chgrp TAB`

and you should see a completion window appear listing all the various groups on your system. Cool! Type `M-x apropos pcomplete/`

to see a list of all the completion engines available.

I’m definitely going to cover this in greater detail later.

Many packages have been changed to use `completion-at-point’

rather than their own completion code.


Another lovely change made in the name of standardization. The command `completion-at-point`

is a generic command that, by fiddling with the variable `completion-at-point-functions`

, you can control how Emacs does completion in a particular buffer. Lots of modes and packages have their own little completion engines, thus diminishing the value of having such a generic facility in place.

`completion-at-point’ now handles tags and semantic completion.


CEDET’s Semantic library is now usable from the Emacs completion framework. The easiest way to test it is to open up a C source code file and typing `M-TAB`

or `C-M-i`

and watch as Semantic automagically completes for you. For languages where semantic is not enabled by default, you can add it the following line to your major mode hook of choice:

```
(add-to-list 'completion-at-point-functions 'semantic-completion-at-point-function)
Completion in a non-minibuffer now tries to detect the end of completion
and pops down the \*Completions\* buffer accordingly.
```


This behaviour has always been a major source of frustration for me and, I’m sure, others as well. Historically Emacs would leave completion windows hanging around well after you were done using them; not so any more. Emacs will try to hide them automatically “when you’re done with them.” This works really well for me in `M-x shell`

as I’m always TAB-completing paths and filenames.

Completion can cycle, depending on completion-cycle-threshold.


Another productivity enhancer! If you set `completion-cycle-threshold`

to `t`

then Emacs will always cycle through the completion choices if there is more than one left. And because this feature affects `completion-at-point`

it should work in most modes. Set it to an integer and it will only cycle if there are fewer than N items. Set it to nil (the default) and it is disabled entirely.

I like this feature, so I have set it to cycle if there are fewer than 5 items:

```
(setq completion-cycle-threshold 5)
New completion style \`substring’.
```


The new `substring`

style gives you “wildcard”-style partial completion where Emacs will cast as wide a net as it can to complete your text.

Historically, Emacs has gone through quite a few completion “styles”; that is, different ways in which Emacs tries to complete your query when you press (usally) TAB. There’s a host of them, and you can (surprise!) add your own as well if you really want to. The association list `completion-styles-alist`

lists all the current styles and the variable `completion-styles`

contains an ordered list of styles to cycle through. To use the new `substring`

style you can add it to the completion styles list. Keep in mind that some modes will override the defaults. See the next item.

```
(add-to-list 'completion-styles 'substring)
Completion style can be set per-category \`completion-category-overrides’.
```


As I mentioned in the above entry you can tell Emacs to only use certain styles in certain parts of Emacs.

Completion of buffers now uses substring completion by default.


This is no doubt a welcome change to the, oh, five or so people out there who choose not to use iswitchb or [IDO Mode](https://www.masteringemacs.org/articles/2010/10/10/introduction-to-ido-mode/). Sarcasm aside, this is useful if you screw up your init file and you need to switch to the `*Messages*`

buffer.

### Mail changes

default of `send-mail-function’ is now `sendmail-query-once’,

which asks the user (once) whether to use the smtpmail package to send

email, or to use the old defaults that rely on external mail

facilities (`sendmail-send-it’ on GNU/Linux and other Unix-like

systems, and `mailclient-send-it’ on Windows).


The first time you use `C-x m`

(`compose-mail`

) and try to send an e-mail Emacs will now ask you how it should send the e-mail. Simple stuff, really.

#### smtpmail changes

smtpmail now uses encrypted connections (via STARTTLS) if the

mail server supports them. It also uses the auth-source framework for

getting credentials.


Good news for people who can’t use unencrypted mail servers.

The variable `smtpmail-auth-credentials’ has been removed.

That variable used to have the default value “~/.authinfo”, in which

case you won’t see any difference. But if you changed it to be a list

of user names and passwords, that setting is now ignored; you will be

prompted for the user name and the password, which will then be saved

to ~/.authinfo.

You can also manually copy the credentials to your ~/.authinfo file.

For example, if you had

(setq smtpmail-auth-credentials

’((“mail.example.org” 25 “jim” “s!cret”)))

then the equivalent line in ~/.authinfo would be

machine mail.example.org port 25 login jim password s!cret

The variable `smtpmail-starttls-credentials’ has been removed.

If you had that set, then you need to put

machine smtp.whatever.foo port 25 key “~/.my_smtp_tls.key” cert “~/.my_smtp_tls.cert”

in your ~/.authinfo file instead.


Useful knowledge if you’re composing mail in Emacs.

### sendmail changes

can now add MIME attachments to outgoing messages with the new

command `mail-add-attachment’.

command `mail-attach-file’ was renamed to `mail-insert-file’; the

old name is now an obsolete alias to the new name.


### Emacs server and client changes

New option `server-port’ specifies the port on which the Emacs

server should listen.

New emacsclient argument -q/–quiet suppresses some status messages.

New emacsclient argument –frame-parameters can be used to set the

frame parameters of a newly-created graphical frame.

If emacsclient shuts down as a result of Emacs signaling an

error, its exit status is 1.

New emacsclient argument –parent-id ID.

This opens a client frame in parent X window ID, via XEmbed, similar

to the –parent-id argument to Emacs.


More changes to Emacs’s Client-Server architecture. The port command change is probably the most interesting bit.

### Internationalization changes

Emacs now supports display and editing of bidirectional text.

Text that includes characters from right-to-left (RTL) scripts, such

as Arabic, Farsi, or Hebrew, is displayed in the correct visual order

as expected by users of those scripts. This display reordering is a

“Full bidirectionality” class implementation of the Unicode

Bidirectional Algorithm. Buffers with no RTL text should look exactly

the same as before.

For more information, see the node “Bidirectional Editing” in the

Emacs Manual.

New buffer-local variable `bidi-display-reordering’.

To disable display reordering in any given buffer, change this to nil.

New buffer-local variable `bidi-paragraph-direction’.

If nil (the default), Emacs determines the base direction of each

paragraph from its text, as specified by the Unicode Bidirectional

Algorithm.

Setting this to `right-to-left’ or `left-to-right’ forces a particular

base direction on each paragraph in the buffer.

Paragraphs whose base direction is right-to-left are displayed

starting at the right margin of the window.

Enhanced support for characters with no glyphs in available fonts.

If a character has no glyphs in any of the available fonts, Emacs

normally displays it either as a hexadecimal code in a box or as a

thin 1-pixel space. In addition to these two methods, Emacs can

display these characters as empty box, as an acronym, or not display

them at all. To change how these characters are displayed, customize

the variable `glyphless-char-display-control’.

On character terminals, these methods are used for characters that

cannot be encoded by the `terminal-coding-system’.

New input methods for Farsi: farsi and farsi-translit.


Right-to-Left support in Emacs has been a long time coming and a difficult and complex change to Emacs’s display engine. If you’re a RTL user I’d love to hear how functional and useful it actually is.

`nobreak-char-display’ now also highlights Unicode hyphen chars

(U+2010 and U+2011).


If `nobreak-char-display`

is `t`

Emacs will highlight facsimile unicode whitespace and hyphen characters so you can tell them apart from their ASCII counterpart.

### Improved GTK integration

GTK scroll-bars are now placed on the right by default.

Use `set-scroll-bar-mode’ to change this.

GTK tool bars can have just text, just images or images and text.

Customize `tool-bar-style’ to choose style. On a Gnome desktop, the default

is taken from the desktop settings.

GTK tool bars can be placed on the left/right or top/bottom of the frame.

The frame-parameter tool-bar-position controls this. It takes the values

top, left, right or bottom. The Options => Show/Hide menu has entries

for this.

The colors for selected text (the `region’ face) are taken from

the GTK theme when Emacs is built with GTK.

Emacs uses GTK tooltips by default if built with GTK. You can turn that

off by customizing x-gtk-use-system-tooltips.


A slew of GTK changes for people who use Emacs compiled with GTK.

New basic faces `error’, `warning’, `success’ are available to

highlight strings that indicate failure, caution or successful operation.


Good news for customize fans. No longer will you have to hunt down fifty different faces that do the same thing. Simply invoke `M-x customize-face RET facename`

, where facename is one of the aforementioned three, and change the face there. The changes you make at the root faces will now properly propagate to all faces that inherit from them.

Lucid menus and dialogs can display antialiased fonts if Emacs is built

with Xft. To change font, use the X resource font, for example:

Emacs.pane.menubar.font: Courier-12

On graphical displays, the mode-line no longer ends in dashes.

Also, the first dash (which does not indicate anything) is just

displayed as a space.


Truly the end of an era.

Basic SELinux support has been added.

This requires Emacs to be linked with libselinux at build time.

Emacs preserves the SELinux file context when backing up, and

optionally when copying files. To this end, copy-file has an extra

optional argument, and backup-buffer and friends include the SELinux

context in their return values.

The new functions file-selinux-context and set-file-selinux-context

get and set the SELinux context of a file.

Tramp offers handlers for file-selinux-context and set-file-selinux-context

for remote machines which support SELinux.


Good news for hardcore SELinux hackers.

### Changes for exiting Emacs

The function kill-emacs is now run upon receipt of the signals

SIGTERM and SIGHUP, and upon SIGINT in batch mode.


A nice change, for sure. However this will not trigger the usual “Do you wish to save your buffer” query as that is done at a higher level in Emacs. So don’t think this’ll save your skin if you nuke Emacs from the commandline!

kill-emacs-hook is now also run in batch mode.

If you have code that adds something to kill-emacs-hook, you should

consider if it is still appropriate to add it in the noninteractive case.


My kill-emacs-hook is mostly filled with miscellaneous gunk like saving my recentf and bookmarks.

### Scrolling changes

New scrolling commands `scroll-up-command’ and `scroll-down-command’

(bound to C-v/[next] and M-v/[prior]) do not signal errors at top/bottom

of buffer at first key-press (instead move to top/bottom of buffer)

when `scroll-error-top-bottom’ is non-nil.

New variable `scroll-error-top-bottom’ (see above).


About time! This is useful if you make macros and you don’t want Emacs to cancel out of your macro recorder (or indeed in the macro itself) if it reaches the end of the buffer. I foresee lots of custom macro recorder functions that disable the top/bottom error signal when you’re recording…

New scrolling commands `scroll-up-line’ and `scroll-down-line’

scroll a line instead of full screen.


Pretty self-explanatory!

New property `scroll-command’ should be set on a command’s symbol to

define it as a scroll command affected by `scroll-preserve-screen-position’.


This is an elisp change that only really concerns people who write elisp packages. Basically, it means you can with greater granularity control if a particular movement command is affected by the user-defined setting in `scroll-preserve-screen-position`

; itself a command that let’s you control how Emacs scrolls on your screen.

If you customize `scroll-conservatively’ to a value greater than 100,

Emacs will never recenter point in the window when it scrolls due to

cursor motion commands or commands that move point (e.f., `M-g M-g’).

Previously, you needed to use `most-positive-fixnum’ as the value of

`scroll-conservatively’ to achieve the same effect.


Interesting change, but not something I find all that useful. I rather prefer knowing where a line (or what have you) I want to see is in roughly the same spot every time.

``Aggressive’’ scrolling now honors the scroll margins.

If you customize `scroll-up-aggressively’ or

`scroll-down-aggressively’ and move point off the window, Emacs now

scrolls the window so as to avoid positioning point inside the scroll

margin.

This is another one of those changes that people with rather interesting views on how Emacs should scroll care about. I personally just use the defaults so I don’t have too much to say about it.

## To Be Continued…

I think I’m going to end my post here. Emacs has hundreds of new features and changes and – according to my modeline – I have only covered about 30% of the NEWS file.
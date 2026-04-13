---
title: What's New in Emacs 24.3
url: https://www.masteringemacs.org/article/whats-new-emacs-24-3
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Emacs version 24.3 is now released to the public. This release, unlike 24.2, is chock full of goodies. I’ve taken the liberty of annotating things that’re relevant to me – and hopefully you, too, dear reader – but I’ve limited my commentary to things I’m familiar with. Always keen to hear what you think about the changes in the comments.

You can retrieve Emacs 24.3 from one of these locations:

**Automatic mirror**

*Note: As of 11 AM on 2013-03-11 I had issues with some mirrors not yet having the new version available.*

[http://ftpmirror.gnu.org/emacs/emacs-24.3.tar.xz](http://ftpmirror.gnu.org/emacs/emacs-24.3.tar.xz)

[http://ftpmirror.gnu.org/emacs/emacs-24.3.tar.gz](http://ftpmirror.gnu.org/emacs/emacs-24.3.tar.gz)

## What’s New in Emacs 24.3

### Installation Changes in Emacs 24.3

The default X toolkit is now Gtk+ version 3.

If you don’t pass

`--with-x-toolkit`

to configure, or if you use

`--with-x-toolkit=gtk`

or`--with-x-toolkit=yes`

, configure will tryto build with Gtk+ version 3, and if that fails, try Gtk+ version 2.

You can explicitly require a specific version by passing


`--with-x-toolkit=gtk2`

or`--with-x-toolkit=gtk3`

to configure.

Although I always use Emacs in a window manager, and actively recommend that people who can do as well, this change is unlikely to affect me much at all. I don’t use scrollbars, toolbars or menubars.

New configure option

`--enable-link-time-optimization`

, to utilizean appropriate feature provided by GCC since version 4.5.0.


|

New configure option

`--without-all`

to disable most of the optionalfeatures (image support, etc.) that are normally enabled by default.


For the luddites.

New configure option

`--enable-gcc-warnings`

(for developing/debuggingEmacs). If building with GCC, this enables compile-time checks that

warn/give errors about possibly-questionable C code. On a recent GNU

system there should be no warnings; on older and on non-GNU systems

the results may be useful to developers.

The configure option

`--enable-use-lisp-union-type`

has beenrenamed to

`--enable-check-lisp-object-type`

, as the resultingLisp_Object type no longer uses a union to implement the compile time

check that this option enables.

The configure option

`--disable-maintainer-mode`

has been removed,as it was confusingly-named and rarely useful.

The configure options

`--program-prefix`

,`--program-suffix`

, and

`--program-transform-name`

apply to more than just the installedbinaries. Now they also affect the man pages, icons, and the

etc/emacs.desktop file; but not the info pages, since this would break

links between the various manuals.

You can use

`NO_BIN_LINK=t make install`

to prevent the installationoverwriting “emacs” in the installation bin/ directory with a link

to “emacs-VERSION”.

Emacs uses libtinfo in preference to libncurses, if available.

On FreeBSD and NetBSD, configure no longer adds /usr/local/lib and

/usr/pkg/lib to the linker search path. You must add them yourself if

you want them.

The standalone scripts

`rcs-checkin`

and`vcdiff`

have been removed(from the bin and libexec directories, respectively). The former is

no longer relevant, the latter is replaced by lisp (in vc-sccs.el).


### Startup Changes in Emacs 24.3

Emacs no longer searches for

`leim-list.el`

files beneath the standardlisp/ directory. There should not be any there anyway. If you have

been adding them there, put them somewhere else; e.g., site-lisp.

The

`--no-site-lisp`

command line option now works for Nextstep builds.

### Changes in Emacs 24.3

#### Help


`C-h f`

(`describe-function`

) can now perform autoloading.When this command is called for an autoloaded function whose docstring

contains a key substitution construct, that function’s library is

automatically loaded, so that the documentation can be shown

correctly. To disable this, set

`help-enable-auto-load`

to nil.

That’s a potentially useful change, though I cannot offhand recall any instances where I’ve been bitten by this. This is not going to guard against unloaded libraries if you are *not* looking up autoloaded commands. In other words, if you’re looking up an obscure function or variable and the library isn’t loaded, this won’t help at all.


`C-h f`

now reports previously-autoloaded functions as “autoloaded”,even after their associated libraries have been loaded (and the

autoloads have been redefined as functions).


I would fill this under “Nice to know”.

#### ImageMagick

Images displayed via ImageMagick now support transparency and the

:background image specification property.

When available, ImageMagick support is automatically enabled.

It is no longer necessary to call

`imagemagick-register-types`

explicitly to install ImageMagick image types; that function is called

automatically at startup, or when customizing an imagemagick- option.


Most excellent. This should help encourage the use of Imagemagick now that it’s loaded by default.

Setting

`imagemagick-types-inhibit`

to t now disables the use ofImageMagick to view images. (You must call

`imagemagick-register-types`

afterwards if you do not use customize to change this.)


… And this is how you disable it

The new variable

`imagemagick-enabled-types`

also affects whichImageMagick types are treated as images. The function


`imagemagick-filter-types`

returns the list of types that will betreated as images.


#### Minibuffer

In minibuffer filename prompts,

`C-M-f`

and`C-M-b`

now move to thenext and previous path separator, respectively.


With the caveat, I suppose, that this is not likely to work if you use iswitchb or IDO.


`minibuffer-electric-default-mode`

can shorten “(default …)” to “[…]”in minibuffer prompts. Just set

`minibuffer-eldef-shorten-default`

non-nil before enabling the mode.


#### Mode line

New option

`mode-line-default-help-echo`

specifies the help text(shown in a tooltip or in the echo area) for any part of the mode line

that does not have its own specialized help text.

You can now click mouse-3 in the coding system indicator to invoke


`set-buffer-file-coding-system`

.

#### Server and client

emacsclient now obeys string values for

`initial-buffer-choice`

,if it is told to open a new frame without specifying any file to visit

or expression to evaluate.

New option

`server-auth-key`

specifies a shared server key.Emacs now generates backtraces on fatal errors.

On encountering a fatal error, Emacs now outputs a textual description

of the fatal signal, and a short backtrace on platforms like glibc

that support backtraces.


#### Other


`C-x C-q`

is now bound to the new minor mode`read-only-mode`

.This minor mode replaces

`toggle-read-only`

, which is now obsolete.

Interesting that they’ve moved it to a new minor mode. I imagine this change was effected to reduce the number of “magic states” a buffer could be in. As a mode, it also means you can customize it further like, say, adding hooks so you can gray out the text if it’s read only.

Most

`y-or-n`

prompts now allow you to scroll the selected window.Typing

`C-v`

or`M-v`

at a y-or-n prompt scrolls forward or backwardrespectively, without exiting from the prompt.


Very nice and welcome change.

In the Package Menu, newly-available packages are listed as “new”,

and sorted above the other “available” packages by default.

If your Emacs was built from a bzr checkout, the new variable


`emacs-bzr-version`

contains information about the bzr revision used.New option

`create-lockfiles`

specifies usage of lockfiles.It defaults to t. Changing it to nil inhibits the creation of lock

files (use this with caution).

New option

`enable-remote-dir-locals`

, if non-nil, allows directory-localvariables on remote hosts.


This is useful if you use dir-local variables remotely, but there’s an obvious security risk if you enable it.

The entry for PCL-CVS has been removed from the Tools menu.

The PCL-CVS commands are still available via the keyboard.

Using “unibyte: t” in Lisp source files is obsolete.

Use “coding: raw-text” instead.

In the buffer made by

`M-x report-emacs-bug`

, the`C-c m`

bindinghas been changed to

`C-c M-i`

(`report-emacs-bug-insert-to-mailer`

).The previous binding, introduced in Emacs 24.1, was a mistake, because


`C-c LETTER`

bindings are reserved for user customizations.

#### Internationalization

New language environment: Persian.

New input method

`vietnamese-vni`

.

#### Nextstep (GNUstep / Mac OS X) port

Support for fullscreen and the frame parameter fullscreen.


A much longed-for feature.

A file dialog is used for open/save operations initiated from the

menu/toolbar.


### Editing Changes in Emacs 24.3

#### Search and Replace

Non-regexp Isearch now performs “lax” space matching.

Each sequence of spaces in the supplied search string may match any

sequence of one or more whitespace characters, as specified by the

variable

`search-whitespace-regexp`

. (This variable is also used by asimilar existing feature for regexp Isearch.)


This is great as you can now find matches even though whitespacing may not be spot on.

New Isearch command

`M-s SPC`

toggles lax space matching.This applies to both ordinary and regexp Isearch.


Handy if you don’t want fuzzy space matching.

New option

`replace-lax-whitespace`

.If non-nil,

`query-replace`

uses flexible whitespace matching too.The default is nil.

Global

`M-s _`

starts a symbol (identifier) incremental search,and

`M-s _`

in Isearch toggles symbol search mode.

`M-s c`

in Isearch toggles search case-sensitivity.

Very useful if you’re coding. It’s equivalent to wrapping an `isearch-forward-regexp`

regexp query in `\_<`

and `\_>`

. Keep in mind that the definition of a symbol varies according to your major mode (and sometimes minor!). It’s usually set to rather sensible defaults in most programming major modes.

### Navigation commands

New binding

`M-g c`

for`goto-char`

.

The word “char” here is rather misleading: it means the absolute position, as an integer, from the beginning of the buffer.

New binding

`M-g TAB`

for`move-to-column`

.

`M-g TAB`

(`move-to-column`

) prompts for a column number if calledinteractively with no prefix arg. Previously, it moved to column 1.

New option

`yank-handled-properties`

allows processing of textproperties on yanked text, in ways that are more general than just

removing them (as is done by

`yank-excluded-properties`

).

Useful if you want to strip out or alter properties on text when it’s yanked. This is unlikely to be of interest to anybody except module developers.

New option

`delete-trailing-lines`

specifies whetherM-x delete-trailing-whitespace should delete trailing lines at the end

of the buffer. It defaults to t.


A nice and useful addition, but be wary as it defaults to true.


`C-u M-=`

now counts lines/words/characters in the entire buffer.

`C-x 8 RET`

is now bound to`insert-char`

, which is now a command.

`ucs-insert`

is now an obsolete alias for`insert-char`

.The

`z`

key no longer has a binding in most special modes.It used to be bound to

`kill-this-buffer`

, but`z`

is too easy toaccidentally type.


Rejoice all who have accidentally killed your buffers.

New command

`C-x r M-w`

(`copy-rectangle-as-kill`

).It copies the region-rectangle as the last rectangle kill.


Very nice. This basically makes works exactly like `M-w`

does except it operates on a rect. No more killing then yanking if you want to copy a rect.

### Registers


`C-x r +`

is now overloaded to invoke`append-to-register`

.

This small change has rather wide ramifications for those of you who use registers in macros. You can now collect text and append it to the end of a register instead of shunting it to a different buffer. Groundbreaking? Not quite, but very useful indeed.

New option

`register-separator`

specifies the register containingthe text to put between collected texts for use with

M-x append-to-register and M-x prepend-to-register.


Combined with the above, this enables you to collate appended texts with a separator symbol.

### Changes in Specialized Modes and Packages in Emacs 24.3

#### Common Lisp emulation (CL)

CL’s main entry is now (require ’cl-lib).


`cl-lib`

is like the old`cl`

except that it uses the namespace cleanly;i.e., all its definitions have the “cl-” prefix (and internal definitions

use the “cl–” prefix).

If

`cl`

provided a feature under the name`foo`

, then`cl-lib`

provides it under the name

`cl-foo`

instead; with the exceptions of thefew

`cl`

definitions that had to use`foo*`

to avoid conflicts withpre-existing Elisp entities. These have been renamed to

`cl-foo`

rather than

`cl-foo*`

.The old

`cl`

is now deprecated and is mainly just a bunch of aliases thatprovide the old, non-prefixed names. Some exceptions are listed below:


This is a good change but I doubt we will ever truly be rid of `cl`

, not for a long tie anyway.


`cl-flet`

is not like`flet`

(which is deprecated).Instead it obeys the behavior of Common-Lisp’s

`flet`

.In particular, in cl-flet function definitions are lexically scoped,

whereas in flet the scoping is dynamic.


`cl-labels`

is slightly different from`labels`

.The difference is that it relies on the

`lexical-binding`

machinery(as opposed to the

`lexical-let`

machinery used previously) to capturedefinitions in closures, so such closures will only work if

`lexical-binding`

is in use.


`cl-letf`

is not exactly like`letf`

.The only difference is in details that relate to some deprecated usage

of

`symbol-function`

in place forms.

`progv`

was rewritten to use the`let`

machinery.A side effect is that variables without corresponding values are bound

to nil rather than being made unbound.

The following methods of extending

`setf`

are obsolete(use features from gv.el instead):


`define-modify-macro`

(use`gv-letplace`

)

`defsetf`

(use`gv-define-simple-setter`

or`gv-define-setter`

)

`define-setf-expander`

(use`gv-define-setter`

or`gv-define-expander`

)

`get-setf-method`

no longer exists (see “Incompatible Lisp Changes”)

### Diff mode

Changes are now highlighted using the same color scheme as in

modern VCSes. Deletions are displayed in red (new faces


`diff-refine-removed`

and`smerge-refined-removed`

, and new definitionof

`diff-removed`

), insertions in green (new faces`diff-refine-added`

and

`smerge-refined-added`

, and new definition of`diff-added`

).

More standardization. Good.

The variable

`diff-use-changed-face`

defines whether to use theface

`diff-changed`

, or`diff-removed`

and`diff-added`

to highlightchanges in context diffs.

The new command

`diff-delete-trailing-whitespace`

removes trailingwhitespace introduced by a diff.

Ediff now uses the same color scheme as Diff mode.


### Python mode

A new version of python.el, which provides several new features, including:

per-buffer shells, better indentation, Python 3 support, and improved

shell-interaction compatible with iPython (and virtually any other

text based shell).


I blogged about a new python mode a long time ago and it seems it’s made it into trunk. That’s probably good news for most Python users, but as I haven’t yet explored the new python.el mode yet, I will cover this in much greater detail in another post.

Some user options have been replaced/renamed, including (old -> new):

python-indent -> python-indent-offset

python-guess-indent -> python-indent-guess-indent-offset

python-pdbtrack-do-tracking-p -> python-pdbtrack-activate

python-use-skeletons -> python-skeleton-autoinsert

Some user options have been removed, including:


`python-indent-string-contents`

: Strings are never indented.

`python-honour-comment-indentation`

:Comments are always considered as indentation markers.


`python-continuation-offset`

: Indentation is automaticallycalculated in a pep8 compliant way depending on the context.


`python-shell-prompt-alist`

,`python-shell-continuation-prompt-alist`

:Have no direct mapping as the shell interaction is completely different.


`python-python-command`

,`python-jython-command`

:Replaced by

`python-shell-interpreter`

.

`inferior-python-filter-regexp`

,`python-remove-cwd-from-path`

,

`python-pdbtrack-minor-mode-string`

,`python-source-modes`

:No longer relevant.

Some commands have been replaced (old -> new):

python-insert-class -> python-skeleton-class

python-insert-def -> python-skeleton-def

python-insert-for -> python-skeleton-for

python-insert-if -> python-skeleton-if

python-insert-try/except -> python-skeleton-try

python-insert-try/finally -> python-skeleton-try

python-insert-while -> python-skeleton-while

python-find-function -> python-nav-jump-to-defun

python-next-statement -> python-nav-forward-sentence

python-previous-statement -> python-nav-backward-sentence

python-beginning-of-defun-function -> python-nav-beginning-of-defun

python-end-of-defun-function -> python-nav-end-of-defun

python-send-buffer -> python-shell-send-buffer

python-send-defun -> python-shell-send-defun

python-send-region -> python-shell-send-region

python-send-region-and-go -> emulate with python-shell-send-region

and python-shell-switch-to-shell

python-send-string -> python-shell-send-string

python-switch-to-python -> python-shell-switch-to-shell

python-describe-symbol -> python-eldoc-at-point


Needless to say, the changes here are likely to break a lot of my custom Python code I’ve written over the years. If you’re relying on customizations to Python or modes that interact with it, I would probably ensure you can fix or live with broken modules until they’re fixed.

### D-Bus

New variables

`dbus-compiled-version`

and`dbus-runtime-version`

.The D-Bus object manager interface is implemented.

Variables of type :(u)int32 and :(u)int64 accept floating points,

if their value does not fit into Emacs’s integer range.

The function

`dbus-call-method`

is now non-blocking.It can be interrupted by

`C-g`

.`dbus-call-method-non-blocking`

is obsolete.Signals can also be sent as unicast messages.

The argument list of

`dbus-register-signal`

has been extended,according to the new match rule types of D-Bus.


`dbus-init-bus`

supports private connections.There is a new function

`dbus-setenv`

.

`desktop-path`

no longer includes the “.” directory.Desktop files are now located in ~/.emacs.d by default.


### Dired


`dired-do-async-shell-command`

executes each file sequentiallyif the command ends in

`;`

(when operating on multiple files).Otherwise, it executes the command on each file in parallel.


Very useful and good for people working with commands on many files.

Typing

`M-n`

in the minibuffer of`dired-do-chmod`

,`dired-do-chgrp`

,

`dired-do-chown`

, and`dired-do-touch`

yanks the attributes of thefile at point.


Hah! This is superb. I really like this change. Now you’re probably thinking the command, `M-n`

, is arbitrary, but not so: in minibuffer prompts that command would go to the last used element in the minibuffer history; by re-using that command here, it achieves the same effect.

When the region is active,

`m`

(`dired-mark`

),`u`

(`dired-unmark`

),

`DEL`

(`dired-unmark-backward`

), and`d`

(`dired-flag-file-deletion`

)mark/unmark/flag all files in the active region.


Can i hear a hallelujah? this is a most welcome change and one that should’ve been in dired since day one.

The minibuffer default for

`=`

(`dired-diff`

) has changed.it is now the backup file for the file at point, if one exists.

in transient mark mode the default is the file at the active mark.


great idea but for most serious files you’re probably using `c-x v =`

, the vcs diff command.


`M-=`

is no longer bound to`dired-backup-diff`

in Dired buffers.The global binding for

`M-=`

,`count-words-region`

is in effect.

### ERC

New module “notifications”, which can send a notification when you

receive a private message or your nickname is mentioned.

ERC will look up server/channel names via auth-source and use any

channel keys found.

New option

`erc-lurker-hide-list`

, similar to`erc-hide-list`

, butonly applies to messages sent by lurkers.


### reStructuredText mode

Keybindings (see

`C-c C-h`

), TAB indentation, filling and auto-filling,fontification, comment handling, and customization have all been revised

and improved.


That’s good. rST mode always did seem a bit… underdeveloped.

Support for

`imenu`

and`which-function-mode`

.

Great!

The reStructuredText syntax is more closely covered.

Sphinx support has been improved.


Sphinx support is very good news for Python docs writers and other fans of Sphinx.


`rst-insert-list`

inserts new list or continues existing lists.A negative prefix argument always works for

`rst-adjust`

.The window configuration is reset after displaying a TOC.

The constant

`rst-version`

describes the rst.el package version.

### Ruby mode

Support for percent literals and recognition of regular expressions

in method calls without parentheses with more methods, including Cucumber

steps definitions.

Improved syntax highlighting and indentation.

New command

`ruby-toggle-block`

, bound to`C-c {`

.Some non-standard keybindings/commands have been removed:


`ruby-electric-brace`

; use`electric-indent-mode`

instead.

`ruby-mark-defun`

; use`mark-defun`

.

`ruby-beginning-of-defun`

and`ruby-end-of-defun`

are replaced byappropriate settings for the variables

`beginning-of-defun-function`

and

`end-of-defun-function`

.

These three changes are all part of a larger drive in Emacs to remove major mode-specific functions that’re better served with the built-in Emacs equivalents.

Non-standard keybindings for

`backward-kill-word`

,`comment-region`

,

`reindent-then-newline-and-indent`

and`newline`

have been removed.

### Shell Script mode

Pairing of parens/quotes uses

`electric-pair-mode`

instead of skeleton-pair.

More duplicate cruft removed and standardized.


`sh-electric-here-document-mode`

now controls auto-insertion of here-docs.

`sh-use-smie`

lets you choose a new indentation and navigation code.

### VHDL mode

The free software compiler GHDL is supported (and now the default).

Support for the VHDL-AMS packages has been added/updated.

Updated to the 2002 revision of the VHDL standard.

Accepts \r and \f as whitespace.


### Apropos

The faces used by Apropos are now directly customizable.

These faces are named

`apropos-symbol`

,`apropos-keybinding`

, and so on;see the

`apropos`

Custom group for details.The old options whose values specified faces to use have been removed

(i.e.

`apropos-symbol-face`

,`apropos-keybinding-face`

, etc.).

### Buffer Menu

This package has been rewritten to use Tabulated List mode.

Option

`Buffer-menu-buffer+size-width`

is now obsolete.Use

`Buffer-menu-name-width`

and`Buffer-menu-size-width`

instead.

### Calendar

You can customize the header text that appears above each calendar month.

See the variable

`calendar-month-header`

.New LaTeX calendar style, produced by

`cal-tex-cursor-week2-summary`

.The calendars produced by cal-html include holidays.

Customize

`cal-html-holidays`

to change this.

### CEDET

The major modes from the parser generators “Bovine” and “Wisent”

are now properly integrated in Emacs. The file suffixes “.by” and “.wy”

are in

`auto-mode-alist`

, and the corresponding manuals are included.

#### EDE

Menu support for the “Configuration” feature. This allows users to

choose the active configuration (such as debug or install) from the menu.

New command

`ede-set`

to interactively set project-local variables.Support for compiling, debugging, and running in “generic” projects.

Autoconf editing support for M4 macros with complex arguments.

Compilation support for the “linux” project type.

“simple” projects have been removed; use “generic” projects instead.


#### Semantic

Support for parsing #include statements inside a namespace in C/C++.

Improved support for ‘extern “C”’ declarations in C/C++.

The ability to ignore more common special C/C++ preprocessor symbols,

such as ‘__nonnull’ and ‘__asm’. Add ‘__cplusplus’ macro when parsing C++.

If available, include cdefs.h as an additional source of preprocessor symbols.

Improved C/C++ function pointer parsing.

In Python, support for converting imports to include file names.

Ability to dynamically determine the Python load path.

Support for the Python ‘WITH’ and ‘AT’ keywords.

Improved tooltip completion.


#### SRecode

The SRecode manual is now included.

Tag generation supports constructor/destructor settings and system

include differentiation.

Addition of ‘Framework’ support: Frameworks are specified when a

particular kind of library (such as Android) is needed in a common language

mode (like Java).

Support for nested templates and let variables override based on priority.

Support for merging tables from multiple related modes, such as

default -> c++ -> arduino.


### Compile

Compile has a new option

`compilation-always-kill`

.

### Customize


`custom-reset-button-menu`

now defaults to t.Non-option variables are never matched in

`customize-apropos`

and

`customize-apropos-options`

(i.e., the prefix argument does nothing forthese commands now).


### Term

The variables

`term-default-fg-color`

and`term-default-bg-color`

are now deprecated in favor of the customizable face

`term`

.

A pre-*customization* anachronism removed at last. Make sure you migrate your term color settings!

You can customize how to display ANSI terminal colors and styles

by customizing the corresponding

`term-color-COLOR`

,

`term-color-underline`

and`term-color-bold`

faces.

If, like me, you customized `ansi-color-names-vector`

to change the default term colours I suggest you switch to using the faces now. The good news here is you can, should desire to, change more than *just* the colours for each ANSI Color: there’s nothing stopping you from forcing a different font for certain colours.

### Tramp

The syntax has been extended in order to allow ad-hoc proxy definitions.


This is a great change and a most needed one if you want to `su`

to a different user once you’ve connected to a another host and you can’t be bothered figuring out how TRAMP proxies work. [STRIKEOUT:Typically I can’t find any information about the new syntax anywhere… I’ll have to dig into the source code and write a post about it later.] Despite my best attempts it seems I completely missed the new chapter, here `(info "(tramp)Ad-hoc multi-hops")`

.

Remote processes are now also supported on remote MS-Windows hosts.


### URL

Structs made by

`url-generic-parse-url`

have nil`attributes`

slot.Previously, this slot stored semicolon-separated attribute-value pairs

appended to some imap URLs, but this is not compatible with RFC 3986.

So now the

`filename`

slot stores the entire path and query components,and the

`attributes`

slot is always nil.New function

`url-encode-url`

for encoding a URI string.The

`url-retrieve`

function now uses this to encode its URL argument,in case that is not properly encoded.

notifications.el supports now version 1.2 of the Notifications API.

The function

`notifications-get-capabilities`

returns the supportedserver properties.


### More misc changes

Flymake uses fringe bitmaps to indicate errors and warnings.

See

`flymake-fringe-indicator-position`

,`flymake-error-bitmap`

and

`flymake-warning-bitmap`

.The FFAP option

`ffap-url-unwrap-remote`

can now be a list of strings,specifying URL types that should be converted to remote file names at

the FFAP prompt. The default is now ’(“ftp”).

New Ibuffer

`derived-mode`

filter, bound to`/ M`

.The old binding for

`/ M`

(filter by used-mode) is now bound to`/ m`

.New option

`mouse-avoidance-banish-position`

specifies where the

`banish`

mouse avoidance setting moves the mouse.In Perl mode, new option

`perl-indent-parens-as-block`

causes non-blockclosing brackets to be aligned with the line of the opening bracket.

In Proced mode, new command

`proced-renice`

renices marked processes.New option

`async-shell-command-buffer`

specifies the buffer to usefor a new asynchronous

`shell-command`

when the default output buffer

`*Async Shell Command*`

is already in use.

Handy if you don’t want your shell output buffer overwritten when you run more than one asynchronous command.

SQL mode has a new option

`sql-db2-escape-newlines`

.If non-nil, newlines sent to the command interpreter will be escaped

by a backslash. The default does not escape the newlines and assumes

that the sql statement will be terminated by a semicolon.

New command

`tabulated-list-sort`

, bound to`S`

in Tabulated List mode(and modes that derive from it), sorts the column at point, or the Nth

column if a numeric prefix argument is given.


Its use should be pretty straight forward but I find that mode a bit buggy. Probably better if you stick to using the one in org mode.


`which-func-modes`

now defaults to t, so Which Function mode, whenenabled, applies to all applicable major modes.


A nice change as Which Function mode worked in more buffers than the `which-func-modes`

gave it credit for.


`winner-mode-hook`

now runs when the mode is disabled, as well as whenit is enabled.

Follow mode no longer works by using advice.

The option

`follow-intercept-processes`

has been removed.

`javascript-generic-mode`

is now an obsolete alias for`js-mode`

.Hooks renamed to avoid obsolete “-hooks” suffix:

semantic-lex-reset-hooks -> semantic-lex-reset-functions

semantic-change-hooks -> semantic-change-functions

semantic-edits-new-change-hooks -> semantic-edits-new-change-functions

semantic-edits-delete-change-hooks -> semantic-edits-delete-change-functions

semantic-edits-reparse-change-hooks -> semantic-edits-reparse-change-functions

semanticdb-save-database-hooks -> semanticdb-save-database-functions

c-prepare-bug-report-hooks -> c-prepare-bug-report-hook

rcirc-sentinel-hooks -> rcirc-sentinel-functions

rcirc-receive-message-hooks -> rcirc-receive-message-functions

rcirc-activity-hooks -> rcirc-activity-functions

rcirc-print-hooks -> rcirc-print-functions

dbus-event-error-hooks -> dbus-event-error-functions

eieio-pre-method-execution-hooks -> eieio-pre-method-execution-functions

checkdoc-style-hooks -> checkdoc-style-functions

checkdoc-comment-style-hooks -> checkdoc-comment-style-functions

archive-extract-hooks -> archive-extract-hook

filesets-cache-fill-content-hooks -> filesets-cache-fill-content-hook

hfy-post-html-hooks -> hfy-post-html-hook

nndiary-request-create-group-hooks -> nndiary-request-create-group-functions

nndiary-request-update-info-hooks -> nndiary-request-update-info-functions

nndiary-request-accept-article-hooks -> nndiary-request-accept-article-functions

gnus-subscribe-newsgroup-hooks -> gnus-subscribe-newsgroup-functions


### Obsolete packages

assoc.el

In most cases, assoc+member+push+delq work just as well.

And in any case it’s just a terrible package: ugly semantics, terrible

inefficiency, and not namespace-clean.

*** bruce.el

*** cust-print.el

*** ledit.el

*** mailpost.el

*** mouse-sel.el

*** patcomp.el


### Incompatible Lisp Changes in Emacs 24.3

Docstrings starting with

`*`

no longer indicate user options.Only variables defined using

`defcustom`

are considered user options.The function

`user-variable-p`

is now an obsolete alias for

`custom-variable-p`

.The return values of

`defalias`

,`defun`

and`defmacro`

have changed,and are now undefined. For backwards compatibility,

`defun`

and

`defmacro`

currently return the name of the newly definedfunction/macro, but this should not be relied upon.


`random`

by default now returns a different random sequence inevery Emacs run. Use

`(random S)`

, where S is a string, to set therandom seed to a value based on S, in order to get a repeatable

sequence in later calls.

If the NEWTEXT arg to

`replace-match`

contains a substring “\?”,that substring is inserted literally even if the LITERAL arg is

non-nil, instead of causing an error to be signaled.


`select-window`

now always makes the window’s buffer current.It does so even if the window was selected before.

The function

`x-select-font`

can return a font spec, instead of afont name as a string. Whether it returns a font spec or a font name

depends on the graphical library.


`face-spec-set`

no longer sets frame-specific attributes when thethird argument is a frame (that usage was obsolete since Emacs 22.2).


`set-buffer-multibyte`

now signals an error in narrowed buffers.The CL package’s

`get-setf-method`

function no longer exists.Generalized variables are now part of core Emacs Lisp, and implemented

differently to the way cl.el used to do it. It is not possible to

define a compatible replacement for

`get-setf-method`

. See the filegv.el for internal details of the new implementation.

The arguments of

`dbus-register-signal`

are no longer just strings,but keywords or keyword-string pairs. The old argument list will

still be supported for Emacs 24.x.

Miscellaneous name changes

Some Lisp symbols have been renamed to correct their spelling,

or to be more consistent with standard Emacs terminology.

Renamed functions

hangul-input-method-inactivate -> hangul-input-method-deactivate

inactivate-input-method -> deactivate-input-method

quail-inactivate -> quail-deactivate

robin-inactivate -> robin-deactivate

viper-inactivate-input-method -> viper-deactivate-input-method

viper-inactivate-input-method-action ->

viper-deactivate-input-method-action

ucs-input-inactivate -> ucs-input-deactivate

Renamed hooks

The old hooks are still supported for backward compatibility, but they

are deprecated and will be removed eventually.

input-method-inactivate-hook -> input-method-deactivate-hook

robin-inactivate-hook -> robin-deactivate-hook

quail-inactivate-hook -> quail-deactivate-hook

Renamed variables

follow-deactive-menu -> follow-inactive-menu

inactivate-current-input-method-function ->

deactivate-current-input-method-function

Some obsolete functions, variables, and faces have been removed:


`last-input-char`

,`last-command-char`

,`unread-command-char`


`facemenu-unlisted-faces`


`rmail-decode-mime-charset`


`iswitchb-read-buffer`


`sc-version`

,`sc-submit-bug-report`


`set-char-table-default`


`string-to-sequence`

(use`string-to-list`

or`string-to-vector`

)

`compile-internal`


`modeline`


`mode-line-inverse-video`


`follow-mode-off-hook`


`cvs-commit-buffer-require-final-newline`

(use

`log-edit-require-final-newline`

instead)

`cvs-changelog-full-paragraphs`

(use

`log-edit-changelog-full-paragraphs`

instead)

`cvs-diff-ignore-marks`

,`cvs-diff-buffer-name`


`vc-ignore-vc-files`

(use`vc-handled-backends`

instead)

`vc-master-templates`

(use`vc-handled-backends`

instead)

`vc-checkout-carefully`


### Lisp Changes in Emacs 24.3

CL-style generalized variables are now in core Elisp.


`setf`

is autoloaded;`push`

and`pop`

accept generalized variables.You can define your own generalized variables using

`gv-define-simple-setter`

,

`gv-define-setter`

, etc.Emacs tries to macroexpand interpreted (non-compiled) files during load.

This can significantly speed up execution of non-byte-compiled code,

but can also bump into previously unnoticed cyclic dependencies.

These are generally harmless: they will simply cause the macro calls

to be left for later expansion (as before), but will result in a

warning (“Eager macro-expansion skipped due to cycle”) describing the cycle.

You may wish to restructure your code so this does not happen.

New sampling-based Elisp profiler.

Try M-x profiler-start, do some work, and then call M-x profiler-report.

When finished, use M-x profiler-stop. The sampling rate can be based on

CPU time or memory allocations.


`defun`

also accepts a (declare DECLS) form, like`defmacro`

.The interpretation of the DECLS is determined by

`defun-declarations-alist`

.New macros

`setq-local`

and`defvar-local`

.Face underlining can now use a wave.


Now you can finally make misspelled words in `ispell-minor-mode`

look like Microsoft Word with squiggly underlines!


`read-regexp`

has a new argument HISTORY; the first argument PROMPTof

`read-regexp`

accepts a string ending with a colon and space, and itssecond argument DEFAULTS can be a list of strings accessible via

`M-n`

in the minibuffer ahead of other hard-coded useful regexp-related values.

More commands use

`read-regexp`

now to read their regexp arguments.

Very useful change for those of us who use readers and often find ourselves reinventing the history wheel.

Completion

New function

`completion-table-with-quoting`

to handle completionin the presence of quoting, such as file completion in shell buffers.

New function

`completion-table-subvert`

to use an existing completiontable, but with a different prefix.


### Debugger

New error type and new function

`user-error`

.These do not trigger the debugger.

New option

`debugger-bury-or-kill`

, saying what to do with thedebugger buffer when exiting debug.

Set

`debug-on-message`

to enter the debugger when a certainmessage is displayed in the echo area. This can be useful when trying

to work out which code is doing something.

New var

`inhibit-debugger`

, automatically set to prevent accidentalrecursive invocations.


### Window handling

New command

`fit-frame-to-buffer`

adjusts the frame height tofit the contents.

The command

`fit-window-to-buffer`

can adjust the frame heightif the new option

`fit-frame-to-buffer`

is non-nil.New macro

`with-temp-buffer-window`

, similar to

`with-output-to-temp-buffer`

.

This is a useful command if you want to generate output with `prin1`

, etc. or print output from an external command in a separate window. I’m personally very happy to see this macro make an appearance.


`temp-buffer-resize-mode`

no longer resizes windows that have beenreused.

New option

`switch-to-buffer-preserve-window-point`

to restore awindow’s point when switching buffers.

New display action alist entries

`window-height`

and`window-width`

specify the size of new windows created by

`display-buffer`

.New display action alist entry

`pop-up-frame-parameters`

, ifnon-nil, specifies frame parameters to give any newly-created frame.

New display action alist entry

`inhibit-switch-frame`

, if non-nil,tells display action functions to avoid changing which frame is

selected.

New display action alist entry

`previous-window`

, if non-nil,specifies window to reuse in

`display-buffer-in-previous-window`

.New display action functions

`display-buffer-below-selected`

,and

`display-buffer-in-previous-window`

.The functions

`get-lru-window`

,`get-mru-window`

and`get-largest-window`

now accept a third argument to avoid choosing the selected window.

Additional values recognized for option

`window-combination-limit`

.The following variables are obsolete, as they can be replaced by

appropriate entries in the

`display-buffer-alist`

function introducedin Emacs 24.1:


`dired-shrink-to-fit`


`display-buffer-reuse-frames`


`display-buffer-function`


`special-display-buffer-names`


`special-display-frame-alist`


`special-display-function`


`special-display-regexps`


### Time


`current-time-string`

no longer requires that its argument’s yearmust be in the range 1000..9999. It now works with any year supported

by the underlying C implementation.


`current-time`

now returns extended-format time stamps(HIGH LOW USEC PSEC), where the new PSEC slot specifies picoseconds.

PSEC is typically a multiple of 1000 on current machines. Other

functions that use this format, such as

`file-attributes`

and

`format-time-string`

, have been changed accordingly. Old-format timestamps are still accepted.

The format of timers in

`timer-list`

and`timer-idle-list`

is now[TRIGGERED-P HI-SECS LO-SECS USECS REPEAT-DELAY FUNCTION ARGS IDLE-DELAY PSECS].

The PSECS slot is new, and uses picosecond resolution. It can be

accessed via the new

`timer--psecs`

accessor.Last-modified time stamps in undo lists now are of the form

(t HI-SECS LO-SECS USECS PSECS) instead of (t HI-SECS . LO-SECS).


### (Old MacDonald had a farm) EIEIO

Improved security when handling persistent objects:


`eieio-persistent-read`

now features optional arguments for specifyingthe class to load, as well as a flag stating whether subclasses are allowed;

if provided, other classes will be rejected by the reader. For

compatibility with existing code, if the class is omitted only a

warning is issued.

New specialized reader for pulling in classes and signaling errors

without evaluation of suspicious code.

All slots that contain objects must have a :type. Slots with lists

of objects must use a new type predicate for a list of an object type.

Support for

`find-function`

and similar utilities, through the additionof filename support to generated symbols.


### Even more misc stuff

Floating point functions now always return special values like NaN,

instead of signaling errors, if given invalid args; e.g., (log -1.0).

Previously, they returned NaNs on some platforms but signaled errors

on others. The affected functions are acos, asin, tan, exp, expt,

log, log10, sqrt, and mod.

New fringe bitmap

`exclamation-mark`

.

Seems like flymake’s using it for errors. Neat.

Miscellaneous changes to special forms and macros


`defun`

and`defmacro`

are now macros rather than special forms.

If you ever wanted to know how a function is created in Emacs, now you can look at the lisp code in `byte-run.el`

. Ditto for `defmacro`

.


`kbd`

is now a function rather than a macro.

### Miscellaneous new functions


`set-temporary-overlay-map`

sets up a temporary keymap thattakes precedence over most other maps for a short while (normally one key).


`autoloadp`

tests if its argument is an autoloaded object.

`autoload-do-load`

performs the autoloading operation.

`buffer-narrowed-p`

tests if the buffer is narrowed.

`file-name-base`

returns a file name sans directory and extension.

`function-get`

fetches a function property, following aliases.

`posnp`

tests if an object is a`posn`

.

`system-users`

returns the user names on the system.

`system-groups`

returns the group names on the system.

`tty-top-frame`

returns the topmost frame of a text terminal.

### The following functions and variables are obsolete:


`automount-dir-prefix`

(use`directory-abbrev-alist`

)

`buffer-has-markers-at`


`macro-declaration-function`

(use`macro-declarations-alist`

)

`window-system-version`

(provides no useful information)

`dired-pop-to-buffer`

(use`dired-mark-pop-up`

)

`query-replace-interactive`


`font-list-limit`

(has had no effect since Emacs

### Changes in Emacs 24.3 on Non-Free Operating Systems

Cygwin builds can use the native MS Windows user interface.

Pass

`--with-w32`

to configure. The default remains the X11 interface.Two new functions are available in Cygwin builds:


`cygwin-convert-file-name-from-windows`

and

`cygwin-convert-file-name-to-windows`

. These functions allow Lispcode to access the Cygwin file-name mapping machinery to convert

between Cygwin and Windows-native file and directory names.

When invoked with the -nw switch to run on the Windows text-mode terminal,

Emacs now supports

`mouse-highlight`

, help-echo (in the echo area), and

`mouse-autoselect-window`

.On MS Windows Vista and later Emacs now supports symbolic links.

On MS Windows, you can pass

`--without-libxml2`

to configure.bat to omitsupport for libxml2, even if its presence is detected.

On Mac OS X, the Nextstep port requires OS X 10.4 or later.

On Mac OS X, configure no longer automatically adds the Fink “/sw”

directories to the search path. You must add them yourself if you want them.


## The End!

Phew. That was a lot of changes and I’ve barely explained 10% of them. Let me know if I glossed over some cool new stuff.
---
title: What's New in Emacs 24 (part 2)
url: https://www.masteringemacs.org/article/what-is-new-in-emacs-24-part-2
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

This is part two of my What’s New in Emacs 24 series. [Part one](https://www.masteringemacs.org/articles/2011/12/06/what-is-new-in-emacs-24-part-1/).

## Trash changes

`delete-by-moving-to-trash’ now only affects commands that specify

trashing. This avoids inadvertently trashing temporary files.


An important change as some features like `flymake`

create

new temporary files every time it runs an external make or linting

tool, resulting in a gazillion temp files ending up in your trash can.

Calling `delete-file’ or `delete-directory’ with a prefix argument

now forces true deletion, regardless of `delete-by-moving-to-trash’.


Very handy addition that mimicks Windows and most major window managers.

New option `list-colors-sort’ defines the color sort order

for `list-colors-display’.


Wow, this is an… interesting.. addition to Emacs. You can govern the *sort* order of colors now such as HSV or RGB distance from a particular color… very neat.

An Emacs Lisp package manager is now included.

This is a convenient way to download and install additional packages,

from a package repository at

[http://elpa.gnu.org].

## Package Manager

`M-x list-packages’ shows a list of packages, which can be

selected for installation.

New command `describe-package’, bound to `C-h P’.

By default, all installed packages are loaded and activated

automatically when Emacs starts up. To disable this, set

`package-enable-at-startup’ to nil. To change which packages are

loaded, customize `package-load-list’.


A much sought-after addition to Emacs. Either Emacs has joined the “App Store” bandwagon or it has finally caught up to XEmacs circa 2001. Your call. Of course, the official stance is that all packages must have its copyright assigned to the FSF, so it’s unlikely that it’ll ever be the *definitive* package source.

I suggest you alter the package manager archive list and add the repository, Marmalade:

```
(require 'package)
(add-to-list 'package-archives '("marmalade" . "http://marmalade-repo.org/packages/"))
```


## Custom Themes

`M-x customize-themes’ lists Custom themes which can be enabled.

New option `custom-theme-load-path’ is the load path for themes.

Emacs no longer looks for custom themes in `load-path’. The default

is to search in `custom-theme-directory’, followed by a built-in theme

directory named “themes/” in `data-directory’.

New option `custom-safe-themes’ records known-safe theme files.

If a theme is not in this list, Emacs queries before loading it, and

offers to save the theme to `custom-safe-themes’ automatically. By

default, all themes included in Emacs are treated as safe.


Color themes, a very popular package and one of the first a lot of people install, is now superseded by a new version bundled with Emacs.

## TRAMP

The user option `remote-file-name-inhibit-cache’ controls whether

the remote file-name cache is used for read access.


This caching mechanism will stop TRAMP from resolving remote file attributes over and over again in a short timespan; you can change numeric value of the variable which govern the cache expiry (in seconds) or enable or disable it permanently with `nil`

or `t`

respectively.

## File- and directory-local variable changes

You can stop directory local vars from applying to subdirectories.

Add an element (subdirs . nil) to the alist portion of any variables

settings to indicate that the section should not apply to

subdirectories.


A welcome change to people who use directory-local variables a lot.

Directory local variables can apply to some file-less buffers.

Affected modes include dired, vc-dir, and log-edit. For example,

adding “(diff-mode . ((mode . whitespace)))” to .dir-locals.el will

turn on `whitespace-mode’ for *vc-diff* buffers. Modes should call

`hack-dir-local-variables-non-file-buffer’ to support this.


Another step in the direction towards “project”-like functionality.

Using “mode: MINOR-MODE” to enable a minor mode is deprecated.

Instead, use “eval: (minor-mode 1)”.


Pretty self-explanatory.

## Misc

New primitive `secure-hash’ that supports many secure hash algorithms

including md5, sha-1 and sha-2 (sha-224, sha-256, sha-384 and sha-512).

The elisp implementation sha1.el is removed. Feature sha1 is provided

by default.


Excellent addition, though I cannot find any commands that let you use it on a string or buffer directly.

## Window changes

The behavior of `display-buffer’ is now customizable in detail.

New option `display-buffer-base-action’ specifies a list of

user-determined display “actions” (functions and optional arguments

for choosing the displaying window).

This takes precedence over the default display action, which is

specified by `display-buffer-fallback-action’.

New option `display-buffer-alist’ maps buffer name regexps to

display actions, taking precedence over `display-buffer-base-action’.


Interesting change that should make it easier for people to control which frame or window a buffer should appear in. Having used the defaults for so long I would find it hard to switch, but I’m sure there are lots of people – especially tiling WM fans – who would want Emacs to use more frames.

New option `window-combination-limit’.

The new option `window-combination-limit’ allows to return the space

obtained for resizing or creating a window more reliably to the window

from which such space was obtained.


This command does a lot more, seemingly, than what the description here says it does; reading the docstring for the variable clouds the issue as it is pretty obtuse. From what I can tell, when you `C-x 0`

a window while this option is enabled you will remain in *its* parent, and that parent is the one in which the new window was spawned from (with `C-x 2`

or `C-x 3`

). That it claims to return the space more effciently may be a side effect of this change in behavior – or maybe it’s the other way around? Either way, enable it and see if you like how it works.

New option `window-combination-resize’.

The new option `window-combination-resize’ allows to split a window that

otherwise cannot be split because it’s too small by stealing space from

other windows in the same combination. Subsequent resizing or deletion

of the window will resize all windows in the same combination as well.


Now *this* is a useful switch (unlike the one above) as now Emacs will assign an equal amount of space to each window when you split or delete windows.

New commands `maximize-window’ and `minimize-window’.

These maximize and minimize the size of a window within its frame.

New commands `switch-to-prev-buffer’ and `switch-to-next-buffer’.

These functions allow to navigate through the live buffers that have

been shown in a specific window.


Sorely missed window and buffer commands finally make an (official) appearance in Emacs. I suggest you bind these commmands to something right away! Of course there’s no `restore-window`

command.

New functions `window-state-get’ and `window-state-put’.

These functions allow to save and restore the state of an arbitrary

frame or window as an Elisp object.


Useful for Elisp hackers looking for a way to save and restore the window states.

The inactive minibuffer has its own major mode `minibuffer-inactive-mode’.

This is handy for minibuffer-only frames, and is also used for the "mouse-1

pops up *Messages*" feature, which can now easily be changed.


Even more streamlining of Emacs.

## Editing Changes in Emacs 24.1

### Search changes

C-y in Isearch is now bound to isearch-yank-kill, instead of

isearch-yank-line.

M-y in Isearch is now bound to isearch-yank-pop, instead of

isearch-yank-kill.

M-s C-e in Isearch is now bound to isearch-yank-line.


So this change is a controversial one, as you had to press `M-y`

to yank in isearch, whereas now it is consistent with the rest of Emacs: `C-y`

yanks and `M-y`

cycles the kill ring. I like the change as it keeps Emacs consistent and easier to use for new users. Not to mention that adding the rest of the line to an isearch query is an uncommon action.

New commands `count-words-region’ and `count-words’.

`count-lines-region’ is now an alias for `count-words-region’,

bound to M-=, which shows the number of lines, words, and characters.


Another sorely missed feature but do be careful using it. The notion of a “word” is governed entirely by the syntax table, and so what counts as a single word in one mode may well be more than one in another. For example, the command “count-words-region” – is that one or three words? Again, it depends on the mode.

The default value of `backup-by-copying-when-mismatch’ is now t.


This variable is only of interest to people who use `backup-by-copying`

and then only if you care about how Emacs preserves the owner and group of the file.

The command `just-one-space’ (M-SPC), if given a negative argument,

also deletes newlines around point.


The `just-one-space`

command is already a very useful tool in programming, and with the new negative argument toggle, even more so.

### Deletion changes

New option `delete-active-region’.

If non-nil, [delete] and DEL delete the region if it is active and no

prefix argument is given. If set to `kill’, these commands kill

instead.

New command `delete-forward-char’, bound to [delete].

This is meant for interactive use, and obeys `delete-active-region’.

The command `delete-char’ does not obey `delete-active-region’.


Another standardization change aimed at helping new users. Confusingly, however, it does not replace the behavior afforded by `M-x delete-selection-mode`

. That mode will only delete the selected text if, and only if, you type a character. So all`delete-active-region`

does is make it so if you press a key bound to `delete-[forward/backward]-char`

it will delete the active region. The two of them, combined, make Emacs behave like other applications.

`delete-backward-char’ is now a Lisp function.

Apart from obeying `delete-active-region’, its behavior is unchanged.

However, the byte compiler now warns if it is called from Lisp; you

should use delete-char with a negative argument instead.


If you’re an elisp author and you use `delete-backward-char`

(or indeed, its *forward* counterpart) while you have the region active, expect it to nuke the entire selection if `delete-active-region`

is `t`

. Better to switch to `delete-char`

and avoid this problem altogether.

The option `mouse-region-delete-keys’ has been deleted.


Because selections are now deleted by default (if `delete-active-region`

is `t`

) with any key bound to `delete-[forward/backward]-char`

, this option is redundant.

## Selection changes.

The default handling of clipboard and primary selections was changed

to conform with modern X applications. In short, most commands for

killing and yanking text now use the clipboard, while mouse commands

use the primary selection.

In the following, we provide a list of these changes, followed by a

list of steps to get the old behavior back if you prefer that.

`select-active-regions’ now defaults to t.

Merely selecting text (e.g. with drag-mouse-1) no longer puts it in

the kill ring. The selected text is put in the primary selection, if

the system possesses a separate primary selection facility (e.g. X).

`select-active-regions’ also accepts a new value, `only’.

This means to only set the primary selection for temporarily active

regions (usually made by mouse-dragging or shift-selection);

“ordinary” active regions, such as those made with C-SPC followed by

point motion, do not alter the primary selection.

`mouse-drag-copy-region’ now defaults to nil.

mouse-2 is now bound to `mouse-yank-primary’.

This pastes from the primary selection, ignoring the kill-ring.

Previously, mouse-2 was bound to `mouse-yank-at-click’.

`x-select-enable-clipboard’ now defaults to t on all platforms.

`x-select-enable-primary’ now defaults to nil.

Thus, commands that kill text or copy it to the kill-ring (such as

M-w, C-w, and C-k) also use the clipboard—not the primary selection.

The “Copy”, “Cut”, and “Paste” items in the “Edit” menu are now

exactly equivalent to, respectively M-w, C-w, and C-y.

Note that on MS-Windows, `x-select-enable-clipboard’ was already

non-nil by default, as Windows does not support the primary selection

between applications.


Yet again, more standardization. That can only be a good thing. This alone should cut the number of mailinglist and IRC channel questions in half.

If you’re a curmudgeonly Emacs hacker, follow this advice to get the old behavior back:

To return to the previous behavior, do the following:

Change `select-active-regions’ to nil.

Change `mouse-drag-copy-region’ to t.

Change `x-select-enable-primary’ to t (on X only).

Change `x-select-enable-clipboard’ to nil.

Bind `mouse-yank-at-click’ to mouse-2.

Support for X cut buffers has been removed.

X clipboard managers are now supported.

To inhibit this, change `x-select-enable-clipboard-manager’ to nil.


## Rectangle Commands

New command `rectangle-number-lines’, bound to `C-x r N’, numbers

the lines in the current rectangle. With a prefix argument, this

prompts for a number to count from and for a format string.


Sorely needed numbering rectangle command makes an appearance at last. Saves you the hassle of using a macro or regular expression.

The default value of redisplay-dont-pause is now t

This makes Emacs feel more responsive to editing commands that arrive

at high rate, e.g. if you lean on some key, because stopping redisplay

in the middle (when this variable is nil) forces more expensive

updates later on, and Emacs appears to be unable to keep up.


I blogged about a similar command earlier, and this, too, is one of those commands you will have to use for a while to find out if it benefits you or not.

The behavior of <TAB> for active regions in Text mode has changed.

In Text and related modes, typing <TAB> (`indent-for-tab-command’)

when the region is active causes Emacs to indent all the lines in the

region, aligning them with the line previous to the first line in the

region (or with the left margin if there is no previous line).


About. Time. Ever hit `TAB`

in a mode with no indentation engine only to see your lines indented like this:

```
foo
bar
baz
```


Well, your woes are over. It will now apply a fixed indentation to the entire region instead of doing it recursively to each one.

## Changes in Specialized Modes and Packages in Emacs 24.1

Archive Mode has basic support for browsing and updating 7z archives.


As 7zip is becoming more and more popular, this change can only be a good thing.

browse-url has a new variable `browse-url-mailto-function’

specifies how mailto: URLs are handled. The default is `browse-url-mail’.


This is a great addition, especially to people who use Emacs for email. Make sure you `(require 'browse-url)`

before assigning to the variable.

## BibTeX mode

BibTeX mode now supports biblatex.

Use the variable bibtex-dialect to select support for different BibTeX

dialects. bibtex-entry-field-alist is now an obsolete alias for

bibtex-BibTeX-entry-alist.

New command `bibtex-search-entries’ bound to C-c C-a.

New `bibtex-entry-format’ option `sort-fields’, disabled by default.

New variable `bibtex-search-entry-globally’.


## Calendar, Diary, and Appt

Diary entries can contain non-printing `comments’.

See the variable `diary-comment-start’.

Appointments can specify their individual warning times.

See the variable `appt-warning-time-regexp’.

The function specified by `appt-disp-window-function’ may be passed

lists of arguments if multiple appointments are due at similar times.

If you are using a custom function for this, you should update it.

New function `diary-hebrew-birthday’.

Elements of `calendar-day-abbrev-array’ and `calendar-month-abbrev-array’

may no longer be nil, but must all be strings.

The obsolete (since Emacs 22.1) method of enabling the appt package

by adding appt-make-list to diary-hook has been removed. Use appt-activate.

Some appt variables (obsolete since Emacs 22.1) have been removed:

appt-issue-message (use the function appt-activate)

appt-visible/appt-msg-window (use the variable appt-display-format)

Some diary function aliases (obsolete since Emacs 22.1) have been removed:

view-diary-entries, list-diary-entries, show-all-diary-entries


The diary and calendar functionality in Emacs is woefully underused. The calendar, in particular, is useful; and like all Emacs features it is extremely advanced and capable of a great many things.

## CC Mode (C, C++, etc.)

New feature to “guess” the style in an existing buffer.


Perhaps one of the more significant features to make an appearance in Emacs 24. This feature should work with any *cc-mode*-derived mode, and hopefully save you the hassle of having to configure the 50 billion different indentation settings Emacs has.

## Comint

comint and modes derived from it use the generic completion code.


All this change really means is that comint-derived modes will, by default, use `completion-at-point`

instead of a now deprecated, comint-specific version.

## Compilation mode

Compilation mode can be used without font-lock-mode.

`compilation-parse-errors-function’ is now obsolete.

`compilation-filter-start’ is let-bound to the start of the text

inserted by the compilation filter function, when calling

compilation-filter-hook.

`compilation-error-screen-columns’ is obeyed in the editing buffer.

So programming language modes can set it, whereas previously only the value

in the *compilation* buffer was used.


## Customize

Customize buffers now contain a search field.

The search is performed using `customize-apropos’.

To turn off the search field, set custom-search-field to nil.


Yay! Very useful and a welcome change. If you’re not comfortable rummaging around Emacs’s internals to track down settings, you now have the option of using the Search interface in customize.

Custom options now start out hidden if at their default values.

Use the arrow to the left of the option name to toggle visibility.

custom-buffer-sort-alphabetically now defaults to t.

The color widget now has a “Choose” button, which allows you to

choose a color via list-colors-display.


Definitely a welcome addition.

## D-Bus

It is possible now, to access alternative buses than the default

system or session bus.

dbus-register-{service,method,property}

The -method and -property functions do not automatically register

names anymore.

The new function dbus-register-service registers a service known name

on a D-Bus without simultaneously registering a property or a method.


D-Bus functionality is a nice-to-have (even though its Windows support is lacking) but I have yet to see any Emacs packages make great use of it. Hopefully external shells like iPython will add support for it to eliminate the reliance on parsing the stdout of a comint process.

## Dired-x

dired-jump and dired-jump-other-window called with a prefix argument

read a file name from the minibuffer instead of using buffer-file-name.

The `dired local variables’ feature provided by Dired-x is obsolete.

The standard directory local variables feature replaces it.


## ERC changes

New vars `erc-autojoin-timing’ and `erc-autojoin-delay’.

If the value of `erc-autojoin-timing’ is ’ident, ERC autojoins after a

successful NickServ identification, or after `erc-autojoin-delay’

seconds. The default value, ’ident, means to autojoin immediately

after connecting.


Very handy if you use ERC for your IRC needs, especially on networks like Freenode where you cannot join certain channels without identifying to nickserv beforehand.

New variable `erc-coding-system-precedence’: If we use `undecided’

as the server coding system, this variable will then be consulted.

The default is to decode strings that can be decoded as utf-8 as

utf-8, and do the normal `undecided’ decoding for the rest.


## Eshell changes

The default value of eshell-directory-name is a directory named

“eshell” in `user-emacs-directory’. If the old “~/.eshell/” directory

exists, that is used instead.


This change was probably prompted by a need for better cross-platform support as some older versions of Windows don’t handle directories and files beginning with ‘.’ very well.

## GDB-MI

GDB User Interface migrated to GDB Machine Interface and now

supports multithread non-stop debugging and debugging of several

threads simultaneously.


## IDO Mode

In ido-mode, C-v is no longer bound to ido-toggle-vc.

The reason is that this interferes with cua-mode.


Sensible change for people who use CUA.

## Image mode

RET (`image-toggle-animation’) toggles animation, if the displayed

image can be animated.

Option `image-animate-loop’, if non-nil, loops the animation.

If nil, `image-toggle-animation’ plays the animation once.


## Info

New command `info-display-manual’ displays an Info manual

specified by its name. If that manual is already visited in some Info

buffer within the current session, the command will display that

buffer. Otherwise, it will load the manual and display it. This is

handy if you have many manuals in many Info buffers, and don’t

remember the name of the buffer visiting the manual you want to

consult.


This command is essentially a wrapper around `M-: (info "(emacs)Top")`

.

## Misc Changes

The Landmark game is now invoked with `landmark’, not `lm’.

MH-E has been upgraded to MH-E version 8.3.1.

See MH-E-NEWS for details.

Modula-2 mode provides auto-indentation.

mpc.el: Can use pseudo tags of the form tag1|tag2 as a union of two tags.

Prolog mode has been completely revamped, with lots of additional

functionality such as more intelligent indentation, electricity, support for

more variants, including Mercury, and a lot more.


Neat. I’ve not done Prolog in many years, but last time I did I found Prolog support in Emacs lacking.

## Rmail

The command `rmail-epa-decrypt’ decrypts OpenPGP data

in the Rmail incoming message.

The variable `rmail-message-filter’ no longer has any effect.

This change was made in Emacs 23.1 but was not advertised at the time.

Try using `rmail-show-message-hook’ instead.


## Shell mode

*This entry is a duplicate of the completion change mentioned in part 1*

Shell mode uses pcomplete rules, with the standard completion UI.

The `shell’ command prompts for the shell path name if the default

directory is a remote file name and neither the environment variable

$ESHELL nor the variable `explicit-shell-file-name’ is set.

New variable `shell-dir-cookie-re’.

If set to an appropriate regexp, Shell mode can track your cwd by

reading it from your prompt.


This will no doubt please a lot of people tired of shell losing track of the PWD. As an alternative you can use `dirtrack`

which is what I have historically used.

## SQL Mode enhancements.

`sql-dialect’ is an alias for `sql-product’.

New variable `sql-port’ specifies the port number for connecting

to a MySQL or Postgres server.


With the new connection string functionality this new option is probably moot for most people who interact with databases frequently.

The command `sql-product-interactive’ now takes a prefix argument,

which causes it to prompt for an SQL product instead of the current

value of `sql-product’.

Product-specific SQL interactive commands now take prefix args.

These commands (`sql-sqlite’, `sql-postgres’, `sql-mysql’, etc.),

given a prefix argument, prompt for a name for the SQL interactive

buffer. This reduces the need for calling `sql-rename-buffer’.


Handy, but it would be better if the buffer named itself more sensibly to begin with - such as using the database and username in the buffer name.

SQL interactive modes suppress command continuation prompts, and

replace tabs with spaces. The first change impacts multiple line SQL

statements entered with C-j between each line, statements yanked into

the buffer and statements sent with `sql-send-*’ functions. The

second change prevents the MySQL and Postgres interpreters from

listing object name completions when sent text via `sql-send-*’

functions.


This is a good change. If it works properly in practice it will eliminate all the annoying continuation prompts and other text flotsam in the inferior sql shell. The only other issue has always been the sending of large buffers to the inferior sql buffer. Earlier Emacsen would hang.

New custom variables control prompting for login parameters.

Each supported product has a custom variable `sql-*-login-params’,

which is a list of the parameters to be prompted for before a

connection is established.

New variable `sql-connection-alist’ for login parameter values.

This can be used to store different username, database and server

values. Connections defined in this variable appear in the submenu

SQL->Start… for making new SQLi sessions.

New command `sql-connect’ starts a predefined SQLi session,

using the login parameters from `sql-connection-alist’.

New “Save Connection” menu item in SQLi buffers.

This gathers the login params specified for the SQLi session, if it

was not started by a connection, and saves them as a new connection.


These changes all govern the much-needed and much-welcome connection list system now in place. As an added cherry on top the dynamic way databases are loaded makes it (relatively) easy – in theory anyway – to add new databases and have most of the features work out of the box.

### Commands for listing database objects and details.

an SQLi session, you can get a list of objects in the database.

The contents of these lists are product specific.

`C-c C-l a’ or the “SQL->List all objects” menu item

lists all the objects in the database. With a prefix argument, it

displays additional details or extend the listing to include other

schemas objects.

`C-c C-l t’ or the “SQL->List Table details” menu item

prompts for the name of a database table or view and displays the list

of columns in the relation. With a prefix argument, it displays

additional details about each column.


Now *this* is neat. This completion functionality is a serious aid if you are using a database like Oracle where every object is defined as metadata.

New options `sql-send-terminator’ and `sql-oracle-scan-on’.


The first option is useful if, like me, you often forget to terminate your queries; the second is mandatory if you use the & placeholders in Oracle as now Emacs will query for the values (like SQLPlus does.)

An API for manipulating SQL product definitions has been added.


There are detailed instructions on how to do this in the commentary section of the library, `sql.el`

.

## TeX modes

latex-electric-env-pair-mode keeps \begin..\end matched on the fly.


## Tramp

There exists a new inline access method “ksu” (kerberized su).


I’ve never used kerberos with su before, but that it is now supported will surely come in handy in the future.

The following access methods are discontinued: “ssh1_old”,

“ssh2_old”, “scp1_old”, “scp2_old”, “imap”, “imaps” and “fish”.

The option `ange-ftp-binary-file-name-regexp’ has changed its

default value to “”.

`url-queue-retrieve’ downloads web pages asynchronously, but allow

controlling the degree of parallelism.


## VC and related modes

Support for pulling on distributed version control systems.

The vc-pull command runs a “pull” operation, if it is supported.

This updates the current branch from upstream. A prefix argument

means to prompt the user for specifics, e.g. a pull location.

`vc-update’ is now an alias for `vc-pull’.

Currently supported by Bzr, Git, and Mercurial.


This is perhaps one of the bigger changes a lot of people have waited for. With Emacs using a DVCS now as its official repository, the addition was inevitable.

Support for merging on distributed version control systems.

The vc-merge command now runs a “merge” operation, if it is supported.

This merges another branch into the current one. This command prompts

the user for specifics, e.g. a merge source.

Currently supported for Bzr, Git, and Mercurial.


Another very welcome feature.

New option `vc-revert-show-diff’ controls whether `vc-revert’

shows a diff while querying the user. It defaults to t.


Good to know that this behavior can be toggled, but I’ll leave it on; you never know when you might revert something you want to keep.

Log entries in some Log View buffers can be toggled to display a

longer description by typing RET (log-view-toggle-entry-display).

In the Log View buffers made by `C-x v L’ (vc-print-root-log), you can

use this to display the full log entry for the revision at point.

Currently supported for Bzr, Git, and Mercurial.

Packages using Log View mode can enable this functionality by

binding `log-view-expanded-log-entry-function’ to a suitable function.


This is useful if you want to customize how Emacs displays the root log view (`C-x v L`

)

New command `vc-ediff’ allows visual comparison of two revisions

of a file similar to `vc-diff’, but using ediff backend.


I’m not sure I’ll switch, as much as I love ediff. Ediff is the 800 lbs gorilla of diffing and merging and, well, when I want to diff something the simple diff view mode works fine.

`vc-toggle-read-only’ is an obsolete alias for `toggle-read-only’.

Since Emacs 23, it has done the same thing as `toggle-read-only’, but

this was not advertised at the time.

The option `vc-initial-comment’ was removed in Emacs 23.2, but

this was not advertised at the time.


## Obsolete modes

partial-completion-mode is obsolete.

You can get a comparable behavior with:

(setq completion-styles ’(partial-completion initials))

(setq completion-pcm-complete-word-inserts-delimiters t)


Never used this mode, but I suppose the more sophisticated completion mechanisms available now have made it redundant.

pc-mode.el is obsolete.


With Emacs slowly standardizing on the same keyboard shortcuts as modern apps, this package has outlived its usefulness. The fact that it aims to emulate a *PC* gives you an idea of how old it is (16 years.)

sregex.el is obsolete, since rx.el is a strict superset.


`rx`

is a wonderful s-expression based regex engine, and there is no reason why Emacs should have other packages lying around that do essentially the same thing.

s-region.el and pc-select are obsolete.

They are superseded by shift-select-mode enabled by default in 23.1.


More standardization and more obsolescence.

## Miscellaneous

f90.el has some support for Fortran 2008 syntax.


Fortran users rejoice.

`copyright-fix-years’ can optionally convert consecutive years to ranges.


I never actually knew this library existed. Cool.

New command `nato-region’ converts text to NATO phonetic alphabet.


That’s not terribly useful, except when you have to spell the word “Zyzygy” to somebody over the phone. It’s right up there with the `[un]morse-region`

commands.

## New Modes and Packages in Emacs 24.1

Occur Edit mode applies edits made in *Occur* buffers to the

original buffers. It is bound to “e” in Occur mode.


Probably one of the best changes in Emacs 24 yet. Forget color themes and package managers. This is the sort of thing that gives Emacs the edge, and now we no longer need a 3rd party package to do this.

New global minor modes electric-pair-mode, electric-indent-mode,

and electric-layout-mode.


These modes are designed to replace the umpteen different electric functions each major mode invariably reinvent. Still more standardization!

tabulated-list.el provides a generic major mode for tabulated data,

from which other modes can be derived.


It seems there are no actual modes that inherit from this generic framework yet, but looking code it seems like it’ll be a doozy to support a variety of tabulated formats with only about 10-15 lines of code.

pcase.el provides the ML-style pattern matching macro `pcase’.

secrets.el is an implementation of the Secret Service API, an

interface to password managers like GNOME Keyring or KDE Wallet. The

Secret Service API requires D-Bus for communication. The command

`secrets-show-secrets’ offers a buffer with a visualization of the

secrets.


Seems like a useful addition to Emacs. I’ll have to study this in greater detail.

notifications.el provides an implementation of the Desktop

Notifications API. It requires D-Bus for communication.


Useful if you combine it with ERC to notify you if you’ve received an IRC message when Emacs is not in focus.

soap-client.el supports access to SOAP web services from Emacs.

soap-inspect.el is an interactive inspector for SOAP WSDL structures.


Very handy, but I wonder if it blocks the thread while it is in operation.

xmodmap-generic-mode for xmodmap files.

New emacs-lock.el package.

(The pre-existing one has been renamed to old-emacs-lock.el and moved

to obsolete/.) Now, Emacs Lock is a proper minor mode

`emacs-lock-mode’. Protection against exiting Emacs and killing the

buffer can be set separately. The mechanism for auto turning off

protection for buffers with inferior processes has been generalized.


If you’re prone to twitch killing this could be the mode for you.

## Incompatible Lisp Changes in Emacs 24.1

`char-direction-table’ and the associated function `char-direction’

were deleted. They were buggy and inferior to the new support of

bidirectional editing introduced in Emacs 24. If you need the

bidirectional properties of a character, use `get-char-code-property’

with the last argument `bidi-class’.

`copy-directory’ now copies the source directory as a subdirectory

of the target directory, if the latter is an existing directory. The

new optional arg COPY-CONTENTS, if non-nil, makes the function copy

the contents directly into a pre-existing target directory.

`compose-mail’ now accepts an optional 8th arg, RETURN-ACTION, and

passes it to the mail user agent function. This argument specifies an

action for returning to the caller after finishing with the mail.

This is currently used by Rmail to delete a mail window.

For mouse click input events in the text area, the Y pixel

coordinate in the POSITION list now counts from the top of the text

area, excluding any header line. Previously, it counted from the top

of the header line.

Removed obsolete name `e’ (use `float-e’ instead).

A backquote not followed by a space is now always treated as new-style.

Test for special mode-class was moved from view-file to view-buffer.

FIXME: This only says what was changed, but not what are the

programmer-visible consequences.

Passing a nil argument to a minor mode function now turns the mode

ON unconditionally.

During startup, Emacs no longer adds entries for `menu-bar-lines’

and `tool-bar-lines’ to `default-frame-alist’ and `initial-frame-alist’.

With these alist entries omitted, `make-frame’ checks the value of the

variable `menu-bar-mode’/`tool-bar-mode’ to determine whether to create

a menu-bar or tool-bar, respectively. If the alist entries are added,

they override the value of `menu-bar-mode’/`tool-bar-mode’.

Regions created by mouse dragging are now normal active regions,

similar to the ones created by shift-selection. In previous Emacs

versions, these regions were delineated by `mouse-drag-overlay’, which

has now been removed.

cl.el no longer provides `cl-19’.

The menu bar bindings’s caches are not used any more.

Use (where-is-internal nil t) instead.

The following obsolete functions and aliases were removed:

comint-kill-output, decompose-composite-char, outline-visible,

internal-find-face, internal-get-face, frame-update-faces,

frame-update-face-colors, x-frob-font-weight, x-frob-font-slant,

x-make-font-bold, x-make-font-demibold, x-make-font-unbold

x-make-font-italic, x-make-font-oblique, x-make-font-unitalic

x-make-font-bold-italic, mldrag-drag-mode-line, mldrag-drag-vertical-line,

iswitchb-default-keybindings, char-bytes, isearch-return-char,

make-local-hook

The following obsolete variables and varaliases were removed:

checkdoc-minor-keymap, vc-header-alist, directory-sep-char, and

font-lock-defaults-alist.

The following obsolete files were removed:

sc.el, x-menu.el, rnews.el, rnewspost.el


## Lisp changes in Emacs 24.1

Code can now use lexical scoping by default instead of dynamic scoping.

The `lexical-binding’ variable lets code use lexical scoping for local

variables. It is typically set via file-local variables, in which case it

applies to all the code in that file.

`eval’ takes a new optional argument `lexical’ to choose the new lexical

binding instead of the old dynamic binding mode.

Lexically scoped interpreted functions are represented with a new form

of function value which looks like (closure ENV ARGS &rest BODY).

New macro `letrec’ to define recursive local functions.

New function `special-variable-p’ to check whether a variable is

declared as dynamically bound.


The first of many changes to Emacs’s elisp engine to make it more performant, feature rich and in line with what people expect of a modern Lisp. A large amount of the existing Emacs packages have already been switched to lexical scoping, but it is apparently difficult to get right as Emacs’s codebase is heavily reliant on dynamic scoping to monkeypatch or extend other parts of the code.

An Emacs Lisp testing tool is now included.

Emacs Lisp developers can use this tool to write automated tests for

their code. See the ERT info manual for details.


Emacs gets its first built-in unit testing framework. Time will tell if it is powerful and easy enough to use for package maintainers to adopt it.

## Changes for bidirectional display and editing

New function `current-bidi-paragraph-direction’.

This returns the actual value of base direction of the paragraph at

point.

New function `bidi-string-mark-left-to-right’.

Given a string containing characters from right-to-left (RTL) scripts,

this function returns another string which can be safely inserted into

a buffer, such that any following text will be always displayed to the

right of that string. (This works by appending the Unicode

“LEFT-TO-RIGHT MARK” character when the argument string might need that.)

is useful when the buffer has overall left-to-right (LTR)

paragraph direction and you need to insert a string whose contents and

directionality are not known in advance, without disrupting the layout

of the line.


## Window changes

Window tree functions are accessible in Elisp.

Functions are provided to return the parent, siblings or child windows

of any window including internal windows (windows not associated with a

buffer) in the window tree.

New function `window-valid-p’ gives non-nil for live and internal

windows.

Window manipulation can deal with internal windows.

Many window handling functions like `split-window’, `delete-window’, or

`delete-other-windows’ as well as the window resizing functions can now

act on any window including internal ones.

window-total-height/-width vs window-body-height/-width.

The function `window-height’ has been renamed to `window-total-height’

and `window-width’ has been renamed to `window-body-width’. The old

names are provided as aliases. Two new functions `window-total-width’

and `window-body-height’ are provided.

Window parameters specific to window handling functions.

For each window you can specify a parameter to override the default

behavior of a number of functions like `split-window’, `delete-window’

and `delete-other-windows’. The variable `ignore-window-parameters’

allows to ignore processing such parameters.

New semantics of third argument of `split-window’.

The third argument of `split-window’ has been renamed to SIDE and can be

set to any of the values ’below, ’right, ’above, or ’left to make the

new window appear on the corresponding side of the window that shall be

split. Any other value of SIDE will cause `split-window’ to split the

window into two side-by-side windows as before.

Window resizing functions.

A new standard function for resizing windows called `window-resize’ has

been introduced. This and all other functions for resizing windows no

longer delete any windows when they become too small.

Deleting the selected window now selects the most recently selected

live window on that frame instead.

`adjust-window-trailing-edge’ adjustments.

`adjust-window-trailing-edge’ can now deal with fixed-size windows and

is able to resize other windows if a window adjacent to the trailing

edge cannot be shrunk any more. This makes its behavior more similar to

that of Emacs 21 without compromising, however, its inability to delete

windows which was introduced in Emacs 22.

Window-local buffer lists.

Windows now have local buffer lists. This means that removing a buffer

from display in a window will preferably show the buffer previously

shown in that window with its previous window-start and window-point

positions. This also means that the same buffer may be automatically

shown twice even if it already appears in another window.


This is perhaps the only change to Emacs’s windowing functionality that most people care about; namely that windows had a habit of forgetting the order in which buffers were shown if you had multiple windows.

`switch-to-buffer’ has a new optional argument FORCE-SAME-WINDOW,

which if non-nil requires the buffer to be displayed in the currently

selected window, signaling an error otherwise. If nil, another window

can be used, e.g. if the selected one is strongly dedicated.

`split-window-vertically’ and `split-window-horizontally’ renamed

to `split-window-below’ and `split-window-right’ respectively.

The old names are kept as aliases.


A sensible name change, especially in light of the above that let you split windows from a certain “side” of the active window.

### Display actions

The second arg to `display-buffer’ and `pop-to-buffer’ is now

named ACTION, and takes a display action of the same form as

`display-buffer-base-action’ (see Changes, above). A non-nil,

non-list value is treated specially, as the old meaning.

New variable `display-buffer-overriding-action’.

The procedure of `display-buffer’ etc. to choose a window is

determined by combining `display-buffer-overriding-action’,

`display-buffer-alist’, the ACTION arg, `display-buffer-base-action’,

and `display-buffer-fallback-action’. The second and fourth of these

are user-customizable variables.

See the docstring of `display-buffer’ for details.


This harkens back to the display buffer change I talked about earlier.

New behavior of `quit-window’.

The behavior of `quit-window’ has been changed in order to restore the

state before the last buffer display operation in that window.

The new option `frame-auto-hide-function’ lets you choose between

iconifying or deleting a frame when burying a buffer shown in a dedicated

frame or quitting a window showing a buffer in a frame of its own.


This is probably only of interest to people who rely heavily on frames instead of windows.

## Completion

New variable completion-extra-properties used to specify extra properties

of the current completion:


- :annotate-function, same as the old completion-annotate-function.
- :exit-function, function to call after completion took place.
Functions on completion-at-point-functions can return any of the properties

valid for completion-extra-properties.

completion-annotate-function is obsolete.

New `metadata’ method for completion tables. The metadata thus returned

can specify various details of the data returned by `all-completions’:


- `category’ is the kind of objects returned (e.g., `buffer’, `file’, …),
used to select a style in completion-category-overrides.


- `annotation-function’ to add annotations in *Completions*.
- `display-sort-function’ to specify how to sort entries in *Completions*.
- `cycle-sort-function’ to specify how to sort entries when cycling.

I’m curious to see what package authors will do with this new functionality. The greater support for annotation in particular should prove interesting.

minibuffer-local-filename-must-match-map is not used any more.

Instead, the bindings in minibuffer-local-filename-completion-map are

combined with minibuffer-local-must-match-map.

New variable `completing-read-function’ allows overriding the

behavior of `completing-read’.


This change is probably prompted by a desire to make it easier for packages like IDO mode to replace the default `completing-read`

function without resorting to monkey patching.

`glyphless-char-display’ can now distinguish between graphical and

text terminal display, via a char-table entry that is a cons cell.

`open-network-stream’ can now be used to open an encrypted stream.

It now accepts an optional `:type’ parameter for initiating a TLS

connection, directly or via STARTTLS. To do STARTTLS, additional

parameters (`:end-of-command’, `:success’, `:capabilities-command’)

must also be supplied.


I hope this change means we’ll see native support for TLS in mail programs like GNUS.

pre/post-command-hook are not reset to nil upon error.

Instead, the offending function is removed.


## New hook types

New function `run-hook-wrapped’ for running an abnormal hook by

passing the hook functions as arguments to a “wrapping” function.

New macro `with-wrapper-hook’ for running an abnormal hook as a

set of “wrapping” filters, similar to around advice.

`server-eval-at’ is provided to allow evaluating forms on different

Emacs server instances.


Hmm. There’s a lot of potential locked away in this one command. Large-scale mapreduce clusters are, I suppose, now possible with Emacs thanks to Elisp and the functions `map`

and `reduce`

:-)

`call-process’ allows a `(:file “file”)’ spec to redirect STDOUT to

a file.

Variable `stack-trace-on-error’ removed.

Also the debugger can now “continue” from an error, which means it will jump

to the error handler as if the debugger had not been invoked instead of

jumping all the way to the top-level.


The ability to continue after encountering an error is a pretty big deal if you use edebug a lot!

The function format-time-string now supports the %N directive, for

higher-resolution time stamps.


The exact nature of how the high-resolution time stamps are sourced is left undefined. This functionality is likely to differ slightly depending on the platform.

New function `read-char-choice’ reads a restricted set of characters,

discarding any inputs not inside the set.


This is pretty handy if you’re making your own minibuffer prompts.

`image-library-alist’ is renamed to `dynamic-library-alist’.

The variable is now used to load all kind of supported dynamic libraries,

not just image libraries. The previous name is still available as an

obsolete alias.

New variable `syntax-propertize-function’.

This replaces `font-lock-syntactic-keywords’ which is now obsolete.

This allows syntax-table properties to be set independently from font-lock:

just call syntax-propertize to make sure the text is propertized.

Together with this new variable come a new hook

syntax-propertize-extend-region-functions, as well as two helper functions:

syntax-propertize-via-font-lock to reuse old font-lock-syntactic-keywords

as-is; and syntax-propertize-rules which provides a new way to specify

syntactic rules.


If I understand the implication of this change, it should eliminate the explicit font lock requirement and thus propertizing text with syntax table properties can now be done even if font locking is disabled. I think.

New hook post-self-insert-hook run at the end of self-insert-command.


You can now hook each keypress post facto.

Syntax tables support a new “comment style c” additionally to style b.


Useful if your programming mode has a very particular, or complex, comment syntax.

frame-local variables cannot be let-bound any more.


## Major and minor mode changes

`prog-mode’ is a new major mode from which programming modes

should be derived.

`prog-mode-hook’ can be used to enable features for programming

modes, e.g. (add-hook ’prog-mode-hook ’flyspell-prog-mode) to enable

on-the-fly spell checking for comments and strings.


Hopefully this switch will mean the end of programming mode-specific hooks for things that you want to set once, and once only (such as binding `newline-and-indent`

.)

New hook `change-major-mode-after-body-hook’, run by

`run-mode-hooks’ just before any other mode hooks.

Enabled globalized minor modes can be disabled in specific modes,

by running (FOO-mode-hook 0) via a mode hook.


This is a useful change if global minor modes are thrust upon you.

`define-minor-mode’ accepts a new keyword :variable.


This let’s you define the variable name in which to store the state of the minor mode. Historically this name was chosen for you automatically.

`delete-file’ and `delete-directory’ now accept optional arg TRASH.

Trashing is performed if TRASH and `delete-by-moving-to-trash’ are

both non-nil. Interactively, TRASH defaults to t, unless a prefix

argument is supplied (see Trash changes, above).


This change echos the other trash change made earlier.

`facemenu-read-color’ is now an alias for `read-color’.

The command `read-color’ now requires a match for a color name or RGB

triplet, instead of signaling an error if the user provides a invalid

input.

Tool-bars can display separators.

Tool-bar separators are handled like menu separators in menu-bar maps,

i.e. via menu entries of the form `(menu-item “–”)’.


I don’t use the tool bar (who does?) but it’s nice to see functionality like that added to Emacs.

### Image API

Animated images support (currently animated gifs only).


Time to dust off all those animated GIFs from the 90s.

`image-animated-p’ returns non-nil if an image can be animated.

`image-animate’ animates a supplied image spec.

`image-animate-timer’ returns the timer object for an image that

is being animated.

`image-extension-data’ is renamed to `image-metadata’.

If Emacs is compiled with ImageMagick support (see Startup

Changes), the function `imagemagick-types’ returns a list of image

file extensions that your installation of ImageMagick supports. The

function `imagemagick-register-types’ enables ImageMagick support for

these image types, minus those listed in `imagemagick-types-inhibit’.

See the Emacs Lisp Reference Manual for more information.


## XML and HTML parsing

If Emacs is compiled with libxml2 support (which is the default),

two new Emacs Lisp-level functions are defined:

`libxml-parse-html-region’ (which will parse “real world” HTML)

and `libxml-parse-xml-region’ (which parses XML). Both return an

Emacs Lisp parse tree.


The snarky remarks about XML as a poor man’s verbose s-expression have finally come full circle now, with the ability to import xml *and* “real world” HTML to a lisp parse tree. This is actually a surprisingly nifty addition and as I work with xml frequently, a rather welcome one as well. All I need now is proper XPath support.

## GnuTLS

Emacs can be compiled with libgnutls support

This is the default. You will then be able to use the functionality

in gnutls.el, namely the `open-gnutls-stream’ and `gnutls-negotiate’

functions. It’s easiest to use these functions through

`open-network-stream’ because it can upgrade connections through

STARTTLS opportunistically or use plain SSL, depending on your needs.

Only versions 2.8.x and higher or GnuTLS have been tested.

[FIXME: this statement needs clarifying, given that GnuTLS >= 2.6.6

is the test used by configure.]

gnutls-log-level

Set `gnutls-log-level’ higher than 0 to get debug output. 1 is for

important messages, 2 is for debug data, and higher numbers are as per

the GnuTLS logging conventions. The output is in *Messages*.


As mentioned a few times earlier, Emacs can now be compiled with native TLS support.

## Isearch

New hook `isearch-update-post-hook’ that runs in `isearch-update’.


## More Misc Changes

Progress reporters can now “spin”.

The MIN-VALUE and MAX-VALUE arguments of `make-progress-reporter’ can

now be nil, or omitted. This makes a “non-numeric” reporter. Each

time you call `progress-reporter-update’ on that progress reporter,

with a nil or omitted VALUE argument, the reporter message is

displayed with a “spinning bar”.


This is pretty cool. I never knew Emacs had a progress bar feature at all!

New variable `revert-buffer-in-progress-p’ is true while a buffer is

being reverted, even if the buffer has a local `revert-buffer-function’.

New variables `delayed-warnings-list’ and `delayed-warnings-hook’ allow

deferring warnings until the main command loop is executed.

`set-auto-mode’ now respects mode: local variables at the end of files,

as well as those in the -*- line.

rx.el has a new `group-n’ construct for explicitly numbered groups.

keymaps can inherit from multiple parents.


This is a subtle but interesting change: you can now build multiple keymaps and pull the keybindings from both of them. How conflicts are resolved is not explained, though.

`debug-on-event’ lets you debug Emacs when stuck because of inhibit-quit.

New reader macro ## which stands for the empty symbol.

This means that the empty symbol can now be read back. Also, #: by itself

(when not immediately followed by a possible symbol character) stands for

an empty uninterned symbol.


## Obsolete functions and variables

buffer-substring-filters is obsolete.

Use `filter-buffer-substring-functions’ instead.

`byte-compile-disable-print-circle’ is obsolete.

`deferred-action-list’ and `deferred-action-function’ are obsolete.

`font-lock-maximum-size’ is obsolete.


## Changes in Emacs 24.1 on non-free operating systems

New configure.bat option –enable-checking builds Emacs with extra

runtime checks.

New configure.bat option –distfiles to specify files to be

included in binary distribution.

New configure.bat option –without-gnutls to disable automatic

GnuTLS detection.

New configure.bat option –lib for general library linkage, works

with the USER_LIBS build variable.

New make target `dist’ to create binary distribution for MS Windows.

Function `w32-default-color-map’ is now obsolete.

On Nextstep/OSX, the menu bar can be hidden by customizing

ns-auto-hide-menu-bar.


## The End

Phew. That’s *a lot of stuff!* It’s difficult to tell for sure what impact the new additions and changes will have, so we’ll just have to wait and see what people come up with in time.

I think the Emacs maintainers have done a phenomenal job improving the quality of Emacs for us old-timers, and by making tough decisions and aligning Emacs more with modern editors to rope in, and not scare away, new users. Yes, it may well upset a lot of old-timers that this and that changed; good thing, then, that Emacs makes it easy to change things (if you know where to look.)
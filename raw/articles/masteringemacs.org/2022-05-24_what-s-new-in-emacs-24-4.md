---
title: What's New In Emacs 24.4
url: https://www.masteringemacs.org/article/whats-new-in-emacs-24-4
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Well, it’s that time of the year again. There’s a new Emacs minor release due out any day now, and it’s become something of a tradition for me to annotate the NEWS file. Of course, “minor” is a relative term here: this release is full of tweaks and changes and is anything but.

At the time of this writing Emacs 24.4 is in feature freeze; no major changes will get in, but the list of changes you see below is not set in stone – but it almost never changes much. Only if there’s a major bug or issue will items get pulled from the release.

If you’re anxious to get started you’ll have to pull down the source and build Emacs yourself.

Oh, one more thing. I’ve only converted the NEWS file but not reorganized it; some changes appear under the wrong headings in the NEWS file. I haven’t changed that at all.

## What’s New In Emacs 24.4

### Installation Changes in Emacs 24.4

```
Emacs can now be compiled with ACL support.
This happens by default if a suitable support library is found at
build time, like libacl on GNU/Linux. To prevent this, use the
configure option ``--disable-acl``.
```


This is excellent news if your flavor of Linux supports ACL. The

extent of Emacs’s support of ACL is unknown, but I doubt it’s all that

sophisticated yet. It’s unlikely dired will know how to set ACL.

```
Emacs can now be compiled with file notification support.
This happens by default if a suitable system library is found at
build time. To prevent this, use the configure option
``--with-file-notification-no``. See below for file-notify features.
FIXME? This feature is not available for the Nextstep port. (?)
```


Nice. I’ll talk about this further down.

```
The configure option ``--without-compress-info`` has been generalized,
and renamed to ``--without-compress-install``. It now prevents compression
of \_any\_ files during installation.
The configure option ``--with-crt-dir`` has been removed.
It is no longer needed, as the crt\*.o files are no longer linked
specially.
Directories passed to configure option ``--enable-locallisppath`` are
no longer created during installation.
Emacs can be compiled with zlib support.
If this library is present (which it normally is on most systems), the
function ``zlib-decompress-region`` becomes available, which can
decompress gzip- and zlib-format compressed data.
```


More data compression support for Emacs. No word if `auto-compression-mode`

will support it out of the box. I presume so.

```
Emacs for NS (OSX, GNUStep) can be built with ImageMagick support.
pkg-config is required to find ImageMagick libraries.
For OSX >= 10.5, the Core text based font backend from the Mac port is used.
For GNUStep and OSX 10.4 the old backend is used.
To use the old backend by default, do on the command line:
% defaults write org.gnu.Emacs FontBackend ns
```


### Startup Changes in Emacs 24.4

```
When initializing ``load-path``, an empty element in the EMACSLOADPATH
environment variable (either leading, e.g., “:/foo”; trailing, e.g.,
“/foo:”; or embedded, e.g., “/foo::/bar”) is replaced with the default
load-path (the one that would have been used if EMACSLOADPATH was unset).
This makes it easier to \_extend\_ the load-path via EMACSLOADPATH
(previously, EMACSLOADPATH had to specify the complete load-path,
including the defaults). (In older versions of Emacs, an empty element
was replaced by “.”, so use an explicit “.” now if that is what you want.)
```


Great if you’re the sort that sets the emacs load path from the commandline - perhaps to support multiple Emacs setups for different purposes. Beware the last gotcha.

```
The -L option, which normally prepends its argument to load-path,
will instead append, if the argument begins with ``:`` (or ``;`` on MS Windows;
i.e., ``path-separator``).
```


Another potential gotcha if you use the -L option.

```
If you use either site-load.el or site-init.el to customize the dumped
Emacs executable, any changes to ``load-path`` that these files make
will no longer be present after dumping. To affect a permanent change
to ``load-path``, use the ``--enable-locallisppath`` option of ``configure``.
The user option ``initial-buffer-choice`` can now specify a function
to set up the initial buffer.
```


Nice. Now you can make Emacs go fetch the latest dilbert comic and display it whenever you launch your Emacs.

### Changes in Emacs 24.4

```
New option ``gnutls-verify-error``, if non-nil, means that Emacs
should reject SSL/TLS certificates that GnuTLS determines as invalid.
(This option defaults to nil at present, but this is expected to change
in a future release.)
Emacs now supports menus on text-mode terminals.
If the terminal supports a mouse, clicking on the menu bar, or on
sensitive portions of the mode line or header line, will drop down the
menu defined at that position. Likewise, clicking C-mouse-2 or
C-mouse-2 or C-mouse-3 on the text area will pop up the menus defined
for those locations.
If the text terminal does not support a mouse, you can activate the
first menu-bar menu by typing F10, which invokes ``menu-bar-open``.
If you want the previous behavior, whereby F10 invoked ``tmm-menubar``,
customize the option ``tty-menu-open-use-tmm`` to a non-nil value.
(Typing M-\\\` will always invoke ``tmm-menubar``, even if
``tty-menu-open-use-tmm`` is nil.)
```


Great news for beginners of Emacs who mistakenly use Emacs in a terminal instead of in a window manager.

```
The \*Messages\* buffer is created in ``messages-buffer-mode``,
a new major mode, with read-only status. Any code that might create
the \*Messages\* buffer should call the function ``messages-buffer`` to do
so and set up the mode.
Emacs now supports ACLs (access control lists).
Emacs preserves the ACL entries of files when backing up.
```


Very important indeed if you rely on ACL to protect your files.

```
New functions ``file-acl`` and ``set-file-acl`` get and set the ACL
entries of a file. On GNU/Linux, the POSIX ACL interface is used via
libacl. On MS-Windows, the NT Security APIs are used to emulate the
POSIX ACL interfaces.
```


Nice that ACL support works natively with Windows’s as well. The Windows ACL system is extremely advanced and I wonder what sort of concessions were made to keep the interface unified and easy to use.

```
Multi-monitor support has been added.
New functions ``display-monitor-attributes-list`` and
``frame-monitor-attributes`` can be used to obtain information about
each physical monitor on multi-monitor setups.
```


Interesting that Emacs has added support for multiple monitors. What the extent of this is – spanning a frame across multiple monitors, perhaps? – is currently unknown.

```
The functions ``display-pixel-width`` and ``display-pixel-height`` now
behave consistently among the platforms: they return the pixel width
or height for all physical monitors associated with the given display
as just they were on X11. To get information for each physical
monitor, use the new functions above. Similar notes also apply to
``x-display-pixel-width``, ``x-display-pixel-height``, ``display-mm-width``,
``display-mm-height``, ``x-display-mm-width``, and ``x-display-mm-height``.
```


This is potentially very important for packages like pos-tip that constructs a nice tooltip replacement for Emacs and thus needs to know where and how to draw itself.

```
The cursor stops blinking after 10 blinks (by default) on X and NS.
You can change the default by customizing ``blink-cursor-blinks``.
```


I wonder how many surveys, usability studies, committee meetings and research went into deciding it must be ten blinks and not nine or eleven. I personally disable blinking carets/cursors everywhere.

```
In keymaps where SPC scrolls forward, S-SPC now scrolls backward.
This affects View mode, etc.
```


Useful, and a similar mnemonic to alt+tab / shift+alt+tab for task switching.

#### Help changes

```
The command ``apropos-variable`` is renamed to ``apropos-user-option``.
``apropos-user-option`` shows all user options while ``apropos-variable``
shows all variables. When called with a universal prefix argument,
the two commands swap their behaviors. When ``apropos-do-all`` is
non-nil, they output the same results.
```


Useful for people who only want customize options displayed, and with a switch to re-enable the old behavior.

`The key ``?`` now describes prefix bindings, like ``C-h``.`


Excellent. I can’t think of any prefix bindings that uses `?`

.

```
The command ``quail-help`` is deleted. Use ``C-h C-\``
(``describe-input-method``) instead.
```


#### Frame and window changes

```
New commands ``toggle-frame-fullscreen`` and ``toggle-frame-maximized``,
bound to <f11> and M-<f10>, respectively.
```


This is probably a big win for a lot of people. I wrote an article on how to maximize Emacs on startup. The fact the topic needs mentioning at all is a testament to how complicated it is to get consistent behavior on every platform.

Not too sure about the key bindings though.

```
New command ``frameset-to-register`` is now bound to ``C-x r f``, replacing
``frame-configuration-to-register``. It offers similar functionality,
plus enhancements like the ability to restore deleted frames. The
command ``frame-configuration-to-register`` still exists, but is unbound.
```


Great news if you use register configurations a lot for windows or frames. Its use is perhaps of greater importance to package writers.

```
New hooks ``focus-in-hook``, ``focus-out-hook``.
These are normal hooks run when an Emacs frame gains or loses input focus.
```


I look forward to seeing what people will use this for!

```
``split-window`` is now a non-interactive function, not a command.
As a command, it was a special case of ``C-x 2`` (``split-window-below``),
and as such superfluous. After being reimplemented in Lisp, its
interactive form was mistakenly retained.
```


Unlikely that too many people call this command directly.

```
New option ``scroll-bar-adjust-thumb-portion``.
Available only on X, this option allows to control over-scrolling
using the scroll bar (i.e. dragging the thumb down even when the end
of the buffer is visible).
```


#### Lisp evaluation changes

```
``eval-defun`` on an already defined defcustom calls the :set function,
if there is one.
A zero prefix arg of ``eval-last-sexp`` (``C-x C-e``),
``eval-expression`` (``M-:``) and ``eval-print-last-sexp`` (``C-j``) inserts
a list with no limit on its length and level (by using nil values of
``print-length`` and ``print-level``), and inserts additional formats for
integers (octal, hexadecimal, and character).
```


That’s very handy!

```write-region-inhibit-fsync`` now defaults to t in batch mode.`


This should speed up batch calls at the cost of some data loss if the writes haven’t been flushed to disk yet.

```
``cache-long-line-scans`` has been renamed to ``cache-long-scans``
because it affects caching of paragraph scanning results as well.
The option ``set-mark-default-inactive`` has been deleted.
This unfinished feature was introduced by accident in Emacs 23.1;
simply disabling Transient Mark mode does the same thing.
The default value of ``comment-use-global-state`` is changed to t,
and this variable has been marked obsolete.
```


#### New user options

```
``read-regexp-defaults-function`` defines a function to read regexps,
used by commands like ``rgrep``, ``lgrep`` ``occur``, ``highlight-regexp``,
etc. You can customize this to specify a function that provides a
default value from the regexp last history element, or from the symbol
found at point.
```


This is great news for package authors as you had to roll your own prompt and make sure you pointed to a shared history varaible, etc. - this is a massive timesaver and should make it easier for Emacs hackers to override how they enter regexps.

```
``load-prefer-newer``, affects how the ``load`` function chooses the
file to load. If this is non-nil, then when both .el and .elc
versions of a file exist, and the caller did not explicitly specify
which one to load, then the newer file is loaded. The default, nil,
means to always load the .elc file.
```


### Editing Changes in Emacs 24.4

#### Indentation changes

```
The behavior of ``C-x TAB`` (``indent-rigidly``) has changed.
When invoked without a prefix argument, it now activates a transient
mode in which typing <left>, <right>, <S-left>, and <S-right> adjusts
the text indentation in the region. Typing any other key resumes
normal editing behavior.
```


By default it would indent by ARG (usually 1 column) but this is more in line with what people might expect coming from other text editors, and it marks a shift towards a more “heavy weight” and inclusive transient mark mode, which I think is a good thing.

```electric-indent-mode`` is enabled by default.`


Contentious. I found it hard to tame this beast when it was first introduced and its behavior, while flexible, left some things to be desired. This goes for the other electric modes as well, like `electric-pair-mode`

.

```
``tab-stop-list`` is now implicitly extended to infinity by repeating
the last step. Its default value is changed to nil which means a tab
stop every ``tab-width`` columns.
```


I nixed tab-stop-list and all that stuff ages ago as it just got in the way, exactly for the reasons outlined above. (That and a general aversion to having tab characters in my files.) This at least makes its behavior consistent.

#### Filling changes

```
New command ``cycle-spacing`` cycles between spacing conventions:
having just one space, no spaces, or reverting to the original
spacing. Like ``just-one-space``, it can handle or ignore newlines and
leave different number of spaces.
```


Useful function, but between `just-one-space`

and `delete-blank-lines`

I find they cover my needs fully. I’ll have to try to work cycle-spacing into my workflow - but as it’s not bound to a key it’ll most likely never get used.

```
``fill-single-char-nobreak-p`` prevents fill from breaking a line after
a 1-letter word, which is an error according to Polish and
Czech typography rules. To globally enable this feature, evaluate:
(add-hook ’fill-nobreak-predicate ’fill-single-char-nobreak-p)
```


Good news for people of Polish or Czech persuasion.

`Uniquify is enabled by default with ``post-forward-angle-brackets`` style.`


Yay.

```
New command ``C-x SPC`` (``rectangle-mark-mode``) makes a rectangular region.
Most commands are still unaware of it, but kill/yank do work on the rectangle.
```


Like I mentioned earlier - this is a move towards a more unified and inclusive transient mark mode. The rectangle stuff in Emacs kind-of works with transient (in that it only cares about point and mark, and not the highlighted transient mark region) – but with this, CUA-mode’s only advantage over TMM is finally gone?

```
New option ``visual-order-cursor-movement``.
If this is non-nil, cursor motion with arrow keys will follow the
visual order of characters on the screen: <left> always moves to the
left, <right> always moves to the right, disregarding the surrounding
bidirectional context.
```


#### Register changes

```
All register commands can now show help with preview.
New command ``C-x C-k x`` (``kmacro-to-register``) stores keyboard
macros in registers.
```


Potentially useful; but you can already cycle the macro ring with `kmacro-cycle-ring-<next/previous>`

so its use is limited.

```
New command ``C-x r f`` (``frameset-to-register``).
See Changes in Emacs 24.4, above.
New command ``delete-duplicate-lines``.
When its arg ADJACENT is non-nil (when called interactively with C-u
C-u) it works like the utility ``uniq``. Otherwise by default it
deletes duplicate lines everywhere in the region without regard to
adjacency. When its arg KEEP-BLANKS is non-nil (when called
interactively with C-u C-u C-u), duplicate blank lines are preserved.
```


This is a *great* addition for those of us who do a lot of text munging in Emacs. It’s also one more thing Emacs can do without custom Elisp or a call to a shell command.

### Changes in Specialized Modes and Packages in Emacs 24.4

```
More packages look for ~/.emacs.d/<foo> additionally to ~/.<foo>.
Affected files:
~/.emacs.d/timelog replaces ~/.timelog
~/.emacs.d/vip replaces ~/.vip
~/.emacs.d/viper replaces ~/.viper
~/.emacs.d/ido.last replaces ~/.ido.last
~/.emacs.d/kkcrc replaces ~/.kkcrc
~/.emacs.d/quickurls replaces ~/.quickurls
~/.emacs.d/idlwave replaces ~/.idlwave
~/.emacs.d/bdfcache.el replaces ~/.bdfcache.el
~/.emacs.d/places replaces ~/.emacs-places
~/.emacs.d/shadows replaces ~/.shadows
~/.emacs.d/shadow\_todo replaces ~/.shadow\_todo
~/.emacs.d/strokes replaces ~/.strokes
~/.emacs.d/notes replaces ~/.notes
~/.emacs.d/type-break replaces ~/.type-break
Also the following files used by the now obsolete otodo-mode.el:
~/.emacs.d/todo-do replaces ~/.todo-do
~/.emacs.d/todo-done replaces ~/.todo-done
~/.emacs.d/todo-top replaces ~/.todo-top
```


This should end Emacs clogging your home directory with crap. That’s a good thing!

#### Backtrace and debugger

```
The Lisp debugger’s ``e`` command now includes the lexical environment
when evaluating the code in the context at point. Hence, it now lets
you access lexical variables.
```


As we move towards lexical scoping, for all the pros and cons of doing so, this will undoubtedly be useful in tracking down pesky scoping issues.

`New command ``v`` (``debugger-toggle-locals``) displays local vars.`


A sorely missed feature of most debuggers finally arrives in Emacs.

```
New minor mode ``jit-lock-debug-mode`` lets you use the debuggers on
code run via JIT Lock.
```


#### Battery

`Battery information via the BSD ``apm`` utility is now supported.`


#### Buffer Menu

```M-s a C-o`` shows lines matching a regexp in marked buffers using Occur.`


#### Calendar and Diary

```
New faces ``calendar-weekday-header``, ``calendar-weekend-header``,
and ``calendar-month-header``.
New option ``calendar-day-header-array``.
New variable ``diary-from-outlook-function``, used by the command
``diary-from-outlook``.
The variable ``calendar-font-lock-keywords`` is obsolete.
```


#### Calc

```
Calc by default now uses the Gregorian calendar for all dates, and
uses January 1, 1 AD as its day number 1. Previously Calc used the
Julian calendar for dates before September 14, 1752, and it used
December 31, 1 BC as its day number 1; the new scheme is more
consistent with Calendar’s calendrical system and day numbering.
The new variable ``calc-gregorian-switch`` lets you configure the
date when Calc switches from the Julian to the Gregorian calendar.
Nil, the default value, means to always use the Gregorian calendar.
The value (YEAR MONTH DAY) means to start using the Gregorian calendar
on the given date.
Support for ISO 8601 dates.
```


Dates and time is one thing calc never handled too well. It could do with a lot more functions to manipulate time and date.

#### CEDET

##### EDE

```
The cpp-root project now supports executing a compile command.
It can be set through the new :compile-command slot or the
buffer-local variable ``compile-command``.
Better selection of include directories for the ‘linux’ project.
Include directories now support out-of-tree build directories and
target architecture auto-detection.
```


##### Semantic

```
Improved detection of used namespaces in current scope in C++.
Parsing of default values for variables and function arguments in C/C++.
They are also displayed by the summarize feature in the modeline.
Improved parsing of function pointers in C/C++.
This also includes parsing of function pointers as function arguments.
Parsing of C/C++ preprocessor macros which open new scope.
For example, this enables parsing of macros which open new namespaces.
Support for ‘this’ pointer in inline member functions in C++.
```


#### cl-lib

```
New macro ``cl-tagbody``.
letf is now just an alias for cl-letf.
```


#### CUA mode

```
CUA mode now uses ``delete-selection-mode`` and ``shift-select-mode``.
Hence, you can now enable it independently from ``transient-mark-mode``,
``delete-selection-mode``, and ``shift-select-mode``.
``cua-highlight-region-shift-only`` is now obsolete.
You can disable ``transient-mark-mode`` to get the same result.
CUA’s rectangles can now be used via ``cua-rectangle-mark-mode``.
```


So now we have two; the old way of doing proper rectangles (via CUA) and a newer way via `rectangle-mark-mode`

. Here’s to hoping that one day we’ll just have one mode.

#### CFEngine mode

```
Support for completion, ElDoc, and Flycheck has been added.
The current CFEngine syntax is parsed from “cf-promises -s json”.
There is a fallback syntax available if you don’t have cf-promises or
if it doesn’t support that option.
Delete Selection mode can now be used without ``transient-mark-mode``.
```


#### Desktop

```
``desktop-auto-save-timeout`` defines the number of seconds idle time
before auto-save of the desktop.
``desktop-restore-frames``, enabled by default, allows saving and
restoring the frame/window configuration (frameset). Additional options
``desktop-restore-in-current-display``, ``desktop-restore-reuses-frames``
and ``desktop-restore-forces-onscreen`` offer further customization.
```


This is no doubt the end goal for adding frameset marshalling to Emacs - so desktop, et al. can restore it correctly. Great news indeed.

#### Dired

`New minor mode ``dired-hide-details-mode`` hides details.`


For when details must be obscured.

`Eldoc Mode works properly in the minibuffer.`


#### Electric Pair mode

```
New ``electric-pair-preserve-balance`` enabled by default.
Pairing/skipping only kicks in when that help the balance of
parentheses and quotes, i.e. the buffer should end up at least as
balanced as before.
You can further control this behaviour by adjusting the predicates
stored in ``electric-pair-inhibit-predicate`` and
``electric-pair-skip-self``.
```


Hopefully this works “as intended” without creating more headaches than it tries to cure.

```
New ``electric-pair-delete-adjacent-pairs`` enabled by default.
In ``electric-pair-mode``, the commands ``backward-delete-char`` and
``backward-delete-char-untabify`` are now bound to electric variants
that delete the closer when invoked between adjacent pairs.
```


As before, this is a great change and one I’ve been using for a long time by advising backward-kill-word.

```
New ``electric-pair-open-newline-between-pairs`` enabled by default.
In ``electric-pair-mode``, inserting a newline between adjacent pairs
opens an extra newline after point, which is indented if
``electric-indent-mode`` is also set.
```


One of the problems I had with electric-pair-mode is that it lacked support for a lot of the language-specific syntax quirks when it came to paired characters. These additions should go a long way towards fixing them all.

```
New ``electric-pair-skip-whitespace`` enabled by default.
Controls if skipping over closing delimiters should jump over any
whitespace slack. Setting it to ``chomp`` makes it delete this
whitespace. See also the variable
``electric-pair-skip-whitespace-chars``.
New variables control the pairing in strings and comments.
You can customize ``electric-pair-text-pairs`` and
``electric-pair-text-syntax-table`` to tweak pairing behaviour inside
strings and comments.
```


#### EPA

```
New option ``epa-mail-aliases``.
You can set this to a list of alias expansions for keys to use
in ``epa-mail-encrypt``.
If one element of the variable’s value is (“foo@bar.com” “foo@hello.org”),
that means: when one of the recipients of the message being encrypted
is ``foo@bar.com``, encrypt the message for ``foo@hello.org`` instead.
If one element of the variable’s value is (“foo@bar.com”),
that means: when one of the recipients of the message being encrypted
is ``foo@bar.com``, ignore that name as regards encryption.
This is useful to avoid a query when you have no key for that name.
```


#### ERC

```
New option ``erc-accidental-paste-threshold-seconds``.
If set to a number, this can be used to avoid accidentally paste large
amounts of data into the ERC input.
```


Built-in client-side flood detection. Very handy.

#### ERT

```
New macro ``skip-unless`` allows skipping ERT tests.
See the ERT manual for details.
```


#### Eshell

```
``eshell`` now supports visual subcommands and options
Eshell has been able to handle “visual” commands (interactive,
non-line oriented commands such as top that require display
capabilities not provided by eshell) by running them in an Emacs
terminal emulator. See ``eshell-visual-commands``.
This feature has been extended to subcommands and options that make a
usually line-oriented command a visual command. Typical examples are
“git log” and "git –help" which display their output in a
pager by default. See ``eshell-visual-subcommands`` and
``eshell-visual-options``.
```


The first part – using a terminal emulator – is a big change for eshell users. Beforehand it kind of did something of the same but not nearly as well; by using ansi-term you get to have your cake and eat it. Still, it’d be great to see terminal emulation built into eshell.

Speaking of subcommands and options: disabling $PAGER completely in `shell`

or `eshell`

is much better. Emacs is a far better pager than any external program will ever be.

```
Added Eshell-Tramp module
External su and sudo commands are now the default; the internal,
Tramp-using variants can still be used by enabling the eshell-tramp
module.
```


TRAMP is awesome but it can be temperamental. By using the proper external ones the woes some of you experience should end.

#### F90 mode

```
New option ``f90-smart-end-names``.
Icomplete is a bit more like Ido. Key bindings to navigate through and select the completions.
The icomplete-separator is customizable, and its default has changed.
Removed icomplete-show-key-bindings.
Icomplete-mode by defaults applies to all forms of minibuffer completion.
(setq icomplete-with-completion-tables ’(internal-complete-buffer))
will revert to the old behavior.
```


This is part of a larger push to render the default completion engine redundant and replace it with a cross between IDO and iswitchb. This is generally a good move, I believe; switching buffers without ido or iswitchb is tedious at best. Adding to that, IDO has its own quirks and a re-implementation might be in hand. I might just give icomplete a whirl instead of IDO now.

#### Ido

`Ido has a manual now.`


Alternatively you can read my article: Introduction to Ido Mode.

```
``ido-use-virtual-buffers`` takes a new value ’auto.
``ido-decorations`` has been slightly extended to give a bit more control.
```


#### Image mode

```
New commands ``n`` (``image-next-file``) and ``p`` (``image-previous-file``)
visit the next image file and the previous image file in the same
directory, respectively.
```


And with one fell swoop Emacs becomes a much better image browser.

```
New commands to show specific frames of multi-frame images.
``f`` (``image-next-frame``) and ``b`` (``image-previous-frame``) visit the
next or previous frame. ``F`` (``image-goto-frame``) shows a specific frame.
```


I just tested this functionality and it works great on GIFs.

Find subliminal messages hidden in all those lolcat GIFs you watch.

```
New commands to speed up, slow down, or reverse animation.
The command ``image-mode-fit-frame`` deletes other windows.
When toggling, it restores the frame’s previous window configuration.
It also has an optional frame argument, which can be used by Lisp
callers to fit the image to a frame other than the selected frame.
```


#### Hi-Lock

```
New option ``hi-lock-auto-select-face``. When non-nil, hi-lock commands
will cycle through faces in ``hi-lock-face-defaults`` without prompting.
```


Oh yes. Thank you. This will automatically pick a highlight face for you instead of you having to select it. Very useful.

```
New global command ``M-s h .`` (``highlight-symbol-at-point``)
highlights the symbol found near point without prompting,
using the next face automatically.
```


Another timesaver.

#### Imenu

`New option ``imenu-generic-skip-comments-and-strings``.`


Avoids false positives from having function/method definitions in comments or strings.

#### Info

```
New face ``info-index-match`` is used to highlight matches in index
entries displayed by ``Info-index-next``, ``Info-virtual-index`` and
``info-apropos``.
```


#### JS Mode

```
Better indentation of multiple-variable declarations.
If declaration spans several lines, variables on the following lines
are lined up to the first one.
We now recognize and better indent continuations in array
comprehensions.
New option ``js-switch-indent-offset`.``
MH-E has been updated to MH-E version 8.5.
See MH-E-NEWS for details.
```


#### Octave mode

:

```
Font locking for texinfo comments and new keywords
Completion in Octave file buffers
Eldoc support
Jump to definition
Documentation lookup/search
Code cleanup and various bug fixes
OPascal mode is the new name for Delphi mode.
All delphi-\* variables and functions have been renamed to opascal-\*.
\`delphi-newline-always-indents is not supported any more.
Use ``electric-indent-mode`` instead.
``delphi-tab`` is gone, replaced by ``indent-for-tab-command``.
```


#### Package

```
The format of ``archive-contents`` files, generated by package
repositories, has changed to allow a new (fifth) element in the data
vectors, containing an associative list with extra properties.
``describe-package`` buffer uses the ``:url`` extra property to
display a ``Homepage`` header, if it’s present.
```


Sorely needed.

```
In the buffer produced by ``describe-package``, there are now buttons
listing the keywords related to that package. You can click on them
to see other packages related to any given keyword.
In the \*Packages\* buffer, ``f`` or the Package->Filter menu filters
the packages by a keyword.
```


#### Prolog mode

```
``prolog-use-smie`` has been removed, along with the non-SMIE
indentation code.
```


#### Remember

```
The new command ``remember-notes`` creates a buffer which is saved
on ``kill-emacs``.
You may think of it as a \*scratch\* buffer whose content is preserved.
In fact, it was designed as a replacement for \*scratch\* buffer and can
be used that way by setting ``initial-buffer-choice`` to
``remember-notes`` and ``remember-notes-buffer-name`` to “\*scratch\*”.
Without the second change, \*scratch\* buffer will still be there for
notes that do not need to be preserved.
The Remember package can now store notes in separates files.
You can use the new function ``remember-store-in-files`` within the
``remember-handler-functions`` option.
See ``remember-data-directory`` and ``remember-directory-file-name-format``
for new options related to this function.
```


#### Rmail

```
Customize ``rmail-mbox-format`` to influence some minor aspects of
how Rmail displays non-MIME messages.
The ``unrmail`` command now converts from BABYL to mboxrd format,
rather than mboxo. Customize ``unrmail-mbox-format`` to change this.
```


#### Ruby mode

```
New option ``ruby-encoding-magic-comment-style``.
New option ``ruby-custom-encoding-magic-comment-template``.
New mode menu.
Improved syntax highlighting and indentation.
Add more Ruby file types to ``auto-mode-alist``.
New option ``ruby-align-to-stmt-keywords``.
New ``electric-indent-mode`` integration.
```


#### Search and Replace

```
New global command ``M-s .`` (``isearch-forward-symbol-at-point``)
starts a symbol (identifier) incremental search forward with the
symbol found near point added to the search string initially.
```


About time. Isearch is great and all but this was a missing step. I still recommend you use my Smart Scan package though. (It’s on MELPA.)

```
``C-x 8 RET`` in Isearch mode reads a character by its Unicode name
and adds it to the search string.
```


Good. It was awkward having to do it outside isearch; you’d need recursive minibuffers to then insert it with registers if you also wanted to yank stuff.

```
``M-s i`` in Isearch mode toggles the variable ``isearch-invisible``
between nil and the value of the option ``search-invisible`` (or ``open``
when it’s nil).
``query-replace`` skips invisible text when ``search-invisible`` is nil,
and opens overlays with hidden text when ``search-invisible`` is ``open``.
A negative prefix arg of replacement commands replaces backward.
``M-- M-%`` replaces a string backward, ``M-- C-M-%`` replaces a regexp
backward, ``M-s w words M-- M-%`` replaces a sequence of words backward.
```


Useful for macros if you rely on point/mark to do your replacing and not just TMM.

```
By default, prefix arguments do not now terminate Isearch mode.
Set ``isearch-allow-prefix`` to nil to restore old behavior.
More Isearch commands accept prefix arguments, namely
``isearch-printing-char``, ``isearch-quote-char``, ``isearch-yank-word``,
``isearch-yank-line``.
Word search now matches whitespace at the beginning/end
of the search string if it contains leading/trailing whitespace.
In an incremental word search or when using a non-nil LAX argument
of ``word-search-regexp``, the lax matching can also match part of
the first word (in addition to the lax matching of the last word).
The same rules are now applied to the symbol search with the difference
that it matches symbols, and non-symbol characters between symbols.
```


This should make it easier to find all those search strings delimited by an artibtrary amount of spacing.

#### SES

`New command ``ses-rename-cell`` allows assigning names to SES cells.`


#### Shell

```
``explicit-bash-args`` now always defaults to use –noediting.
During initialization, Emacs no longer expends a process to decide
whether it is safe to use Bash’s –noediting option. These days
–noediting is ubiquitous; it was introduced in 1996 in Bash version 2.
```


A bit of house keeping. Always nice.

#### Shell Script mode

```
``sh-mode`` now has the mode own ``add-log-current-defun-function``.
You can pick the name of the function and the variables with ``C-x 4 a``.
```


If you use sh-mode and ChangeLog files, this is for you.

```
The SMIE indentation engine is now used by default.
SMIE indentation can be customized via ``smie-config``.
The customization can be guessed by Emacs by providing a sample indented
file and letting SMIE learn from it.
```


This is actually a really cool indentation engine that was added in Emacs 23 I believe.

#### Term mode

`New option ``term-suppress-hard-newline``.`


**UPDATE:** This fixes the annoying issue in Emacs’s terminal emulator where the text would not wrap like a normal terminal would. Emacs used to hard break if the text exceeded the size of the original window - but now it won’t.

```
Todo mode has been rewritten and enhanced.
New features include:
- support for multiple todo files and archive files of done items;
- renaming, reordering, moving, merging, and deleting categories;
- sortable tabular summaries of categories and the types of items they contain;
- cross-category lists of items filtered by specific criteria;
- more fine-grained interaction with the Emacs diary, by being able to decide
for each todo item whether it appears in the Fancy Diary display;
- highly flexible new item insertion and item editing;
- moving items between categories, storing done items in their category or in
archive files, undoing or unarchiving done items;
- reprioritizing items by inputting a numerical priority;
- extensive customizability of operation and display, including numerous faces.
The Todo mode user manual describes all commands and most user options.
To support some of these features, a new file format is used, which is
incompatible with the old format; however, you can convert old todo and done
item files to the new format on initializing the first new todo file, or at any
later time with the provided conversion command. The old version of
todo-mode.el has been made obsolete and renamed otodo-mode.el.
```


I’ve never used todo-mode, having always preferred orgmode for this. Perhaps I’ll take a look now that it has been given a major revamp.

```
trace-function was largely rewritten.
New features include:
- no prompting for the destination buffer, unless a prefix-arg was used.
- additionally to prompting for a destination buffer, when a prefix-arg is
used, the user can enter a “context”, i.e. Lisp expression whose value at the
time the function is entered/exited will be printed along with the function
name and arguments. Useful to trace the value of (current-buffer) or
(point) when the function is invoked.
```


#### Tramp

```
The experimental url syntax for remote file names is withdrawn.
New connection method “adb”, which allows to access Android
devices by the Android Debug Bridge. The variable ``tramp-adb-program``
can be used to adapt the path of the “adb” program, if needed.
```


Very cool news for Android hackers.

```
The connection methods “plink1”, “ssh2”, “ssh2”, “scp1”, “scp2”,
“scpc” and “rsyncc” are discontinued. The ssh option
“ControlMaster=auto” is set automatically in all ssh-based methods,
when possible.
Handlers for ``file-acl`` and ``set-file-acl`` for remote machines
which support POSIX ACLs.
```


Impressive that ACL support also works for remote files.

```
Handlers for ``file-notify-add-watch`` and ``file-notify-rm-watch``
for remote machines which support filesystem notifications.
```


This is a big one for me; `auto-revert-tail-mode`

is fantastic but over TRAMP it made many requests - hopefully this will cut down on unnecessary requests.

#### VC and related modes

```
In VC directory mode, ``D`` displays diffs between VC-controlled
whole tree revisions.
In VC directory mode, ``L`` lists the change log for the current VC
controlled tree in a window.
In VC directory mode, ``I`` shows a log of changes that will be
received with a pull operation.
``C-x v G`` (globally) and ``G`` (in VC directory mode) ignores a file
under current version control system. When called with a prefix
argument, you can remove a file from the ignored file list.
```


Very useful if you’re a heavy user of VC like I am.

```
``cvs-append-to-ignore`` has been renamed to ``vc-cvs-append-to-ignore``
because it is moved to vc-cvs.el.
```


#### VHDL mode

```
New options: ``vhdl-actual-generic-name``, ``vhdl-beautify-options``.
New commands: ``vhdl-fix-statement-region``, ``vhdl-fix-statement-buffer``.
```


#### Woman

```
The commands ``woman-default-faces`` and ``woman-monochrome-faces``
are obsolete. Customize the ``woman-*`` faces instead.
```


#### Obsolete packages:

```
Iswitchb is made obsolete by icomplete-mode.
longlines.el is obsolete; use visual-line-mode instead.
sup-mouse.el.
terminal.el is obsolete; use term.el instead.
The previous version of todo-mode.el is obsolete and renamed otodo-mode.el.
xesam.el.
yow.el is obsolete; use fortune.el or cookie1.el instead.
The Info-edit command is obsolete. Editing Info nodes by hand
has not been relevant for some time.
```


### New Modes and Packages in Emacs 24.4

```
New package ``eww`` is a built-in web browser.
It is only available if Emacs is compiled with libxml2 support.
```


Wow! This is great. w3m was a major pain in the neck to get working right sometimes, and it was never really that good. This browser actually does a pretty good job. It renders images, tables and most HTML elements. A perfectly adequate alternative for most browsers if all you want to do is read text. Combine it with a web-based RSS reader or a site like readability and you’re in business! It does a pretty good job rendering this blog.

```
New minor mode ``superword-mode``, defined in subword.el
``superword-mode`` overrides the default word motion commands to treat
symbol\_words as a single word, similar to what ``subword-mode`` does and
using the same internal functions.
```


A nice addition indeed. `subword-mode`

is great for camelCase languages.

```
New package nadvice.el offers lighter-weight advice facilities.
It is layered as:
- add-function/remove-function which can be used to add/remove code on any
function-carrying place, such as process-filters or ``<foo>-function`` hooks.
- advice-add/advice-remove to add/remove a piece of advice on a named function,
much like ``defadvice`` does.
```


Both `add/remove-function`

looks very useful.

```
New package frameset.el.
It provides a set of operations to save a frameset (the state of all
or a subset of the existing frames and windows, somewhat similar to a
frame configuration), both in-session and persistently, and restore it
at some point in the future.
New package filenotify.el provides an interface for file system
notifications. It requires that Emacs be compiled with one of the
low-level libraries gfilenotify.c, inotify.c or w32notify.c.
```


Excellent for people who rely on external tools to update files they’re editing or generally interested in.

### Incompatible Lisp Changes in Emacs 24.4

```
``kill-region`` lost its ``yank-handler`` optional argument.
``(input-pending-p)`` no longer runs other timers which are ready to
run. The new optional CHECK-TIMERS param allows for the prior behavior.
``defvar`` and ``defcustom`` in a let-binding affect the “external” default.
The syntax of ?» and ?« is now punctuation instead of matched parens.
Some languages match those as »…« and others as «…» so better stay neutral.
In compiled Lisp files, the header no longer includes a timestamp.
```


This is probably to avoid tripping up source control systems?

```
The default file coding for Emacs Lisp files is now utf-8.
(See ``file-coding-system-alist``.) In most cases, this change is
transparent, but files that contain unusual characters without
specifying an explicit coding system may fail to load with obscure
errors. You should either convert them to utf-8 or add an explicit
``coding:`` cookie.
```


A sane default for most of us, I think.

```
``overriding-terminal-local-map`` no longer replaces the local keymaps.
It used to disable the minor mode, major mode, and text-property keymaps,
whereas now it simply has higher precedence.
Default process filters and sentinels are not nil any more.
Instead they default to a function which does what the nil value used to do.
``read-event`` does not return decoded chars in ttys any more.
As was the case in Emacs 22 and before, the decoding of terminal
input, according to ``keyboard-coding-system``, is not performed in
``read-event`` any more. But unlike in Emacs 22, this decoding is still
done before input-decode-map, function-key-map, etc.
Removed ``inhibit-local-menu-bar-menus``.
Frame-local variables that affect redisplay do not work any more.
More specifically, the redisplay does not bother to check for a frame-local
value when looking up variables.
nil and “unbound” are indistinguishable in ``symbol-function``.
``symbol-function`` does not signal a ``void-function`` error any more.
To determine if a symbol’s function definition is void, use ``fboundp``.
``defadvice`` does not honor the ``freeze`` flag and cannot advise
special-forms any more.
``dolist`` no longer binds VAR while evaluating the RESULT form,
when lexical binding is enabled. Previously, VAR was bound to nil,
which often led to spurious unused-variable warnings.
The return value of ``backup-buffer`` has changed.
The second argument is no longer an SELinux context, instead it is an
alist of extended attributes as returned by the new function
``file-extended-attributes``. The attributes can be applied to another
file using ``set-file-extended-attributes``.
``visited-file-modtime`` now returns -1 for nonexistent files.
Formerly it returned a list (-1 LOW USEC PSEC), but this was ambiguous
in the presence of files with negative time stamps.
The cars of the elements in ``interpreter-mode-alist`` are now
treated as regexps rather than literal strings.
```


### Lisp Changes in Emacs 24.4

`The second argument of ``eval`` can now specify a lexical environment.`


This could have interesting applications for evaluating code with different contexts - perhaps as part of a greater push for concurrency ?

```
New functions ``special-form-p`` and ``macrop``.
New macro ``define-alternatives`` can be used to define generic commands.
Generic commands are interactive functions whose implementation can be
selected among several alternatives, as a matter of user preference.
The ``defalias-fset-function`` property lets you catch ``defalias``
calls, and redirect them to your own function, instead of ``fset``.
Docstrings can be made dynamic by adding a ``dynamic-docstring-function``
text-property on the first char.
New variable ``enable-dir-local-variables``.
Directory-local variables are ignored if this is nil. This may be
useful for modes that want to ignore directory-locals while still
respecting file-local variables.
New function ``get-pos-property``.
```


#### Completion changes

```
The separator for ``completing-read-multiple`` can now be a regexp.
The default separator has been changed to allow surrounding spaces
around the comma.
The ``common-substring`` arg of ``display-completion-list`` is obsolete.
Either use ``completion-all-completions``, which returns highlighted
strings (including for partial or substring completion), or call
``completion-hilit-commonality`` to add the highlight.
```


#### Terminal changes

```
Functions to pop up menus and dialogs now work on all terminals,
including TTYs. This includes ``x-popup-menu``, ``x-popup-dialog``,
``message-box``, ``yes-or-no-p``, etc.
The function ``display-popup-menus-p`` will now return non-nil for a
display or frame whenever a mouse is supported on that display or
frame.
New hook ``tty-setup-hook``.
New hook ``pre-redisplay-function``.
New bool-vector set operation functions:
``bool-vector-exclusive-or``
``bool-vector-union``
``bool-vector-intersection``
``bool-vector-set-difference``
``bool-vector-not``
``bool-vector-subsetp``
``bool-vector-count-consecutive``
``bool-vector-count-population``
```


Helper functions - always a good thing.

`Comparison functions =, <, >, = now take many arguments.`


Ah yes - that’s a nice change.

`Error-handling changes`


No idea what?

```
New function ``define-error``.
``with-demoted-errors`` takes an additional argument ``format``.
New macro with-eval-after-load. Like eval-after-load, but better behaved.
New library subr-x.el for misc helper functions
``hash-table-keys``
``hash-table-values``
``string-blank-p```
\`string-empty-p\`
\`string-join\`
\`string-reverse\`
\`string-trim-left
``string-trim-right``
``string-trim``
``string-remove-prefix``
``string-remove-suffix``
```


More functions for manipulating strings?! Awesome! This is one part Elisp is sorely lacking. A large part is perhaps that if you want to manipulate strings you should use a buffer (advice I agree with, by the way) – but sometimes it’s just not that simple.

```
Obsoleted functions:
``log10``
``dont-compile``
``lisp-complete-symbol``
``field-complete``
``minibuffer-completion-contents``
``isearch-nonincremental-exit-minibuffer``
``isearch-filter-visible``
``generic-make-keywords-list``
``get-upcase-table`` (use ``case-table-get-table`` instead).
``with-wrapper-hook`` is obsoleted by ``add-function``.
The few hooks that used with-wrapper-hook are replaced as follows:
``abbrev-expand-function`` obsoletes ``abbrev-expand-functions``.
``completion-in-region-function`` obsoletes ``completion-in-region-functions``.
``filter-buffer-substring-function`` obsoletes ``filter-buffer-substring-functions``.
``byte-compile-interactive-only-functions`` is now obsolete.
It has been replaced by the symbol property ’interactive-only.
``split-string`` now takes an optional argument TRIM.
The value, if non-nil, is a regexp that specifies what to trim from
the start and end of each substring.
```


This makes split-string all the more useful

`New function ``string-suffix-p``.`


Nice.

#### File-handling changes

```
Support for filesystem notifications.
Emacs now supports notifications of filesystem changes, such as
creation, modification, and deletion of files. This requires the
``glib`` API, or the ‘inotify’ API (on GNU/Linux systems only). On
MS-Windows systems, this is supported for Windows XP and newer
versions.
```


Cross platform support. Very good.

```
The 9th element returned by ``file-attributes`` is now unspecified.
Formerly, it was t if the file’s gid would change if file were deleted
and recreated. This value has been inaccurate for years on many
platforms, and nobody seems to have noticed or cared.
The 6th argument to ``copy-file`` has been renamed to
PRESERVE-EXTENDED-ATTRIBUTES as it now handles both SELinux context
and ACL entries.
The function ``file-ownership-preserved-p`` now has an optional
argument GROUP which causes it check for file group too. This can be
used in place of the 9th element of ``file-attributes``.
The function ``set-visited-file-modtime`` now accepts a 0 or -1
argument, with the same interpretation as the returned value of
``visited-file-modtime``.
```


#### Changes in autorevert.el

```
If Emacs is compiled with file notification support, notifications
are used instead of checking the time stamp of the files. You can
disable this by setting the user option ``auto-revert-use-notify`` to
nil. Alternatively, a regular expression of directories to be
excluded from file notifications can be specified by
``auto-revert-notify-exclude-dir-regexp``.
```


As I’ve talked about at length now, this inotify support is a big thing.

```
The new user option ``auto-revert-remote-files`` enables reversion
of remote files when set to non-nil.
```


Also useful.

#### Face changes

```
The function ``face-spec-set`` is now like ``setq`` for face specs.
Its third arg now accepts values specifying a face spec type (defface,
custom, or override spec), and the relevant spec is set accordingly.
New function ``add-face-text-property``, which can be used to
conveniently prepend/append new face properties.
Face specs set via Custom themes now replace the ``defface`` spec
rather than inheriting from it (as do face specs set via Customize).
New face characteristic (supports :underline (:style wave))
specifies whether or not the terminal can display a wavy line.
New face spec attribute :distant-foreground
specifies foreground to use if background color is near the foreground
color that would otherwise have been used.
```


#### Image API

```
``image-animated-p`` is now ``image-multi-frame-p``.
It returns non-nil for any image that contains multiple frames,
whether or not it specifies a frame delay.
New variable ``image-default-frame-delay`` gives the frame delay for
animated images which do not specify a frame delay.
New functions ``image-current-frame`` and ``image-show-frame`` for getting
and setting the current frame of a multi-frame image.
```


#### EIEIO

```
Namespace cleanup by obsolete-aliasing functions to use ``eieio-`` prefix.
object-name -> eieio-object-name
object-class -> eieio-object-class
object-class-fast -> eieio–object-class
object-name-string -> eieio-object-name-string
object-num-slots -> eieio–object-num-slots
object-set-name-string -> eieio-object-set-name-string
class-parent -> eieio-class-parent
class-parents -> eieio-class-parents
class-children -> eieio-class-children
class-num-slots -> eieio–class-num-slots
class-precedence-list -> eieio-class-precedence-list
All generated class-\* and object-\* field accessors are now
prefixed with ``eieio-`` as well.
Obsoleted functions:
class-of
class-direct-subclasses
class-direct-superclasses
```


#### Changes in encoding and decoding of text

```
New coding-system ``prefer-utf-8``.
This is like ``undecided`` but prefers UTF-8 on decoding if the text to
be decoded does not contain any invalid UTF-8 sequences. On encoding,
any non-ASCII characters are automatically encoded as UTF-8.
```


Very very useful. It’s a belt and braces thing; try UTF-8, as that’s probably the right thing, and if that fails leave it undecided. IMO this should be the default setting.

```
New attributes of coding-systems whose type is ``undecided``.
Two new attributes, ``:inhibit-null-byte-detection`` and
``:inhibit-iso-escape-detection``, determine how to detect encoding of
text that includes null bytes and ISO-2022 escape sequences,
respectively. Each of these attributes can be either nil, zero, or
t. If it is t, decoding text ignores null bytes and, respectively,
ISO-2022 sequences. If it is nil, null bytes cause text to be decoded
with no-conversion and ISO-2022 sequences cause Emacs to assume the
text is encoded in one of the ISO-2022 encodings, such as
iso-2022-7bit. If the value is zero, Emacs consults the variables
inhibit-null-byte-detection and inhibit-iso-escape-detection, which
see.
The new attribute ``:prefer-utf-8``, if non-nil, causes Emacs to prefer
UTF-8 encoding and decoding, whenever possible.
These attributes are only meaningful for coding-systems of type
``undecided``. (The type of a coding-system is determined by its
``:coding-type`` attribute and can be accessed by calling the
``coding-system-type`` function.)
``time-to-seconds`` is not obsolete any more.
The lock for ‘DIR/FILE’ is now ‘DIR/.#FILE’ and may be a regular file.
When you edit DIR/FILE, Emacs normally creates a symbolic link
DIR/.#FILE as a lock that warns other instances of Emacs that DIR/FILE
is being edited. Formerly, if there was already a non-symlink file
named DIR/.#FILE, Emacs fell back on the lock names DIR/.#FILE.0
through DIR/.#FILE.9. These fallbacks have been removed, so that
Emacs now no longer locks DIR/FILE in that case.
On file systems that do not support symbolic links, the lock is now a
regular file with contents being what would have been in the symlink.
New functions ``group-gid`` and ``group-real-gid``.
```


#### Changes to the Emacs Lisp Coding Conventions in Emacs 24.4

```
The package descriptor and name of global variables, constants,
and functions should be separated by two hyphens if the symbol is not
meant to be used by other packages.
```


### Changes in Emacs 24.4 on Non-Free Operating Systems

```
The procedure for building Emacs on MS-Windows has changed.
It is now built by running the same configure script as on all other
platforms. This requires the MSYS environment and MinGW development
tools. See the updated instructions in nt/INSTALL for details.
Using the Posix configure script and Makefile’s also means a change in
the directory structure of the Emacs installation on Windows. It is
now the same as on GNU and Unix systems. In particular, the auxiliary
programs, such as cmdproxy.exe and hexl.exe, are in
libexec/emacs/VERSION/i686-pc-mingw32 (where VERSION is the Emacs
version), version-independent site-lisp is in share/emacs/site-lisp,
version-specific Lisp files are in share/emacs/VERSION/lisp and in
share/emacs/VERSION/site-lisp, Info docs are in share/info, and data
files are in share/emacs/VERSION/etc. (Emacs knows about all these
directories and will find the files in there automatically; there’s no
need to set any variables due to this change.)
Emacs on Windows 2000 and later can now access files and directories
whose names cannot be encoded in the current system codepage.
The new variable ``w32-unicode-filenames`` controls this feature: if it
is t, Emacs uses Unicode APIs to pass file names to system calls,
which lifts the limitation of file names to the current locale.
The “generate a backtrace on fatal error” feature now works on MS Windows.
The backtrace is written to the ‘emacs\_backtrace.txt’ file in the
directory where Emacs was running.
The variable ``buffer-file-type`` is no longer supported.
Setting it /codehas no effect, and %t in the mode-line format is ignored.
Likewise, ``file-name-buffer-file-type-alist`` is now obsolete, and
modifying it has no effect.
Lock files now work on MS-Windows.
This allows to avoid losing your edits if the same file is being
edited in another Emacs session or by another user. See the node
“Interlocking” in the Emacs User Manual for the details. To disable
file locking, customize ``create-lockfiles`` to nil.
Improved fullscreen support on Mac OS X.
Both native (>= OSX 10.7) and “old style” fullscreen are supported.
Customize ``ns-use-native-fullscreen`` to change style. For >= 10.7
native is the default.
OSX >= 10.7 can use sRGB colorspace.
Customize ``ns-use-srgb-colorspace`` to change style. t is the default.
Note: This does not apply to images.
```


## Conclusion

And there you have it. A lot of changes, most of them are seemingly small changes, but they’re almost all quality-of-life improvements. And I think that’s the only way to really move a product forward: small, incremental improvements.

Is it worth upgrading? That’s up to you. I’m already using the new version; the web browser in particular will be useful for manuals.
---
title: What's New in Emacs 29.1?
url: https://www.masteringemacs.org/article/whats-new-in-emacs-29-1
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Wonderful news! Emacs 29.1 is out now. If you’re wondering what’s new, and why it’s *absolutely* worth upgrading, keep reading. I’ve annotated the NEWS file – as I’ve been doing for the last thirteen years – with my own thoughts and comments on the deluge of new and interesting features.

To celebrate, [my book on Emacs](https://www.masteringemacs.org/book) is also on sale: 29% off.

Before I go into the specifics of every minor item, a quick summary of what I think are the major highlights of Emacs 29.1:

- Official tree-sitter support
Tree-sitter is a third-party library that parses your text (usually code, but also things like Markdown) into a

*concrete syntax tree*. It’s one of the hallmark features in Emacs 29, though it is optional for now.I have written extensively about tree sitter. If you’re new, and wondering why you should care, read my article on

[tree-sitter and the complications of parsing languages](https://www.masteringemacs.org/article/tree-sitter-complications-of-parsing-languages).Briefly, a concrete syntax tree is the distillation of your text or code, and so it’s better than regular expressions and

*ad hoc*snippets of code at extracting meaning from your code. It offers better font locking (syntax highlighting); correct and more precise indentation; and limitless potential to extract syntactically interesting elements from your code. That means you can do[structured movement and editing with tree-sitter](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), as my package Combobulate aims to do, in the vein of paredit and similar tools.Installing tree-sitter is not straight forward, at least until your package manager starts shipping Emacs 29 with tree sitter support. My article on

[how to get started with tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter)is a good place to start if you’re using Linux.- EGlot, the Language Server Client
EGlot, the leaner complement to the fully-featured LSP-mode, is now built into Emacs. It should work out of the box. Just type

`M-x eglot`

in a buffer to get started.- Use-package
I wrote about

[use-package, a declarative configuration tool](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool)back when it came out. That was a decade ago, almost. It’s finally in Emacs, which is a good thing indeed.It’s an easier and more expressive way of sharing Emacs configuration snippets, and knowing it’s built in just makes everything much easier.

- Better long line support
There have been, ah, several bites at this rather bitter cherry over the years.

Emacs gums up on very long lines. To say it’s infuriating would be an understatement. I’ve been caught out by this a million times. Sometimes I have to kill Emacs as it’s desperately trying to append to the same, long line of text.

It’s still not

*solved*, but it*is*a lot better. More on that below.- Native SQLite Support
SQLite support, in one form or another, has been around for a while. Now you can legitimately compile Emacs with sqlite support, which is a large step forward.

As much as we like to delude ourselves into thinking that unstructured orgmode text, or even s-expressions, represent the pinnacle of text editing and the acme of scrappy hackerdom, that mantra does come with a significant penalty to performance. Ask anyone with very large org mode files or someone who wants to fast, random access to clown-sized s-expression trees. I’m sure we’ll see a much larger effort towards representing – yes, indeed, the whole point of Emacs – text in buffers as we know it, but with a fast query engine and efficient storage medium in the backend. The two need not be mutually exclusive.

- Changing the init directory
You can now instruct Emacs to read its initialization from another directory from the command line. Hugely useful if you’re using and testing multiple Emacs versions at the same time.

- Pixel Scroll Precision Mode
You can enable

`M-x pixel-scroll-precision-mode`

and get smooth scrolling like you do in other programs.

## Installation Changes in Emacs 29.1

```
Ahead-of-time native compilation can now be requested via configure.
Use '--with-native-compilation=aot' to request that all the Lisp files
in the Emacs tree should be natively compiled ahead of time. (This is
slow on most machines.)
This feature existed in Emacs 28.1, but was less easy to request.
```


Native compilation was the marquee feature in Emacs 28. It uses GCC’s libgccjit to add just-in-time compilation for all elisp code, resulting in – usually – greatly improved performance. My article, [Speed up Emacs with libjansson and native elisp compilation](https://www.masteringemacs.org/article/speed-up-emacs-libjansson-native-elisp-compilation), has all the gory details.

This new switch is, as it says, really just a way of front loading the (frustrating to some, but I do not mind) elisp compilation that usually runs in the background in Emacs. You could tell it to do this before also, but it was admittedly harder.

The thing is, native compilation is only run once; once it’s done, it won’t run again unless the source file changes.

So, if you want to do it all up front while you’re building Emacs from source, you can with this switch.

```
Emacs can be built with the tree-sitter parsing library.
This library, together with separate grammar libraries for each
language, provides incremental parsing capabilities for several
popular programming languages and other formatted files. Emacs built
with this library offers major modes, described elsewhere in this
file, that are based on the tree-sitter's parsers. If you have the
tree-sitter library installed, the configure script will automatically
include it in the build; use '--without-tree-sitter' at configure time
to disable that.
Emacs modes based on the tree-sitter library require an additional
grammar library for each mode. These grammar libraries provide the
tree-sitter library with language-specific lexical analysis and
parsing capabilities, and are developed separately from the
tree-sitter library itself. If you don't have a grammar library
required by some Emacs major mode, and your distro doesn't provide it
as an installable package, you can compile and install such a library
yourself. Many libraries can be downloaded from the tree-sitter site:
https://github.com/tree-sitter
Emacs provides a user command, 'treesit-install-language-grammar',
that automates the download and build process of a grammar library.
It prompts for the language, the URL of the language grammar's VCS
repository, and then uses the installed C/C++ compiler to build the
library and install it.
You can also do this manually. To compile such a library after
cloning its Git repository, compile the files "scanner.c" and
"parser.c" (sometimes named "scanner.cc" and "parser.cc") in the "src"
subdirectory of the library's source tree using the C or C++ compiler,
then link these two files into a shared library named
"libtree-sitter-LANG.so" ("libtree-sitter-LANG.dll" on MS-Windows,
"libtree-sitter-LANG.dylib" on macOS), where LANG is the name of the
language supported by the grammar as it is expected by the Emacs major
mode (for example, "c" for 'c-ts-mode', "cpp" for 'c++-ts-mode',
"python" for 'python-ts-mode', etc.). Then place the shared library
you've built in the same directory where you keep the other shared
libraries used by Emacs, or in the "tree-sitter" subdirectory of your
'user-emacs-directory', or in a directory mentioned in the variable
'treesit-extra-load-path'.
You only need to install language grammar libraries required by the
Emacs modes you will use, as Emacs loads these libraries only when the
corresponding mode is turned on in some buffer for the first time in
an Emacs session.
We generally recommend to use the latest versions of grammar libraries
available from their sites, as these libraries are in constant
development and occasionally add features and fix important bugs to
follow the advances in the programming languages they support.
```


As I recommended in the beginning, my article on [installing tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) is a good place to start if you’re unfamiliar with the finer points of installing tree-sitter. Doubly so for the shared libraries you need for the languages you want tree-sitter to use. I demonstrate how you can both compile from source, but also download pre-compiled binaries. The latter is especially important for OSes like Windows where you may not have the tooling required to do this yourself.

It’s… a significant barrier to entry, in my opinion, to require all this work before you can use tree-sitter. The maintainers’ reasons for not shipping the libraries is also reasonable: it’s not in the scope of the GNU Emacs project to lug around a bunch of libraries written by third-party sources.

Having said that, the frustration of setting it up is somewhat alleviated by the helpful `treesit-install-language-grammar`

function, as it’ll attempt to guess the target and compiler switches required and automatically check out the tree-sitter libraries from Ghit. But, still, it could be easier.

So, yeah, again: read my article where I cover all the gotchas and things you need to know. This sort of stuff is the prize you get for going through with it all:

![](../../assets/307b8fb6558102f3.gif)

[Combobulate](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), adds advanced editing and movement using tree-sitter. This is Combobulate's expand region feature, bound to

`M-h`

.Thanks to tree-sitter you can have crisp and clear “expand region” functionality that’ll correctly mark the boundaries of each syntactic unit.

```
Emacs can be built with built-in support for accessing SQLite databases.
This uses the popular sqlite3 library, and can be disabled by using
the '--without-sqlite3' option to the 'configure' script.
```


With formal support of SQLite in Emacs, I can imagine that this’ll be one of those options most distro maintainers will enable by default, as SQLite’s widely used in most distros already. That’s good new for everyone: SQLite will find a place in all manner of places in Emacs over time.

All we need now is a nice, ergonomic and Lispy query builder layer on top. Any takers?

```
Support for the WebP image format.
This support is built by default when the libwebp library is
available, and includes support for animated WebP images. To disable
WebP support, use the '--without-webp' configure flag. Image
specifiers can now use ':type webp'.
```


Useful if you do a lot of web development where that is becoming a common file format. I cannot divine how this integrates with the imagemagick configure flag, though. The implication is it is not required at all or that it even works with imagemagick.

```
Emacs now installs the ".pdmp" file using a unique fingerprint in the name.
The file is typically installed using a file name akin to
"...dir/libexec/emacs/29.1/x86_64-pc-linux-gnu/emacs-<fingerprint>.pdmp".
If a constant file name is required, the file can be renamed to
"emacs.pdmp", and Emacs will find it during startup anyway.
```


This should be of interest to few, except maybe distro maintainers.

```
Emacs on X now uses XInput 2 for input events.
If your X server has support and you have the XInput 2 development
headers installed, Emacs will use the X Input Extension for handling
input. If this causes problems, you can configure Emacs with the
option '--without-xinput2' to disable this support.
'(featurep 'xinput2)' can be used to test for the presence of XInput 2
support from Lisp programs.
```


I reported a couple of bugs against this (which were fixed within the hour!) particularly around mouse wheel scrolling not working well. If you do compile Emacs with this flag, as I have and still do, I’d keep an eye on weird input event regressions. Make sure you report them.

```
Emacs can now be optionally built with the Cairo XCB backend.
Configure Emacs with the '--with-cairo-xcb' option to use the Cairo
XCB backend; the default is not to use it. This backend makes Emacs
moderately faster when running over X connections with high latency,
but is currently known to crash when Emacs repeatedly closes and opens
a display connection to the same terminal; this could happen, for
example, if you repeatedly visit files via emacsclient in a single
client frame, each time deleting the frame with 'C-x C-c'.
```


Cairo’s an open source 2d rendering library that Emacs added support for some versions ago.

```
Emacs now supports being built with pure GTK.
To use this option, make sure the GTK 3 (version 3.22.23 or later) and
Cairo development files are installed, and configure Emacs with the
option '--with-pgtk'. Unlike the default X and GTK build, the
resulting Emacs binary will work on any underlying window system
supported by GDK, such as Wayland and Broadway. We recommend that you
use this configuration only if you are running a window system other
than X that's supported by GDK. Running this configuration on X is
known to have problems, such as undesirable frame positioning and
various issues with keyboard input of sequences such as 'C-;' and
'C-S-u'. Running this on WSL is also known to have problems.
Note that, unlike the X build of Emacs, the PGTK build cannot
automatically switch to text-mode interface (thus emulating '-nw') if
it cannot determine the default display; it will instead complain and
ask you to invoke it with the explicit '-nw' option.
```


The warning about not running Emacs built with `--with-pgtk`

under X cannot be understated. You really shouldn’t do that, though you’ll occasionally see references to people insisting that you build Emacs with it, regardless of the window system you’re using. If you’re not using Wayland/Broadway, you probably do not care about this.

```
Emacs has been ported to the Haiku operating system.
The configuration process should automatically detect and build for
Haiku. There is also an optional window-system port to Haiku, which
can be enabled by configuring Emacs with the option '--with-be-app',
which will require the Haiku Application Kit development headers and a
C++ compiler to be present on your system. If Emacs is not built with
the option '--with-be-app', the resulting Emacs will only run in
text-mode terminals.
To enable Cairo support, ensure that the Cairo and FreeType
development files are present on your system, and configure Emacs with
'--with-be-cairo'.
Unlike X, there is no compile-time option to enable or disable
double-buffering; it is always enabled. To disable it, change the
frame parameter 'inhibit-double-buffering' instead.
```


```
Emacs no longer reduces the size of the Japanese dictionary.
Building Emacs includes generation of a Japanese dictionary, which is
used by Japanese input methods. Previously, the build included a step
of reducing the size of this dictionary's vocabulary. This vocabulary
reduction is now optional, by default off. If you need the Emacs
build to include the vocabulary reduction, configure Emacs with the
option '--with-small-ja-dic'. In an Emacs source tree already
configured without that option, you can force the vocabulary reduction
by saying
make -C leim generate-ja-dic JA_DIC_NO_REDUCTION_OPTION=''
after deleting "lisp/leim/ja-dic/ja-dic.el".
```


```
The docstrings of preloaded files are not in "etc/DOC" any more.
Instead, they're fetched as needed from the corresponding ".elc"
files, as was already the case for all the non-preloaded files.
```


## Startup Changes in Emacs 29.1

```
'--batch' and '--script' now adjust the garbage collection levels.
These switches now set 'gc-cons-percentage' to 1.0 (up from the
default of 0.1). This means that batch processes will typically use
more memory than before, but use less time doing garbage collection.
Batch jobs that are supposed to run for a long time should adjust the
limit back down again.
```


That’s excellent news and it cuts out the middle-man of having to manually `let`

-bind these variables if you were doing complex things in batch mode.

```
Emacs can now be used more easily in an executable script.
If you start an executable script with
#!/usr/bin/emacs -x
Emacs will start without reading any init files (like with '--quick'),
and then execute the rest of the script file as Emacs Lisp. When it
reaches the end of the script, Emacs will exit with an exit code from
the value of the final form.
```


I’ll have to experiment and see if I can elide the need for `bash`

in my tool `ezf`

, which is an Emacs-only version of the `fzf`

tool. See: [Fuzzy Finding with Emacs Instead of fzf](https://www.masteringemacs.org/article/fuzzy-finding-emacs-instead-of-fzf).

```
Emacs now supports setting 'user-emacs-directory' via '--init-directory'.
Use the '--init-directory' command-line option to set
'user-emacs-directory'.
```


Wonderful news for those of us who have to test our packages using various Emacs versions and user configurations.

```
Emacs now has a '--fingerprint' option.
This will output a string identifying the current Emacs build, and exit.
```


Useful if you run Emacs in CI, I guess.

```
New hook 'after-pdump-load-hook'.
This is run at the end of the Emacs startup process, and is meant to
be used to reinitialize data structures that would normally be done at
load time.
```


This is unlikely to be of use to anyone except elisp grognards doing very particular things.

### Native Compilation

```
New command 'native-compile-prune-cache'.
This command deletes old subdirectories of the eln cache (but not the
ones for the current Emacs version). Note that subdirectories of the
system directory where the "*.eln" files are installed (usually, the
last entry in 'native-comp-eln-load-path') are not deleted.
```


If you regularly rebuild Emacs from scratch, it’s probably worth enabling this.

```
New function 'startup-redirect-eln-cache'.
This function can be called in your init files to change the
user-specific directory where Emacs stores the "*.eln" files produced
by native compilation of Lisp packages Emacs loads. The default
eln cache directory is unchanged: it is the "eln-cache" subdirectory
of 'user-emacs-directory'.
```


Files are put in your – usually `.emacs.d`

– directory by default. If you dislike Emacs polluting that directory you can now change it.

## Incompatible changes in Emacs 29.1

```
The image commands have changed key bindings.
In previous Emacs versions, the '+', '-' and 'r' keys were bound when
point was over an image. In Emacs 29.1, additional commands have been
added, and this made it more likely that users would trigger the image
commands by mistake. To avoid this, all image commands have been
moved to the 'i' prefix keymap, so '+' is now 'i +', '-' is now 'i -',
and 'r' is now 'i r'. In addition, these commands are now repeating,
so you can rotate an image twice by saying 'i r r', for instance.
```


It’s not clear, but all the key bindings (incl. the new ones) now live under `i`

. See `M-x describe-keymap image-slice-map`

.

```
Emacs now picks the correct coding-system for X input methods.
Previously, Emacs would use 'locale-coding-system' for input
methods, which could in some circumstances be incorrect, especially
when the input method chose to fall back to some other coding system.
Emacs now automatically detects the coding-system used by input
methods, and uses that to decode input in preference to the value of
'locale-coding-system'. This unfortunately means that users who have
changed the coding system used to decode X keyboard input must adjust
their customizations to 'locale-coding-system' to the variable
'x-input-coding-system' instead.
```


Not sure how many people this is likely to affect, but fixing this is nice. I do feel the variable is a little bit mis-named now, as I would not ordinarily connect locale (be it in the i18n or unix LOCALE sense of the word) to my X windows keyboard input.

```
Bookmarks no longer include context for encrypted files.
If you're visiting an encrypted file, setting a bookmark no longer
includes excerpts from that buffer in the bookmarks file. This is
implemented by the new hook 'bookmark-inhibit-context-functions',
where packages can register a function which returns non-nil for file
names to be excluded from adding such excerpts.
```


Heh. Whoops. It’s easy to see how it could happen due to how bookmarking is implemented in Emacs. The perils of having so many disparate and tangled systems all working together in (mostly) harmony.

```
'show-paren-mode' is now disabled in 'special-mode' buffers.
In Emacs versions previous to Emacs 28.1, 'show-paren-mode' defaulted
off. In Emacs 28.1, the mode was switched on in all buffers. In
Emacs 29.1, this was changed to be switched on in all editing-related
buffers, but not in buffers that inherit from 'special-mode'. To go
back to how things worked in Emacs 28.1, put the following in your
init file:
(setopt show-paren-predicate t)
```


Unlikely to bother too many people in *theory* when you read this, but it also affects Help and Info buffers! So if you want it back in those, you clearly have to re-set it for all special buffers.

```
Explicitly-set read-only state is preserved when reverting a buffer.
If you use the 'C-x C-q' command to change the read-only state of the
buffer and then revert it, Emacs would previously use the file
permission bits to determine whether the buffer should be read-only
after reverting the buffer. Emacs now remembers the decision made in
'C-x C-q'.
```


That’s a handy fix for me if you also use TRAMP or such-like to view files that you only have read permissions to look at. Now you can have auto revert on and yet still apply things like `M-x flush-lines`

without losing the read only flag on revert.

```
The Gtk selection face is no longer used for the region.
The combination of a Gtk-controlled background and a foreground color
controlled by the internal Emacs machinery led to low-contrast faces
in common default setups. Emacs now uses the same 'region' face on
Gtk and non-Gtk setups.
```


Never spotted this issue myself, though it’s nice to see these little burrs get filed off, one by one.

```
'C-h f' and 'C-h x' may now require confirmation when you press 'RET'.
If the text in the minibuffer cannot be completed to a single function
or command, typing 'RET' will not automatically complete to the shortest
candidate, but will instead ask for confirmation. Typing 'TAB' will
complete as much as possible, and another 'TAB' will show all the
possible completions. This allows you to insist on the functions name
even if Help doesn't appear to know about it, by confirming with a
second 'RET'.
```


I’m unclear if this is a generic change to the completion system or if it’s limited to just those two commands.

```
'w' ('dired-copy-filename-as-kill') has changed behavior.
If there are several files marked, file names containing space and
quote characters will be quoted "like this".
```


Good. I’ve been caught out by that bug before.

```
The 'd' command now more consistently skips dot files.
In previous Emacs versions, commands like 'C-u 10 d' would put the "D"
mark on the next ten files, no matter whether they were dot files
(i.e., "." and "..") or not, while marking the next ten lines with the
mouse (in 'transient-mark-mode') and then hitting 'd' would skip dot
files. These now work equivalently.
```


Another nice fix. Imagine the panic of seeing `..`

or `.`

marked D after you’ve triggered the delete action…

`'/ a' in "*Packages*" buffer now limits by archive name(s) instead of regexp.`


I don’t have any strong feelings about this. Is regexp search ever really useful in a repository where you’re looking for things by name? Word stemming and other such techniques would be a more useful feature than regexp. I can’t imagine too many people mind this.

```
Setting the goal columns now also affects '<prior>' and '<next>'.
Previously, 'C-x C-n' only affected 'next-line' and 'previous-line',
but it now also affects 'scroll-up-command' and 'scroll-down-command'.
```


Goal columns change the default column offset point is placed at on a line. Set it to 10, and point is set at the 10th column position when you move up or down a line. All this does is make it so your page up / down keys also respect it.

(You can unset a goal column with `C-0 C-x C-n`

.)

```
Isearch in "*Help*" and "*info*" now char-folds quote characters by default.
This means that you can say 'C-s `foo' (GRAVE ACCENT) if the buffer
contains "‘foo" (LEFT SINGLE QUOTATION MARK) and the like. These
quotation characters look somewhat similar in some fonts. To switch
this off, disable the new 'isearch-fold-quotes-mode' minor mode.
```


This is useful outside those buffers, of course. If you work with prose where the unicode glyphs are common, you can instead search for their elementary ASCII cousins instead and still match. Turn it on – why not?

```
Sorting commands no longer necessarily change modification status.
In earlier Emacs versions, commands like 'sort-lines' would always
change buffer modification status to "modified", whether they changed
something in the buffer or not. This has been changed: the buffer is
marked as modified only if the sorting ended up actually changing the
contents of the buffer.
```


You can still toggle a buffer’s modification manually with `M-~`

though.

```
'string-lines' handles trailing newlines differently.
It no longer returns an empty final string if the string ends with a
newline.
```


```
'TAB' and '<backtab>' are now bound in 'button-map'.
This means that if point is on a button, 'TAB' will take you to the
next button, even if the mode has bound it to something else. This
also means that 'TAB' on a button in an 'outline-minor-mode' heading
will move point instead of collapsing the outline.
```


Nice change. Buttons aren’t just *buttons*, they are often clickable things generally speaking. Hyperlinks often also fall under this category.

```
'outline-minor-mode-cycle-map' is now parent of 'outline-minor-mode'.
Instead of adding text property 'keymap' with 'outline-minor-mode-cycle'
on outline headings in 'outline-minor-mode', the keymap
'outline-minor-mode-cycle' is now active in the whole buffer.
But keybindings in 'outline-minor-mode-cycle' still take effect
only on outline headings because they are bound with the help of
'outline-minor-mode-cycle--bind' that checks if point is on a heading.
```


Mechanical change that is unlikely to affect day-to-day use if you use outline. I suspect this is mostly done to make it easier to search keymaps or perhaps fix some obscure keyboard events that don’t activate property keymaps.

```
'Info-default-directory-list' is no longer populated at Emacs startup.
If you have code in your init file that removes directories from
'Info-default-directory-list', this will no longer work.
```


```
'C-k' no longer deletes files in 'ido-mode'.
To get the previous action back, put something like the following in
your Init file:
(require 'ido)
(keymap-set ido-file-completion-map "C-k" #'ido-delete-file-at-head)
```


Terrifying default, if you ask me. Good riddance.

```
New user option 'term-clear-full-screen-programs'.
By default, term.el will now work like most terminals when displaying
full-screen programs: When they exit, the output is cleared, leaving
what was displayed in the window before the programs started. Set
this user option to nil to revert back to the old behavior.
```


As always I recommend you explore alternatives to term. See [Running Shells and Terminal Emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview),

```
Support for old EIEIO functions is not autoloaded any more.
You need an explicit '(require 'eieio-compat)' to use 'defmethod'
and 'defgeneric' (which were made obsolete in Emacs 25.1 by
'cl-defmethod' and 'cl-defgeneric').
Similarly you might need to '(require 'eieio-compat)' before loading
files that were compiled with an old EIEIO (Emacs<25).
```


Mostly of interest to people maintaining libraries.

```
'C-x 8 .' has been moved to 'C-x 8 . .'.
This is to open up the 'C-x 8 .' map to bind further characters there.
```


Unlikely to affect a great many people.

```
'C-x 8 =' has been moved to 'C-x 8 = ='.
You can now use 'C-x 8 =' to insert several characters with macron;
for example, 'C-x 8 = a' will insert U+0101 LATIN SMALL LETTER A WITH
MACRON. To insert a lone macron, type 'C-x 8 = =' instead of the
previous 'C-x ='.
```


It’s just another keymap with a range of characters.

## Eshell

Eshell is Emacs’s builtin shell written entirely in Elisp. It’s, like, totally awesome. See [Mastering Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell).

```
Eshell's PATH is now derived from 'exec-path'.
For consistency with remote connections, Eshell now uses 'exec-path'
to determine the execution path on the local or remote system, instead
of using the PATH environment variable directly.
```


Should aid with using TRAMP from Eshell.

```
'source' and '.' no longer accept the '--help' option.
This is for compatibility with the shell versions of these commands,
which don't handle options like '--help' in any special way.
```


```
String delimiters in argument predicates/modifiers are more restricted.
Previously, some argument predicates/modifiers allowed arbitrary
characters as string delimiters. To provide more unified behavior
across all predicates/modifiers, the list of allowed delimiters has
been restricted to "...", '...', /.../, |...|, (...), [...], <...>,
and {...}. See the "(eshell) Argument Predication and Modification"
node in the Eshell manual for more details.
```


Seems like a sensible change, though I wonder if there are any instances where this limitation won’t work?

```
Eshell pipelines now only pipe stdout by default.
To pipe both stdout and stderr, use the '|&' operator instead of '|'.
```


That is in keeping with the behavior of other shells, so that’s good.

```
The 'delete-forward-char' command now deletes by grapheme clusters.
This command is by default bound to the '<Delete>' function key
(a.k.a. '<deletechar>'). When invoked without a prefix argument or
with a positive prefix numeric argument, the command will now delete
complete grapheme clusters produced by character composition. For
example, if point is before an Emoji sequence, pressing '<Delete>'
will delete the entire sequence, not just a single character at its
beginning.
```


Interesting change, but if you use `C-d`

then know that it calls `delete-char`

and not `delete-forward-char`

. Consider rebinding it if you want this feature.

If you regularly work with languages that make use of grapheme clusters – or if you’re a Javascript developer and write purely with Emoji characters – then this is most likely a useful feature for you.

```
'load-history' does not treat autoloads specially any more.
An autoload definition appears just as a '(defun . NAME)' and the
'(t . NAME)' entries are not generated any more.
```


This is of little to no impact to most users.

```
The Tamil input methods no longer insert Tamil digits.
The input methods 'tamil-itrans' and 'tamil-inscript' no longer insert
the Tamil digits, as those digit characters are not used nowadays by
speakers of the Tamil language. To get back the previous behavior,
use the new 'tamil-itrans-digits' and 'tamil-inscript-digits' input
methods instead.
```


```
New variable 'current-time-list' governing default timestamp form.
Functions like 'current-time' now yield '(TICKS . HZ)' timestamps if
this new variable is nil. The variable defaults to t, which means
these functions default to timestamps of the forms '(HI LO US PS)',
'(HI LO US)' or '(HI LO)', which are less regular and less efficient.
This is part of a long-planned change first documented in Emacs 27.
Developers are encouraged to test timestamp-related code with this
variable set to nil, as it will default to nil in a future Emacs
version and will be removed some time after that.
```


```
Functions that recreate the "*scratch*" buffer now also initialize it.
When functions like 'other-buffer' and 'server-execute' recreate
"*scratch*", they now also insert 'initial-scratch-message' and set
the major mode according to 'initial-major-mode', like at Emacs
startup. Previously, these functions ignored
'initial-scratch-message' and left "*scratch*" in 'fundamental-mode'.
```


Heh, you know, whenever I’ve had to recreate that buffer myself I always found I missed the usual scratch buffer blurb.

```
Naming of Image-Dired thumbnail files has changed.
Names of thumbnail files generated when 'image-dired-thumbnail-storage'
is 'image-dired' now always end in ".jpg". This fixes various issues
on different platforms, but means that thumbnails generated in Emacs 28
will not be used in Emacs 29, and vice-versa. If disk space is an
issue, consider deleting the 'image-dired-dir' directory (usually
"~/.emacs.d/image-dired/") after upgrading to Emacs 29.
```


Or you could rename them yourself. See [Working with multiple files in dired](https://www.masteringemacs.org/article/working-multiple-files-dired) and [WDired: Editable Dired Buffers](https://www.masteringemacs.org/article/wdired-editable-dired-buffers).

```
The 'rlogin' method in the URL library is now obsolete.
Emacs will now display a warning if you request a URL like
"rlogin://foo@example.org".
```


```
Setting 'url-gateway-method' to 'rlogin' is now obsolete.
Emacs will now display a warning when setting it to that value.
The user options 'url-gateway-rlogin-host',
'url-gateway-rlogin-parameters', and 'url-gateway-rlogin-user-name'
are also obsolete.
```


```
The rlogin.el library, and the 'rsh' command are now obsolete.
Use something like 'M-x shell RET ssh <host> RET' instead.
```


Rlogin is a series of, putting it mildly, insecure legacy protocols from the disco era of software. They’re long-abandoned and consigned to the history books. So, I mean, yeah, sure, rlogin is awful, but… that horse has long bolted, had millennial kids and is comfortably on its way to retirement. So I think Emacs is a bit late to the party here.

```
The user function 'url-irc-function' now takes a SCHEME argument.
The user option 'url-irc-function' is now called with a sixth argument
corresponding to the scheme portion of the target URL. For example,
this would be "ircs" for a URL like "ircs://irc.libera.chat".
```


```
The linum.el library is now obsolete.
We recommend using either the built-in 'display-line-numbers-mode', or
the 'nlinum' package from GNU ELPA instead. The former has better
performance, but the latter is closer to a drop-in replacement.
1. To use 'display-line-numbers-mode', add something like this to your
init file:
(global-display-line-numbers-mode 1)
;; Alternatively, to use it only in programming modes:
(add-hook 'prog-mode-hook #'display-line-numbers-mode)
2. To use 'nlinum', add this to your Init file:
(package-install 'nlinum)
(global-nlinum-mode 1)
;; Alternatively, to use it only in programming modes:
(add-hook 'prog-mode-hook #'nlinum-mode)
3. To continue using the obsolete package 'linum', add this line to
your Init file, in addition to any existing customizations:
(require 'linum)
```


The “new” (it debuted in Emacs 26) line numbers mode is excellent and far and away the best way to show line numbers in Emacs. I can’t imagine too many are sad to see linum get obsoleted.

```
The thumbs.el library is now obsolete.
We recommend using the 'image-dired' command instead.
```


```
The autoarg.el library is now marked obsolete.
This library provides the 'autoarg-mode' and 'autoarg-kp-mode' minor
modes to emulate the behavior of the historical editor Twenex Emacs.
We believe it is no longer useful.
```


Interesting historical curiosity that lives on in Emacs, now in an obsolete state. Obsolete in Emacs usually means that it’ll get removed *eventually* or, indeed, never; it comes down to how many flare-ups there are on the mailing list.

Still, Emacs’s many dusty corners remain, to me, a fun time capsule and a look back at how things were. We shouldn’t rush into removing things just because they’re mostly forgotten.

```
The quickurl.el library is now obsolete.
Use 'abbrev', 'skeleton' or 'tempo' instead.
```


Yet another snippet completion tool. Abbrev is useful for [correcting typos and misspellings](https://www.masteringemacs.org/article/correcting-typos-misspellings-abbrev), and Skeleton and Tempo are two peas in a pod that offer textual expansion using a simple s-expression-based language.

`The url-about.el library is now obsolete.`


It seems to generate an HTML page with a list of supported URL schemes. There’s no commentary nor any real version history to accompany it. its actual use is a mystery to me.

```
The autoload.el library is now obsolete.
It is superseded by the new loaddefs-gen.el library.
```


```
The netrc.el library is now obsolete.
Use the 'auth-source-netrc-parse-all' function in auth-source.el
instead.
```


`The url-dired.el library is now obsolete.`


```
The fast-lock.el and lazy-lock.el libraries have been removed.
They have been obsolete since Emacs 22.1.
The variable 'font-lock-support-mode' is occasionally useful for
debugging purposes. It is now a regular variable (instead of a user
option) and can be set to nil to disable Just-in-time Lock mode.
```


Neither are likely to be missed by anyone. Lazy locking and Fast Locking were both attempts to speed up Emacs’s font locking facilities using a number of heuristics and obtuse variables. They’re gone, but the arcana lives on in Emacs’s Just-in-Time font locking engine.

```
The 'utf-8-auto' coding-system now produces BOM on encoding.
This is actually a bugfix, since this is how 'utf-8-auto' was
documented from day one; it just didn't behave according to
documentation. It turns out some Lisp programs were using this
coding-system on the wrong assumption that the "auto" part means some
automagic handling of the end-of-line (EOL) format conversion; those
programs will now start to fail, because BOM signature in UTF-8 encoded
text is rarely expected. That is the reason we mention this bugfix
here.
In general, this coding-system should probably never be used for
encoding, only for decoding.
```


## Changes in Emacs 29.1

```
New user option 'major-mode-remap-alist' to specify favorite major modes.
This user option lets you remap the default modes (e.g. 'perl-mode' or
'latex-mode') to your favorite ones (e.g. 'cperl-mode' or
'LaTeX-mode') instead of having to use 'defalias', which can have
undesirable side effects.
This applies to all modes specified via 'auto-mode-alist', file-local
variables, etc.
```


*Bit* of a hack. Essentially, it’s a “remap” facility for major modes, akin to `defalias`

which would not work here. Use it, as it says above, to swap one major mode for another.

However, and it forgets to say this explicitly, its primary use case is for tree-sitter-enabled major modes as they are separate from their non-TS kin; use this variable to rewire them. See [my article on getting started with tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) for an example of how to use it.

Note that this variable only remaps the major mode command – it does *not* fix your mode hooks or other settings!

`Emacs now supports Unicode Standard version 15.0.`


[Unicode 15](https://www.unicode.org/versions/Unicode15.0.0/) adds:

Unicode 15.0 adds 4,489 characters, for a total of 149,186 characters. These additions include 2 new scripts, for a total of 161 scripts, along with 20 new emoji characters, and 4,193 CJK (Chinese, Japanese, and Korean) ideographs.


```
New user option 'electric-quote-replace-consecutive'.
This allows you to disable the default behavior of consecutive single
quotes being replaced with a double quote.
```


This is referring to `electric-pair[-local]-mode`

, the built-in pairing tool for characters. You’re *probably* using it already in newer Emacsen.

```
Emacs is now capable of editing files with very long lines.
The display of long lines has been optimized, and Emacs should no
longer choke when a buffer on display contains long lines. The
variable 'long-line-threshold' controls whether and when these display
optimizations are in effect.
A companion variable 'large-hscroll-threshold' controls when another
set of display optimizations are in effect, which are aimed
specifically at speeding up display of long lines that are truncated
on display.
If you still experience slowdowns while editing files with long lines,
this may be due to line truncation, or to one of the enabled minor
modes, or to the current major mode. Try turning off line truncation
with 'C-x x t', or try disabling all known slow minor modes with
'M-x so-long-minor-mode', or try disabling both known slow minor modes
and the major mode with 'M-x so-long-mode', or visit the file with
'M-x find-file-literally' instead of the usual 'C-x C-f'.
In buffers in which these display optimizations are in effect, the
'fontification-functions', 'pre-command-hook' and 'post-command-hook'
hooks are executed on a narrowed portion of the buffer, whose size is
controlled by the variables 'long-line-optimizations-region-size' and
'long-line-optimizations-bol-search-limit', as if they were in a
'with-restriction' form. This may, in particular, cause occasional
mis-fontifications in these buffers. Modes which are affected by
these optimizations and by the fact that the buffer is narrowed,
should adapt and either modify their algorithm so as not to expect the
entire buffer to be accessible, or, if accessing outside of the
narrowed region doesn't hurt performance, use the
'without-restriction' form to temporarily lift the restriction and
access portions of the buffer outside of the narrowed region.
The new function 'long-line-optimizations-p' returns non-nil when
these optimizations are in effect in the current buffer.
```


So long, `so-long-mode`

. Having said that, I’m still getting coughs and sputters on long lines, on occasion. But it’s a marked improvement over older Emacsen. You should follow the advice given above and experiment to find the right settings for you.

```
New command to change the font size globally.
To increase the font size, type 'C-x C-M-+' or 'C-x C-M-='; to
decrease it, type 'C-x C-M--'; to restore the font size, type 'C-x
C-M-0'. The final key in these commands may be repeated without the
leading 'C-x' and without the modifiers, e.g. 'C-x C-M-+ C-M-+ C-M-+'
and 'C-x C-M-+ + +' increase the font size by three steps. When
'mouse-wheel-mode' is enabled, 'C-M-wheel-up' and 'C-M-wheel-down' also
increase and decrease the font size globally. Additionally, the
user option 'global-text-scale-adjust-resizes-frames' controls whether
the frames are resized when the font size is changed.
```


You can already use `C-x C-=`

and friends to adjust a single buffer, so it’s nice to see it extended to all of Emacs. Great for projectors and screen sharing.

```
New config variable 'syntax-wholeline-max' to reduce the cost of long lines.
This variable is used by some operations (mostly syntax-propertization
and font-locking) to treat lines longer than this variable as if they
were made up of various smaller lines. This can help reduce the
slowdowns seen in buffers made of a single long line, but can also
cause misbehavior in the presence of such long lines (though most of
that misbehavior should usually be limited to mis-highlighting). You
can recover the previous behavior with:
(setq syntax-wholeline-max most-positive-fixnum)
```


Definitely worth playing with if you have performance issues. It’s set to 10,000 which I think sounds like a reasonable default. Syntax here refers to a huge range of commands, many of them you probably don’t know of, like `parse-partial-sexp`

and `syntax-ppss`

. Needless to say, everything from font locking to navigation and editing are affected in one way or another.

```
New bindings in 'find-function-setup-keys' for 'find-library'.
When 'find-function-setup-keys' is enabled, 'C-x L' is now bound to
'find-library', 'C-x 4 L' is now bound to 'find-library-other-window'
and 'C-x 5 L' is now bound to 'find-library-other-frame'.
```


Okay, so the wording’s a bit diffuse. When you [evaluate](https://www.masteringemacs.org/article/evaluating-elisp-emacs) `(find-function-setup-keys)`

it’ll bind a bunch of key bindings in the `C-x`

, `C-x 4`

and `C-x 5`

keymaps.

I didn’t even *know* about this feature. Turns out Stallman added it in 1998. Huh. The more you know. So yeah, if execute that function you’ll get some handy key bindings to jump to functions and now libraries.

```
New key binding after 'M-x' or 'M-X': 'M-X'.
Emacs allows different completion predicates to be used with 'M-x'
(i.e., 'execute-extended-command') via the
'read-extended-command-predicate' user option. Emacs also has the
'M-X' (note upper case X) command, which only displays commands
especially relevant to the current buffer. Emacs now allows toggling
between these modes while the user is inputting a command by hitting
'M-X' while in the minibuffer.
```


Nice change. The `M-X`

(note case) key binding filters the list of commands to the ones deemed “relevant” to your active buffer. It’s a nifty feature and a nice way to discover new things.

`Interactively, 'kill-buffer' will now offer to save the buffer if unsaved.`


Not much to say here: good.

```
New commands 'duplicate-line' and 'duplicate-dwim'.
'duplicate-line' duplicates the current line the specified number of times.
'duplicate-dwim' duplicates the region if it is active. If not, it
works like 'duplicate-line'. An active rectangular region is
duplicated on its right-hand side. The new user option
'duplicate-line-final-position' specifies where to move point
after duplicating a line.
```


Apparently one of the ‘meme arguments’ for why Vi(m) is better, as it has the option to easily do this. Well, good news, Vim users: you can now prostrate yourself before Emacs.

Now annoyingly, they didn’t bind them to a key. (Why?). Let’s fix that real quick:

:

`(global-set-key (kbd "C-x j") #'duplicate-dwim)`


`C-x j`

seems free; we’ll wedge it in there.

`Files with the ".eld" extension are now visited in 'lisp-data-mode'.`


```
'network-lookup-address-info' can now check numeric IP address validity.
Specifying 'numeric' as the new optional HINTS argument makes it
check if the passed address is a valid IPv4/IPv6 address (without DNS
traffic).
(network-lookup-address-info "127.1" 'ipv4 'numeric)
=> ([127 0 0 1 0])
```


Speaking of network stuff. Did you know that Emacs [has a host of wrappers for commandline network utilities](https://www.masteringemacs.org/article/network-utilities-emacs)?

```
New command 'find-sibling-file'.
This command jumps to a file considered a "sibling file", which is
determined according to the new user option 'find-sibling-rules'.
```


No word on whether this is meant to replace – or indeed, augment – the existing `M-x ffap`

(find file at point) that tries to do much the same. There’s also `M-x ff-find-related-file`

which works well indeed.

It’s worth noting that both of these options come with a laundry list of heuristics already, such as finding header files belonging to a source file.

The `find-sibling-rules`

variable, meanwhile, is empty.

Mmm… there’s a missed opportunity here to merge this stuff.

```
New user option 'delete-selection-temporary-region'.
When non-nil, 'delete-selection-mode' will only delete the temporary
regions (usually set by mouse-dragging or shift-selection).
```


Actually, this is a neat little feature. If you use the mark commands to select stuff, like `C-M-SPC`

or `M-@`

, then you’d delete the text if you typed a character. With this option, it only happens if you select by some other means.

```
New user option 'switch-to-prev-buffer-skip-regexp'.
This should be a regexp or a list of regexps; buffers whose names
match those regexps will be ignored by 'switch-to-prev-buffer' and
'switch-to-next-buffer'.
```


If you use either of these commands (`C-x C-<right/left>`

) to navigate, you’d probably want to add all the flotsam and jetsam you don’t want to switch to.

```
New command 'rename-visited-file'.
This command renames the file visited by the current buffer by moving
it to a new name or location, and also makes the buffer visit this new
file.
```


Yep. Emacs has never had the ability to rename a file *in-situ* from the buffer. Until someone pointed that out to me I thought it did. But then I remember I rename everything in dired — and seemingly so did everyone else who used Emacs up until now when that command was added.

A long, over-due command.

## Menus

```
The entries following the buffers in the "Buffers" menu can now be altered.
Change the 'menu-bar-buffers-menu-command-entries' variable to alter
the entries that follow the buffer list.
```


You can customize Emacs’s menu entries by altering this variable.

```
'delete-process' is now a command.
When called interactively, it will kill the process running in the
current buffer (if any). This can be useful if you have runaway
output in the current buffer (from a process or a network connection),
and want to stop it.
```


Very useful. You should know about `M-x list-processes`

also.

```
New command 'restart-emacs'.
This is like 'save-buffers-kill-emacs', but instead of just killing
the current Emacs process at the end, it starts a new Emacs process
(using the same command line arguments as the running Emacs process).
'kill-emacs' and 'save-buffers-kill-emacs' have also gained new
optional arguments to restart instead of just killing the current
process.
```


Nice to have.

## Drag and Drop

Just as a quick side note: you can drag and drop a bunch of stuff into Emacs and have it do the right thing. Files get opened, for instance, if you drag them into Emacs. If you drag them into message buffer you’ll instead *attach* them as a file. Great if you do email in Emacs like I do.

```
New user option 'mouse-drag-mode-line-buffer'.
If non-nil, dragging on the buffer name part of the mode-line will
drag the buffer's associated file to other programs. This option is
currently only available on X, Haiku and Nextstep (GNUstep or macOS).
```


Neat. No way I’ll ever remember that, but it’s a nice addition.

```
New user option 'mouse-drag-and-drop-region-cross-program'.
If non-nil, this option allows dragging text in the region from Emacs
to another program.
```


That I *will* remember though.

```
New user option 'mouse-drag-and-drop-region-scroll-margin'.
If non-nil, this option allows scrolling a window while dragging text
around without a scroll wheel.
```


Another one of those features people who move to Emacs come to depend on.

```
The value of 'mouse-drag-copy-region' can now be the symbol 'non-empty'.
This prevents mouse drag gestures from putting empty strings onto the
kill ring.
```


You’d probably want to set this to t.

```
New user options 'dnd-indicate-insertion-point' and 'dnd-scroll-margin'.
These options allow adjusting point and scrolling a window when
dragging items from another program.
```


```
The X Direct Save (XDS) protocol is now supported.
This means dropping an image or file link from programs such as
Firefox will no longer create a temporary file in a random directory,
instead asking you where to save the file first.
```


Never heard of this protocol before, but it reads like a fine improvement over the copy-to-temp approach Emacs employed before.

```
New user option 'record-all-keys'.
If non-nil, this option will force recording of all input keys,
including those typed in response to passwords prompt (this was the
previous behavior). The default is nil, which inhibits recording of
passwords.
```


Keep in mind Emacs still records most stuff you type. See the lossage for an example: `C-h l`

.

```
New function 'command-query'.
This function makes its argument command prompt the user for
confirmation before executing.
```


```
The 'disabled' property of a command's symbol can now be a list.
The first element of the list should be the symbol 'query', which will
cause the command disabled this way prompt the user with a y/n or a
yes/no question before executing. The new function 'command-query' is
a convenient method of making commands disabled in this way.
```


There are a handful of commands marked disabled in Emacs as they’re confusing to beginners. You might’ve run into the prompts when you typed one of them.

```
'count-words' will now report buffer totals if given a prefix.
Without a prefix, it will only report the word count for the narrowed
part of the buffer.
```


`'count-words' will now report sentence count when used interactively.`


Cue the interminable arguments over what constitutes a sentence.

```
New user option 'set-message-functions'.
It allows more flexible control of how echo-area messages are displayed
by adding functions to this list. The default value is a list of one
element: 'set-minibuffer-message', which displays echo-area messages
at the end of the minibuffer text when the minibuffer is active.
Other useful functions include 'inhibit-message', which allows
specifying, via 'inhibit-message-regexps', the list of messages whose
display should be inhibited; and 'set-multi-message' that accumulates
recent messages and displays them stacked together.
```


Nifty new features. The echo area is a busy area now, particularly if you’re using a lot of tools, all vying for your attention. Maybe give the multi-message approach a shot if you’re missing messages? I wrote about a similar problem with Eldoc and competing messages. [Seamlessly Merge Multiple Documentation Sources with Eldoc](https://www.masteringemacs.org/article/seamlessly-merge-multiple-documentation-sources-eldoc).

```
New user option 'find-library-include-other-files'.
If set to nil, commands like 'find-library' will only include library
files in the completion candidates. The default is t, which preserves
previous behavior, whereby non-library files could also be included.
```


```
New command 'sqlite-mode-open-file' for examining an sqlite3 file.
This uses the new 'sqlite-mode' which allows listing the tables in a
DB file, and examining and modifying the columns and the contents of
those tables.
```


Nifty!

```
'write-file' will now copy some file mode bits.
If the current buffer is visiting a file that is executable, the
'C-x C-w' command will now make the new file executable, too.
```


Along the same lines, you should consider the switch to [make script files executable automatically](https://www.masteringemacs.org/article/script-files-executable-automatically).

```
New user option 'process-error-pause-time'.
This determines how long to pause Emacs after a process
filter/sentinel error has been handled.
```


If you regularly cancel out of compilation buffers or other processes and find the delay annoying, try setting it to 0.

```
New faces for font-lock.
These faces are primarily meant for use with tree-sitter. They are:
'font-lock-bracket-face', 'font-lock-delimiter-face',
'font-lock-escape-face', 'font-lock-function-call-face',
'font-lock-misc-punctuation-face', 'font-lock-number-face',
'font-lock-operator-face', 'font-lock-property-name-face',
'font-lock-property-use-face', 'font-lock-punctuation-face',
'font-lock-regexp-face', and 'font-lock-variable-use-face'.
```


This is part of the tree-sitter changes. As TS allows for far more precise selection of syntactic constructs, it made sense to add a bunch of faces.

You’ll want to customize them to suit your needs.

```
New face 'variable-pitch-text'.
This face is like 'variable-pitch' (from which it inherits), but is
slightly larger, which should help with the visual size differences
between the default, non-proportional font and proportional fonts when
mixed.
```


```
New face 'mode-line-active'.
This inherits from the 'mode-line' face, but is the face actually used
on the mode lines (along with 'mode-line-inactive').
```


```
New face attribute pseudo-value 'reset'.
This value stands for the value of the corresponding attribute of the
'default' face. It can be used to reset attribute values produced by
inheriting from other faces.
```


Useful if you want some, but not all, inheriting faces.

```
New X resource "borderThickness".
This controls the thickness of the external borders of the menu bars
and pop-up menus.
```


```
New X resource "inputStyle".
This controls the style of the pre-edit and status areas of X input
methods.
```


```
New X resources "highlightForeground" and "highlightBackground".
Only in the Lucid build, this controls colors used for highlighted
menu item widgets.
```


```
On X, Emacs now tries to synchronize window resize with the window manager.
This leads to less flicker and empty areas of a frame being displayed
when a frame is being resized. Unfortunately, it does not work on
some ancient buggy window managers, so if Emacs appears to freeze, but
is still responsive to input, you can turn it off by setting the X
resource "synchronizeResize" to "off".
```


```
On X, Emacs can optionally synchronize display with the graphics hardware.
When this is enabled by setting the X resource "synchronizeResize" to
"extended", frame content "tearing" is drastically reduced. This is
only supported on the Motif, Lucid, and no-toolkit builds, and
requires an X compositing manager supporting the extended frame
synchronization protocol (see
https://fishsoup.net/misc/wm-spec-synchronization.html).
This behavior can be toggled on and off via the frame parameter
'use-frame-synchronization'.
```


```
New frame parameter 'alpha-background' and X resource "alphaBackground".
This controls the opacity of the text background when running on a
composited display.
```


Party like it’s 1998. Remember back when everyone took screenshots of their KDE/GNOME/WindowMaker desktops and they all had that obligatory semi-translucent terminal window?

```
New frame parameter 'shaded'.
With window managers which support this, it controls whether or not a
frame's contents will be hidden, leaving only the title bar on display.
```


```
New user option 'x-gtk-use-native-input'.
This controls whether or not GTK input methods are used by Emacs,
instead of XIM input methods. Defaults to nil.
```


```
New user option 'use-system-tooltips'.
This controls whether to use the toolkit tooltips, or Emacs's own
native implementation of tooltips as small frames. This option is
only meaningful if Emacs was built with GTK+, Nextstep, or Haiku
support, and defaults to t, which makes Emacs use the toolkit
tooltips. The existing GTK-specific option
'x-gtk-use-system-tooltips' is now an alias of this new option.
```


I long ago disabled tooltips and made them appear in the echo area instead:

```
(tooltip-mode nil)
(setq tooltip-use-echo-area t)
(setq x-gtk-use-system-tooltips nil)
```


```
Non-native tooltips are now supported on Nextstep.
This means Emacs built with GNUstep or built on macOS is now able to
display different faces and images inside tooltips when the
'use-system-tooltips' user option is nil.
```


```
New minor mode 'pixel-scroll-precision-mode'.
When enabled, and if your mouse supports it, you can scroll the
display up or down at pixel resolution, according to what your mouse
wheel reports. Unlike 'pixel-scroll-mode', this mode scrolls the
display pixel-by-pixel, as opposed to only animating line-by-line
scrolls.
```


Pixel-perfect scrolling, at least in theory. On my computer it does act funny around large images, though this is mostly a limitation of Emacs’s display engine, more than the pixel scrolling.

## Terminal Emacs

```
Emacs will now use 24-bit colors on terminals that support "Tc" capability.
This is in addition to previously-supported ways of discovering 24-bit
color support: either via the "RGB" or "setf24" capabilities, or if
the 'COLORTERM' environment variable is set to the value "truecolor".
```


Emacs has had 24-bit support for years, so this is really only about catching the tail end of termcaps.

```
Select active regions with xterm selection support.
On terminals with xterm "setSelection" support, the active region may be
saved to the X primary selection, following the
'select-active-regions' variable. This support is enabled when
'tty-select-active-regions' is non-nil.
```


Worth setting to t if you prefer running Emacs in a GUI terminal.

```
New command to set up display of unsupported characters.
The new command 'standard-display-by-replacement-char' produces Lisp
code that sets up the 'standard-display-table' to use a replacement
character for display of characters that the text-mode terminal
doesn't support. This code is intended to be used in your init files.
This feature is most useful with the Linux console and similar
terminals, where Emacs has a reliable way of determining which
characters have glyphs in the font loaded into the terminal's memory.
```


This is the default character to display if Emacs or you terminal cannot. If you have strong views on this, you should contemplate changing it.

```
New functions to set terminal output buffer size.
The new functions 'tty--set-output-buffer-size' and
'tty--output-buffer-size' allow setting and retrieving the output
buffer size of a terminal device. The default buffer size is and has
always been BUFSIZ, which is defined in your system's stdio.h. When
you set a buffer size with 'tty--set-output-buffer-size', this also
prevents Emacs from explicitly flushing the tty output stream, except
at the end of display update.
```


I’ve no opinion nor any wisdom to share as to why you’d want to change this. Keen to hear from people who do though.

## ERT

ERT is Emacs’s unit test framework.

```
New ERT variables 'ert-batch-print-length' and 'ert-batch-print-level'.
These variables will override 'print-length' and 'print-level' when
printing Lisp values in ERT batch test results.
```


```
Redefining an ERT test in batch mode now signals an error.
Executing 'ert-deftest' with the same name as an existing test causes
the previous definition to be discarded, which was probably not
intended when this occurs in batch mode. To remedy the error, rename
tests so that they all have unique names.
```


```
ERT can generate JUnit test reports.
When environment variable 'EMACS_TEST_JUNIT_REPORT' is set, ERT
generates a JUnit test report under this file name. This is useful
for Emacs integration into CI/CD test environments.
```


```
Unbound test symbols now signal an 'ert-test-unbound' error.
This affects the 'ert-select-tests' function and its callers.
```


## Emoji

There’s a NEWS category just for Emoji now?

```
Emacs now has several new methods for inserting Emoji.
The Emoji commands are under the new 'C-x 8 e' prefix.
```


This is now the primary composition key for dealing with emoji.

```
New command 'emoji-insert' (bound to 'C-x 8 e e' and 'C-x 8 e i').
This command guides you through various Emoji categories and
combinations in a graphical menu system.
```


`C-x 8 e e`

opens a [Magit-style](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git) popup using the now-builtin transient package. I think this is the first instance of using transient in Emacs?

```
New command 'emoji-search' (bound to 'C-x 8 e s').
This command lets you search for and insert an Emoji based on names.
```


Like `C-x 8 RET`

, but the search space limited to just emoji.

```
New command 'emoji-list' (bound to 'C-x 8 e l').
This command lists all Emoji (categorized by themes) in a special
buffer and lets you choose one of them to insert.
```


Rather useful overview of smileys in a buffer. This is my preferred method for picking out emoji; note that the emoji are hyperlinked will insert the smiley at point.

```
New command 'emoji-recent' (bound to 'C-x 8 e r').
This command lets you choose among the Emoji you have recently
inserted and insert it.
```


```
New command 'emoji-describe' (bound to 'C-x 8 e d').
This command will tell you the name of the Emoji at point. (It also
works for non-Emoji characters.)
```


It prints the unicode descriptor for the character at point. It’s also available in `C-u C-x =`

.

```
New commands 'emoji-zoom-increase' and 'emoji-zoom-decrease'.
These are bound to 'C-x 8 e +' and 'C-x 8 e -', respectively. They
can be used on any character, but are mainly useful for Emoji.
```


```
New command 'emoji-zoom-reset'.
This is bound to 'C-x 8 e 0', and undoes any size changes performed by
'emoji-zoom-increase' and 'emoji-zoom-decrease'.
```


```
New input method 'emoji'.
This allows you to enter Emoji using short strings, eg ':face_palm:'
or ':scream:'.
```


I think I wrote the first input method to insert Emoji. In fact, it was the upcoming emoji code in Emacs 29 that prompted me to blog about it: [Inserting Emoji with Input Methods](https://www.masteringemacs.org/article/inserting-emoji-input-methods).

Input methods are a nifty way of inserting chorded text. It’s a really pleasant way of inserting diacritics. If you’re unfamiliar with input methods, then check out [Olé! Diacritics in Emacs](https://www.masteringemacs.org/article/diacritics-in-emacs).

## Help

`Variable values displayed by 'C-h v' in "*Help*" are now fontified.`


Yep. Big fan of this change.

```
New user option 'help-clean-buttons'.
If non-nil, link buttons in "*Help*" buffers will have any surrounding
quotes removed.
```


```
'M-x apropos-variable' output now includes values of variables.
Such an apropos buffer is more easily viewed with outlining after
enabling 'outline-minor-mode' in 'apropos-mode'.
```


Nifty change indeed. The apropos commands in Emacs should not be slept on.

```
New docstring syntax to indicate that symbols shouldn't be links.
When displaying docstrings in "*Help*" buffers, strings that are
"`like-this'" are made into links (if they point to a bound
function/variable). This can lead to false positives when talking
about values that are symbols that happen to have the same names as
functions/variables. To inhibit this buttonification, use the new
"\\+`like-this'" syntax.
```


```
New user option 'help-window-keep-selected'.
If non-nil, commands to show the info manual and the source will reuse
the same window in which the "*Help*" buffer is shown.
```


If you have strong preferences on where the windows should go, consider enabling this. Alternatively, my article on [Demystifying Emacs’s Window Manager](https://www.masteringemacs.org/article/demystifying-emacs-window-manager) will teach you how to tame window management in Emacs.

```
Commands like 'C-h f' have changed how they describe menu bindings.
For instance, previously a command might be described as having the
following bindings:
It is bound to <open>, C-x C-f, <menu-bar> <file> <new-file>.
This has been changed to:
It is bound to <open> and C-x C-f.
It can also be invoked from the menu: File → Visit New File...
```


```
The 'C-h .' command now accepts a prefix argument.
'C-u C-h .' would previously inhibit displaying a warning message if
there was no local help at point. This has been changed to call
'button-describe'/'widget-describe' and display button/widget help
instead.
```


```
New user option 'help-enable-variable-value-editing'.
If enabled, 'e' on a value in "*Help*" will pop you to a new buffer
where you can edit the value. This is not enabled by default, because
it is easy to make an edit that yields an invalid result.
```


There’s also `c`

in a help window to open its customize window. That is perhaps of more use to most people.

```
'C-h b' uses outlining by default.
Set 'describe-bindings-outline' to nil to get back the old behavior.
```


`C-h b`

is a great command to know about. It displays all the pertinent bindings in a buffer.

```
Jumping to function/variable source now saves mark before moving point.
Jumping to source from a "*Help*" buffer moves point when the source
buffer is already open. Now, the old point is pushed onto mark ring.
```


The global/local mark rings are worth learning about. They’re useful beacons for moving around in Emacs and they are always precipitated by a user-led action.

```
New key bindings in "*Help*" buffers: 'n' and 'p'.
These will take you (respectively) to the next and previous "page".
```


Page here meaning the old-fashioned concept in LISP and Emacs where the FORM FEED (`^L`

) character is used to denote a page in code. That’s what all the `xxx-page`

command do; they operate on them.

`'describe-char' now also outputs the name of Emoji sequences.`


```
New key binding in "*Help*" buffer: 'I'.
This will take you to the Emacs Lisp manual entry for the item
displayed, if any.
```


There is also `i`

which goes to the manual; this, in turn, tries to find the elisp symbol reference.

```
The 'C-h m' ('describe-mode') "*Help*" buffer has been reformatted.
It now only includes local minor modes at the start, and the global
minor modes are listed after the major mode.
```


I like this change, as this is most likely what you want to look at first, anyway.

```
The user option 'help-window-select' now affects apropos commands.
The apropos commands will now select the apropos window if
'help-window-select' is non-nil.
```


See above regarding windows.

```
'describe-keymap' now considers the symbol at point.
If the symbol at point is a keymap, 'describe-keymap' suggests it as
the default candidate.
```


Always nice to see contextual completions. I wish more commands did this.

```
New command 'help-quick' displays an overview of common commands.
The command pops up a buffer at the bottom of the screen with a few
helpful commands for various tasks. You can toggle the display using
'C-h C-q'.
```


This is cheat sheet for keyboard shortcuts. My view is still that you should use the menu bar until you’ve memorized the keys you’re ever likely to encounter in a cheat sheet.

```
Emacs now comes with Org v9.6.
See the file "etc/ORG-NEWS" for user-visible changes in Org.
```


## Outline Mode

Outline is the progenitor to Org mode and works in much the same way. It is, of course, vastly simpler.

```
Support for customizing the default visibility state of headings.
Customize the user option 'outline-default-state' to define what
headings will be visible initially, after Outline mode is turned on.
When the value is a number, the user option 'outline-default-rules'
determines the visibility of the subtree starting at the corresponding
level. Values are provided to control showing a heading subtree
depending on whether the heading matches a regexp, or on whether its
subtree has long lines or is itself too long.
```


### Outline Minor Mode

```
New user option 'outline-minor-mode-use-buttons'.
If non-nil, Outline Minor Mode will use buttons to hide/show outlines
in addition to the ellipsis. The default is nil, but in 'help-mode'
it has the value 'insert' that inserts the buttons directly into the
buffer, and you can use 'RET' to cycle outline visibility. When
the value is 'in-margins', Outline Minor Mode uses the window margins
for buttons that hide/show outlines.
```


```
Buttons and headings now have their own keymaps.
'outline-button-icon-map', 'outline-overlay-button-map', and
'outline-inserted-button-map' are now available as defined keymaps
instead of being anonymous keymaps.
```


## Windows

See my article on [Demystifying Emacs’s Window Manager](https://www.masteringemacs.org/article/demystifying-emacs-window-manager) to truly understand how all these window changes below work, and how you can use them. The subject is well beyond the scope of this blog entry.

```
New commands 'split-root-window-below' and 'split-root-window-right'.
These commands split the root window in two, and are bound to 'C-x w 2'
and 'C-x w 3', respectively. A number of other useful window-related
commands are now available with key sequences that start with the
'C-x w' prefix.
```


I am glad they added these. One of the things about Emacs’s window system is that you only ever operate within the part of the tree – Emacs’s window layout is stored in a simple tree structure – that your active window is in. So, splitting against the root window wasn’t possible without elisp.

```
New display action 'display-buffer-full-frame'.
This action removes other windows from the frame when displaying a
buffer on that frame.
```


This is a `display-buffer`

action that ensures a buffer is displayed in a new frame.

```
'display-buffer' now can set up the body size of the chosen window.
For example, a 'display-buffer-alist' entry of
(window-width . (body-columns . 40))
will make the body of the chosen window 40 columns wide. For the
height use 'window-height' and 'body-lines', respectively.
```


The body is the size of the window without the margins and all the other bits. You can already set the height/width of a window, but now you can also do it with just the body. Should allow for more fine-grained control.

```
'display-buffer' provides more options for using an existing window.
The display buffer action functions 'display-buffer-use-some-window' and
'display-buffer-use-least-recent-window' now honor the action alist
entry 'window-min-height' as well as the entries listed below to make
the display of several buffers in a row more amenable.
```


Excellent news. Placing a window is difficult for Emacs as it has to respect a range of constraints and criteria. And when it fails to do it the way you want or expect it to, it can easily lead to user frustration.

```
New buffer display action alist entry 'lru-frames'.
This allows specifying which frames 'display-buffer' should consider
when using a window that shows another buffer. It is interpreted as
per the ALL-FRAMES argument of 'get-lru-window'.
```


LRU meaning Least-Recently-Used.

```
New buffer display action alist entry 'lru-time'.
'display-buffer' will ignore windows with a use time higher than this
when using a window that shows another buffer.
```


```
New buffer display action alist entry 'bump-use-time'.
This has 'display-buffer' bump the use time of any window it returns,
making it a less likely candidate for displaying another buffer.
```


Taken together, you can use this to cycle buffers through windows using a combination of lru-time and bump-use-time. Now I’m curious to hear where this was first used.

```
New buffer display action alist entry 'window-min-width'.
This allows specifying a preferred minimum width of the window used to
display a buffer.
```


Useful to help constrain where Emacs can put a buffer (or a window, for that matter) and it should hopefully prevent things from popping up in tiny little windows that won’t fit the buffer’s content.

```
You can specify on which window 'scroll-other-window' operates.
This is controlled by the new 'other-window-scroll-default' variable,
which should be set to a function that returns a window. When this
variable is nil, 'next-window' is used.
```


A hidden feature of Emacs is the ability to carry out a limited number of actions on other, nearby windows. `C-M-S-v`

scrolls down the ‘other’ window (useful if you have two or more windows, one you’re editing and the other you’re reading along from.)

But now you can seemingly customize how this ‘other’ window is chosen.

## Frames

```
Deleted frames can now be undeleted.
The 16 most recently deleted frames can be undeleted with 'C-x 5 u' when
'undelete-frame-mode' is enabled. Without a prefix argument, undelete
the most recently deleted frame. With a numerical prefix argument
between 1 and 16, where 1 is the most recently deleted frame, undelete
the corresponding deleted frame.
```


Neat! I’m sure we’ve all closed a frame by accident.

```
The variable 'icon-title-format' can now have the value t.
That value means to use 'frame-title-format' for iconified frames.
This is useful with some window managers and desktop environments
which treat changes in frame's title as requests to raise the frame
and/or give it input focus, or if you want the frame's title to be the
same no matter if the frame is iconified or not.
```


## Tab Bars and Tab Lines

Tab *bars* are window configurations; custom set pieces for how you want to arrange your windows. Tab *lines* are just a tabbed list of buffers.

```
New user option 'tab-bar-auto-width' to automatically determine tab width.
This option is non-nil by default, which resizes tab-bar tabs so that
their width is evenly distributed across the tab bar. A companion
option 'tab-bar-auto-width-max' controls the maximum width of a tab
before its name on display is truncated.
```


If you want dynamic sizing and dislike truncated names, try it out.

```
'C-x t RET' creates a new tab when the provided tab name doesn't exist.
It prompts for the name of a tab and switches to it, creating a new
tab if no tab exists by that name.
```


Great if you want to navigate by tab name *or* maybe create a new one if that name does not exist.

```
New keymap 'tab-bar-history-mode-map'.
By default, it contains 'C-c <left>' and 'C-c <right>' to browse
the history of tab window configurations back and forward.
```


This feature is already in older Emacsen; what’s new is the mode map.

## BIDI

```
Better detection of text suspiciously reordered on display.
The function 'bidi-find-overridden-directionality' has been extended
to detect reordering effects produced by embeddings and isolates
(started by directional formatting control characters such as RLO and
LRI). The new command 'highlight-confusing-reorderings' finds and
highlights segments of buffer text whose reordering for display is
suspicious and could be malicious.
```


*Confusables* are a group of unicode characters that appear to look like well-known (often Western) characters but are in actual fact from other scripts. This is what spammers and scammers tend to use to make it appear like a domain name or email is actually someone else.

## Emacs Server and Client

Emacs has a client-server architecture, of course. It’s great! Set `EDITOR`

to `emacsclient`

and then `M-x server-start`

(or any number of other ways of starting an Emacs server!) and now your Emacs will open files in a running instance.

```
New command-line option '-r'/'--reuse-frame' for emacsclient.
With this command-line option, Emacs reuses an existing graphical client
frame if one exists; otherwise it creates a new frame.
```


```
New command-line option '-w N'/'--timeout=N' for emacsclient.
With this command-line option, emacsclient will exit if Emacs does not
respond within N seconds. The default is to wait forever.
```


```
'server-stop-automatically' can be used to automatically stop the server.
The Emacs server will be automatically stopped when certain conditions
are met. The conditions are determined by the argument to
'server-stop-automatically', which can be 'empty', 'delete-frame' or
'kill-terminal'.
```


Worthwhile if you have a use case that requires shutting down the server when you are finished. I, however, tend to keep it running forever and ever.

## Rcirc

Rcirc is one of *two* IRC clients in Emacs. The other is ERC.

```
New command 'rcirc-when'.
This shows the reception time of the message at point (if available).
```


```
New user option 'rcirc-cycle-completion-flag'.
Rcirc now uses the default 'completion-at-point' mechanism. The
conventional IRC behavior of completing by cycling through the
available options can be restored by enabling this option.
```


```
New user option 'rcirc-bridge-bot-alist'.
If you are in a channel where a bot is responsible for bridging
between networks, you can use this variable to make these messages
appear more native. For example, you might set the option to:
(setopt rcirc-bridge-bot-alist '(("bridge" . "{\\(.+?\\)}[[:space:]]+")))
for messages like
09:47 <bridge> {john} I am not on IRC
to be reformatted into
09:47 <john> I am not on IRC
```


```
New formatting commands.
Most IRC clients (including rcirc) support basic formatting using
control codes. Under the 'C-c C-f' prefix a few commands have been
added to insert these automatically. For example, if a region is
active and 'C-c C-f C-b' is invoked, markup is inserted for the region
to be highlighted in bold.
```


Remember when ornery graybeard *ircII* users would shout at mIRC users for using colors in channels? Now you can shout at mIRC users in boldface.

## Imenu

`'imenu' is now bound to 'M-g i' globally.`


I prefer `M-i`

. It’s bound to `tab-to-tab-stop`

, which is beyond useless. Nevertheless, it’s about time they bind one of the most useful navigational aids to a key.

```
New function 'imenu-flush-cache'.
Use it if you want Imenu to forget the buffer's index alist and
recreate it anew next time 'imenu' is invoked.
```


This is of interest to major mode programmers.

```
Emacs is now capable of abandoning a window's redisplay that takes too long.
This is controlled by the new variable 'max-redisplay-ticks'. If that
variable is set to a non-zero value, display of a window will be
aborted after that many low-level redisplay operations, thus
preventing Emacs from becoming wedged when visiting files with very
long lines. The default is zero, which disables the feature: Emacs
will wait forever for redisplay to finish. (We believe you won't need
this feature, given the ability to display buffers with very long
lines.)
```


I hope so, too.

## Editing Changes in Emacs 29.1

```
'M-SPC' is now bound to 'cycle-spacing'.
Formerly it invoked 'just-one-space'. The actions performed by
'cycle-spacing' and their order can now be customized via the user
option 'cycle-spacing-actions'.
```


If you didn’t know, this used to set the amount of whitespace around point to just one space. Super-duper command in code and prose: combine with `M-^`

to ‘lift’ the current line to the one above. That’d usually leave excess spacing, which you could then delete with `M-SPC`

.

I recommend you review `cycle-spacing-actions`

now that it’s changed.

```
'zap-to-char' and 'zap-up-to-char' are case-sensitive for upper-case chars.
These commands now behave as case-sensitive for interactive calls when
they are invoked with an uppercase character, regardless of the value
of 'case-fold-search'.
```


Case folding is mostly applied to the likes of isearch and replace-regexp. With it on (the default), Emacs will ignore casing *unless* you enter an uppercase letter. At that point Emacs becomes case-sensitive in search and replace. Great feature and really underrated.

```
'scroll-other-window' and 'scroll-other-window-down' now respect remapping.
These commands (bound to 'C-M-v' and 'C-M-V') used to scroll the other
windows without looking at customizations in that other window. These
functions now check whether they have been rebound in the buffer shown
in that other window, and then call the remapped function instead. In
addition, these commands now also respect the
'scroll-error-top-bottom' user option.
```


I’ve never remapped them, so I never knew there were problems when you did.

```
Indentation of 'cl-flet' and 'cl-labels' has changed.
These forms now indent like this:
(cl-flet ((bla (x)
(* x x)))
(bla 42))
This change also affects 'cl-macrolet', 'cl-flet*' and
'cl-symbol-macrolet'.
```


I have no real opinion on this, but clearly someone did.

```
New user option 'translate-upper-case-key-bindings'.
Set this option to nil to inhibit the default translation of upper
case keys to their lower case variants.
```


If true (default), then Emacs will convert an upper case key binding to a lower case one provided there is no upper case binding. It is, in other words, there to catch mistyped commands. Just leave it as is. It’s a good default.

```
New command 'ensure-empty-lines'.
This command increases (or decreases) the number of empty lines before
point.
```


I can definitely find a user for this in [keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood), where it’s hard to assert the presence or absence of a certain number of things without a lot of diligence.

```
Improved mouse behavior with auto-scrolling modes.
When clicking inside the 'scroll-margin' or 'hscroll-margin' region,
point is now moved only when releasing the mouse button. This no
longer results in a bogus selection, unless the mouse has also been
dragged.
```


`'kill-ring-max' now defaults to 120.`


I never noticed the old limit, to be honest. I couldn’t even tell you what it was.

```
New user option 'yank-menu-max-items'.
Customize this option to limit the number of entries in the menu
"Edit → Paste from Kill Menu". The default is 60.
```


```
New user option 'copy-region-blink-predicate'.
By default, when copying a region with 'kill-ring-save', Emacs only
blinks point and mark when the region is not denoted visually, that
is, when either the region is inactive, or the 'region' face is
indistinguishable from the 'default' face.
Users who would rather enable blinking unconditionally can now set
this user option to 'always'. To disable blinking unconditionally,
either set this option to 'ignore', or set 'copy-region-blink-delay'
to 0.
```


`Performing a pinch gesture on a touchpad now increases the text scale.`


Wait until you find out that Emacs has mouse gestures. `M-x strokes-help`

.

## Show Paren Mode

Show paren mode highlights the matching delimiters at point.

```
New user option 'show-paren-context-when-offscreen'.
When non-nil, if the point is in a closing delimiter and the opening
delimiter is offscreen, shows some context around the opening
delimiter in the echo area. The default is nil.
This option can also be set to the symbols 'overlay' or 'child-frame',
in which case the context is shown in an overlay or child-frame at the
top-left of the current window. The latter option requires a
graphical frame. On non-graphical frames, the context is shown in the
echo area.
```


This is a *great* feature, as it does more than it implies here. I recommend you experiment with it on (or set to `overlay`

or `child-frame`

).

## Comint

Comint is the general term for Emacs’s interface that communicates with sub-processes, like bash or python.

```
'comint-term-environment' is now aware of connection-local variables.
The user option 'comint-terminfo-terminal' and the variable
'system-uses-terminfo' can now be set as connection-local variables to
change the terminal used on a remote host.
```


Connection-local variables are variables, much like buffer-local ones, that are specific to a particular network connection.

```
New user option 'comint-delete-old-input'.
When nil, this prevents comint from deleting the current input when
inserting previous input using '<mouse-2>'. The default is t, to
preserve previous behavior.
```


```
New minor mode 'comint-fontify-input-mode'.
This minor mode is enabled by default in "*shell*" and "*ielm*"
buffers. It fontifies input text according to 'shell-mode' or
'emacs-lisp-mode' font-lock rules. Customize the user options
'shell-fontify-input-enable' and 'ielm-fontify-input-enable' to nil if
you don't want to enable input fontification by default.
```


Handy and a good default. You’ll get free syntax highlighting. It’s already there for the output, but until now, it never worked with the input.

## Mwheel

```
New user options for alternate wheel events.
The user options 'mouse-wheel-down-alternate-event' and
'mouse-wheel-up-alternate-event' as well as the variables
'mouse-wheel-left-alternate-event' and
'mouse-wheel-right-alternate-event' have been added to better support
systems where two kinds of wheel events can be received.
```


## Internationalization

```
The '<Delete>' function key now allows deleting the entire composed sequence.
For the details, see the item about the 'delete-forward-char' command
above.
```


This was covered earlier.

```
New user option 'composition-break-at-point'.
Setting it to a non-nil value temporarily disables automatic
composition of character sequences at point, and thus makes it easier
to edit such sequences by allowing point to "enter" the composed
sequence.
```


```
Support for many old scripts and writing systems.
Emacs now supports, and has language-environments and input methods,
for several dozens of old scripts that were used in the past for
various languages. For each such script Emacs now has font-selection
and character composition rules, a language environment, and an input
method. The newly-added scripts and the corresponding language
environments are:
Tai Tham script and the Northern Thai language environment
Brahmi script and language environment
Kaithi script and language environment
Tirhuta script and language environment
Sharada script and language environment
Siddham script and language environment
Syloti Nagri script and language environment
Modi script and language environment
Baybayin script and Tagalog language environment
Hanunoo script and language environment
Buhid script and language environment
Tagbanwa script and language environment
Limbu script and language environment
Balinese script and language environment
Javanese script and language environment
Sundanese script and language environment
Batak script and language environment
Rejang script and language environment
Makasar script and language environment
Lontara script and language environment
Hanifi Rohingya script and language environment
Grantha script and language environment
Kharoshthi script and language environment
Lepcha script and language environment
Meetei Mayek script and language environment
Adlam script and language environment
Mende Kikakui script and language environment
Wancho script and language environment
Toto script and language environment
Gothic script and language environment
Coptic script and language environment
Mongolian-traditional script and language environment
Mongolian-cyrillic language environment
```


```
The "Oriya" language environment was renamed to "Odia".
This is to follow the change in the official name of the script. The
'oriya' input method was also renamed to 'odia'. However, the old
name of the language environment and the input method are still
supported.
```


```
New Greek translation of the Emacs tutorial.
Type 'C-u C-h t' to select it in case your language setup does not do
so automatically.
```


`New Ukrainian translation of the Emacs tutorial.`


`New Farsi/Persian translation of the Emacs tutorial.`


```
New default phonetic input method for the Tamil language environment.
The default input method for the Tamil language environment is now
"tamil-phonetic" which is a customizable phonetic input method. To
change the input method's translation rules, customize the user option
'tamil-translation-rules'.
```


```
New 'tamil99' input method for the Tamil language.
This supports the keyboard layout specifically designed for the Tamil
language.
```


```
New input method 'slovak-qwerty'.
This is a variant of the 'slovak' input method, which corresponds to
the QWERTY Slovak keyboards.
```


```
New input method 'cyrillic-chuvash'.
This input method is based on the russian-computer input method, and
is intended for typing in the Chuvash language written in the Cyrillic
script.
```


```
New input method 'cyrillic-mongolian'.
This input method is for typing in the Mongolian language using the
Cyrillic script. It is the default input method for the new
Mongolian-cyrillic language environment, see above.
```


## Changes in Specialized Modes and Packages in Emacs 29.1

### Ecomplete

Ecomplete is an address book auto completion tool.

```
New commands 'ecomplete-edit' and 'ecomplete-remove'.
These allow you to (respectively) edit and bulk-remove entries from
the ecomplete database.
```


```
New user option 'ecomplete-auto-select'.
If non-nil and there's only one matching option, auto-select that.
```


```
New user option 'ecomplete-filter-regexp'.
If non-nil, this user option describes what entries not to add to the
database stored on disk.
```


### Auth Source

Auth source is one of Emacs’s secrets stores. It’s used by GNUS and many other programs. I’ve written a detailed article on [keeping secrets in Emacs with GnuPG and Auth Sources](https://www.masteringemacs.org/article/keeping-secrets-in-emacs-gnupg-auth-sources).

```
New user option 'auth-source-pass-extra-query-keywords'.
Whether to recognize additional keyword params, like ':max' and
':require', as well as accept lists of query terms paired with
applicable keywords. This disables most known behavioral quirks
unique to auth-source-pass, such as wildcard subdomain matching.
```


### Dired

Dired is the Emacs Directory Editor, bound to `C-x d`

.

```
'dired-guess-shell-command' moved from dired-x to dired.
This means that 'dired-do-shell-command' will now provide smarter
defaults without first having to require 'dired-x'. See the node
"(emacs) Shell Command Guessing" in the Emacs manual for more details.
```


`dired-x`

was one of those red-headed step children of Dired. It’s always had a long list of really useful features that, somehow, never really made it into the main file, for unknown reasons. That wouldn’t matter if it was loaded by default, but it wasn’t. So you always had two types of Dired users: those who did, and those who did not, know about or use dired-x.

Anyway. This is a welcome change. It’ll offer better guesses for what to do with the file at point.

```
'dired-clean-up-buffers-too' moved from dired-x to dired.
This means that Dired now offers to kill buffers visiting files and
dirs when they are deleted in Dired. Before, you had to require
'dired-x' to enable this behavior. To disable this behavior,
customize the user option 'dired-clean-up-buffers-too' to nil. The
related user option 'dired-clean-confirm-killing-deleted-buffers'
(which see) has also been moved to 'dired'.
```


Controversial default, but a lot of people use dired as the focal point of their work.

```
'dired-do-relsymlink' moved from dired-x to dired.
The corresponding key 'Y' is now bound by default in Dired.
```


```
'dired-do-relsymlink-regexp' moved from dired-x to dired.
The corresponding key sequence '% Y' is now bound by default in Dired.
```


Relative symlinks should’ve been part of dired from day one.

```
'M-G' is now bound to 'dired-goto-subdir'.
Before, that binding was only available if the dired-x package was
loaded.
```


Another useful command worth knowing about.

```
'dired-info' and 'dired-man' moved from dired-x to dired.
The 'dired-info' and 'dired-man' commands have been moved from the
dired-x package to dired. They have also been renamed to
'dired-do-info' and 'dired-do-man'; the old command names are obsolete
aliases.
The keys 'I' ('dired-do-info') and 'N' ('dired-do-man') are now bound
in Dired mode by default. The user options 'dired-bind-man' and
'dired-bind-info' no longer have any effect and are obsolete.
To get the old behavior back and unbind these keys in Dired mode, add
the following to your Init file:
(with-eval-after-load 'dired
(keymap-set dired-mode-map "N" nil)
(keymap-set dired-mode-map "I" nil))
```


These commands will render a groff/troff/lroff ‘man’ file, or a TeXInfo info manual and open it.

```
New command 'dired-do-eww'.
This command visits the file on the current line with EWW.
```


EWW is Emacs’s Web Wowser.

```
'browse-url-of-dired-file' can now call the secondary browser.
When invoked with a prefix arg, this will now call
'browse-url-secondary-browser-function' instead of the default
browser. 'browse-url-of-dired-file' is bound to 'W' by default in
dired mode.
```


Interesting addition. Meanwhile `M-x browse-url`

does not feature this.

```
New user option 'dired-omit-lines'.
This is used by 'dired-omit-mode', and now allows you to hide based on
other things than just the file names.
```


Omit mode hides things you do not wish to see in a dired buffer. Great way to filter out junk.

```
New user option 'dired-mouse-drag-files'.
If non-nil, dragging file names with the mouse in a Dired buffer will
initiate a drag-and-drop session allowing them to be opened in other
programs.
```


I use the mouse often in other programs, and drag and drop is in that weird sweet spot for me, speed-wise, where dragging in and out of Emacs is a desirable thing to be able to do.

```
New user option 'dired-free-space'.
Dired will now, by default, include the free space in the first line
instead of having it on a separate line. To get the previous behavior
back, say:
(setopt dired-free-space 'separate)
```


```
New user option 'dired-make-directory-clickable'.
If non-nil (which is the default), hitting 'RET' or 'mouse-1' on
the directory components at the directory displayed at the start of
the buffer will take you to that directory.
```


```
Search and replace in Dired/Wdired supports more regexps.
For example, the regexp ".*" will match only characters that are part
of the file name. Also "^.*$" can be used to match at the beginning
of the file name and at the end of the file name. This is used only
when searching on file names. In Wdired this can be used when the new
user option 'wdired-search-replace-filenames' is non-nil (which is the
default).
```


Great change. The search scope for regexp in dired and [wdired](https://www.masteringemacs.org/article/wdired-editable-dired-buffers) is now confined to the filename, which is infinitely more useful than the previous behavior.

### Elisp

```
New command 'elisp-eval-region-or-buffer' (bound to 'C-c C-e').
This command evals the forms in the active region or in the whole buffer.
```


Great addition, as `M-x eval-buffer`

was never bound to anything.

```
New commands 'elisp-byte-compile-file' and 'elisp-byte-compile-buffer'.
These commands (bound to 'C-c C-f' and 'C-c C-b', respectively)
byte-compile the visited file and the current buffer, respectively.
```


Also useful if you rely on the byte compiler to flag common mistakes.

### Games

Emacs ships with a range of [fun computer games](https://www.masteringemacs.org/article/fun-games-in-emacs).

```
New user option 'tetris-allow-repetitions'.
This controls how randomness is implemented (whether to use pure
randomness as before, or to use a bag).
```


### Battery

The Battery library concerns tooling related to laptop batteries.

```
New user option 'battery-update-functions'.
This can be used to trigger actions based on the battery status.
```


### DocView

DocView is Emacs’s image and document converter. It converts all manner of documents to simple images so you can browse them in Emacs.

```
doc-view can now generate SVG images when viewing PDF files.
If Emacs is built with SVG support, doc-view can generate SVG files
when using MuPDF as the converter for PDF files, which generally leads
to sharper images (especially when zooming), and allows customization
of background and foreground color of the page via the new user
options 'doc-view-svg-background' and 'doc-view-svg-foreground'. To
activate this behavior, set 'doc-view-mupdf-use-svg' to non-nil if
your Emacs has SVG support. Note that, with some versions of MuPDF,
SVG generation is known to sometimes produce SVG files that are buggy
or can take a long time to render.
```


SVG support is a nice addition, thanks to Emacs’s support for libsvg.

### Enriched Mode

Enriched mode (“Rich-Text Format”, to others) is a useful little mode if you want basic WYSIWYG-style document editing.

```
New command 'enriched-toggle-markup'.
This allows you to see the markup in 'enriched-mode' buffers (e.g.,
the "HELLO" file). Bound to 'M-o m' by default.
```


### Shell Script Mode

```
New user option 'sh-indent-statement-after-and'.
This controls how statements like the following are indented:
foo &&
bar
```


```
New Flymake backend using the ShellCheck program.
It is enabled by default, but requires that the external "shellcheck"
command is installed.
```


Shellcheck’s amazing for shell script writers of all stripes. Do not write bash or sh scripts without it.

### CC Mode

`C++ Mode now supports most of the new features in the C++20 Standard.`


```
In Objective-C Mode, no extra types are recognized by default.
The default value of 'objc-font-lock-extra-types' has been changed to
nil, since too many identifiers were getting misfontified as types.
This may cause some actual types not to get fontified. To get the old
behavior back, customize the user option to the value suggested in its
doc string.
```


### Cperl Mode

```
New user option 'cperl-file-style'.
This option determines the indentation style to be used. It can also
be used as a file-local variable.
```


### Gud

GUD is the Grand Unified Debugger. A frontend for a range of debuggers.

```
'gud-go' is now bound to 'C-c C-v'.
If given a prefix, it will prompt for an argument to use for the
run/continue command.
```


```
'perldb' now recognizes '-E'.
As of Perl 5.10, 'perl -E 0' behaves like 'perl -e 0' but also activates
all optional features of the Perl version in use. 'perldb' now uses
this invocation as its default.
```


### Customize

`M-x customize`

is Emacs’s configuration tool.

```
New command 'custom-toggle-hide-all-widgets'.
This is bound to 'H' and toggles whether to hide or show the widget
contents.
```


### Diff Mode

```
New user option 'diff-whitespace-style'.
Sets the value of the buffer-local variable 'whitespace-style' in
'diff-mode' buffers. By default, this variable is '(face trailing)',
which preserves behavior of previous Emacs versions.
```


```
New user option 'diff-add-log-use-relative-names'.
If non-nil insert file names in ChangeLog skeletons relative to the
VC root directory.
```


### Ispell

```
'ispell-region' and 'ispell-buffer' now push the mark.
These commands push onto the mark ring the location of the last
misspelled word where corrections were offered, so that you can then
skip back to that location with 'C-x C-x'.
```


You can pop the mark with `C-u C-SPC`

and return from whence you came.

### Dabbrev

Although dynamic abbrev is powerful, I prefer [Hippie Expand](https://www.masteringemacs.org/article/text-expansion-hippie-expand).

`New function 'dabbrev-capf' for use on 'completion-at-point-functions'.`


```
New user option 'dabbrev-ignored-buffer-modes'.
Buffers with major modes in this list will be ignored. By default,
this includes "binary" buffers like 'archive-mode' and 'image-mode'.
```


### Package

Package is Emacs’s package manager.

```
New command 'package-upgrade'.
This command allows you to upgrade packages without using 'list-packages'.
A package that comes with the Emacs distribution can only be upgraded
after you install, once, a newer version from ELPA via the
package-menu displayed by 'list-packages'.
```


```
New command 'package-upgrade-all'.
This command allows upgrading all packages without any queries.
A package that comes with the Emacs distribution will only be upgraded
by this command after you install, once, a newer version of that
package from ELPA via the package-menu displayed by 'list-packages'.
```


Convenience commands, really. Nice to have.

```
New commands 'package-recompile' and 'package-recompile-all'.
These commands can be useful if the ".elc" files are out of date
(invalid byte code and macros).
```


```
New DWIM action on 'x' in "*Packages*" buffer.
If no packages are marked, 'x' will install the package under point if
it isn't already, and remove it if it is installed. Customize the new
option 'package-menu-use-current-if-no-marks' to the nil value to get
back the old behavior of signaling an error in that case.
```


I’d probably turn it off. Seems easy to fat finger and delete something.

```
New command 'package-vc-install'.
Packages can now be installed directly from source by cloning from
their repository.
```


Many of us have been waiting for this feature. It checks out – using VC, Emacs’s generic version control frontend – a repository and installs it as a package.

Unfortunately, it does not plug into `use-package`

.

```
New command 'package-vc-install-from-checkout'.
An existing checkout can now be loaded via package.el, by creating a
symbolic link from the usual package directory to the checkout.
```


This is really handy for those of us who develop packages and want to test that it all works.

```
New command 'package-vc-checkout'.
Used to fetch the source of a package by cloning a repository without
activating the package.
```


```
New command 'package-vc-prepare-patch'.
This command allows you to send patches to package maintainers, for
packages checked out using 'package-vc-install'.
```


Handy – I look forward to seeing if this gets used.

```
New command 'package-report-bug'.
This command helps you compose an email for sending bug reports to
package maintainers, and is bound to 'b' in the "*Packages*" buffer.
```


Also very nice. And a good way of acknowledging the role that repositories play in the package ecosystem in Emacs today.

```
New user option 'package-vc-selected-packages'.
By customizing this user option you can specify specific packages to
install.
```


```
New user option 'package-install-upgrade-built-in'.
When enabled, 'package-install' will include in the list of
upgradeable packages those built-in packages (like Eglot and
use-package, for example) for which a newer version is available in
package archives, and will allow installing those newer versions. By
default, this is disabled; however, if 'package-install' is invoked
with a prefix argument, it will act as if this new option were
enabled.
In addition, when this option is non-nil, built-in packages for which
a new version is available in archives can be upgraded via the package
menu produced by 'list-packages'. If you do set this option non-nil,
we recommend not to use the 'U' command, but instead to use '/ u' to
show the packages which can be upgraded, and then decide which ones of
them you actually want to update from the archives.
If you customize this option, we recommend you place its non-default
setting in your early-init file.
```


The thing this solves is this: how should Emacs handle upgrades to packages it ships with? I recommend you cautiously decide whether to upgrade builtin packages or not.

### Emacs Sessions (Desktop)

Desktop mode saves your Emacs session and restores it when you restart Emacs.

```
New user option to load a locked desktop if locking Emacs is not running.
The option 'desktop-load-locked-desktop' can now be set to the value
'check-pid', which means to allow loading a locked ".emacs.desktop"
file if the Emacs process which locked it is no longer running on the
local machine. This allows avoiding questions about locked desktop
files when the Emacs session which locked it crashes, or was otherwise
interrupted and didn't exit gracefully. See the "(emacs) Saving
Emacs Sessions" node in the Emacs manual for more details.
```


### Miscellaneous

```
New command 'scratch-buffer'.
This command switches to the "*scratch*" buffer. If "*scratch*" doesn't
exist, the command creates it first. You can use this command if you
inadvertently delete the "*scratch*" buffer.
```


Weirdly useful, this. I like the scratch buffer.

### Debugging

```
'q' in a "*Backtrace*" buffer no longer clears the buffer.
Instead it just buries the buffer and switches the mode from
'debugger-mode' to 'backtrace-mode', since commands like 'e' are no
longer available after exiting the recursive edit.
```


A quality of life change more than anything.

```
New user option 'debug-allow-recursive-debug'.
This user option controls whether the 'e' (in a "*Backtrace*"
buffer or while edebugging) and 'C-x C-e' (while edebugging) commands
lead to a (further) backtrace. By default, this variable is nil,
which is a change in behavior from previous Emacs versions.
```


```
'e' in edebug can now take a prefix arg to pretty-print the results.
When invoked with a prefix argument, as in 'C-u e', this command will
pop up a new buffer and show the full pretty-printed value there.
```


I like this a lot. Pretty printing output is still a bit poor in Emacs, in my opinion.

```
'C-x C-e' now interprets a non-zero prefix arg to pretty-print the results.
When invoked with a non-zero prefix argument, as in 'C-u C-x C-e',
this command will pop up a new buffer and show the full pretty-printed
value there.
```


```
You can now generate a backtrace from Lisp errors in redisplay.
To do this, set the new variable 'backtrace-on-redisplay-error' to a
non-nil value. The backtrace will be written to a special buffer
named "*Redisplay-trace*". This buffer will not be automatically
displayed in a window.
```


### Compile

`M-x compile`

is a generic compilation system with error highlighting, and more. See [Compiling and running scripts in Emacs](https://www.masteringemacs.org/article/compiling-running-scripts-emacs).

```
New user option 'compilation-hidden-output'.
This regular expression can be used to make specific parts of
compilation output invisible.
```


Can come in handy if you deal with noisy build output

```
The 'compilation-auto-jump-to-first-error' user option has been extended.
It can now have the additional values 'if-location-known' (which will
only jump if the location of the first error is known), and
'first-known' (which will jump to the first known error location).
```


Now *that* is helpful. It’s worth your time trying that out if you are a regular user of compile, as I am.

```
New user option 'compilation-max-output-line-length'.
Lines longer than the value of this option will have their ends
hidden, with a button to reveal the hidden text. This speeds up
operations like grepping on files that have few newlines. The default
value is 400; set to nil to disable hiding.
```


This should help stop things like minified files from gumming up everything.

### Flymake

Flymake is the on-the-fly syntax and linter frontend. There is also [Flycheck, a Flymake replacement](https://www.masteringemacs.org/article/spotlight-flycheck-a-flymake-replacement).

`New user option 'flymake-mode-line-lighter'.`


The mode line’s become a dumping ground for every little minor mode or feature, so being able to easily remove the overly verbose “Flymake” string is welcome.

I had to resort to all manner of trickery to hide it before. See [hiding and replacing modeline strings with clean-mode-line](https://www.masteringemacs.org/article/hiding-replacing-modeline-strings).

```
New minor mode 'word-wrap-whitespace-mode' for extending 'word-wrap'.
This mode switches 'word-wrap' on, and breaks on all the whitespace
characters instead of just 'SPC' and 'TAB'.
```


```
New mode, 'emacs-news-mode', for editing the NEWS file.
This mode adds some highlighting, makes the 'M-q' command aware of the
format of NEWS entries, and has special commands for doing maintenance
of the Emacs NEWS files. In addition, this mode turns on
'outline-minor-mode', and thus displays customizable icons (see
'icon-preference') in the margins. To disable these icons, set
'outline-minor-mode-use-buttons' to a nil value.
```


### Kmacro

KMacro is Emacs’s macro recorder or, more accurately, the extensions built in top of the original. You can do an awful lot of cool stuff with them: [Keyboard Macros are Misunderstood](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood).

```
Kmacros are now OClosures and have a new constructor 'kmacro' which
uses the 'key-parse' syntax. It replaces the old 'kmacro-lambda-form'
(which is now declared obsolete).
```


This shouldn’t affect any existing, recorded macros.

```
savehist.el can now truncate variables that are too long.
An element of user option 'savehist-additional-variables' can now be
of the form '(VARIABLE . MAX-ELTS)', which means to truncate the
VARIABLE's value to at most MAX-ELTS elements (if the value is a list)
before saving the value.
```


### Minibuffer and Completions

Minibuffer completion’s a dizzying array of options now. I’ve written a guide on [understanding minibuffer completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion) if you want to know more.

```
New commands for navigating completions from the minibuffer.
When the minibuffer is the current buffer, typing 'M-<up>' or
'M-<down>' selects a previous/next completion candidate from the
"*Completions*" buffer and inserts it to the minibuffer.
When the user option 'minibuffer-completion-auto-choose' is nil,
'M-<up>' and 'M-<down>' do the same, but without inserting
a completion candidate to the minibuffer, then 'M-RET' can be used
to choose the currently active candidate from the "*Completions*"
buffer and exit the minibuffer. With a prefix argument, 'C-u M-RET'
inserts the currently active candidate to the minibuffer, but doesn't
exit the minibuffer. These keys are also available for in-buffer
completion, but they don't insert candidates automatically, you need
to type 'M-RET' to insert the selected candidate to the buffer.
```


If you use the *Completions* buffer to help select matches – one of many possible workflows – then you’re likely to find this selection mechanism a useful alternative to the cumbersome methods of picking and choosing from that buffer before.

If you use a fancy type-as-you-complete completion framework, then you’re not likely to benefit from this change at all.

```
Choosing a completion with a prefix argument doesn't exit the minibuffer.
This means that typing 'C-u RET' on a completion candidate in the
"*Completions*" buffer inserts the completion into the minibuffer,
but doesn't exit the minibuffer.
```


Niche use, but the completion system’s flexible and omnipresent, as you can ‘enter’ the completion mechanism using any number of features in Emacs, such as `M-x shell`

, where the ability to repeatedly insert matches is useful.

```
The "*Completions*" buffer can now be automatically selected.
To enable this behavior, customize the user option
'completion-auto-select' to t, then pressing 'TAB' will switch to the
"*Completions*" buffer when it pops up that buffer. If the value is
'second-tab', then the first 'TAB' will display "*Completions*", and
the second one will switch to the "*Completions*" buffer.
```


This feature also plays into the *Completions* buffer workflow. I’ve never been a huge fan of mucking around with manually selecting stuff, preferring instead to type my way to an answer and then only use the buffer as a popup of remaining choices.

```
New user option 'completion-auto-wrap'.
When non-nil, the commands 'next-completion' and 'previous-completion'
automatically wrap around on reaching the beginning or the end of
the "*Completions*" buffer.
```


```
New values for the 'completion-auto-help' user option.
There are two new values to control the way the "*Completions*" buffer
behaves after pressing a 'TAB' if completion is not unique. The value
'always' updates or shows the "*Completions*" buffer after any attempt
to complete. The value 'visual' is like 'always', but only updates
the completions if they are already visible. The default value t
always hides the completion buffer after some completion is made.
```


All this controls is how or when the buffer is shown, which is again down to the specifics of your completion setup. If you want the buffer to only appear when you tab twice, now you can.

```
New commands to complete the minibuffer history.
'minibuffer-complete-history' ('C-x <up>') is like 'minibuffer-complete'
but completes on the history items instead of the default completion
table. 'minibuffer-complete-defaults' ('C-x <down>') completes
on the list of default items.
```


```
User option 'minibuffer-eldef-shorten-default' is now obsolete.
Customize the user option 'minibuffer-default-prompt-format' instead.
```


```
New user option 'completions-sort'.
This option controls the sorting of the completion candidates in
the "*Completions*" buffer. Available styles are no sorting,
alphabetical (the default), or a custom sort function.
```


Sort order is weirdly important, as you can sort by frequency, context, etc. I expect this feature will prove enduring and popular going forward.

```
New user option 'completions-max-height'.
This option limits the height of the "*Completions*" buffer.
```


Instead of toying with `display-buffer-alist`

, you can now set this height directly.

```
New user option 'completions-header-format'.
This is a string to control the header line to show in the
"*Completions*" buffer before the list of completions.
If it contains "%s", that is replaced with the number of completions.
If nil, the header line is not shown.
```


```
New user option 'completions-highlight-face'.
When this user option names a face, the current
candidate in the "*Completions*" buffer is highlighted with that face.
The nil value disables this highlighting. The default is to highlight
using the 'completions-highlight' face.
```


```
You can now define abbrevs for the minibuffer modes.
'minibuffer-mode-abbrev-table' and
'minibuffer-inactive-mode-abbrev-table' are now defined.
```


That’s actually quite helpful. [Abbrev](https://www.masteringemacs.org/article/correcting-typos-misspellings-abbrev) is meant for simple typos and word replacements, and indeed they can happen anywhere, even in the minibuffer.

### Isearch and Replace

```
Changes in how Isearch responds to 'mouse-yank-at-point'.
If a user does 'C-s' and then uses '<mouse-2>' ('mouse-yank-primary')
outside the echo area, Emacs will, by default, end the Isearch and
yank the text at mouse cursor. But if 'mouse-yank-at-point' is
non-nil, the text will now be added to the Isearch instead.
```


```
Changes for values 'no' and 'no-ding' of 'isearch-wrap-pause'.
Now with these values the search will wrap around not only on repeating
with 'C-s C-s', but also after typing a character.
```


Isearch will by default wrap around and start anew if you double-tap `C-s`

at the end of the search.

```
New user option 'char-fold-override'.
Non-nil means that the default definitions of equivalent characters
are overridden.
```


The character folding feature (turning one character into another, for the purposes of ease of searching) is governed by this, new, variable, and `char-fold-[include/exclude]`

.

```
New command 'describe-char-fold-equivalences'.
It displays character equivalences used by 'char-fold-to-regexp'.
```


This command is an intuitive display of what a character is folded to, if anything.

```
New command 'isearch-emoji-by-name'.
It is bound to 'C-x 8 e RET' during an incremental search. The
command accepts the Unicode name of an Emoji (for example, "smiling
face" or "heart with arrow"), like 'C-x 8 e e', with minibuffer
completion, and adds the Emoji into the search string.
```


Oddly specific, but… OK.

### GDB/MI

```
New user option 'gdb-debuginfod-enable-setting'.
On capable platforms, GDB 10.1 and later can download missing source
and debug info files from special-purpose servers, called "debuginfod
servers". Use this new option to control whether 'M-x gdb' instructs
GDB to download missing files from debuginfod servers when you debug
the corresponding programs. The default is to ask you at the
beginning of each debugging session whether to download the files for
that session.
```


### Glyphless Characters

```
New minor mode 'glyphless-display-mode'.
This allows an easy way to toggle seeing all glyphless characters in
the current buffer.
```


```
The extra slot of 'glyphless-char-display' can now have cons values.
The extra slot of the 'glyphless-char-display' char-table can now have
values that are cons cells, specifying separate values for text-mode
and GUI terminals.
```


```
"Replacement character" feature for undisplayable characters on TTYs.
The 'acronym' method of displaying glyphless characters on text-mode
frames treats single-character acronyms specially: they are displayed
without the surrounding '[..]' "box", thus in effect treating such
"acronyms" as replacement characters.
```


### Registers

Registers are single-character short-hands that can store a wide range of things, including strings, numbers, points, window configurations, and much more.

```
Buffer names can now be stored in registers.
For instance, to enable jumping to the "*Messages*" buffer with
'C-x r j m':
(set-register ?m '(buffer . "*Messages*"))
```


Neat addition.

### Pixel Fill

`This is a new package that deals with filling variable-pitch text.`


```
New function 'pixel-fill-region'.
This fills the region to be no wider than a specified pixel width.
```


### Info

`Command 'info-apropos' now takes a prefix argument to search for regexps.`


Great command, and worth knowing about, as it’ll free-form search *all* known Info manuals. See [Full text searching in Info mode with Apropos](https://www.masteringemacs.org/article/full-text-searching-info-mode-apropos).

```
New command 'Info-goto-node-web' and key binding 'G'.
This will take you to the "gnu.org" web server's version of the current
info node. This command only works for the Emacs and Emacs Lisp manuals.
```


Convenient shortcut if you want to give someone a link to a manual page.

### Shortdoc

Shortdoc is Emacs’s extensible cheat sheet for elisp. See [Emacs’s Builtin Elisp Cheat Sheet](https://www.masteringemacs.org/article/emacs-builtin-elisp-cheat-sheet).

```
New command 'shortdoc-copy-function-as-kill' bound to 'w'.
It copies the name of the function near point into the kill ring.
```


```
'N' and 'P' are now bound to 'shortdoc-{next,previous}-section'.
This is in addition to the old keybindings 'C-c C-n' and 'C-c C-p'.
```


### VC

VC is Emacs’s generic Version Control system that works with all major and minor version control systems. They’re bound to `C-x v`

. I love VC, even though I use Magit with Git for 95% of what I do.

It works really well and offers a unified view of all version control systems it supports.

```
New command 'vc-pull-and-push'.
This commands first does a "pull" command, and if that is successful,
does a "push" command afterwards. Currently supported in Git and Bzr.
```


Handy time saver.

```
'C-x v b' prefix key is used now for branch commands.
'vc-print-branch-log' is bound to 'C-x v b l', and new commands are
'vc-create-branch' ('C-x v b c') and 'vc-switch-branch' ('C-x v b s').
The VC Directory buffer now uses the prefix 'b' for these branch-related
commands.
```


This is a great set of features, and if you use VC, you should definitely learn them.

```
New command 'vc-dir-mark-by-regexp' bound to '% m' and '* %'.
This command marks files based on a regexp. If given a prefix
argument, unmark instead.
```


Much like dired. Note that this is meant to be run in `C-x v d`

, the dired-style VC buffer.

```
New command 'C-x v !' ('vc-edit-next-command').
This prefix command requests editing of the next VC shell command
before execution. For example, in a Git repository, you can produce a
log of more than one branch by typing 'C-x v ! C-x v b l' and then
appending additional branch names to the 'git log' command.
The intention is that this command can be used to access a wide
variety of version control system-specific functionality from VC
without complexifying either the VC command set or the backend API.
```


```
'C-x v v' in a diffs buffer allows to commit only some of the changes.
This command is intended to allow you to commit only some of the
changes you have in your working tree. Begin by creating a buffer
with the changes against the last commit, e.g. with 'C-x v D'
('vc-root-diff'). Then edit the diffs to remove the hunks you don't
want to commit. Finally, type 'C-x v v' in that diff buffer to commit
only part of your changes, those whose hunks were left in the buffer.
```


Partial commits of hunks is a great feature of Magit, and I am happy to see it in VC also.

```
'C-x v v' on an unregistered file will now use the most specific backend.
Previously, if you had an SVN-covered "~/" directory, and a Git-covered
directory in "~/foo/bar", using 'C-x v v' on a new, unregistered file
"~/foo/bar/zot" would register it in the SVN repository in "~/" instead of
in the Git repository in "~/foo/bar". This makes this command
consistent with 'vc-responsible-backend'.
```


```
Log Edit now fontifies long Git commit summary lines.
Writing shorter summary lines avoids truncation in contexts in which
Git commands display summary lines. See the two new user options
'vc-git-log-edit-summary-target-len' and 'vc-git-log-edit-summary-max-len'.
```


```
New 'log-edit-headers-separator' face.
It is used to style the line that separates the 'log-edit' headers
from the 'log-edit' summary.
```


```
The function 'vc-read-revision' accepts a new MULTIPLE argument.
If non-nil, multiple revisions can be queried. This is done using
'completing-read-multiple'.
```


```
New function 'vc-read-multiple-revisions'.
This function invokes 'vc-read-revision' with a non-nil value for
MULTIPLE.
```


```
New command 'vc-prepare-patch'.
Patches for any version control system can be prepared using VC. The
command will query what commits to send and will compose messages for
your mail user agent. The behavior of 'vc-prepare-patch' can be
modified by the user options 'vc-prepare-patches-separately' and
'vc-default-patch-addressee'.
```


### Message

Message is Emacs’s Message mode intended for e-mails and suchlike.

```
New user option 'mml-attach-file-at-the-end'.
If non-nil, 'C-c C-a' will put attached files at the end of the message.
```


Don’t forget that you can drag files into a message buffer.

`Message Mode now supports image yanking.`


```
New user option 'message-server-alist'.
This controls automatic insertion of the "X-Message-SMTP-Method"
header before sending a message.
```


### HTML Mode

`HTML Mode now supports "text/html" and "image/*" yanking.`


Not much to say: great addition. Now I just have to remember that it can do this.

### Texinfo Mode

```
'texinfo-mode' now has a specialized 'narrow-to-defun' definition.
It narrows to the current node.
```


### EUDC

EUDC is a directory client frontend for various protocols, such as LDAP. If you work in a corporate environment, you’re probably using LDAP. You can use EUDC to talk to Microsoft Exchange (or FreeIPA, or …) and pull out contracts and whatnot from it. Powerful stuff.

```
Deprecations planned for next release.
After Emacs 29.1, some aspects of EUDC will be deprecated. The goal
of these deprecations is to simplify EUDC server configuration by
making 'eudc-server-hotlist' the only place to add servers. There
will not be a need to set the server using the 'eudc-set-server'
command. Instead, the 'eudc-server-hotlist' user option should be
customized to have an entry for the server. The plan is to obsolete
the 'eudc-hotlist' package since Customize is sufficient for changing
'eudc-server-hotlist'. How the 'eudc-server' user option works in this
context is to-be-determined; it can't be removed, because that would
break compatibility, but it may become synchronized with
'eudc-server-hotlist' so that 'eudc-server' is always equal to '(car
eudc-server-hotlist)'. The first entry in 'eudc-server-hotlist' is the
first server tried by 'eudc-expand-try-all'. The hotlist
simplification will allow 'eudc-query-form' to show a drop down of
possible servers, instead of requiring a call to 'eudc-set-server'
like it does in this release. The default value of
'eudc-ignore-options-file' will be changed from nil to t.
```


```
New user option 'eudc-ignore-options-file' that defaults to nil.
The 'eudc-ignore-options-file' user option can be configured to ignore
the 'eudc-options-file' (typically "~/.emacs.d/eudc-options"). Most
users should configure this to t and put EUDC configuration in the
main Emacs initialization file ("~/.emacs" or "~/.emacs.d/init.el").
```


```
'eudc-expansion-overwrites-query' to 'eudc-expansion-save-query-as-kill'.
The user option 'eudc-expansion-overwrites-query' is renamed to
'eudc-expansion-save-query-as-kill' to reflect the actual behavior of
the user option. The former is kept as alias.
```


```
New command 'eudc-expand-try-all'.
This command can be used in place of 'eudc-expand-inline'. It takes a
prefix argument that causes 'eudc-expand-try-all' to return matches
from all servers instead of just the matches from the first server to
return any. This is useful for example, if one wants to search LDAP
for a name that happens to match a contact in one's BBDB.
```


```
New behavior and default for user option 'eudc-inline-expansion-format'.
EUDC inline expansion result formatting defaulted to
("%s %s <%s>" firstname name email)
Since email address specifications need to comply with RFC 5322 in
order to be useful in messages, there was a risk of producing syntax
which was standard with RFC 822, but is marked as obsolete syntax by
its successor RFC 5322. Also, the first and last name part was never
enclosed in double quotes, potentially producing invalid address
specifications, which may be rejected by a receiving MTA. Thus, this
variable can now additionally be set to nil (the new default), or a
function. In both cases, the formatted result will be in compliance
with RFC 5322. When set to nil, a default format very similar to the
old default will be produced. When set to a function, that function
is called, and the returned values are used to populate the phrase and
comment parts (see RFC 5322 for definitions). In both cases, the
phrase part will be automatically quoted if necessary.
```


```
New function 'eudc-capf-complete' with 'message-mode' integration.
EUDC can now contribute email addresses to 'completion-at-point' by
adding the new function 'eudc-capf-complete' to
'completion-at-point-functions' in 'message-mode'.
```


The missing link that ties EUDC into Emacs’s general-purpose completion framework called “capf” (short for `completion-at-point-functions`

)

```
Additional attributes of query and results in eudcb-macos-contacts.el.
The EUDC back-end for the macOS Contacts app now provides a wider set
of attributes to use for queries, and delivers more attributes in
query results.
```


```
New back-end for ecomplete.
A new back-end for ecomplete allows information from that database to
be queried by EUDC, too. The attributes present in the EUDC query are
used to select the entry type in the ecomplete database.
```


```
New back-end for mailabbrev.
A new back-end for mailabbrev allows information from that database to
be queried by EUDC, too. Only the attributes 'email', 'name', and
'firstname' are supported.
```


### EWW/SHR

EWW is Emacs’s Web Wowser. SHR is the renderer that powers it.

```
New user option to automatically rename EWW buffers.
The 'eww-auto-rename-buffer' user option can be configured to rename
rendered web pages by using their title, URL, or a user-defined
function which returns a string. For the first two cases, the length
of the resulting name is controlled by the user option
'eww-buffer-name-length'. By default, no automatic renaming is
performed.
```


```
New user option 'shr-allowed-images'.
This complements 'shr-blocked-images', but allows specifying just the
allowed images.
```


```
New user option 'shr-use-xwidgets-for-media'.
If non-nil (and Emacs has been built with support for xwidgets),
display <video> elements with an xwidget. Note that this is
experimental; it is known to crash Emacs on some systems, and just
doesn't work on other systems. Also see etc/PROBLEMS.
```


If you compile Emacs with xwidget support, then maybe — just maybe – you might be able to watch a video link in your EWW buffer.

```
New user option 'eww-url-transformers'.
These are used to alter an URL before using it. By default it removes
the common "utm_" trackers from URLs.
```


### Find Dired

Who needs `find`

and `xargs`

when you have [Dired, the find & xargs replacement](https://www.masteringemacs.org/article/dired-shell-commands-find-xargs-replacement)?

```
New command 'find-dired-with-command'.
This enables users to run 'find-dired' with an arbitrary command,
enabling running commands previously unsupported and also enabling new
commands to be built on top.
```


### Gnus

For some, GNUS is a news, mail, and rss reader; for others, it’s a lifestyle.

```
Tool bar changes in Gnus/Message.
There were previously two styles of tool bars available in Gnus and
Message, referred to as 'gnus-summary-tool-bar-retro',
'gnus-group-tool-bar-retro' and 'message-tool-bar-retro', and
'gnus-summary-tool-bar-gnome', 'gnus-group-tool-bar-gnome' and
'message-tool-bar-gnome'. The "retro" tool bars have been removed (as
well as the icons used), and the "gnome" tool bars are now the only
pre-defined toolbars.
```


```
'gnus-summary-up-thread' and 'gnus-summary-down-thread' bindings removed.
The 'gnus-summary-down-thread' binding to 'M-C-d' was shadowed by
'gnus-summary-read-document', and these commands are also available on
'T u' and 'T d' respectively.
```


```
Gnus now uses a variable-pitch font in the headers by default.
To get the monospace font back, you can put something like the
following in your ".gnus" file:
(set-face-attribute 'gnus-header nil :inherit 'unspecified)
```


`The default value of 'gnus-treat-fold-headers' is now 'head'.`


```
New face 'gnus-header'.
All other 'gnus-header-*' faces inherit from this face now.
```


```
New user option 'gnus-treat-emojize-symbols'.
If non-nil, symbols that have an Emoji representation will be
displayed as emojis. The default is nil.
```


```
New command 'gnus-article-emojize-symbols'.
This is bound to 'W D e' and will display symbols that have Emoji
representation as Emoji.
```


```
New mu backend for gnus-search.
Configuration is very similar to the notmuch and namazu backends. It
supports the unified search syntax.
```


Interesting. `mu`

is a standalone mail indexer, and `mu4e`

a mail reader on top of it. So it’s perhaps possible, then, to use GNUS for mail reading, and outsource storing and indexing?

```
'gnus-html-image-cache-ttl' is now a seconds count.
Formerly it was a pair of numbers '(A B)' that represented 65536*A + B,
to cater to older Emacs implementations that lacked bignums.
The older form still works but is undocumented.
```


### Rmail

Rmail is yet another way of interacting with email in Emacs.

```
Rmail partial summaries can now be applied one on top of the other.
You can now narrow the set of messages selected by Rmail summary's
criteria (recipients, topic, senders, etc.) by making a summary of the
already summarized messages. For example, invoking
'rmail-summary-by-senders', followed by 'rmail-summary-by-topic' will
produce a summary where both the senders and the topic are according
to your selection. The new user option
'rmail-summary-progressively-narrow' controls whether the stacking of
the filters is in effect; customize it to a non-nil value to enable
this feature.
```


```
New Rmail summary: by thread.
The new command 'rmail-summary-by-thread' produces a summary of
messages that belong to a single thread of discussion.
```


### EIEIO

EIEIO is Elisp’s CLOS-style object oriented system. It’s also a nursery rhyme.

Old MacDonald had a farm…


`'slot-value' can now be used to access slots of 'cl-defstruct' objects.`


### Align

Align is Emacs’s text alignment facility.

```
Alignment in 'text-mode' has changed.
Previously, 'M-x align' didn't do anything, and you had to say 'C-u
M-x align' for it to work. This has now been changed. The default
regexp for 'C-u M-x align-regexp' has also been changed to be easier
for inexperienced users to use.
```


### Help

Help is, well, help. It’s the mode you interact with when you ask Emacs for help.

```
New mode, 'emacs-news-view-mode', for viewing the NEWS file.
This mode is used by the 'C-h N' command, and adds buttons to manual
entries and symbol references.
```


```
New user option 'help-link-key-to-documentation'.
When this option is non-nil (which is the default), key bindings
displayed in the "*Help*" buffer will be linked to the documentation
for the command they are bound to. This does not affect listings of
key bindings and functions (such as 'C-h b').
```


More interlinking is always a good thing. I’m glad they’re spending more time improving this in recent Emacsen.

### Info Look

```
info-look specs can now be expanded at run time instead of a load time.
The new ':doc-spec-function' element can be used to compute the
':doc-spec' element when the user asks for info on that particular
mode (instead of at load time).
```


### Ansi Color

Ansi color is Emacs’s rather tired and limited ANSI color feature.

```
Support for ANSI 256-color and 24-bit colors.
256-color and 24-bit color codes are now handled by ANSI color
filters and displayed with the specified color.
```


### Term Mode

Term is Emacs’s terminal emulator. Not to be confused with shells!

```
New user option 'term-bind-function-keys'.
If non-nil, 'term-mode' will pass the function keys on to the
underlying shell instead of using the normal Emacs bindings.
```


```
Support for ANSI 256-color and 24-bit colors, italic and other fonts.
'term-mode' can now display 256-color and 24-bit color codes. It can
also handle ANSI codes for faint, italic and blinking text, displaying
it with new 'term-{faint,italic,slow-blink,fast-blink}' faces.
```


### Project

Project is the latest in a long, *long* list of project management solutions built into Emacs. This one seems to have a bit more staying power than the others before it (filesets, CEDET’s project management suite EDE, filecache, …) and that is a good thing.

Emacs has sorely lacked a proper project manager that people can rally behind.

```
'project-find-file' and 'project-or-external-find-file' can include all.
The commands 'project-find-file' and 'project-or-external-find-file'
now accept a prefix argument, which is interpreted to mean "include
all files".
```


```
New command 'project-list-buffers' bound to 'C-x p C-b'.
This command displays a list of buffers from the current project.
```


Scoping buffers to the project is good. Shame it’s not using `M-x ibuffer`

.

```
'project-kill-buffers' can display the list of buffers to kill.
Customize the user option 'project-kill-buffers-display-buffer-list'
to enable the display of the buffer list.
```


```
New user option 'project-vc-extra-root-markers'.
Use it to add detection of nested projects (inside a VCS repository),
or projects outside of VCS repositories.
As a consequence, the 'VC project backend' is formally renamed to
'VC-aware project backend'.
```


```
New user option 'project-vc-include-untracked'.
If non-nil, files untracked by a VCS are considered to be part of
the project by a VC project based on that VCS.
```


### Xref

Xref is the cross-referencing tool that replaced the rather poor and cumbersome “TAGS” search machinery.

```
New command 'xref-go-forward'.
It is bound to 'C-M-,' and jumps to the location where you previously
invoked 'xref-go-back' ('M-,', also known as 'xref-pop-marker-stack').
```


```
The depth of the Xref marker stack is now infinite.
The implementation of the Xref marker stack was changed in a way that
allows as many places to be saved on the stack as needed, limited only
by the available memory. Therefore, the variables
'find-tag-marker-ring-length' and 'xref-marker-ring-length' are now
obsolete and unused; setting them has no effect.
```


Not sure I ever knew, much less reached, the old limit.

```
'xref-query-replace-in-results' prompting change.
This command no longer prompts for FROM when called without prefix
argument. This makes the most common case faster: replacing entire
matches.
```


`New command 'xref-find-references-and-replace' to rename one identifier.`


Handy, as it saves on typing.

`New variable 'xref-current-item' (renamed from a private version).`


`New function 'xref-show-xrefs'.`


```
'outline-minor-mode' is supported in Xref buffers.
You can enable outlining by adding 'outline-minor-mode' to
'xref-after-update-hook'.
```


I didn’t know I wanted this in my life, but… I do! that’s a neat feature. And, just sayin’, if it weren’t for this NEWS entry, nobody – ever – would figure this out.

### File Notifications

Emacs can stay updated on file system changes thanks to a range of OS-specific mechanisms.

`The new command 'file-notify-rm-all-watches' removes all file notifications.`


### Sql

```
Sql now supports sending of passwords in-process.
To improve security, if an sql product has ':password-in-comint' set
to t, a password supplied via the minibuffer will be sent in-process,
as opposed to via the command-line.
```


### Image Mode

```
New command 'image-transform-fit-to-window'.
This command fits the image to the current window by scaling down or
up as necessary. Unlike 'image-transform-fit-both', this can scale
the image up as well as down. It is bound to 's w' in Image Mode by
default.
```


I do use the Image mode feature in Emacs, but I’ve never had to scale an image up; but it’s good to know it’s there.

```
New command 'image-mode-wallpaper-set'.
This command sets the desktop background to the current image. It is
bound to 'W' in Image Mode by default.
```


I live in Emacs; it may as well be my wallpaper.

```
'image-transform-fit-to-{height,width}' are now obsolete.
Use the new command 'image-transform-fit-to-window' instead.
The keybinding for 'image-transform-fit-to-width' is now 's i'.
```


```
User option 'image-auto-resize' can now be set to 'fit-window'.
This works like 'image-transform-fit-to-window'.
```


```
New user option 'image-auto-resize-max-scale-percent'.
The new 'fit-window' option will never scale an image more than this
much (in percent). It is nil by default, which means no limit.
```


```
New user option 'image-text-based-formats'.
This controls whether or not to show a message, when opening certain
image formats, explaining how to edit it as text. The default is to
show this message for SVG and XPM.
```


```
New command 'image-transform-set-percent'.
It allows resizing the image to a percentage of its original size, and
is bound to 's p' in Image mode.
```


```
'image-transform-original' renamed to 'image-transform-reset-to-original'.
The old name was confusing, and is now an obsolete function alias.
```


```
'image-transform-reset' renamed to 'image-transform-reset-to-initial'.
The old name was confusing, and is now an obsolete function alias.
```


### Images

```
New commands 'image-crop' and 'image-cut'.
These commands allow interactively cropping/cutting the image at
point. The commands are bound to keys 'i c' and 'i x' (respectively)
in the local keymap over images. They rely on external programs, by
default "convert" from ImageMagick, to do the actual cropping/eliding
of the image file.
```


```
New commands 'image-flip-horizontally' and 'image-flip-vertically'.
These commands horizontally and vertically flip the image under point,
and are bound to 'i h' and 'i v', respectively.
```


```
Users can now add special image conversion functions.
This is done via 'image-converter-add-handler'.
```


### Image Dired

Yep, image dired is a thing. It’ll generate thumbnails of images and display them alongside the file.

```
'image-dired-image-mode' is now based on 'image-mode'.
This avoids converting images in the background, and makes Image-Dired
noticeably faster. New keybindings from 'image-mode' are now
available in the "*image-dired-display-image*" buffer; press '?' or
'h' in that buffer to see the full list.
```


This is just a consolidation of code.

```
Navigation and marking commands now work in image display buffer.
The following new bindings have been added:
- 'n', 'SPC' => 'image-dired-display-next'
- 'p', 'DEL' => 'image-dired-display-previous'
- 'm' => 'image-dired-mark-thumb-original-file'
- 'd' => 'image-dired-flag-thumb-original-file'
- 'u' => 'image-dired-unmark-thumb-original-file'
```


They have been sorely missed. I never quite understood why they couldn’t do this before. I ended up writing my own glue code to do this.

```
New command 'image-dired-unmark-all-marks'.
It removes all marks from all files in the thumbnail and the
associated Dired buffer, and is bound to 'U' in the thumbnail and
display buffer.
```


```
New command 'image-dired-do-flagged-delete'.
It deletes all flagged files, and is bound to 'x' in the thumbnail
buffer. It replaces the command 'image-dired-delete-marked', which is
now an obsolete alias.
```


```
New command 'image-dired-copy-filename-as-kill'.
It copies the name of the marked or current image to the kill ring,
and is bound to 'w' in the thumbnail buffer.
```


```
New command 'image-dired-wallpaper-set'.
This command sets the desktop background to the image at point in the
thumbnail buffer. It is bound to 'W' by default.
```


```
'image-dired-slideshow-start' is now bound to 'S'.
It is bound in both the thumbnail and display buffer, and no longer
prompts for a timeout; use a numerical prefix (e.g. 'C-u 8 S') to set
the timeout.
```


```
New user option 'image-dired-marking-shows-next'.
If this option is non-nil (the default), marking, unmarking or
flagging an image in either the thumbnail or display buffer shows the
next image.
```


```
New face 'image-dired-thumb-flagged'.
If 'image-dired-thumb-mark' is non-nil (the default), this face is
used for images that are flagged for deletion in the Dired buffer
associated with Image-Dired.
```


```
Image information is now shown in the header line of the thumbnail buffer.
This replaces the message that most navigation commands in the
thumbnail buffer used to show at the bottom of the screen.
```


```
New specifiers for 'image-dired-display-properties-format'.
This is used to format the new header line. The new specifiers are:
"%d" for the name of the directory that the file is in, "%n" for
file's number in the thumbnail buffer, and "%s" for the file size.
The default format has been updated to use this. If you prefer the
old format, add this to your Init file:
(setopt image-dired-display-properties-format "%b: %f (%t): %c")
```


```
New faces for the header line of the thumbnail buffer.
These faces correspond to different parts of the header line, as
specified in 'image-dired-display-properties-format':
- 'image-dired-thumb-header-directory-name'
- 'image-dired-thumb-header-file-name'
- 'image-dired-thumb-header-file-size'
- 'image-dired-thumb-header-image-count'
```


```
PDF support.
Image-Dired now displays thumbnails for PDF files. Type 'RET' on a
PDF file in the thumbnail buffer to visit the corresponding PDF.
```


```
Support GraphicsMagick command line tools.
Support for the GraphicsMagick command line tool ("gm") has been
added, and is used when it is available instead of ImageMagick.
```


```
Support Thumbnail Managing Standard v0.9.0 (Dec 2020).
This standard allows sharing generated thumbnails across different
programs. Version 0.9.0 adds two larger thumbnail sizes: 512x512 and
1024x1024 pixels. See the user option 'image-dired-thumbnail-storage'
to use it; it is not enabled by default.
```


```
Reduce dependency on external "exiftool" program.
The 'image-dired-copy-with-exif-file-name' command no longer requires
an external "exiftool" program to be available. The user options
'image-dired-cmd-read-exif-data-program' and
'image-dired-cmd-read-exif-data-options' are now obsolete.
```


```
Support for bookmark.el.
The command 'bookmark-set' (bound to 'C-x r m') is now supported in
the thumbnail view, and will create a bookmark that opens the current
directory in Image-Dired.
```


Nifty addition to Emacs’s general-purpose bookmarking tool.

```
The 'image-dired-slideshow-start' command no longer prompts.
It no longer inconveniently prompts for a number of images and a
delay: it runs indefinitely, but stops automatically on any command.
You can set the delay with a prefix argument, or a negative prefix
argument to prompt for a delay. Customize the user option
'image-dired-slideshow-delay' to change the default from 5 seconds.
```


```
'image-dired-show-all-from-dir-max-files' increased to 1000.
This user option controls asking for confirmation when starting
Image-Dired in a directory with many files. Since Image-Dired creates
thumbnails in the background in recent versions, this is not as
important as it used to be. You can now also customize this option to
nil to disable this confirmation completely.
```


`'image-dired-thumb-size' increased to 128.`


`'image-dired-db-file' renamed to 'image-dired-tags-db-file'.`


```
'image-dired-display-image-mode' renamed to 'image-dired-image-mode'.
The corresponding keymap is now named 'image-dired-image-mode-map'.
```


```
Some commands have been renamed to be shorter.
- 'image-dired-display-thumbnail-original-image' has been renamed to
'image-dired-display-this'.
- 'image-dired-display-next-thumbnail-original' has been renamed to
'image-dired-display-next'.
- 'image-dired-display-previous-thumbnail-original' has been renamed
to 'image-dired-display-previous'.
The old names are now obsolete aliases.
```


```
'image-dired-thumb-{height,width}' are now obsolete.
Customize 'image-dired-thumb-size' instead, which will set both the
height and width.
```


```
HTML image gallery generation is now obsolete.
The 'image-dired-gallery-generate' command and these user options are
now obsolete: 'image-dired-gallery-thumb-image-root-url',
'image-dired-gallery-hidden-tags', 'image-dired-gallery-dir',
'image-dired-gallery-image-root-url'.
```


```
'image-dired-rotate-thumbnail-{left,right}' are now obsolete.
Instead, use commands 'image-dired-refresh-thumb' to generate a new
thumbnail, or 'image-rotate' to rotate the thumbnail without updating
the thumbnail file.
```


```
Some commands and user options are now obsolete.
Since 'image-dired-display-image-mode' is now based on 'image-mode',
some commands and user options are no longer needed and are now obsolete:
'image-dired-cmd-create-temp-image-options',
'image-dired-cmd-create-temp-image-program',
'image-dired-display-current-image-full',
'image-dired-display-current-image-sized',
'image-dired-display-window-height-correction',
'image-dired-display-window-width-correction',
'image-dired-temp-image-file'.
```


```
New function 'exif-field'.
This is a convenience function to extract the field data from
'exif-parse-file' and 'exif-parse-buffer'.
```


### Bookmarks

Bookmarks is Emacs’s general-purpose bookmark facility. Nearly anything can be bookmarked, recalled and edited. It’s a powerful feature, and greatly underused. Try bookmarking: files, eww buffers, info node buffers, dired, image dired, and more.

```
'list-bookmarks' now includes a type column.
Types are registered via a 'bookmark-handler-type' symbol property on
the jumping function.
```


```
'bookmark-sort-flag' can now be set to 'last-modified'.
This will display bookmark list from most recently set to least
recently set.
```


```
When editing a bookmark annotation, 'C-c C-k' will now cancel.
It is bound to the new command 'bookmark-edit-annotation-cancel'.
```


```
New user option 'bookmark-fringe-mark'.
This option controls the bitmap used to indicate bookmarks in the
fringe (or nil to disable showing this marker).
```


### Xwidget

Xwidget is an optional, compiled module that – in theory – grants access to ‘widgets’ like Chromium in Emacs. I say *in theory*, as it can be quite unstable.

```
New user option 'xwidget-webkit-buffer-name-format'.
This option controls how xwidget-webkit buffers are named.
```


```
New user option 'xwidget-webkit-cookie-file'.
This option controls whether the xwidget-webkit buffers save cookies
set by web pages, and if so, in which file to save them.
```


```
New minor mode 'xwidget-webkit-edit-mode'.
When this mode is enabled, self-inserting characters and other common
web browser shortcut keys are redefined to send themselves to the
WebKit widget.
```


```
New minor mode 'xwidget-webkit-isearch-mode'.
This mode acts similarly to incremental search, and allows searching
the contents of a WebKit widget. In xwidget-webkit mode, it is bound
to 'C-s' and 'C-r'.
```


Seems useful, if it behaves like isearch does elsewhere.

```
New command 'xwidget-webkit-browse-history'.
This command displays a buffer containing the page load history of
the current WebKit widget, and allows you to navigate it.
```


```
On X, the WebKit inspector is now available inside xwidgets.
To access the inspector, right click on the widget and select "Inspect
Element".
```


```
"Open in New Window" in a WebKit widget's context menu now works.
The newly created buffer will be displayed via 'display-buffer', which
can be customized through the usual mechanism of 'display-buffer-alist'
and friends.
```


### Tramp

Tramp is the remote connection tool in Emacs. It’s excellent, and one of my favorite features.

```
New connection methods "docker", "podman" and "kubernetes".
They allow accessing containers provided by Docker and similar
programs.
```


Great feature additions. Now you can trivially `cd`

into a docker container from [Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell), from `find-file`

, or anywhere else that accepts a filepath.

```
Tramp supports abbreviating remote home directories now.
When calling 'abbreviate-file-name' on a Tramp file name, the result
will abbreviate the user's home directory, for example by abbreviating
"/ssh:user@host:/home/user" to "/ssh:user@host:~".
```


```
New user option 'tramp-use-scp-direct-remote-copying'.
When set to non-nil, Tramp does not copy files between two remote
hosts via a local copy in its temporary directory, but lets the 'scp'
command do this job.
```


```
Proper password prompts for methods "doas", "sudo" and "sudoedit".
The password prompts for these methods reflect now the credentials of
the user requesting such a connection, and not of the user who is the
target. This has always been needed, just the password prompt and the
related 'auth-sources' entry were wrong.
```


```
New user option 'tramp-completion-use-cache'.
During user and host name completion in the minibuffer, results from
Tramp's connection cache are taken into account. This can be disabled
by setting the user option 'tramp-completion-use-cache' to nil.
```


### Browse URL

Browse url opens up an URL in your browser.

```
New user option 'browse-url-default-scheme'.
This user option decides which URL scheme that 'browse-url' and
related functions will use by default. For example, you could
customize this to "https" to always prefer HTTPS URLs.
```


```
New user option 'browse-url-irc-function'.
This option specifies a function for opening "irc://" links. It
defaults to the new function 'browse-url-irc'.
```


```
New function 'browse-url-irc'.
This multipurpose autoloaded function can be used for opening "irc://"
and "ircs://" URLS by any caller that passes a URL string as an initial
arg.
```


```
Support for the Netscape web browser has been removed.
This support has been obsolete since Emacs 25.1. The final version of
the Netscape web browser was released in February, 2008.
```


```
Support for the Galeon web browser has been removed.
This support has been obsolete since Emacs 25.1. The final version of
the Galeon web browser was released in September, 2008.
```


```
Support for the Mozilla web browser is now obsolete.
Note that this historical web browser is different from Mozilla
Firefox; it is its predecessor.
```


### Python Mode

```
Project shells and a new user option 'python-shell-dedicated'.
When called with a prefix argument, 'run-python' now offers the choice
of creating a shell dedicated to the current project. This shell runs
in the project root directory and is shared among all project buffers.
Without a prefix argument, the kind of shell (buffer-dedicated,
project-dedicated or global) is specified by the new
'python-shell-dedicated' user option.
```


A welcome addition. This is the benefit of having a builtin *and* well-supported project tool in Emacs.

### Ruby Mode

`New user option 'ruby-toggle-block-space-before-parameters'.`


`Support for endless methods.`


```
New user options that determine indentation logic.
'ruby-method-params-indent', 'ruby-block-indent',
'ruby-after-operator-indent', 'ruby-method-call-indent',
'ruby-parenless-call-arguments-indent'. See the docstrings for
explanations and examples.
```


### Eshell

Eshell is Emacs’s shell written in elisp.

```
New feature to easily bypass Eshell's own pipelining.
Prefixing '|', '<' or '>' with an asterisk, i.e. '*|', '*<' or '*>',
will cause the whole command to be passed to the operating system
shell. This is particularly useful to bypass Eshell's own pipelining
support for pipelines which will move a lot of data. See section
"Running Shell Pipelines Natively" in the Eshell manual, node
"(eshell) Pipelines".
```


Pipelining in eshell was never all that feature complete; it could also be slow. These redirections allow us to circumvent eshell in favor of a shell that implements it correctly – and expediently.

```
New module to help supplying absolute file names to remote commands.
After enabling the new 'eshell-elecslash' module, typing a forward
slash as the first character of a command line argument will
automatically insert the Tramp prefix. The automatic insertion
applies only when 'default-directory' is remote and the command is a
Lisp function. This frees you from having to keep track of whether
commands are Lisp function or external when supplying absolute file
name arguments. See the "(eshell) Electric forward slash" node in the
Eshell manual for details.
```


One annoyance about `cd`

’ing into a remote directory in Tramp was always how easy it was to accidentally `cd`

*out* of it again. This will go some way towards alleviating that.

```
Improved support for redirection operators in Eshell.
Eshell now supports a wider variety of redirection operators. For
example, you can now redirect both stdout and stderr via '&>' or
duplicate one output handle to another via 'NEW-FD>&OLD-FD'. For more
information, see the "(eshell) Redirection" node in the Eshell manual.
```


```
New eshell built-in command 'doas'.
The privilege-escalation program 'doas' has been added to the existing
'su' and 'sudo' commands from the 'eshell-tramp' module. The external
command may still be accessed by using '*doas'.
```


`doas`

is slowly taking over as a smaller – safer – alternative to the sprawling `sudo`

program.

```
Double-quoting an Eshell expansion now treats the result as a single string.
If an Eshell expansion like '$FOO' is surrounded by double quotes, the
result will always be a single string, no matter the type that would
otherwise be returned.
```


```
Concatenating Eshell expansions now works more similarly to other shells.
When concatenating an Eshell expansion that returns a list, "adjacent"
elements of each operand are now concatenated together,
e.g. '$(list "a" "b")c' returns '("a" "bc")'. See the "(eshell)
Expansion" node in the Eshell manual for more details.
```


```
Eshell subcommands with multiline numeric output return lists of numbers.
If every line of the output of an Eshell subcommand like '${COMMAND}'
is numeric, the result will be a list of numbers (or a single number
if only one line of output). Previously, this only converted numbers
when there was a single line of output.
```


```
Built-in Eshell commands now follow Posix/GNU argument syntax conventions.
Built-in commands in Eshell now accept command-line options with
values passed as a single token, such as '-oVALUE' or
'--option=VALUE'. New commands can take advantage of this with the
'eshell-eval-using-options' macro. See "Defining new built-in
commands" in the "(eshell) Built-ins" node of the Eshell manual.
```


```
Eshell globs ending with "/" now match only directories.
Additionally, globs ending with "**/" or "***/" no longer raise an
error, and now expand to all directories recursively (following
symlinks in the latter case).
```


```
Lisp forms in Eshell now treat a nil result as a failed exit status.
When executing a command that looks like '(lisp form)' and returns
nil, Eshell will set the exit status (available in the '$?'
variable) to 2. This allows commands like that to be used in
conditionals. To change this behavior, customize the new
'eshell-lisp-form-nil-is-failure' user option.
```


### Shell

Shell mode is Emacs’s wrapper around a common shell, usually bash or the cmd.exe on Windows.

```
New user option 'shell-kill-buffer-on-exit'.
Enabling this will automatically kill a "*shell*" buffer as soon as
the shell session terminates.
```


Nope, not for me. I accidentally kill or terminate my shell, and I don’t want to lose the output of the buffer as a result of that.

```
New minor mode 'shell-highlight-undef-mode'.
Customize 'shell-highlight-undef-enable' to t if you want to enable
this minor mode in "*shell*" buffers. It will highlight undefined
commands with a warning face as you type.
```


Seems useful. I’d have to use it for a while to determine how reliable it is.

### Calc

`M-x calc`

is Emacs’s all-powerful symbolic RPN calculator. It’s fantastically advanced, and well worth learning if you do a lot of mathematics.

```
New user option 'calc-kill-line-numbering'.
Set it to nil to exclude line numbering from kills and copies.
```


I always found that annoying, so I am glad there is now a switch to disable it.

### Hierarchy

Hierarchy is a tree list user interface component.

```
Tree Display can delay computation of children.
'hierarchy-add-tree' and 'hierarchy-add-trees' have an optional
argument which allows tree-widget display to be activated and computed
only when the user expands the node.
```


Being able to thunk the calculations of the child node matches should certainly improve performance (or delay computation until it is needed, anyway) but I do not know of too many packages that use hierarchy.

### Proced

Proced is Emacs’s answer to `top`

and `ps`

. [Displaying and Interacting with processes using Proced](https://www.masteringemacs.org/article/displaying-interacting-processes-proced) is a good place to start if you want to learn more.

```
proced.el shows system processes of remote hosts.
When 'default-directory' is remote, and 'proced' is invoked with a
negative argument like 'C-u - proced', the system processes of that
remote host are shown. Alternatively, the user option
'proced-show-remote-processes' can be set to non-nil.
'proced-signal-function' has been marked obsolete.
```


Nifty! You can built a neat little server dashboard with a couple of keyboard macros and some window configurations.

```
Proced can now optionally show process details in color.
New user option 'proced-enable-color-flag' enables coloring of Proced
buffers. This option is disabled by default; customize it to a
non-nil value to enable colors.
```


I’ve enabled it, as it does make things easier to read.

### Miscellaneous

```
New user option 'webjump-use-internal-browser'.
When non-nil, WebJump will use an internal browser to open web pages,
instead of the default external browser.
```


```
New user option 'font-lock-ignore'.
This option provides a mechanism to selectively disable font-lock
keyword-driven fontifications.
```


I can’t immediately discern if this works with tree-sitter based font locking. Probably not, as it uses `font-lock-keywords`

to drive it.

```
New user option 'auto-save-visited-predicate'.
This user option is a predicate function which is called by
'auto-save-visited-mode' to decide whether or not to save a buffer.
You can use it to automatically save only specific buffers, for
example buffers using a particular mode or in some directory.
```


```
New user option 'remote-file-name-inhibit-auto-save-visited'.
If this user option is non-nil, 'auto-save-visited-mode' will not
auto-save remote buffers. The default is nil.
```


```
New package vtable.el for formatting tabular data.
This package allows formatting data using variable-pitch fonts.
The resulting tables can display text in variable pitch fonts, text
using fonts of different sizes, and images. See the "(vtable) Top"
manual for more details.
```


Emacs had long had a package that can tabulate data: `tabulated-list.el`

. This new, and improved version, adds a range of new features.

```
New minor mode 'elide-head-mode'.
Enabling this minor mode turns on hiding header material, like
'elide-head' does; disabling it shows the header. The commands
'elide-head' and 'elide-head-show' are now obsolete.
```


```
New package ansi-osc.el.
Support for OSC ("Operating System Command") escape sequences has been
extracted from comint.el in order to provide interpretation of OSC
sequences in compilation buffers.
Adding the new function 'ansi-osc-compilation-filter' to
'compilation-filter-hook' enables interpretation of OSC escape
sequences in compilation buffers. By default, all sequences are
filtered out.
The list of handlers (already covering OSC 7 and 8) has been extended
with a handler for OSC 2, the command to set a window title.
```


Emacs 27 added better directory tracking support for OSC 8. I wrote about [how to set it up for Shell-mode](https://www.masteringemacs.org/article/running-shells-in-emacs-overview).

```
'recentf-mode' now uses abbreviated file names by default.
This means that e.g. "/home/foo/bar" is now displayed as "~/bar".
Customize the user option 'recentf-filename-handlers' to nil to get
back the old behavior.
```


Recent Files is a capable, little feature. It can recall recently used files at will.

```
New command 'recentf-open'.
This command prompts for a recently opened file in the minibuffer, and
visits it.
```


```
'ffap-machine-at-point' no longer pings hosts by default.
It will now simply look at a hostname to determine if it is valid,
instead of also trying to ping it. Customize the user option
'ffap-machine-p-known' to 'ping' to get the old behavior back.
```


`The 'run-dig' command is now obsolete; use 'dig' instead.`


```
Some 'bib-mode' commands and variables have been renamed.
To respect Emacs naming conventions, the variable 'unread-bib-file'
has been renamed to 'bib-unread-file'. The following commands have
also been renamed:
'addbib' to 'bib-add'
'return-key-bib' to 'bib-return-key'
'mark-bib' to 'bib-mark'
'unread-bib' to 'bib-unread'
```


```
'outlineify-sticky' command is renamed to 'allout-outlinify-sticky'.
The old name is still available as an obsolete function alias.
```


`The url-irc library now understands "ircs://" links.`


```
New command 'world-clock-copy-time-as-kill' for 'world-clock-mode'.
It copies the current line into the kill ring.
```


I betcha didn’t know Emacs had a `M-x world-clock-mode`

. It goes well with `M-x sunrise-sunset`

and `M-x phases-of-moon`

.

```
'edit-abbrevs' now uses font-locking.
The new face 'abbrev-table-name' is used to display the abbrev table
name.
```


```
New key binding 'O' in "*Buffer List*".
This key is now bound to 'Buffer-menu-view-other-window', which will
view this line's buffer in View mode in another window.
```


Nice to have. You should just use `M-x ibuffer`

though.

### Scheme Mode

```
Auto-detection of Scheme library files.
Emacs now automatically enables the Scheme mode when opening R6RS
Scheme Library Source (".sls") files and R7RS Scheme Library
Definition (".sld") files.
```


```
Imenu members for R6RS and R7RS library members.
Imenu now lists the members directly nested in R6RS Scheme libraries
('library') and R7RS libraries ('define-library').
```


### New Modes and Packages in Emacs 29.1

```
Eglot: Emacs Client for the Language Server Protocol.
Emacs now comes with the Eglot package, which enhances various Emacs
features, such as completion, documentation, error detection, etc.,
based on data provided by language servers using the Language Server
Protocol (LSP). See the new Info manual "(eglot) Top" for more. Also
see "etc/EGLOT-NEWS".
If you want to be able to use 'package-install' to upgrade Eglot to
newer versions released on GNU ELPA, customize the new option
'package-install-upgrade-built-in' to a non-nil value.
```


You should *definitely* read the manual for this package if you want to use it. You’ll want to make sure you have the right language server, et al. But, generally speaking, `M-x eglot`

is all you need.

```
use-package: Declarative package configuration.
use-package is now shipped with Emacs. It provides the 'use-package'
macro, which allows you to isolate package configuration in your init
file in a way that is declarative, tidy, and performance-oriented.
See the new Info manual "(use-package) Top" for more.
If you want to be able to use 'package-install' to upgrade use-package
to newer versions released on GNU ELPA, customize the new option
'package-install-upgrade-built-in' to a non-nil value.
```


```
New package 'wallpaper'.
This package provides the command 'wallpaper-set', which sets the
desktop background image. Depending on the system and the desktop,
this may require an external program (such as "swaybg", "gm",
"display" or "xloadimage"). If so, a suitable command should be
detected automatically in most cases. It can also be customized
manually if needed, using the new user options 'wallpaper-command' and
'wallpaper-command-args'.
```


A fine complement to `M-x zone`

, Emacs’s screensaver.

```
New package 'oclosure'.
This allows the creation of OClosures, which are "functions with
slots" or "function objects" that expose additional information about
themselves. Use the new macros 'oclosure-define' and
'oclosure-lambda' to create OClosures. See the "(elisp) OClosures"
node for more information.
```


```
New generic function 'oclosure-interactive-form'.
Used by 'interactive-form' when called on an OClosure.
This allows specific OClosure types to compute their interactive specs
on demand rather than precompute them when created.
```


```
New theme 'leuven-dark'.
This is a dark version of the 'leuven' theme.
```


```
New mode 'erts-mode'.
This mode is used to edit files geared towards testing actions in
Emacs buffers, like indentation and the like. The new ert function
'ert-test-erts-file' is used to parse these files.
```


One of the hardest things about writing tests for a text editor package is having to keep tabs on the point, the text, the window layout, etc. *Anything* that helps make that easier is a win for everyone.

```
New major mode 'js-json-mode'.
This is a lightweight variant of 'js-mode' that is used by default
when visiting JSON files.
```


```
New major mode 'csharp-mode'.
A major mode based on CC Mode for editing programs in the C# language.
This mode is auto-enabled for files with the ".cs" extension.
```


```
New major modes based on the tree-sitter library.
These new major modes are available if Emacs was built with the
tree-sitter library. They provide support for font-locking,
indentation, and navigation by defuns based on parsing the buffer text
by a tree-sitter parser. Some major modes also offer support for
Imenu and 'which-func'.
The new modes based on tree-sitter are for now entirely optional, and
you must turn them on manually, or load them in your init file, or
customize 'auto-mode-alist' to turn them on automatically for certain
files. You can also customize 'major-mode-remap-alist' to
automatically turn on some tree-sitter based modes for the same files
for which a "built-in" mode would be turned on. For example:
(add-to-list 'major-mode-remap-alist '(ruby-mode . ruby-ts-mode))
If you try these modes and don't like them, you can go back to the
"built-in" modes by restarting Emacs. (If you use desktop.el to save
and restore Emacs sessions, make sure no buffer under these modes is
recorded in the desktop file, before restarting.) But please tell us
why you didn't like the tree-sitter based modes, so that we could try
improving them.
Each major mode based on tree-sitter needs a language grammar library,
usually named "libtree-sitter-LANG.so" ("libtree-sitter-LANG.dll" on
MS-Windows), where LANG is the corresponding language name. Emacs
looks for these libraries in the following places:
. in the directories mentioned in the list 'treesit-extra-load-path'
. in the "tree-sitter" subdirectory of your 'user-emacs-directory'
(by default, "~/.emacs.d/tree-sitter")
. in the standard system directories where other shared libraries are
usually installed
We recommend to install these libraries in one of the standard system
locations (the last place in the above list).
If a language grammar library required by a mode is not found in any
of the above places, the mode will display a warning when you try to
turn it on.
```


This is a good summary of what you need to do to start using tree-sitter. But, as I’ve said before, it can be a bit gnarly if you haven’t done this sort of thing before. My guide to [tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) is a good place to start.

```
New major mode 'typescript-ts-mode'.
A major mode based on the tree-sitter library for editing programs
in the TypeScript language.
```


```
New major mode 'tsx-ts-mode'.
A major mode based on the tree-sitter library for editing programs
in the TypeScript language, with support for TSX.
```


Both TSX/TS modes are welcome additions.

```
New major mode 'c-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the C language.
```


```
New major mode 'c++-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the C++ language.
```


```
New command 'c-or-c++-ts-mode'.
A command that automatically guesses the language of a header file,
and enables either 'c-ts-mode' or 'c++-ts-mode' accordingly.
```


```
New major mode 'java-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the Java language.
```


```
New major mode 'python-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the Python language.
```


```
New major mode 'css-ts-mode'.
An optional major mode based on the tree-sitter library for editing
CSS (Cascading Style Sheets).
```


```
New major mode 'json-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the JSON language.
```


```
New major mode 'csharp-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the C# language.
```


```
New major mode 'bash-ts-mode'.
Am optional major mode based on the tree-sitter library for editing
Bash shell scripts.
```


```
New major mode 'dockerfile-ts-mode'.
A major mode based on the tree-sitter library for editing
Dockerfiles.
```


This is Emacs’s first Dockerfile mode. There is no regular mode for it.

```
New major mode 'cmake-ts-mode'.
A major mode based on the tree-sitter library for editing CMake files.
```


```
New major mode 'toml-ts-mode'.
An optional major mode based on the tree-sitter library for editing
files written in TOML, a format for writing configuration files.
```


```
New major mode 'go-ts-mode'.
A major mode based on the tree-sitter library for editing programs in
the Go language.
```


```
New major mode 'go-mod-ts-mode'.
A major mode based on the tree-sitter library for editing "go.mod"
files.
```


```
New major mode 'yaml-ts-mode'.
A major mode based on the tree-sitter library for editing files
written in YAML.
```


This mode is a bit lacking in many areas. There is no indentation, for instance. You may want to use the third-party `yaml`

mode instead.

```
New major mode 'rust-ts-mode'.
A major mode based on the tree-sitter library for editing programs in
the Rust language.
```


```
New major mode 'ruby-ts-mode'.
An optional major mode based on the tree-sitter library for editing
programs in the Ruby language.
```


### Incompatible Lisp Changes in Emacs 29.1

```
The implementation of overlays has changed.
Emacs now uses an implementation of overlays that is much more
efficient than the original one, and should speed up all the
operations that involve overlays, especially when there are lots of
them in a buffer.
As result of this, some minor incompatibilities in behavior could be
observed, as described below. Except those minor incompatibilities,
no other changes in behavior of overlays should be visible on the Lisp
or user level, with the exception of better performance and the order
of overlays returned by functions that don't promise any particular
order.
```


Overlays are ranges of positions in Emacs that you can apply to a buffer and assign all manner of metadata and contextual information. This is how a wide range of Emacs’s features work: from flymake errors to buttons to many other things. Speedups and efficiency gains here pay dividends everywhere else.

```
The function 'overlay-recenter' is now a no-op.
This function does nothing, and in particular has no effect on the
value returned by 'overlay-lists'. The purpose of 'overlay-recenter'
was to allow more efficient lookup of overlays around a certain buffer
position; however with the new implementation the lookup of overlays
is efficient regardless of their position, and there's no longer any
need to "optimize" the lookup, nor any notion of a "center" of the
overlays.
```


```
The function 'overlay-lists' returns one unified list of overlays.
This function used to return a cons of two lists, one with overlays
before the "center" position, the other after that "center". It now
returns a list whose 'car' is the list of all the buffer overlays, and
whose 'cdr' is always nil.
```


```
'format-prompt' now uses 'substitute-command-keys'.
This means that both the prompt and 'minibuffer-default-prompt-format'
will have key definitions and single quotes handled specially.
```


```
New function 'substitute-quotes'.
This function works like 'substitute-command-keys' but only
substitutes quote characters.
```


```
'find-image' now uses 'create-image'.
This means that images found through 'find-image' also have
auto-scaling applied. (This only makes a difference on HiDPI
displays.)
```


```
Changes in how "raw" in-memory XBM images are specified.
Some years back Emacs gained the ability to scale images, and you
could then specify ':width' and ':height' when using 'create-image' on all
image types -- except XBM images, because this format already used the
':width' and ':height' arguments to specify the width/height of the "raw"
in-memory format. This meant that if you used these specifications
on, for instance, XBM files, Emacs would refuse to display them. This
has been changed, and ':width'/':height' now works as with all other image
formats, and the way to specify the width/height of the "raw"
in-memory format is now by using ':data-width' and ':data-height'.
```


```
"loaddefs.el" generation has been reimplemented.
The various "loaddefs.el" files in the Emacs tree (which contain
information about autoloads, built-in packages and package prefixes)
used to be generated by functions in autoloads.el. These are now
generated by loaddefs-gen.el instead. This leads to functionally
equivalent "loaddefs.el" files, but they do not use exactly the same
syntax, so using 'M-x update-file-autoloads' no longer works. (This
didn't work well in most files in the past, either, but it will now
signal an error in any file.)
In addition, files are scanned in a slightly different way.
Previously, ';;;###' specs inside a top-level form (i.e., something
like '(when ... ;;;### ...)' would be ignored. They are now parsed as
usual.
```


```
Themes have special autoload cookies.
All built-in themes are scraped for ';;;###theme-autoload' cookies
that are loaded along with the regular auto-loaded code.
```


```
'buffer-modified-p' has been extended.
This function was previously documented to return only nil or t. This
has been changed to nil/'autosaved'/non-nil. The new 'autosaved'
value means that the buffer is modified, but that it hasn't been
modified since the time of last auto-save.
```


```
'with-silent-modifications' also restores buffer autosave status.
'with-silent-modifications' is a macro meant to be used by the font
locking machinery to allow applying text properties without changing
the modification status of the buffer. However, it didn't restore the
buffer autosave status, so applying font locking to a modified buffer
that had already been auto-saved would trigger another auto-saving.
This is no longer the case.
```


```
'prin1' doesn't always escape "." and "?" in symbols any more.
Previously, symbols like 'foo.bar' would be printed by 'prin1' as
"foo\.bar". This now prints as "foo.bar" instead. The Emacs Lisp
reader interprets these strings as referring to the same symbol, so
this is virtually always backwards-compatible, but there may
theoretically be code out there that expects a specific printed
representation.
The same is the case with the "?" character: The 'foo?' symbol is now
printed as "foo?" instead of "foo\?".
If the "." and "?" characters are the first character in the symbol,
they will still be escaped, so the '.foo' symbol is still printed as
"\.foo" and the '?bar' symbol is still printed as "\?bar".
```


```
Remapping 'mode-line' face no longer works as expected.
'mode-line' is now the parent face of the new 'mode-line-active' face,
and remapping parent of basic faces does not work reliably.
Instead of remapping 'mode-line', you have to remap 'mode-line-active'.
```


```
'make-process' has been extended to support ptys when ':stderr' is set.
Previously, setting ':stderr' to a non-nil value would force the
process's connection to use pipes. Now, Emacs will use a pty for
stdin and stdout if requested no matter the value of ':stderr'.
```


PTYs (pseudo-terminals) are generally much faster and better to use than pipes when you want to interface with a sub-process.

```
User option 'mail-source-ignore-errors' is now obsolete.
The whole mechanism for prompting users to continue in case of
mail-source errors has been removed, so this option is no longer
needed.
```


### Fonts

```
Emacs now supports 'medium' fonts.
Emacs previously didn't distinguish between the 'regular'/'normal'
weight and the 'medium' weight, but it now also supports the (heavier)
'medium' weight. However, this means that if you specify a weight of
'normal' and the font doesn't have this weight, Emacs won't find the
font spec. In these cases, replacing ":weight 'normal" with ":weight
'medium" should fix the issue.
```


Better and more sophisticated font rendering is always a positive. Emacs has made so many strides in this area over the years. Don’t forget that `M-x customize-face default`

is still a good way to experiment with fonts.

```
Keymap descriptions by Help commands have changed.
'help--describe-command', 'C-h b' and associated functions that output
keymap descriptions have changed. In particular, prefix commands are
not output at all, and instead of "??" for closures/functions, these
functions output "[closure]"/"[lambda]". You can get back the old
behavior of including prefix commands by customizing the new option
'describe-bindings-show-prefix-commands' to a non-nil value.
```


```
'downcase' details have changed slightly.
In certain locales, changing the case of an ASCII-range character may
turn it into a multibyte character, most notably with "I" in Turkish
(the lowercase is "ı", 0x0131). Previously, 'downcase' on a unibyte
string was buggy, and would mistakenly just return the lower byte of
this, 0x31 (the digit "1"). 'downcase' on a unibyte string has now
been changed to downcase such characters as if they were ASCII. To
get proper locale-dependent downcasing, the string has to be converted
to multibyte first. (This goes for the other case-changing functions,
too.)
```


```
Functions in 'tramp-foreign-file-name-handler-alist' have changed.
Functions to determine which Tramp file name handler to use are now
passed a file name in dissected form (via 'tramp-dissect-file-name')
instead of in string form.
```


```
'def' indentation changes.
In 'emacs-lisp-mode', forms with a symbol with a name that start with
"def" have been automatically indented as if they were 'defun'-like
forms, for instance:
(defzot 1
2 3)
This heuristic has now been removed, and all functions/macros that
want to be indented this way have to be marked with
(declare (indent defun))
or the like. If the function/macro definition itself can't be
changed, the indentation can also be adjusted by saying something
like:
(put 'defzot 'lisp-indent-function 'defun)
```


```
The 'inhibit-changing-match-data' variable is now obsolete.
Instead, functions like 'string-match' and 'looking-at' now take an
optional INHIBIT-MODIFY argument.
```


```
'gnus-define-keys' is now obsolete.
Use 'define-keymap' instead.
```


```
MozRepl has been removed from js.el.
MozRepl was removed from Firefox in 2017, so this code doesn't work
with recent versions of Firefox.
```


```
The function 'image-dired-get-exif-data' is now obsolete.
Use 'exif-parse-file' and 'exif-field' instead.
```


```
'insert-directory' alternatives should not change the free disk space line.
This change is now applied in 'dired-insert-directory'.
```


```
'compilation-last-buffer' is (finally) declared obsolete.
It has been obsolete since Emacs 22.1, actually.
```


```
Calling 'lsh' now elicits a byte-compiler warning.
'lsh' behaves in somewhat surprising and platform-dependent ways for
negative arguments, and is generally slower than 'ash', which should be
used instead. This warning can be suppressed by surrounding calls to
'lsh' with the construct '(with-suppressed-warnings ((suspicious lsh)) ...)',
but switching to 'ash' is generally much preferable.
```


```
Some functions and variables obsolete since Emacs 24 have been removed:
'Buffer-menu-buffer+size-width', 'Electric-buffer-menu-mode',
'Info-edit-map', 'allout-abbreviate-flattened-numbering',
'allout-exposure-change-hook', 'allout-mode-deactivate-hook',
'allout-structure-added-hook', 'allout-structure-deleted-hook',
'allout-structure-shifted-hook', 'ansi-color-unfontify-region',
'archive-extract-hooks', 'auth-source-forget-user-or-password',
'auth-source-hide-passwords', 'auth-source-user-or-password',
'automatic-hscrolling', 'automount-dir-prefix', 'bibtex-complete',
'bibtex-entry-field-alist', 'buffer-has-markers-at',
'buffer-substring-filters', 'byte-compile-disable-print-circle',
'c-prepare-bug-report-hooks', 'cfengine-mode-abbrevs',
'change-log-acknowledgement', 'chart-map',
'checkdoc-comment-style-hooks', 'comint--unquote&expand-filename',
'comint-dynamic-complete', 'comint-dynamic-complete-as-filename',
'comint-dynamic-simple-complete', 'comint-unquote-filename',
'command-history-map', 'compilation-parse-errors-function',
'completion-annotate-function', 'condition-case-no-debug',
'count-lines-region', 'crisp-mode-modeline-string',
'custom-print-functions', 'cvs-string-prefix-p', 'data-debug-map',
'deferred-action-function', 'deferred-action-list',
'dired-pop-to-buffer', 'dired-shrink-to-fit',
'dired-sort-set-modeline', 'dired-x-submit-report',
'display-buffer-function',
'ediff-choose-window-setup-function-automatically',
'eieio-defgeneric', 'eieio-defmethod', 'emacs-lock-from-exiting',
'erc-complete-word', 'erc-dcc-chat-filter-hook',
'eshell-add-to-window-buffer-names', 'eshell-cmpl-suffix-list',
'eshell-for', 'eshell-remove-from-window-buffer-names',
'eshell-status-in-modeline', 'filesets-cache-fill-content-hooks',
'font-list-limit', 'font-lock-maximum-size',
'font-lock-reference-face', 'gnus-carpal',
'gnus-debug-exclude-variables', 'gnus-debug-files',
'gnus-local-domain', 'gnus-outgoing-message-group',
'gnus-registry-user-format-function-M', 'gnus-secondary-servers',
'gnus-subscribe-newsgroup-hooks', 'gud-inhibit-global-bindings',
'hangul-input-method-inactivate', 'hfy-post-html-hooks',
'image-extension-data', 'image-library-alist',
'inactivate-current-input-method-function', 'inactivate-input-method',
'inhibit-first-line-modes-regexps',
'inhibit-first-line-modes-suffixes', 'input-method-inactivate-hook',
'intdos', 'javascript-generic-mode', 'javascript-generic-mode-hook',
'latex-string-prefix-p', 'macro-declaration-function' (function),
'macro-declaration-function' (variable), 'mail-complete',
'mail-complete-function', 'mail-mailer-swallows-blank-line',
'mail-sent-via', 'make-register', 'makefile-complete',
'menu-bar-kill-ring-save', 'meta-complete-symbol', 'meta-mode-map',
'mh-kill-folder-suppress-prompt-hooks',
'minibuffer-completing-symbol',
'minibuffer-local-filename-must-match-map', 'mode25', 'mode4350',
'mpc-string-prefix-p', 'msb-after-load-hooks',
'nndiary-request-accept-article-hooks',
'nndiary-request-create-group-hooks',
'nndiary-request-update-info-hooks', 'nnimap-split-rule',
'nntp-authinfo-file', 'ns-alternatives-map',
'ns-store-cut-buffer-internal', 'package-menu-view-commentary',
'pascal-last-completions', 'pascal-show-completions',
'pascal-toggle-completions', 'pcomplete-arg-quote-list',
'pcomplete-quote-argument', 'prolog-char-quote-workaround',
'python-buffer', 'python-guess-indent', 'python-indent',
'python-info-ppss-comment-or-string-p', 'python-info-ppss-context',
'python-info-ppss-context-type', 'python-preoutput-result',
'python-proc', 'python-send-receive', 'python-send-string',
'python-use-skeletons', 'quail-inactivate', 'quail-inactivate-hook',
'query-replace-interactive', 'rcirc-activity-hooks',
'rcirc-print-hooks', 'rcirc-receive-message-hooks',
'rcirc-sentinel-hooks', 'read-filename-at-point', 'redraw-modeline',
'reftex-index-map', 'reftex-index-phrases-map',
'reftex-select-bib-map', 'reftex-select-label-map', 'reftex-toc-map',
'register-name-alist', 'register-value', 'report-emacs-bug-info',
'report-emacs-bug-pretest-address',
'rmail-default-dont-reply-to-names', 'rmail-dont-reply-to',
'rmail-dont-reply-to-names', 'robin-inactivate',
'robin-inactivate-hook', 'rst-block-face', 'rst-comment-face',
'rst-definition-face', 'rst-directive-face', 'rst-emphasis1-face',
'rst-emphasis2-face', 'rst-external-face', 'rst-literal-face',
'rst-reference-face', 'semantic-change-hooks',
'semantic-edits-delete-change-hooks',
'semantic-edits-new-change-hooks',
'semantic-edits-reparse-change-hooks', 'semantic-grammar-map',
'semantic-grammar-syntax-table', 'semantic-lex-reset-hooks',
'semanticdb-elisp-sym-function-arglist',
'semanticdb-save-database-hooks', 'set-face-underline-p',
'set-register-value', 'sh-maybe-here-document', 'speedbar-key-map',
'speedbar-syntax-table', 'starttls-any-program-available',
'strokes-modeline-string', 'strokes-report-bug',
'term-default-bg-color', 'term-default-fg-color',
'tex-string-prefix-p', 'timeclock-modeline-display',
'timeclock-modeline-display', 'timeclock-update-modeline',
'toggle-emacs-lock', 'tooltip-use-echo-area', 'turn-on-cwarn-mode',
'turn-on-iimage-mode', 'ucs-input-inactivate', 'ucs-insert',
'url-recreate-url-attributes', 'user-variable-p',
'vc-string-prefix-p', 'vc-toggle-read-only', 'view-return-to-alist',
'view-return-to-alist-update', 'w32-default-color-map' (function),
'which-func-mode' (function), 'window-system-version',
'winner-mode-leave-hook', 'x-cut-buffer-or-selection-value'.
```


```
Some functions and variables obsolete since Emacs 23 have been removed:
'find-emacs-lisp-shadows', 'newsticker-cache-filename',
'process-filter-multibyte-p', 'redisplay-end-trigger-functions',
'set-process-filter-multibyte', 'set-window-redisplay-end-trigger',
'unify-8859-on-decoding-mode', 'unify-8859-on-encoding-mode',
'vc-arch-command', 'window-redisplay-end-trigger', 'x-selection'.
```


```
Some functions and variables obsolete since Emacs 21 or 22 have been removed:
'c-toggle-auto-state', 'find-file-not-found-hooks',
'ls-lisp-dired-ignore-case', 'query-replace-regexp-eval'.
```


```
New generic function 'function-documentation'.
It can dynamically generate a raw docstring depending on the type of a
function. Used mainly for docstrings of OClosures.
```


```
Base64 encoding no longer tolerates latin-1 input.
The functions 'base64-encode-string', 'base64url-encode-string',
'base64-encode-region' and 'base64url-encode-region' no longer accept
characters in the range U+0080..U+00FF as substitutes for single bytes
in the range 128..255, but signal an error for all multibyte characters.
The input must be unibyte encoded text.
```


```
The 'clone-indirect-buffer-hook' is now run by 'make-indirect-buffer'.
It was previously only run by 'clone-indirect-buffer' and
'clone-indirect-buffer-other-window'. Since 'make-indirect-buffer' is
called by both of these, the hook is now run by all 3 of these
functions.
```


```
'?\' at the end of a line now signals an error.
Previously, it produced a nonsense value, -1, that was never intended.
```


```
Some libraries obsolete since Emacs 24.1 and 24.3 have been removed:
abbrevlist.el, assoc.el, complete.el, cust-print.el,
erc-hecomplete.el, mailpost.el, mouse-sel.el, old-emacs-lock.el,
patcomp.el, pc-mode.el, pc-select.el, s-region.el, and sregex.el.
```


```
Many seldom-used generalized variables have been made obsolete.
Emacs has a number of rather obscure generalized variables defined,
that, for instance, allowed you to say things like:
(setf (point-min) 4)
These never caught on and have been made obsolete. The form above,
for instance, is the same as saying
(narrow-to-region 4 (point-max))
The following generalized variables have been made obsolete:
'buffer-file-name', 'buffer-local-value', 'buffer-modified-p',
'buffer-name', 'buffer-string', 'buffer-substring', 'current-buffer',
'current-column', 'current-global-map', 'current-input-mode',
'current-local-map', 'current-window-configuration',
'default-file-modes', 'documentation-property', 'eq', 'frame-height',
'frame-width', 'frame-visible-p', 'global-key-binding',
'local-key-binding', 'mark', 'mark-marker', 'marker-position',
'mouse-position', 'point', 'point-marker', 'point-max', 'point-min',
'read-mouse-position', 'screen-height', 'screen-width',
'selected-frame', 'selected-screen', 'selected-window',
'standard-case-table', 'syntax-table', 'visited-file-modtime',
'window-height', 'window-width', and 'x-get-secondary-selection'.
```


```
The 'dotimes' loop variable can no longer be manipulated in the loop body.
Previously, the 'dotimes' loop counter could be modified inside the
loop body, but only in code using dynamic binding. Now the behavior
is the same as when using lexical binding: changes to the loop
variable have no effect on subsequent iterations. That is,
(dotimes (i 10)
(print i)
(setq i (+ i 6)))
now always prints the numbers 0 .. 9.
```


### Lisp Changes in Emacs 29.1

```
Interpreted closures are "safe for space".
As was already the case for byte-compiled closures, instead of capturing
the whole current lexical environment, interpreted closures now only
capture the part of the environment that they need.
The previous behavior could occasionally lead to memory leaks or
to problems where a printed closure would not be 'read'able because
of an un'read'able value in an unrelated lexical variable.
```


```
New accessor function 'file-attribute-file-identifier'.
It returns the list of the inode number and device identifier
retrieved by 'file-attributes'. This value can be used to identify a
file uniquely. The device identifier can be a single number or (for
remote files) a cons of 2 numbers.
```


```
New macro 'while-let'.
This is like 'when-let', but repeats until a binding form is nil.
```


Useful addition. I’m liking all the `xxx-let`

bindings they’ve been adding over the years. It cuts down on chaff and it retains readability.

```
New function 'make-obsolete-generalized-variable'.
This can be used to mark setters used by 'setf' as obsolete, and the
byte-compiler will then warn about using them.
```


```
New functions 'pos-eol' and 'pos-bol'.
These are like 'line-end-position' and 'line-beginning-position'
(respectively), but ignore fields (and are more efficient).
```


```
New function 'compiled-function-p'.
This returns non-nil if its argument is either a built-in, or a
byte-compiled, or a natively-compiled function object, or a function
loaded from a dynamic module.
```


```
'deactivate-mark' can have new value 'dont-save'.
This value means that Emacs should deactivate the mark as usual, but
without setting the primary selection, if 'select-active-regions' is
enabled.
```


```
New 'declare' form 'interactive-args'.
This can be used to specify what forms to put into 'command-history'
when executing commands interactively.
```


```
The FORM argument of 'time-convert' is mandatory.
'time-convert' can still be called without it, as before, but the
compiler now emits a warning about this deprecated usage.
```


```
Emacs now supports user-customizable and themable icons.
These can be used for buttons in buffers and the like. See the
"(elisp) Icons" and "(emacs) Icons" nodes in the manuals for details.
```


```
New arguments MESSAGE and TIMEOUT of 'set-transient-map'.
MESSAGE specifies a message to display after activating the transient
map, including a special formatting spec to list available keys.
TIMEOUT is the idle time after which to deactivate the transient map.
The default timeout value can be defined by the new variable
'set-transient-map-timeout'.
```


```
New forms 'with-restriction' and 'without-restriction'.
These forms can be used as enhanced alternatives to the
'save-restriction' form combined with, respectively,
'narrow-to-region' and 'widen'. They also accept an optional label
argument, with which labeled narrowings can be created and lifted.
See the "(elisp) Narrowing" node for details.
```


### Connection Local Variables

```
Some connection-local variables are now user options.
The variables 'connection-local-profile-alist' and
'connection-local-criteria-alist' are now user options, in order to
make it more convenient to inspect and modify them.
```


```
New function 'connection-local-update-profile-variables'.
This function allows to modify the settings of an existing
connection-local profile.
```


```
New macro 'with-connection-local-application-variables'.
This macro works like 'with-connection-local-variables', but it allows
using another application instead of 'tramp'. This is useful when
running code in a buffer where Tramp has already set some
connection-local variables.
```


```
New macro 'setq-connection-local'.
This allows dynamically setting variable values for a particular
connection within the body of 'with-connection-local-{application-}variables'.
See the "(elisp) Connection Local Variables" node in the Lisp
Reference manual for more information.
```


```
'plist-get', 'plist-put' and 'plist-member' are no longer limited to 'eq'.
These function now take an optional comparison PREDICATE argument.
```


`'read-multiple-choice' can now use long-form answers.`


`'M-s c' in 'read-regexp' now toggles case folding.`


```
'completing-read' now allows a function as its REQUIRE-MATCH argument.
This function is called to see whether what the user has typed is a
match. This is also available from functions that call
'completing-read', like 'read-file-name'.
```


```
'posn-col-row' can now give position data based on windows.
Previously, it reported data only based on the frame.
```


`'file-expand-wildcards' can now also take a regexp as PATTERN argument.`


`vc-mtn (the VC backend for Monotone) has been made obsolete.`


```
'gui-set-selection' can specify different values for different data types.
If DATA is a string, then its text properties are searched for values
for each specific data type while the selection is being converted.
```


```
New eldoc function 'elisp-eldoc-var-docstring-with-value'.
This function includes the current value of the variable in eldoc display
and can be used as a more detailed alternative to 'elisp-eldoc-var-docstring'.
```


```
'save-some-buffers' can now be extended to save other things.
Traditionally, 'save-some-buffers' saved buffers, and also saved
abbrevs. This has been generalized via the
'save-some-buffers-functions' variable, and packages can now register
things to be saved.
```


```
New function 'string-equal-ignore-case'.
This compares strings ignoring case differences.
```


```
'symbol-file' can now report natively-compiled ".eln" files.
If Emacs was built with native-compilation enabled, Lisp programs can
now call 'symbol-file' with the new optional 3rd argument non-nil to
request the name of the ".eln" file which defined a given symbol.
```


`New macro 'with-memoization' provides a very primitive form of memoization.`


```
'max-char' can now report the maximum codepoint according to Unicode.
When called with a new optional argument UNICODE non-nil, 'max-char'
will now report the maximum valid codepoint defined by the Unicode
Standard.
```


### Seq

Seq is a library that adds a range of functions that operate on all manner of sequences. It’s filled a gaping void that the likes of `dash.el`

also tries to fill.

```
New function 'seq-split'.
This returns a list of sub-sequences of the specified sequence.
```


```
New function 'seq-remove-at-position'.
This function returns a copy of the specified sequence with the
element at a given (zero-based) index removed.
```


```
New function 'seq-positions'.
This returns a list of the (zero-based) indices of elements matching a
given predicate in the specified sequence.
```


```
New function 'seq-keep'.
This is like 'seq-map', but removes all nil results from the returned
list.
```


### Themes

Color themes, that is.

```
New hooks 'enable-theme-functions' and 'disable-theme-functions'.
These are run after enabling and disabling a theme, respectively.
```


```
Themes can now be made obsolete.
Using 'make-obsolete' on a theme is now supported. This will make
'load-theme' issue a warning when loading the theme.
```


```
New hook 'display-monitors-changed-functions'.
It is called whenever the configuration of different monitors on a
display changes.
```


```
'prin1' and 'prin1-to-string' now take an optional OVERRIDES argument.
This argument can be used to override values of print-related settings.
```


```
New minor mode 'header-line-indent-mode'.
This is meant to be used by Lisp programs that show a header line
which should be kept aligned with the buffer contents when the user
switches 'display-line-numbers-mode' on or off, and when the width of
line-number display changes. See the "(elisp) Header Lines" node in
the Emacs Lisp Reference manual for more information.
```


```
New global minor mode 'lost-selection-mode'.
This global minor mode makes Emacs deactivate the mark in all buffers
when the primary selection is obtained by another program.
```


```
On X, Emacs will try to preserve selection ownership when a frame is deleted.
This means that if you make Emacs the owner of a selection, such as by
selecting some text into the clipboard or primary selection, and then
delete the current frame, you will still be able to insert the
contents of that selection into other programs as long as another
frame is open on the same display. This behavior can be disabled by
setting the user option 'x-auto-preserve-selections' to nil.
```


```
New predicate 'char-uppercase-p'.
This returns non-nil if its argument its an uppercase character.
```


### Byte Compilation

```
Byte compilation will now warn about some quoting mistakes in docstrings.
When writing code snippets that contains the "'" character (APOSTROPHE),
that quote character has to be escaped to avoid Emacs displaying it as
"’" (LEFT SINGLE QUOTATION MARK), which would make code examples like
(setq foo '(1 2 3))
invalid. Emacs will now warn during byte compilation if it sees
something like that, and also warn about when using RIGHT/LEFT SINGLE
QUOTATION MARK directly. In both these cases, if these characters
should really be present in the docstring, they should be quoted with
"\=".
```


```
Byte compilation will now warn about some malformed 'defcustom' types.
It is very common to write 'defcustom' types on the form:
:type '(choice (const :tag "foo" 'bar))
I.e., double-quoting the 'bar', which is almost never the correct
value. The byte compiler will now issue a warning if it encounters
these forms.
```


```
'restore-buffer-modified-p' can now alter buffer auto-save state.
With a FLAG value of 'autosaved', it will mark the buffer as having
been auto-saved since the time of last modification.
```


```
New minor mode 'isearch-fold-quotes-mode'.
This sets up 'search-default-mode' so that quote characters are
char-folded into each other. It is used, by default, in "*Help*" and
"*info*" buffers.
```


We talked about this before.

```
New macro 'buffer-local-set-state'.
This is a helper macro to be used by minor modes that wish to restore
buffer-local variables back to their original states when the mode is
switched off.
```


This should help minor mode authors that temporarily alter values restore them to their correct, former values without keeping a copy of the values around.

```
New macro 'with-buffer-unmodified-if-unchanged'.
If the buffer is marked as unmodified, and code does modifications
that, in total, means that the buffer is identical to the buffer
before, mark the buffer as unmodified again.
```


```
New function 'malloc-trim'.
This function allows returning unused memory back to the operating
system, and is mainly meant as a debugging tool. It is currently
available only when Emacs was built with glibc as the C library.
```


```
'x-show-tip' no longer hard-codes a timeout default.
The new variable 'x-show-tooltip-timeout' allows the user to alter
this for packages that don't use 'tooltip-show', but instead call the
lower level function directly.
```


```
New function 'current-cpu-time'.
It gives access to the CPU time used by the Emacs process, for
example for benchmarking purposes.
```


```
New function 'string-edit'.
This is meant to be used when the user has to edit a (potentially)
long string. It pops up a new buffer where you can edit the string,
and the provided callback is called when the user types 'C-c C-c'.
```


Great addition. There’s a wide range of cases in Emacs where that would come in handy.

```
New function 'read-string-from-buffer'.
This is a modal version of 'string-edit', and can be used as an
alternative to 'read-string'.
```


```
The return value of 'clear-message-function' is not ignored anymore.
If the function returns 'dont-clear-message', then the message is not
cleared, with the assumption that the function cleared it itself.
```


```
The local variables section now supports defining fallback modes.
This was previously only available when using a property line (i.e.,
putting the modes on the first line of a file).
```


```
New function 'flush-standard-output'.
This enables display of lines that don't end in a newline from
batch-based Emacs scripts.
```


```
New convenience function 'buttonize-region'.
This works like 'buttonize', but for a region instead of a string.
```


`'macroexp-let2*' can omit TEST argument and use single-var bindings.`


```
New macro-writing macros, 'cl-with-gensyms' and 'cl-once-only'.
See the "(cl) Macro-Writing Macros" manual section for descriptions.
```


```
New variable 'last-event-device' and new function 'device-class'.
On X Windows, 'last-event-device' specifies the input extension device
from which the last input event originated, and 'device-class' can be
used to determine the type of an input device.
```


```
Variable 'track-mouse' can have a new value 'drag-source'.
This means the same as 'dropping', but modifies the mouse position
list in reported motion events if there is no frame underneath the
mouse pointer.
```


```
New functions for dragging items from Emacs to other programs.
The new functions 'x-begin-drag', 'dnd-begin-file-drag',
'dnd-begin-drag-files', and 'dnd-direct-save' allow dragging contents
(such as files and text) from Emacs to other programs.
```


```
New function 'ietf-drums-parse-date-string'.
This function parses RFC5322 (and RFC822) date strings, and should be
used instead of 'parse-time-string' when parsing data that's standards
compliant.
```


```
New macro 'setopt'.
This is like 'setq', but is meant to be used for user options instead
of plain variables, and uses 'custom-set'/'set-default' to set them.
```


Intended as a drop-in replacement for customizable options, as they can have edge triggers that run when the value changes. That is something `setq`

cannot do, which can in rare cases lead to bugs.

```
New utility predicate 'mode-line-window-selected-p'.
This is meant to be used from ':eval' mode line constructs to create
different mode line looks for selected and unselected windows.
```


```
New variable 'messages-buffer-name'.
This variable (defaulting to "*Messages*") allows packages to override
where messages are logged.
```


```
New function 'readablep'.
This function says whether an object can be written out and then
read back by the Emacs Lisp reader.
```


```
New variable 'print-unreadable-function'.
This variable allows changing how Emacs prints unreadable objects.
```


```
The user option 'polling-period' now accepts floating point values.
This means Emacs can now poll for input during Lisp execution more
frequently than once in a second.
```


```
New function 'bidi-string-strip-control-characters'.
This utility function is meant for displaying strings when it is
essential that there's no bidirectional context. It removes all the
bidirectional formatting control characters (such as RLM, LRO, PDF,
etc.) from its argument string. The characters it removes are listed
in the value of 'bidi-control-characters'.
```


```
The Gnus range functions have been moved to a new library, range.el.
All the old names have been made obsolete.
```


```
New function 'function-alias-p'.
This predicate says whether an object is a function alias, and if it
is, the alias chain is returned.
```


`New variable 'lisp-directory' holds the directory of Emacs's own Lisp files.`


```
New facility for handling session state: 'multisession-value'.
This can be used as a convenient way to store (simple) application
state, and the command 'list-multisession-values' allows users to list
(and edit) this data.
```


```
New function 'get-display-property'.
This is like 'get-text-property', but works on the 'display' text
property.
```


```
New function 'add-display-text-property'.
This is like 'put-text-property', but works on the 'display' text
property.
```


```
New 'min-width' 'display' property.
This allows setting a minimum display width for a region of text.
```


```
New 'cursor-face' text property.
This uses 'cursor-face' instead of the default face when cursor is on or
near the character and 'cursor-face-highlight-mode' is enabled. The
user option 'cursor-face-highlight-nonselected-window' is similar to
'highlight-nonselected-windows', but for this property.
```


```
New event type 'touch-end'.
This event is sent whenever the user's finger moves off the mouse
wheel on some mice, or when the user's finger moves off the touchpad.
```


```
New event type 'pinch'.
This event is sent when a user performs a pinch gesture on a touchpad,
which is comprised of placing two fingers on the touchpad and moving
them towards or away from each other.
```


```
New hook 'x-pre-popup-menu-hook'.
This hook is run before 'x-popup-menu' is about to display a
deck-of-cards menu on screen.
```


```
New hook 'post-select-region-hook'.
This hook is run immediately after 'select-active-regions'. It causes
the region to be set as the primary selection.
```


```
New function 'buffer-match-p'.
Check if a buffer satisfies some condition. Some examples for
conditions can be regular expressions that match a buffer name, a
cons-cell like '(major-mode . shell-mode)' that matches any buffer
where 'major-mode' is 'shell-mode' or a combination with a condition
like '(and "\\`\\*.+\\*\\'" (major-mode . special-mode))'.
```


```
New function 'match-buffers'.
It uses 'buffer-match-p' to gather a list of buffers that match a
condition.
```


```
New optional arguments TEXT-FACE and DEFAULT-FACE for 'tooltip-show'.
They allow changing the faces used for the tooltip text and frame
colors of the resulting tooltip frame from the default 'tooltip' face.
```


### Text Security and Suspiciousness

```
New library textsec.el.
This library contains a number of checks for whether a string is
"suspicious". This usually means that the string contains characters
that have glyphs that can be confused with other, more commonly used
glyphs, or contains bidirectional (or other) formatting characters
that may be used to confuse a user.
```


This is back to what I was saying earlier about *confusables*.

```
New user option 'textsec-check'.
If non-nil (which is the default), Emacs packages that are vulnerable
to attackers trying to confuse the users will use the textsec library
to mark suspicious text. For instance shr/eww will mark suspicious
URLs and links, Gnus will mark suspicious From addresses, and
Message mode will query the user if the user is sending mail to a
suspicious address. If this variable is nil, these checks are
disabled.
```


```
New function 'textsec-suspicious-p'.
This is the main function Emacs applications should be using to check
whether a string is suspicious. It heeds the 'textsec-check' user
option.
```


### Keymaps and Key Definitions

```
'where-is-internal' can now filter events marked as non key events.
If a command maps to a key binding like '[some-event]', and 'some-event'
has a symbol plist containing a non-nil 'non-key-event' property, then
that binding is ignored by 'where-is-internal'.
```


```
New functions for defining and manipulating keystrokes.
These all take the syntax defined by 'key-valid-p', which is basically
the same syntax as the one accepted by the 'kbd' macro. None of the
older functions have been deprecated or altered, but they are now
de-emphasized in the documentation, and we encourage Lisp programs to
switch to these new functions.
Use 'keymap-set' instead of 'define-key'.
Use 'keymap-global-set' instead of 'global-set-key'.
Use 'keymap-local-set' instead of 'local-set-key'.
Use 'keymap-global-unset' instead of 'global-unset-key'.
Use 'keymap-local-unset' instead of 'local-unset-key'.
Use 'keymap-substitute' instead of 'substitute-key-definition'.
Use 'keymap-set-after' instead of 'define-key-after'.
Use 'keymap-lookup' instead of 'lookup-key' and 'key-binding'.
Use 'keymap-local-lookup' instead of 'local-key-binding'.
Use 'keymap-global-lookup' instead of 'global-key-binding'.
```


I’m glad they’re thinking about unifying the rather inconsistent key binding system in Emacs, but we’re decades away from ever obsoleting the existing ones. They’re just too ingrained (and they work fine.)

```
'define-key' now takes an optional REMOVE argument.
If non-nil, remove the definition from the keymap. This is subtly
different from setting a definition to nil: when the keymap has a
parent such a definition will shadow the parent's definition.
```


Weirdly, removing (not marking `nil`

or `ignore`

) was quite hard.

```
'read-multiple-choice' now takes an optional SHOW-HELP argument.
If non-nil, show the help buffer immediately, before any user input.
```


```
New function 'key-valid-p'.
The 'kbd' function is quite permissive, and will try to return
something usable even if the syntax of the argument isn't completely
correct. The 'key-valid-p' predicate does a stricter check of the
syntax.
```


```
New function 'key-parse'.
This is like 'kbd', but only returns vectors instead of a mix of
vectors and strings.
```


```
New ':type' for 'defcustom' for keys.
The new 'key' type can be used for options that should be a valid key
according to 'key-valid-p'. The type 'key-sequence' is now obsolete.
```


```
New function 'define-keymap'.
This function allows defining a number of keystrokes with one form.
```


```
New macro 'defvar-keymap'.
This macro allows defining keymap variables more conveniently.
```


```
'defvar-keymap' can specify 'repeat-mode' behavior for the keymap.
Use ':repeat t' to have all bindings be repeatable or for more
advanced usage:
:repeat (:enter (commands ...) :exit (commands ...))
```


```
'kbd' can now be used in built-in, preloaded libraries.
It no longer depends on edmacro.el and cl-lib.el.
```


```
New substitution in docstrings and 'substitute-command-keys'.
Use \\`KEYSEQ' to insert a literal key sequence "KEYSEQ" (for example
\\`C-k') in a docstring or when calling 'substitute-command-keys',
which will use the same face as a command substitution. This should
be used only when a key sequence has no corresponding command, for
example when it is read directly with 'read-key-sequence'. It must be
a valid key sequence according to 'key-valid-p'.
```


```
'lookup-key' is more permissive when searching for extended menu items.
In Emacs 28.1, the behavior of 'lookup-key' was changed: when looking
for a menu item '[menu-bar Foo-Bar]', first try to find an exact
match, then look for the lowercased '[menu-bar foo-bar]'.
This has been extended, so that when looking for a menu item with a
symbol containing spaces, as in '[menu-bar Foo\ Bar]', first look for
an exact match, then the lowercased '[menu-bar foo\ bar]' and finally
'[menu-bar foo-bar]'. This further improves backwards-compatibility
when converting menus to use 'easy-menu-define'.
```


```
New function 'file-name-split'.
This returns a list of all the components of a file name.
```


```
New function 'file-name-parent-directory'.
This returns the parent directory of a file name.
```


```
New macro 'with-undo-amalgamate'.
It records a particular sequence of operations as a single undo step.
```


```
New command 'yank-media'.
This command supports yanking non-plain-text media like images and
HTML from other applications into Emacs. It is only supported in
modes that have registered support for it, and only on capable
platforms.
```


```
New command 'yank-media-types'.
This command lets you examine all data in the current selection and
the clipboard, and insert it into the buffer.
```


```
New variable 'yank-transform-functions'.
This variable allows the user to alter the string to be inserted.
```


```
New command 'yank-in-context'.
This command tries to preserve string/comment syntax when yanking.
```


```
New function 'minibuffer-lazy-highlight-setup'.
This function allows setting up the minibuffer so that lazy
highlighting of its content is applied in the original window.
```


```
New text property 'inhibit-isearch'.
If set, 'isearch' will skip these areas, which can be useful (for
instance) when covering huge amounts of data (that has no meaningful
searchable data, like image data) with a 'display' text property.
```


```
'insert-image' now takes an INHIBIT-ISEARCH optional argument.
It marks the image with the 'inhibit-isearch' text property, which
inhibits 'isearch' matching the STRING argument.
```


```
New variable 'replace-regexp-function'.
Function to call to convert the entered FROM string to an Emacs
regexp in 'query-replace' and similar commands. It can be used to
implement a different regexp syntax for search/replace.
```


```
'E' in 'query-replace' now edits the replacement with exact case.
Previously, this command did the same as 'e'.
```


```
New variables to customize defaults of FROM for 'query-replace*' commands.
The new variable 'query-replace-read-from-default' can be set to a
function that returns the default value of FROM when 'query-replace'
prompts for a string to be replaced. An example of such a function is
'find-tag-default'.
The new variable 'query-replace-read-from-regexp-default' can be set
to a function (such as 'find-tag-default-as-regexp') that returns the
default value of FROM when 'query-replace-regexp' prompts for a regexp
whose matches are to be replaced. If these variables are nil (which
is the default), 'query-replace' and 'query-replace-regexp' take the
default value from the previous FROM-TO pair.
```


### Lisp pretty-printer (‘pp’)

```
New function 'pp-emacs-lisp-code'.
'pp' formats general Lisp sexps. This function does much the same,
but applies formatting rules appropriate for Emacs Lisp code. Note
that this could currently be quite slow, and is thus appropriate only
for relatively small code fragments.
```


```
New user option 'pp-use-max-width'.
If non-nil, 'pp' and all 'pp-*' commands that format the results, will
attempt to limit the line length when formatting long lists and
vectors. This uses 'pp-emacs-lisp-code', and thus could be slow for
large lists.
```


```
New function 'file-has-changed-p'.
This convenience function is useful when writing code that parses
files at run-time, and allows Lisp programs to re-parse files only
when they have changed.
```


`'abbreviate-file-name' now respects magic file name handlers.`


```
New function 'font-has-char-p'.
This can be used to check whether a specific font has a glyph for a
character.
```


```
'window-text-pixel-size' now accepts a new argument IGNORE-LINE-AT-END.
This controls whether or not the last screen line of the text being
measured will be counted for the purpose of calculating the text
dimensions.
```


```
'window-text-pixel-size' understands a new meaning of FROM.
Specifying a cons as the FROM argument allows to start measuring text
from a specified amount of pixels above or below a position.
```


```
'window-body-width' and 'window-body-height' can use remapped faces.
Specifying 'remap' as the PIXELWISE argument now checks if the default
face was remapped, and if so, uses the remapped face to determine the
character width/height.
```


```
'set-window-vscroll' now accepts a new argument PRESERVE-VSCROLL-P.
This means the vscroll will not be reset when set on a window that is
"frozen" due to a mini-window being resized.
```


### XDG Support

```
New function 'xdg-state-home'.
It returns the new 'XDG_STATE_HOME' environment variable. It should
point to a file name that "contains state data that should persist
between (application) restarts, but that is not important or portable
enough to the user that it should be stored in $XDG_DATA_HOME".
(This variable was introduced in the XDG Base Directory Specification
version 0.8 released on May 8, 2021.)
```


Let’s hope this is the beginning of well-behaved elisp code (incl. core Emacs!) that’ll put all their junk files there instead of in my `.emacs.d`

directory.

```
New function 'xdg-current-desktop'.
It returns a list of strings, corresponding to the colon-separated
list of names in the 'XDG_CURRENT_DESKTOP' environment variable, which
identify the current desktop environment.
(This variable was introduced in XDG Desktop Entry Specification
version 1.2.)
```


```
New function 'xdg-session-type'.
It returns the 'XDG_SESSION_TYPE' environment variable. (This is not
part of any official standard; see the man page pam_systemd(8) for
more information.)
```


```
New macro 'with-delayed-message'.
This macro is like 'progn', but will output the specified message if
the body takes longer to execute than the specified timeout.
```


```
New function 'funcall-with-delayed-message'.
This function is like 'funcall', but will output the specified message
if the function takes longer to execute than the specified timeout.
```


### Locale

```
New variable 'current-locale-environment'.
This holds the value of the previous call to 'set-locale-environment'.
```


```
New macro 'with-locale-environment'.
This macro can be used to change the locale temporarily while
executing code.
```


### Table

Table creates editable ASCII tables. I find it incredibly buggy.

```
New user option 'table-latex-environment'.
This allows switching between "table" and "tabular".
```


### Tabulated List Mode

```
A column can now be set to an image descriptor.
The 'tabulated-list-entries' variable now supports using an image
descriptor, which means to insert an image in that column instead of
text. See the documentation string of that variable for details.
```


```
':keys' in 'menu-item' can now be a function.
If so, it is called whenever the menu is computed, and can be used to
calculate the keys dynamically.
```


```
New major mode 'clean-mode'.
This is a new major mode meant for debugging. It kills absolutely all
local variables and removes overlays and text properties.
```


```
'kill-all-local-variables' can now kill all local variables.
If given the new optional KILL-PERMANENT argument, it also kills
permanent local variables.
```


```
Third 'mapconcat' argument SEPARATOR is now optional.
An explicit nil always meant the empty string, now it can be left out.
```


```
New function 'image-at-point-p'.
This function returns t if point is on a valid image, and nil
otherwise.
```


```
New function 'buffer-text-pixel-size'.
This is similar to 'window-text-pixel-size', but can be used when the
buffer isn't displayed.
```


```
New function 'string-pixel-width'.
This returns the width of a string in pixels. This can be useful when
dealing with variable pitch fonts and glyphs that have widths that
aren't integer multiples of the default font.
```


```
New function 'string-glyph-split'.
This function splits a string into a list of strings representing
separate glyphs. This takes into account combining characters and
grapheme clusters, by treating each sequence of characters composed on
display as a single unit.
```


### Xwidget

```
The function 'make-xwidget' now accepts an optional RELATED argument.
This argument is used as another widget for the newly created WebKit
widget to share settings and subprocesses with. It must be another
WebKit widget.
```


```
New function 'xwidget-perform-lispy-event'.
This function allows you to send events to xwidgets. Usually, some
equivalent of the event will be sent, but there is no guarantee of
what the widget will actually receive.
On GTK+, only key and function key events are implemented.
```


```
New function 'xwidget-webkit-load-html'.
This function is used to load HTML text into WebKit xwidgets
directly, in contrast to creating a temporary file to hold the
markup, and passing the URI of the file as an argument to
'xwidget-webkit-goto-uri'.
```


```
New functions for performing searches on WebKit xwidgets.
Some new functions, such as 'xwidget-webkit-search', have been added
for performing searches on WebKit xwidgets.
```


```
New function 'xwidget-webkit-back-forward-list'.
This function returns the history of page-loads in a WebKit xwidget.
```


```
New function 'xwidget-webkit-estimated-load-progress'.
This function returns the estimated progress of page loading in a
WebKit xwidget.
```


```
New function 'xwidget-webkit-stop-loading'.
This function terminates all data transfer during page loads in a
WebKit xwidget.
```


```
'load-changed' xwidget events are now more detailed.
In particular, they can now have different arguments based on the
state of the WebKit widget. 'load-finished' is sent when a load has
completed, 'load-started' when a load first starts, 'load-redirected'
after a redirect, and 'load-committed' when the WebKit widget first
commits to the load.
```


```
New event type 'xwidget-display-event'.
These events are sent whenever an xwidget requests that Emacs displays
another xwidget. The only arguments to this event are the xwidget
that should be displayed, and the xwidget that asked to display it.
```


```
New function 'xwidget-webkit-set-cookie-storage-file'.
This function is used to control where and if an xwidget stores
cookies set by web pages on disk.
```


```
New variable 'help-buffer-under-preparation'.
This variable is bound to t during the preparation of a "*Help*" buffer.
```


```
Timestamps like '(1 . 1000)' now work without warnings being generated.
For example, '(time-add nil '(1 . 1000))' no longer warns that the
'(1 . 1000)' acts like '(1000 . 1000000)'. This warning, which was a
temporary transition aid for Emacs 27, has served its purpose.
```


```
'encode-time' now also accepts a 6-element list with just time and date.
'(encode-time (list SECOND MINUTE HOUR DAY MONTH YEAR))' is now short for
'(encode-time (list SECOND MINUTE HOUR DAY MONTH YEAR nil -1 nil))'.
```


```
'date-to-time' now accepts arguments that lack month, day, or time.
The function now assumes the earliest possible values if its argument
lacks month, day, or time. For example, (date-to-time "2021-12-04")
now assumes a time of "00:00" instead of signaling an error.
```


```
'format-seconds' now allows suppressing zero-value trailing elements.
The new "%x" non-printing control character will suppress zero-value
elements that appear after "%x".
```


```
New events for taking advantage of touchscreen devices.
The events 'touchscreen-begin', 'touchscreen-update', and
'touchscreen-end' have been added to take better advantage of
touch-capable display panels.
```


```
New error symbol 'permission-denied'.
This is a subcategory of 'file-error', and is signaled when some file
operation fails because the OS doesn't allow Emacs to access a file or
a directory.
```


`Warning about "eager macro-expansion failure" is now an error.`


```
Previously, the X "reverseVideo" value at startup was heeded for all frames.
This meant that if you had a "reverseVideo" resource on the initial
display, and then opened up a new frame on a display without any
explicit "reverseVideo" setting, it would get heeded there, too. (This
included terminal frames.) In Emacs 29, the "reverseVideo" X resource
is handled like all the other X resources, and set on a per-frame basis.
```


```
The ':underline' face attribute now accepts a new property.
The property ':position' now specifies the position of the underline
when used as part of a property list specification for the
':underline' attribute.
```


```
'defalias' records a more precise history of definitions.
This is recorded in the 'function-history' symbol property.
```


```
New hook 'save-place-after-find-file-hook'.
This is called at the end of 'save-place-find-file-hook'.
```


```
'indian-tml-base-table' no longer translates digits.
Use 'indian-tml-base-digits-table' if you want digits translation.
```


```
'indian-tml-itrans-v5-hash' no longer translates digits.
Use 'indian-tml-itrans-digits-v5-hash' if you want digits
translation.
```


```
'shell-quote-argument' has a new optional argument POSIX.
This is useful when quoting shell arguments for a remote shell
invocation. Such shells are POSIX conformant by default.
```


```
'make-process' can set connection type independently for input and output.
When calling 'make-process', communication via pty can be enabled
selectively for just input or output by passing a cons cell for
':connection-type', e.g. '(pipe . pty)'. When examining a process
later, you can determine whether a particular stream for a process
uses a pty by passing one of 'stdin', 'stdout', or 'stderr' as the
second argument to 'process-tty-name'.
```


```
'signal-process' now consults the list 'signal-process-functions'.
This is to determine which function has to be called in order to
deliver the signal. This allows Tramp to send the signal to remote
asynchronous processes. The hitherto existing implementation has been
moved to 'internal-default-signal-process'.
```


```
Some system information functions honor remote systems now.
'list-system-processes' returns remote process IDs.
'memory-info' returns memory information of remote systems.
'process-attributes' expects a remote process ID.
This happens only when the current buffer's 'default-directory' is
remote. In order to preserve the old behavior, bind
'default-directory' to a local directory, like
(let ((default-directory temporary-file-directory))
(list-system-processes))
```


```
New functions 'take' and 'ntake'.
'(take N LIST)' returns the first N elements of LIST; 'ntake' does
the same but works by modifying LIST destructively.
```


`'string-split' is now an alias for 'split-string'.`


```
'format-spec' now accepts functions in the replacement.
The function is called only when used in the format string. This is
useful to avoid side-effects such as prompting, when the value is not
actually being used for anything.
```


```
The variable 'max-specpdl-size' has been made obsolete.
Now 'max-lisp-eval-depth' alone is used for limiting Lisp recursion
and stack usage. 'max-specpdl-size' is still present as a plain
variable for compatibility but its limiting powers have been taken away.
```


```
New function 'external-completion-table'.
This function returns a completion table designed to ease
communication between Emacs's completion facilities and external tools
offering completion services, particularly tools whose full working
set is too big to transfer to Emacs every time a completion is
needed. The table uses new 'external' completion style exclusively
and cannot work with regular styles such as 'basic' or 'flex'.
```


```
Magic file name handlers for 'make-directory-internal' are no longer needed.
Instead, Emacs uses the already-existing 'make-directory' handlers.
```


```
'(make-directory DIR t)' returns non-nil if DIR already exists.
This can let a caller know whether it created DIR. Formerly,
'make-directory's return value was unspecified.
```


### Changes in Emacs 29.1 on Non-Free Operating Systems

### MS-Windows

```
Emacs now supports double-buffering on MS-Windows to reduce display flicker.
(This was supported on Free systems since Emacs 26.1.)
To disable double-buffering (e.g., if it causes display problems), set
the frame parameter 'inhibit-double-buffering' to a non-nil value.
You can do that either by adding
'(inhibit-double-buffering . t)
to 'default-frame-alist', or by modifying the frame parameters of the
selected frame by evaluating
(modify-frame-parameters nil '((inhibit-double-buffering . t)))
```


```
Emacs now supports system dark mode.
On Windows 10 (version 1809 and higher) and Windows 11, Emacs will now
follow the system's dark mode: GUI frames use the appropriate light or
dark title bar and scroll bars, based on the user's Windows-wide color
settings.
```


```
Emacs now uses native image APIs to display some image formats.
On Windows 2000 and later, Emacs now defaults to using the native
image APIs for displaying the BMP, GIF, JPEG, PNG, and TIFF images.
This means Emacs on MS-Windows needs no longer use external image
support libraries to display those images. Other image types -- XPM,
SVG, and WEBP -- still need support libraries for Emacs to be able to
display them.
The use of native image APIs is controlled by the variable
'w32-use-native-image-API', whose value now defaults to t on systems
where those APIs are available.
```


```
Emacs now supports display of BMP images using native image APIs.
When 'w32-use-native-image-API' is non-nil, Emacs on MS-Windows now
has built-in support for displaying BMP images.
```


```
GUI Yes/No dialogs now include a "Cancel" button.
The "Cancel" button is in addition to "Yes" and "No", and is intended
to allow users to quit the dialog, as an equivalent of 'C-g' when Emacs
asks a yes/no question via the echo area. This is controlled by the
new variable 'w32-yes-no-dialog-show-cancel', by default t. Set it to
nil to get back the old behavior of showing a modal dialog with only
two buttons: "Yes" and "No".
```


### Cygwin

`'process-attributes' is now implemented.`


### macOS

```
The 'ns-popup-font-panel' command has been removed.
Use the general command 'M-x menu-set-font' instead.
```
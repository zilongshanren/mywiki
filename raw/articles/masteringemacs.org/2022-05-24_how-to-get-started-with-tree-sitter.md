---
title: How to Get Started with Tree-Sitter
url: https://www.masteringemacs.org/article/how-to-get-started-tree-sitter
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I think it’s time to talk about how you can start using one of the more impressive additions to Emacs 29: tree-sitter. Briefly, tree-sitter is a library that transforms source code – or any other structured text, like Markdown – into a *concrete syntax tree*. I’ve written about [tree sitter and the complications of parsing languages](https://www.masteringemacs.org/article/tree-sitter-complications-of-parsing-languages) and why it’s a big deal: correct syntax highlighting; cleverer editing and movement; and better indentation are just some of the benefits of tree-sitter.

And in Emacs 29, support for tree-sitter is built in. Sort of. It’s an optional extra, so you must compile Emacs from source, or hope that someone else will do it for you. In my experience, unless you’re using a bleeding-edge Linux distribution, you’re in for quite a wait. So I’ve compiled a guide on how to get started with tree-sitter in Emacs: not just the compilation, but how to get started using it. You see, getting everything to work properly is a bit more involved than just compiling Emacs with tree-sitter support.

![](../../assets/307b8fb6558102f3.gif)

[Combobulate](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), adds advanced editing and movement using tree-sitter. This is Combobulate's expand region feature, bound to

`M-h`

.Despite the high activation cost of getting tree-sitter up and running, I firmly believe it’s worth it. Here’s what you’ll need to do to get it set up.

## Building Emacs with Tree-Sitter Support

*Note that these compilation instructions cover Linux, and use Ubuntu/Debian as the example distribution. Tree-sitter will also work on other platforms, like Microsoft Windows. For compiling or installing the grammars on more platforms than just Linux, see below.*

Grab the latest Emacs sources from Savannah, Emacs’s official git repo. You can use the official tarballs instead, but for now I recommend you check out the

`emacs-29`

branch, or just`master`

if you’re OK with living life on the bleeding edge. I always use`master`

:`$ git clone https://git.savannah.gnu.org/git/emacs.git -b emacs-29`

Next, you’ll need to install the prerequisites required for Emacs to compile. With Debian/Ubuntu-based systems, that is easy, as you can rely on

`apt-get build-deps`

to do the heavy lifting by having it install the dependencies for one of the Emacs versions it your distro*does*support.Building Emacs is not hard, and the simplest way to do this is to follow my existing guide where I detail how to do all of this, step-by-step, to get native compilation working:

If you’ve never bothered with native compilation, you should: it provides a significant speed boost. You may as well build Emacs with it also.

I would urge you to get this step working first: we’ll amend it slightly to add tree-sitter support (and other optional goodies) next. The approach outlined in that article is the barebones version of Emacs, but once you get it building on your system, you can easily recompile Emacs from scratch with additional features, as needed.

Next, you’ll need to check out tree-sitter’s source code:

`$ git clone git@github.com:tree-sitter/tree-sitter.git`

I, once again, stick to the

`master`

branch, but you can use a tagged release if you prefer a stable release.Your distro may already include tree-sitter as a package, as in the case of Debian:

`$ sudo apt-get install libtree-sitter-dev`

That is occasionally enough to install tree-sitter so it works with Emacs.

*However*, given how easy tree-sitter is to install, having no real depencies of its own, and it being a rather fast-moving project, I recommend you just build it from source also.Time to build tree-sitter. Provided your Emacs builds, so should tree-sitter:

`$ cd tree-sitter/ $ make $ make install`

That is all it takes. Note that

`make install`

normally requires root. It’ll install a shared library to (usually)`/usr/local/lib`

.In

*theory*, that’s all it takes for Emacs to compile with tree-sitter support.*However*, if Emacs complains during the build that it can’t find the shared library`libtree-sitter.so`

, try this:`$ export LD_LIBRARY_PATH=/usr/local/lib/`

And retry building Emacs.

Now you can start building Emacs with tree-sitter. I’ll assume you followed my other tutorial and you’re now at a point where Emacs builds (without) tree-sitter. Now all you need to do is add

`--with-tree-sitter`

(technically, it should detect tree-sitter automatically, but I prefer being explicit) to the call to`./configure`

:`./configure --with-tree-sitter --with-native-compilation ... CC=gcc-10`

Now run

`make`

then`make install`

. Everything should build and link and you’ll wind up with your own build of Emacs.

That takes care of Emacs. Unfortunately, that is not enough to reap the benefits of tree-sitter. We’ll have to install some language grammars also.

## Installing the Language Grammars

Neither tree-sitter nor Emacs come installed with language grammars. Just like kids’ toys and batteries, they’re sold separately. So you’re required to download and compile the sources for each language grammar you want to use.

You must compile each language into a shared library and put in a place where tree-sitter can find them. It is not especially hard to do so, but it can be a frustrating experience as it’ll depend on: your platform; your choice of compilers; whether the grammar author chose C++ or just C, and so on. Furthermore, there is often no `Makefile`

, so you have to tell the compiler yourself to build a shared library.

Luckily, there are two simpler ways than the manual way: the builtin method in Emacs, or relying on the kindness of strangers.

Before I explain both methods, I must point out that, at the end of the day, regardless of the method you choose – and especially if you’re compiling the grammars yourself – that you must put them in a directory where Emacs and tree-sitter can find them:

- Emacs will look in
`treesit-extra-load-path`

if you have it set; - Then, in a subdirectory called
`tree-sitter`

under`user-emacs-directory`

— e.g.,`~/.emacs.d/tree-sitter/`

. - And finally it’ll look in all the usual
`/lib`

locations scattered around your filesystem.

I prefer the Emacs directory approach myself. The grammars are small and, unless you make it a habit to swap between wildly different system architectures, you can safely commit the shared libraries to git and lug ’em around with you.

Anyway. Let’s install the grammar libraries. Onwards!

### Compiling and Installing with the builtin method in Emacs

This is perhaps the simplest, but it’ll only work if you don’t have an exceptional setup (so it won’t work well unless you have GCC and run some flavor of Linux.) But if your Linux installation’s plain as day, expect this method to work fine if you successfully compiled Emacs and tree-sitter from scratch.

The command `M-x treesit-install-language-grammar`

installs a language grammar by first cloning the git repo hosting it and then compiling it and storing the shared library in your `.emacs.d`

directory.

In order to determine where – and what – it can install, you must first tell Emacs where to find the language grammars. The variable `treesit-language-source-alist`

is a simple alist that expects a form in the format of `(LANG . (URL REVISION SOURCE-DIR CC C++))`

. Where only `LANG`

and `URL`

are mandatory. Leave out the rest and Emacs will try to do the right thing. It is not customizable using the *Customize* interface, unfortunately, so you must set and edit it manually.

Here’s an example. Do note that it’s not a complete list of grammars available:

(setq treesit-language-source-alist
'((bash "https://github.com/tree-sitter/tree-sitter-bash")
(cmake "https://github.com/uyha/tree-sitter-cmake")
(css "https://github.com/tree-sitter/tree-sitter-css")
(elisp "https://github.com/Wilfred/tree-sitter-elisp")
(go "https://github.com/tree-sitter/tree-sitter-go")
(html "https://github.com/tree-sitter/tree-sitter-html")
(javascript "https://github.com/tree-sitter/tree-sitter-javascript" "master" "src")
(json "https://github.com/tree-sitter/tree-sitter-json")
(make "https://github.com/alemuller/tree-sitter-make")
(markdown "https://github.com/ikatyang/tree-sitter-markdown")
(python "https://github.com/tree-sitter/tree-sitter-python")
(toml "https://github.com/tree-sitter/tree-sitter-toml")
(tsx "https://github.com/tree-sitter/tree-sitter-typescript" "master" "tsx/src")
(typescript "https://github.com/tree-sitter/tree-sitter-typescript" "master" "typescript/src")
(yaml "https://github.com/ikatyang/tree-sitter-yaml")))
*Note*: Since I wrote this, they have discovered the untold benefits of versioned releases. They used to be unversioned and some still are.
You can -- should! -- use tagged releases where possible. Most of Emacs 29.x is written for grammars released no later than mid 2023. If you use grammars *newer* than that, you'll probably run into font locking and indentation problems.
I `maintain a list <https://github.com/mickeynp/combobulate>`__ of grammar versions valid with Combobulate and Emacs 29, but it is not a complete list. It may serve as a starting point if you are unsure, though.


As you can see, there’s not much to it. A couple of the languages require a little path and branch fiddling as their directory structure differ from the accepted standard.

Once you’ve found the languages you like, you’ll need to install them. Call the command `M-x treesit-install-language-grammar`

for each language and that’s usually all there is to it.

If that’s too much manual work, just bulk install all of ’em in one go. [Evaluate this elisp form](https://www.masteringemacs.org/article/evaluating-elisp-emacs) to do so:

It can happen that `LANGUAGE`

is named differently than the shared library. In the unlikely event that happens you can use `treesit-load-name-override-list`

. You’re more likely to encounter this if you’re using competing grammars for the same language, or if the name does not match the shared library name.

Every language has a function entry point named `tree_sitter_<LANGUAGE>`

in the library, and if the `<LANGUAGE>`

does not match up with the filename (usually `libtree-sitter-<LANGUAGE>.so`

), Emacs won’t load the module. This is not the case with the example I gave above, but you may run into it if you’re using niche language grammars or if you want multiple ones serving the same language (for some reason.)

Here is what that could look like:

### Using pre-compiled language grammars

Before Emacs 29 added tree-sitter support, Tuấn-Anh Nguyễn created [a third-party tree-sitter package](https://github.com/ubolonton) that adds tree-sitter based font locking and support for tree-sitter in all modern versions of Emacs. It’s excellent, though it has a number of limitations (mostly due to Emacs’s dynamic module system more than anything else.) But if you want tree-sitter support in older Emacsen, you should check it out. It’s a MELPA package install away and it pretty much works out of the box.

Nevertheless, Tuấn-Anh also took the time to build a CI release system that tracks a large portion of the most common language grammars — complete with builds for Windows, Mac and various Linux architectures. Really superb work.

So if you’re on Windows or if you find the idea of building the grammars cumbersome, you should give his precompiled packages a shot.

You can find them [on his Github releases](https://github.com/emacs-tree-sitter/tree-sitter-langs/releases) page. You can also download the `tree-sitter-langs`

package from MELPA, but I recommend you just download the shared libs directly instead, as you’ll in any event have to rename them and place the grammar libraries somewhere else.

The names of the files are `<LANGUAGE>.so`

(or with your platform’s equivalent extension) which is not in keeping with the expected naming style in Emacs. You must first rename them so they’re named `libtree-sitter-<LANGUAGE>.so`

. This is as good a time as any to learn how to bulk rename them with Emacs’s `M-x dired`

and the [editable dired buffers](https://www.masteringemacs.org/article/wdired-editable-dired-buffers) feature.

Once they’re named appropriately, put them in the directory called `tree-sitter`

in `user-emacs-directory`

. Or pick another place for them, as per the search path order I wrote about earlier. But for most of us, putting them in `~/.emacs.d/tree-sitter`

is good enough.

### Check if a grammar is working

Determining if a grammar is available is not intuitive nor obvious unless you use elisp. You must call the `treesit-language-available-p`

function to check:

Emacs will return `t`

if it’s a known language and `nil`

otherwise. Use this to check if you’ve compiled, installed or copied (all depending on the method you chose) the grammars correctly.

Before you proceed: consider if you have the right grammar version installed. The grammar authors have a habit of making breaking changes to the grammar structure. That’s all well and good, but it’ll break your Emacs major modes’ font lock system if it encounters an unrecognized query pattern. If you run into that problem, try downgrading your grammar package version and use a tagged release.

### How to use Tree-Sitter

Yep. This part needs a tutorial introduction also. Emacs now implements a very different way of font locking (syntax highlighting) than most – though not all! – major modes in Emacs, as most of them use regular expressions to feed Emacs’s font lock engine with syntactic information. Now that it’s using an actual syntax tree to extract information, Emacs is a lot more accurate.

Because of the complete 180-degree turn in, well, almost everything, the Emacs developers decided against wedging tree-sitter support into the existing modes. Instead it’s relegated to its *own*, “TS”-powered, major modes. I understand *why* – some of the major modes are complex and naively cramming tree-sitter-powered features into them will require more longer-term engineering effort to sort out than they can currently muster – but it’s still, well, they’re different modes, with all the drawbacks and benefits that bring.

Modes that use tree-sitter are all named `<major-mode>-ts-mode`

. That’s the naming standard and it does mean you can quickly check if Emacs supports your pet major mode out of the box: typing `C-h a -ts-mode$`

should do the trick. The apropos window will list all known tree-sitter major modes.

Note that, just because you have installed a grammar, does *not* mean Emacs supports it. Someone still has to write the – admittedly, *way* easier – syntax and indentation logic and all that good stuff.

One interesting outcome of tree-sitter support is that Emacs has now gained new major modes it did not have before. Like `dockerfile-ts-mode`

.

So to use tree-sitter you must activate the new major mode manually. Emacs will, by default, use the existing major modes, even if you have everything set up correctly.

To coax Emacs into using the new major modes by default, you’ll have to either:

- Edit
`auto-mode-alist`

,`interpreter-mode-alist`

, etc. and change over all the references you care about to use new`<LANGUAGE>-ts-mode`

major modes; or… - Use
`major-mode-remap-alist`

, an icky hack that maps one major mode symbol to another behind-the-scenes. That feature, rather conveniently, debuted in Emacs 29 also.

Hacky though I think it is, I’d pick the `major-mode-remap-alist`

for now: it’s easy to get started with, and you can always migrate everything to the harder, and more explicit, way once you’re happy with your new tree-sitter-enabled major modes.

Here’s an example, and this time you can instead use `M-x customize-option`

to customize it to your liking, if you prefer the customize interface.

As you can see there’s not much to it. Whenever Emacs is asked to activate `css-mode`

, it’ll instead call `css-ts-mode`

.

Despite the major mode switcheroo gimmick, it does not remove most of the obstacles and annoyances of having a new major mode.

At this point, I’d try out some of the major modes you want to use. Annoyingly, there’s no easy way to see if you’re using the normal or the TS-powered major mode: you can look at the lighter in the mode line, but it’s often the same text as the normal mode. The quickest way to tell is to type `M-: major-mode`

and you’ll see which major mode you’re using.

I’ve heard tales of the TS-powered major modes being “temporary”, but… there’s nothing so permanent like a temporary solution. I understand why the distinction has to exist (for now), but it’s still awkward, and this approach does leave a number of unsolved problems you’ll still have to solve yourself:

- You must duplicate and/or change your mode hooks.
`python-mode-hook`

is distinct from`python-ts-mode-hook`

, and you should ensure you copy over your settings. - Your indentation customizations (if you have them) may not work. Indeed, any customizations you’ve applied to one mode won’t
*necessarily*apply. They*might*, but there’s no guarantee they will. It comes down to the mode and the feature. - Font lock faces are now more detailed and expressive than ever before. This is one area you probably definitely
*will*and*want*to customize, if only to take advantage of better syntax highlighting. - Third-party packages will blithely assume you’re using the default major mode and not your turbo-charged tree-sitter equivalent, and so they may not activate or work at all in the TS-powered one. It’ll take a while for this distinction to percolate, and for packages to check for one or the other.
- Most TS-powered modes ‘derive’ from the original major mode, with varying levels of overlapping customizations and features. The best way to see what your new major mode can (or cannot) do is, uh, well.. to read the source. Sorry.

Nevertheless, it’s worth the pain, as you’ll only have to do it once.

Keep in mind that file-local variables – they appear in the top of your file as `-*- ... -*-`

or in the bottom as `Local Variables:`

– **ignore your major mode remaps**. So, if you have `mode: python;`

in a file-local variable, you’re getting the regular `python-mode`

and *not* `python-ts-mode`

.

### Tweaking the Font Locking

One of the benefits of having a concrete syntax tree is precision. Emacs is now capable of precisely highlighting things it couldn’t before: it can distinguish function calls from keywords or identifiers. To better support that, there’s now a host of new font lock faces.

Due to the large array of things you can color, Emacs now separates its font locking into *font lock features*. This feature’s akin to the long-existing `font-lock-maximum-decoration`

that the chromatically averse can tweak to disable some or all of Emacs’s coloring if it’s too ostentatious. If you belong to that cohort – most of whom refer to this as “[angry fruit salad](https://en.wiktionary.org/wiki/angry_fruit_salad)” – then you’re in for a technicolor razzle-dazzle.

Every TS-enabled major mode will decide on its own list of *features*. The features are buffer-local and set in `treesit-font-lock-feature-list`

, with each sub-list representing a *level* of highlighting. If you want to change it, you’ll need a mode hook to alter it properly.

For most, it’s enough to change the font lock feature level. To do so, customize `treesit-font-lock-level`

. Every incrementation of the level will color more and more things: one you reach the higher echelons, it does become a bit much, even for me. But it’s great to have that flexibility and the power to decide which things should, and which things should not, be highlighted.

**NOTE**: `treesit-font-lock-level`

has a special *setter* attached to it, so as to automatically recompute the font lock features in all your buffers when you change the level. If you use Customize, then you don’t have to do anything, but if you normally use `setq`

, you’ll have to use `customize-set-variable`

instead to ensure the setter is called properly.

It’s worth experimenting with the font lock level: the default is conservative and in line with what Emacs normally font locks. This is one of the capstone features of tree-sitter, and you should absolutely tweak it to your liking. To go along with each feature is an equivalent `font-lock-<feature>-face`

. You can list all the pertinent faces with `M-x customize-apropos-faces RET ^font-lock-`

. It’s very likely your theme (or your own face customizations if you maintain your own faces, like I do) is missing these customizations, so be sure to check, as their defaults make everything look rather samey.

The general intent behind the level is that you set it once and you get – approximately – the same general style of font locking in all TS-powered modes. I think that intent holds up rather well, even though what gets font locked, and how, is up to each major mode author.

### Inspecting the Tree-sitter tree

One benefit of tree-sitter is access to the live concrete syntax tree of your source code. You can inspect the tree in a buffer with `M-x treesit-explore-mode`

and `M-x treesit-inspect-mode`

. There’s a lot more you can do with it, so I recommend you consult the manual, or stay tuned for more in-depth articles on this topic here!

## “Fixing” the S-Expression Commands

**NOTE:** This problem is fixed in Emacs 30.1.

Emacs has had s-expression-based commands for decades. They’re bound to keys like `C-M-f`

, `C-M-SPC`

, and `C-M-k`

.

They work well in a wide range of languages because they’re delightfully dumb: they look for structured expressions – such as `(`

and `)`

, `"`

and `"`

, and so forth – and treat them as cohesive, syntactic ‘unit’. In the absence of such structured units, they fall back and behave much like word-based movement and editing.

Not so in tree-sitter major modes. They’ve been “upgraded” to try and guess the syntactic units you probably want to move over or edit.

That sounds like a great idea until you realize that it is not possible to make one-size-fits all commands that do this. Believe me: *I’ve tried*. Every language is different, and even a modest language grammar will have hundreds of node types and millions of combinations. Whereas before you could predict where point would end up after calling these commands, now you probably can’t. Worse, the commands do not mirror the old behavior at all: they’re erratic and unpredictable.

If you already use these commands, and you also dislike this unwanted and unasked for change in behavior, then you can use this snippet to revert to the old way:

(defun mp-remove-treesit-sexp-changes ()
(when (eq forward-sexp-function #'treesit-forward-sexp)
(setq forward-sexp-function nil))
(when (eq transpose-sexps-function #'treesit-transpose-sexps)
(setq transpose-sexps-function #'transpose-sexps-default-function))
(when (eq forward-sentence-function #'treesit-forward-sentence)
(setq forward-sentence-function #'forward-sentence-default-function)))
(add-hook 'prog-mode-hook #'mp-remove-treesit-sexp-changes)


## Structured Editing and Movement

![](../../assets/4385aecf90b39885.gif)

One of the tantalizing things that a library like tree-sitter offers is better and more correct editing and movement that understands the syntax of your code. That’s one of the things my package [Combobulate](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter) sets out to do: to provide advanced editing and movement across a swathe of languages.

Now that you’ve gotten tree-sitter working, why not take my [Combobulate package](https://github.com/mickeynp/combobulate) for a spin? It’s a work-in-progress still, so expect bugs, but it’s got a host of useful features that’ll speed up your day-to-day coding.
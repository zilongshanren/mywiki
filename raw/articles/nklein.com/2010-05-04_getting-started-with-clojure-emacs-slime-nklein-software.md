---
title: 'Getting started with Clojure/Emacs/Slime :: nklein software'
url: http://nklein.com/2010/05/getting-started-with-clojureemacsslime/
author: Pat
published: '2010-05-04'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I spent some considerable time yesterday poring over the shelves in the programmer’s section of a local bookstore yesterday. Based on the available jobs at the moment, I was trying to decide whether it would be less painful to learn C#/.NET/AFW/blurpz or Hibernate/Springs/Struts/glorpka. My lambda, those things are fugly. When I open a book to find that my simple database example

takes eight XML configuration files and twenty-five lines of calls to the same function (with a 25-character identifier (which, technically, should be namespace qualified, too)), I just don’t want to go there.

So, I walked away with [Programming Clojure](http://search.barnesandnoble.com/Programming-Clojure/Stuart-Halloway/e/9781934356333/?itm=1&USRI=%22Programming+Clojure%22) and a determination to think really hard

about how to get paid to do something that’s not intensely painful.

Well, yesterday afternoon and late-night were intensely painful trying to get Clojure/Emacs/Slime all working together. Today, magickly, I messed something up in my *.emacs* file that convinced swank-clojure to download its own copies of the three JAR files it needs and zoom… I’m out of the gate.

Someday, I’d still like to be able to use my own JAR files for all of this, but in the meantime, I’m up and running.

## Here’s what works

This is the relevant configuration from my *.emacs* file. It draws partly from [these instructions by I’m not sure who](http://riddell.us/ClojureWithEmacsSlimeSwankOnUbuntu.html), partly from [this message by Constantine Vetoshev](http://www.mail-archive.com/clojure@googlegroups.com/msg26852.html), partly from how my *.emacs* file was previously arranged, partly from sources now lost in the browser history sea, and partly from sheer luck.

First, some generic stuff up at the beginning:

(let ((default-directory (concat dir "/")))

(normal-top-level-add-subdirs-to-load-path)))

(add-to-list 'load-path "~/.emacs.d/site-lisp")

(add-subdirs-to-load-path "~/.emacs.d/site-lisp")

Then, prepping slime a bit:

(add-to-list 'load-path "~/.emacs.d/site-lisp/slime/contrib")

(add-hook 'lisp-mode-hook (lambda () (slime-mode t)))

(add-hook 'inferior-lisp-mode-hook (lambda () (inferior-slime-mode t)))

(setq common-lisp-hyperspec-root

"file:///Developer/Documentation/Lisp/clhs/HyperSpec/")

(slime-setup '(slime-repl))

(setq slime-net-coding-system 'utf-8-unix)

Then, setting up some general stuff for easy lisp implementations. (The *–sbcl-nolineedit* is something I personally use in my *.sbclrc* to decide whether to load *linedit*.)

'((sbcl ("sbcl" "--sbcl-nolineedit"))

(ccl ("ccl"))

(ccl64 ("ccl64"))))

Some commands to simplify things so I don’t have to remember to M–– M-x slime

:

`(defun ,name ()

(interactive)

(let ((slime-default-lisp ,mapping))

(slime))))

(defslime-start ccl 'ccl)

(defslime-start ccl64 'ccl64)

(defslime-start clojure 'clojure)

(defslime-start sbcl 'sbcl)

Then, Clojure-specific SLIME stuff

(add-to-list 'auto-mode-alist '("\\.clj$" . clojure-mode))

(require 'swank-clojure)

(setq slime-lisp-implementations

(append slime-lisp-implementations

`((clojure ,(swank-clojure-cmd) :init swank-clojure-init))))

And, a touch more slime stuff to make things a little happier.

(lambda ()

(setq slime-truncate-lines nil)

(slime-redirect-inferior-output)))

In my *.emacs.d/site-lisp*, I did the following:

% git clone git://git.boinkor.net/slime.git

% git clone http://github.com/technomancy/swank-clojure.git

% git clone http://github.com/jochu/clojure-mode.git

## What didn’t work

Before accidentally triggering swank-clojure to download its own JARs, I tried installing what I could with ELPA. I tried installing clojure, clojure-contrib, and swank-clojure with Lein. I tried installing them with Maven. I tried various combinations of versions of clojure and swank-clojure.

I have no idea how the JARs that swank-clojure built itself got built. I cannot reproduce it.

**Edit:** Ah, it appears that the Subversion repository for Clojure that I found is deprecated. But, I don’t have the energy to try the git repository myself at this point. Maybe next week.

Two words: Clojure Box. Took me 2 minutes. Works out of the box.

Clojure-Box is for Windows. I’m on a Mac. Further, I already have Emacs, Slime, paredit, and clojure-mode installed and running. I already had Clojure running. I just wanted to make it go with swank-clojure.

There are a variety of “out-of-the-box” and “pre-packaged” solutions for lots of things that I want to do. I generally don’t want six copies of everything on my machine though (especially when “everything” includes Emacs and a Lisp implementation), so I prefer to steer clear of those things when I can… or stick to only one “pre-package” system. 1/2 the point of package management is lost if I need five separate copies of libX11.dylib and eight copies of freetype.h on my machine.

Sorry to hear the bad experience. I had a similar experience until I discovered Incanter [1], the numerical/scientific computing package that is built on Clojure. It has the only sane Clojure getting-started installation procedure I could find [2] for someone using emacs/slime.

[1] http://incanter.org/

[2] http://wiki.github.com/liebke/incanter/#getstarted

Best wishes.

Thank you for this. Until now, I’ve been forced to use inferior lisp mode for either clojure or common lisp after they started adding all of the newbie friendly automagic install stuff to clojure mode.

Thanks! I had the same problem a few months ago and I gave up by commenting the clojure elisp code out when I worked with SBCL and the SBCL elisp code when I worked with Clojure. Now I don’t need to do that 😀

I posted about setting up Emacs for Clojure development here:

http://charsequence.blogspot.com/2010/07/setup-emacs-for-development-with.html

Patrick — do these directions still work? I was just trying to follow this, and in the middle of the readme for for swank-clojure I read:

where “the method outlined above” was some stuff about Leiningen and Maven that was just Greek to me, since I am just trying to get started with Clojure, and want a pretty much vanilla Clojure REPL to work with.

This seems like “just figure out all about ASDF and then you can start your lisp environment…”

I fought with Leiningen and Maven for way too long back in May. I haven’t downloaded any Clojure or emacs-specific Clojure stuff since then. My REPL for Clojure still works with precompiled JARs that it fetched itself.

I hope the above still works, or I just won’t ever upgrade.

OK, looks like the right solution is to get leiningen from github, then use leiningen to install swank-clojure and start swank-clojure from the terminal. Then use slime-connect to hook up. No longer are we to get our own copy of swank-clojure in el and install it ourselves.

[…] Useful link: http://nklein.com/2010/05/getting-started-with-clojureemacsslime/ […]
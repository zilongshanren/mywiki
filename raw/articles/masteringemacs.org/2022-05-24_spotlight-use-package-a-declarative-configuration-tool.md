---
title: 'Spotlight: use-package, a declarative configuration tool'
url: https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Have you ever heard of [use-package](https://github.com/jwiegley/use-package/)? It’s a declarative way of expressing package configuration in Emacs but without the tears. It’s written by the inimitable [John Wiegley](http://www.newartisans.com/), a former GNU Emacs lead maintainer and author of many cool tools like [a command line ledger](http://ledger-cli.org/), Emacs’s [Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell), and much more.

It’s fair to say most of us have declared *.emacs bankruptcy* at least once. It comes about when the passage of time and your ossified hacks-upon-hacks conspire against you, and you’re wondering why you have thousands of lines dedicated to something you haven’t touched in a decade.

Even in a post-hack world of package managers, starter kits, and sane defaults, it still sneaks up on you as you pile on more and more packages and customizations. `use-package`

goes some way towards solving that by introducing a simple, declarative macro that – through some eldritch elisp magic – ensures your package is loaded only when it’s needed, and that its settings are loaded alongside it, in a deterministic and understandable manner.

`use-package`

is easy to use, and it ships with a nice `README.md`

file explaining how it works. The only thing holding back its adoption is that, before Emacs 29.1, it did not ship with Emacs. Now that it’s included, you can build your Emacs configuration “from scratch” without first having to bootstrap the installation of use-package.

Here’s an example of how you can use it. Please note that use-package is rather feature rich, and I really only touch on the basics, here. I do feel you get by with little more than the directives I show you below, though; most of the other ones allow for more advanced features, which you may not need at all.

If you regularly use Emacs’s [dictionary lookup feature](https://www.masteringemacs.org/article/wordsmithing-in-emacs) you may want to customize it to your liking:

```
(use-package dictionary
:bind (("M-#" . dictionary-lookup-definition))
:config
(setq dictionary-use-single-buffer t)
(setq dictionary-server "localhost"))
```


Here I declare that `dictionary`

– for that is the name of the feature in Emacs – must bind a global key, `M-#`

, to `dictionary-lookup-definition`

in addition to configuring a couple of variables. What’s a feature you ask? Anything that `(featurep 'something)`

returns non-nil to. Keep an eye out for `(require 'something)`

.

One other thing about features: where do you put things that do not belong to any *one* feature? Well, there’s a “meta” feature called `emacs`

just for that purpose. Use that for all the other stray bits of code you want to stash together.

You can combine your customizations with `:config`

, `:init`

and `:preface`

. Each type works in a slightly different way.

The `:config`

keyword executes the code *after* a package is loaded; the `:init`

keyword executes the code *before* the package is loaded; and the `:preface`

keyword is there so the Emacs byte compiler *and* the lisp evaluator know about things like function and symbol declarations.

My personal view is to put most things into `:config`

(as you probably want to initialize your own settings *after* the package has loaded its own defaults) and only toy with `:init`

and `:preface`

if you have a good reason to, or you regularly define your own commands, variables or functions for use with that package.

Here’s an example where I change the default `M-x re-builder`

– [re-builder is Emacs’s regexp builder](https://www.masteringemacs.org/article/re-builder-interactive-regexp-builder) – syntax to `string`

:

```
(use-package re-builder
:bind (("C-c R" . re-builder))
:config (setq reb-re-syntax 'string))
```


You can even migrate all your hand-crafted `auto-mode-alist`

alterations to `use-package`

. Here I declare that `.txt`

, `.rst`

and `.rest`

files must use `rst-mode`

:

```
(use-package rst
:mode (("\\.txt\\'" . rst-mode)
("\\.rst\\'" . rst-mode)
("\\.rest\\'" . rst-mode)))
```


You can use it with built-in “packages” in Emacs also. Here I re-bind certain keys and set up a hook [against Emacs’s builtin terminal emulator](https://www.masteringemacs.org/article/running-shells-in-emacs-overview):

```
(use-package term
:preface
(defun mp-term-custom-settings ()
(local-set-key (kbd "M-p") 'term-send-up)
(local-set-key (kbd "M-n") 'term-send-down))
:config
(add-hook 'term-load-hook 'mp-term-custom-settings)
(define-key term-raw-map (kbd "M-o") 'other-window)
(define-key term-raw-map (kbd "M-p") 'term-send-up)
(define-key term-raw-map (kbd "M-n") 'term-send-down))
```


As you can see, it keeps everything nice and tidy. The older way of evaluating things after load, or even just `require`

’ing all the packages you use and then applying your changes is completely unnecessary with `use-package`

. `use-package`

is clever enough to only autoload commands you’ve bound (or explicitly declared with `:commands`

), meaning Emacs won’t load the package into memory until you actually need it. In practical terms, it should greatly speed up your Emacs start time.

Once you’ve rewired your Emacs configuration to `use-package`

you’re going to want to jump to the requisite package definitions. To do this, enable `use-package-enable-imenu-support`

. Now you can use Emacs’s Imenu (`M-g i`

in Emacs 29, or just `M-x imenu`

) to jump to the definition. Nifty!

Although it does require learning a new “mini-language”, I think `use-package`

is worth considering if you’re even moderately organized.
---
title: 'Polymode: Multiple Major Modes and How to Use SQL and Python in one Buffer'
url: https://www.masteringemacs.org/article/polymode-multiple-major-modes-how-to-use-sql-python-in-one-buffer
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

How do you mix and match programming languages in the same buffer? That is a question that Emacs users have struggled with in ever-greater numbers as programming languages meld together in spaghetti-like ways: Templating Languages and Code; Documentation and Code; Code and more Code. Most of us have to deal with a soup of Jinja and YAML; Javascript and HTML; and so on – and that presents a number of unique challenges to text editors.

The answer – one of several, as is Emacs’s wont – is [Polymode](https://github.com/polymode/polymode). Polymode seamlessly blends two or more major modes together in the same buffer. Now to understand why that is interesting, a quick history lesson…

## Why Just The One Major Mode?

Back in the day, the idea of buffers having ephemeral “modes” that you can activate and deactivate at will was a bit of a revelation, and one that drove the design of many other editors — even if they never really adopted the same flexibility as Emacs.

You have *one* major mode, and it would drive the bulk of your interactions with that buffer: it would font lock (syntax highlight), bind keys to helper commands, manage the indentation, and other mode-specific tasks. All of it supported by generous helpings of gnarly regexp, for font locking, and dastardly arcane elisp for the indentation (anyone who doubts me is encouraged to peruse the C mode’s indentation engine, weighing in at half a meg of elisp.)

The problem, then, begins when you want bijou additions to your major mode: maybe a fancy spell checker that checks only strings (`M-x flyspell-prog-mode`

); or perhaps a feature that expands text as you write (`M-x abbrev-mode`

, Skeletons, YASnippet, *ad infinitum*.) The solution is a minor mode: it can add keys, some light syntax highlighting, but otherwise stays in the background.

So that’s where minor modes entered the frame. They can, in theory, do *anything*, but are generally respectful enough not to tamper with the global state of the major mode that it is cohabitating with.

But nobody ever really gave much pause to the idea that you’d want to combine multiple major modes and support it as a first-class citizen; and for the odd language that did need to mix and match, the language major mode was programmed with that in mind.

But today, that contract no longer works. Advanced packages like Web Mode_ simply builds in support for all conceivable templating language and programming languages mixes that you’d want to combine in the web development world. Web-mode’s a particularly *good* example of an all-inclusive package, but if you want to mix and match uncommon combinations, you are on your own.

Luckily, there are several packages that attempt to do this. MuMaMo and Multi-Mode were two of the earliest packages that attempted to rectify this, but they all suffered from the problem of having to Large Hadron Collider things together that weren’t meant to be: font locking and especially indentation are easily at odds with eachother, as there is no formal framework in place that would let you selectively stop and start one part or the other: not to mention how stateful each major mode is, ramming all manner of hooks and other complex code into a buffer to make it work. So most people generally avoided these packages unless they were web developers, where you really needed that feature.

And for many years – Web-Mode excluded – there were few attempts to bridge this chasm.

But that all changed with a little-known feature called *indirect buffers*.

## Indirect Buffers

Indirect buffers are, to simplify a fairly complex feature, a way of partitioning a buffer into “sub-buffers”, known as *indirect buffers*. Each indirect buffer has a life of its own, with buffer-local variables, modes, keymaps, and so on – in effect circumventing the hairy problem of how do you mix immiscible major modes.

Polymode makes heavy use of this feature – along with a lot of clever logic – to discombobulate a base buffer into constituent indirect buffers, based on logic such as regular expressions, and then recombobulate them back together again, each with its own major mode.

## Enter Polymode

I found out about Polymode recently, and it’s a swell package. It’s not 100% bugfree yet, as it’s new in town, but I have high hopes that it’ll serve as a platform for mode authors to adopt and use, as it’s quite striking how easy you can combine multiple modes.

With about 10 lines of code I managed to jury-rig `Jinja2-mode`

and `yaml-mode`

, giving me the features of both: YAML indentation for the YAML parts, and syntax highlighting for the templated Jinja2 part. I subsequently discovered that someone had already done this for Ansible, called [poly-ansible](https://gitlab.com/mavit/poly-ansible) that can easily be modified to work with Salt.

## Polymode: Mixing SQL and Python

![Polymode Python Screenshot](../../assets/b75bb0a22a0a2686.png)


Instead of demonstrating YAML and Jinja2, I figured I’d merge Python with SQL, with `M-x sql-mode`

highlighting (and comint support!) in multiline strings. (And yes, SQL in strings is a serious antipattern, but we’ll pretend that we’re doing this for *science*.)

As the screenshot shows, the multiline strings are highlighted and, when your point enters the chunk – the term used for the part where the modes change – it switches to that major mode for all intents. That means polymode not only gives you the added tinsel of font locking both languages, it also lets you navigate, edit, and access the same commands you have in a dedicated sql-mode buffer, but inside a Python buffer.

How cool is that? In fact, with a few minor tweaks, I made it so you can *send* the contents of a string directly to a dedicated sql-mode comint process, such as that of `M-x sql-postgres`

(or whatever your database flavor is.)

Honestly, the things you can do so little code is very impressive.

Let’s walk through some of the basics to get started.

**NOTE**: I, rather oddly, use an ancient version of `python.el`

by Dave Love that shipped with Emacs 5+ years ago. I expect it’ll still work OK with other Python modes though!

```
(use-package polymode
:ensure t
:mode ("\.py$" . poly-python-sql-mode)
:config
(setq polymode-prefix-key (kbd "C-c n"))
(define-hostmode poly-python-hostmode :mode 'python-mode)
```


I start out by configuring a *hostmode*, which is the name given to the “main” entrypoint for a mode. For python files, I’d want `python-mode`

. I name it `poly-python-hostmode`

; remember that, as I’ll use it later.

Next, I rebind `polymode-prefix-key`

away from the default `M-n`

, which is a key binding I treasure for other things.

I also use the `:mode`

slot to replace the default major mode for python files with the new `poly-python-sql-mode`

, which I’ll describe in a moment.

```
(define-innermode poly-sql-expr-python-innermode
:mode 'sql-mode
:head-matcher (rx "r" (= 3 (char "\"'")) (* (any space)))
:tail-matcher (rx (= 3 (char "\"'")))
:head-mode 'host
:tail-mode 'host
)
```


OK, believe it or not, but this is the meat and potatoes of getting this whole thing to work. I define an *innermode*, which is major mode I want to use inside my Python mode. Take note of the two `head/tail-matcher`

slots. They tell polymode where one major mode begins and ends. I use the superb `rx`

macro to describe a regular expression that’ll match the multiline python string, but you could just as easily give it functions to help it find the beginning and end of another major mode.

As it’s just for demonstration purposes, I limit the regexp so it only matches “raw” strings (Meaning `r"foo"`

vs just `"foo"`

.) You are free to elide that part if you like!

```
s = r"""
SELECT 1 + 1
;
"""
```


Next, I need to tell polymode the things it’s matching belongs to the host mode and not the inner mode. What does that mean? Well, if I made it `body`

and not `host`

, then the string quotes would be considered part of the SQL mode instead of Python, which I don’t want. For some languages (like templating languages) you’d want `body`

and not `host`

because `{{`

and `}}`

, for instance, form part of the template *language* itself.

Now to put it all together:

```
(defun poly-python-sql-eval-chunk (beg end msg)
"Calls out to `sql-send-region' with the polymode chunk region"
(sql-send-region beg end))
(define-polymode poly-python-sql-mode
:hostmode 'poly-python-hostmode
:innermodes '(poly-sql-expr-python-innermode)
(setq polymode-eval-region-function #'poly-python-sql-eval-chunk)
(define-key poly-python-sql-mode-map (kbd "C-c C-c") 'polymode-eval-chunk))
```


The `define-polymode`

macro is the one that binds it all together: we describe the host mode (from earlier) and give it a list of inner modes to use. I also make a few tweaks so `C-c C-c`

– the standard “send to comint” command – works with polymode’s concept of chunks. And that’s it. Define the whole shebang (see below for the full example) and when you next open a `.py`

file (or invoke `M-x poly-python-sql-mode`

manually) you should see the multiline strings highlight correctly.

If you have an interactive SQL comint buffer running, you can use `M-x sql-set-sqli-buffer`

**in the Python-part of the mode** and `C-c C-c`

will happily send the contents of the chunk to that buffer for evaluation.

Finally, you can explore the `C-c n`

keymap (or `M-n`

if you use the default) for other handy commands like `C-c n M-k`

to kill the text in a chunk to the kill ring.

So that’s polymode – what a cool package!

### Full Example

```
(use-package polymode
:ensure t
:mode ("\.py$" . poly-python-sql-mode)
:config
(setq polymode-prefix-key (kbd "C-c n"))
(define-hostmode poly-python-hostmode :mode 'python-mode)
(define-innermode poly-sql-expr-python-innermode
:mode 'sql-mode
:head-matcher (rx "r" (= 3 (char "\"'")) (* (any space)))
:tail-matcher (rx (= 3 (char "\"'")))
:head-mode 'host
:tail-mode 'host)
(defun poly-python-sql-eval-chunk (beg end msg)
"Calls out to `sql-send-region' with the polymode chunk region"
(sql-send-region beg end))
(define-polymode poly-python-sql-mode
:hostmode 'poly-python-hostmode
:innermodes '(poly-sql-expr-python-innermode)
(setq polymode-eval-region-function #'poly-python-sql-eval-chunk)
(define-key poly-python-sql-mode-map (kbd "C-c C-c") 'polymode-eval-chunk))
;; Bug? Fix polymode kill chunk so it works.
(defun polymode-kill-chunk ()
"Kill current chunk."
(interactive)
(pcase (pm-innermost-span)
(`(,(or `nil `host) ,beg ,end ,_) (delete-region beg end))
(`(body ,beg ,_ ,_)
(goto-char beg)
(pm--kill-span '(body))
;; (pm--kill-span '(head tail))
;; (pm--kill-span '(head tail))
)
(`(tail ,beg ,end ,_)
(if (eq beg (point-min))
(delete-region beg end)
(goto-char (1- beg))
(polymode-kill-chunk)))
(`(head ,_ ,end ,_)
(goto-char end)
(polymode-kill-chunk))
(_ (error "Canoot find chunk to kill")))))
```
---
title: Seamlessly Merge Multiple Documentation Sources with Eldoc
url: https://www.masteringemacs.org/article/seamlessly-merge-multiple-documentation-sources-eldoc
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

It’s easy to take *Eldoc*, Emacs’s mild-mannered echo area documentation lookup system, for granted. Originally built for displaying Emacs Lisp documentation at point in the echo area – hence the *El* in *Eldoc* – it now works with a bewildering array of tools.

Eldoc is neither brassy nor is it intrusive, and it is why I love it. It epitomizes Emacs’s philosophy of quiet enjoyment and distraction-free editing. It hides in the background, and it only emerges to share its thoughts about the goings-on around point when it has something clever to say.

Sadly, it’s often drowned out by its braying neighbors: LSP notifications; compiler and linter messages from [Flycheck or FlyMake](https://www.masteringemacs.org/article/spotlight-flycheck-a-flymake-replacement) and who knows what else.

And that’s a problem. Jostling for space in the echo area is a tale as old as Emacs. If you have ever struggled to read an Eldoc or Flycheck message, only to have it mobbed out by another, then you know what I am talking about.

So to work around it, or to imitate lesser editors, intrepid hackers have created a bewildering array of packages to display these messages here, there and – much to my chagrin – everywhere.

The limitation is really Emacs’s fault: the echo area is for transient messages. It was never meant to handle a chorus of noisy packages, all yapping at the same time. But here we are, and it is a vexing problem.

So let’s go about fixing it, thanks to an obscure new Eldoc feature introduced in Emacs 28.

## Configuring Eldoc’s Documentation Strategy

Emacs 28 added the variable `eldoc-documentation-strategy`

. I even wrote about how useful it would be in my article on [what’s new in Emacs 28.1](https://www.masteringemacs.org/article/whats-new-in-emacs-28-1). It controls how Eldoc should handle disparate documentation sources. Yep, that’s right: Eldoc can finally display information from multiple sources **at the same time**!

There are several settings. Each one determines how documentation appears in the echo area. I would encourage you to experiment with each setting and find the one that works for you, but the ones I want to highlight are `eldoc-documentation-compose-eagerly`

and `eldoc-documentation-compose`

.

Both options accomplish the same thing: they mash multiple sources of information together, a feat not possible in earlier versions of Eldoc without a lot of hacking around. The *eager* option displays results as they come in; the other collates all the answers and displays them when they’re all ready. I like the eager option myself.

How it works is very simple. If you add a function (with `add-hook`

) to `eldoc-documentation-functions`

then Eldoc will query the functions in the order they’re in and source documentation from them. Writing such a function is easy, too.

Unfortunately, most packages ought to support this out of the box, but as it’s fairly new, most do not. The ones that do include Eglot and Flymake, though Eglot specifically alters the documentation strategy, so you’ll have to override it in a mode hook. But more on how later.

## Merge Flycheck and Eldoc Messages

But what about packages that don’t work with Eldoc? For instance, Flycheck does not support it, so let me show you how to make it work with Eldoc.

First things first: Eldoc looks for stuff at point, so we need something that can give us the Flycheck messages at point. That’s very easy, thanks to the `flycheck-overlay-errors-at`

function.

Next, we need to design the Eldoc documentation function. It has to be *just so* as it uses a callback mechanism to in effect daisy chain messages together as it walks through the documentation functions.

Here’s one such example — but please experiment, as it’s rather easy to alter this approach to work with other things that Eldoc wouldn’t ordinarily work with.

```
(defun mp-flycheck-eldoc (callback &rest _ignored)
"Print flycheck messages at point by calling CALLBACK."
(when-let ((flycheck-errors (and flycheck-mode (flycheck-overlay-errors-at (point)))))
(mapc
(lambda (err)
(funcall callback
(format "%s: %s"
(let ((level (flycheck-error-level err)))
(pcase level
('info (propertize "I" 'face 'flycheck-error-list-info))
('error (propertize "E" 'face 'flycheck-error-list-error))
('warning (propertize "W" 'face 'flycheck-error-list-warning))
(_ level)))
(flycheck-error-message err))
:thing (or (flycheck-error-id err)
(flycheck-error-group err))
:face 'font-lock-doc-face))
flycheck-errors)))
```


How it works is very simple: I loop over each “error” and for each error I return a string with a dash of color, for good effect. The `:thing`

property is a way of highlighting an especially important part of a documentation string — say the function name or, in this case, the ID or group a Flycheck message belongs to.

With that out of the way, all you have to do is add it to `eldoc-documentation-functions`

and tell Flycheck to not display things as it normally would. Something like this ought to do it:

```
(use-package flycheck
:preface
(defun mp-flycheck-eldoc (callback &rest _ignored)
"Print flycheck messages at point by calling CALLBACK."
(when-let ((flycheck-errors (and flycheck-mode (flycheck-overlay-errors-at (point)))))
(mapc
(lambda (err)
(funcall callback
(format "%s: %s"
(let ((level (flycheck-error-level err)))
(pcase level
('info (propertize "I" 'face 'flycheck-error-list-info))
('error (propertize "E" 'face 'flycheck-error-list-error))
('warning (propertize "W" 'face 'flycheck-error-list-warning))
(_ level)))
(flycheck-error-message err))
:thing (or (flycheck-error-id err)
(flycheck-error-group err))
:face 'font-lock-doc-face))
flycheck-errors)))
(defun mp-flycheck-prefer-eldoc ()
(add-hook 'eldoc-documentation-functions #'mp-flycheck-eldoc nil t)
(setq eldoc-documentation-strategy 'eldoc-documentation-compose-eagerly)
(setq flycheck-display-errors-function nil)
(setq flycheck-help-echo-function nil))
:hook ((flycheck-mode . mp-flycheck-prefer-eldoc)))
```


And that’s pretty much it! Flycheck messages will appear alongside all your other Eldoc documentation messages.

## Fixing Flymake and Eglot

That leaves Flymake and Eglot. Flymake uses Eldoc now by default; that part works fine. That leaves Eglot.

```
(use-package eglot
:preface
(defun mp-eglot-eldoc ()
(setq eldoc-documentation-strategy
'eldoc-documentation-compose-eagerly))
:hook ((eglot-managed-mode . mp-eglot-eldoc)))
```


And that’s that. Now Eglot works in much the same way.

Let’s take a look at some other minor Eldoc features most people don’t know about.

## Lesser Known Eldoc Features

### Dedicated Eldoc Documentation Buffer

Start with `M-x eldoc-doc-buffer`

. It opens a dedicated Eldoc buffer for your documentation. Much like the echo area, this one displays what ever is at point. Great for long-winded error messages that won’t fit on the echo area.

The only annoying thing about it is that it prefers to pop open in an existing window — I find it annoying.

As I’ve written about before in [my article on taming Emacs’s window manager](https://www.masteringemacs.org/article/demystifying-emacs-window-manager) we can tweak its display behavior to better suit us.

```
(add-to-list 'display-buffer-alist
'("^\\*eldoc for" display-buffer-at-bottom
(window-height . 4)))
```


Its buffer name changes depending on the context, and the display rule reflects that. The rule forces the buffer to appear at the bottom of the frame instead with a fixed window height of about 4 lines.

If you really want to, you can tweak `eldoc-display-functions`

and remove the echo area display if you prefer a dedicated buffer.

### Adding More Trigger Commands

Eldoc detects movement and uses its idle delay (`eldoc-idle-delay`

) to determine when to ask its backend documentation functions for information. However, to improve performance, it won’t trigger on *every* command; instead, it maintains a list of common interactive commands.

One problem with that approach is that if you use things like Paredit or [Combobulate, my structured movement and editing package](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), then it won’t display if you interact with one of those commands.

Luckily there’s the `eldoc-add-command-completion`

command:

```
(use-package eldoc
:preface
(add-to-list 'display-buffer-alist
'("^\\*eldoc for" display-buffer-at-bottom
(window-height . 4)))
(setq eldoc-documentation-strategy 'eldoc-documentation-compose-eagerly)
:config
(eldoc-add-command-completions "paredit-")
(eldoc-add-command-completions "combobulate-"))
```


## Conclusion

And that’s that. Eldoc’s finally capable of handling multiple documentation backends! Combine it with the strategy to display multiple document sources at the same time, and you can ditch all those rickety packages that overwhelm your senses with obnoxious popups, tooltips and overlays.

And as you can see, writing your own integration is really easy too. Happy reading!
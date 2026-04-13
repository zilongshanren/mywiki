---
title: 'IEdit: Interactive, multi-occurrence editing in your buffer'
url: https://www.masteringemacs.org/article/iedit-interactive-multi-occurrence-editing-in-your-buffer
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Have you ever heard of [iedit for Emacs](https://github.com/victorhge/iedit) by Victor Ren? Me neither, until recently, and that’s a terrible shame as it is a cornerstone of my programming workflow now that I’ve learned about it.

So what does it do, then?

Well, quite simply, you can edit multiple, identical string occurrences at the same time. The twist here is it uses in-buffer editing without disrupting your workflow with prompts, windows or any of that stuff. You plonk your point down on a word you want to change; you run `iedit-mode`

; and now all the occurrences of that word is highlighted on your screen. When you alter a highlighted word, the other highlighted words change also. How cool is that? Modern IDEs have it already – usually hidden away in the “Refactoring” section – and does exactly the same thing, but iedit is a lot dumber as it cannot infer context beyond *I want to iedit all occurrences of*word* point is on.*

If you regularly replace variables or words with `M-%`

or `C-M-%`

— well, you can retire that workflow now, as iedit will handle it for you. Sure, go ahead; use the older way if you have complex, partial replacements you want to do, but if you’re renaming a variable in a buffer… Why not use iedit?

Here’s a sample demonstration showing what exactly it is I’m talking about, in brilliant technicolor:

![Emacs with IEdit active](../../assets/ca7a9d09107e0db3.png)


## Improving iedit

So iedit’s pretty great and all that, but I don’t replace words across a whole buffer very often; sure, I hear you say: “just `narrow-to-defun`

with `C-x n d`

!” Indeed, narrowing’s great, but this blog is all about half-baked, half-inventions and cobbled-together scripts, and this post is no exception!

I prefer a workflow that minimizes the use of commands to do routine tasks – a fairly common goal for most Emacs hackers. The snippet below does just that. When invoked, it activates iedit for the current defun only.

Note: Don’t forget that although *defun* is Lisp-speak, most modes support all the defun-like commands such as `mark-defun`

or `narrow-to-defun`

.

If you pass an argument to the function, it will *iedit* all occurrences in the entire buffer.

The *iedit* author suggest that you bind `iedit-mode`

– the default command for entering *iedit* – to `C-;`

and I agree: it’s rarely used and easy to type.

```
(require 'iedit)
(defun iedit-dwim (arg)
"Starts iedit but uses \\[narrow-to-defun] to limit its scope."
(interactive "P")
(if arg
(iedit-mode)
(save-excursion
(save-restriction
(widen)
;; this function determines the scope of `iedit-start'.
(if iedit-mode
(iedit-done)
;; `current-word' can of course be replaced by other
;; functions.
(narrow-to-defun)
(iedit-start (current-word) (point-min) (point-max)))))))
(global-set-key (kbd "C-;") 'iedit-dwim)
```
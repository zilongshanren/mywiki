---
title: Why Emacs has Buffers
url: https://www.masteringemacs.org/article/why-emacs-has-buffers
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re new to Emacs, you may wonder why you read and write text from *buffers* as opposed to, you know, *files* or *documents*. There’s the fact that it’s not skeuomorphic, and thus the term lacks the spark that connects it to a real-life concept. Most people have heard of *files* and *documents* in real life, and the term *buffer* is instead a capacious term with little grounding to most people.

To computer scientists and programmers alike, however, the term *buffer* has meaning and purpose; it’s still an unsatisfactory answer, even if it *is* the real reason why Emacs uses the term *buffer*. And just leaving it there – that a buffer is a chunk of memory and used as a means of shuttling data to and fro peripheral hardware, like your disk – does not go far enough in explaining *why*. All editors use *buffers* internally.

In Emacs, the *buffer* is the focal point of nearly all user (and machine!) interactions. You read and you write, and you do so in a structure that tugs at its roots in computer science, but it’s so much more than that. And that’s really what I want to talk about, as it will go a long way towards explaining why Emacs and Emacs Lisp is the way it is.

## What of Strings?

Ask a programmer to write a text editor, and they’ll think of strings and how they are, ultimately, the spine of a text editor. And that seems like a natural and foregone conclusion, indeed: you *need* some way of representing the *text* in a text editor, and strings fill the gap nicely. Fancier programmers may talk about [ropes](https://en.wikipedia.org/wiki/Rope_(data_structure)) and [gap buffers](https://en.wikipedia.org/wiki/Gap_buffer) as a way of optimizing how you store and modify text, and yet I must insist that this is still not a good enough answer to explain what a *buffer* is in Emacs. It’d satisfy the *technical* answer, but not the *philosophical* one.

Junior Emacs Lisp programmers quickly discover – much to their surprise and perhaps consternation – the rather sparse set of functions that operate on strings. Strings are everywhere in elisp; they serve a vital role, and you would struggle to get much done without them. And yet the bulk of functions that do operate on strings solve common problems – like splitting, joining, trimming, and so forth – and the rest a much narrower purpose.

Working with strings is a foregone conclusion to most programmers — it’s a large part of what we do. But the problem with strings (as they relate to the contents of a file, for instance) in Emacs begin when you consider that they have representation – a presence – on your screen. Strings are sequences of characters, but how you look and perceive the string on your screen is a lot more complicated. You’ve got images and different font faces; word-wrapped lines that differ from the physical newlines they’re actually separated by; and not to mention things like narrowed buffers or outright invisible text, like collapsed org mode sections.

You’d need a robust toolkit to operate on these strings in such a way that it’s intuitive and that the mental model of what you see on the screen and how it’s stored is not too different. In fact, this part’s crucial: for every serious elisp hacker, there’s a 100 occasional ones that turn out little snippets of elisp to improve their workflow. Emacs has millions of lines of elisp and thousands of third-party packages exactly *because* the mental shift required is non-existent.

Emacs is not bifurcated, but a lapse of judgment 40 years ago could’ve made it so: a complex, string-fiddly world for Serious Programmers; and a safe, boring, but disjointed, world that “users” are expected to use. That’s how most editors and IDEs work, and you have to pay the piper if you want to join the Serious Programmers.

But not so in Emacs. You see, in Emacs, the buffer you see and interact with on your screen *is* the string.

## Benefits of Emacs’s Buffers

It might surprise you to learn this, but if you want to do complex editing in elisp, you carry it out on a buffer. Maybe that buffer’s the same one as the buffer you asked Emacs to change; maybe it’s a temporary one created for the occasion.

Either way, if you want a custom function that jumps to the next paragraph and kills the one ahead, then you’d combine calls to `forward-paragraph`

and `kill-paragraph`

. In fact, `kill-paragraph`

*itself* uses `forward-paragraph`

to find the extents of the text it needs to kill.

Operating directly on the buffer removes the awkward bifurcation of concerns you’d have with strings and the representation of said strings on your screen.

You also get to leverage the force multiplier of elisp built on elisp — like `kill-paragraph`

using `forward-paragraph`

to find out where the beginning and end of a paragraph is.

```
(defun kill-paragraph (arg)
"Kill forward to end of paragraph.
With ARG N, kill forward to Nth end of paragraph;
negative ARG -N means kill backward to Nth start of paragraph."
(interactive "p")
(kill-region (point) (progn (forward-paragraph arg) (point))))
```


Clever, but also simple. But the *good* kind of simple. You can enable Emacs’s interactive debugger and step through your elisp code as Emacs diligently goes about its business modifying stuff in your buffer. That’s a really powerful visual *and* debug aid. You can even poke around Emacs as it’s doing it and alter the outcome by messing with the buffer state as you’re debugging.

But that’s not all. Emacs’s buffers play a larger role than that:

- Network I/O
Reading from, and writing to, files is a natural enough thing to do in any editor.

But in Emacs this extends to network I/O. You can ask Emacs open a network socket and output the contents to a buffer so you can use the full power of Emacs to interpret and modify the contents. That’s really powerful stuff, and adds symmetry to the idea that in Emacs everything is treated as a buffer.

You’re also given an insight into the actual communication that takes place, as you can inspect the buffer — that is particularly useful if you’re debugging a problem.

- Ephemeral Storage
Maybe you’re munging data or you need a temporary storage space for some logs — just chuck it in a throw-away buffer. You don’t need to save it to a file first as, well, a

*buffer*need not be a file in Emacs.This is of course well-known to everyone who uses Emacs as it’s something Emacs makes heavy use of itself. The

`*Help*`

buffers are one such example.- Pseudo-Terminals and Processes
Not too dissimilar from network I/O at all, but still a great concept to support natively.

If you call

`M-x comint-run`

you can feed it the name of a binary, interactive or otherwise, and Emacs will try to do the right thing. And, yep, it’s using a good, old-fashioned buffer to drive the interaction.More on this:

- Enriching the Output from Commands
When you use

`M-x grep`

,`M-x compile`

,`M-x dired`

, etc. you’re really just looking at a thin veneer on top of the*literal output*from these commands.Try it. Create a throwaway buffer and put this in it and call

`M-x grep-mode`

:`hello.txt:1234:Hello, World`

Emacs uses

`default-directory`

to infer the relative paths to the file(s) in the Grep output. But click on that link, and Emacs will try to take you to`hello.txt`

on line 1234.The same holds for many other commands in Emacs, like

`M-x compile`

.From Emacs’s perspective, it’s a simple and effective way of enriching and integrating commandline tools. And you get to combine them with the power of Emacs.

Why use

`find`

on the command line when you can feed it into Emacs and`dired`

and use`dired`

to bulk edit (or execute commands against) some or all of the output from a`find`

command?More on this:


I think the *buffer* is one of the smartest design decisions in Emacs – along with using LISP as the programming language – because it’s just so flexible and, well, simple? It’s why Emacs’s keyboard macro system works as well as it does: it literally records what you’re doing in the buffer, which results in the exact same outcome when you play it back. That the keyboard macro system is *itself written in elisp* reinforces my point.

So why use the name *buffer*? Because a *buffer* can be a *file*, but it need not be; a *buffer* can host a *document*, but also the output of a process. Emacs’s *buffer* is, technically, just a buffer; yet the philosophy behind it is so much more than that.
---
title: Tree Sitter and the Complications of Parsing Languages
url: https://www.masteringemacs.org/article/tree-sitter-complications-of-parsing-languages
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

You might be surprised to hear when you visit a file in Emacs that the syntax highlighting you are shown on your screen is – most likely – a potpourri of regular expressions with a dash of functions and syntax table definitions. As it turns out, this approach is just about good enough right up until the point where it isn’t.

So there’s a whole host of features in Emacs that tries to work around the inevitable performance or parsing gaps, like giving up if the search space is too large; only partially scanning the buffer; and so on. So when the font locking turns to treacle, and if you’re trained in the eldritch arts, you might have strong opinions on arcana like `jit-lock-stealth-time`

and `jit-lock-antiblink-grace`

.

So why keep doing it that way, then? Well it’s more than good enough. I can think of very few examples where it wasn’t for me; but that’s not to say it’s the platonic ideal of what syntax highlighting should or ought to be, though.

But what’s more surprising is that’s how *most* IDEs and text editors work. Why?

Well, because it’s gosh-darn hard to do it the right way. The proper way is to start with a *grammar* of the language, usually Extended Backus-Naur Format, and work your way through its terse definitions of the language until you have a reasonable grasp of what you need to do and, ah — yes. Now you have to write the parser. And it mustn’t be slow, either; oh, and you have to make it work with broken code, too. Because that’s the resting state of all code that you are editing: as you type the syntax highlighter beavers away in the background to give you some semblance of what reality would look like, if only you’d *hurry up and make it syntactically correct*, thank-you-very-much.

If a regular expression is the answer that yields *two* problems (as the old joke goes), then this is surely the one that yields three or four.

Even if you did have the grammar and an able parser, the grammar might be wrong or it might lack sufficient context to parse it with that alone. For Python it’s good enough; for C or C++ then I wish you good luck. And for Perl (or whatever it’s called these days) only Larry Wall himself can save you.

It’s a hard problem, and many have had a bite of the cherry over the years with mixed results. Building a parser that can handle the unsteady state your ever-changing source code finds itself in is very, very difficult. You also need to generate incremental changes to the *tree* that your parser yields so it doesn’t have to redo the whole thing on every keypress. It’s a really hard problem, but the rewards are *so* worth it though:

- Perfect syntax highlighting.
- Semantic clues, like: variables and function arguments are correctly highlighted in the scope they are relevant in; perfect navigational aids for function and class names; easy refactoring and so much more.
- Inspectable tree that you can use to build out additional tooling relevant to a language.
*Proper*multi-language support like Javascript + React-style JSX in the same page. Or PHP + HTML. Or Yaml + Jinja, etc. etc.

And the list goes on.

## But what about CEDET?

A long time ago a very smart guy named Eric Ludlam created [CEDET](http://cedet.sourceforge.net/), the *Collection of Emacs Development Environment Tools*, a large collection of development tools that aimed to give Emacs a complete IDE-like experience. Eric clearly worked a lot with C++ so that’s what it supported best most of all, but it supports many other common languages like Python, Java and Javascript.

But CEDET opted for something much cleverer than just a package for the C++ universe: he wrote the *Semantic Bovinator*, a parser designed to solve the four points I mentioned above. Unfortunately it never really caught on, even though an effort was made about 10 years ago to hulk smash parts of the code into Emacs proper, where big parts of it lives today. Some features like EDE (project management suite),Speedbar (a navbar), EIEIO (Common Lisp-style Classes) and Semantic Mode (the main draw of CEDET) made it into Emacs core.

(And yes, Eric clearly loved farm-themed naming schemes. Like the old nursery rhyme *Old Macdonald had a farm… EIEIO*)

You can try it right now in your Emacs: open up a Javascript, C/C++, Java, or Python file and type `M-x semantic-mode`

. Now navigate with `M-x senator-xxxxx`

or check out the Semantic keymap with: `C-c , C-h`

. The grammar files haven’t been updated in a long while so it’s possible your code’s ahead of the grammar and it may fail; but still, a herculean effort, and *very* impressive. And I’ll bet you didn’t know Emacs had that for the better part of a decade.

I used CEDET for a while back in the day when it was still actively maintained, and in a parallel universe it might’ve been what we’d all be using today. It worked just shy of well enough for Python that I could not switch to it. It’s a shame it was dropped on the floor as it had everything: EDE the project management suite; semantic code search and completion in Semantic; Speedbar (`M-x speedbar`

); SRecode, a templatized code generator, and so much more.

Which then brings me to the crux of the article: Tree-sitter.

## Tree-sitter

**Note:** Since I wrote this, there is now official support for tree-sitter in Emacs core. See my article [How to Get Started with Tree-Sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) for more information.

Enter [tree sitter](https://github.com/tree-sitter/tree-sitter). It started its life as the semantic tool powering the Atom text editor, before finding its home in many other places, including Github’s code navigation.

It’s quick, and it solves most of the problems I talked about earlier. It also has an impressive list of languages it supports and a *very* large community backing which is important. It’s also available in Emacs for you to use right now: [Emacs Tree Sitter](https://github.com/emacs-tree-sitter/elisp-tree-sitter) and it’s on MELPA. Download, install, and type `M-x tree-sitter-hl-mode`

in a buffer to try it out. It requires module support in your Emacs, though, but that’s usually not a problem with newer Emacsen.

So this is the future of incremental language parsing. And it’ll be the future, too, in Emacs, as there are considerations under way to include the bindings needed to talk to tree sitter directly.

But that’s not all. Tree sitter is easy to use, and it comes with a query language *that uses S-expressions* — which in my mind is fate alone that it was meant to be.

“But what about LSP?” I can hear some of you say. The reason (most) LSP servers don’t offer syntax highlighting is because of the drag on performance. Every keystroke you type must be sent to the server, processed, a partial tree returned, and your syntax highlighting updated. Repeat that up to 100 words per minute (or whatever your typing speed is) and you’re looking at a lot of cross-chatter that is just better suited for in-process communication. But of course that doesn’t mean it can’t replace the language parsing used for other features in LSP!

So I like to think of tree sitter’s role in Emacs as the spiritual successor to what Eric Ludlam started back in the day. It’s super quick and available with several bindings; it has an S-expression-based query language; and it supports dozens of languages out of the box, with more to come. And the author’s a really friendly guy, too.

Luckikly, Emacs 29 adds native tree sitter support and a long-term plan to fully rewrite most major modes to use it. It’ll be interesting to see how the support for tree sitter evolves over time.

## ParEdit Everywhere: Meet Combobulate

[ParEdit](https://www.emacswiki.org/emacs/ParEdit), if you don’t know it, is a supercharged minor mode for LISP-likes. It comes with a large array of tools that operate on S-expressions like merging, joining, splitting and navigating. It’s both powerful and intuitive.

I only use maybe 15% of its capabilities but it greatly speeds up the tedium of refactoring elisp. It’s also a bit of a “holy grail” of what people want in *other* languages.

A decade ago I hacked paredit to kinda-sorta-but-not-really work on Python (yes, seriously) and although some of the features worked it was never really going to happen, but the idea stuck with me. Now that tree sitter (and the *excellent* Emacs Tree Sitter package) is a “thing” I had another crack at it, but this time written from scratch to better pander to the different types of programming languages.

I call it [Combobulate](https://github.com/mickeynp/combobulate). I have written an article about Combobulate and its role as a complex tool for [structured editing and movement](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter).
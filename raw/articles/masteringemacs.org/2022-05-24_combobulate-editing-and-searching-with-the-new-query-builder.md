---
title: 'Combobulate: Editing and Searching with the new Query Builder'
url: https://www.masteringemacs.org/article/combobulate-editing-searching-new-query-builder
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Today I’d like to talk about a slew of new features in [Combobulate](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), my tree-sitter-powered package that adds structured movement and editing to a slew of programming languages. You’ll need Emacs 29, and you must [set up tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) also to use it.

One of the main talking points of tree-sitter is the tree structure it generates from your code. Dealing with tree structures when you want to compare and contrast parts of the tree with a pattern is hard, particularly if you want to, say: check that a class has a method, and that method has a variable named “foo,” which, in turn, is assigned a value… and so on.

I think you get the picture. So, to navigate these expansive trees by hand, it ships with a functional, though quirky, query language modeled on LISP s-expressions. The query language combines search and hierarchical pattern matching into a pragmatic little language. In Emacs 29, it’s used to font lock your code and control indentation. But it’s valuable to more than just major mode authors. It’s valuable to *you*, the overworked developer just trying to get through the day; you just haven’t realized that you need it in your life yet.

![](../../assets/005b66d055135a25.gif)

Now, the thing is, writing queries and testing queries is not fun at all if you want to experiment. Particularly if you have never interfaced with concrete syntax trees, pattern matching, and language grammars before. There’s the double-whammy of learning the query language and its, ah… quirks, and of course, the practicalities of *doing* something with the queries once you’ve written them.

So, one of the things I wanted to write in Combobulate is a user-friendly query builder. Much like Emacs’s venerable [re-builder, an interactive regexp builder](https://www.masteringemacs.org/article/re-builder-interactive-regexp-builder), I built Combobulate’s query builder to work in much the same way. And just like regular expressions, there’s an art and a science to building them.

Tree-sitter queries work like this: you write a query, which looks an awful lot like S-expressions – see the screenshot above for an example – and then you annotate portions of the query with `@name`

, with `name`

being anything you like. That tells tree-sitter to remember the nodes that you’re interested in, provided they match the tree structure you’ve specified. You can be as precise or imprecise as you like: if you want every pair in a dictionary, no problem; if you want just the keys of a dictionary assigned to a variable, then that’s no problem either. Provided your query matches something, it’ll collate all the captured nodes – you can have as many groups as you like – into a list of matches once it’s done scanning your tree.

All you have to do now is yoink the matches and do something useful with them. And that’s where things get a little bit harder. Want to highlight stuff? Now you have to write highlighter code. I hope you know your way around font locking or overlay mechanics. Want multiple cursors placed at every node? Yep. More code. Ditto pretty much everything else.

And that’s where the other new features in Combobulate enter the fray. I’ve added a handful of utilities that’ll do 80% of what you probably want to do with a query.

## Query Building

You can access Combobulate’s query builder either from the popup (`C-x o o`

by default) or by typing `C-c o B q`

. You’ll see a window appear below your current buffer. The query builder is tied to the window you invoked the command in, so keep that in mind.

The query builder has its own popup (`C-c o`

by default), and you can, of course, use `C-h b`

also to see a list of valid key bindings.

Now, if you haven’t already, I recommend you crack open [the Query syntax manual](https://tree-sitter.github.io/tree-sitter/using-parsers#query-syntax) on tree-sitter’s website. It’s a quick read.

Combobulate will proffer completions at point, using your favorite completion framework. It’ll do a reasonable job of being context-aware, so it’ll correctly suggest field names and node names based on the tree hierarchy you’ve described. There’s font locking (syntax highlighting) and basic pretty printing also.

You can pick the color to highlight with by naming the group after a font face, but the names tend to be long. To make life a bit easier, Combobulate ships with a large selection of colors that it’ll auto-suggest if you type `@`

. The names are mapped to font faces when the query is executed. You can customize the list, of course, by modifying `combobulate-query-match-face-alist`

. If you use a name Combobulate does not recognize, it’ll pick a random color for you. Some capture group names have contextual meaning elsewhere in Combobulate, but more on that below.

### Cookie-Cutter Node Queries

Combobulate can pluck the hierarchy of nodes leading to point and insert it into the query builder. You can edit that hierarchy to suit your needs. Use it as a starting point if you’re new to query writing or just want to get on with it. `C-c n`

will copy and match the text of the node at point; `C-c h`

will ask you to pick a parent node from the node at point and then generate the hierarchy from the point node to the parent node you chose. An excellent way to quickly build up a hierarchy of nodes if you want to match function calls inside a method inside a class.

The matcher predicate, `#match`

, is a regexp only, unfortunately. That’s useful, yes, except when it’s not. Combobulate will try to escape regexp metacharacters for you, but I do admit it’s rather imperfect.

Don’t forget, for browsing the node tree, there’s `M-x treesit-explore-mode`

. Marking text in the buffer will update the explorer to show the marked nodes. I recommend you lean into that feature also.

### Highlighting Queries

Because query writing is usually *ad hoc*, or at the very least, something scoped to a file or a directory, you can install queries as highlighters using a file or directory local variable (`C-c f`

and `C-c d`

, respectively).

Combobulate now has two highlighter variables: `combobulate-highlight-queries-alist`

, which is safe for file and directory-local use, and `combobulate-highlight-queries-default`

, an internal variable for language-specific highlighters. Combobulate does come with a couple of default highlighters, just to demonstrate what it can do.

Here’s one that catches the rather insidious implicit tuple notation in Python. I’ve been programming in Python for decades, and this one’ll catch me out every now and again because I refactored something from somewhere else and forgot to remove the comma.

It’s not Combobulate’s job to be a linter or style checker, but it does highlight the utility of on-the-fly querying.

Oh, and if you just want to highlight something for a little while, then `C-c b`

will install the query into the current buffer. I find the command helpful when I need to keep an eye on certain things, particularly during gnarly refactoring sessions. The highlighting is a bit more specific and utilitatiran than the usual [regexp highlighter](https://www.masteringemacs.org/article/highlighting-by-word-line-regexp) feature, but when you absolutely have to highlight only functions calls and nothing else, this is the highlighter for you.

You can also save your query (`C-c C-s`

) to the *query ring*, so you can recall the queries later, not just inside the query builder but in other parts of Combobulate, too. If you use `savehist-mode`

(make sure it’s loaded *after* Combobulate though!), then Combobulate will automatically persist the query ring between sessions.

And if this is all just too much, you can use the “DWIM” feature in `C-c o h h`

. It’ll try to guess the thing at point you want to match. It’s far from perfect, but it might be all you need?

### Editing Nodes

Combobulate’s had support for multiple cursors since day one. It’s a hallmark feature. Correctly selecting the elements you want to edit has always been a challenge with regexp and the bare-bones tooling available to us before the likes of tree-sitter.

Combobulate’s existing editing facilities (see `C-o o t`

) work well enough for localized editing: editing matching tags in JSX; editing all the elements in a list; or the arguments of a function. But if you want specialized editing that suits *your* needs, then you’d have to roll up your sleeves and write some code.

Now, though, you can write your own query and annotate the nodes you want to edit with `@before`

, to put the cursor at the start of a node; `@after`

, for the end; or `@mark`

, to mark the node with a region. Press `C-c e`

(in the query builder) to edit them with multiple cursors. Simple as that.

It also works *outside* the query builder provided you have saved your query to the query ring. Type `C-c o t q`

to edit the active query in the ring, and `C-c o M-n/p`

to cycle the active ring query.

One caveat is limiting the scope of the search. You can do this by either marking the region you want to act on and then narrowing to that region with Emacs’s narrowing feature: `C-x n n`

to narrow; `C-x n w`

to widen. The other method is writing a specific enough prompt to match just the things you want. (The third, having the query mechanism activate at a specific node instead of the root node of the tree, is currently not supported.)

Thanks to the query ring, you can write a handful of useful queries and store them for later use. And if that’s too much of a bother, you can write some elisp code to do this for you:

Now [bind it to a key](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) and you’re set.

Now, you might ask, what if you *don’t* use Multiple Cursors? Perhaps you [prefer keyboard macros](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood) which do have their own set of unique benefits. Well, read on…

### Navigating Query Matches

Editing queries is but one side of the coin. The obverse is, of course, moving or navigating by query matches. Combobulate’s got basic support for Xref, the cross-referencing feature. It’s been in Emacs for what feels like forever, but nowadays it’s actually useful and it plays a prominent role as a long-sought-after replacement for the antediluvian TAGS search (that never really played well with anything else.)

The Xref commands (usually bound to `M-?`

, `C-M-?`

, `M-.`

, etc.) are worth learning about if you have never used them before. Eglot and friends plug into it, to provide seamless reference and definition search and much, much more.

Combobulate does *not* plug into the backend system in Xref. The query thing is far too niche and specialized to want to do that. Instead, you must type `C-c x`

in a query builder buffer, or `C-c o x b`

to trigger Combobulate’s xref feature. It’ll use the query ring if you invoke the xref command outside of the query builder.

Xref’s default behavior is to create a buffer with ordered matches that you can navigate with `M-g M-n`

and `M-g M-p`

, much like you can with [Occur mode](https://www.masteringemacs.org/article/searching-buffers-occur-mode), [Grep & find](https://www.masteringemacs.org/article/dired-shell-commands-find-xargs-replacement), and [Compilation mode](https://www.masteringemacs.org/article/compiling-running-scripts-emacs).

*ad hoc*searching.

The problem with popping up a buffer is that it assumes you want to consume *all* the matches, or at least browse the matches alongside the code. So, if you want to quickly skip to a particular entry, the UI is a bit cumbersome.

Luckily, you can fix that by customizing `xref-show-definitions-function`

and `xref-show-xrefs-function`

. Set them both to `xref-show-definitions-completing-read`

and you’ll instead see your matches presented in your minibuffer (see picture) where you can pick the one you want. I betcha didn’t know Xref could do that! (Note that I had to set *both* variables for this feature to work properly. YMMV, but try setting `xref-show-definitions-function`

on its own first.)

Because completing read is more likely to prove useful for speedy jumping, there’s a special `combobulate-xref-show-xrefs-function`

variable that defaults to `xref-show-definitions-completing-read`

. Set it to `nil`

to use the default Xref behavior, particularly if you want to use keyboard macros where you want to keep track of where you are between macro playbacks.

So what can you use all this for then? Well, why not map out your routes (as I’ve done in the screenshot above) to quickly jump to the router entry in React. Or why not – and I’m sure you have this problem too – collect all your import or include statements with a query so you can jump to the one you want to amend? Sure, your LSP server’s supposed to help you with that, but let’s be honest: it’s often slow and, more often than not, a little bit forgetful or wrong about what you want.

And there you have it. The latest crop of features to hit Combobulate which, you know, is still beta software. So expect bugs! You can [find Combobulate on Github](https://github.com/mickeynp/combobulate).

There are no comments. Why not write one?
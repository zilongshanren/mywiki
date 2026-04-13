---
title: Let's Write a Tree-Sitter Major Mode
url: https://www.masteringemacs.org/article/lets-write-a-treesitter-major-mode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Ah, major modes. There are hundreds of them, and most work in the background, rarely surfacing to tell you what they do or why. They power Emacs, and they grant purpose and verisimilitude [to buffers, one of the most important concepts in Emacs](https://www.masteringemacs.org/article/why-emacs-has-buffers). Without major modes – or indeed the buffers that depend on them – you’d be stuck with a rather dumb and basic editor.

Major modes – particularly programming major modes – are often complex because they have to deal with the raw complexity of interfacing with the syntax of a language: font locking, so the text is highlighted; indentation, so you can format your code; navigation, to help you go where you need to; and editing, so you can avail yourself of Emacs’s complex editing facilities. Major modes are often layered: one major mode deriving some of its complexity from another major mode; others, still, depend on a litany of complex interactions with other parts of Emacs to function. To unravel one complex major mode, you’ll spend weeks pulling at strings woven into the cloth that Emacs is cut from.

It’s a clever system that holds up well for many of its users: the presentable, user-visible edifice is there for all to behold and is generally manageable, once you know your way around Emacs. Peer beneath the surface – perhaps you want to tweak the font locking or indentation – and you might encounter a fiendishly intricate tangle of regular expressions and elisp code that binds the indentation and font lock system together — if you’re lucky you’ll find a neat braid, and if you’re not… a Gordian knot.

That’s hardly the fault of Emacs: it’s just… really complex to get right. The indentation engine for C-like languages (`cc-engine.el`

) is half a meg of dense elisp code: its module description is “core syntax guessing engine for CC mode”, which is a delightfully gnomic summary. It contains 40 years of continued, incremental development and hard-won lessons. It’s a testament to the complexity of some programming languages – *cough* C and C++ – that it’s even required, and still receiving updates.

Tree-sitter is a standard bearer for a new way of doing things, and the topic of this post. I’ve been writing a lot about tree-sitter, and [the complications of parsing languages](https://www.masteringemacs.org/article/tree-sitter-complications-of-parsing-languages). One of tree-sitter’s benefits is that it eschews the need for error-prone regexp by scanning your code and yielding a detailed *concrete syntax tree*, much like a real compiler would do.

Side note: as ambrosial as tree-sitter may be, even it can’t half nelson C into complete submission; achieving tree-like perfection will have to wait if you write tangled preprocessor statements, or regularly write code to the standards required by

[the IOCCC].

But for all other languages, it’s generally very good — and much, *much* simpler to work with. As I’ll demonstrate by writing a major mode for HTML with indentation, syntax highlighting, and Imenu support. Curiously, Emacs 29 doesn’t ship with tree-sitter-enabled HTML support, so this should serve as a fine template for all the other languages that build on top of HTML.

I’m hoping this will demonstrate just how approachable it is to write or amend a TS-enabled major mode. If your favorite language has a TS grammar but lacks an Emacs major mode, you could probably write something that’ll get 80% of the job done in a day or two, even if you’re reasonably new to elisp.

Anyway. Let’s get cracking.

## Prerequisites

You’ll need Emacs 29 compiled with tree-sitter, and you’ll need to know how to install TS grammars. My article [on getting started with tree-sitter](https://www.masteringemacs.org/article/how-to-get-started-tree-sitter) will show you how to do all of this. Start with that.

Next, you’ll need to install the HTML language grammar. You can find it on [on Github](https://github.com/tree-sitter/tree-sitter-html). Note that, for reasons that strain credulity, TS grammars are unversioned. There is no way, aside from a commit hash, to tell which version is which. So “use the latest source, Luke” is, unfortunately, the guiding principle here.

**NOTE:** They’ve finally realized you can number things and have slowly started doing so. But many are still not tagged and few third-party grammars are either. This document assumes you are using the grammar with the tag *v0.20.1*. [Direct link to it here](https://github.com/tree-sitter/tree-sitter-html/releases/tag/v0.20.1). Earlier versions will not work; later ones may not either!

Let’s talk about nice-to-haves. You don’t *have* to do this, but you might find it useful, particularly if you’re following along with another grammar and you are merely using this for reference.

Combobulate, my structured and editing package, has code completion, syntax highlighting, and more for tree-sitter’s query language. Query building is essential: you’ll need it for indentation and font locking. Here’s an article where I talk about the feature in more detail: [Combobulate: Editing and Searching with the new Query Builder](https://www.masteringemacs.org/article/combobulate-editing-searching-new-query-builder).

Some knowledge of Emacs’s tree-sitter implementation is helpful, if not required, if you want to really delve into it: `(info "(elisp) Parsing Program Source")`

. The [official manual](https://tree-sitter.github.io/tree-sitter/) is worth reading also. Make sure you read the chapter on query syntax as I will only cover what we need for HTML, which is a simple language with few moving parts.

You’ll want to use `M-x treesit-explore-mode`

to visualize the tree hierarchy in a buffer. You can only do this once you’ve created the parser, which is one of the first things we configure in the new major mode.

You can find the complete [source on my Github](https://github.com/mickeynp/html-ts-mode).

## How Tree-Sitter Interacts with Buffers

It’s important to recognize that a tree-sitter-powered “major mode” need not be a major mode. The new major modes in Emacs 29 configure a bunch of stuff like font locking and so on, but you don’t *have* to rewrite everything. You can create a tree-sitter parser against any buffer, and keep it at arms length from your existing major modes. Combobulate, for instance, would work reasonably well in non-TS-powered modes (though it does not officially support this presently.)

So, you can have your cake and eat it. It also means you don’t *necessarily* have to use TS for everything: you can often pick and choose. But keep in mind that some major modes use indentation to help with font locking, or font locking to help with indentation. Replace one, and the other may not work!

If you just want to experiment with structured movement and editing, then know that you don’t *have* to create a new major mode. You can build stuff on top of an existing major mode that you like.

## Defining the Major Mode

One of the main things to remember is that we should leverage what’s already there. There’s already an HTML mode in Emacs, naturally. To find it, use `M-x find-function`

to go to where `html-mode`

is. We can see from its form that it inherits from `sgml-mode`

: `(define-derived-mode html-mode sgml-mode ...)`

. `sgml-mode`

, in turn, derives from `text-mode`

.

Now, we *could* inherit from `html-mode`

and try to leverage what that major mode does already, but given that we want to effectively undo all the work that mode does, I think it makes more sense to just use `sgml-mode`

. SGML does do some things that seem a bit off when you first look at its `define-derived-mode`

declaration.

### A quick overview of SGML-mode

*You’ll have to crack open sgml-mode.el to follow along, as it’s too much stuff to include here.*

It’s got a bunch of stuff referencing

`tildify`

. What’s that? Well, given the insignificance of whitespace in SGML-alike languages, you need a way of representing “hard” spaces:` `

is one such method. So, there’s a bunch of complex code to do all of that in`tildify`

. It doesn’t really interfere with what we want to do, and besides: we’re not interested in converting`tildify`

to tree-sitter either.Also, even if you’re a heavy user of Emacs and HTML, I’m 99% sure that you’ve never heard of tildify!

- Aside from that, it does a bunch of work around paragraphs – it’s common for major modes to adjust the paragraph syntax, as it’s meant for prose and not code, to something akin to “paragraphs in code” – and that is what it’s doing here too.
- Adaptive fill is another useful and expansive feature. It’s bound to
`M-q`

(`fill-paragraph`

) and many other commands. And all the code here is doing is to try and guide the fill code so it plays well with SGML-like syntax. Whether it works well or not is in the eye of the beholder. - There’s code to set the comment start, end, and how line breaks are determined. Again, this is something you could reimplement in TS if you wanted, but you’d be leaping ahead of Emacs 29 as there is little official support for TS-powered commenting.
Skeleton is a code templating tool that is often used for more than just that: before

`M-x electric-pair`

became a thing, it was often a stand-in for a wide range of things, such as closing braces or sneakily inserting spaces and newlines in the right places.It’s very similar to its cousin, Tempo, in that they work in much the same way, and both have been neglected for the better part of twenty years.

- There’s some font lock stuff – we’ll ditch that for sure.
`syntax-propertize-function`

is part of Emacs’s core machinery – a lot of it written in C – to help Emacs determine boundaries of things like braces and other syntactically important pairs, like quotes for strings. It does more than that; but it’s commonly used for that.- Imenu takes a regexp (or in TS, a function or regexp) to help you jump to semantically useful HTML element. We’ll be replacing that also.
- Indentation is controlled in part by
`indent-line-function`

. We’ll definitely replace that. The syntax table is also worth mentioning. It’s a table mapping characters to a purpose. Like defining

`;`

is a comment in C; or that`"`

denotes the beginning and end of a string. It’s also responsible for what Emacs consider a word, a symbol, and so on. There’s an existing one called`sgml-mode-syntax-table`

.We

*could*write our own, or we can trust that 30 years of incremental improvements to SGML-mode and friends has resulted in a syntax table that, out of the box at least, probably does what we want.

So… yeah, there is not a lot to the initialization of the major mode. And as you can see, I’m picking and choosing what I want to replace: if the indentation engine works well, you can probably get away with reusing it, if you’re fortunate enough to have an existing one to work from.

### Bare bones HTML major mode

With that in mind, we can write our skeleton major mode.

```
(require 'sgml-mode)
;;;###autoload
(define-derived-mode html-ts-mode sgml-mode "HTML[ts]"
"Major mode for editing HTML with tree-sitter."
:syntax-table sgml-mode-syntax-table
(setq-local font-lock-defaults nil)
(when (treesit-ready-p 'html)
(treesit-parser-create 'html)
(html-ts-setup)))
```


The awkwardly named `treesit-ready-p`

returns non-nil if it is “ready” to deal with the symbol you give it. The symbol being the name of the grammar, which in turn depends on the name of the compiled grammar library you’ve installed.

As far as I know, this is the best (and only) way to check for the presence of a valid grammar. There are no user-facing commands to do this. Either way, if you [eval the elisp](https://www.masteringemacs.org/article/evaluating-elisp-emacs) as it’s shown, you should get back `t`

.

The next step is creating the parser. To do that, you execute `treesit-parser-create`

. Note that it does indeed return the parser object you asked for, but it *also* installs it into the current buffer — so the function name is a bit misleading.

Effectively, despite creating a parser, we want the side-effect of it installing itself into the buffer. To list parsers belonging to a buffer, consult `treesit-parser-list`

.

I recommend you keep the logic of configuring tree-sitter in its own function like I’ve done with `html-ts-setup`

. It just makes debugging and resetting the state easier, so it’s not a hard requirement.

```
(defun html-ts-setup ()
"Setup treesit for html-ts-mode."
;; Our tree-sitter setup goes here.
;; This handles font locking -- more on that below.
(setq-local treesit-font-lock-settings
(apply #'treesit-font-lock-rules
html-ts-font-lock-rules)))
;; This handles indentation -- again, more on that below.
(setq-local treesit-simple-indent-rules html-ts-indent-rules)
;; ... everything else we talk about go here also ...
;; End with this
(treesit-major-mode-setup))
```


The *one thing* you must remember to do after you’ve configured tree-sitter, is to call `treesit-major-mode-setup`

. Do it after you’ve set up your indentation and font lock rules. It’s an essential step, and if you miss it, or apply it inconsistently during development, your font lock and indentation rules won’t apply properly.

Now, let’s write some font lock rules.

## Font Locking

One common criticism of trad-style font locking is the lack of granularity. You had a few levels ranging from zero, to mostly zero, to angry fruit salad, as people who disliked full font locking would often call it. And the lack of contextual granularity didn’t help either: `M-x customize-apropos-face`

and type `font lock face`

and you’ll see a lot more than you did in earlier Emacsen. That’s a good thing: now we have the option to highlight function calls and function names differently, for example.

To better understand how that’s applied, you need to look at `treesit-font-lock-feature-list`

. It’s a list of lists: the sub-lists contain symbols that are unique to each TS major mode. The symbols map to what they’re going to highlight (like `comment`

for comments, and `tag`

for the HTML tag names), and the lists they’re in correspond to the level of font lock engagement. Set `treesit-font-lock-level`

to a number corresponding to how many of the tiers in the list you want Emacs to render. It’s a nice marriage of old and new: you can reshuffle the list to match what you want, if you’re so inclined, or you can set `treesit-font-lock-level`

to a number, if you prefer a simpler approach to managing this.

I’ve opted for this simple feature list. By all means add or remove things to suit your needs.

```
(setq-local treesit-font-lock-feature-list
'((comment)
(constant tag attribute)
(declaration)
(delimiter)))
```


Next up, you need to write the font lock rules. The variable `treesit-font-lock-settings`

is the ultimate variable that controls how font locking works. You probably don’t need to touch it directly. Instead, you’re encouraged to use the function `treesit-font-lock-rules`

to build your rules.

The `treesit-font-lock-rules`

function again is a bit peculiar. It takes a variadic number of arguments which must follow a prescribed pattern, like so:

```
(treesit-font-lock-rules
:language 'html
:override t
:feature 'delimiter
'([ "<" ">" "/>" "</"] @font-lock-bracket-face)
:language 'html
:override t
:feature 'comment
'((comment) @font-lock-comment-face)
... )
```


As you can see, you must specify the `:language`

the rule belongs to. That means you can interleave multiple languages – but more on that in a bit. The `:override`

property is there so you can optionally override a previously-applied font lock rule. Useful as you’ll undoubtedly end up with overlapping rules if your language is complex.

The `:feature`

is the name of the feature. You can pick anything you like, but you’ll need to ensure it is somewhere in `treesit-font-lock-feature-list`

also.

And finally, you write the query you want to highlight.

Top tip. *Don’t* make the mistake a lot of the TS major mode authors did by cramming all their rules into a function call to `treesit-font-lock-rules`

. That’s what the function asks you to do, but I think it’s a huge faux pas, and a peculiar design choice.

If you hardcode the rules as arguments to that function, you (or more likely, a user of your mode) can’t amend the rules post-facto. You can if you put them in a variable first, and then `apply`

them: that way you don’t have to quote everything left, right and center like I did above.

Do this instead:

```
(defvar html-ts-font-lock-rules
'(:language html
:override t
:feature delimiter
(["<" ">" "/>" "</"] @font-lock-bracket-face)
:language html
:override t
:feature comment
((comment) @font-lock-comment-face))
```


If you need to make it dynamic, you still can, using functions or other methods for building the list dynamically from composable variables. (This is more important than you think if you have a grammar that largely intersects with other ones.)

And to apply the rules:

```
(setq-local treesit-font-lock-settings
(apply #'treesit-font-lock-rules
html-ts-font-lock-rules)))
```


Much nicer, and someone else can use your rules in their major mode.

Regardless of the method used, you can safely append to `treesit-font-lock-settings`

at any point, if you so desire. You can add your own rules (using `:override t`

if you have to) to add custom highlighters to an existing major mode, even.

Curiously, there’s no customizable variable for this sort of thing, and so this is the only way. Still, you can do it, and Combobulate’s query builder can do it for you also, if you use it for highlighting.

### Resetting the Font Lock Engine

One common problem is cycling the font lock changes. You can try `C-x x f`

to call `font-lock-update`

. That might do it, depending on your workflow. `defvar`

forms don’t re-set when you `M-x eval-buffer`

, so be sure to eval them manually (`C-M-x`

or `C-x C-e`

) if you do it this way.

A courtesy call to `treesit-major-mode-setup`

won’t go amiss if you think things aren’t working out for you. Query errors may not surface depending on how you reset things. So try different things; go back to a known state (comment stuff out), and retry.

Another way that I like is to cycle the major modes: switch to `M-x fundamental-mode`

and back again.

And what if you to do all of it in one go? [Record a quick keyboard macro](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood).

### Writing Queries

The cardinal rule is the capturing group – which is what tree-sitter matches against, which needn’t be the whole query, much like regexp capturing groups – must be named after the font lock face you want to use. So use something like `@font-lock-comment-face`

for comments.

Here’s an example from Combobulate. I’m using Combobulate’s builtin highlighter shortcuts, but you can use `@some-font-lock-face`

instead.

Combobulate needs to know about the language nodes you want to highlight. To do this for a language that Combobulate does not support (let’s be honest, that’s most likely the case for the language you’re writing!) you will need to:


- Clone Combobulate.
- Edit
`sources.ini`

and add a new entry to the grammar and node JSON files.- Call
`build-relationships.py`

either inside the Docker container if you do not have Python 3.11, or outside.- Re-evaluate the updated
`combobulate-rules.el`

file.- Type
`M-x combobulate-query-builder`

in a buffer with your language code in it. You’ll be prompted for the language to activate.- You’re ready to query.

If you don’t want to use Combobulate to help you, the builtin method – the only method – is to call `treesit-query-capture`

with a starting node (often the one from `treesit-buffer-root-node`

or `treesit-parser-root-node`

) and the query and then manually inspect the output to see if it’s right. Ugh. It’s messy, and it’s hard work. Trust me, I know. I recommend you [learn how to use IELM](https://www.masteringemacs.org/article/evaluating-elisp-emacs) if you decide to go this route.

Also keep in mind that you can give the query machinery (including the font lock rules function) two different styles of queries: strings, which exactly match the syntax that tree-sitter’s official query manual (and engine) expects; *or*, an s-expression form with a few crucial differences. (Combobulate’s query builder works with strings.)

The differences are rather important to know about:

`.`

in the string form (indicating anchoring) becomes`:anchor`

in the s-expression format.- Predicates, like
`#match`

and`#eq`

, become`:match`

and`:eq`

. - Quantifiers, such as
`+`

and`*`

, turn into`:+`

and`:*`

.

That’s it.

When you write a query, make sure you use at least one capturing group or you’ll get zero matches. It’s a design feature: no capture group, no matches. Confusing, but that’s how it is.

So, building on the example query from the screenshot above, the complete version would look a bit like this:

```
(defvar html-ts-font-lock-rules
'(:language html
:override t
:feature tag
((element
[(start_tag (tag_name) @font-lock-variable-name-face)
(self_closing_tag (tag_name) @font-lock-variable-name-face)
(end_tag (tag_name) @font-lock-variable-name-face)]))))
```


Not much to it.

Here’s the complete list:

```
(defvar html-ts-font-lock-rules
'(:language html
:feature delimiter
([ "<!" "<" ">" "/>" "</"] @font-lock-bracket-face)
:language html
:feature comment
((comment) @font-lock-comment-face)
:language html
:feature attribute
((attribute (attribute_name)
@font-lock-constant-face
"=" @font-lock-bracket-face
(quoted_attribute_value) @font-lock-string-face))
:language html
:feature tag
((script_element
[(start_tag (tag_name) @font-lock-doc-face)
(end_tag (tag_name) @font-lock-doc-face)]))
:language html
:feature tag
([(start_tag (tag_name) @font-lock-function-call-face)
(self_closing_tag (tag_name) @font-lock-function-call-face)
(end_tag (tag_name) @font-lock-function-call-face)])
:language html
:override t
:feature declaration
((doctype) @font-lock-keyword-face)))
```


Done right, when you activate `M-x html-ts-mode`

you’ll see everything light up. If not, try fidgeting with `treesit-font-lock-level`

— but beware! It has an edge-trigger to reset font locking in all tree-sitter buffers so changes take effect. You’ll have to set it with `setopt`

or `customize-set-variable`

for the changes to take effect. (Or reset it manually like I showed you above.)

But, yeah, well. That’s it. Churn out some queries and stick ’em in a variable. That’s the long and the short of it. I’ve only covered the basics, but you can use `#match`

and friends to match nodes by regexp — convenient, if you want to highlight comments beginning with TODO, or what have you. The sky is the limit here.

Now, let’s do indentation.

## Indentation

If you’ve never written an indentation engine ‘the old-fashioned way,’ then, well, *lucky you*. Indentation engines are approximately one-third art, one-third science, and one-third misery.

Rewriting an existing indentation engine with tree-sitter will likely shed a chunk of weight and complexity. The declarative indentation engine – based on SMIE, the Simple-Minded Indentation Engine, that’s been in Emacs for years – does cut down on the tedium also.

The key take-away here is to write *one* rule at a time. Pick one corner of the buffer and start from there and work your way through, adding one rule as you go. That’s my recommendation, anyway. Enabling `treesit--indent-verbose`

is also helpful here: when you indent, Emacs will tell you the rule that fired.

Much like font locking, one variable controls indentation: `treesit-simple-indent-rules`

. You feed it declarative rules that look a bit like this:

```
;; Alist of (LANGUAGE . RULES)
`((html
;; Rule 1
((parent-is "element") parent 2)
;; Rule 2
((node-is ,(regexp-opt '("element" "self_closing_tag"))) parent 2)
...
))
```


Such that each RULES entry is of the form `(MATCHER ANCHOR OFFSET)`

. Where `(node-is "element")`

is the MATCHER, in this case a special form defined in `treesit-simple-indent-presets`

. There are many other useful forms, each matching a different node in the tree. Make sure you look, even if you can probably get by with just one or two matchers.

The second value is the ANCHOR, `parent`

, indicating that the indentation engine must find the parent of the node point is near or on: here it’s `element`

for the first rule. The OFFSET is how much to indent, and you can use a variable instead of a scalar.

With little more than simple declarative rules like this one, you can build an effective indentation engine with a bit of grit and perseverance. You probably don’t need more than 10-15 rules for most languages. As always, you can look at how other major modes in Emacs are doing it for inspiration.

You need to read the docstring for `treesit-simple-indent-presets`

and `treesit-simple-indent-rules`

. The manual entries are must-reads also: just punch `i`

from the `*Help*`

window to jump to the pertinent manual node.

One way to write rules is with a simple 1-2-3 exercise:

- Add or amend a rule to
`treesit-simple-indent-rules`

.`*scratch*`

or IELM are good ways to do this. - Reload your major mode, as per above. Now hit
`TAB`

at where you want to test your new rule and observe (with`treesit--indent-verbose`

set to`t`

) that it’s firing the right rule*and*that you’re happy with the indentation. - Hit
`RET`

at the end of the newly-indented line and check if the indentation of the new line is also correct.

You can also try `M-x indent-region`

(bound to `C-M-\\`

) and indent the whole region and observe that everything is properly indented. Combine with `C-M-% ^\s-+ RET RET`

to clear out lines beginning with whitespace to test this.

I can’t promise this will work flawlessly. It *might* work, but it comes down to your major mode and your requirements: it would not work in Python or YAML, for example, as whitespace is contextual in those languages.

There is no amount of writing endlessly about this that can make up for the fact that this is a case of sitting down and experimenting.

I do have some general tips that may help:

The ANCHOR determines the baseline indentation that you can optionally add or subtract from with OFFSET. Never forget this. You first match

*something*(`parent-is`

,`node-is`

, etc.) and*then*you find an anchor from*that*node: perhaps its`parent`

, or something else.The OFFSET is exactly that: a change from the ANCHOR’s position.

- You can pass regexps to the node type. You can use this to compress node rules that are identical to one another. Use
`regexp-opt`

or`rx`

to do this. Some code is

*self-similar*. That is, you can nest the same node type inside the other. Not always, but often. Think of arrays:`[1, 2, [3, ...]]`

.You can define these with two rules:

`((node-is "element") parent 2)`

, to indent the current node; and`((parent-is "element") parent 2)`

to catch the parent. That’ll ensure arbitrarily nested nodes indent properly.Bear in mind that you’ll have to decide on the indentation style separately, of course. For HTML it’s simple.

- Order matters, so if things don’t work well, and you get snared by an earlier rule than the one you wanted, try moving the rules around. They’re processed first-to-last in the order they’re kept in the list.
Ending with a

`no-node`

rule can be useful as a “catch-all” at the end of your rules list.`(no-node parent 0)`

, for example, simply looks at the parent and maintains its indentation offset.Don’t sleep on this rule. It can carry you through an awful lot of “yeah, just keep the current offset”.

- It’s just lisp. So if you want feature switches or toggles, you can splice stuff with backquote (or any number of other ways) to make up the ultimate set of rules.
- You probably want a rule for the root node. In HTML it’s
`document`

(NOTE: in earlier versions it was called`fragment`

), and in other languages it might be`program`

,`source`

,`document`

, etc. This is the baseline rule. I’d put it at the top, but it’s not an iron clad rule.

Let’s look at how to indent HTML. Well… one way of doing it, anyway!

```
(setq-local treesit-simple-indent-rules
`((html
((parent-is "document") column-0 0)
((node-is ,(regexp-opt '("element" "self_closing_tag"))) parent 2)
((node-is "end_tag") parent 0)
((node-is "/") parent 0)
((parent-is "element") parent 2)
((node-is "text") parent 0)
((node-is "attribute") prev-sibling 0)
((node-is ">") parent 0)
((parent-is "start_tag") prev-sibling 0)
(no-node parent 0))))
```


That’s it. There’s more to do in terms of tidying it up (you can merge more nodes, but this is supposed to be readable and instructive) but that is all it takes.

Let me explain the rules as they are.

`document`

is the root node, and if it’s the parent of point when we indent then we anchor against*its*zeroth column (`column-0`

) and add zero to the offset. In other words, the base indentation for anything that is a child of`document`

is 0, because the node itself has an offset of zero also.`element`

and`self_closing_tag`

are the bread-and-butter of SGML languages. The rule looks at those two nodes at point, checks the parent’s offset and adds two. This gives us nice, simple tree-like indentation so that nested elements are indented properly.`end_tag`

needs a bit of explaining. In tree terms, the structure looks a bit like this`(element (start_tag) (end_tag))`

. Meaning, the end and start tags are children of a super-node called`element`

.So when I tell Emacs I want the offset of

`end_tag`

’s`parent`

, I’m getting the offset of`element`

. I want it to be zero, because I want the HTML start and end tags to line up:`<foo> <bar/> Hello, World! </foo>`

- You can match against anonymous nodes, as I do with
`/`

and`>`

. All I want from them that they respect the offset of their parent so they indent properly also. - I occasionally need to align things according to the parent of a node. In the little example above, this would correspond to things like
`text`

. In this case I want to indent by two where the parent is`element`

. That catches`text`

. - Attributes are much the same as what we’ve seen before, but with a crucial difference. I want my attributes to look at their sibling to determine their own indentation: in this case with
`prev-sibling`

and an offset of 0. Emacs will essentially respect the offset of the preceding attribute when it has to indent the current attribute node. `start_tag`

gets the same treatment as attributes do: try to hew to the previous sibling’s offset.- And finally, a catch-all
`no-node`

entry that maintains the offset of its parent.

I’m sure there are better ways of doing it; there are worse ways, too. Ultimately, you can arrive at something that works well using any number of approaches, which I think is a positive thing indeed.

## Imenu

Imenu is the last piece of the puzzle for our scrappy HTML tree-sitter major mode. Conceptually, ignoring tree-sitter here, Imenu is nothing more than a manicured list of stuff to show. It’s not hard to write manually, from scratch, either.

The tree-sitter “simple imenu” system is anything but, though. It’s a bit awkward to use, as it finds its initial matches with either a regular expression or a custom function that is passed each node in the tree. You cannot use a query directly. If you want to pick the name for the Imenu entry (the node name itself is rarely useful or expressive enough) then you’ll have to write a function to do this also. That, or start tangling with the way the tree-sitter defun finder works, as it’s tightly coupled to that system.

Anyway. Here’s a basic example to demonstrate what I am talking about.

```
(defun html-ts-imenu-node-p (node)
(and (string-match-p "^h[0-6]$" (treesit-node-text node))
(equal (treesit-node-type (treesit-node-parent node))
"start_tag")))
(defun html-ts-imenu-name-function (node)
(let ((name (treesit-node-text node)))
(if (html-ts-imenu-node-p node)
(concat name " / "
(thread-first (treesit-node-parent node)
(treesit-node-next-sibling)
(treesit-node-text)))
name)))
(setq-local treesit-simple-imenu-settings
`(("Heading" html-ts-imenu-node-p nil html-ts-imenu-name-function)))
```


The gist here is, we need a way to pick the right nodes, which I am doing here with `html-ts-imenu-node-p`

. You’ll also need a way of building the name of the Imenu entry (`html-ts-imenu-name-function`

). Note that I am using a lesser-known feature in Emacs called `thread-first`

. It “threads” the output from `(treesit-node-parent node)`

into the *first* argument slot of `treesit-node-next-sibling`

, and *that* output into the first argument of `treesit-node-text`

, which is then returned.

Retrieving the element’s `raw_text`

takes a bit of work, but it’s manageable. To see why I need to do this, look at (with `treesit-explore-mode`

) the structure of the node I want to match: the `tag_name`

element is the one we’re matching against to begin with. To get to `raw_text`

I need to get its parent and then its sibling.

Finally, I just assign the desired category (“Heading”) and how to match them.

Imenu caches its results. Use `M-: (imenu-flush-cache)`

to clear out the Imenu cache between tests. And don’t forget about [Which Function Mode](https://www.masteringemacs.org/article/which-function-mode), which plugs into the Imenu machinery to show you the current “function” point is in.

And that’s that.

## Next Steps

With that in place, and knowledge of how to do all of this, tackling `treesit-defun-name-function`

and `treesit-defun-type-regexp`

should be a walk in the park, as it’s similar to Imenu.

Other things worth considering is adding font locking and indentation to the `style`

and `script`

tags. One benefit of tree-sitter is that it can seamlessly merge multiple grammars rather easily with `treesit-range-rules`

.

Unfortunately, Emacs 29’s support for this is still rather poor and immature. And ideally, you’d want to recycle the CSS and JS rules from their respective TS-enabled major modes. But, sadly, that is not so easy to do, as the rules are not declared directly in a variable. You’d have to come up with a wide range of gnarly tricks to get at them. It’s not hard or impossible, but it’s harder than it should be.

And it does not solve the tricky problem of having their respective major modes activate in the right places, either. [Polymode can share major modes in a buffer](https://www.masteringemacs.org/article/polymode-multiple-major-modes-how-to-use-sql-python-in-one-buffer) but it’s not seen much in the way of improvement over the years, and it does not understand tree-sitter.

Still, though, a job well done. I spent longer writing the article than I did writing this integration, which I think says it all.

You can find the complete file, which should work out of the box in the [html-ts-mode](https://github.com/mickeynp/html-ts-mode) repo on my Github.
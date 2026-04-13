---
title: 'Combobulate: Interactive Node Editing with Tree-Sitter'
url: https://www.masteringemacs.org/article/combobulate-interactive-node-editing-treesitter
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Recently, I talked about the challenges around improving [Combobulate](https://www.masteringemacs.org/article/combobulate-structured-movement-editing-treesitter), my package that adds structured editing and movement to Emacs, so navigation is [intuitive and works the way a human expects](https://www.masteringemacs.org/article/combobulate-intuitive-structured-navigation-treesitter). Briefly, instead of relying on elaborate guesswork that breaks easily, there is now a little mini-language that captures how to pluck the right node from the concrete syntax tree provided by tree-sitter, a library that makes it a snap to parse and access said tree of any language for which there is a supported grammar.

Intuitive navigation is hard because if you ask a human developer to navigate up, down, left or right in their code, they can do so effortlessly, as there’s little ambiguity around, say, what constitutes the next “line of code”. Good luck asking a computer to make the right choice when it’s got a baker’s dozen of wildly different nodes to contend with. Hence the mini-language.

But I’ve talked about [that already](https://www.masteringemacs.org/article/combobulate-intuitive-structured-navigation-treesitter). You should read that article first, if you haven’t. So today I’d like to talk about a related issue: when you ask Combobulate to do something – say, cloning the node at point, and in effect duplicating a piece of code – and Combobulate can’t decide which node is the right one, because there’s more than one legitimate node to clone at point.

The problem space is similar to intuitive navigation, but with a twist. When we navigate we have a limited number of sensible directions we can move (up, down, left, right) and the bindings to go with it – `C-M-n`

to move to the next sibling, `C-M-u`

to move up to a parent, etc. – and when we invoke them we’d expect Emacs to just, you know, go to the right place. You don’t *really* want annoying minibuffer prompts, banners, billboards, smoke signals, crop circles or much of anything else to petition you and impede your train of thought. You just want to scoot away and not have Emacs stop you to ask for directions.

Fair enough. Combobulate goes to a lot of trouble to try and pick the right thing for you in most cases, whether you’re editing or moving. Sometimes, though, you must ask the user to make a choice.

And what’s the best way to do that?

## Decisions, decisions…

![](../../assets/e67e4afc171a4fc2.gif)

`TAB`

at the start of a statement and Combobulate will calculate all possible indentation levels and let you choose the one you want interactively.It’s a quagmire, really, because I’d had this issue multiple times where I really wanted some way of asking the user to make a choice. I had played around with the obvious contenders: some form of `completing-read`

(Emacs’s way of doing [minibuffer completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion)) and a hook to update the buffer as you browse through the candidates. It didn’t really work all that well as it assumes you have a completion system that lets you cruise through the candidates interactively. Not everyone uses that; default Emacs has you `TAB`

endlessly to scratch out a completion like some sort of neolithic farm hand. So that method wouldn’t work well for people who use that type of completion, and it also has the annoying problem of feeling like it was the wrong tool for the job. What if someone uses Helm or any number of other completion systems?

I brainstormed some other methods like a [Magit](https://www.masteringemacs.org/article/introduction-magit-emacs-mode-git) transient popup-like thing that you’d pick nodes from, but it also felt cumbersome and I couldn’t figure out how to get transient to do what I wanted it to do.

So I did what I always do: I got bored and went off in search of something else to do.

Right around that time I’d added a primitive version of “expand region”. It is a simple concept, really: given successive key presses, expand the region to incorporate larger and larger structural elements, starting from point. It’s a nifty way of picking things that ordinary Emacs methods struggle to do well at, though I never cared much for it pre-tree-sitter as I found it too imprecise. Lots of people love it, though, and I figured that it’d be super handy with tree-sitter, as it’s so granular, and I wanted to support a wide range of workflows. So I added a basic version in about 30 minutes, and off it went to Github.

![](../../assets/083f4e9fdd2be10d.gif)

`M-h`

. It highlights the item ahead of the current region, to give you an idea of where you are going. A customizable feature to let you select by number is also enabled here, and Combobulate will show you how much it has selected in the tree view as well.A few days later I got a polite and *totally obvious in hindsight* request to make possible to *shrink* the region. It’s all too easy to overshoot your mark as you’re tapping away and, having done so, you’d have no recourse but to start from scratch. Argh. Terrible UX!

So I put on my thinking cap and started wondering how I could crowbar something into `combobulate-mark-node-dwim`

(bound to `M-h`

) so it can toggle the direction and, I… I realized I should just re-use *another* feature I’d added some months prior: a node / region-based indentation command in Python that lets you interactively browse and select the indentation level you want your node or region to have. (Believe it or not, but Emacs’s crummy Python mode can’t cycle all possible indentations of a region. It’s madness. The crux of the code to build it is *right there*, too. No TS required at all.)

The python indentation command (see above) acts like a carousel: keep moving in one or the other direction and you’ll wind up back where you started. That’s great for a wide range of things, particularly when you’re not sure how many finger taps away something is: is it two or *three* indentations I want? Tap a bit and find out, as your buffer updates automatically.

The indentation command was also a bit ham fisted in some ways, but it was a huge improvement over the ghastly python-mode indentation logic you had before which involved manual tedium and `C-x TAB`

to indent by column.

I gambled that if I could file off the rough edges, and build some tooling around it into Combobulate, it could work well for a wide range of tasks. I sat down and spent a fair bit of time hammering out a system of rules and concepts that makes for, I think, a pleasant user experience. Carousel seems like as good a name for it as anything, so that’s what I’ll call it from now on.

If you’re already using Combobulate you’ll of course be familiar with the carousel concept already as it’s been in Combobulate for quite a while.

### Reading a Key vs Minibuffer Prompting

Let me explain. There’s a philosophical view (and some who disagree with this) that certain user-facing actions in Emacs don’t require a full-blown *minibuffer prompt* and that *reading a key* is enough. Which one is the right choice is rarely too contentious, but in a few instances you could lean towards either method, and that’s usually where tempers flash.

Reading a key is mechanically simple: you call `read-key`

(or one of its close relatives) and Emacs will patiently wait for a *key*; any key or key sequence, really. There is no minibuffer history to contend with; recursive minibuffers don’t apply, so you can’t switch out of the minibuffer window, either. You can display a prompt, but the main focus is really about user anticipation: once you know how the command works, and you know it expects a key, you just type it and get on with it. It is about as zero-effort as requesting user input could ever be. It’s used in a wide range of contexts in Emacs today, and it’s perfect when all you need from a user is a key.

The alternative is *minibuffer prompting* which is the all-singing, all-dancing prompt experience you know already.

I want Combobulate’s carousel to read a key: the reason is that it means I can capture the key you typed and, if I decide I have no use for it, I can put the key back on the `unread-command-events`

. I could in theory still do that with the minibuffer prompt, but I still have to deal with the fact that it’s a complex system designed for non-trivial user interactions.

Reading a key is simpler, and that’s important because it meshes well with the idea that the carousel is there to offer a seamless transition in to, and out of it.

### Seamless transition

If you want to expand the region with `M-h`

, you probably want to follow that up with another key. Perhaps `C-w`

to kill the region you just expanded. By *reading the key* I can separate `TAB`

and `S-TAB`

(to cycle to the next and previous choice in the carousel) from irrelevant keys the carousel does not care about. Then, by putting the key the carousel *does not* care about back into the event loop, you can have Emacs carry out what ever it was going to do as though the carousel wasn’t there at all.

End result? You can hit `M-h`

and tap, tap, tap and press any other key that is not recognized by the carousel, and it’ll just execute the key as though you’d never had the carousel at all. No transition; no annoying in-your-face “are you really sure?” prompting; and no thinking required. It behaves the way an experienced Emacs user would expect it to work, and as if you never had the carousel active, even though, there it is, indicating in the echo area that it’s active and awaiting your input.

### Maintaining your tempo

I mentioned that `TAB`

and `S-TAB`

cycle nodes. But if you tap, say, `M-h`

for the first time, the carousel interface appears, and you can then repeatedly type `M-h`

again which is the same as pressing `TAB`

. That way you don’t have to move your fingers away from the triggering key and that helps preserve tempo. It makes for a smoother and easier user experience as you don’t have to context shift: oh I hit `M-h`

and now I have to `TAB`

to expand.

Because I look up the key in a boring, old [keymap](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) it’s easy for anyone to come along and modify it if they want the carousel to use other keys. It also means I can add additional keys that only apply to specific commands: Combobulate’s expand region functionality lets you cycle between the next and previous candidates with `M-h`

and `M-S-h`

, respectively.

The third reason why it’s useful to have the same key is that some operations are incredibly destructive and may leave your buffer in a “broken” state: the syntax is invalid, and tree-sitter may struggle to glue it back together. Having a cohesive view of the buffer at the beginning and operating on it from a clean slate is crucial.

### Cohesion

Let’s say you’re deleting code as part of a refactoring operation you’re doing. As you go about doing it, you’re definitely going to leave your code in a broken state at some point. That’s all well and good: you’re a human, and you can fix it.

Tree-sitter has error-correction built into its parser, but just because it can mend, and partially recover from, broken syntax, does not mean it leaves the resulting tree in a state where an automated tool like Combobulate can make sensible decisions.

That’s particularly true of highly destructive operations like Combobulate’s *splicing* where you’re eliding text as you try to snip and glue two pieces of code back together: the code you’ve decided to keep, and the code *around* the code you’re keeping that the splice deleted. Think of HTML where you want to delete the outer tag but keep the things inside it - that’s one part of what you can do with splicing.

The problem is, maybe you want to splice two times, but the first splice irrevocably breaks your code in such a way that you’d never be able to make it to the second splice. And how do you delete the “outer” something of any old random piece of code, anyway? Take a look at the figure below to see what I mean.

![](../../assets/a596b96c3c8df456.gif)

`M-<up>`

splices up, keeping the siblings, which in this case is one line of code, and then deletes successive parents until it's at the root of the buffer. Note that along the way it leaves the tree in a broken state.Combobulate can splice nearly anything into something else. But that doesn’t mean it makes *syntactic sense* to do so. Maybe you do want it in a broken state; perhaps you want to tweak something to make it legal syntax again. Combobulate can’t read your mind so it has to calculate all possible paths.

If the splice up command – as it used to do – only went up one level, you could easily break the tree in such a way that you wouldn’t be able to splice again. A broken tree often begets an even more broken tree.

To work around *that*, the carousel virtualizes editing and computes everything on the fly, starting from the clean slate your buffer is (presumably!) in when you first initiate the command.

### Virtualized Editing

![](../../assets/6889afa67996a96f.gif)

`C-c o c`

clones a node and, if there are ambiguities, Combobulate will let you cycle through all the choices and interactively preview the change it'll make to your buffer.This was one of the harder things to build.

Tree-sitter generates your tree on-the-fly as you type. Every key press compels tree-sitter to rebuild all or parts of the tree. That is its main benefit, and a lot of work was put into making it fast enough for even the fastest typist to not experience any lag or latency.

Unfortunately, if you ask for a node and subsequently edit the buffer, that node is invalidated and marked outdated. If you try to do anything with it – anything at all, even asking it for its type or where it was in the buffer – it throws an error in your face.

So you can’t collect the node(s) you want at the start and then modify the buffer in-situ, like the indentation example above shows. The first tap would kill the old nodes (we changed the indentation!), and render that approach useless.

Combobulate constructs proxy nodes, and almost every part of Combobulate will accept these proxy nodes in lieu of the real deal. They are slimmed-down versions of the real things, but they reify the most important things we’d want to cling to: the point range in the buffer; the type; the text contained therein; etc.

So when you ask Combobulate to present a carousel it actually virtualizes the nodes before any sort of change can take place. It neatly skirts most issues and lets you write code that can in theory modify the buffer without worrying about your nodes expiring when you touch the buffer. Of course, modifying the buffer means you hold on to outdated information, and Combobulate is no oracle, so if you make substantial changes, the proxy nodes might be thoroughly useless.

Luckily, that’s usually not a problem because of Combobulate’s refactoring display system.

Part of the challenge around the proxy node thing is that most commands do small, localized editing operations: indent some code; expand an envelope; splice some code; clone a node. You get the idea.

As you tap through the carousel’s list of valid nodes, it should show you what would happen if the transformation you asked for is carried out on the currently selected node.

For this to work well, the carousel works in unison with Combobulate’s refactoring system. The latter sounds fancier than it really is: all it lets you do is describe simple transformations, and visual ones to aid users, to make to a buffer. Add in the carousel’s ability to use *undo change groups* to revert buffer changes between choices and you can have visible modifications made to your buffer that is properly restored as you cycle through the choices.

I think it’s important that, if you ask a command to make changes to your buffer, and if there’s more than one way to make that change, that you can preview all possible options. Combine it with the carousel interface and you’re afforded a fair amount of slop when it comes to point positioning.

And if you don’t like the change? You can hit `C-g`

, as with most things in Emacs, to abort the command.

So that’s the carousel interface. I think it makes it much easier to visualize what’s going to happen in a non-committal way, and at the same time scroll through the valid node choices available to you.
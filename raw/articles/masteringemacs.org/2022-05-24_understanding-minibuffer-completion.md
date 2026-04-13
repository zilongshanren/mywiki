---
title: Understanding Minibuffer Completion
url: https://www.masteringemacs.org/article/understanding-minibuffer-completion
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Long ago – so long, in fact, that there’s neither a `NEWS`

nor a source control commit entry for it – Emacs introduced `completing-read`

. `completing-read`

, if you’re not familiar with it, prompts for input from the user and proffers completions. In other words, it’s the function responsible for Emacs’s *minibuffer completion*. It can do more than that; but that’s a quick summary.

Ordinarily, that’d be the end of that, right?

And for the longest time, that *was* the end of it. Historically, Emacs’s completer was rather simple – with little more than basic word completion – and not much better than what you’d get in your garden-variety shell. So intrepid Emacs hackers wrote their own completion functions that went above and beyond what `completing-read`

could do, and that gave us a litany of packages that tried to fix the rather tedious default completer.

I can’t even begin to list all of them. I won’t even try to list all the ones *in Emacs*. A storied example of a completion framework that has been around since the 90s that survives and thrives to this day is [IDO Mode](https://www.masteringemacs.org/article/introduction-to-ido-mode).

IDO holds a special place in my heart. When I started using Emacs I used the default completer because I did not know any better. Imagine my surprise when I cottoned on to IDO mode! It was a large productivity boost and it gave me a different – as I was still rather new to Emacs – insight into Emacs and how it works and what you can do with it. Here’s an off-hand command that *replaces the entire prompt and completion system*. There’s a reason the second article I ever wrote on Mastering Emacs was about IDO.

But IDO is not perfect. It works by hook or by crook; but imperfectly, too, as IDO has to patch parts of Emacs to make it work. That causes friction as you’ll need separate completion functions – `ido-find-file`

vs `find-file`

, for example – for each completion category you want IDO to work with.

Luckily, over the years, the Emacs maintainers made a concerted effort to make completion in Emacs more accessible and extensible.

If you long ago abandoned the default completer – or if you have never tried customizing it – you should give it another shot. Here’s why:

- Category-aware Completion
What you’re looking for is as important as the

*type*of what you’re looking for. How you complete files with`C-x C-f`

is altogether different than what you’d use when you complete buffer names with`C-x b`

or symbols with`M-x`

.Emacs is now aware of the type of completion you’re doing. That means you can tailor your completion styles by category.

- Multiple Styles of Completion
Completion style is a matter of personal preference. It’s something you use all day, every day. And it’s something that you develop an intuition for. So if Emacs ever were to change the defaults – and they’ve cautiously done so over the last decade and a half – you’d want the ability to

*revert*those changes or, indeed, adopt other completion styles you didn’t use before.Combined with category-aware completion, you can tell Emacs that you want flex-style matching (a style of matching such that

`bk`

matches`book`

) for`C-x C-f`

but initials matching (`ttl`

matches`toggle-truncate-lines`

) for`M-x`

.And this is again something that package authors can build on; both by adding more categories, and by extending the type of completion styles Emacs supports.

- Cycling through completion alternatives
Instead of seizing up and asking for more text when there are two or more completion candidates, you can tell Emacs to cycle through them instead.

- Incremental Completion
Yep. Emacs has had

`M-x icomplete-mode`

for an eternity, but it’s seen a number of improvements over the years.Incremental completion supplants the RSI-inducing

`TAB`

-style completion with a candidate list that narrows visually as you type.`M-x fido-mode`

– called Fake IDO, as it’s a facsimile of IDO – is built on top of it, and is new to Emacs 28. But more on FIDO later.- Annotations
Instead of just showing the completion candidates themselves, Emacs has greatly improved the way you attach metadata to them. Package authors can now annotate the completion matches with additional information, like showing a key binding belonging to a symbol in

`M-x`

.- Interoperable Completion Tables
Though it does not directly benefit minibuffer completion much, I would be remiss if I did not at least mention it here, as it’s a core part of Emacs’s plan to open up the completion machinery to one and all.

One common issue in Emacs was the lack of compatibility between completion tables, the bit responsible for sourcing completion candidates. If you wrote code that generates completion data, you’d have to pick a completion tool to expose it through. So if you really liked Helm, you might write some glue code to make it work well with Helm. And if someone else comes along later and wants to make it work with IDO, they’d have to do all manner of nasty deeds to yank the raw data and feed it into IDO.

That’s luckily a thing of the past.

Years ago I wrote about

[PComplete, EShell’s completion framework](https://www.masteringemacs.org/article/pcomplete-context-sensitive-completion-emacs)and it is one example of a standalone completer: it has a number of sources that generate completion data, and a completion layer designed to work specifically with`M-x eshell`

and`M-x shell`

. If you wanted that completion data to show up in Helm — you’d have to roll up your sleeves and write some glue code.Today, it works seamlessly with any completion framework you use, thanks to this consolidation – including the default minibuffer completion system, if you so desire.


OK, so those are the major improvements. Let’s look at how you can take advantage of them.

## Customizing Minibuffer Completion

First things first. Completion intersects with a large swathe of packages and settings in Emacs. Make sure you disable those first. I recommend you test the completion settings in a clean-room environment. Run `emacs -q`

and experiment there instead.

I also want to make it clear that completion is still a planet-sized ball of yarn. Completion systems are messy – *period*. Doubly so in Emacs, as it still supports a wide gamut of third-party and native packages spanning *decades*.

### Minibuffer Key Bindings

A quick key binding refresher is in order, perhaps. There’s only a few, but perhaps more than you know about.

Key Binding | Description |
`RET` , `C-j` | Maybe complete, and maybe exit |
`TAB` | Complete |
`SPC` | Complete Word |
`C-g` | Abort |
`M-v` | Switch to `*Completions*` window |
`TAB` `TAB` or `?` | Show `*Completions*` window |

Some of the key bindings change slightly depending on context. You cannot complete invalid symbols in `M-x`

, for example, as that wouldn’t make sense. But when you switch buffers with `C-x b`

you *can* — maybe you wanted to create a new one. That means `RET`

may complete or exit depending on what you’re asking Emacs to do.

`SPC`

is useful to know about, and you’ve probably discovered that one by accident yourself. It completes to the next “word”. How useful word completion is comes down to the completion styles you’re using. More on those in a bit.

You can double-tap `TAB`

, or type `?`

, to show the `*Completions*`

window. Whether double-tapping works depends on `completion-auto-help`

. But I’ll rate the odds are near zero that you or anyone else has ever bothered changing it!

`M-v`

is one you probably don’t know about. It’s also bound to the harder to type `M-g M-c`

. Neither are particularly logical, although the `M-g`

prefix keymap does have keys that jump to things, so that’s probably why.

Anyway, it reveals and puts the point in the `*Completions*`

window. You can then navigate in it:

Key Binding | Description |
| Forward and backward match |
`z` | Kill buffer |
`RET` | Select match |
`M-g M-c` | Back to minibuffer |

Whether this is of use to you depends greatly on whether you prefer sifting through the `*Completions*`

window or not. Note that you have to use `z`

to kill the buffer and not `q`

like in most other transient buffers.

#### Customizing `*Completions*`


There’s a couple of customizable options that affect `*Completions*`

. The first is `completions-format`

. It controls how matches are ordered: horizontal, vertical, or one column.

The other is `completions-annotations`

, a face for the annotations (if any).

### Changing the default Completion Mechanism

IDO and friends had to assert themselves using hooks and by reinventing the `completing-read`

function. But Emacs 24.1 introduced `completing-read-function`

that hollowed out `completing-read`

and made it a proxy for any function you wanted, provided you mirrored `completing-read`

’s function arguments. What was once the default completer is now named, unsurprisingly, `completing-read-default`

.

Emacs has a number of elementary functions responsible for *reading* an answer from the user. `read-buffer`

for buffers; `read-file-name`

for file names; and so on. They were ‘hollowed out’, so to speak, long before `completing-read`

was and they behave in much the same way: you can tap into how Emacs reads specific input from a user and alter it. I won’t be talking about them any more as I’d rather look at completion as a whole. And it’s in any event filtered through `completing-read`

more often than not, anyway.

And anyway, if you’re using a ‘modern’ third-party completion framework, you can see if it hooks into these systems with `C-h v`

: try it on `completing-read-function`

, `read-file-name-function`

. Some won’t show up here: `icomplete`

being one of them (more on why later); and IDO being another.

Newer completion frameworks are more likely to follow Emacs’s best practices like setting `completion-read-function`

, and maybe the reader functions, but not all of them will. That does not necessarily make them worse than those that do set it.

### Completion Categories

Completing stuff is contextual, and as I alluded to earlier, what you want when you’re completing a file is not necessarily how you’d look up a symbol with `M-x`

or an Xref reference with `M-?`

. Emacs solves that problem by letting you pick completion styles for each category, if you so choose.

What they are, and what they do, is a bit loosey-goosey: it’s up to the provider of completion information to tell Emacs what category it belongs to. Nevertheless, `completion-category-defaults`

offers up a selection of the most common ones:


`buffer`

,`unicode-name`

,`project-file`

,`xref-location`

,`info-menu`

, and`symbol-help`

.

You don’t have to worry about adding, changing or removing categories at all.

What you do care about is how Emacs applies completion styles. Indeed, what you’re completing may exist outside the boundaries of the categories you see above — but more on how that’s resolved below.

### Cycling through Candidates

It’s disabled by default, so most don’t know about this feature, but instead of insisting that you complete more text when you `TAB`

or `SPC`

, you can instead tell Emacs to *cycle* through the remaining candidates.

That’s obviously useful in *some* instances, and you can control when it should take effect by editing `completion-cycle-threshold`

. That variable affects cycle thresholds at a *global* level. You can also configure it per-category, as you’ll see below.

When you set `completion-cycle-threshold`

to `t`

you are effectively disabling the usual `TAB`

mechanism in favor of one that cycles through all the candidates. That is probably undesirable if you have a large number of matches!

So, if you instead give it a number, then it’ll only kick in when there are fewer than that number of candidate matches available. Set it to `nil`

and you disable it.

It’s definitely worth experimenting with, particularly when you have only a few candidate matches left to filter against. Try experimenting with small values like 2, 3, or 5.

### Annotations

Though it’s not that widely used yet in native Emacs, it does come with annotations in Emacs 28.

`suggest-key-bindings`

shows the key bindings, if any, belonging to each symbol in `M-x`

. It’s enabled by default. And the variable `completions-detailed`

controls whether Emacs should include the docstring description for completion candidates in commands like `describe-function`

. I think it’s super handy. so I’ve enabled it.

### Changing Completion Styles

This is perhaps one of the more important things you can change about Emacs’s completer.

The first one is one you’re not interested in editing directly unless you’re writing your own completion routine. But it’s good to know about because it’s where the Emacs draws the style definitions from. So if you crack open `completion-styles-alist`

you’ll see the `NAME`

; a docstring describing how that completion style works; and the names of the functions that do all the work.

In my Emacs, there’s a `helm`

style (because I also use Helm.) It replicates Helm’s multi-completion style so you can use it outside Helm — how nice of the Helm team!

Other styles include `emacs21`

, `emacs22`

, `basic`

, `flex`

, `partial-completion`

, and `initials`

. Your Emacs may have more or less. I recommend you experiment and look yourself.

The variable `completion-category-defaults`

is “internal” and controls the default completion styles for each *category*. You can override it by editing `completion-category-overrides`

.

If you’re not an elisp maven, I recommend you use `M-x customize-option`

to experiment as it supports the nested association list structures required for some of the variables to work. However, note that due to what I think is an oversight, the list of valid categories is strictly less than what’s available to you.

You can control category and the list of styles you want to use. The list of styles is **ordered**: Emacs will apply the first completer, then the second, and so on. So you’ll have to experiment with the ordering to find one you like.

You can also control whether Emacs should cycle candidates by category.

Here’s an example where I enable `initials`

and `flex`

for the `buffer`

category. It will cycle matches if there are fewer than three:

```
(setq completion-category-overrides
'((buffer
(styles initials flex)
(cycle . 3))))
```


*Finally*, that leaves `completion-styles`

. It hosts a list of “catch-all” completers you want **everywhere**. And when I say everywhere, I mean *everywhere*. You see, Emacs checks the completion styles in this order:

- First it checks the category defaults in
`completion-category-defaults`

. - Next, it checks if there are any overrides in
`completion-category-overrides`

. If there are, it uses them instead of #1. - Then, it merges the styles from #1 or #2 with
`completion-styles`

. The category-specific styles in #1 or #2 take precedence over the styles in`completion-styles`

.

If you’re experimenting with completion styles just modify `completion-styles`

. It is my preferred suggestion if you don’t need category-specific overrides. You can always migrate them to categories later.

### Case Sensitivity Matching

Emacs cleverly turns off case-sensitive buffer and file matching if you’re on Windows. On platforms with case-sensitive file systems, it’s enabled by default. But that *does* mean you have to reach for the shift key when you want to complete case-sensitive matches. Not fun.

So if that bothers you, you can force Emacs to ignore casing:

```
(setq read-buffer-completion-ignore-case t)
(setq read-file-name-completion-ignore-case t)
```


### Ignoring File Names and Paths

There are plenty of useless files and directories that you don’t want to match against. You can tell Emacs to not show them by default by customizing `completion-ignored-extensions`

. It comes with a healthy list by default.

Directories must end with a `/`

or Emacs won’t treat it as a directory, though!

It’s got a decent list of defaults already baked in, but I’m sure you can think of more things to add to it:

```
(add-to-list 'completion-ignored-extensions ".bin")
(add-to-list 'completion-ignored-extensions "some-dir/")
```


Emacs will *still* match against ignored “extensions” if there are no other plausible matches, so you’ll never find yourself in a position where you cannot possibly match them.

## Environment Variable Completion

One little-known feature of the default completer is that you can jump to the values of environment variables. Try inputting `$HOME`

(or another of your choice) in `C-x C-f`

. Windows users also benefit from this, but the syntax is the same as Linux.

## Icomplete

Icomplete has been in Emacs for a long while. If you’re not familiar with it, it adds “incremental” completion much in the style of Helm, IDO, and most third-party completers. It does so – contrary to all the talk I just did about `completing-read-function`

earlier – by augmenting the completion experience of the *default* Emacs completion system using hooks.

That means you benefit, more or less, from many of the customizations I just talked about. So if you *do* use Icomplete, you should definitely customize the previously mentioned variables.

Icomplete is still a little bit different than the likes of IDO and most third-party completers. It still carries some of the `TAB`

-style completion mentality that the default completer also uses.

Icomplete also has a useful set of customizable options – too many to repeat here – but they include faces for matches, how long you have to wait before completion candidates appear after typing, and more. If the timings seem “off” to you, you should tweak them. Type `M-x customize-group icomplete`

to customize Icomplete.

Pressing `RET`

won’t pick the selected option; you’re still expected to fully complete in completion prompts that require you to do so (notably `M-x`

). For things like file and buffer prompts, `RET`

will instead just create a blank file or buffer.

Icomplete has its own set of key bindings *in addition to* the minibuffer completion key bindings I listed above:

Key Binding | Description |
`M-TAB` | Force completion |
`C-j` | Force completion and exit |
`C-,` , `C-.` | Forward and backward selection |

Force completion is an Icomplete term. Forcing a completion takes the text of the selected candidate and puts that in your prompt. `M-TAB`

is `Alt+Tab`

which is a rather common key binding to switch windows in most window managers. So you probably won’t be able to use that one without rebinding it.

But the one you’re more likely to care about anyway is `C-j`

: it picks the selected match and exits the completion. Combine it with `C-,`

and `C-.`

and you can move forward or backward through the candidate list.

If you think `C-j`

behaves the way you’d expect `RET`

to behave then you can you of course rebind it. But in that case, you’re better off using FIDO Mode.

## FIDO: Fake Ido

Built on top of Icomplete, FIDO is an attempt to bring some of the features of IDO mode to Icomplete. It’s not entirely successful; but it does make a reasonable attempt at it.

I have written about [IDO Mode](https://masteringemacs.org/article/introduction-to-ido-mode) before, so I will not retread it here. But I’ll summarize why people use IDO: file finding with IDO is exceptionally ergonomic, and it has a large collection of useful key bindings. It also has excellent flex matching, which inspired Emacs’s `flex`

completion style.

FIDO mode builds on top of Icomplete’s key bindings which, in turn, is built on top of Emacs’s default completion key bindings.

Key Binding | Description |
`C-k` | Kill buffer or delete file |
`M-j` | Like `C-j` in IDO. Uses the prompt text. |
`C-s` , `C-r` | Forward or backward selection |
`DEL` | Maybe go up a directory (if it is a file completion) otherwise delete backward char |
`RET` | Pick selected candidate |

If you don’t use IDO, then I think FIDO a great upgrade over Icomplete if you don’t like TAB-style completion. It all but eliminates the percussive *tab, tab, tab* routine you inevitably find yourself in as you try to winnow down your candidate matches to the one you like.

But if you *do* use IDO, it’s not an upgrade at all for file or buffer completion. It definitely *is* for other types of completion if you like IDO-style completion there, though.

What is more interesting is that it is built on top of Icomplete. Many of its features come from tweaking Icomplete and the default completion styles to mirror those found in IDO — so that’s a massive win for the extensibility of Emacs’s default completer.

## Vertical Completion

Quite a few people prefer vertical completion as opposed to the horizontal style of organizing candidates. So if you like vertical completion, then you should know that Emacs 28 introduced `M-x fido-vertical-mode`

and `M-x icomplete-vertical-mode`

.

You can configure how many vertical candidates to show by customizing `max-mini-window-height`

. But beware: this affects all commands that display text in the minibuffer.

## Conclusion

After a decade of slow and steady improvements, Emacs’s default completer is more advanced and capable than it seems. I imagine that, over time, we’ll see more completion frameworks built on top of it.

If you ditched the default completer, then maybe it’s time you give the default completion system another try. Perhaps it does what you need?

And if not, then why not use multiple completion systems? I do. Each category of completion has its own set of challenges and requirements, and perhaps we ask for too much when we expect one completion framework to get everything right, for everyone, all the time.

I really like Helm for its bountiful supply of completion sources replete with topical actions. It’s super fast, comes with both caching and lazy filtering, and it is great for candidate matches where you need more space than you could reasonably fit in the minibuffer. I also use IDO, as I like how it does file and buffer matching.

There’s no harm in picking and choosing what you like.

It’s Emacs, after all.
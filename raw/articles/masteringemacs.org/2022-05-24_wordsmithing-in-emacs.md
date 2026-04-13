---
title: Wordsmithing in Emacs
url: https://www.masteringemacs.org/article/wordsmithing-in-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I was just reading [Jon’s article on Webster’s dictionary from 1913](https://irreal.org/blog/?p=10815) and it prompted me to write about Emacs 28’s dictionary feature.

For you see, I wholeheartedly agree with Jon’s premise that Webster’s 1913 dictionary is a stalwart of wordsmiths everywhere. And Jon (and the thread of blogs he also links to) go to great lengths to make it accessible from Emacs. But as I’ll show you in a moment you can easily enable Webster’s 1913 dictionary (among many others!) in Emacs thanks to the new dictionary lookup feature in Emacs 28.

`M-x dictionary`

is Emacs's dictionary lookup interface.Now I want to make it clear that I distinguish between *spell checking* and looking up a word’s definition in the dictionary. But let’s start with the spell checker first before moving on to the fancy new dictionary lookup system.

## Spell Checking in Emacs

Spell checking is not a builtin feature in Emacs *per se*. Instead it’s outsourced to an external program — usually `aspell`

or the older `ispell`

.

The first thing I recommend you do is decide which dictionary you want to use. You can do so with `M-x ispell-change-dictionary`

or by setting `ispell-local-dictionary`

. I prefer the latter. I can then control the dictionary with a directory or file-local variable.

That way it’ll take effect only for certain files or directory hierarchies, and it means I can switch between US and UK variants of English easily.

The easiest way to do this is with `M-x add-file-local-variable`

. Enter `ispell-local-dictionary`

and then the dictionary you want to use. (You can do the same with directory-local variables and `M-x add-dir-local-variable`

.) Either way, Emacs will either modify your current file or the directory you chose.

**NOTE**: Regardless of the method you use, you must string-quote the value yourself. E.g., `"british"`

and *not* `british`

.

If you don’t know what to input, you can customize `M-x customize-option ispell-dictionary-alist`

to glean the name(s) of the dictionaries you want. This is rather important if you want a dictionary with or without accents, for instance. But make sure the actual dictionary you want is installed on your system.

There’s a large range of customizable options, right up to and including the ability to vary the dictionary used for the fields in an e-mail message. You probably don’t want all that complexity, but it’s there if you need it. Customize `M-x customize-group ispell`

for a complete list of capabilities.

Now you can tell Emacs to spell check the word at point with `M-$`

. It has the benefit of working everywhere as it’s a global key.

For prose and the like, I also enable `M-x flyspell-mode`

as it adds squiggly underlines to misspelled words. There’s an equivalent for programming languages called `M-x flyspell-prog-mode`

that only activates on comments and strings.

## Dictionary Lookup

If you’re as prone to sesquipedalianisms as I am, then you’ll love the new dictionary lookup feature in Emacs 28. I didn’t know this, but there’s an entire client-server protocol (RFC 2229) specifically for this. And it’s delightfully feature rich. I like the cross-referencing especially. It powers Emacs’s dictionary feature and, by default, it’ll reach out to a remote server for the dictionary lookups. But as I’ll explain in a moment, running your own locally is trivial and much better.

Anyway. If you want to look up a word you can type `M-x dictionary`

. You’re taken to a dedicated interface that you can use to look up words or change the search strategy and dictionary to use. It’s the high-touch interactive version, but there are also shortcut commands that skip all of that.

That is why I prefer `M-x dictionary-lookup-definition`

as it looks up the definition of the word at point. I have conveniently [bound that to the key](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) `M-#`

. It’s next to `M-x ispell-word`

(`M-$`

) and to me that seems like as good a place as any.

The definition window that pops up works in much the same way as the info browser or describe system, but it’s admittedly not built on that. But common key bindings do work:

Key Binding | Description |
`SPC` / `S-SPC` | Scroll forward / backward |
`l` | Go to previous definition |
`s` | Search for a new word |
`d` | Search for word at point |
`n` / `p` or `TAB` / `S-TAB` | Forward or backward between links |
`m` | Search for word by pattern |
`D` , `M` | Change default dictionary or search strategy |

There’s also the ever-useful `M-x dictionary-search`

that looks up a word you input. There’s also `M-x dictionary-match-words`

that searches by pattern and strategy.

The strategy warrants a closer look. I recommend you try `M-x dictionary-select-strategy`

and pick one you like. There’s a whole host of ways you can match words, so I recommend that you experiment.

### Tweaking the Layout and Display

The dictionary package is rather generous with its placement of windows and generation of buffers. So if you want just one buffer, I recommend you customize `dictionary-use-single-buffer`

.

I don’t like how it places windows, though. It uses `switch-to-buffer-other-window`

which I consider an anti-pattern for a package to use. It compels Emacs to use a window other than the one you’re using — that, possibly, is what you want. If it is not, you have to [tweak Emacs’s window display rules](https://www.masteringemacs.org/article/demystifying-emacs-window-manager) *and* enable a magic variable to force Emacs to change the window display!

So. I rather like the idea of the digital dictionary being a sidebar companion, much like it would’ve been in the days of yore with lecterns and candlelight and all that, and not an intrusive pop-up like it is now.

So here’s a snippet that customizes `display-buffer-alist`

. The setting forces `*Dictionary*`

buffers to pop up in a sidebar on the left with a fixed width:

```
;; mandatory, as the dictionary misbehaves!
(setq switch-to-buffer-obey-display-actions t)
(add-to-list 'display-buffer-alist
'("^\\*Dictionary\\*" display-buffer-in-side-window
(side . left)
(window-width . 50)))
```


Side windows are indivisible and attach to the sides (unsurprisingly) of an Emacs frame. Feel free to tweak it to your liking. I wrote an article on how to tame [Emacs’s window display](https://www.masteringemacs.org/article/demystifying-emacs-window-manager), so that is a good place to start if you want to know more.

### Running your own Dictionary Server

Emacs’s dictionary lookup will, by default, communicate with a third-party server when you ask it to look up a word. I’d rather it didn’t, so I changed it. Here’s how I did this on Ubuntu:

```
$ sudo apt-get install dictd dict dict-{wn,vera,jargon,devil,gcide,foldoc}
$ sudo systemctl enable dictd
```


I had to manually enable the dictionary service daemon, as that is a requirement for this to work.

To make Emacs use your local server instead of a remote one, customize `dictionary-server`

to `localhost`

:

`(setq dictionary-server "localhost")`


There’s a large range of dictionaries available in Ubuntu/Debian, and I only included the bare essentials above. Of note is `gcide`

, which is a community-maintained version of Webster’s 1913 dictionary. All installed dictionaries are activated and made available to the dictionary server.
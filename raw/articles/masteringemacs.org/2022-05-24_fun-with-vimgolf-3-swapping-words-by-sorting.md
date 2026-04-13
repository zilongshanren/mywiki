---
title: 'Fun with Vimgolf 3: Swapping Words by Sorting'
url: https://www.masteringemacs.org/article/fun-vimgolf-3-swapping-words-sorting
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

[Jon over at Irreal’s](http://irreal.org/blog/?p=1546) been busy with VimGolf challenges, and I figured I’d throw in my two pieces of eight.

The “challenge” is a simple. Take this text:

```
app.config['CHALLENGE_FOLDER'] = SOLUTIONS_FOLDER
app.config['SOLUTIONS_FOLDER'] = CHALLENGE_FOLDER
```


And turn it into

```
app.config['CHALLENGE_FOLDER'] = CHALLENGE_FOLDER
app.config['SOLUTIONS_FOLDER'] = SOLUTIONS_FOLDER
```


As you can see, a simple transposition between two words on a line is all that we need, and Jon’s come up with a solution that solves it in 8 keystrokes. Arguably something like his solution is what *I* would do were I to do it in real life.

I’m not sure if the Vim guys count typing out strings of text as one atomic operation or if they count each character; in Emacs, arguably, each character is in itself a command as each key stroke will invoke `self-insert-command`

but it’s more fun to think of strings of text as a single keystroke, for simplicity’s sake, and to give ourselves a sporting chance against our Vim nemeses.

So here’s my solution. It only solves this particular challenge and nothing more. It relies on the good ole sort order – that `C`

come before `S`

.

`C-x h`

Mark whole buffer`M-x sort-regexp-fields`

Run sort-regexp-fields.

See Sorting Text by Line, Field and Regexp in Emacs for more information.


```
Regexp specifying records to sort: \([a-z\_]+\)$
We want each record – that’s the part of the line we want Emacs to use for sorting – to be the last word on each line
```


`Regexp specifying key within record: \1`


The key – that’s the part inside the capturing group from above – we want to sort by is the entire capturing group.

And we’re done. So how does it work? Well, we rely on the side effect that the word `CHALLENGE_FOLDER`

is less than, lexicographically, `SOLUTIONS_FOLDER`

, because `C`

comes before `S`

.

It boils down to this: `sort-regexp-fields`

is **pure magic**. As my article on the subject talks about at length, you can tell Emacs to only sort by *parts* of a line – the part that matches the regular expression – and using *that* match, you can then tell Emacs how you want to sort that data. We tell Emacs to sort by the last word on each line and leave the rest untouched. Simple :)

So how many keystrokes is that? Good question. I don’t know: it depends on how you count it. Two if you count the commands only; four if you count the commands and the prompts; and many more if you count each character.

As always, these challenges are pointless (though fun!) but they do force you to think on your feet.
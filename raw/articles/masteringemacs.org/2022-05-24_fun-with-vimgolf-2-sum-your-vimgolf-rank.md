---
title: 'Fun with Vimgolf 2: Sum your vimgolf rank'
url: https://www.masteringemacs.org/article/fun-with-vimgolf-2-sum-your-vimgolf-rank
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

## Overall Vimgolf Rank

Here’s another fun vimgolf challenge. The task is simple: get the sum of all the ranks on your vimgolf profile page.

Suppose you are trying to figure out what your overall rank is at Vimgolf(the sum of all the ranks you got), and as a Vim ninja you decided to use Vim to do the job. Your solution should work for every Vimgolf profile page(The actual input file for this challenge is my Vimgolf profile page). So, direct answer insertion is considered cheating.


A pretty specific goal, but the concept will work with anything involving summing numbers in a buffer. Anyway, off we go..

Given this input:

```
Generate Fibonacci Numbers - Rank: 1/66, Score: 20
Use your super vim powers to generate Fibonacci Numbers.
Remove Accent off the Letter - Rank: 1/49, Score: 38
Remove all the accent from extremely accented statements.
Remember FizzBuzz? - Rank: 1/118, Score: 53
Output FizzBuzz to 100. Start with nothing.
(snip)
```


Get this output:

`794`


Now, in the vim challenge you are supposed to end up, as I understand it, with a buffer with nothing but the result – but that’s not a very productive (nor easy) way to accomplish the task.

### Option 1: Using Registers

The first thing we need to do is mark the entire buffer with `C-x h`

. Next, we need to set an *emacs register* – which is a simple store and recall *register* that you can save things like text, numbers, the point and frame or window configurations to for later re-use – by typing `M-0 C-x r n a`

. To break that down a bit, we use the universal argument `M-0`

to tell Emacs that we want the number zero stored in a numeric register `a`

by calling `number-to-register`

, bound to `C-x r n`

.

Next, we will use `query-replace-regexp`

bound to `C-M-%`

and use a little-known feature of Emacs’s regexp engine to, in effect, use the [side effect](http://en.wikipedia.org/wiki/Side_effect_(computer_science)) of a regexp replace on each match.

Input the following:

```
Query replace regexp: Rank: \([0-9]+\)
Query replace regexp with: \,(increment-register (string-to-number \1) ?a)
```


So here we are invoking `increment-register`

(bound to `C-x r +`

) and passing it the contents of the regexp capture group 1 (the rank) by first converting it to an integer so `increment-register`

can make sense of it. We are also passing `?a`

as we need to give it the *character* `a`

and not the string.

When you replace all matches (type `!`

) you’ll see that Emacs will do a “rolling sum” by returning the contents of the new register and thus slowly add up all the ranks, one by one. Thus, if you scroll to the very bottom the last “match” will have the correct answer.

Obviously altering the text is probably not desirable so simply `C-/`

to undo the regexp replace.

And that’s it. Not the snappiest solution but it shows what you can do with Emacs if you really want to.

### Option 2: Using Elisp

Well, if you can write elisp this problem is trivial; the code below will do the same as the above, but it’s a little bit neater and perhaps a bit easier to recycle for other tasks as well.

If you want to know how to run it, then you should read my article on [Evaluating Elisp in Emacs](https://www.masteringemacs.org/articles/2010/11/29/evaluating-elisp-emacs/).

```
(let ((counter 0))
(while (re-search-forward "Rank: \\([0-9]+\\)" (point-max) t)
(incf counter (string-to-number (match-string 1))))
(message "Total sum %d" counter))
```
---
title: Removing blank lines in a buffer
url: https://www.masteringemacs.org/article/removing-blank-lines-buffer
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

This is a frequent question so I figured I’d mention the solution here:

You want to remove all empty (blank) lines from a buffer. How do you do it? Well, it’s super easy.

Mark what you want to change (or use `C-x h`

to mark the whole buffer) and run this:

`M-x flush-lines RET ^$ RET`


And you’re done. So what does that mean? Well, `M-x flush-lines`

will flush (remove) lines that match a regular expression, and `^$`

contain the meta-characters `^`

for *beginning of string* and `$`

for *end of string*. Ergo, if the two meta-characters are next to eachother, it must be a blank line.

We can also generalize it further and remove lines that may have whitespace (only!) characters:

`M-x flush-lines RET ^\s-*$ RET`


In this case `\s-`

is the syntax class (type `C-h s`

to see your buffer’s syntax table) for whitespace characters. The `*`

meta-character, in case you are not a regexp person, means *zero or more* of the preceding character.

**Update** – Pete Wilson asks: “How do you collapse multiple lines into one blank line?”.

That’s a bit harder, mostly because `flush-lines`

only works well on whole, single lines. For multi-line processing you have two choices: you can abuse regexp, or you can use a macro. It’s fairly easy to do it with regexp in this case, but for more complex data-scrubbing I would use a macro; nevertheless, I will do it both ways*.

**I’m pretty sure my macro/regexp examples are general enough to work in all cases; but let me know if they aren’t*

For the regexp approach I will use `C-M-%`

(`query-replace-regexp`

) and because I have to use a literal newline character I will use Emacs’s `quoted-insert`

command, bound to `C-q`

. So to insert a newline, you would type `C-q C-j`

.

The `^J`

represents the literal newline or *line feed* character (see [ASCII Control Characters](http://en.wikipedia.org/wiki/ASCII#ASCII_control_characters) on Wikipedia for more information).

So the text we want to search for looks like this:

```
Search For: ^^J\{2,\}
Replace With: ^J
```


So how does it work? Well, we tell Emacs to search for any *two or more* newlines that are at the beginning of a string – where each line is considered a string by Emacs – and because we search for two or more we skip the ones that only have a single newline. So if there are 10 newlines in a row, we replace them all in one fell swoop with a *single* newline. You can omit the replacement newline to remove them altogether!
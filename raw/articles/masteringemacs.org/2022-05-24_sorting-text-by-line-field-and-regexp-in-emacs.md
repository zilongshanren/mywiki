---
title: Sorting Text by Line, Field and Regexp in Emacs
url: https://www.masteringemacs.org/article/sorting-text-line-field-regexp-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Sorting text is such a common operation that Emacs has several commands dedicated to it, ranging from line-based sorting to complex field sorting by regexp.

## Important Points

### Case Sensitivity

By default Emacs will distinguish between upper and lowercase alphabet when determining sort order, and this behavior is governed by the variable `sort-fold-case`

. Set it to `t`

to force Emacs to ignore case differences when sorting.

### Sorting Order

Emacs will by default use *lexicographic* sorting for all but the `sort-numeric-fields`

command. Make sure you use the right command for the job if you want to sort numbers.

You can reverse the order of *some* sort commands by using a negative argument; for the commands where this does not work you must use `M-x reverse-region`

.

## Sorting by line

The simplest sorting routine is `sort-lines`

and that function does pretty much what you would expect it to.

Let’s sort these names *by line*:

```
Jerry
Elaine
George
Cosmo
```


And this is what the expected output should be:

```
Cosmo
Elaine
George
Jerry
```


## Sorting by Paragraphs and Pages

To sort by paragraph you use the `sort-paragraph`

command. The definition of a paragraph varies by mode, but it is usually defined as anything that is separated by one or more newlines. The variables `paragraph-start`

and `paragraph-separate`

control how paragraphs work.

Emacs will treat something as a page if it is delimited by the *form feed* character, which is ASCII 12. To sort by page use the `sort-pages`

command.

## Sorting by Fields

Sorting by a field is much akin to sorting tabulated data: you have a list of data and you wish to sort by only a subset of that data – a field.

Emacs has two commands to do this: `sort-fields`

for most things; and `sort-numeric-fields`

for numeric sort order. Both **require** a numeric argument if you want to sort by anything other than the first field, where a *field* is defined as anything separated by a whitespace such TAB or SPACE. If you pass a negative argument, then Emacs will count backwards when picking the field to use.

I recommend that you use the numeric sort if you intend to sort by numbers as Emacs is clever enough to detect hexadecimal (if beginning with `0x`

) and octal (if beginning with `0`

) or an entirely different base, as determined by the `sort-numeric-base`

variable, which defaults to `10`

(for decimal.)

*If you don’t sort numbers using the numeric command you risk sorting your numbers the wrong way.*

### Sorting fields

Let’s sort by first name and then by last name:

```
Jerry Seinfeld
Cosmo Kramer
Elaine Benes
George Costanza
```


To sort by first name I type `M-x sort-fields`

. No need for a numeric argument as it will default to one, which is the first field – the first name field:

```
Cosmo Kramer
Elaine Benes
George Costanza
Jerry Seinfeld
```


OK, so that’s nice and easy. Sorting by last name is just as easy. Type `M-2 M-x sort-fields`

and you should see this:

```
Elaine Benes
George Costanza
Cosmo Kramer
Jerry Seinfeld
```


### Sorting fields numerically

Sorting numerically with `sort-numeric-fields`

is much the same as with `sort-fields`

, though I will highlight why it is important to use the correct command when you want to sort numbers.

Consider the following data:

```
4 - Locke
8 - Reyes
15 - Ford
16 - Jarrah
23 - Shephard
42 - Kwon
```


I want to sort by the number, but I will do so with `sort-fields`

and *not* `sort-numeric-fields`

:

```
15 - Ford
16 - Jarrah
23 - Shephard
4 - Locke
42 - Kwon
8 - Reyes
```


Hmm. Not exactly the intended output. The `sort-fields`

command (indeed, so would `sort-lines`

) will sort *lexicographically* and not *numerically*.

Again, with `sort-numeric-fields`

this time:

```
4 - Locke
8 - Reyes
15 - Ford
16 - Jarrah
23 - Shephard
42 - Kwon
```


Much better.

## Sorting by Regular Expression

I love this command. It’s very powerful and lets you do sorting with the precision of a regular expression.

The `sort-regexp-fields`

works by searching the region for everything that matches a *record regexp* and for each match it finds, it looks in that record for a *key regexp*. The key is used to determine how to sort each *record*.

What this means, in practical terms, for you is that you can *sort just a subset of your text* and leave the rest untouched. In other words, you could, if you wanted to, sort only parts of the text but leave the rest as it were; for example, sort everybody’s first name but without shuffling the last name as well.

The key prompt, if left blank, will default to `\&`

, which is the entire match string. If you have capturing groups in the record regexp, you can use the usual `\N`

subexpression matching.

### Emulating sort-lines

To emulate `sort-lines`

you can run `sort-regexp-fields`

with these parameters:

```
Regexp specifying records to sort: ^.*$
Regexp specifying key within record: \&
```


### Complex sorting

Say you want to sort the text below by the *last* character in each last name:

```
Cosmo Kramer
Elaine Benes
George Costanza
Jerry Seinfeld
```


Invoke `sort-regexp-fields`

and use the following parameters:

```
Regexp specifying records to sort: \w+\(\w\)$
Regexp specifying key within record: \1
```


The resultant output is what you would expect –– *almost*:

```
Cosmo Costanza
Elaine Seinfeld
George Kramer
Jerry Benes
```


The sort command only sorted the last name – which is all the *record* regexp matched – and left the first names alone. Let’s try again with a revised record parameter:

```
Regexp specifying records to sort: ^.+\w+\(\w\)$
Regexp specifying key within record: \1
```


Now the output is correct:

```
George Costanza
Jerry Seinfeld
Cosmo Kramer
Elaine Benes
```


So regexp sorting is really powerful but can introduce subtle errors you may not spot right away. *Always* match the entirety of each unit – each record – and never do partial matchess *unless* that is what you want, of course. Use the subexpression matches to pick out the actual keys you want to sort by.

## Conclusion

Sorting in Emacs is really powerful and a very useful tool if you do any sort of data scrubbing or manipulation. But beware the differences between *lexicographic* and *numeric* sorting when you work with numbers, and double-check the regexps you use when you sort by regexp fields.
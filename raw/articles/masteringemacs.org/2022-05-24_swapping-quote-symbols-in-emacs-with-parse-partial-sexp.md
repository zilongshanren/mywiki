---
title: Swapping quote symbols in Emacs with parse-partial-sexp
url: https://www.masteringemacs.org/article/swapping-quote-symbols-emacs-parsepartialsexp
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Ever wonder how Emacs *knows* that the point is next to a balanced expression like a bracket or a string? That `kill-sexp`

or `up-list`

knows how to kill the balanced expression at point or move up one level in a nested set of brackets, in just about any major mode out there?

At a higher level the mode author may choose to write his own parsing routines for handling balanced expressions in that particular mode; but unless your mode’s very special (LaTeX comes to mind) most choose to rely on Emacs’s own ability to parse certain recurring concepts that appear in most major modes – be it something as simple as `text-mode`

or as complicated as a full-blown major mode. A few modes may augment this basic parser with additional functionality, but for a lot of languages (particularly C-like languages) – it’s more than enough.

The secret is `parse-partial-sexp`

and `syntax-ppss`

. The latter function is still an undocumented snippet in `syntax.el`

and yet it’s a first-class citizen used in hundreds of places all over the Emacs elisp source code.

So what makes a barely-kept secret to mode writers such an interesting function? It possesses the unique ability to parse and understand common syntactic elements: comments; strings; and balanced expressions, like brackets. It uses Emacs’s syntax table, a giant key-value table used by modes and some commands to tell Emacs how it should treat alphabetical characters and special characters like `[`

and `"`

.

So the good news is all that information’s already taken care of for you by the mode authors: all you have to do is think of instances where you may want to edit or move by syntax.

So let’s say you want to switch the quote symbols in Python from single to double-quote or vice versa:

```
def foobar():
s = 'Hello█ World'
return s
```


We want to run one command that turns `'Hello█ World'`

into `"Hello█ World"`

where `█`

is the point.

Because `syntax-ppss`

understands the basics of our major mode’s language syntax this is rather easy to do.

Let’s write a function that determines if point is in a string or not (actually, such a function already exists in `thingatpt.el`

called `in-string-p`

):

```
(defun point-in-string-p (pt)
"Returns t if PT is in a string"
(eq 'string (syntax-ppss-context (syntax-ppss pt))))
```


Here I’m using `syntax-ppss-context`

, a helper function that can return three different states: `comment`

, `string`

, or `nil`

.

If you eval `M-: (point-in-string-p (point))`

you can test if the point in the active buffer is in a string or not.

Making a function that does the same for comments is trivial: replace `string`

with `comment`

and bob’s your uncle.

The next piece of the puzzle is that we need to be able to move out of a string if we’re in one or throw an error if we are not. We need to “move out” of it as we want to replace the quotes surrounding a string; the easiest way to do this reliably is to find the bounds of the string: the beginning and end.

```
(defun beginning-of-string ()
"Moves to the beginning of a syntactic string"
(interactive)
(unless (point-in-string-p (point))
(error "You must be in a string for this command to work"))
(while (point-in-string-p (point))
(forward-char -1))
(point))
```


This function is marked as interactive so it can be called through `M-x`

, bound to a key, used in macros, and so forth. Then we test if we’re not in a string: if we are not, we bail out with an error. You could remove that check and rely on the while loop failing the initial condition but then you wouldn’t get an error message that would propagate.

The while loop itself is simple: as long as we’re in a string go forward by negative one characters (that’s the elisp convention for going backwards.) And finally we return the location of point.

The next step is to go to the end of the string. We can do that in two ways: extend `beginning-of-string`

so it’s generic and will take a direction: `-1`

for backwards and `1`

for forwards. The other is to use Emacs’s own set of commands that work on s-expressions, like `forward-sexp`

(`C-M-f`

.)

The latter is easier (and the former left as an exercise to the reader.) What we need now are the points immediately before and after each quote symbol before we start changing things.

If we change the first quote symbol at the beginning of the string then we are left with invalid syntax and Emacs’s `parse-partial-sexp`

cannot reconcile the two mismatched quotes when we call `forward-sexp`

. So we have to store the positions first, and *then* change the quotes.

The other thing we have to remember is to move the point back to the original position where the user called the command; not doing so is considered bad form in elisp land: you should not move the point unless the point (ha) of the command is to move around the buffer.

```
(defun swap-quotes ()
"Swaps the quote symbols in a \\[python-mode] string"
(interactive)
(save-excursion
(let ((bos (save-excursion
(beginning-of-string)))
(eos (save-excursion
(beginning-of-string)
(forward-sexp)
(point)))
(replacement-char ?\'))
(goto-char bos)
;; if the following character is a single quote then the
;; `replacement-char' should be a double quote.
(when (eq (following-char) ?\')
(setq replacement-char ?\"))
(delete-char 1)
(insert replacement-char)
(goto-char eos)
(delete-char -1)
(insert replacement-char))))
```


This interactive command will swap the quotes of the string point is in. It starts out by recording the position of the beginning and end of the string. If we’re not in a string, the command will exit with the error propagated from the `beginning-of-string`

command above.

Next we go to the beginning of the string and we check what the replacement character should be and delete the next character and insert our replacement character. The same is repeated for the end of the string. And finally because we `save-excursion`

at the beginning of the command the point is placed back at its original position.

There are a few obvious improvements: the delete/insertion code could be abstracted into a `letf`

-bound function - but that seems like overkill. Another optimization is supporting triple quotes by using the `looking-at`

function and passing it a regular expression that matches single or double quotes, in singles or triples, and replacing the match with the replacement character.

But the function works. And it could easily work for other modes with interchangeable quotes – or even other paired expressions, like brackets. In fact, making it work with brackets is easier as the built-in command `up-list`

(`C-M-u`

) will go to the beginning of a balanced pair and `forward-sexp`

will go to the end of the balanced pair at point.

Thanks to a little-known feature of Emacs’s syntax parser you can make some simple assumptions about the text in a buffer and act on it in a structured manner.
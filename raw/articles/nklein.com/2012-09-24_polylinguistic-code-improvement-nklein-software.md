---
title: 'Polylinguistic Code Improvement :: nklein software'
url: http://nklein.com/2012/09/polylinguistic-code-improvement/
author: Pat
published: '2012-09-24'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I have started the [Coursera](http://coursera.org) course: [Functional Programming Principles in Scala](https://www.coursera.org/course/progfun). The first assignment was a few simple recursion problems: calculate a given entry in Pascal’s triangle, verify that the parens are balanced in a list of characters, and count the number of ways one can give change for a given amount with given coin denominations. I did those assignments six days ago.

Last night, for grins, I thought I would implement them in Common Lisp. I started out doing them without referencing the Scala code that I’d written. Then, I got lazy and pulled up the Scala code for the last problem and a half.

For all three problems, I came up with better solutions that translated back into the Scala. Some of it was just the benefit of looking at the previous solution again. Some of it was thinking about it with a new language in mind. Some of it was being more comfortable with Lisp. It was such a dramatic improvement in the code that even though I had scored 10/10 six days ago, I still reworked the Scala code and resubmitted it last night.

As it relates to Common Lisp development specifically…. One of the first Lisp books that I read was Paul Graham’s [On Lisp](http://www.paulgraham.com/onlisp.html). In that book, he does a great deal of turning recursive functions into tail-recursive functions. I had followed his idiom of calling the internal function `rec`

:

(labels ((rec (n accum)

(if (zerop n)

accum

(rec (1- n) (* n accum)))))

(rec n 1)))

For the Scala, I started out naming the internal function with a `Rec`

suffix on the function name:

def factorialRec (n: Int, accum: Int): Int =

if (n == 0) accum

else factorialRec(n-1, n*accum)

factorialRec(n,1)

Now, I’m partial to just re-using the function name:

(labels ((factorial (n accum)

(if (zerop n)

accum

(factorial (1- n) (* n accum)))))

(factorial n 1)))

I am also following this course. I must say I enjoy the video lectures, how Martin Odersky presents

There are a few other options available, but these are the biggies (to see a full list, look in the misc/scala-tool-support/ directory under the Scala installation root). My personal recommendation is that you use jEdit or TextMate, though if youâre feeling adventurous youâre free to try one of the Eclipse plugins too. Scala support in Eclipse has the advantage (at least with the beta plugin ) of features like semantic highlighting, code completion (of both Scala and imported Java classes) and other IDE-like features. In my experience though, both Eclipse plugins were unstable to the point of unusable and as such, not worth the trouble. Scala is a much cleaner language than Java, so it really does have less of a need for a super powerful IDE. It would be nice, no question about that, but not essential .
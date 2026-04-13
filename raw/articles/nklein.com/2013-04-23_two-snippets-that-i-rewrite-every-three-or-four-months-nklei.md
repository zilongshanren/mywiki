---
title: 'Two snippets that I rewrite every three or four months… :: nklein software'
url: http://nklein.com/two-snippets-I-rewrite-too-often
author: Pat
published: '2013-04-23'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

A friend of mine is taking a cryptography course this semester. One of his current homework problems involves creating ,

, and

values for

[RSA Encryption](http://en.wikipedia.org/wiki/RSA_(algorithm)). Always one to play the home game when math is involved, I found myself rewriting two snippets of code that I always end up writing any time I do any number-theory related coding.

One of them is simple `EXPONENT-MODULO`

that takes a base , an exponent

, and a modulus

and returns

. There are more efficient ways to do this, but this one is much faster than the naÃ¯ve method and quite easy to rewrite every time that I need it. The idea is that when

is odd, you recursively calculate

and return

. When

is even, you recursively calculate

and return

.


(cond

((zerop e) 1)

((evenp e) (let ((a (expt-mod b (/ e 2) m)))

(mod (* a a) m)))

(t (mod (* b (expt-mod b (1- e) m)) m))))

The other snippet of code is a good deal trickier. Every time I need it, I spend way more time than I want to futzing with examples, getting lost in subscripts, etc. So, while I could rewrite the above in a moment, what’s below, I hope I have the search-fu to find this post next time I need it.

If you have a number and some number

which is relatively prime to (shares no factors except for one with)

, then there exists some number

such that

. And, in fact, all such numbers

for a given

differ by a multiple of

, so there is a unique such

.


Another way of saying and

are relatively prime is to say that their greatest common divisor

is one. Besides being the biggest number that divides into both

and

, the

is also the smallest positive number expressible as

for integers

and

. If you keep track of the steps you use when calculating the greatest common divisor (which in this case is

) while using the

[Euclidean algorithm](http://en.wikipedia.org/wiki/Euclidean_algorithm) you can (with enough care) backtrack through the steps and determine and

for your given

and

.


For example, suppose you had and

. You want to know what

you’d need for

.


The steps in the Euclidean algorithm show:

Working backwards, you can express as a combination of

. Then, you can express

as a combination of

and so on:


Wheee… in my example chosen to be easy to backtrack, the answer comes out to be which is equal to

modulo

. So,

. I picked a lucky number that is its own inverse modulo

. It’s not usually like that. For example,

.


So, anyhow, here’s a function that takes and

and returns two values

and

so that

.


(multiple-value-bind (q r) (truncate n a)

(if (zerop r)

(values 1 0)

(multiple-value-bind (x y) (gcd-as-linear-combination r a)

(values (- y (* q x)) x)))))

Assuming that and

are relatively prime with

, the first value returned is

‘s inverse modulo

.


Recursion, ew.

Here’s the one i’m using:

(defun modular-exp (base exponent modulus)

(loop with result = 1

while (plusp exponent)

if (oddp exponent)

do (setf result (mod (* result base) modulus))

do (setf exponent (truncate exponent 2)

base (mod (* base base) modulus))

finally (return result)))

Thanks for the interesting read. I’ve added these functions to my Emacs environment. I think I found a bug (well, a typo) in expt-mod, the line

(mod (* a a) n)))

should have an m instead of n, shouldn’t it?

Indeed. I had been using different variables than I wanted to use in explaining the code. I didn’t get them all switched. Will fix….
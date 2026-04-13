---
title: 'Inverse functions with fixed-points :: nklein software'
url: http://nklein.com/inverse-functions-with-fixed-points
author: Pat
published: '2013-07-18'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

## Introduction

[SICP](http://mitpress.mit.edu/sicp/) has a few sections devoted to using a general, damped fixed-point iteration to solve square roots and then nth-roots. The [Functional Programming In Scala](https://class.coursera.org/progfun-2012-001/class/index) course that I did on Coursera did the same exercise (at least as far as square roots go).

The idea goes like this. Say that I want to find the square root of five. I am looking then for some number so that

. This means that I’m looking for some number

so that

. So, if I had a function

and I could find some point

where

, I’d be done. Such a point is called a fixed point of

.


There is a general method by which one can find a fixed point of an arbitrary function. If you type some random number into a calculator and hit the “COS” button over and over, your calculator is eventually going to get stuck at 0.739085…. What happens is that you are doing a recurrence where . Eventually, you end up at a point where

(to the limits of your calculator’s precision/display). After that, your stuck. You’ve found a fixed point. No matter how much you iterate, you’re going to be stuck in the same spot.


Now, there are some situations where you might end up in an oscillation where , but

for some

. To avoid that, one usually does the iteration

for some averaging function

. This “damps” the oscillation.


## The Fixed Point higher-order function

In languages with first-class functions, it is easy to write a higher-order function called `fixed-point`

that takes a function and iterates (with damping) to find a fixed point. In SICP and the Scala course mentioned above, the `fixed-point`

function was written recursively.

(labels ((close-enough? (v1 v2)

(<= (abs (- v1 v2)) tolerance))

(average (v1 v2)

(/ (+ v1 v2) 2))

(try (guess)

(let ((next (funcall fn guess)))

(cond

((close-enough? guess next) next)

(t (try (average guess next)))))))

(try (* initial-guess 1d0))))

It is easy to express the recursion there iteratively instead if that’s easier for you to see/think about.

(flet ((close-enough? (v1 v2)

(<= (abs (- v1 v2)) tolerance))

(average (v1 v2)

(/ (+ v1 v2) 2)))

(loop :for guess = (* initial-guess 1d0) :then (average guess next)

:for next = (funcall fn guess)

:until (close-enough? guess next)

:finally (return next))))

## Using the Fixed Point function to find k-th roots

Above, we showed that the square root of is a fixed point of the function

. Now, we can use that to write our own square root function:


(fixed-point (lambda (x) (/ n x)))

By the same argument we used with the square root, we can find the -th root of 5 by finding the fixed point of

. We can make a function that returns a function that does k-th roots:


(lambda (n)

(fixed-point (lambda (x) (/ n (expt x (1- k)))))))

(setf (symbol-function 'cbrt) (kth-root 3))

## Inverting functions

I found myself wanting to find inverses of various complicated functions. All that I knew about the functions was that if you restricted their domain to the unit interval, they were one-to-one and their domain was also the unit interval. What I needed was the inverse of the function.

For some functions (like ), the inverse is easy enough to calculate. For other functions (like

), the inverse seems possible but incredibly tedious to calculate.


Could I use fixed points to find inverses of general functions? We’ve already used them to find inverses for . Can we extend it further?


After flailing around Google for quite some time, I found this article by [Chen, Lu, Chen, Ruchala, and Olivera](http://online.medphys.org/resource/1/mphya6/v35/i1/p81_s1?isAuthorized=no) about using fixed-point iteration to find inverses for deformation fields.

There, the approach to inverting was to formulate

and let

. Then, because


That leaves the relationship that

I messed this up a few times by conflating and

so I abandoned it in favor of the tinkering that follows in the next section. Here though, is a debugged version based on the cited paper:


(lambda (x)

(let ((iterant (lambda (v)

(flet ((u (x)

(- (funcall fn x) x)))

(- (u (+ x v)))))))

(+ x (fixed-point iterant 0d0 tolerance)))))

Now, I can easily check the average variance over some points in the unit interval:

(flet ((sqr (x) (* x x)))

(/ (loop :with dx = (/ (1- steps))

:with inverse = (pseudo-inverse fn)

:repeat steps

:for x :from 0 :by dx

:summing (sqr (- (funcall fn (funcall inverse x)) x)))

steps)))

(check-pseudo-inverse #'identity) => 0.0d0

(check-pseudo-inverse #'sin) => 2.8820112095939962D-12

(check-pseudo-inverse #'sqrt) => 2.7957469632748447D-19

(check-pseudo-inverse (lambda (x) (* x x x (+ (* x (- (* x 6) 15)) 10))))

=> 1.3296561385041381D-21

## A tinkering attempt when I couldn’t get the previous to work

When I had abandoned the above, I spent some time tinkering on paper. To find , I need to find

so that

. Multiplying both sides by

and dividing by

, I get

. So, to find

, I need to find a

that is a fixed point for

:


(lambda (x)

(let ((iterant (lambda (y)

(/ (* x y) (funcall fn y)))))

(fixed-point iterant 1 tolerance))))

This version, however, has the disadvantage of using division. Division is more expensive and has obvious problems if you bump into zero on your way to your goal. Getting rid of the division also allows the above algorithms to be generalized for inverting endomorphisms of vector spaces (the function being the only slightly tricky part).


## Denouement

I finally found a use of the `fixed-point`

function that goes beyond -th roots. Wahoo!


As you probably discovered, you can use most root finding algorithms for scalar/vector functions to find their inverses (mileage may vary depending on algorithm/function combination), eg. Newton’s method, by the simple transformation: for

f(x) = c solve f(x) – c = 0 with your favorite algorithm.

This will give you the x for which f(x) = c ie. the inverse f^-1(c).

This way can also make efficient use of derivatives, which can be analytic for most functions even when their inverse is not.

Root finding methods are generally more efficient versions of the standard fixed point iteration, but they can be something else as well, eg. genetic algorithms, which are good if the inverse is multi-valued.
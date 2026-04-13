---
title: 'Quadratic Number Fields :: nklein software'
url: http://nklein.com/2025/08/quadratic-number-fields/
author: Pat
published: '2025-08-05'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I want to explore arrangements of balls in *n*-dimensions. In particular, I am interested in exploring [kissing numbers](https://en.wikipedia.org/wiki/Kissing_number) in five or more dimensions. I want to ensure that if I come up with a configuration which improves upon the known lower-bounds that I have a precise specification of where to place the kissing balls.

If I place a unit ball at the origin, all of the other unit balls that touch it have centers two units away from the origin. So, I need a set of length two vectors such that for any pair of those vectors, the dot product is at most two (the dot product is and with

less than

then unit spheres at those locations would overlap each other). If I keep (n-1) of the coordinates rational, the n-th coordinate will be the square root of a rational number.


So, I want to do math involving rational numbers and square roots of rational numbers without subjecting myself to floating-point errors.

I created a library using `GENERIC-CL`

to do this math. The library is called `RATIONAL-EXTENSIONS`

(though I am wondering if I should call it `QUADRATIC-NUMBER-FIELDS`

instead). You can find it here: [https://github.com/nklein/rational-extensions](https://github.com/nklein/rational-extensions)

This library allows one do things like:

(* (+ 1 (sqrt 2/3)) (- 1 (sqrt 2/3))) => 1/3 ;; instead of 0.33333328<br>

With this, I have started working on application to allow one to explore kissing spheres in n-dimensional space. Here is an early screenshot with 13 5-dimensional balls kissing a central ball. Five of those, I calculated by hand as corners of a regular 5-simplex of side-length 2 with one vertex at the origin. The other 8 balls, I placed by rotated around in the (x,y,z) view on the left and/or the (z,w,v) view on the right and dropping a ball.

![](../../assets/5cf038650b0338c7.jpg)

More when that app is more full-featured and less clunky.
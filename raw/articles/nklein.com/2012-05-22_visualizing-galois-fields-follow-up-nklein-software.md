---
title: 'Visualizing Galois Fields (Follow-up) :: nklein software'
url: http://nklein.com/2012/05/visualizing-galois-fields-follow-up/
published: '2012-05-22'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In my [previous article](http://nklein.com/2012/05/visualizing-galois-fields/), I should have finished by remapping the multiplication and addition tables so that the multiplication table was in cyclic order. In cyclic order, the zeroth column (or row) represents zero and the -th column (or row) (for

) represents

for some generator

. As such, the multiplication table is simply

in the zeroth row and column and

for the spot

.


![gf256m](../../assets/d2176f9488b0aff8.png)


![gf256m](../../assets/d2176f9488b0aff8.png)

Once resorted by the order of the powers of a generator , the multiplication table look the same regardless of the

. The addition, however, looks different for different generators. Below are the addition tables for two of them:

on the right and

on the left. They make as decent a stereo as any of the other pairs so far.


![gf256a-00000011](../../assets/f4b86c8d9e0ac80f.png)


![gf256a-00000011](../../assets/f4b86c8d9e0ac80f.png)

![gf256a-11001000](../../assets/198f47cd1ff87c48.png)


![gf256a-11001000](../../assets/198f47cd1ff87c48.png)

Here’s the code that I used to generate the remapping for a given generator.

(let ((to (make-array (list limit) :initial-element 0))

(from (make-array (list limit) :initial-element 0))

(used (make-hash-table :test #'equal)))

;; fill up the lookup tables

(setf (gethash 0 used) t)

(nlet fill-tables ((exp 1) (acc 1))

(when (< exp limit)

(setf (aref to exp) acc

(aref from acc) exp

(gethash acc used) t)

(fill-tables (1+ exp) (funcall fn acc generator))))

;; return a closure around the lookup tables

(when (= (hash-table-count used) limit)

(lambda (direction n)

(ecase direction

(:to (aref to n))

(:from (aref from n)))))))

If you’ve read it, you can probably tell by my code that I’m still under the influence of [Let Over Lambda](http://letoverlambda.com/). If you haven’t read it, it is quite worth the read.

Then, I used a modified version of the `draw-heightmap`

function which also takes in the remapping function.

(let ((png (make-instance 'zpng:pixel-streamed-png

:color-type :grayscale

:width limit

:height limit)))

(with-open-file (stream filename

:direction :output

:if-does-not-exist :create

:element-type '(unsigned-byte 8))

(zpng:start-png png stream)

(dotimes (xx limit)

(dotimes (yy limit)

(let* ((a (funcall map :to xx))

(b (funcall map :to yy))

(c (funcall map :from (funcall op a b))))

(zpng:write-pixel (list c) png))))

(zpng:finish-png png)))

(values))
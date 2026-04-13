---
title: 'Literate WordPress :: nklein software'
url: http://nklein.com/2010/05/literate-wordpress/
author: Pat
published: '2010-05-06'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I use [WordPress](http://wordpress.org/) along with the [CodeColor](http://wordpress.org/extend/plugins/codecolorer/) plugin. This works fairly well for me. I find myself, however, breaking code up into sometimes awkward chunks to describe the code here or leaving things in very long segments.

Further, I often leave them ordered in my post in an order where they would compile if you just copied them into a file in the order presented. That’s not always the most useful order to present the code.

[Literate programming](http://en.wikipedia.org/wiki/Literate_programming) seeks to tackle exactly these problems. So, I got to thinking: Why don’t I write some filters for

[noweb](http://www.cs.tufts.edu/~nr/noweb/) to output into WordPress+CodeColorer.

### My Solution

My solution is in two parts, one filter of general use to all noweb users which simply inserts `@language`

tags into the noweb stream and a noweave backend that outputs something you can just paste into the WordPress (HTML) input box.

Here is an example of how I used this to process the *post.nw* file that I used to compose this post.

noweave -n -filter langify-nw -backend wordpress-nw post.nw

[langify-nw](http://nklein.com/wp-content/uploads/2010/05/langify-nw.txt)script[wordpress-nw](http://nklein.com/wp-content/uploads/2010/05/wordpress-nw.txt)script[tee-nw](http://nklein.com/wp-content/uploads/2010/05/tee-nw.txt)script useful for debugging noweb streams[post.nw](http://nklein.com/wp-content/uploads/2010/05/post.nw)literate source for this post (technically, I tweaked it a bit after proofreading without going back to the source combining the first two paragraphs and changing <h2>’s to <h3>’s and adding this parenthetical)

The *langify-nw* script guesses the language for each chunk based on the filename extension on the top-level chunk that incorporates that chunk. That’s why I used filename extensions on the top-level chunks in this post.

### An Example

Several months back, I posted some code for [rendering anti-aliased text in OpenGL](http://nklein.com/2010/01/better-text-rendering-with-cl-opengl-and-zpb-ttf/). At the bottom of that post, I had an unwieldy 33-line function that you have to scroll to see with the way my blog is styled.

This would have been an excellent candidate for literate programming. Here is that same function broken up with noweb chunks with some descriptive text sprinkled between chunks.

At the heart of the algorithm, I need to take some point `<px, py, pz>`

, run it backwards through all of the projection matrices so that I have it in pixel coordinates, and calculate the distance between that and the screen coordinates of the origin. So, I have this little function here to do that calculation given the object-local coordinates `<px, py, pz>`

and the origin’s screen coordinates `<ox, oy, oz>`

.

(dist-to-point-from-origin (px py pz ox oy oz)

(multiple-value-bind (nx ny nz)

(glu:un-project px py pz

:modelview modelview

:projection projection

:viewport viewport)

(dist nx ny nz ox oy oz)))

That, of course, also needs to determine the distance between two three-dimensional points. For my purposes, I don’t need the straight-line distance. I just need the maximum delta along any coordinate axis.

(dist (x1 y1 z1 x2 y2 z2)

(max (abs (- x1 x2))

(abs (- y1 y2))

(abs (- z1 z2))))

Also, to do those reverse-projections, I need to retrieve the appropriate transformation matrices.

(modelview (gl:get-double :modelview-matrix))

(projection (gl:get-double :projection-matrix))

(viewport (gl:get-integer :viewport))

Once I have those pieces, I am just going to collect those matrices, unproject the origin, then find half of the minimum unprojected distance of the points `<1, 0, 0>`

and `<0, 1, 0>`

from the origin.

(defun calculate-cutoff (font-loader size)

(gl:with-pushed-matrix

#<:use "scale based on font-size">

(let (#<:use "collect projection matrices">)

(labels (#<:use "dist labels decl">

#<:use "dist-to-point-from-origin labels decl">)

(multiple-value-bind (ox oy oz)

(glu:un-project 0.0 0.0 0.0

:modelview modelview

:projection projection

:viewport viewport)

(/ (min (dist-to-point-from-origin 1 0 0 ox oy oz)

(dist-to-point-from-origin 0 1 0 ox oy oz))

2)))))))

Oh, and being the tricksy devil that I am, I scaled things based on my font size before doing any of that.

(let ((ss (/ size (zpb-ttf:units/em font-loader))))

(gl:scale ss ss ss)

Seeing a lot of “”s around now, it is like everything is quoted or something. For instance it says ‘”Leave a Reply”‘ instead of ‘Leave a Reply’. Don’t see what is causing it in the source though..

What browser are you using? I’m not seeing quotes around

anywhere.Oops… I had left an open <q> tag in this post. WordPress was then putting open-and-close <q&;gt tags inside almost all subtags trying to save me from myself. Oops.
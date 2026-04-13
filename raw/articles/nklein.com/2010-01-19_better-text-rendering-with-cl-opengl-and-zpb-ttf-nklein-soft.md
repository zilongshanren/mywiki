---
title: 'Better Text Rendering with CL-OpenGL and ZPB-TTF :: nklein software'
url: http://nklein.com/2010/01/better-text-rendering-with-cl-opengl-and-zpb-ttf/
author: Pat
published: '2010-01-19'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Last month, I posted [some code for rendering text](http://nklein.com/2009/12/rendering-text-with-cl-opengl-and-zpb-ttf/) under CL-OpenGL with ZPB-TTF. Toward the very end of that post, I said:

Technically, that check with the squared distance from the calculated midpoint to the segment midpoint shouldnât just compare against the number one. It should be dynamic based on the current OpenGL transformation. I should project the origin and the points and through the current OpenGL projections, then use the reciprocal of the maximum distance those projected points are from the projected origin in place of the one. Right now, I am probably rendering many vertexes inside each screen pixel.


It was pretty obvious that when you tried to render something very small, it looked quite jaggy and much more solid than you would expect.

![anti-aliasing](../../assets/caf569b4a69b59d5.png)


![anti-aliasing](http://nklein.com/wp-content/uploads/2010/01/anti-aliasing.png)

As you can see in the above image, the old version was placing up to 63 vertices for the same parabolic arc within a pixel. The new code is much more careful about this and will only place two vertices from a given parabolic arc within a pixel. You can see that in the upper rendering, the

**s**is almost totally obliterated and the tiny bits sticking down from the

**5**and

**8**are much darker than in the lower rendering.

Here is the new code:

[draw](http://nklein.com/wp-content/uploads/2010/01/draw.lisp): better anti-aliasing[gl](http://nklein.com/wp-content/uploads/2010/01/gl.lisp): smaller ‘frames-per-second’ indicator and some parameters to make it easier to toggle the main display[test](http://nklein.com/wp-content/uploads/2010/01/test.lisp): small tweak to make it work better under SLIME

### Using a better cutoff value

The squared distance

check that I mentioned now employs a cutoff value:

(let ((mx (/ (+ sx ex) 2.0))

(my (/ (+ sy ey) 2.0))

(mt (/ (+ st et) 2.0)))

(let ((nx (funcall int-x mt))

(ny (funcall int-y mt)))

(let ((dx (- mx nx))

(dy (- my ny)))

(when (< (* cutoff cutoff) (+ (* dx dx) (* dy dy)))

(interpolate sx sy nx ny int-x int-y cutoff st mt)

(gl:vertex nx ny)

(interpolate nx ny ex ey int-x int-y cutoff mt et))))))

I have tweaked the **(render-string …)** and **(render-glyph …)** accordingly to propagate that value down to the interpolate function, and I have added a method to calculate the appropriate cutoff value.

### Calculating the appropriate cutoff value

The appropriate cutoff value depends upon the font, the desired rendering size in viewport coordinates, and the current OpenGL transformations. The basic idea is that I prepare the OpenGL transformation the same way that I will later do for rendering the font; I will reverse-project ,

, and

; I will calculate the distances from the reverse-projected

to each of the other two reverse-projected points; and then I will take half of that as my cutoff value. This effectively means that once the midpoint of my parabola arc is within half of a screen pixel of where the midpoint of a line segment would be, I just use a line segment.


(gl:with-pushed-matrix

(let ((ss (/ size (zpb-ttf:units/em font-loader))))

(gl:scale ss ss ss)

(let ((modelview (gl:get-double :modelview-matrix))

(projection (gl:get-double :projection-matrix))

(viewport (gl:get-integer :viewport)))

(labels ((dist (x1 y1 z1 x2 y2 z2)

(max (abs (- x1 x2))

(abs (- y1 y2))

(abs (- z1 z2))))

(dist-to-point-from-origin (px py pz ox oy oz)

(multiple-value-bind (nx ny nz)

(glu:un-project px py pz

:modelview modelview

:projection projection

:viewport viewport)

(dist nx ny nz ox oy oz))))

(multiple-value-bind (ox oy oz)

(glu:un-project 0.0 0.0 0.0

:modelview modelview

:projection projection

:viewport viewport)

(/ (min (dist-to-point-from-origin 1 0 0 ox oy oz)

(dist-to-point-from-origin 0 1 0 ox oy oz))

2)))))))

Thanks a lot 🙂

[…] months back, I posted some code for rendering anti-aliased text in OpenGL. At the bottom of that post, I had an unwieldy 33-line function that you have to scroll to see with […]
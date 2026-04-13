---
title: 'NeHe Tutorial 04: Rotation :: nklein software'
url: http://nklein.com/2010/06/nehe-tutorial-04-rotation/
author: Pat
published: '2010-06-02'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

[Introduction](http://nklein.com#tut04-toc1)[Rotation state](http://nklein.com#tut04-toc2)[Preparing the](http://nklein.com#tut04-toc3)`tick`

function[Drawing rotated triangles and quadrilaterals](http://nklein.com#tut04-toc4)[Drawing rotated triangles and quadrilaterals (alternate version)](http://nklein.com#tut04-toc8)

In the [previous tutorial](http://nklein.com/2010/06/nehe-tutorial-03-color/), we drew a colored triangle and quadrilateral on the screen. The [next NeHe tutorial](http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=04) rotates these polygons on the screen.

This tutorial will mark my first significant departures from the original NeHe tutorials. In this NeHe tutorial, he updates the polygons’ angles inside the display function. I’m going to move those out into GLUT’s `tick`

function. The NeHe tutorial also keeps those angles in some global variables. I am going to tuck them inside my window class.

Again, we’re going to start with our simple-tutorial base.

#<:use "simple-tutorial.lisp">

Here is the resulting [tut04.lisp](http://nklein.com/wp-content/uploads/2010/06/tut04.lisp).

"tut04: rotation"

Our rotation state is just going to be two angles: one for the triangle and one for the quad. They are both going to default to zero.

(defclass rotation-state ()

((triangle-angle :initarg :triangle-angle :reader triangle-angle)

(quad-angle :initarg :quad-angle :reader quad-angle))

(:default-initargs :triangle-angle 0.0

:quad-angle 0.0))


I have opted here to make the rotation-state immutable (unless you side-step and act on the slots directly). I’m doing this largely as a personal experiment. Below, you will see that rather than update the members of the rotation state in the window, I simply replace the whole rotation state for the window. You may not wish to do this yourself, especially for something so simple as a pair of angles.

We’re also going to add the rotation state into our window class.

(rotation-state :initarg :rotation-state :accessor rotation-state)

:rotation-state (make-instance 'rotation-state)

CL-GLUT provides us with an easy mechanism to get a callback at a regular interval. First, we need to add another initarg when we create our window to tell it how often we’d like a callback. We’re going to try to stay near 60 frames per second. The tick interval is specified in milliseconds.

:tick-interval (round 1000 60) ; milliseconds per tick

Then, we need to fill in the body of the callback. In the callback, we’re going to update the rotation state and then let GLUT know we need to redraw the screen.

(defmethod glut:tick ((win my-window))

; retrieve the current rotation

(let* ((cur (rotation-state win))

; retrieve the current angles

(tri (triangle-angle cur))

(quad (quad-angle cur)))

(setf (rotation-state win) ; replace the rotation state

(make-instance 'rotation-state

:triangle-angle (+ tri 0.2)

:quad-angle (+ quad 0.15))))

(glut:post-redisplay)) ; tell GLUT to redraw

In the base code, we already cleared the color buffer and the depth buffer and reset the modelview matrix. In our previous two tutorials, we positioned the triangle, drew it, then moved from there over to where we were going to draw the quadrilateral.

Now though, we’re going to have to be more careful. We’re going to move over to where the triangle is to be drawn, rotate the coordinate system, and draw the triangle. If we then tried to translate over to where we want to draw the quadrilateral, we’d have to figure out how to do it in the rotated coordinate system. Rather than do that, we are just going to reset the transformation altogether before positioning the quad.

(let* ((cur (rotation-state win))

(triangle-angle (triangle-angle cur))

(quad-angle (quad-angle cur)))

#<:use "position triangle">

#<:use "rotate triangle">

#<:use "draw triangle">

#<:use "reset transformation">

#<:use "position quad">

#<:use "rotate quad">

#<:use "draw quad">

)

For the triangle, we’re going to slide to the left and back into the screen.

(gl:translate -1.5 0.0 -6.0) ; translate left and into the screen

Then, we’re going to rotate the coordinate system around the Y-axis.

Imagine you’re riding on your bicycle. If your front wheel were centered at the origin, it would be rotating around the X-axis.

If a revolving door is centered at the origin, it would be rotating around the Y-axis.

If your car steering wheel is centered at the origin, you rotate it around the Z-axis to turn the car.

So, to draw the triangle rotated, we’re going to rotate the coordinate system around the Y-axis.

; rotate around the y-axis

(gl:rotate triangle-angle 0.0 1.0 0.0)


The first parameter to rotate is an angle (in degrees). The remaining parameters are the axis about which to rotate.

Now, we’re just going to draw the triangle like we did in the previous tutorial.

(gl:with-primitives :triangles ; start drawing triangles

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex -1.0 -1.0 0.0) ; bottom-left vertex

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex 1.0 -1.0 0.0)) ; bottom-right vertex

To reset the transformation, we’re just going to load the identity transformation again. Below, we will show an alternate way to write this code that doesn’t involve going the whole way back to a blank slate.

(gl:load-identity)

In the previous tutorials, we translated `3.0 0.0 0.0`

to get from where the triangle was drawn to where the quadrilateral will be drawn. This time, though, we have already gone back to center. We will need to translate to the right and back into the screen.

(gl:translate 1.5 0.0 -6.0) ; translate right and into the screen

Now, we’re going to rotate the coordinate system around the x-axis.

; rotate around the x-axis

(gl:rotate quad-angle 1.0 0.0 0.0)

Then, we’ll just draw the quadrilateral exactly as we did in the previous tutorial.

(gl:color 0.5 0.5 1.0) ; set the color to light blue

(gl:with-primitives :quads ; start drawing quadrilaterals

(gl:vertex -1.0 1.0 0.0) ; top-left vertex

(gl:vertex 1.0 1.0 0.0) ; top-right vertex

(gl:vertex 1.0 -1.0 0.0) ; bottom-right vertex

(gl:vertex -1.0 -1.0 0.0)) ; bottom-left vertex

In the previous tutorial, we mentioned that the color is now set to light blue until we explicitly change it again. Similarly, the modelview matrix is set to be shifted to the right and into the screen and then rotated around the x-axis. It will be like this until we explicitly reset it. Fortunately, our template code resets the modelview matrix to the identity matrix at the very beginning of our `display`

routine.

In the previous section, we positioned, rotated, and drew the triangle. Then, we reset the modelview matrix and positioned, rotated, and drew the quadrilateral.

Sometimes, you don’t want to have to reset everything back to the the identity matrix before continuing on. For that, we can take advantage of the `with-pushed-matrix`

macro provided by CL-OpenGL.

OpenGL maintains a (finite) stack on which you can push the modelview matrix (and a smaller stack on which you can push the projection matrix). In C, you have to explicitly push and pop the matrix:

glPushMatrix();

// do something here

glPopMatrix();


With CL-OpenGL, you can take advantage of the `with-`

pattern to avoid having to remember to keep your pushes and pops paired up. The `with-pushed-matrix`

effectively remembers the current transformation and restores it at the end of the form.

(let* ((cur (rotation-state win))

(triangle-angle (triangle-angle cur))

(quad-angle (quad-angle cur)))

#<:use "position triangle">

(gl:with-pushed-matrix

#<:use "rotate triangle">

#<:use "draw triangle">

)

#<:use "position quad (original) .lisp">

(gl:with-pushed-matrix

#<:use "rotate quad">

#<:use "draw quad">

)

)

Here, we can go back to the original positioning for the quadrilateral because at the time we’re going to move, we’re back to using the original matrix from where we positioned the triangle. We don’t have to move back into the screen, but we have to move twice as far to the right.

(gl:translate 3.0 0.0 0.0) ; translate right


Everything else is the same as in the previous section.

[…] the previous tutorial, we drew a rotating triangle and a rotating square on the screen. The next NeHe tutorial fleshes […]
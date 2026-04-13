---
title: 'NeHe Tutorial 02: Drawing Triangles and Quadrilaterals :: nklein software'
url: http://nklein.com/2010/06/nehe-tutorial-02-drawing-triangles-and-quadrilaterals/
author: Pat
published: '2010-06-01'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In the [previous tutorial](http://nklein.com/2010/06/nehe-tutorials-for-cl-opengl/), we made a basic shell of a CL-OpenGL application. I have slightly modified it for this tutorial so that it has some hooks where we can add in code specific to this tutorial.

In this tutorial, we’re going to draw a triangle and a quadrilateral in our window. We’re going to start with our simple-tutorial base.

#<:use "simple-tutorial.lisp">

Here is the whole [tut02.lisp](http://nklein.com/wp-content/uploads/2010/06/tut02.lisp).

"tut02: triangles and quads"

In the base display code, we already cleared the color buffer and the depth buffer and reset the modelview matrix. Now, we’re going to translate the modelview matrix so that when we draw our triangle, it is going to be in front of our viewpoint and off to our left. Then, we’ll draw the triangle, translate over toward the right, and draw the quadrilateral.

(gl:translate -1.5 0.0 -6.0) ; translate left and into the screen

#<:use "draw triangle">

(gl:translate 3.0 0.0 0.0) ; translate right

#<:use "draw quadrilateral">


The parameters to `gl:translate`

are x, y, and z (respectively). After the `gl:load-identity`

, the modelview matrix is centered at the origin with the positive x axis pointing to the right of your screen, the positive y axis pointing up your screen, and the positive z-axis pointing out of your screen.

With the way that we set up the projection matrix in the `reshape`

method, the origin of the modelview space should be dead-center in our window.

Now that we’ve moved over to the side a little bit and back a ways, we’re going to draw a triangle. The CL-OpenGL code looks like this:

(gl:with-primitives :triangles ; start drawing triangles

(gl:vertex 0.0 1.0 0.0) ; top vertex

(gl:vertex -1.0 -1.0 0.0) ; bottom-left vertex

(gl:vertex 1.0 -1.0 0.0)) ; bottom-right vertex


The `with-primitives`

form lets OpenGL know how to use the vertexes we’re going to make. In this case, it’s going to make a triangle out of each set of three vertexes. If we had six vertexes there, we’d end up with two triangles.

Here, we drew the vertexes in clockwise order. By default, OpenGL considers this triangle to be facing away from us, then. With our current OpenGL settings, this does not make a difference since OpenGL will draw both front and back faces.

Each call to `vertex`

gives the x, y, and z (respectively) coordinates in the modelview projection for the vertex. You will note that I used floating-point numbers here. I could have easily written them as integers like `(gl:vertex 1 -1 0)`

. CL-OpenGL would convert them to floating point numbers for me on the fly. I tend to use floating point constants when possible to try to save it the extra work. I should check, sometime, to be sure though that I don’t pay a boxing/unboxing penalty that negates the benefit.

Drawing quadrilaterals is much like drawing triangles. Here, of course, we need four vertexes.

(gl:with-primitives :quads ; start drawing quadrilaterals

(gl:vertex -1.0 1.0 0.0) ; top-left vertex

(gl:vertex 1.0 1.0 0.0) ; top-right vertex

(gl:vertex 1.0 -1.0 0.0) ; bottom-right vertex

(gl:vertex -1.0 -1.0 0.0)) ; bottom-left vertex


In this case, we drew a square. We could draw any convex quadrilateral.

Again, we drew the vertexes in clockwise order. By default, OpenGL considers this triangle to be facing away from us, then. With our current OpenGL settings, this does not make a difference since OpenGL will draw both front and back faces.

We’re also going to add a slot that keeps track of whether or not our window is full screen.

(fullscreen :initarg :fullscreen :reader fullscreen-p)

:fullscreen nil

Then, before we display our window, we’re going to switch to fullscreen mode if this is true.

(when (fullscreen-p win) ; check to see if fullscreen needed

(glut:full-screen)) ; if so, then tell GLUT

Here, we add an extra case to the keypress handler. We destroy our window and create a new one with the fullscreen property toggled if we get an `'f'`

on the keyboard.

((#\f #\F) ; when we get an 'f'

; save whether we're in fullscreen

(let ((full (fullscreen-p win)))

(glut:close win) ; close the current window

(glut:display-window ; open a new window with fullscreen toggled

(make-instance 'my-window

:fullscreen (not full)))))

[…] the previous tutorial, we drew a plain triangle and quadrilateral on the screen. The next NeHe tutorial colors this […]

I have a question about this tutorial. In your source you have a function “keyboard”. Here is it:

(declare (ignore xx yy))

(case key

((#\q #\Q #\Escape) (glut:destroy-current-window))

((#\f #\F) ; when we get an 'f'

; save whether we're in fullscreen

(let ((full (fullscreen-p win)))

(glut:close win) ; close the current window

(glut:display-window ; open a new window with fullscreen toggled

(make-instance 'my-window

:fullscreen (not full)))))

))

But when I launch it, I had an error, that “win” is unbound. How can I fix it?

(Yeah, I can change (glut:close win) to (glut:destroy-current-window))

The method declaration in my file is:

The

`(win my-window)`

means that this method parameter is going to be called`win`

and this is the version of the method for when this parameter is of type`my-window`

. In the bit you pasted, you renamed`win`

to`window`

in the declaration.
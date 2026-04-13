---
title: 'NeHe Tutorial 05: Solids :: nklein software'
url: http://nklein.com/2010/06/nehe-tutorial-05-solids/
author: Pat
published: '2010-06-02'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In the [previous tutorial](http://nklein.com/2010/06/nehe-tutorial-04-rotation/), we drew a rotating triangle and a rotating square on the screen. The [next NeHe tutorial](http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=05) fleshes out these polygons into solid shapes: a (square-bottomed) pyramid and a cube.

Again, we’re going to start with our simple-tutorial base.

#<:use "simple-tutorial.lisp">

Here is the resulting [tut05.lisp](http://nklein.com/wp-content/uploads/2010/06/tut05.lisp).

"tut05: solid shapes"

This tutorial is almost identical to the previous one. For variety, I am going to use what I called the alternate version

of managing the modelview matrix in the previous tutorial.

Again, our rotation state is just going to be two angles: one for the pyramid and one for the cube. They are both going to default to zero.

(defclass rotation-state ()

((pyramid-angle :initarg :pyramid-angle :reader pyramid-angle)

(cube-angle :initarg :cube-angle :reader cube-angle))

(:default-initargs :pyramid-angle 0.0

:cube-angle 0.0))

We’re also going to add the rotation state into our window class.

(rotation-state :initarg :rotation-state :accessor rotation-state)


And, make sure we initialize our rotation state.

:rotation-state (make-instance 'rotation-state)

Again, we’re going to try to stay near 60 frames per second.

:tick-interval (round 1000 60) ; milliseconds per tick

And, our tick method is unchanged from the previous tutorial except that we now have a pyramid and cube instead of a triangle and quad.

(defmethod glut:tick ((win my-window))

; retrieve the current rotation

(let* ((cur (rotation-state win))

; retrieve the current angles

(pyramid (pyramid-angle cur))

(cube (cube-angle cur)))

(setf (rotation-state win) ; replace the rotation state

(make-instance 'rotation-state

:pyramid-angle (+ pyramid 0.2)

:cube-angle (+ cube 0.15))))

(glut:post-redisplay)) ; tell GLUT to redraw

In the base code, we already cleared the color buffer and the depth buffer and reset the modelview matrix. Now, we’re going to retrieve our rotations, position our pyramid, save our modelview matrix, rotate for it, draw it, and restore our saved modelview matrix. Then, we’re going to position our cube, save our modelview matrix, rotate for it, draw it, and restore our saved modelview matrix.

(let* ((cur (rotation-state win))

(pyramid-angle (pyramid-angle cur))

(cube-angle (cube-angle cur)))

#<:use "position pyramid">

(gl:with-pushed-matrix

#<:use "rotate pyramid">

#<:use "draw pyramid">

)

#<:use "position cube">

(gl:with-pushed-matrix

#<:use "rotate cube">

#<:use "draw cube">

)

)

For the pyramid, we’re going to slide to the left and back into the screen.

(gl:translate -1.5 0.0 -6.0) ; translate left and into the screen

Then, we’re going to rotate the coordinate system around the Y-axis.

; rotate around the y-axis

(gl:rotate pyramid-angle 0.0 1.0 0.0)


Again, the first parameter to rotate is an angle (in degrees). The remaining parameters are the axis about which to rotate.

Now, we’re going to draw the pyramid. We’re going to draw each of the four triangles that make up the pyramid. We’re going to keep each vertexes colored the same way regardless of which face the vertex is being drawn on at the moment.

(gl:with-primitives :triangles ; start drawing triangles

#<:use "draw pyramid faces">

)

The front face is going to be just about the same as our triangle from the previous tutorials. We’re just going to kick the bottom forward a bit.

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex (front)

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex -1.0 -1.0 1.0) ; bottom-left vertex (front)

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex 1.0 -1.0 1.0) ; bottom-right vertex (front)

The right face is going to share two vertexes with our front face and introduce a third.

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex (right)

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex 1.0 -1.0 1.0) ; bottom-left vertex (right)

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex 1.0 -1.0 -1.0) ; bottom-left vertex (right)

The back face is going to share two points with the right face and one point with the front face.

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex (back)

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex 1.0 -1.0 -1.0) ; bottom-left vertex (back)

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex -1.0 -1.0 -1.0) ; bottom-left vertex (back)

The left face is going to share two points with the back face and two points with the front face (and, of course, the apex with the right face).

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex (left)

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex -1.0 -1.0 -1.0) ; bottom-left vertex (left)

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex -1.0 -1.0 1.0) ; bottom-left vertex (left)

This completes the four sides of our pyramid. The NeHe tutorial doesn’t bother drawing a bottom for the pyramid. It won’t ever be seen with the way the rest of this code is organized, but I am going to include it here for completeness.

(gl:with-primitives :quads

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex 1.0 -1.0 1.0) ; front-right corner

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex 1.0 -1.0 -1.0) ; back-right corner

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex -1.0 -1.0 -1.0) ; back-left corner

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex -1.0 -1.0 1.0)) ; front-left corner

At the point we need to position the cube, we’re sitting at the point where the triangle was drawn. So, we need to slide to the right before drawing the cube.

(gl:translate 3.0 0.0 0.0) ; translate right

Now, we’re going to rotate the coordinate system around the x-axis.

; rotate around the x-axis

(gl:rotate cube-angle 1.0 0.0 0.0)

Now, we’re going to draw the cube with each face a different color.

(gl:with-primitives :quads ; start drawing quadrilaterals

#<:use "draw cube faces">

)

The top face is going to be green. We are taking care here to draw the vertexes in counter-clockwise order when viewed from above the cube.

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex 1.0 1.0 -1.0) ; right top back

(gl:vertex -1.0 1.0 -1.0) ; left top back

(gl:vertex -1.0 1.0 1.0) ; left top front

(gl:vertex 1.0 1.0 1.0) ; right top front

The bottom face is going to be orange. We are still taking care to draw the vertexes in counter-clockwise order when looking at this face from outside the cube. For the bottom face, that would be looking at the cube from below. For consistency, should we later want to texture map the cube, we’re going to start working from the front of the cube this time instead of the back as if we just flipped the cube 180 degrees forward and are now looking at the bottom.

(gl:color 1.0 0.5 0.0) ; set the color to orange

(gl:vertex 1.0 -1.0 1.0) ; right bottom front

(gl:vertex -1.0 -1.0 1.0) ; left bottom front

(gl:vertex -1.0 -1.0 -1.0) ; left bottom back

(gl:vertex 1.0 -1.0 -1.0) ; right bottom back

Next, we’re going to draw the front face. We are going to make it red. Again, we’re going to keep our vertexes counter clockwise and we’re going to start with the one that’s in the upper right when we’re looking at the face.

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 1.0 1.0 1.0) ; right top front

(gl:vertex -1.0 1.0 1.0) ; left top front

(gl:vertex -1.0 -1.0 1.0) ; left bottom front

(gl:vertex 1.0 -1.0 1.0) ; right bottom front

Next, we’re going to draw the back face. We are going to make it yellow. Again, we’re going to keep our vertexes counter clockwise and we’re going to start with the one that’s in the upper right when we’re looking at the face (as if we’ve rotated the cube forward 180 degrees so that what was back is now front).

(gl:color 1.0 1.0 0.0) ; set the color to yellow

(gl:vertex 1.0 -1.0 -1.0) ; right bottom back

(gl:vertex -1.0 -1.0 -1.0) ; left bottom back

(gl:vertex -1.0 1.0 -1.0) ; left top back

(gl:vertex 1.0 1.0 -1.0) ; right top back

We’re going to draw the left side in blue.

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex -1.0 1.0 1.0) ; left top front

(gl:vertex -1.0 1.0 -1.0) ; left top back

(gl:vertex -1.0 -1.0 -1.0) ; left bottom back

(gl:vertex -1.0 -1.0 1.0) ; left bottom front

For this tutorial, we’re never going to see the right side of the cube, but we’re going to draw it anyway for completeness. It will be magenta.

(gl:color 1.0 0.0 1.0) ; set the color to magenta

(gl:vertex 1.0 1.0 -1.0) ; right top back

(gl:vertex 1.0 1.0 1.0) ; right top front

(gl:vertex 1.0 -1.0 1.0) ; right bottom front

(gl:vertex 1.0 -1.0 -1.0) ; right bottom back

And, now we have a cube.

In all of the above examples, we have only used `vertex`

inside a `with-primitives`

call. There is good reason for this. We cannot just make a vertex whenever we want. It has to be a part of a shape. The `with-primitives`

call starts building a shape (so far, we’ve only used triangles or quads) and then ends the shape at the end of the form. In C, we would need to do something like this to explicitly begin and end the shape.

glBegin(GL_TRIANGLES);

glVertex3f( 0.0, 1.0, 0.0 );

glVertex3f( -1.0, -1.0, 0.0 );

glVertex3f( 1.0, -1.0, 0.0 );

glEnd();

If you try to make a vertex that isn’t part of a shape, things get corrupted. In C, you can probably still limp along and never notice. Unless you explicitly check the OpenGL error state on a regular basis, you’ll never notice that OpenGL is screaming quietly to itself.

CL-OpenGL checks the OpenGL error state for us though. It notices right away that something has gone wrong if we try to make a vertex outside of a `with-primitives`

call.

[…] the previous tutorial, we drew a rotating pyramid and a rotating cube. The next NeHe tutorial renders a textured cube […]
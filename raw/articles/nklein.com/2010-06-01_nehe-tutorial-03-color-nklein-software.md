---
title: 'NeHe Tutorial 03: Color :: nklein software'
url: http://nklein.com/2010/06/nehe-tutorial-03-color/
author: Pat
published: '2010-06-01'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In the [previous tutorial](http://nklein.com/2010/06/nehe-tutorial-02-drawing-triangles-and-quadrilaterals/), we drew a plain triangle and quadrilateral on the screen. The [next NeHe tutorial](http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=03) colors this triangle and quadrilateral.

We’re going to start with our simple-tutorial base.

#<:use "simple-tutorial.lisp">

"tut03: color"

In the base display code, we already cleared the color buffer and the depth buffer and reset the modelview matrix. Now, we’re going to translate the modelview matrix so that when we draw our triangle, it is going to be in front of our viewpoint and off to our left. Then, we’ll draw the triangle, translate over toward the right, and draw the quadrilateral.

(gl:translate -1.5 0.0 -6.0) ; translate left and into the screen

#<:use "draw triangle">

(gl:translate 3.0 0.0 0.0) ; translate right

#<:use "draw quadrilateral">


The above is untouched from the previous tutorial.

Now that we’ve moved over to the side a little bit and back a ways, we’re going to draw a triangle. We open with the `with-primitives`

call and then specify the vertexes.

(gl:with-primitives :triangles ; start drawing triangles

#<:use "draw triangle vertexes">

)

Before, we simply listed the vertexes. Here, we are going to specify a color before each vertex.

(gl:color 1.0 0.0 0.0) ; set the color to red

(gl:vertex 0.0 1.0 0.0) ; top vertex


The arguments to `color`

are the red, green, and blue values (respectively). The values range from zero (for the darkest) to one (for the brightest). I have omitted here the optional fourth argument for the alpha channel. It defaults to `1.0`

.

It is important to note that we have set the global color to red. This vertex will be red because the global color was red at the time we created the vertex. If we failed to ever set the color again, everything would be red.

Here, however, we’re going to make the next vertex green.

(gl:color 0.0 1.0 0.0) ; set the color to green

(gl:vertex -1.0 -1.0 0.0) ; bottom-left vertex

We are going to make the final vertex blue for this triangle.

(gl:color 0.0 0.0 1.0) ; set the color to blue

(gl:vertex 1.0 -1.0 0.0) ; bottom-right vertex

Note: the global color is now blue. We could leave it blue and it would be blue until we set it to some other color.

Drawing quadrilaterals is much like drawing triangles. Here, of course, we need four vertexes. In this case, however, we’re going to color the whole quadrilateral the same color. So, we are just going to set the global color to a light blue and then draw the quadrilateral exactly as we did in the previous tutorial.

(gl:color 0.5 0.5 1.0) ; set the color to light blue

(gl:with-primitives :quads ; start drawing quadrilaterals

(gl:vertex -1.0 1.0 0.0) ; top-left vertex

(gl:vertex 1.0 1.0 0.0) ; top-right vertex

(gl:vertex 1.0 -1.0 0.0) ; bottom-right vertex

(gl:vertex -1.0 -1.0 0.0)) ; bottom-left vertex

Now, the color is still this light blue. It will remain so until we reset the color to red when drawing the triangle during the next time our screen is redrawn.

[…] the previous tutorial, we drew a colored triangle and quadrilateral on the screen. The next NeHe tutorial rotates these […]
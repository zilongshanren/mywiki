---
title: Processing little tricks - bleuje
url: https://bleuje.com/processing-tricks/
published: '2025-01-01'
source_blog: bleuje
source_site: https://bleuje.com/
category: graphics
fetched: '2026-04-19'
---

Processing techniques I wish I used earlier.

## push() and pop()

At the very beginning of drawing with Processing I didn’t use them and wanted to describe positions with longer formulas and more maths. I didn’t realize how useful and worth getting used to they were. I don’t want to explain how to use push() and pop() here, a lot of people must have explained it way better than I would be able to do. In a lot of cases it feels like it’s the only way to code things simply. As far as I know, it’s also the only way to use the sphere function, because it doesn’t have position as parameters (it draws it at current (0,0,0)).

## sphereDetail

Useful to make the sphere function draw lower quality spheres, it helps to draw a lot of small spheres much faster. See [description in documentation](https://processing.org/reference/sphereDetail_.html).

## PVector’s copy() function

Let’s say you have two PVectors v1 and v2 and that you want to get their sum v3. Doing PVector v3 = v1.add(v2) works, except that it modifies v1 (and makes it equal to the sum). It happened many times to me that debugging wasn’t easy because of this v1 being reused later. This problem can be solved by writting PVector v3 = v1.copy().add(v2);

## Resolution change using scale function

If you want to change the resolution of your sketch, it’s natural to use the scale to make the drawing larger according to the ratio of change of canvas size. So if for example you change the canvas size from 600 x 600 to 800 x 800, you can use scale(800.0/600) at the beginning of the draw() functions. However there’s a problem if you use the width and height global variables in your drawing: these change with the new canvas size and it’s a problem because the scale function already does the job of changing the size of the drawing. If you used them you can store 600 in some variables W and H, and then replace width and height by W and H. Then scale will do well its job.

## modelZ (and modelX, modelY)

Let’s say you used matrix transforms (translate and rotate functions). Your current (0,0,0) position is at some (x,y,z), when you ignore the transforms. modelZ(0,0,0) gives that z. Let’s call that (x,y,z) that ignores the transforms the “real position”. Then modelZ(X,Y,Z) is the real z position of your current (X,Y,Z). This can be very useful to map that z depth information to color, for example to have darker color in the distance (it can often help seeing 3D shapes clearly). modelX and modelY are the same, giving the “real” x and y positions. I saw this function in some beesandbombs code on day. [See modelZ in Processing documentation](https://processing.org/reference/modelZ_.html)
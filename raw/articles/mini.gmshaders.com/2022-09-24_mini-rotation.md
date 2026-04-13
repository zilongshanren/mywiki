---
title: 'Mini: Rotation'
url: https://mini.gmshaders.com/p/gm-shaders-mini-rotation-1364623
author: Xor
published: '2022-09-24'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Rotation

### How to rotate a vector

Hi,

Today, we're gonna go over rotation and matrices. This tutorial should be easier to digest than code-golfing or raymarching. Let's dig in!

## Rotating a Point

Suppose we have a horizontal line and we want to rotate it by some angle.

A diagram would help, so I wrote a shader to illustrate:

Here you can see the line segment, starting at the red point "A" and ending at the blue point "B". Since we're starting with a horizontal line (at 0 degrees), calculating a new endpoint is quite simple.

If you remember trigonometry, you'll probably know what to do here. We use cosine for the x-coordinate and sine for the y-coordinate, and multiply by our line length:

`vec2 B = A + vec2(cos(angle), -sin(angle)) * line_length;`



The cosine (bottom) and sine (right) are illustrated by the perpendicular lines connecting the red and blue dots.

**Note:** `cos()`

and `sin()`

use radians that range from 0 to 2*pi instead of degrees (0 - 360). If you want to work with degrees, just use the `radians(degrees)`

function to convert an angle to radians first.

Okay, so this is a simple rotation where we know point B starts at 0 degrees from point A. Let's try rotating points at any angle

## 2D Rotation

Let's think like a mathematician! We know how to rotate a horizontal line, so can we use that insight for vertical lines? Here's a diagram:

Here you can see that when we rotate a horizontal (red to blue line) and vertical line (red to green), the x and y offsets for the blue point seem to match the y and x offsets for the green point. This isn't a coincidence and is true for any angle that we might pick. So if we're calculating the green point's coordinates, we just swap the sine and cosine:

`vec2 C = A + vec2(sin(angle), cos(angle)) * line_length;`



Notice that with point "C" both x and y coordinates are positive (right and down), whereas with point "B" x is positive (right), but y is negative (upward).

Now that we have a way of rotating horizontal and vertical lines, do you have any guesses on rotating diagonal lines?

## Matrices

Well, it's as simple as doing a horizontal rotation for the x-coordinate and a vertical rotation for the y-coordinate!

So, suppose we had a fourth point that completes the square, it would be computed like so:

`vec2 D = A + vec2(cos(angle)+sin(angle), cos(angle)-sin(angle)) * line_length;`



That's it!

We can clean things up by using a 2D matrix:

`mat2 rotation = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));`



So if we want to rotate a point at vec2(2, 3), we can do:

`vec2 E = rotation * vec2(2.0, 3.0);`



Which is an easy way of writing:

```
E.x = 2.0 * cos(angle) - 3.0 * sin(angle);
E.y = 2.0 * sin(angle) +3.0 * cos(angle);
```



**Note:** Doing vec2 * mat2 is not the same as mat2 * vec2! This will rotate clockwise instead of counter-clockwise, so make sure you're intentional. Here's a brief explanation of why: Matrices are organized in rows and columns, so swapping the order will swap the columns and rows, and in our case: `-sin(angle)`

and `sin(angle)`


## 3D Rotation

You may be wondering about rotation on 3D or higher-dimensional points.

What if you want to rotate a camera or a 3D object?

Thankfully, there's an easy rule that works with any number of dimensions! Just rotate 2 axes at a time. Here's an example of a 3D vector:

```
vec3 P = vec3(1,2,3);
P.xy *= rotation1; //Rotating about the z-axis
P.xz *= rotation2; //Rotating about the y-axis
```



That seems like enough for today.

## Conclusion

Rotation coordinates are an interesting process that can be broken down into simple processes for each axis and then applied using matrices. It's quite helpful to understand how these matrices work before approaching 3D camera math.

[Here's a ShaderToy demo](https://www.shadertoy.com/view/ftyfzh) that shows rotation in action.

If you found this helpful, [please consider buying me a donut](https://ko-fi.com/xor)! It helps me continue to write tutorials like these, and I share some cool code examples with my supporters. Thanks!
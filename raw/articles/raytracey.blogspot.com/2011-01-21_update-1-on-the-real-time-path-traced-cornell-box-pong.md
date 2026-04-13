---
title: Update 1 on the real-time path traced Cornell Box Pong
url: http://raytracey.blogspot.com/2011/01/update-1-on-real-time-path-traced.html
author: Sam Lapere
published: '2011-01-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

First update on my real-time path traced game project!!! :D

Here's a screenshot of the scene:




Everything you see in the picture is either a sphere or a part of a (very large) sphere. Ceiling, floor, side walls and back wall are in fact huge intersecting spheres, giving the impression of planes. The circular light source in the ceiling is also a part of a light emitting sphere protruding through the ceiling. The Pong bats are also parts of spheres protruding through the side walls. I included some diffuse spheres to show off the color bleeding and the obligatory reflective sphere as well.


I ran into trouble making the Pong bats as described in my previous post, so I decided to make the bats by using just one sphere per bat instead of two. The sketch below shows how it’s done:




In order to make the path traced image converge as fast as possible (in under 100 milliseconds to allow for some playability), I made the lightsource in the ceiling bigger. I think you should be able to get 30 fps in this scene on a GTX 580 and with 64 samples per pixel per frame at the default resolution. (If you have one of these cards or another Fermi-based card, please leave a comment with your performance statistics, press "p" in tokaspt to see the fps counter and change the spppp)


The above Pong scene can be downloaded here:


On to the gameplay, which still needs to be implemented. The gameplay mechanics are extremely simple: all the movement of the spheres happens in 2D, just like in the original Pong game: the ball is moving in a vertical plane between the Pong bats and the bats can only move up or down. Only 3 points need to be changed per frame: the centers of the 2 spheres making up the bats (only up and down) and the center of the blue ball. The blue ball bounces off the ceiling and the floor in the direction of the side walls. If the player or the computer fails to bounce the ball back with the bats and the ball hits the red sphere (red wall) or the green sphere (green wall) the game is lost for that player and another game begins. Since everything is happening in 2D this is just a matter of simple collision detection calculation between two circles. There are plenty of 2D Pong games on the net with open source code (single player and multi-player), so I only have to copy one of those and change the tokaspt source. Should be a piece of cake, except that I haven't done anything like this before :)


Here's a screenshot of the scene:

![](../../assets/79196a3d53c4621d.png)

![](../../assets/79196a3d53c4621d.png)

Everything you see in the picture is either a sphere or a part of a (very large) sphere. Ceiling, floor, side walls and back wall are in fact huge intersecting spheres, giving the impression of planes. The circular light source in the ceiling is also a part of a light emitting sphere protruding through the ceiling. The Pong bats are also parts of spheres protruding through the side walls. I included some diffuse spheres to show off the color bleeding and the obligatory reflective sphere as well.

I ran into trouble making the Pong bats as described in my previous post, so I decided to make the bats by using just one sphere per bat instead of two. The sketch below shows how it’s done:

![](../../assets/c8f18cfefe5ddd66.jpg)

![](../../assets/c8f18cfefe5ddd66.jpg)

In order to make the path traced image converge as fast as possible (in under 100 milliseconds to allow for some playability), I made the lightsource in the ceiling bigger. I think you should be able to get 30 fps in this scene on a GTX 580 and with 64 samples per pixel per frame at the default resolution. (If you have one of these cards or another Fermi-based card, please leave a comment with your performance statistics, press "p" in tokaspt to see the fps counter and change the spppp)

The above Pong scene can be downloaded here:

[http://www.2shared.com/file/PqfY-sBV/pongscene.html](http://www.2shared.com/file/PqfY-sBV/pongscene.html)Place the file in the tokaspt folder and open it from within tokaspt by pressing F9. You also need[tokaspt](http://code.google.com/p/tokaspt/)and a CUDA enabled GPU.On to the gameplay, which still needs to be implemented. The gameplay mechanics are extremely simple: all the movement of the spheres happens in 2D, just like in the original Pong game: the ball is moving in a vertical plane between the Pong bats and the bats can only move up or down. Only 3 points need to be changed per frame: the centers of the 2 spheres making up the bats (only up and down) and the center of the blue ball. The blue ball bounces off the ceiling and the floor in the direction of the side walls. If the player or the computer fails to bounce the ball back with the bats and the ball hits the red sphere (red wall) or the green sphere (green wall) the game is lost for that player and another game begins. Since everything is happening in 2D this is just a matter of simple collision detection calculation between two circles. There are plenty of 2D Pong games on the net with open source code (single player and multi-player), so I only have to copy one of those and change the tokaspt source. Should be a piece of cake, except that I haven't done anything like this before :)

## 6 comments:

If it were me I'd hack out the gl_scene method for loading the scene file, and get it to setup the main game loop. i.e. to update the sphere positions.


I'll be interested to see how this pans out

A quick question: would it not be easier to simply use axis-aligned bounding boxes instead of spheres? They aren't as pretty with regards to lighting, but they're fast and will if nothing else give you proper paddles to work with.


(Also, in the old Pong, everything was a square, even the ball; so it seems appropriate to follow the convention!)

Kerrash, thanks for the tip! I'll see what I can do.


Jason, it would indeed be simpler to use axis aligned boxes to represent the paddles, the thing is that tokaspt only supports spheres as primitives, not triangles. This is because ray-sphere intersections are very cheap to compute, much cheaper than ray-triangle intersections. Collision detection between spheres (or circles in 2D) is also quite straightforward. To be honest, I'm quite happy with the results so far, the convex paddles are quite original imo.

No, I don't mean triangle: I mean directly intersecting axis-aligned boxes! The code is simple, looking something like this: http://ompf.org/ray/ray_box.html


Modifying the code to give you the normal is pretty close to trivial, as well. (I've written some toys that do so, e.g. http://lonelypinkelephants.com/random/pt.html, if you're looking for a code sample.)

Thanks for the link! I think I will stick with the default spheres for now, but I could add the axis aligned boxes later on when I have familiarized myself a bit with CUDA.

Post a Comment
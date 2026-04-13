---
title: 'Update 6 Cornell Box Pong: first physics test'
url: http://raytracey.blogspot.com/2011/02/update-6-cornell-box-pong-first-physics.html
author: Sam Lapere
published: '2011-02-03'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've recreated and programmed the scene from Cornell Box Pong in

[Box2D](http://www.box2d.org/), an awesome open-source 2D physics engine. I've made a video of the whole process:[youtube Cornell Box Pong physics test](http://www.youtube.com/watch?v=HzU0wVOFWHI)(fraps heavily reduces the framerate of the physics simulation)

![](../../assets/cd7070deda98399c.png)


![](../../assets/cd7070deda98399c.png)

The size and position of the the 3D spheres in tokaspt's Cornell Box Pong scene are exactly replicated in the Box2D scene. The walls are curved, because they are part of huge intersecting spheres and the lightsource is a huge light emitting sphere which peeks through the sphere representing the ceiling, as shown at the end of the video. The right paddle is currently just bouncing up and down, but it will be controlled later on by some basic AI routine. The left paddle is user controlled with mouse or keys. The Pong ball has mass, friction and restitution characteristics. Unlike the original Pong game, which uses a top down view, Cornell Box Pong uses a side view and the Pong ball in this game is subjected to gravitational forces as it bounces around in the Cornell Box.

The physics engine outputs the continuously changing x and y coordinates of the Pong ball and the paddles which can be fed to the real-time path traced CBP scene running inside tokaspt. It also tells if a collision between the Pong ball and one of the side walls has occurred, which means the game ends and another begins.

## 2 comments:

Looks great ! is the scene really as "curved" as what is visible in the simulation ?

Yes it is. Sphere positions and radii in 2D and 3D are exactly the same.


I'm still tweaking the Pong ball physics, so this is not going to be the final thing.

Post a Comment
---
title: 'Unbiased Truck Soccer: First physics test with Bullet Physics'
url: http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-first-physics.html
author: Sam Lapere
published: '2011-03-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**UPDATE: I've uploaded the executables for the Bullet physics test and the new scene with the soccer playing field at**

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)I've recreated the truck from 'Unbiased Truck Soccer' in the Bullet Physics engine and applied some physical properties to make it behave like a real vehicle like suspension stiffness, damping, rolling and friction.

![](../../assets/c855ccf00ebcca1c.jpg)


![](../../assets/c855ccf00ebcca1c.jpg)

This is a video of what the gameplay should be like when using the Bullet Physics engine, made with the built-in debug OpenGL renderer of Bullet:

And a Soccer game is not complete without a huge open playing field. The goals will be represented by a blue and a red sphere. Players can score by bumping the soccer ball against the opponent's sphere.

[The hardest part is using the output of the Bullet Physics engine to update the position of the trucks and the soccer ball in the real-time path tracer. It should be fairly straightforward though, so I hope to have a working version soon!](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEguGIMvkI8OiXHf_-FjWfZG-_0Le4IE1XJdRb4QryKODMSt4IkzMzDSrLA-aBLv9t2qcjVxvSPfVbfvC33aujI2Kw6cEsCv9Us6GuyKgQSYxdwLADTVXRGo8zgPxXc6bZDl_Jls2wp4RyM/s1600/tokap+uts1.jpg)

![](../../assets/c7bd91426d572fd5.jpg)


![](../../assets/c7bd91426d572fd5.jpg)

![](../../assets/bf5f17bf915e8b3d.jpg)


![](../../assets/bf5f17bf915e8b3d.jpg)

## 2 comments:

Hello, it's radiant again.




I would love to take another in this program.

Unfortunately my computer is in maintenance at the moment. So I will check back within a week.

It's good to see this program evolve.

A few questions.

//Where is the source for this program

//What free compiler should be used

//And to code such a dynamic program what math skills do you need.iv gotten Cs and Ds in math, yet have a 90% understanding on the mathematical theory of path tracing then all of my math teachers here.

Hi radiant! It would be awesome if you could make another video with that GTX580 of yours! :D





Source code for this 'game' can be found at http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list. If you want I can upload the source file for the physics (coded with bullet physics library) as well, so you can mess around with it and try different settings.

The compiler I use is Visual C++ 2008 Express Edition, which is free and can be downloaded from http://msdn.microsoft.com/en-us/express/future/bb421473. You will also need the CUDA SDK.

Most of the code (>95%) in 'Tokap' is not written by myself, I used an open-source CUDA path tracer (tokaspt from http://code.google.com/p/tokaspt/). Kerrash has added support for dynamic objects, and I've built a game scene out of spheres. If you want to code a similar program yourself, I suggest you take a look at the free online courses on learning to program (I have recently started learning to program as well to be able to add functionality to Tokap). If you just want to make games with it, you can take a look at the source code and modify a few a parameters, write a simple time dependent function (e.g. use the parameter 'ball_y' in the file 'gl_scene.cc') to dynamically change the radius, position or color of the spheres, or change the simulation speed by changing the value of the parameter 'ball_vy' on line 368 in gl_scene.cc, recompile to see the result.

A C or D in math will suffice ;)

Post a Comment
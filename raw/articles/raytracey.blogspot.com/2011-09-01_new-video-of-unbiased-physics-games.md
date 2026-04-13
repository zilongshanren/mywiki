---
title: New video of Unbiased Physics Games
url: http://raytracey.blogspot.com/2011/09/new-video-of-unbiased-physics-games.html
author: Sam Lapere
published: '2011-09-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Thursday, September 1, 2011

New video of Unbiased Physics Games

Changed the ground color and brightened up the sky in preparation for an upcoming demo called "Unbiased Stunt Racer" (courtesy of Anonymous blog reader :). It looks a little bit more realistic now (480p video on GTS 450):

The video looks great! to bad the wheels go through the ground a couple of times, is the only glitch I can see. What about a sky/sun system to really get the realism going :D

Thanks. The wheels going through the ground is a glitch in the Bullet physics simulation, which performs collision detection between the wheels and other objects through ray casting. The faster the vehicle, the greater the chance for interpenetrating objects. I could increase the physics simulation accuracy by increasing the number of iterations per frame, but it's quite taxing on performance, so I'll leave it like that.

About the sky/sun: there is a light emitting sphere and explicit shadow rays are traced. A real physically correct sky/sun system (like Preetham sky) is something I will look into in the future. I have modified some things in the sampling (removed the stratified sampling) to improve realism at the cost of noise, which you will see in my next demo.

## 2 comments:

The video looks great! to bad the wheels go through the ground a couple of times, is the only glitch I can see. What about a sky/sun system to really get the realism going :D

Thanks. The wheels going through the ground is a glitch in the Bullet physics simulation, which performs collision detection between the wheels and other objects through ray casting. The faster the vehicle, the greater the chance for interpenetrating objects. I could increase the physics simulation accuracy by increasing the number of iterations per frame, but it's quite taxing on performance, so I'll leave it like that.


About the sky/sun: there is a light emitting sphere and explicit shadow rays are traced. A real physically correct sky/sun system (like Preetham sky) is something I will look into in the future. I have modified some things in the sampling (removed the stratified sampling) to improve realism at the cost of noise, which you will see in my next demo.

Post a Comment
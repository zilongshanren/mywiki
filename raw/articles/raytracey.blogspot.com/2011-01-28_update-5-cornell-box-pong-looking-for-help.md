---
title: 'Update 5 Cornell Box Pong: looking for help'
url: http://raytracey.blogspot.com/2011/01/update-5-cornell-box-pong-looking-for.html
author: Sam Lapere
published: '2011-01-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For the past couple of days, I've been scratching my head over how to modify the tokaspt source code (gl_scene_cc to be more specific) in order to cram in some 2D gameplay physics (circle/circle collision detection) and direct user interaction with the paddles. Unfortunately without much success. I've come to the disheartening conclusion that I know too little about C++ to be able to write useful working code for the game (I know how to program very basic routine-like stuff with loops, hoping that would suffice, but alas). If anyone is interested to help out with this project, I would be eternally grateful! You can contact me at the address on this page

[http://i55.tinypic.com/2ppfqma.jpg](http://i55.tinypic.com/2ppfqma.jpg)UPDATE: for the game physics of Cornell Box Pong, I've decided to use

[Box2D](http://www.box2d.org/), an excellent easy-to-learn and open source 2D physics engine used by many iPhone games, which uses an advanced continuous collision detection model. You can also specify parameters such as gravity, friction, physics simulation rate and accuracy of the physics.If I'm done with this project, I plan to integrate Bullet, the open source 3D physics engine, into tokaspt so real-time path traced physics driven animations like in

## 4 comments:

Well I am a professional developer so it would be pretty ignorant of me not to offer my help :)


What's you preferred method to chat?

Cool! Thanks a lot Kerrash!

Hi my names Magnus Wootton, I go by "rouncer" most of the time.

What kind of hardware are you using to get these convergance rates!!! this is phenomenal!!!

I want to start coding for raytraced games too, but this is the only place I saw it at decent enough speed, I wonder why that is also...

Im a good coder too, but looks like you got help already.

Hi Magnus,





I remember your username rouncer from the ompf forum. First I want to clarify something: what you see in the looped animation is not real-time, but prerendered on my 8600 GT M. Every frame rendered for 3 seconds. According to my estimates, a GTX 580 is approximately 30 times faster (or more because of the L1 and L2 cache) than a 8600 GT M. This means that the same frame that took 3 seconds to render on my 8600 GT M, should take about 0.1 seconds rendertime on a GTX580, so it would run at 10 fps at the quality you see in the animation.

The convergence rates of tokaspt, developed by tbp from ompf.org, are indeed phenomenal because it is highly specialized for what it does: it only uses spheres as primitives, which are very cheap to raytrace, and uses a bunch of clever tricks to maximize occupancy on the GPU. The Pong scene is also designed to maximize convergence speed: it consists of only 13 spheres (walls, ceiling, floor, light source, Pong ball, Pong paddles and background spheres) and has a very large light source so the scene is mostly lit with direct lighting.

If you're interested, extra help with this project would be very welcome and appreciated! If you have a CUDA enabled GPU, you can download tokaspt from Google Code and run the Pong scene (download link in one of my previous posts). Currently I'm figuring out the 2D collision detection system.

If you're interested please contact me on my e-mail address at http://i55.tinypic.com/2ppfqma.jpg

Post a Comment
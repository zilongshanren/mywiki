---
title: Unbiased Stunt Racer!
url: http://raytracey.blogspot.com/2011/09/unbiased-stunt-racer.html
author: Sam Lapere
published: '2011-09-05'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For the last couple of days, I've been busy creating "Unbiased Stunt Racer", a new real-time path traced demo involving physics, a vehicle and a shooting robot. It's actually a mix of a platformer and a stunt driving game. First you have to reach a platform by driving the vehicle over a ramp, then you have to reach another platform with a robot which is shooting at you, by driving over two rails where a nasty chrome sphere hinders the passage. The final goal is to push the robot off of his cosy place. The sunlight is constantly changing position and color, casting nice soft shadows over the scene. Below is a walkthrough video (rendered on GTS450) and some screenshots:

The number of samples per pixel can now be altered at runtime with the O and P keys. Pressing space resets the car. I've converted some of the stratified sampling in the original code back to purely random sampling, resulting in a slightly noisier but more realistic image.


An executable demo for Unbiased Stunt Racer is available at

An executable demo for Unbiased Stunt Racer is available at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)The biggest advantage of using real-time ray tracing/path tracing for these "games" (besides having higher quality graphics) is that almost anyone can immediately start creating simple games without worrying about lighting, shadows, multiple reflections, refractions and all combinations of these effects. Everything just works as expected and without any effort on the artist side. It's like a "push button" game engine: just create the scene and the renderer takes care of everything else.

## 10 comments:

This one works on my computer. This is great. But there are several problems that i found :

- I think you used constant numbers for Bullet updates. Unbiased_Stunt_Racer_usercam is running at 250 FPS with 4spp and everything is lightning fast (robot spinning, car, sun moving). You should use "the time since last update" in place of your consts.

- The more spp I use, the darker the image.

- When you go off the track, the car seems to fly. The farther you go, the higher is the car.

BTW, Keep it up with the great things ;)

Thanks, glad it's working on your computer. But 250 fps?? That's nuts, what hardware are you using?




I'm indeed using a fixed framerate for the Bullet physics simulation (20 fps), which works great on my system, but apparently not on yours :). I should change that.

I've noticed the darkening with higher spp as well, I don't have an explanation for that right now. I know that the path length increases with higher spp/passes, it's a specific Russian Roulette like optimization by Jacco. You would expect a brighter image with increasing path length, which is confusing. I should dig deeper into the rendering part.

The "floor" that you see in the demo is not flat, it's in fact a giant sphere. The floor in the physics world is a plane, so the further you go with the car, the greater the curvature of the sphere which makes the car seem to float.

these are great explaination to all my points :)


I'm running on a i7 2600k with a 580GTX

Edge-Avoiding A-Trous Wavelet Transform for fast Global Illumination Filtering:


http://www.youtube.com/watch?v=5OzUl-6zjV0

http://www.uni-ulm.de/in/mi/graphics/atrous-filter.html

I know the paper and I'm thinking of implementing the filter at some point in the future :)

Mine can't start because of FreeImage.dll was not found. Is this some cuda thing? Will try to update my drivers

I've uploaded a new version with the missing dll's. Let me know if it works.

Thanks, it works great now :)

No problem, glad it's working now :)

Post a Comment
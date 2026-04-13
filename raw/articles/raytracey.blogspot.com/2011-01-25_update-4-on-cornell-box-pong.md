---
title: Update 4 on Cornell Box Pong
url: http://raytracey.blogspot.com/2011/01/update-4-on-cornell-box-pong.html
author: Sam Lapere
published: '2011-01-25'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](http://i54.tinypic.com/2wr4012.gif)


![](http://i54.tinypic.com/2wr4012.gif)

And 2 youtube videos:

[http://www.youtube.com/watch?v=Ze1U8X4Awuc](http://www.youtube.com/watch?v=Ze1U8X4Awuc)

[http://www.youtube.com/watch?v=rCqXd6bAw0k](http://www.youtube.com/watch?v=rCqXd6bAw0k)

[Download scene](http://www.2shared.com/file/rdPQLxj5/pong01.html)(needs tokaspt to run)

The benefits of real-time path tracing in this scene are obvious and impossible or very difficult to achieve with rasterization based techniques:


- refraction in the glass sphere in front

- reflection on curved surfaces

- diffuse interreflection, showing color bleeding on the background spheres and on the Pong ball

- soft shadows behind the background spheres and under the Pong ball when touching the ground

- true ambient occlusion (no fakes as used by SSAO, or the much better quality AOV) when the balls approach ceiling or floor

- indirect lighting (ceiling, parts of the back wall in shadow)

- anti-aliasing (multiple stochastic samples per pixel)


Now I want to focus on getting the game code ready.

- refraction in the glass sphere in front

- reflection on curved surfaces

- diffuse interreflection, showing color bleeding on the background spheres and on the Pong ball

- soft shadows behind the background spheres and under the Pong ball when touching the ground

- true ambient occlusion (no fakes as used by SSAO, or the much better quality AOV) when the balls approach ceiling or floor

- indirect lighting (ceiling, parts of the back wall in shadow)

- anti-aliasing (multiple stochastic samples per pixel)

Now I want to focus on getting the game code ready.

Update: I've made the room higher and all the walls, celing and floor are now convex, which should simplify the collision detection:

![](../../assets/0ba1051756e29314.png)


![](../../assets/0ba1051756e29314.png)

## 4 comments:

Great, looks cool !

Wonder how easy it'll be to follow the game with a noisy picture though :)

Thanks!


The amount of noise depends entirely on your graphics card. I know for sure that the game will look like a noisy mess on my 8600gt m, but on a Fermi card it should look like the simulation that I've made, which I think has a very acceptable noise level (the quality of the picture was also reduced when making the GIF, so quality should be even better). From tests I've seen on other forums, Fermi cards are at least 20 times faster than my laptop GPU.

Definitely a cool idea for a game, can't wait to try it out. How's the progress so far?

Thanks.



About the progress, I'm still learning the C++ language so I can modify gl_scene_cc in tokaspt source code and incorporate a simple 2D physics model for circle/circle collision detection and deflection.

I'm not going to touch the CUDA part, because it's more than fine as it is right now and programming CUDA is not my thing. I haven't started coding yet and I'm not sure if I will be any time soon.

If you're a programmer, feel free to try out some things yourself, it should be really simple if you're familiar with C++ (which I am not currently). Source code for the original Pong game can easily be found with google.

Post a Comment
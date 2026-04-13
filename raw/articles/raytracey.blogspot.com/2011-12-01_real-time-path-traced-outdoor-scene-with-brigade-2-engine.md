---
title: Real-time path traced outdoor scene with Brigade 2 engine
url: http://raytracey.blogspot.com/2011/12/real-time-path-traced-outdoor-scene.html
author: Sam Lapere
published: '2011-12-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Jacco Bikker has just posted a gorgeous looking new video of a WIP game oozing with atmosphere, which is running on the real-time path tracer Brigade 2:

A downloadable direct feed version (strongly recommended) can be found here:

[http://igad.nhtv.nl/~bikker/files/sections.avi](http://igad.nhtv.nl/~bikker/files/sections.avi)The video description says it all:

"This is some early footage from the student game "It's About Time", created by students of the IGAD program of the NHTV university of applied sciences, Breda, The Netherlands. This game uses the Brigade 2 path tracer for rendering. Although this results in a noisy image, the lighting is very realistic. A proof-of-concept demo of the game will be ready in January 2012. After that, the team intends to continue working on the project until the end of the academic year."

Some screengrabs from the video:

Note the ambient occlusion under the cylindrical stones and the greenish color bleeding on them


The lighting in the video is of the same quality as a precomputed lightmap, but is completely real-time. Obviously there is still some noise, most visible in indirectly lit parts of the scene, but I personally think it adds a special touch to the image, while at the same time attesting to the "real-timeness" of the lighting. The Brigade engine will truly shine when moving objects and animated characters will be added, which will both receive and radiate the same "perfect" physically based lighting as their environments. Moreover, this scene is just showing diffuse materials, but Brigade 2 can handle materials such as glass (with physically based light attenuation according to Beer's law), glossy (Blinn shader) and perfectly specular effortlessly, as proven in the videos in

[this post](http://raytracey.blogspot.com/2011/11/new-videos-of-brigade.html).In the image below, notice the indirect lighting with brownish color bleeding under the wooden roof.

![](../../assets/a7725ffb94bc4e01.png)


![](../../assets/a7725ffb94bc4e01.png)

Today's games use a variety of tricks to approximate indirect lighting, such as high quality precomputed lightmaps (e.g. RAGE from id Software, Mirror's Edge from D.I.C.E.), instant radiosity (e.g. Geomeric's Enlighten technology in Battlefield 3, Lightsprint in Rockstar's L.A. Noire), cascaded light propagation volumes (LPV) with screen space GI (Crysis 2) and point based color bleeding (

[Danger Planet tech demo from Fantasy Labs](http://www.youtube.com/watch?v=HiazZdVlOKw), based on Michael Bunnell's surfel technique which was also used in Pixar's Up and in Pirates of the Caribbean). Each of these techniques has its own drawbacks:- full or partial precomputation of lighting,

- limited scene destructability,

- real-time hard shadows superimposed over high quality, prebaked soft shadows resulting in an ugly shadow mix (RAGE and Mirror's Edge are nice examples)

- limited number of bounces

- crudely approximated, diffuse only indirect lighting

- no influence from the color of dynamic objects on the environment (e.g. a red wall will cast a reddish glow on a nearby white barrel, but a red explosive barrel near a white wall will do nothing)

- time consuming artist intervention (e.g. manual light probe placement in areas of interest)

While it's great to see that some games are finally implementing real-time GI approximations, they are still hacks that start to break when mirrors, glass and highly glossy objects are added to the scene. Real-time path tracing solves all these issues in one breath. While the performance on one current high-end GPU is still not sufficient, very nice looking real-time path traced prototypes (with animation) are already possible, giving a glimpse of where game graphics are headed when GPU clusters in the cloud come into play.

Right now, I'm busy working on some Brigade 2 powered real-time demo's (with Bullet physics) which I hope to show very soon.

## 2 comments:

"Right now, I'm busy working on some Brigade 2 powered real-time demo's (with Bullet physics) which I hope to show very soon."


Cant wait :-)

I've succeeded at making a physics-enabled executable demo of the scene with the glass horse shown in the previous Brigade2 videos (with only diffuse objects though, I still need to figure out how to change materials). The demo is currently very simple, just a light bouncing up and down, obeying the laws of gravity, but the moving shadows are awesome.


I'll upload a video soon.

Post a Comment
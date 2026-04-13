---
title: 'Real-time GPU path tracing: Physics dragons 2'
url: http://raytracey.blogspot.com/2013/01/real-time-gpu-path-tracing-physics.html
author: Sam Lapere
published: '2013-01-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The following video accompanies



It shows 1024 dynamic instances of a Stanford dragon model of 100k triangles each, for a total of 100 million triangles, path traced with Brigade in real-time. Brigade easily allows path tracing of several billion triangles in real-time (we tried 4096 randomly spinning instances of the Asian city model which contains over 400k triangles, and the framerate was surprisingly fluent). This is impossible with OpenGL or DirectX. This is the prime reason why games must switch to a pure ray tracing or path tracing approach (hybrid raster/ray tracing will just not work) if game developers want to have scenes with several hundred million triangles filling the screen. And that's not even taking the perfect soft shadows, depth of field, reflections, refractions, arbitrary BRDFs and color bleeding into account.

[the screenshots from the previous post](http://raytracey.blogspot.co.nz/2012/12/real-time-gpu-path-tracing-physics.html):It shows 1024 dynamic instances of a Stanford dragon model of 100k triangles each, for a total of 100 million triangles, path traced with Brigade in real-time. Brigade easily allows path tracing of several billion triangles in real-time (we tried 4096 randomly spinning instances of the Asian city model which contains over 400k triangles, and the framerate was surprisingly fluent). This is impossible with OpenGL or DirectX. This is the prime reason why games must switch to a pure ray tracing or path tracing approach (hybrid raster/ray tracing will just not work) if game developers want to have scenes with several hundred million triangles filling the screen. And that's not even taking the perfect soft shadows, depth of field, reflections, refractions, arbitrary BRDFs and color bleeding into account.

## 20 comments:

So, are you in the know of how this instancing trick works? Is it similar to modulating the ray position which gives you instances in a grid?



You just have to transform the rays for each instance. The tricky part is making it run efficient and in real-time.

Hmm, I'm quite curious to see realtime NON-photorealistic rendering implemented on top of Brigade :D

A little off-topic but how come the physics are so bad?

It looks like all the dragons have sphere colliders, or is that part of the test?

Dima, there are already tons of engines doing real-time non-photorealistic rendering out there, why would you need a path tracer for that?



Paul, yep, the dragons are enclosed by spheres in Bullet. Having correct physics was not a priority. The main reason for this test was to see how well Brigade's scene graph could handle lots of randomly spinning instances moving in random directions (instead of arrays of spinning instances like the car test from a previous post), for which a simple collapsing physics sim is ideal. We were wondering if the path tracing performance would degrade much if instances moved further and further apart from each other.

The results were even better than I expected, the performance didn't go down at all. When I first saw this running on my system at this speed, I smiled really hard.

So you are not using directX or openGL So how are you suppose to talk to the gpu then ?

Wow! Sam this is amazing.






Im guessing that the instances are placed using a matrix transform, would this allow for scaling and or shearing of instances not just position and rotation?

Being able to alter the instance properties a little further, ie being able to modify the instances' materials would be something for the future...

Im still amazed that we can do real time path tracing at these sorts of speeds! By the way what hardware is being used to do this what GPU's are being used?

Finally is this version of brigade using uni directional path tracing, ie from camera to light sources, or is it using bidirectional path tracing or even more complex MLT or some of the newer ERPT stuff that you mentioned in some earlier posts?

@Warai Otoko: This is using the CUDA api to communicate with the Nvidia GPUs directly to do the work, its not using any graphics apis!

Hi Sam, Love what you guys are doing. Is this going to be supported on Open CL hardware (AMD). Also what are the long term plans, Is there a chance this will be open up for use with a percentage of profits on releases like UDK/Cryengine 3. I would love to start on a project to use this in the future.

Warai Otoko: no, we're using GPGPU languages (cuda and opencl)









Hi Lensman, thanks. We can do scaling of the instances too, no shearing yet. We can also customze each instance with its own materials already, but we haven't shown that yet.

I'm also amazed that we can do path tracing at these speeds and I feel we can push it even further :) I'd rather not say what GPU this was running on, because we're still constantly optimizing it.

This is using unidirectional path tracing currently, but there is already something else around the corner which produces instant caustics. MLT and ERPT are impractical for real-time purposes, they are just too slow right now.

KingBadger3D, thanks! Brigade supports AMD cards and actually runs amazingly well on the latest 7000 series. Integration in game engines is a potential future direction ;)

>> ...why would you need a path tracer for that?




First of all, because of the performance :) As you have said yourself, "this is the prime reason why games must switch to a pure ray tracing or path tracing approach."

Well, since photorealism is not required, super-detailed NPR games could rely on a different technology (e.g. Unlimited Detail), but path tracing looks like an interesting alternative.

Also, some NPRs are transforming photorealistic pictures into "paintings", so they get extra benefit from path tracing :-)

I'm just curious how easy/hard it might be to make Brigade generate the necessary metadata (depth/normal/object-ID/etc. buffers... which, I suppose, would be useful even for many "photorealistic" games).

Also, it might be interesting to see if NPR postprocessing would make path tracing artifacts more or less apparent.

@dima:





I think you're missing the point regarding brigade... Brigade is a path tracer rather than a standard raytracer. What you are describing regarding the npr rendering requirements would be fulfilled by a gpu accelerated raytracer, brigades predecessor was one!

The whole point of a pathtracer is that it handles all those effects such as proper soft shadowing and colour bleeding, caustics etc that npr doesn't care about!

Dima: you've got a very good point there. There is a reason why the newest generation of DCC tools (e.g. Isotropix Clarisse) are moving away from OpenGL rasterized viewports, because they are unbearably slow in heavy scenes and completely impractical. Having a raytraced viewport is the only way to interact with scenes containing hundreds of millions or even billions of polygons. The same goes for games of course.



It's actually pretty easy to create depth, normal and position buffers with a raytracer and post-processing does help a lot.

Lensman: Brigade can also do simple ray tracing with one sample per pixel (which is superfast), but then you loose things like soft shadows, DOF, AO, glossy reflections and anti-aliasing (and of course indirect diffuse lighting). But it does specular reflections and refractions, so combined with a prebaked lightmap, it could easily look better than Mirror's Edge (which contained mostly static environments anyway).

Sam: Whilst I agree brigade could probably be made to work as a raytracer, a pathtracer doing just 1 sample per pixel is not the same thing as a raytracer. For example in a pathtracer, the 1 ray per pixel hits a diffuse surface for example, it then has some chance of being reflected into a random direction ie bouncing light around. Whereas in a proper raytracer, the 1 ray per pixel hitting a diffuse surface would immediately check for being in shadow and then return its diffuse colour according to the angle the surface is to the light.


Dima: Yes I agree with you regarding highly complex models ie CAD used in aviation industry etc. Here using a gpu accelerated raytracer definitely has advantages and will continue to become better suited as model detail goes up and rasterizers start choking on the millions of micro polygons in the scene.

Hi Lensman, I actually meant that Brigade can also do Whitted style ray tracing, without any Monte Carlo randomness, it's just another kernel you can choose from in addition to the different path tracing kernels.

Sam, Can we have a new build to play with. As a AMD user at the mo i cant test anything as open CL isnt supported )plus your little racing taxi as an example with the bullet physics would be good).

KingBadger3D: Brigade will be released for game devs once the tools are finished. The car in the city demo in the city is only for internal use unfortunately. But don't despair, we're going to show something spectacular in a few weeks.

Sweet, Also im not sure if youve seen this as a good year old but very interesting i would think for you guys. It's a very interesting noise removal setup for qmc path tracer. On Filtering the Noise from the Random Parameters in Monte Carlo Rendering, Link:http://agl.unm.edu/rpf/index.php

I saw that paper the day it was published (even made a post about it). It looks good but is not useful for Brigade, unless you want to play at 0.003 fps. There is an open source executable demo of this algorithm out there, check Timo Aila's website, he compares RPF to his own method (which is better of course, but also not quite real-time).

"we're going to show something spectacular in a few weeks."



And i bet thats all you can say :-)

Will it be something playable for us, or just video?

Yep, that's all :)


It's not going to be a video, but will be played in front of a live audience :)

Post a Comment
---
title: 'Real-time photorealistic GPU path tracing: Streets of Asia with dynamic water'
url: http://raytracey.blogspot.com/2012/04/real-time-photorealistic-gpu-path.html
author: Sam Lapere
published: '2012-04-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The video from the previous blogpost got over 75,000 views on Youtube, just a tad more than the usual 200 or so views per vid, so I decided to upgrade it a bit with a Stanford dragon and some teapots with glossy materials. Jeroen van Schijndel (OTOY developer working on Brigade) implemented dynamic water that



[also reacts to the player](http://www.youtube.com/watch?v=KRnsLmnN1TE)(test made with Brigade). It's nothing short of amazing to see the water ripples rendered with real-time reflection and refraction. The BVH acceleration structure for the mesh describing the water surface is updated every frame allowing for real-time path traced water. Brigade also got an incredible speed boost since the previous demo, it's even more real-time now :):**4 minute Youtube video:**


[http://www.youtube.com/watch?v=5-naYSmhGOY](http://www.youtube.com/watch?v=5-naYSmhGOY)



Stay tuned for a new demo of a photoreal, real-time path traced massive modern city, which I will reveal very soon. A preview screenshot (still lots of materials to tweak):

## 40 comments:

liar! the city is not a rendering, it's a photograph! :D

lol, the kind of reaction I like :)

It's hard to see with that level of noise... Were there caustics? BTW, is it possible to place camera under the water and see a correct "underwater" picture?

Also, it would be interesting to see the related effect of "water film / drops of water on camera lens" :)

Any possibility of glossy reflections ? Not all materials are pure mirrors, like glazed tiles, polished wood, brushed metal...

subtleD: there are no caustics, when the camera goes under water. I suspect this is due to one-sided surfaces.


Anonymous: the dragon and some teapots are glossy, you can also see some glossy floor tiles on the screenshots in my previous post.

With glossy reflection I mean you still see a mirror image, but it is heavily blurred like at http://www.blender.org/development/release-logs/blender-246/glossy-reflectionrefraction/

I know what you mean. I'm currently using a glossy shader which doesn't blur the reflection, but just blends between diffuse and specular. I will use more diverse materials in an upcoming demo.

Thanks for adding the resolution and SPP to the top!

Hi Sam! May you add to the massive modern city any model of modern car if you have some of course?

The city model has some cars in it as well, what you see in the screenshot is just a tiny bit. It's actually pretty detailed at the ground level with traffic signs, lanterns, waste bins, mailboxes, garbage etc. I didn't want to spoil it too much yet :)

hope it will be looking not worse like this: (OTOY)


may be at least it's someday in the future ))

OTOY:

http://www.youtube.com/watch?v=k4aE6HK7JEo&feature=related

Funny that you mention this, that video was actually my inspiration for this city scene :)



Btw, that's BCN city from JJ Palomo (Big Lazy Robot). It's actually due to this guy's work that I developed a passion for photorealistic graphics. I've always wanted to recreate that BCN video in real-time since the first time I saw it back in 2006 and now I finally have the tools to do it :D

There's also another amazingly photoreal video at http://www.3dblasphemy.com/OPTIMUS/OPTIMUS.html

And it was my inspiration about future possibilities of real-time render engines. Just a one thought about creating beautiful world what I want see now impressed me since that time. I like OTOY films:

http://www.youtube.com/watch?v=f6HcENb4Nek

http://www.youtube.com/watch?v=0YjXCae4Gu0&feature=related

Sam,I wish you good luck in your work and I'm waiting nearest fine results in it. Hope we will delighted after finished your work and new graphics processor release.)))

IL, thanks, finest results are on the way ;)

What makes you think those videos are rendered in realtime with OTOY?


Or are you simply linking to some neat rendered animations?

I know for a fact that they are rendered with vray...unless they were recreated/ported over later on.

http://forums.cgsociety.org/showthread.php?f=139&t=242576&page=2&pp=15

Please look at this technique: http://agl.unm.edu/rpf/


It allows you to smooth out the noise in paritally rendered frames using a dynamically sized blur filter based on how the variance of the sample rays propagates to various parts of the image.

Anonymous: the Ruby cinema 2.0 video is real-time and was made by OTOY in collaboration with Big Lazy Robot (3DBlasphemy)


Anonymous (last post): yeah, the random parameter filtering looks interesting, but it's far from real-time. Maybe a GPU implementation (or better yet a hardware implementation) could run at 30 fps.

There is actually a raytraced game by OTOY that will be released this year:

http://www.brightsideofnews.com/news/2009/9/21/worlds-first-ray-traced-pc-game-and-movie-to-arrive-in-2012.aspx

Congrats on getting featured in Gpuscience.com.

Cool :)

Sorry Sam, but there is no evidence at all that the Ruby video you are referring to is real time. Everything indicates it is a pre-rendered CG video clip by BLR as they tell on their portfolio page http://www.biglazyrobot.com/

Somehow this video got associated with AMD (cinema 2.0, never to be heard of again). The idea probably was to make use of 3D scanned surface information of faces, as is used in VFX relighting for movies (and this did not even make it into the Ruby movie).

I don't know where you've read on BLR's portfolio that it's prerendered. This is what that site actually says:


"This is our first project for AMD. We built this clip to promote the new AMD's Cinema 2.0, a new and exciting real-time tech.

Otoy and AMD have use all our stuff to test a new and amazing real-time technology as part of the new Cinema 2.0."

Keep the good work Sam!


each demo its looking more realistic.

Greeting from Brazil. :)

We built this clip...

What do you think clip means ?

It is a CG prerendered video clip like all the other clips listed at the BLR portfolio. That's what a VFX company like BLR does, create clips with tools like Maya, Max, ...

Possibly also a mix of CG with real video sequences, to be clear.

Jonatas, muito obrigado. Espero que o proximo demo vai ser ainda mais legal :)

I know, GTX580 has limit for double precision, but GTX680 is worse in DP, but better in SP float.

Does Brigade Engine use DP calculations?

If yes, Tesla should be better for this?

If no, why you don`t use GTX680?

StaseG: Brigade doesn't use double precision, there's no advantage in using Tesla. Moreover GeForce is faster than Tesla or Quadro at path tracing.


As for the 680, it's worse than the GTX 580 for Brigade and CUDA apps in general.

Samuel: not necessarily. Apparently, Aila & Laine's ray traversal kernels are 40% faster on GTX680 with the latest (minor) changes. We simply didn't apply this in Brigade yet.


- Jacco.

Then I shall wait for the Kepler optimized Brigade code :)

Thanks :)

And one more question.

I`ve seen some examples of GPGPU computing, using GLSL.

http://www.youtube.com/watch?v=aJCcqa87ZsQ

And I know only one path tracer (Made by Evan), that use GLSL in calculation.

Why you don`t use GLSL computing in Brigade?

@StaseG: In GLSL, inter-thread communication is not possible (unless you do multi-pass, which introduces different inefficiencies). CUDA currently provides the best mix between low-level control and raw performance. OpenCL abstracts things a bit further, which removes some low-level opportunities. I think CUDA is currently the best 'base platform'; ideally other platforms should be targetted using some kind of cross compilation (there are tools for that; didn't have time to seriously investigate those yet).


- Jacco.

StaseG: CUDA is more flexible and powerful for general purpose GPU computing than GLSL + everything Jacco said

Cuda is great, if you have a Nvidia GPU. And using Cuda is great for Nvidia because it locks out the competition. And even using Cuda there is still like 4 levels of compute backwards incompatibility.

If you target a very niche application that may be all you need, for any other use case it is not a smart choice as you limit your market.

In my experience Direct Compute is similar good as Cuda, and is supported well by both Nvidia and AMD. It is still early days for GPU compute, and eventually a C++ language extension may be the definitive solution.

@Anonymous: frankly, I would never trust Microsoft with a GPGPU language. But it would be interesting to see how a complex piece of code runs on CUDA and Direct Compute, performance wise, and implementation-efficiency wise.




Right now, I believe the cross-compile approach is good. The GPGPUs are similar on a hardware level, and the languages are similar as a result; just use what you prefer, or what gives you sufficient control over your target hardware.

Regarding multiple levels of CUDA backwards compatibility: true, but not such a problem for Brigade: we simply need tons of performance anyway so anything before GTX470 is not that relevant... That's a case-specific argument, obviously.

- Jacco.

"Anonymous said...













Sorry Sam, but there is no evidence at all that the Ruby video you are referring to is real time."

I made that demo 4 years ago. JJ and his guys made a animated clip in Max+VRAY, and I made a real time demo from that dataset.

BTW, the scope of the AMD cinema 2.0 demo just to show relightingof a video clip- and nothing else. I wanted to do more, so I pushed the demo further, adding the ability to navigate through the scene as well. I spent weeks at BLR in 2008 to get the data I needed to get that working.

I exported the scene as voxels from MAX, the GI lighting info from VRAY per voxel, and did reflections/raycasting using the voxel data. I also exported lightfields (per material) generated by VRAY to identically match the way VRAY did reflections.

One reason the live demo wasn't released by AMD was because it was over 3 GB. AMD didn't enable binary CAL GPGPU kernels by the time the 4870 launched in summer 2008, so we didn't include our GPU codec in the final exe. If we had, it would have reduced the demo by 50x or more. It was a valuable lesson in shaping our future GPGPU work. It led us to write our own OCL compiler+runtime (from scratch) for Cypress and Cayman GPUs.

For anyone interested in what the 2008 voxel demo looked like, see @ 1:12 in this video (it's just a few seconds long - it is also streaming from the cloud):

http://vimeo.com/22048037

When we presented an updated version of the demo at Siggraph 2008, I had the city scene deforming. This was to show we weren't limited to tracing static data. There was a video made for this Siggraph presentation, although I can't find the link off hand.

There was also an experimental version done using tri-meshes converted to voxel data in real time (not using any of the VRAY GI info in this case). It was just a test, but the post FX was based on the combustion layers JJ made for the beauty shots:

http://techcrunch.files.wordpress.com/otoy15.png

I have to second Sam's post regarding JJ's work. He's an absolute genius and an inspiration to me and many of us working at OTOY.

-Jules

PS. When Brigade is further along, we'll test the Ruby Demo scene with it. I have tested it at 1080p in Octane, and it looks great.

Nice to see Jules Urbach talking more about the old Cinema 2.0 tech demos.



I was wondering what really happened when it was MIA at Radeon's 4870 launch.

I'm still eagerly waiting for more Gaiking media releases.

I really like the idea of making a film + computer game simultaneously with almost no apparent graphical differences between the two (although I'm pretty sure there still will be, realistically speaking).

Will there be any updates about OTOY for the upcoming E3? Or maybe SIGGRAPH?

Jules, Have you this video of your test of the Ruby Demo scene in Octane ? It will be wonderful to watch this. ))

Thanks for the clarifications Jules, nothing better than first hand information :)

Post a Comment
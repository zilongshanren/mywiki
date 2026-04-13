---
title: get my slides from GDC2012.
url: https://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/
author: Done- Here Comment By Directtovideo
published: '2012-03-15'
source_blog: direct to video
source_site: https://directtovideo.wordpress.com
category: graphics
fetched: '2026-04-13'
---

As promised, [they’re here!](https://directtovideo.wordpress.com/wp-content/uploads/2012/03/gdc_2012_released.ppt) I’m afraid I had to delete all the videos, but apparently the recording of the full thing should be in the GDC Vault at some point.

[PDF [here](https://directtovideo.wordpress.com/wp-content/uploads/2012/03/gdc_2012_released.pdf)]


*Yes I am aware that SlideShare managed to crop the bejesus out of my presentation*

To everyone who showed up to my talk – thanks for coming! [Here are the slides](https://directtovideo.wordpress.com/wp-content/uploads/2012/03/gdc_2012_released.ppt) as a memento of the occasion!

To anyone who couldn’t make it and wants to read the slides, [here they are](https://directtovideo.wordpress.com/wp-content/uploads/2012/03/gdc_2012_released.ppt)! Good luck making sense of them!

To anyone who was at GDC but went to something else instead – [here’s what you missed](http://www.youtube.com/watch?v=dQw4w9WgXcQ&ob=av2e)!

If you did see the presentation live, I was supposed to ask you to fill out the evaluation forms (only if you liked it, obviously – I don’t want to get 100 forms back saying “bat shit mental”). Oh, and I was also supposed to ask you to turn off your mobile phone, no flash photography, no video cameras, and that there are two exits at the back and to file out in row order in case of emergency, but I forgot. Apparently we all made it out alive.

Please do tell me what you thought on here too.

Very nice talk! I’m in the “To anyone who couldn’t make it and wants to read the slides, here they are! Good luck making sense of them!” group 😉

They make perfect sense by the way, very cool 🙂

Comment by Paulo Falcao — March 15, 2012 @ 1:28 pm

Hi Matt,

Any chance you provide them in PDF as well?

Comment by Gregory Pakosz (@gpakosz) — March 15, 2012 @ 3:47 pm

done- here 🙂

Comment by directtovideo — March 15, 2012 @ 4:39 pm

Truly awesome stuff! I really like the ray-traced AO.

Comment by MJP — March 15, 2012 @ 5:49 pm

Thank you thank you. Good and chewy, filled with practical implementation. Bravo!

Comment by Robin Green — March 15, 2012 @ 5:54 pm

Hello, Matt. The slides are awesome and inspirational. I was very pleased to find some information about SDF in context of blobs rendering, cause i am trying to code efficient renderer of this stuff for some time. But i can`t grasp some steps. Can you tell more about your slide “Evaluating Particles, Fast”? About additive blending, summation in alpha channel and division. Big thanks in advance..

Comment by iodiott — March 17, 2012 @ 11:25 am

Hello, Matt. The slides are awesome and inspirational. I was very pleased to find some information about SDF in context of blobs rendering, cause I am trying to code efficient renderer of this stuff for some time. But I can`t grasp some steps in your algo. Can you tell more about slide “Evaluating Particles, Fast”? About writing out, additive blending, summation in alpha channel and division. Big thanks in advance 🙂

A few words about my attempts. I`ve started with simple ray-marching of few analytically defined blobs. http://goo.gl/6r5mw Than I studied optimization methods: depth peeling, Bezier clipping, empty space skipping, BVH… but after some time understand that this stuff is quite useless and rather complicated when you want to render many-many blobs. Then I stumbled on your old post about Frameranger. And it was Holy Grail, particularly comments, where you told the same things. So I digged up my old voxel-renderer of volume texture and began to experiment. http://goo.gl/MFk0o

Now I am trying to figure out how to build properly distance field and visualize it 🙂

Comment by iodiot — March 17, 2012 @ 12:04 pm

I’ll try explain as best I can.. this is the basic approach (“Evaluating Metaballs, Fast”) that we used more or less the same on Numb Res on DX9 as well, so I’m not giving too much new stuff away here. 🙂

You have a 3D texture which can be rendered to, format is e.g. R32G32B32A32_FLOAT (- size could be e.g. 128x128x128). Create a bounding box which contains your particles (approximately) that will be the space your 3d texture contains, and generate a transform which maps from world to 3d texture space. Bind the texture as a render target.

Render the particles as points; transform to 3d texture space in vertex shader, then in the geometry shader you expand the points into quads, calculate the render target slice for the point, and you also expand across several slices of the texture. It should cover several pixels in x,y and z so you will probably end up outputting e.g. 11 quads each 11×11 pixels in size to give a 5 pixel radius spread.

In the pixel shader you get the destination pixel position – i.e. the destination pixel in the 3d texture grid, because it has a slice index too – and you have the particle’s position. Transform both into same space then calculate the weight (Weight) using the blobby equation of the point on the pixel. Then write out float4(Position.xyz * Weight, Weight), use additive blending.

Now you have 2 options with the final 3d texture:

1. The alpha channel contains the sum of metaball potentials of each point on the grid. evaluate using marching cubes.

2. Evaluate a signed distance from The texture sample T and the texel position P:

float3(T.xyz / T.w) = the weighted centre position of the particles affecting point P (weighted by blobby equation).

approx signed distance = length(P – (T.xyz/T.w)) – Radius.

Radius is a constant approx metaball radius.

Better results can be achieved by hacking radius using the field, but lets leave that as an exercise for the reader. 🙂

Finally this approach still gives you a sparse field; for potentials its not a problem as you can clear to 0, but for distance fields if you want to raymarch you should put a fast sweep as a post process to fill it out.

hope that helps..

Comment by directtovideo — March 19, 2012 @ 9:35 am

Big thanks for this exhaustive answer. I finally understood your method, at least I want to believe it 🙂

Comment by iodiot — March 19, 2012 @ 1:22 pm

[…] get my slides from GDC2012. « direct to video. Tagged as: glsl, graphics Leave a comment Comments (0) Trackbacks (0) ( subscribe to comments on this post ) […]

Pingback by GDC 2012 slides “Advanced Procedural Rendering” « Dysnomia Games — May 24, 2012 @ 7:54 am

Hi Matt/smash, is FLT gonna present anything at Assembly 2012?

Comment by Tiago — July 3, 2012 @ 12:24 am

[…] la presentación, Matt Swoboda, comparte algunas de las tecnicas de renderización producerales que nos puede ayudar a mejorar la […]

Pingback by TECH : Advanced Procedural Rendering con DirectX 11 « Daniel Parente Blog — July 31, 2012 @ 3:43 pm

[…] So there is this cool technique that had gained significant popularity in the demoscene called “Signed Distance Fields”. There’s a truly excellent presentation by iq of rgba (Iñigo Quilez) posted on his website http://www.iquilezles.org which he presented at nvscene back in 2008 called “Rendering Worlds with Two Triangles”. I wanted to play around with some GLSL and thought this would be a really interesting algorithm to take a look at. You can see some of the power of these types of functions in a presentation that smash of fairlight (Matt Swaboda) gave at GDC earlier this year https://directtovideo.wordpress.com. […]

Pingback by Signed Distance Fields – Part 1 | Halogenica — November 16, 2012 @ 9:53 am

There is a ridiculous amount of useful information packed in these slides. Thanks so much for posting them!

Comment by Centigonal — April 7, 2013 @ 2:41 am

[…] [4] https://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/ […]

Pingback by The future of screenspace reflections | Bart Wronski — January 25, 2014 @ 11:09 pm
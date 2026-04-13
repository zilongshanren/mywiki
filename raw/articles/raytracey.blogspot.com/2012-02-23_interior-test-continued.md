---
title: Interior test continued
url: http://raytracey.blogspot.com/2012/02/interior-test-continued.html
author: Sam Lapere
published: '2012-02-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Playing some more with Brigade 2. I really can't get enough of its awesome and ultrafast photorealistic rendering quality, it's as if you're walking around inside a photograph. Only a headmounted display is missing to make the illusion complete.

I've made yet another short video, this time rendered at 1280x720 (full render resolution), to show that Brigade can really render with superb image quality in just a few milliseconds:

The quality at this resolution is almost perfect: multiple reflections, refractions, glossy and diffuse surfaces, soft shadows, ambient occlusion, depth of field and subtle diffuse interreflection (mostly visible on the character) all render perfectly and combine just as you would expect in the real world. Take for example the reflection of the shadow cast by the glass horse (reflection+refraction+shadow): this effect would be completely undoable in a rasterizer, which struggles already with multiple transparent objects obscuring each other. No current game handles reflections of dynamic objects and characters well (let alone multiple reflections) and the reflected objects don't cast any shadows. Reflections of refracting objects aren't even an option. Luckily though, mirror rooms are not very common in the real world, so this special case can be safely ignored in games (unless you want to make a game in which ballrooms play a prominent role :).

This is my current wallpaper, 1600x900 render resolution, which rendered in just 4 seconds on 2 GTX 580s (actually it looked noise-free in under one second):

In future experiments, I will be focussing on achieving the highest possible lighting quality in real-time. For example, I think the amazing photoreal animations in the following videos (rendered with OpenCL GPU path tracing) will be possible in real-time very soon:

[http://www.youtube.com/watch?v=wPjsvA5f4pE](http://www.youtube.com/watch?v=wPjsvA5f4pE)

[http://www.youtube.com/watch?v=bSQoJW9ajmU](http://www.youtube.com/watch?v=bSQoJW9ajmU)

UPDATE: an avid reader of my blog advised me to add buttons for Twitter and Facebook, I'm still looking for the most unobtrusive way to add them ;-) Thanks Huub!

## 8 comments:

ALERT!!!

you may not add OpenCL on nvidia card only for your samples because 28x.xx and 29x.xx drivers have still issue - OCL 1.1 is 1.5x slower than OCL 1.0.

phew! I was just about to hit the "Compile with OpenCL" button here, thanks for warning me.


I've read about that issue before though. I don't think Nvidia cares as long as AMD cards don't outperform theirs in OpenCL apps.

quite impressive !

Can you give a bit more details on many diffuse/glossy bounce are generating ?

hallo, i like the effort you invest

into this "realtime" stuff. but everything here looks blurry/noisy and all examples here need at least several seconds to produce an acceptable quality (and this with 2 gtx580). getting 20fps is a factor of 50-100 ? and hd resolution is another factor of 4 on top. so where do you see to get these factors from ?

Harry, the max path depth is set to 8 for glossy, diffuse and glass. You can see in the screenshot that reflections are 8 levels deep and the diffuse character and glossy ball remain correctly lit up to the 7th level. The glass horse becomes darker and less transparent with each level of reflection, because refractive objects need at least 3 bounces to become transparent.


Anonymous, all the noise issues will be taken care of with better algorithms. What I'm showing is just naive brute force path tracing without any filtering and other improvements applied (there are already some optimizations in the code to make it render MUCH faster). The video shows that the quality is acceptable at hd resolution (720p) in under one second. The blur is only temporary. It's entirely possible to render noisefree at high framerates and resolutions with some cleverness, it'll just take some time ;-)

Would it be possible to add sub surface scattering to Brigade? I'd to see some of that on the female model


BTW are you a C++ programmer?

I don't see why it wouldn't be possible to add SSS at some point.


Yes, I know a bit of C++.

Thanks for the info. This is truelly amazing. I am quite struggling to get 8 diffuse bounce in a decent time with Arnold. ( I am also pulling 0.5 Tb of texture and millions of poly so it is slow :p )

Post a Comment
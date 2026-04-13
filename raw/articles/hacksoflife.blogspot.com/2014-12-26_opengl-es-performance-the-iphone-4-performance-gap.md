---
title: 'OpenGL ES Performance: The iPhone 4 Performance Gap'
url: http://hacksoflife.blogspot.com/2014/12/opengl-es-performance-iphone-4.html
author: Benjamin Supnik
published: '2014-12-26'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Now that we've shipped


X-Plane 10 Mobile requires iOS 8. One reason why Chris set the OS requirement so high was to intentionally exclude the iPhone 4 from our device set.


For most of the project, we worked with the iPhone 4 as our minimum device, and for the entire project, it suffered performance problems that we didn't see in any of the newer devices. The iPad 2 and iPhone 4S (the next hardware up) both performed


I don't know what caused the gap, but it wasn't a "this phone is 20% slower" or "this ipad has 4x the shader units" kind of gap. It was more like "this code runs fine on newer devices and we can just see the iPhone 4 trying to beat itself to death with its old-style dock connector so it doesn't have to run another frame of our main rendering loop".


I do not know what was going on under the hood, but I can share a few observations besides "If the 4 is having performance problems, it may be specific to the iPhone 4."




Once we cut the iPhone 4 and the 4S became the "runt of the litter" handling the low-end became a lot easier. The iPhone 4S is incredibly capable for an older-generation smart-phone, and while it is the first to run out of CPU cycles or fill rate, the losses were proportional to spec, not "fall on your face and die."


I'm hoping to post a little bit more about performance tuning OpenGL ES in future posts, but from this point forward, any advice I have will apply to the 4S and above. Having cut the iPhone 4 from our product, I no longer have time to figure out what makes it go fast.*


* One of the difficulties of OpenGL and OpenGL ES is that while the spec specifies

[X-Plane 10 Mobile,](https://itunes.apple.com/us/app/x-plane-10-mobile-flight-simulator/id566661426?mt=8)I can blog the occasional OpenGL ES performance note without revealing a stealth project.X-Plane 10 Mobile requires iOS 8. One reason why Chris set the OS requirement so high was to intentionally exclude the iPhone 4 from our device set.

For most of the project, we worked with the iPhone 4 as our minimum device, and for the entire project, it suffered performance problems that we didn't see in any of the newer devices. The iPad 2 and iPhone 4S (the next hardware up) both performed

*significantly*better.I don't know what caused the gap, but it wasn't a "this phone is 20% slower" or "this ipad has 4x the shader units" kind of gap. It was more like "this code runs fine on newer devices and we can just see the iPhone 4 trying to beat itself to death with its old-style dock connector so it doesn't have to run another frame of our main rendering loop".

I do not know what was going on under the hood, but I can share a few observations besides "If the 4 is having performance problems, it may be specific to the iPhone 4."

- The iPhone 4 was the only device that would get bottlenecked on vertex count. This was a real problem for us because we had models that we couldn't cut vertex count on without our artists spending a ton of time. We had already LODed out everything expendable on the 4 and we were still getting jammed in the 3-d cockpit.
- The iPhone 4 is very sensitive to the number of varyings and
**how they are packed**!!!! I found that packing fog and emissive light level into a 2-component varying significantly improved performance compared to having them as individual scalers. (Of course, cutting the number of varyings made the biggest improvement.) - The iPhone 4 seemed to be spending significant driver time recycling the pool of "orphaned" buffers - that is, VBOs that had been completely discarded and respecified on a per-frame basis.

*kinds*of performance problems we were having, not just a matter of degree.Once we cut the iPhone 4 and the 4S became the "runt of the litter" handling the low-end became a lot easier. The iPhone 4S is incredibly capable for an older-generation smart-phone, and while it is the first to run out of CPU cycles or fill rate, the losses were proportional to spec, not "fall on your face and die."

I'm hoping to post a little bit more about performance tuning OpenGL ES in future posts, but from this point forward, any advice I have will apply to the 4S and above. Having cut the iPhone 4 from our product, I no longer have time to figure out what makes it go fast.*

* One of the difficulties of OpenGL and OpenGL ES is that while the spec specifies

*what*the APIs do, they don't specify how fast they do it. Performance isn't guaranteed, deterministic, or often even published except in IHV presentations. One of the big pluses of Metal (and possibly GLNext) is deterministic performance - an API that tells you what will be expensive and what won't be.
It would be interesting if you would post some numbers like





ReplyDeletehow many vertices were you shading and the tiler utilization from the GPU driver instrument.

Also the render and device utilization from the GPU driver.

Afaik idevices have a unified architecture so you could shade more vertices if you fragment shader is cheaper.

In frame capture you can see the number of cycles in each shader .

Were you applying any post processing ?

2. yes packing varyings helps a lot but you need to be carefull with UV's since unpacking them in the frameshader is considered a dependent lookup and it will be much slower on the SGX543

3. what was the size in bytes of the orphaned buffers per frame ?

Also how big was the driver overhead ? what was your CPU utilization (again from the time profiler from instuments)

Hi Mihai,








ReplyDeleteI'm afraid I don't have good numbers for most of your questions, because the app doesn't run on the 4 anymore; after we dropped support and settled on iOS 8 we stopped maintaining iphone 4 support (which always required lowering lots of internal settings). I can go back and try to run the app on it but I may just hit a wall. A few notes:

1. When we'd bottle up on vertices, we'd see 95%+ tiler utilization and sometimes < 30% renderer utilization. We were in non-retina on the 4 (to keep our fps above, like, 5 fps) and changes to the fragment shader didn't seem to move tiler utilization; just varying and pure vertex count. We don't have any post processing.

2. Right - that was actually the big limit on our packing - once we simplified the lighting model as much as possible -most- varyings were driving texture lookup and had to be in XY, stopping us from having all vec4 varyings.

3. I don't know the size in bytes - there were a lot of orphan ops by -quantity- due to code that turned out after ship to be sort of stupid by design. The interesting thing is: when I realized how many orphans were happening I went back and re-ran the app through the time profiler...indeed, I missed the "bug" in ship because on newer devices the orphaning is nearly invisible - less than 1% for a "pathological" case.

So either the newer phones handle this much better or something was changed in iOS 8 - I don't know which one, but it was definitely a very different looking profile!
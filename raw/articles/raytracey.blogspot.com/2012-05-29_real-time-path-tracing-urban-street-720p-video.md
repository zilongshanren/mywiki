---
title: 'Real-time path tracing: Urban street 720p video'
url: http://raytracey.blogspot.com/2012/05/real-time-path-tracing-urban-street.html
author: Sam Lapere
published: '2012-05-29'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Unfortunately, the video quality is pretty bad with lots of splotchy artifacts due to Youtube's video compression.

**The original video file****(1.85 GB AVI)****can be downloaded from**[https://www.dropbox.com/s/6ivqouikojbtf3t/Brigadestreet.avi](https://www.dropbox.com/s/6ivqouikojbtf3t/Brigadestreet.avi)
Color bleeding test, note the reddish glow on the building's facade getting stronger with more sunlight:

Dynamic mesh light test:

- a light emitting Stanford bunny mesh illuminates the scene and casts soft shadows. The bunny is fully dynamic.

- a light emitting Doom 3 zombie which can be animated as well:

## 31 comments:

Awesome. I am curious about video quality without youtube screwITall compression.

It's a lot better uncompressed. Youtube's compression apparently can't handle Monte Carlo noise and turns the image into a splotchy mess.

Wonderful lighting.

It's amazing to see that especially the well-lit parts converge instantly.



Yet I've got a question I guess. The trash bins seem to have a transparent texture which Brigade can't handle corretly yet, it seems. I'm curious if it is hard to implement the ability to render transparent textures correctly? I guess the rays would need to check whether the object they collided with has a transparent texture and whether they hit a point of the texture that would allow them to pass through and that does not seem super effecient.

I am wondering which would turn out to be faster: Using polygons for the grid or the the check I mentioned above.

Areas that are directly lit by sunlight only need one sample, additional samples only have an effect on reducing aliasing. Areas in shadow/lit by skydome need more samples to converge.


Alpha/transparent textures are not supported yet and would probably require a mix material with a diffuse shader for the base texture and a transparent shader for the alpha mask. I think it's still more efficient to use alpha maps than creating extra geometry, although in this case it wouldn't matter much.

Hi Sam. Im wondering. If you use 50 or 100 or even 1000 object lights, how it affect render times? Will it render faster with more light in scene?

I found that Brigade is quite robust with the number of light emitting triangles. The last screenshot in the post shows an emitting Doom 3 zombie mesh, which renders very fast, the emitting Bunny is a little bit slower, as the mesh contains about 5000 emitting triangles. Brigade has built-in optimizations to pick lights based on size, distance, visibility, etc. to minimize noise and I must say that it works great.


In the sci-fi scene, I found that many small lights made the scene converge much faster than using one big light emitting quad, which was very strange. Brigade sometimes works counterintuitive and has different strengths and limitations than rasterization (mostly strengths though ;).

really nice results.. as usual. really like the emitter shots.

@Sam,


youtube has awful compression, try Vimeo instead!

I have a Vimeo account, but it only allows files up to 500 MB. FileFactory isn't ideal either, but at least you can upload files up to 2 GB.

@Sam,


well I tried to DL from FileFactory on a free account.. and no go, filefactory just stopped streaming it at about 500M. Ever since this whole megaupload thing free DL services have been complete crap.

Damn, I was afraid that was going to happen. I think I'll remove the download link, the service is too unreliable. Thanks for letting me know.

Sam, you can pre-compress your file prior to uploading to Vimeo with particular settings, and they won't re-compress the file.


If you want, I can share a folder on my Dropbox and figure out what settings work (I'm on a Mac).

Thanks Erich, I'll look into it. The issue is that most compression algos look for spatial and temporal coherency between pixels, which doesn't work at all for images with Monte Carlo noise, creating splotchy and blocky artifacts.


I can send you the original video file if you want and if you have the time to tinker with it.

@Erich: By the way, I've read about your computer photography technique that you're using at Fohr and I'm very curious about it. Care to elaborate a bit?

Sam,

I compressed a large animation yesterday with XVid, using a target quantizer of 3, and that really does not do much to the noise. It does however compress a 4Gb Fraps video to 800Mb. Note that fraps itself is also doing compression, unless you go for 'raw'.

- Jacco.

Hi Jacco, thanks for the tip. Will see if that works

On another note, there are strong rumors that Sony will soon buy either Olive or Gaikai. As a reaction Microsoft will likely buy the remaining one. If that would happen, I wonder what would happen with OTOY, at least for gaming.

The plot thickens...


seriously, you will find out in the coming months.

Nintendo still has a pile of cash, better add some Mario dolls cruising around.

Hi Sam,







I keep getting this error when I try to compile the brigade2 examples that come with the archive @ jacco's site.

fatal error C1047: The object or library file '..\release\framework.lib' was created with an older compiler than other objects; rebuild old objects and libraries

first off I tried VS9 and VS10, and both don't work.

I think it has to do with the dependencies glee.lib and brigade32.lib , that make up framework.lib.

do you know how to fix this?

Regards

Sam,


Just to be clear on one thing , you get this error when you try to build example 1,2 or 3, after you have built framework.lib without errors, the examples compile fine, but when it tries to link you get that error above.

Nicholas: Someone else had the same problem. A fresh install of VS2008 did the trick

Hi Sam,


VS 2008 or VS 2008 + SP1?

So it's VS 2008, and don't install SP1.

@Sam






So I got it to compile and link but now I get this error from Brigade and it crashes:

error :Failed to find cached CUDA kernel (sm20)the file(tracerCUDA_sm20.cubin) is not in the archive either , so I tried substituting it with some from jacco's demos but they don't work.

btw: your demos do work from your google code page.

The cubin file is not included in the Brigade package. You could email Jacco for an updated package.

Yes thanks Sam, I did just that.

*grrrrr*



It appears Vimeo is always re-encoding after all.

Having said that, x264 does have special settings for clips with lots of grain. Oh well.

@Nicholas,


I have the exact same problem, except mine says sm21 and then CUDA 301 under it.

Did you end up resolving this problem?

@Anon,


sm21 must be because you are using a gtx 6xx I figure, and to resolve this you need to contact Jacco.

Post a Comment
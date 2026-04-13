---
title: G-Buffer Normals, Revisited
url: http://hacksoflife.blogspot.com/2011/02/g-buffer-normals-revisited.html
author: Benjamin Supnik
published: '2011-02-04'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[G-buffer format](http://hacksoflife.blogspot.com/2010/12/yet-another-this-is-our-gbuffer-format.html)for X-Plane 10, which, as of this writing is still in development.

[SebH](http://sebh-blog.blogspot.com/)brought up CryTek's

[normal map compression](http://sebh-blog.blogspot.com/2010/08/cryteks-best-fit-normals.html)and I hand-waived a bit and wondered to myself whether some kind of normal map goblin was going to pop up later in the development cycle.

The short answer: yes.

I will try to write up a post later describing the precision problems with normal maps in more detail, but for now I'll post the problem and its partial solution, while I still have the debug code in my shaders.

![](../../assets/d5da80b0af8a5843.png)


![](../../assets/d5da80b0af8a5843.png)

![](../../assets/1279dd4ebe87c60e.png)


![](../../assets/1279dd4ebe87c60e.png)

This is a Baron 58 that Tom Kyler is working on for version 10. He is probably

*not*very happy that I'm posting pictures of it, because it's still in progress, and while I think it looks pretty good, our art guys get a lot of, um, "artsy goodness" into the models in the last few passes. (If the lighting seems a little, um, bizarre, it probably is; lord knows what state of debug the sun shader was in when I took these pics.)

The left side image is the airplane, lit by an evening sun that has just barely set, directly behind us, the right image is the fully reconstructed per pixel eye space normals. The small icons show the rough contents of the four layers of our G-Buffer.

So far things seem reasonably sane - the engine nacelle is lit from the side but not the top. But here's where things go south:

![](../../assets/0f782a25b9af3303.png)


![](../../assets/0f782a25b9af3303.png)

![](../../assets/b2f00d7396e13ec0.png)


![](../../assets/b2f00d7396e13ec0.png)

This is a wing with a light on the leading edge. The surface normal of the wing is almost perpendicular to the light direction, which really stress-tests the quality of our normal vectors. The first picture is the 'classic' G-Buffer technique: 16-bit-float dx and dy eye-space vectors, with Z reconstructed in shader. As you can see, it develops banding at the very low edge of angle-based attenuation. (Note that this area would be super-dark if we weren't in linear space.) The second image shows the full XYZ normal (burning an extra G-Buffer 16-bit channel)...clearly this fixes the problem of reconstruction from low-precision sources, but channels are hard to come by in gbuffers.

![](../../assets/1ae4f6c12cdd3f7a.png)


![](../../assets/1ae4f6c12cdd3f7a.png)

Fortunately I found this totally awesome write-up of different

[normal compression](http://aras-p.info/texts/CompactNormalStorage.html)schemes. The above picture on the right is a

[Lambert Azimuthal Equal-Area Projection](http://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection)using two channels.

Here are a few more pics of the gbuffer normal map, both projected and expanded:

![](../../assets/b4f31b12a193d246.png)


![](../../assets/b4f31b12a193d246.png)

![](../../assets/e81c7c7b379ce2ac.png)


![](../../assets/e81c7c7b379ce2ac.png)

![](../../assets/d9317bf24f50a636.png)


![](../../assets/d9317bf24f50a636.png)

![](../../assets/c9947b58275dc350.png)


![](../../assets/c9947b58275dc350.png)

Side benefit: Lambertian projection copes with negative eye space Z (but not 0,0,-1, which is unlikely even with tangent space normal maps on art assets) so no more hand-waving there.

One last thought for now: this entire post refers to the 'normal map' layer of a g-buffer, that is, the saved per-pixel normal information. Compression of 'normal map' textures for art assets is a bit of a different problem - the most immediate note is that they can be compressed off-line, so non-realtime compression techniques are fair game.

FYI, Crytek's best fit normals also don't have this problem of "negative view space Z" since they store all 3 components. They could as well be in world space if that's better suitable for you.


ReplyDeleteWhat BFN does is, it enables high quality normals using 8 bits/channel only; whereas usually 8 bits per channel is not really enough to have stable specular highlights.
---
title: CBox Unbiased Truck
url: http://raytracey.blogspot.com/2011/05/cbox-unbiased-truck.html
author: Sam Lapere
published: '2011-05-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/058680c8fa0b1760.png)


![](../../assets/058680c8fa0b1760.png)

I've modified


[the scene in the Kajiya path tracer](http://raytracey.blogspot.com/2011/05/real-time-path-traced-unbiased-trucker.html)a bit more: it now consists of a Cornell Box out of axis aligned boxes with the (in)famous truck from Unbiased Truck Soccer:![](../../assets/f701fdf1ba9633c1.png)


![](../../assets/f701fdf1ba9633c1.png)

Color bleeding from the red and green wall:

![](../../assets/3e3e2d255d88ea3e.png)


![](../../assets/3e3e2d255d88ea3e.png)

![](../../assets/fa69eb02bd664a4f.png)


![](../../assets/fa69eb02bd664a4f.png)

The screenshots were rendered with 8600M GT (6 fps default view). On a GTS 450, the demo runs at 70 fps in default view. It should run at >200 fps on a GTX 580 with 8 samples per pixel. This new path tracer is just incredible fun, I can't stop messing with it.


Executable and source code at

Executable and source code at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)UPDATE: a more challenging lighting set up with an open box only illuminated by the sky:

The truck seen from behind, indirectly lit by skylight bounced off the back and side walls. As expected with standard path tracing, the noise is a lot worse in this scenario. Bidirectional path tracing should converge faster using fewer samples.

## 8 comments:

G'day its radiant again,








Really enjoy reading your blogs :)

With the mirror exe, is it possible to increase the number of bounces in the scene.

EG: have an infinite number of reflections looking in the mirror.

.......................

Also,

I remember reading on an article about this algorithm that blurs out all unwanted grain/noise in real time gpu based rendering. It happens instantly and doesn't slow down the ray tracer. If this gets implemented into tokap, it will be revolutionary.

Thanks,

Radiant

~Michael

Hi,








yes, it's possible to increase the number of bounces by increasing the samples per pixel. Jacco Bikker has developed a novel way of implementing Russian Roulette. You can read about it here:

http://ompf.org/forum/viewtopic.php?f=6&t=3174#p24202

To increase the spp count, you must change the number of passes in the source code and recompile. If you have trouble compiling the source code, I'd be glad to help out. Some tips: use VC++2008 if possible, and download CUDA toolkit 32-bit even when you're on a 64-bit machine, you'll also need the 2010 version of cutil_math.h, the 2011 version doesn't have proper float4*float4 operator support. You can also add these lines to the 2011 version and it will work:

inline __host__ __device__ float4 operator*(float4 a, float4 b)

{

return make_float4(a.x * b.x, a.y * b.y, a.z * b.z, a.w * b.w);

}

inline __host__ __device__ void operator*=(float4 &a, float4 b)

{

a.x *= b.x; a.y *= b.y; a.z *= b.z; a.w *= b.w;

}

About the a-trous filter paper: I had already read it when it was published in May last year. While the results in the video and paper look impressive, it's only useful for blurring the noise on diffuse and glossy surfaces with low frequency textures, but doesn't work so well for specular surfaces. Nonetheless it's still worth implementing. There's some more info about the usefulness of this paper here:

http://ompf.org/forum/viewtopic.php?f=6&t=1723#p18918

Have fun compiling! Once you're able to successfully compile the source code, it's really fun changing scene elements, materials, skylight color and so on.

There's also a Pixar paper on reducing Monte Carlo noise in raytraced indirect illumination:



http://graphics.pixar.com/library/ShotRendering/paper.pdf

and a video: http://graphics.pixar.com/library/ShotRendering/Shotrender.mov

Hello,



I was wondering what your email/skype is. I have been getting trouble with compiling the engine and need some peer to peer walk thoughs, and also your knowledge in diving though the code.

Leave me a pm in the octane forum :)

Sorry if it is a bother for you.

Hi radiant. No problem at all, I'm glad to help and I'll send you a pm. I won't be able to help you right away though, since I'm currently travelling in the stunningly beautiful Canadian Rockies and only have sporadic internet access. But it's great to see someone's interested in this ;)

Nice, I hope you aren't using CUDA because Microsoft bought NVIDIA today and that means you'll need to rewrite it using DirectCompute or MR :D

Nope, Microsoft has not bought NVIDIA. It's just a deal to prevent a 3rd party to buy NVIDIA ( M$ will have rights to buy the stock 1st ), that's all.

Apparently, the agreement between Nvidia and MS is more than 10 years old, but it is kind of weird that Nvidia has brought it up again last week.

Post a Comment
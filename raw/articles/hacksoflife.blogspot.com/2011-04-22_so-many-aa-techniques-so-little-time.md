---
title: So Many AA Techniques, So Little Time
url: http://hacksoflife.blogspot.com/2011/04/so-many-aa-techniques-so-little-time.html
author: Benjamin Supnik
published: '2011-04-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Where does aliasing come from? It comes from decisions that are made "per-pixel", in particular (1) whether a pixel is inside or outside a triangle and (2) whether a pixel meets or fails the alpha test.

Texture filtering will not alias if the texture is mip-mapped; since the texel is pulled out by going "back" from a screen pixel to the texture, as long as we have mip-mapping, we get smooth linear interpolation. (See Texture AA below.)

### Universal Techniques

Super-Sampled Anti-Aliasing ([SSAA](http://en.wikipedia.org/wiki/Supersampling)). The oldest trick in the book - I list it as universal because you can use it pretty much anywhere: forward or deferred rendering, it also anti-aliases alpha cutouts, and it gives you better texture sampling at high anisotropy too. Basically, you render the image at a higher resolution and down-sample with a filter when done. Sharp edges become anti-aliased as they are down-sized.

Of course, there's a reason why people don't use SSAA: it costs a fortune. Whatever your fill rate bill, it's 4x for even minimal SSAA.

### Hardware FSAA Techniques

These techniques cover the entire frame-buffer and are implemented in hardware. You just ask the driver for them and go home happy - easy!Multi-Sampled Anti-Aliasing (

[MSAA](http://en.wikipedia.org/wiki/Multisample_anti-aliasing)). This is what you typically have in hardware on a modern graphics card. The graphics card renders to a surface that is larger than the final image, but in shading each "cluster" of samples (that will end up in a single pixel on the final screen) the pixel shader is run only once. We save a ton of fill rate, but we still burn memory bandwidth.

This technique does not anti-alias any effects coming out of the shader, because the shader runs at 1x, so alpha cutouts are jagged. This is the most common way to run a forward-rendering game. MSAA does not work for a deferred renderer because lighting decisions are made after the MSAA is "resolved" (down-sized) to its final image size.

Coverage Sample Anti-Aliasing (

[CSAA](ftp://download.nvidia.com/developer/SDK/Individual_Samples/DEMOS/Direct3D9/src/CSAATutorial/docs/CSAATutorial.pdf)). A further optimization on MSAA from NVidia. Besides running the shader at 1x and the framebuffer at 4x, the GPU's rasterizer is run at 16x. So while the depth buffer produces better anti-aliasing, the intermediate shades of blending produced are even better.

### 2-d Techniques

The above techniques can be thought of as "3-d" because (1) they all play nicely with the depth buffer, allowing hidden surface removal and (2) they all run during rasterization, so the smoothing is correctly done between different parts of a 3-d model. But if we don't need the depth buffer to work, we have other options.[Antialiased Primitives](http://glprogramming.com/red/chapter06.html#name2). You can ask OpenGL to anti-alias your primitives as you draw them; the only problem is that it doesn't work. Real anti-aliased primitives aren't required by the spec, and modern hardware doesn't support them.

[Texture Anti-Aliasing](http://homepage.mac.com/arekkusu/bugs/invariance/TexAA.html). You can create the appearance of an anti-aliased edge by using a textured quad and buffering your texture with at least one pixel of transparent alpha. The sampling back into your texture from the screen is done at sub-pixel resolution and is blended bilinearly; the result will be that the 'apparent' edge of your rendering (e.g. where inside your quad the opaque -> alpha edge appears) will look anti-aliased. Note that you must be alpha blending, not alpha testing.

If you're working in 2-d I strongly recommend this technique; this is how a lot of X-Plane's instruments work. It's cheap, it's fast, the anti-aliasing is the highest quality you'll see, and it works on all hardware. Of course, the limit is that this isn't compatible with the Z buffer. If you haven't designed for this solution a retro-fit could be expensive.

### Post-Processing Techniques

There are a few techniques that attempt to fix aliasing as a post-processing step. These techniques don't depend on what was drawn - they just "work". The disadvantages of these techniques are the processing time to run the filter iself (e.g. they can be quite complex and expensive) and (because they don't use any of the real primitive rendering information) the anti-aliasing can be a bit of a loose cannon.Morphological Anti-Aliasing (

[MLAA](http://www.realtimerendering.com/blog/morphological-antialiasing/)) and Fast Approximate Anti-Aliasing (

[FXAA](http://timothylottes.blogspot.com/2011/03/nvidia-fxaa.html)). These techniques analyze the image after rendering and attempt to identify and blur out stair-stepped patterns. ATI is providing an MLAA post-process as a driver option, which is interesting because it moves us back to the traditional game ecosystem where full screen anti-aliasing just works without developer input.

Edit: See also Directionally Localized Anti-Aliasing (

[DLAA](http://and.intercon.ru/releases/talks/dlaagdc2011/)).

(From a hardware standpoint, full screen anti-aliasing burns GPU cycles and sells more expensive cards, so ATI and NVidia don't want gamers to not have the option of FSAA. But most new games are deferred now, making MSAA useless. By putting MLAA in the driver, ATI gets back to burning GPU to improve quality, even if individual game developers don't write their own post-processing shader.)

It is not clear to me what the difference is between MLAA and FXAA - I haven't taken the time to look at both algorithms in detail. They appear to be similar in general approach at least.

Temporal Anti-Aliasing (

[TAA](http://en.wikipedia.org/wiki/Temporal_anti-aliasing)). This is a post process filter that blends the frame with the previous frame. Rather than have more samples on the screen (e.g. a 2x bigger screen in all dimensions for SSAA) we use the past frame as a second set of samples. The camera is moved less than one pixel between frames to ensure that we get different samples between frames. When blending pixels, we look for major movement and try to avoid blending with a sample that wasn't based on the same object. (In other words, if the camera moves quickly, we don't want ghosting.)

### Deferred-Rendering Techniques

This set of techniques are post-processing filters that specifically use the 3-d information saved in the G-Buffer of a deferred renderer. The idea is that with a G-Buffer we can do a better job of deciding when to resample/blur.Edge Detection and Blur. These techniques locate the edge of polygons by looking for discontinuities in the depth or normal vector of a scene, and then blur those pixels a bit to soften jaggies. This is one of the older techniques for anti-aliasing a deferred renderer - I first read about it in

[GPU Gems 2](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter09.html). The main advantage is that this technique is dirt cheap.

Sub-pixel Reconstruction Anti-Aliasing (

[SRAA](http://research.nvidia.com/publication/subpixel-reconstruction-antialiasing)). This new technique (published by NVidia) uses an MSAA G-Buffer to reconstruct coverage information. The G-Buffer is MSAA; you resolve it and then do a deferred pass at 1x (saving lighting) but then go back to the original 4x MSAA G-Buffer to edge detect.

About MLAA and FXAA: while the basic idea behind them is the same ("look for something that most likely is the edge and try to reconstruct it"), it seems that they achieve it with very different implementations (especially for something like FXAA II).




ReplyDelete"Classic MLAA" is the Intel paper with a quite slow CPU implementation; not directly applicable to GPUs. And then there are various takes on it. For example, Jimenez' at al approach from GPU Gems 2: http://www.iryoku.com/mlaa/ Sony's take on it (runs on SPUs in PS3) is somewhat different as far as I know. AMD's driver implementation likely to be different as well. So "MLAA" is quite vague term by now ;)

(btw, disadvantage of putting MLAA into the driver: there's no application control. Enable it and watch it destroy your 2D UI stuff!)

Andreev's DLAA should also be put into the gallery of MLAA-like approaches: http://and.intercon.ru/releases/talks/dlaagdc2011/

Thanks for the link...re: MLAA + driver, agreed, the GL is too abstract for the driver to know when a good time to anti-alias a deferred image might be. I liked that NV provides FXAA sample code in a portable shader. :-)


ReplyDeleteThere may be a continuum of heuristic post-processing edge-detection techniques...at some point where do we draw the line between a unique algorithm vs. heuristic tuning vs. constant tuning?
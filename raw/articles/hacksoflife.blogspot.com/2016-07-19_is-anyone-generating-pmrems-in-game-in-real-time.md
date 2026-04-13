---
title: Is Anyone Generating PMREMs In-Game in Real-Time?
url: http://hacksoflife.blogspot.com/2016/07/is-anyone-generating-pmrems-in-game-in.html
author: Benjamin Supnik
published: '2016-07-19'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of the standard solutions that has emerged for physically based rendering (PBR) is to use pre-filtered mipmapped radiance environment maps (PMREMs).


Put in very imprecise terms, a PMREM is a cube map that has a perfect reflection of the environment in the lowest (largest) mip and successively blurrier images in the lower mips. Typically the image is convolved with your material's distribution function at various roughnesses, and a cosine lobe is used at the lowest resolution.


From this, specular lighting is sampled from the LOD level that matches material roughness, and a low LOD is used for diffuse lighting.


What I haven't seen is any papers on games doing this entirely in-engine.


There's plenty written on


But the only work I've seen on real-time PMREMs is the old


The problem that X-Plane faces in adopting modern game-engine graphics is that we can't bake. Our "level" is the entire planet, and it is built out of user-installed scenery packages that can be mixed and matched in real-time. This includes adding a mix of surface objects onto a mesh from another pack. Baking is out the question because the final assembly of the level only exists when the user starts the app.


So I have been experimenting with both SH-based convolution of cube maps and simply importance sampling a distribution function on the GPU. It appears we're reaching the point where both of these can potentially function in real-time...at least, if you have a big GPU, a relatively low-res cube map (e.g. 256x256, not 1024x1024) and only one cube map.**


My question is: is anyone else already doing this? Is this a thing?




* You can add a lot more spherical harmonic coefficients, but it doesn't scale well in image quality; the amazing thing about SH are that the artifacts from having a very small number of bands are, perhaps by luck, very acceptable for low frequency lighting. The problem is that, as coefficients are added in, things get worse. The original image isn't reconstructed well (for the number of bands we can hope to use on a GPU) and the artifacts become significantly less desirable.


** To be clear: importance sampling is only going to work for a very, very small number of samples. I believe that for "tight" distributions it should be possible to find filter kernels that are equivalent to the importance-sampled result that can run in realtime. For very wide distributions, this is out of the question, but in that case, SH convolution might provide a reasonable proxy. What I don't know yet is what goes "in the middle". My guess is: some kind of incorrect and hacky but tolerable blend of the two.

Put in very imprecise terms, a PMREM is a cube map that has a perfect reflection of the environment in the lowest (largest) mip and successively blurrier images in the lower mips. Typically the image is convolved with your material's distribution function at various roughnesses, and a cosine lobe is used at the lowest resolution.

From this, specular lighting is sampled from the LOD level that matches material roughness, and a low LOD is used for diffuse lighting.

What I haven't seen is any papers on games doing this entirely in-engine.

There's plenty written on

[baking these cubemaps](https://seblagarde.wordpress.com/2012/06/10/amd-cubemapgen-for-physically-based-rendering/)ahead of time, and it appears that quite a few engines are augmenting PMREMs with screen space reflections (with various heuristics to cope with materials being rough and all of the weird things SSR can have).But the only work I've seen on real-time PMREMs is the old

[GPU Gems 2 chapter](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter10.html)that projects the original cube map into spherical harmonics (and then back into a cube map) as a way of getting a reasonable low frequency or diffuse cube map. But this was written back when a clean reflection and a diffuse map were good enough; it doesn't handle rough specular reflections at all.*The problem that X-Plane faces in adopting modern game-engine graphics is that we can't bake. Our "level" is the entire planet, and it is built out of user-installed scenery packages that can be mixed and matched in real-time. This includes adding a mix of surface objects onto a mesh from another pack. Baking is out the question because the final assembly of the level only exists when the user starts the app.

So I have been experimenting with both SH-based convolution of cube maps and simply importance sampling a distribution function on the GPU. It appears we're reaching the point where both of these can potentially function in real-time...at least, if you have a big GPU, a relatively low-res cube map (e.g. 256x256, not 1024x1024) and only one cube map.**

My question is: is anyone else already doing this? Is this a thing?

* You can add a lot more spherical harmonic coefficients, but it doesn't scale well in image quality; the amazing thing about SH are that the artifacts from having a very small number of bands are, perhaps by luck, very acceptable for low frequency lighting. The problem is that, as coefficients are added in, things get worse. The original image isn't reconstructed well (for the number of bands we can hope to use on a GPU) and the artifacts become significantly less desirable.

** To be clear: importance sampling is only going to work for a very, very small number of samples. I believe that for "tight" distributions it should be possible to find filter kernels that are equivalent to the importance-sampled result that can run in realtime. For very wide distributions, this is out of the question, but in that case, SH convolution might provide a reasonable proxy. What I don't know yet is what goes "in the middle". My guess is: some kind of incorrect and hacky but tolerable blend of the two.

I experimented with this in Overgrowth (sampling a distribution function on the GPU), and it worked fine! I ended up going with cached cube map chains because it's possible given the kind of levels we're dealing with, but it seems feasible to me.


ReplyDeleteIf you're updating every frame, maybe you could take advantage of temporal coherency by accumulating a smaller number of samples over the last few frames.

It's not that uncommon to do the pre-filtering dynamically. DICE discuss doing so in their SIGGRAPH 2014 presentation (http://www.frostbite.com/2014/11/moving-frostbite-to-pbr/ - see pages 65-68 in the course notes. They did a fast box filter followed by filtered importance sampling (http://cgg.mff.cuni.cz/~jaroslav/papers/2008-egsr-fis/2008-egsr-fis-final-embedded.pdf) to get the correct lobe shape. However, a much better approach was published at I3D this year ("Fast Filtering of Reflection Probes" by Josiah Manson and Peter-Pike Sloan). Unfortunately the authors haven't put a preprint online yet for some reason - I would try contacting them, or at worst buying it from the Eurographics Digital Library.

ReplyDeleteMason and Sloan's paper is apparently up:



Deletehttp://josiahmanson.com/research/ggx_filtering/ggx_filtering.pdf

and it's great -- they're somewhere between 2 and 3 steps ahead of me. My naive implementation uses importance sampling, which is (barely barely) viable for low roughness and small cube maps, ish.

My thought was to do the usual "stupid GL tricks" and precompute a sampling pattern for the distribution function that simultaneously leverages bilinear filtering hardware, corrects the cube map distortion, and avoids over-sample for very low roughness at the pole. It even occurred to me to precompute a cheap mip chain and use it to "gather" the long tail of GGX.

It looks like Manson and Sloan have done this, only with better chosen intermediate functions and a much more clever method for saving the sampling offset table.

I believe that Krzysztof Narkowicz from Flying Wild Hog mentioned that run-time specular probe generation was one of the use-cases for their real-time BC6H compressor:




ReplyDeletehttps://knarkowicz.files.wordpress.com/2016/03/knarkowicz_realtime_bc6h_gdc_2016.pdf

https://github.com/knarkowicz/GPURealTimeBC6H

You might want to try asking him about it on Twitter, his handle is @knarkowicz
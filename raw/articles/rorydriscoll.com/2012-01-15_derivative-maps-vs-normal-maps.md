---
title: Derivative Maps vs Normal Maps
url: https://www.rorydriscoll.com/2012/01/15/derivative-maps-vs-normal-maps/
author: Rory
published: '2012-01-15'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

This post is a quick follow up to my [previous post](http://www.rorydriscoll.com/2012/01/11/derivative-maps/) on derivative maps. This time I’m going to compare the quality and performance of derivative maps with the currently accepted technique, normal maps.

I’ll be using the precomputed derivative maps for comparison since the ddx/ddy technique just isn’t acceptable in terms of quality.

## Quality

Here’s the close up shot of the sphere with the moon texture again. This shows the derivative map implementation, and if you mouse over, you’ll see the normal map version.

![Moon texture comparison](../../assets/16b0e620bbbc88d3.png)


There are some slight differences because the height of the derivative map doesn’t quite match the heights used to precompute the normal map, but overall I would say that they are remarkably similar. It looks to me that the normal map is preserving more of the detail though.

Here’s a high-contrast checkerboard, again with the normal map shown if you mouse over.

![Checkerboard texture comparison](../../assets/33bfbb4567379f73.png)


I’m no artist, but I would say the the derivative map results are close enough to the normal maps to call the technique viable from a quality standpoint.

EDIT: I had some issues with artifacts which I posted here. It turns out they were (embarrassingly) caused by my mipmap generation which was introducing a row of garbage at each level. Combined with FXAA and anisotropic filtering, this caused the weird vertical stripes I posted before.
I’ve removed the images since I don’t want to give the wrong impression of the quality of derivative maps. |

## Performance

I ran these tests on my Macbook Pro which has an AMD 6750M. The shader in question is a simple shader for filling out the gbuffer render targets. All shaders were compiled using shader model 5. I took the frame times from the Fraps frame counter and the other numbers came from Gpu Perf Studio.

For comparison, I’ve included an implementation with no normal perturbation at all.

Perturbation |
Frame |
Pixels |
Tex Inst |
Tex Busy |
ALU Inst |
ALU Busy |
ALU/Tex |
|---|---|---|---|---|---|---|---|
| None | 1.08 ms | 262144 | 3 | 27.5 % | 14 | 32.1 % | 4.667 |
| Normal map | 1.37 ms | 262144 | 4 | 36.5 % | 23 | 52.4 % | 5.75 |
| Derivative map | 1.36 ms | 262144 | 9 | 82.0 % | 28 | 63.8 % | 3.11 |

Despite the extra shader instructions, the derivative map method is basically as fast as normal maps on my hardware. As Mikkelsen predicted, it seems like having one fewer vertex attribute interpolator offsets the cost of the extra ALU instructions.

Note that the derivative map shader has nine texture instructions compared to just four for the normal maps. The extra five instructions are the two sets of ddx/ddy instructions, and the instruction to get the texture dimensions. The pixel shader can issue one texture instruction and one ALU instruction on the same cycle, these are essentially free.

The only performance overhead which has any impact for derivative maps are the five extra ALU instructions.

## Memory

As I mentioned in my previous post, derivative maps also have the tremendous benefit of not requiring tangent vectors. In my case, with a simple vertex containing position, normal, tangent and one set of texcoords, the tangent takes up 27% of the mesh space.

Given that most games these days have tens of megabytes of mesh data, this would turn into some pretty decent memory savings. There’s also a minor benefit on the tool-side to not having to spend time generating face tangents and merging them into the vertices.

## Conclusion

Well, for me it’s pretty clear. On my setup, derivative maps have a similar quality with the same performance but less memory. This makes them a win in my book. Of course, these numbers will vary wildly based on the API and hardware, so this can’t be taken as a blanket ‘derivative maps are better than normal maps’ statement, but they look promising. Good job Morten Mikkelsen!

I would love to see a similar comparison for the current generation of console hardware (hint, hint!).

If you have DirectX 11, then you should be able to run the demo [here](http://www.rorydriscoll.com/wp-content/uploads/2012/01/DerivativeMaps.zip).

Have you tested on surfaces other than a flat plane? Also, with larger triangles?

Using ddx/ddy is going to give you a constant value across the whole triangle, right? Thus you should see faceting in the lighting which would look bad on low poly models.

The geometry here is actually a sphere. This method uses ddx/ddy purely to calculate a local space for projecting the gradient, not to interpolate the height derivative. Given that the technique doesn’t require a consistent local space, I don’t see this causing issues.

I certainly haven’t noticed any issues so far, but I haven’t tried any variety of models yet.

Great article !

source code or PerfStudio capture 🙂 ?

I have issues understanding the number of Tex inst: 4 with NM vs 9 with DM.

I would have thought that 3 tex fetches would have been enough to compute the gradient but it seems that you are using 6 of them.

I’m probably missign something here.

I did mention the number of texture instructions briefly in the post since I thought it might look a bit odd. To clarify, here are the instructions:

sample_indexable x 4: Diffuse, specular, gloss, derivative map

deriv_rtx_coarse x 2: Position, uv

deriv_rty_coarse x 2: Position, uv

resinfo_indexable x 1: Get the texture dimensions

The derivative map shader include is here, and the rest of the geometry pass shader is here

Regarding the silhouette issue you are seeing. Did you try and multiply the normal by the absolute value of the determinant instead of dividing the second term by it? This is also how it is done in the paper.

I did try that but it didn’t help. I’ve been using FXAA and anisotropic filtering, and once I took them off then the artifacts became much more pronounced.

I took a look at your demo Morten (which looks way better), and you’re using MSAA I believe. Did you try it without?

I don’t remember noticing any significant differences in that regard when disabling mssa. If you want to try it in the demo just comment out the code in the function ModifyDeviceSettings(). Assuming you have the June 2010 sdk installed then building the demo is super easy.

Just got back and tried running it without msaa. I am not seeing any issues here. I’ve made a precompiled binary available so you can try it assuming you haven’t yet:

http://dl.dropbox.com/u/55891920/bumpdemo_nomsaa.zip

I did try it, and didn’t really see any significant issues. I think that I can see some slight artifacts, but it’s barely noticeable.

I went through the shader debugger several times yesterday, and it does just seem to be that I have some pretty steep changes in normal, and the uv derivative gets pretty large on the edges.

I’ll have to see how toning down the bump scale affects it. I’m sure that the shader is correct, and the divide by determinant made no difference.

Okay,

I just thought I’d throw a few ideas out there.

I am noticing you seem to have a lot of details as we approach the silhouette edge. Are you sure the mip mapping is working properly?

Have you tried your setup in a non deferred setup just to try and simplify everything (no g-buffer)?

Do you have centroid sampling enabled?

Have you tried running your implementation on a different card/vendor?

Mip mapping is enabled and working for sure. I have anisotropic filtering enabled, so that’s possibly the cause of the extra details on the silhouettes. I’ll try disabling that for the derivative map when I get home.

I haven’t tried on a non-deferred setup, but I’ve been debugging the normal buffer output of the geometry pass (where the artifacts are clearly visible), so I don’t think this will help.

I’m not using centroid sampling, since I thought that was just used for MSAA. Is that not right?

I haven’t tried any different cards yet. I only have access to one DX11 machine!

Thanks for the tips. I’ll persevere and work out what’s causing this, since it’ll surely be something that others implementing the technique will need to address.

Failing everything I’m going to have to walk over to ND and collar you in person!

if you can setup your sample to just render the image you want at the resolution you want over and over again then I can take a screen-shot on the machine that I have here.

I’ve uploaded my binaries here. Hopefully this should work on any DirectX 11 machine.

Thank you. Could you also give me the texture and the object?

Morten.

for the mesh just obj and for the texture the .dds with whatever compression you are using in the demo.

The source assets are here. I build my runtime textures with no compression from the tga.

I’ve also included the height map I built the derivative map from.

ok, so when I run it through my own stuff I do get significantly better results.

http://dl.dropbox.com/u/55891920/results.zip

The details fade nicely as we approach the silhouette. However, if I position the poles of the sphere such that it’s at the silhouette this means the mip mapping will transcend far down the mip chain. And given that it’s a singularity and how distorted your mapping is at the poles I am not entirely surprised to see issues for this particular case since derivatives of all orientations will eventually “bleed in” as we go further down the mips. With self-occlusion off this issue becomes a little worse and that’s how I think you have it in your shader from what I can tell. I am however not able to produce any visual issues except for the two singularities on the sphere.

I don’t know why the filtering in your demo looks so much worse then it does in mine but it could be anisotropic. Also beware that current gen AMD gpus have pretty horrible filter quality for textures with less then 16 bits per channel –> http://jbit.net/~sparky/filt_issue/BC4_height_tex_bump.png

This is an extreme case of magnification where each texel covers about 256×256 pixels. It looks the same using 8 bits per channel. If you want to test this just convert your texture to 16 bits per channel and use that. If that doesn’t help then try disabling anisotropic filtering altogether.

Thanks a lot for the info. I’ll test out a different model when I get home for sure. Are you using parallax mapping to do the self occlusion?

I’ll definitely also try using 16 bit channels for the derivatives when I can. For now, I’ll edit the post to let new readers know that this is going on.

Either way, it looks like these artifacts are bugs in my implementation at the moment.

By self-occlusion I mean either using actual shadow mapping or shadow volumes or use the old-school cheesy hack when you don’t have shadows where you scale your bumped lighting by something like saturate(4*dot(vGeomNormal, vLightDir)) where vGeomNormal is the normalized interpolated vertex normal and vLightDir is of course the normalized direction towards the light. Specifically, this prevents things like specular high-lights from occurring on parts of the object that should be in shadow (just behind the silhouette typically).

Ah fair enough. Yes – shadows are on my todo list, and they would certainly help out with the noticeable issues on the back faces to the light. I still see them on the front faces, but, like you said, this could be one of many other factors.

What I have confirmed is that the vertical striping I show in the image is due to FXAA. If I turn it off, then I still get a few bright pixels, but they are no longer smeared like that.

No I didn’t mean to say that the issue goes away completely with self occlusion on. Just that it’s significantly reduced. As I was saying I think there are a series of issues in that demo. The singularities at the poles and the quality of the texture is one issue. But then you also have some issue with the filtering as far as I can tell because I am seeing too many details at the silhouette.

Derivative maps not only consume lessmemory than a non-compressed normal map, they also have two MASSIVE advantages: no seams and no mismatch between app’s TS.
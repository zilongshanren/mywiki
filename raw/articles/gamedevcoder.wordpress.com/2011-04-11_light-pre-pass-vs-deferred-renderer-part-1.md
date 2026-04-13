---
title: Light Pre-Pass vs Deferred Renderer – Part 1
url: https://gamedevcoder.wordpress.com/2011/04/11/light-pre-pass-vs-deferred-renderer-part-1/
published: '2011-04-11'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**My questions**

I have recently decided I want to spend some time experimenting with various approaches to renderers being used across PC and console games these days. In particular I wanted to look more closely at pros and cons of “traditional” Deferred with respect to Light Pre-Pass renderer which is slowly becoming more and more popular.

(1) What are the differences between the 2 approaches?

(2) What are the main limitations of each approach and what tricks do people do to workaround these?

These were my key questions which I can hopefully answer now, at least to some extent. If you just want to learn more about both techniques you may still find some useful information here.

**Quick intro**

Before I start I want to do a quick reminder on how each method works in a nutshell:

*“Standard” deferred shading* is a 2-stage process:

(1) draw (opaque) geometry storing its attributes (i.e. position as depth, normals, albedo color, specular color and other material properties) in a number of full screen buffers (typically 3 or 4)

(2) for each light source, draw its volume and accumulate lit surface color into final render target

I recommend you take a look at these great [Killzone 2 slides](http://www.slideshare.net/ozlael/deferred-rendering-in-killzone-2) for more detailed overview of sample deferred renderer implementation.

*Light pre-pass* is a 3-stage process:

(1) draw (opaque) geometry storing its attributes necessary for lighting (i.e. position as depth, normals and specular power)

(2) for each light source, draw its volume and accumulate just the lighting into an additional render target

(3) draw (opaque) geometry again; evaluate full material shader and apply lighting sampled from a buffer generated in step 2; this step is de facto forward shading

Read more on light pre-pass on [Wolfgang Engel’s blog](http://diaryofagraphicsprogrammer.blogspot.com/2008/03/light-pre-pass-renderer.html) or in his [presentation](http://www.bungie.net/images/Inside/publications/siggraph/Engel/LightPrePass.ppt). Also, take a look at this highly informative [presentation by Insomniac](http://cmpmedia.vo.llnwd.net/o1/vault/gdc09/slides/gdc09_insomniac_prelighting.pdf) from GDC’09.

**My answers**

Now that we know the basics, let’s go over each of my initial questions and try to give answers to each:

**(1) What is the key difference between the 2 approaches?**

*Number and cost of drawing stages*

The first obvious difference is that light pre-pass requires 3, not 2 stages. On one hand this sounds like more expensive because you have 2 geometry passes in light pre-pass instead of 1 in deferred shading but on the other hand both of these geometry passes are cheaper. In light pre-pass, the first geometry pass only outputs what’s necessary for lighting phase: depth, normals and optionally specular power. The second geometry pass (3rd stage) doesn’t typically need normals and it may take advantage of early z cull, including hierarchical z cull on some hardware – hence the depth has already been written. Unfortunately the first geometry pass isn’t going to be as fast as just a depth pre-pass, especially on hardware with support for double speed depth pass – this is because we also output normals and specular power. For this reason, with light pre-pass, it might even be worthwhile to use custom CPU/SPU based geometry occlusion system.

On the other hand light pre-pass has considerably lower bandwidth and memory requirements – no heavyweight 4-render-target output and sampling needed any more. In fact, light pre-pass might even be doable without [MRT](http://en.wikipedia.org/wiki/Multiple_Render_Targets) (only if you can read depth straight from depth buffer i.e. X360, PS3 or DX10/11).

There’s an interesting [post mortem](http://gameangst.com/?p=141) by one guy who implemented both light pre-pass and deferred renderers in their engine on 3 platforms: X360, PS3 and PC. He says he got better performance with deferred renderer mostly due to having single geometry pass.

*Material variety*

One of the benefits of light pre-pass is it gives you a bit more freedom in terms of material variety (compared to deferred shading). It means you can run different shader for each geometry and so, you can calculate final lit surface color differently. Instead of having single pass per light as in deferred shading, here we’re having single pass per mesh. Having said that, you’re still quite limited in terms of variety in lighting models because available lighting attributes have already been calculated (during 2nd pass) – these typically only include accumulated [Phong shading](http://en.wikipedia.org/wiki/Phong_shading) factors being N dot L and (R dot V) ^ SpecularPower (typically with light color and attenuation factors applied).

*MSAA*

Another nice feature of light pre-pass is that it works much better (again, compared to deferred shading) with MSAA. It’s still not going to be 100% correct MSAA (unless DX10/11 level features are used) because lighting buffer used in the last drawing pass won’t be sampled at MSAA’ed resolution (talking about light buffer sampler here). However, it’s fairly trivial to get MSAA’ed geometry with non-MSAA lighting which may yield pretty good results.

**(2) What are the main limitations of each approach and what tricks do people do to workaround these?**

*Transparency*

With both deferred shading and light pre-pass transparency is still typically done using old school forward shading after opaque geometry. There’s no efficient way around this, at least none that I know of.

*MSAA*

With deferred shading it’s become standard to use some kind of post-processing to smooth the edges. This can be as simple as finding edges based on depth and normals and blurring these – see GPU Gems 2 chapter on how they did it in [STALKER](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter09.html). Another popular, purely color based, approach to antialiasing is called Morphological Antialiasing (or just MLAA) – see [Realtime Rendering blog](http://www.realtimerendering.com/blog/morphological-antialiasing/) for more info. It’s even been added as an [on/off feature](http://www.tomshardware.com/reviews/radeon-hd-6870-radeon-hd-6850-barts,2776-4.html) to Radeon HD 6000-series cards and it’s also widely used on PS3 via its SPU processors. Other interesting color based antialiasing methods include [FXAA](http://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf) or [SRAA](http://research.nvidia.com/publication/subpixel-reconstruction-antialiasing). Now, as mentioned before, with light pre-pass we may just be able to stick with geometry-only-MSAA. Otherwise any of mentioned post-processing AA techniques still apply.

*Specular color in light pre-pass*

If you’re aiming at just using single light buffer, that means you have 4 attributes 3 of which are used for RGB components of the dot(N, L) * LightColor * LightAttenuation and so, you only have 1 left for specular lighting. Having 1 instead of 3 attributes we choose to just store single specular lighting [luminance](http://en.wikipedia.org/wiki/Luminance_(relative)) value (for example, luminance = 0.3 * R + 0.59 * G + 0.11 * B). But that means we loose specular lighting color which, if there’s non-white lights in the scene, may result in highly undesirable looks. Fortunately there’s this cool “trick” that let’s you reconstruct light color from diffuse lighting components. It’s not perfect as it only works correctly for a single light but it’s definitely better than nothing – see [Max’s Programming Blog](http://www.m4x0r.com/blog/2010/05/specular-color-in-light-pre-pass-renderer/) for a nice explanation of it.

*Materials / lighting models variety*

Both approaches are very limited in terms of material / lighting models variety. In a traditional forward renderer the shader had access to both light and material properties and so it could implement any kind of fancy material. In deferred renderer material properties are accessed first, then what the lighting pass gets is just fixed set of generic attributes (e.g. albedo color, specular color). Now, with light pre-pass, we have a bit different situation. One could say it’s even less flexible because we’re pretty much locked with Phong diffuse / specular shading model. Unfortunately, implementing something more complex like [Oren-Nayar](http://wiki.gamedev.net/index.php/D3DBook:(Lighting)_Oren-Nayar) isn’t easily doable with light pre-pass as is the case with any other “non-standard” material / lighting models.

The only way I can think of one could support multiple material / lighting models in their deferred renderer (doesn’t apply to light pre-pass) is by storing material id during the first pass in a G-buffer and then branching in a shader code based on its value. It may not be too bad performance wise due to coherency among samples but this means your shader code gets more complex (messy!) too. Neverthless, I think this could be quite a good approach to multiple material / lighting models.

That’s it for now. I feel like the more you investigate the topic the more difficult it is to choose the best approach for specific needs. I plan to discuss such choice dilemmas too in Part 2, stay tuned!

We have also “another type” of Deferred Shading. Let’s call it “Deferred Shading with Light Pre-Pass”

1) We output Geometry Properties

2) Do light pass in light accumulation buffer(s) like in Light Pre-Pass

3) Instead of drawing geometry seconds time we get Albedo from G-Buffer and applying lighting from light accumulation buffer.

This is how I am doing in my engine.

G-Buffer is:

MRT1 R- Depth GB- Compressed Normals A- Material ID

MRT2 R- YAlbedo G- YSpecular B- YEmissive A- Specular Power

MRT3 R- UVAlbedo G- UVSpecular B- UVEmissive A- Reflection Power

L-Buffer:

MRT1: Diffuser RGB

MRT2: Specular RGB

FXAA, SRAA are good, but quite expensive sometimes. There is another – GPAA. It’s here Quite good results, looks like MSAA 8x.

Hi Pavel,

Thanks for sharing!

(1) Yeah, I was thinking about this approach too at some point. I’d be interested to know how much faster it was for you compared to just a deferrer renderer if you had a chance to try both. I guess this should greatly depend on light overdraw – the more light overdraw, the better your method shall be compared to typical deferred renderer.

(2) GPAA indeed looks very interesting. I’d be curious to see how it compares performance wise to mentioned, purely post-processing, methods. My only worry is that it’s dependent on the geometry complexity but maybe it’s worth it – in the end this method eliminates need for hackish edge detection algorithms altogether.

This method(Deferred Shading with Light Pre-Pass) is not faster than traditional Deferred Shading. It’s easier to use different materials, but not really different: like in S.T.A.L.K.E.R. Clear Sky we take 3D texture with precomputed attributes and adds them to Ambient pass using Material ID.

My method is not really good because of two passes where we write to MRT’s.

That’s quite bad. Better method is(like in S.T.A.L.E.R. Clear Sky):

1) G-Buffer

(Direct3D9) – both RGBA16F

MRT1: Depth.R, Normals.GB, materialID.A

MRT2: Albedo.RGB, SpecularPower.A

(Direct3D9 with Depth Buffer hacks) – both RGBA16F

Depth from Depth-Stencil Buffer.

MRT1: Normal.RGB, materialID.A

MRT2: Albedo.RGB, SpecualarPower.A

(Direct3D10/Direct3D10.1/Direct3D11) – both different

Depth from Depth-Stencil Buffer.

MRT1: Normal.RGB, materialID.A (RGBA16F)

MRT2: Albedo.RGB, SpecualarPower.A (RGBA8)

2) L-Buffer

RT: DiffuseLight.RGB, MonochromeSpecular.A (RGBA8 or RGBA16F)

Also you can find paper about Frostbite 2 from DICE, where they use Deferred Shading. They discuss problems with antialiasing and how we can avoid them.

About Clear Sky you can find presentation “S.T.A.L.K.E.R. Clear Sky a showcase for Direct3D 10/Direct3D 10.1” [Lobanchikov]

Pingback: Real-Time Rendering · Seven Things for May 4th, 2011

Thought you might be interested in my experience of both techniques:

Some rudimentary tests here:

http://frictionalgames.blogspot.com/2010/10/pre-pass-lighting-redux.html

And the final choice and reasons here:

http://frictionalgames.blogspot.com/2010/12/bye-bye-pre-pass-lighting.html

Thomas:

I have just had a read through your blog posts. Very interesting stuff!

And yeah, as you pointed out, material variety in light pre-pass is actually very illusive because what largely defines material (in computer graphics) is how surface interacts with light. Unfortunately, with just N dot L and (R dot V) ^ SpecularPower (or even some other “fixed” light factors) accumulated in light buffer it’s not possible to construct very interesting and varied materials. I believe this is why traditional forward renderers in games will be in use for a long long time…

Someone needed to mention inferred lighting must well be me. Similar to the light prepass it collect lighting information but at lower resolution. The number of buffers used to collect the lighting information is 2 or even 1 like Red Faction; (RGB-Diffuse, A-Specular). It handles hardware antialias, and transparency antialias as well. To accomplish this it uses 16bits of information in one of the GBuffers.

Because it is at a lower resolutions it handles things like multiple lights very well, as well as full screen lighting effects light Z based ambient occlusion. Since it treats the transparency layers similar to the opaque layer it allows any shadow technique to be used even in the transparency polygons. However it does have some limitations.

When it comes to valance performance and quality of pixel and simplicity it does quite well. Better yet it works great on the XBOX ;-P

Cheers

Oren-Nayar is not hard to do with a light-prepass renderer. I’ve done it and am shipping a game with it. You just need to store roughness value somewhere. That’s it. And you can even derive the roughness value from specular power value most of the time.

If you are interested, here is a blog post about my implementation details.

Thanks, Pope!

I guess what I had in mind writing that Oren-Nayar is difficult to incorporate into light pre-pass renderer was that it’s problematic to combine it with simple Lambertian diffuse lighting i.e. shade some geometry using simple Lambertian N dot L and some other using more complex Oren-Nayar. If you’re fine shading _all_ of your geometry using Oren-Nayar, then that’s indeed possible to implement reasonably easily as described on your blog.

However, I was (silently) assuming one may not want to use more expensive lighting models for everything simply for performance reasons. Sorry for confusion.

Having said that, implementing combined Oren-Nayar with Lambertian lighting in your renderer is actually still possible with light pre-pass (for example using branching in a shader based on roughness value).
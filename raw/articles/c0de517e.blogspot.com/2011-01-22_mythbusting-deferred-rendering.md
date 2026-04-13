---
title: 'Mythbusting: deferred rendering'
url: http://c0de517e.blogspot.com/2011/01/mythbuster-deferred-rendering.html
published: '2011-01-22'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Today I want to write a bit about deferred rendering and its myths. Let's go...

**1) Is deferred good?**

Yes, deferred is great. Indeed, you should always think about it. If for "deferred" we mean doing the right computations in the right space... You see, deferred shading is "just" an application of a very general "technique". We routinely take these kind of decisions, and we should always be aware of all our options.

Do we do a separable, two-pass blur or a single pass one? Do we compute shadows on the objects or splat them in screen-space? What do I pass through vertices, and what through textures?

We always choose where to split our computation in multiple passes, and in which space to express the computation and its input parameters. That is fundamental!

Deferred shading is just the application of this technique to a specific problem: what we do if we have many analytic, lights in a dynamic scene? With traditional "forward" rendering the lights are constant inputs to the material shader, and that creates a problem when you don't know which lights will land on which shader. You have to start to create permutations, generate the same shader with support of different number of lights, then at runtime see how many lights influence a given object and assign the right shader variant... All this can be complicated, so people started thinking that maybe having lights as shader constants was not really the best solution.

Bear with me. Let's say that you have a forward renderer that does assign lights to objects, it's working but you're fed of it. You might start noticing that it works better if the objects are not huge and you can cap the maximum number of lights per object. In theory, the finer you can split your objects the best, you don't have too many lights overlapping a given pixel, maybe 3/4 maximum, but when the objects are large compared to the lights area of influence things start to be painful.

What would you start thinking? Wouldn't it be natural to think that maybe you can write the indices of the lights somewhere else, not in the pixel shaders constants? Well, you might think to write some indices to your lights in the pixels... here it comes the

[Light-Indexed Deferred Rendering](http://lightindexed-deferredrender.googlecode.com/files/LightIndexedDeferredLighting1.1.pdf).
Let's say on the other hand that in your forward renderer you really hated to create multiple shaders to support different numbers of lights per object. So you went all multipass instead. First you render all your objects with ambient lighting only, then for each extra light you render the object with additive blending feeding as input that light.

It works fine but each and every time you're executing the vertex shader again, and computing the texture blending to multiply your light with the albedo. As you add more textures, things really become slow. So what? Well, maybe you could write the albedo out to a buffer and avoid computing it so many times. Hey! Maybe I could write all the material attributes out, normals and specular. Cool. But now really I don't need the original geometry at all, I can use the depth buffer to get the position I'm shading, and draw light volumes instead. Here it comes, the standard deferred rendering approach!

So yes, you should think deferred. And make your own version, to suit your needs!

*p.s. it would have been better probably to call deferred shading "image-space shading". It's all about the space the computations happen into. What will we call our rendering the day we combine virtual texture mapping (clipmaps, megatextures or what you wanna call them) with the idea of baking shading in UV space?*

[Surface caching](http://www.bluesnews.com/abrash/chap68.shtml), I see. Well it's ok, nowadays people call globals "singletons" and pure evil "design patterns", you always need to come up with cool names.**2) Deferred is the only way to deal with many lights.**

Well if you've read what I wrote above you already know the answer. No :)

Actually I'll go further than that and say that nowadays that the technique has "cooled down" there is no reason for anyone to be implementing pure deferred renderers. And if you're doing deferred chances are that you have a multipass forward technique as well, just to handle alpha. Isn't that foolish? You should at the very least leverage it on objects that are hit by a

[single light](http://www.eurogamer.net/articles/digitalfoundry-halo-reach-tech-interview)!
And depending on your game multipass on everything can be an option, or generating all the shader permutations, or doing a hybrid of the two, or of the three (with deferred thrown in too). Or you might want to defer only some attributes and not others, work in different spaces...

But it's not only about this kind of optimizations. You should really look at your game art and understand what its the best space to represent your lights. The latest game I shipped defers only SSAO and shadows, and I experimented with many different forms of lighting, from using analytic to spherical bases to cubemaps. And it ends up using a mix of everything...



**3) Deferred is an alternative to light maps.**

Not really.

Many artists came to me thinking that deferred is the future because it allows you to place lights in realtime. Well I'm telling you, with CUDA, distributed processing and so forth, if your lightmap generation is taking ages and your artists can't have decent feedback, it's a problem of your tools, not really of the lightmap technique per se.

Also deferred handles a good number of lights only if they are unshadowed point lights. So either you get a game that looks like some bad phong-shiny

[3d studio](http://www.youtube.com/watch?v=V7Lp0iv_HqY)[4 dos](http://image60.webshots.com/60/2/7/32/2906207320093815875IqpPIX_ph.jpg), rendering or your artists have to start placing a lot of lights with "cookies" to fake GI (and back to the 90ies we are).
Or we will need better realtime GI alternatives... like

[computing light maps in realtime](http://www.geomerics.com/products.htm)... Still, they are not bad, for static scenes or the static part of your scene light maps still make a lot of sense and they will always do as they are an expression of another of these general techniques: precomputation a.k.a. trading space for performance.**4) Deferred shading is slower than deferred lighting (a.k.a. light prepass).**

Depends. The usual argument here is that deferred shading requires more memory than deferred lighting, thus more bandwidth, thus it's slower because deferred is bandwidth limited. It turns out that's a mix of false statements with some questionable ones.

First, it's false that deferred shading uses considerably more memory. Without going into too many details, usually deferred shading engines use four RGBA8 rendertargets plus the depth, plus a rendertarget to store the final shaded stuff. Deferred lighting needs at least a RGBA8 (normals and specular exponent) plus depth for lighting. Lighting needs to be stored into two RGBA8 to have comparable quality (some squeeze this into a single RGBA8, some use two RGBA16, it really depends on what's the dynamic range of your lights), plus you need the buffer for the final rendered stuff. So it's basically 6 32bit buffers versus 5, not such a huge difference.

Second, more memory does not imply more bandwidth. And here is where things start to be variable. Both methods are basically overdraw free in the "attribute writing" passes, as you can sort your objects front to back and use a bit of z-prepass (or even a full one if you want to compute SSAO or shadows in screenspace at that point). The geometry pass in the deferred lighting is also basically overdraw free (as the hi-z has been already primed). So what it really matters is the lighting pass. Now if you have a lot of overdraw there, you are in danger. You can decide if to be bottlenecked in the blend stage (i.e. on ps3 with deferred lighting) or in the texture one (deferred shading). Or you can decide to do the right thing and do the "

[tiled" variant](http://visual-computing.intel-research.net/art/publications/deferred_rendering/)of deferred rendering.

Last but not least, deferred might not be actually be bandwidth limited. I've seen more than one engine where things were actually ALU bound. And I've seen more than one engine struggling with vertex shading, thus being limited by the two geometrical passes deferred lighting has.

And I'm

[not alone](http://gameangst.com/?p=141), in the end it really depends on your scene, on your platform and your bottlenecks. Deferred lighting is an useful technique but it's not a clear winner over deferred shading or any other technique.


**5) Deferred lighting can express better materials than deferred shading.**

Nah, not really. It's true that you have a second geometry pass where you can pass per vertex attributes and do some magic, but it turns out that the amount of magic you can perform with the lights already computed and fixed to the phong model is really little. Really little.

Also consider that deferred lighting works with a fundamental flaw, that is blending together specular contributions. It also in many implementations allow only for monochromatic "specular light".

Now there are some lighting hacks that work better with deferred lighting and some others that work better with deferred shading but in general both techniques decouple lights from objects "too late". They do it at the material parameter level, that's to say deep into the BRDF. In the end all your materials will use the very same shading model, minus some functions applied to it via lookup tables.

To the opposite end it the light-indexed technique, that decouples lighting from materials as "early" as possible, that's to say at the light attribute fetching stage. Can something be in a middle ground between the two? Maybe we could encode the lights in a way that still allows BRDF processing without needing to fetch the single analytical light attributes and integrate them one at a time? Maybe we could store the radiance instead of the irradiance... Maybe in a SH? I've heard a few discussions over this and it's in general impractical but recently Crytek managed to do something related to this in the

[cryEngine 2](http://advances.realtimerendering.com/s2010/Kaplanyan-CryEngine3%28SIGGRAPH%202010%20Advanced%20RealTime%20Rendering%20Course%29.pdf)to express anisotropic materials.**6) Deferred lighting works better with MSAA.**

Yes. Sort-of.

If you don't write per sample attributes, all deferred techniques really do not work with MSAA if you don't use some care when fetching the screen space attributes, that might be a bilateral filter, the "

[inferred lighting](http://www.google.ca/url?sa=t&source=web&cd=2&sqi=2&ved=0CCwQFjAB&url=http%3A%2F%2Fgraphics.cs.uiuc.edu%2F%7Ekircher%2Finferred%2Finferred_lighting_paper.pdf&rct=j&q=inferred%20lighting&ei=DL87Ta-SJpSosQObhPSpAw&usg=AFQjCNHHIkB3fdOwrVwa-IQzbmK-zkBH9A&cad=rja)" discontinuity filter or other solutions. This ends up to be the "preferred way" of doing MSAA and it's applicable to everything. And many nowadays do not MSAA at all and do a postfilter, like MLAA, instead.
Even if you just do shadows in screen space, as for example the first Crysis does, you will end up with aliasing if you don't filter (and crysis does, but the shadow discontinuities are not everywhere in the scene so it's ok-ish).

Now with DirectX 10.1 or with some advanced trickery on previous APIs you can read individual MSAA samples and decide where to compute shading per sample (instead of per pixel). That means that you will need to store all the samples in memory and keep them around for the lighting stage, as these attributes are not colors, can't be blended together in a meaningful way.

This enables you to compute and read per-sample attributes at discontinuities, and this is where deferred lighting has an advantage, as the attributes that go into the lighting stage are packed in just a single buffer so storing them per-sample requires the same amount of memory as your final buffer (and in fact it can be shared with your final buffer, as you won't need these after the lighting stage), and the lighting buffer can be MSAA-resolved as lighting will blend properly.

Doing the same with deferred shading would be a bit crazy, as you would need to store per-sample attributes of four buffers. It is possible even if really not too good to do a "manual" MSAA-resolve on the G-Buffer (thus not keeping all the samples for the lighting stage) where you do standard MSAA averaging for the albedo and use the "nearest" (to the camera) sample for the rest and it somewhat works.



To close this article, I'll put here some tips and less talked about things about deferred techniques. One advantage of both deferred lighting and shading is that you get cheap decals (both "volumetric" and "standard" ones) as you don't have to compute lighting multiple times, the decals lie on a surface, so you can fetch the lighting you've already computed for it.

That of course means that the decal will need to change the surface's normals if needed blending its own, so you don't really get two separate and separately lit layers but it's still a great way to add local detail without multitexturing the whole surface...

If you think about it a second, it's the very same advantage you have with lights, you don't need to assign them per mesh thus potentially wasting computations on parts of the mesh that are not lit by a given light or need to split the mesh in complicated ways.


Also, it is neat to be able to inject some one-pixel "probes" in the gbuffer here and there, and have lighting computed on them "for free" (well... cache trashing and other penalties aside) for particles, transparencies and other effects, i.e. see the work


Another advantage that is especially relevant today (with tessellation...), is that you can somehow lessen the problem of non full pixel quads generated by small triangles (and the absence of quad fusion on GPUs). This is especially true of deferred shading, as it employs a single gbuffer pass that is taxing on bandwidth but less on processing (or... it could be that way). In deferred lighting you can achieve a nearly perfect culling (i.e. with occlusion queries generated during the first gbuffer pass) and zero overdraw in the second geometry pass, but you still have the quad problem...


Which unfortunately, will also affect what

**Update: What they don't want you to know! :)**To close this article, I'll put here some tips and less talked about things about deferred techniques. One advantage of both deferred lighting and shading is that you get cheap decals (both "volumetric" and "standard" ones) as you don't have to compute lighting multiple times, the decals lie on a surface, so you can fetch the lighting you've already computed for it.

That of course means that the decal will need to change the surface's normals if needed blending its own, so you don't really get two separate and separately lit layers but it's still a great way to add local detail without multitexturing the whole surface...

If you think about it a second, it's the very same advantage you have with lights, you don't need to assign them per mesh thus potentially wasting computations on parts of the mesh that are not lit by a given light or need to split the mesh in complicated ways.

Also, it is neat to be able to inject some one-pixel "probes" in the gbuffer here and there, and have lighting computed on them "for free" (well... cache trashing and other penalties aside) for particles, transparencies and other effects, i.e. see the work

[Saints Row 3 did](http://www.volition-inc.com/publications/lighting-and-simplifying-saints-row-the-third/).Another advantage that is especially relevant today (with tessellation...), is that you can somehow lessen the problem of non full pixel quads generated by small triangles (and the absence of quad fusion on GPUs). This is especially true of deferred shading, as it employs a single gbuffer pass that is taxing on bandwidth but less on processing (or... it could be that way). In deferred lighting you can achieve a nearly perfect culling (i.e. with occlusion queries generated during the first gbuffer pass) and zero overdraw in the second geometry pass, but you still have the quad problem...

Which unfortunately, will also affect what

## 6 comments:

I have to agree with you on point #3...there seems to be a disturbing trend of games foregoing any kind prebaked GI in favor of faking it with lots of deferred lights and nasty hacks like SSAO. I helped my coworker develop a GI baker in CUDA that uses PRT for real-time preview/light tweaking, and even with totally unoptimized code it can finish a complex scene in a few minutes on an older consumer-level GPU. It seems a lot of people just no longer want to deal with the complexity of researching, implementing, and maintaining such a system.


Also with regards to #6...you can't resolve an MSAA lighting buffer prior to sampling it in the final pass. It will cause artifacts for pixels where 1 or more triangles only cover a fraction of subsamples. During the final pass you also need to avoid sampling subsamples of the lighting pass buffer that don't "belong" to the triangle being rasterized, either by running the shader at per-sample frequency or by using SV_Coverage in D3D11.

MJP: Is just that some people just go with the latest trend, they switch their brain off and not think that every new technique is a tool in your arsenal but it's still up to you to use the right tools in the right places.

MJP: About #6 I agree that it's not really correct (at all) but I've seen that done and mhm I might be fuzzy on this but I think it does produce something reasonable.

"So it's basically 6 32bit buffers versus 5, not such a huge difference."






Ummm... Can you go into detail on how you would lay out your buffers for light prepass?

As far as I can tell light prepass requires only one additional buffer - the light accumulation buffer - over forward rendering. Total is light buffer, final/normal buffer, depth buffer = 3 (or 4 if you need more light precision).

Since the normals/specpower are not needed after the light prepass, they can share the final buffer. Normals can be rendered into the final buffer, light buffer calculated, then normals overwritten in the final pass with the final color.

Also, light prepass avoids the annoyances associated with MRTs.

Why would anyone use deferred shading, again? :)

Steve: you're not going far with an 8bit light buffer, you need at least 16 or two 8 bits (diffuse and specular), i've seen games shipping with two 16 bits... So that counts for two. Also i was reasoning about bandwidth so i did not count the fact that you can save memory by shring buffs, as that won't reduce bandwidth. And i wrote it clearly in the post i think. Also i can see still a few reasons to go deferred shading, it really depends on the kind of game you're doing and how are your lights vs geometry. A game for example with dense geometry and dunno, the need to do cool decals in the gbuffer will work way better with deferred shading. Also i don't love the fact that the specular is fundamentall wrong in deferred lighting bu i didn't stud in depth was kind of visual defects that leads to

Wrt #4, deferred lighting has to perform another vertex transform pass that happens regardless of Hi-Z, which can be expensive especially if its not a simple ModelViewProj transform. However, an advantage on some platforms is the second (colour) pass can be predicated on the visibility result of the first (depth) pass if things are drawn in the correct order.


Clustered lighting is also pretty cool as it works equally well for forward or deferred passes, but it does have a significant CPU overhead with sorting and "bucketing" a large number of lights if done in view-space.

Post a Comment
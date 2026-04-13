---
title: Hair rendering trick(s)
url: https://bartwronski.com/2014/07/20/hair-rendering-tricks/
published: '2014-07-20'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

I didn’t really plan to write this post as I’m quite busy preparing for Siggraph and enjoying awesome Montreal summer, but after 3 similar discussion with friends developers I realized that the simple hair rendering trick I used during the prototyping stage at CD Projekt Red for Witcher 3 and Cyberpunk 2077 (I have no idea if guys kept that though) is worth sharing as it’s not really obvious. It’s not about hair simulation or content authoring, I’m not really competent to talk about those subjects and it’s really well covered in [AMD Tress FX](http://developer.amd.com/tools-and-sdks/graphics-development/graphics-development-sdks/amd-radeon-sdk/) or [nVidia HairWorks](https://developer.nvidia.com/hairworks) (plus I know that lots of game rendering engineers work on that topic as well), so check them out if you need awesome looking hair in your game. The trick I’m going to cover is to improve quality of typical alpha-tested meshes used in deferred engines. Sorry, but no images in this post though!

## Hair rendering problems

There are usually two problems associated with hair rendering that lot of games and game engines (especially deferred renderers) struggle with.

- Material shading
- Aliasing and lack of transparency

First problem is quite obvious – hair shading and material. Using standard Lambertian diffuse and Blinn/Blinn-Phong/microfacet specular models you can’t get proper looks of hair, you need some hair specific and strongly anisotropic model. Some engines try to hack some hair properties into the G-Buffer and use branching / material IDs to handle it, but as recently [John Hable wrote in his great post about needs for forward shading ](http://www.filmicworlds.com/2014/05/31/materials-that-need-forward-shading/)– it’s difficult to get hair right fitting those properties into G-Buffer.

I’m also quite focused on performance, love low-level and analyzing assembly and it just hurts me to see branches and tons of additional instructions (sometimes up to hundreds…) and registers used to branch for various materials in the typical deferred shading shader. I agree that the performance impact can be not really significant compared to bandwidth usage on fat GBuffers and complex lighting models, but still it’s the cost that you pay for whole screen even though hair pixels don’t occupy too much of the screen area.

One of tricks we used on The Witcher 2 was faking hair specular using only dominant light direction + per character cube-maps and applying it as “emissive” mesh lighting part. It worked ok only because of really great artists authoring those shaders and cube-maps, but I wouldn’t say it is an acceptable solution for any truly next-gen game.

Therefore hair really needs forward shading – but how to do it efficiently and not pay the usual overdraw cost and combine it with deferred shading?

### Aliasing problem.

A nightmare of anyone using alpha-tested quads or meshes with hair strands for hair. Lots of games can look just terrible because of this hair aliasing (the same applies for foliage like grass). Epic proposed to [fix it by using MSAA](http://udn.epicgames.com/Three/rsrc/Three/DirectX11Rendering/MartinM_GDC11_DX11_presentation.pdf), but this definitely increases the rendering cost and doesn’t solve all the issues. I tried to do it using alpha-to-coverage as well, but the result was simply ugly.

Far Cry 3 and some other games used screen-space blur on hair strands along the hair tangenta and it can improve the quality a lot, but usually end parts of hair strands either still alias or bleed some background onto hair (or the other way around) in non-realistic manner.

Obvious solution here is again to use forward shading and transparency, but then we will face other family of problems: overdraw, composition with transparents and problems with transparency sorting. Again, AMD Tress FX solved it completely by using order-independent transparency algorithms on just hair, but the cost and effort to implement it can be too much for many games.

## Proposed solution

The solution I tried and played with is [quite similar to what Crytek described that they tried in their GDC 2014 presentation](http://www.crytek.com/download/2014_03_25_CRYENGINE_GDC_Schultz.pdf). I guess we prototyped it independently in similar time frame (mid-2012?). Crytek presentation didn’t dig too much into details, so I don’t know how much it overlaps, but the core idea is the same. Another good reference is [this old presentation ](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Scheuermann_HairRendering.pdf)from Scheuermann from ATI at GDC 2004! Their technique was different and based only on forward shading pipeline, not aimed to combined with deferred shading – but the main principle of multi pass hair rendering and treating transparents and opaque parts separately is quite similar. Thing worth noting is that with DX11 and modern GPU based forward lighting techniques it became possible to do it much easier. 🙂

Proposed solution is a hybrid of deferred and forward rendering techniques to solve some problems with it. It is aimed for engines that still rely on hair alpha tested stripes for hair rendering, have fluent alpha transition in the textures, but still most of hair strands are solid, not transparent and definitely not sub-pixel (then forget about it and hope you have the perf to do MSAA and even supersampling…). You also need to have some form of forward shading in your engine, but I believe that’s the only way to go for the next gen… [Forward+](https://diglib.eg.org/EG/DL/conf/EG2012/short/005-008.pdf.abstract.pdf)/[clustered shading](http://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf) is a must for material variety and properly lit transparency – even in mainly deferred rendering engines. I really believe in advantages of combining deferred and forward shading for different rendering scenarios within a single rendering pipeline.

Let me describe first proposed steps:

- Render your hair with full specular occlusion / zero specularity. Do alpha testing in your shaders with value Aref close to 1.0. (Artist tweakable).
- Do your deferred lighting passes.
- Render forward pass of hair speculars with no alpha blending, z testing set to “equal”. Do the alpha testing exactly like in step 1.
- Render forward pass of hair specular and albedo for hair transparent part with alpha blending (scaled from 0 to Aref to 0-1 range), inverse alpha test (1-Aref) and regular depth test.

This algorithm assumes that you use regular Lambertian hair diffuse model. You can easily swap it, feel free to modify point 1 and 3 and first draw black albedo into G-Buffer and add the different diffuse model in step 3.

### Advantages and disadvantages

There are lots of advantages of this trick/algorithm – even with non-obvious hair mesh topologies I didn’t see any problems with alpha sorting – because alpha blended areas are small and usually on top of solid geometry. Also because most of the rendered hair geometry writes depth values it works ok with particles and other transparents. You avoid hacking of your lighting shaders, branching and hardcore VGPR counts. You have smooth and aliasing-free results and a proper, any shading model (not needing to pack material properties). It also avoids any excessive forward shading overdraw (z-testing set to equal and later regular depth testing on almost complete scene). While there are multiple passes, not all of them need to read all the textures (for example no need to re-read albedo after point 1 and G-Buffer pass can use some other normal map and no need to read specular /gloss mask). The performance numbers I had were really good – as hair covers usually very small part of the screen except for cutscenes – and proposed solution meant zero overhead/additional cost on regular mesh rendering or lighting.

Obviously, there are some disadvantages. First of all, there are 3 geometry passes for hair (one could get them to 2, combining points 3 and 4, but getting rid of some of advantages). It can be too much, especially if using some spline/tessellation based very complex hair – but this is simply not an algorithm for such cases, they really do need some more complex solutions… Again, see Tress FX. There can be a problem of lack of alpha blending sorting and later problems with combining with particles – but it depends a lot on the mesh topology and how much of it is alpha blended. Finally, so many passes complicate renderer pipeline and debugging can be problematic as well.


## Bonus hack for skin subsurface scattering

As a bonus description how in a very similar manner we hacked skin shading in The Witcher 2.

We couldn’t really separate our speculars from diffuse into 2 buffers (already way too many local lights and big lighting cost, increasing BW on those passes wouldn’t help for sure). We didn’t have ANY forward shading in Red Engine at the time as well! For skin shading I really wanted to do SSS without blurring neither albedo textures nor speculars. Therefore I came up with following “hacked” pipeline.

- Render skin texture with white albedo and zero specularity into G-Buffer.
- During lighting passes always write specular not modulated by specular color and material properties into the alpha channel (separate blending) of lighting buffer.
- After all lights we had diffuse response in RGB and specular response in A – only for skin.
- Do a typical
[bilateral separable screen space blur (Jimenez)](http://www.iryoku.com/sssss/)on skin stencil-masked pixels. For masking skin I remember trying both 1 bit from G-Buffer or “hacking” test for zero specularity/white albedo in the G-Buffer – both worked well, don’t remember which version we shipped though. - Render skin meshes again – multiplying RGB from blurred lighting pixels by albedo and adding specularity times the specular intensity.

The main disadvantage of this technique is losing all specular color from lighting (especially visible in dungeons), but AFAIK there was a global, per-environment artist specified specular color multiplier value for skin. A hack, but it worked. Second, smaller disadvantage was higher cost of SSS blur passes (more surfaces to read to mask the skin).

In more modern engines and current hardware I honestly wouldn’t bother, do separate lighting buffers for diffuse and specular responses instead, but I hope it can inspire someone to creatively hack their lighting passes. 🙂

## References

[5] h[ttps://developer.nvidia.com/hairworks ](https://developer.nvidia.com/hairworks)

[6] “Forward+: Bringing Deferred Lighting to the Next Level” Takahiro Harada, Jay McKee, and Jason C.Yang [https://diglib.eg.org/EG/DL/conf/EG2012/short/005-008.pdf.abstract.pdf](https://diglib.eg.org/EG/DL/conf/EG2012/short/005-008.pdf.abstract.pdf)

[7] “Clustered deferred and forward shading”, Ola Olsson, Markus Billeter, and Ulf Assarsson [http://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf](http://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf)

[8] “[Screen-Space Perceptual Rendering of Human Skin](http://www.iryoku.com/sssss/)“, Jorge Jimenez, Veronica Sundstedt, Diego Gutierrez

[9] “[Hair Rendering and Shading](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Scheuermann_HairRendering.pdf)“, Thorsten Scheuermann, GDC 2004

Interested in how you handled DOF and the transparent bits of hair. I came up with a similar solution to Ryse, but the assets I was working with had a lot of transparency so it ended up with “focus halos” where the alpha blended depth/coc would be more in-focus (but still blurry) than the background. From their slides, their hair is vary coarse/opaque so works ok. You can see some of the focus halo artifacts in the hair tips and eyebrows.

Unfortunately I didn’t test it with DOF. 😦 But I agree that it would be a problem – but just like every transparents have problem with DOF. Anyway the method I propose works on the assumption of transparent bits being significantly smaller than the opaque parts – other way it will break on order dependency and lack of sorting.

One solution to transparents and DOF is composing them after the opaque DOF. We actually used it for rain DOF in AC4 – OOF rain was rendered into offscreen buffers, blurred /stretched during drawing and then later composed with the main scene after DOF PP. It was proposed in Epic’s Samaritan Demo presentation as well – although it can cause different kinds of problems – trade-off of one kind of artifacts for other kind of artifacts (depending on the rendering pipeline, how many transparents there are etc.) as always… The problem is in both lack of OIT and in the way fake PP DOF works. 🙂

🙂 Yeah, I ended up compositing after DOF for in-focus hair as well, which feels like a giant hack. Ready for when I can just ray-trace DOF. 🙂

Hi, you said “combining points 3 and 4, but getting rid of some of advantages”. Could you be more specific?

I wrote that post 6 years ago, so now some details seem fuzzy, but I *believe* it was an idea to do all post-deferred hair as combined alpha blended depth test only and less-equal, with a branch depending on depth equality.

Disadvantage is potential massive overdraw, having to branch your shaders.

Note that the post has dated pretty badly – now everyone seems to be doing very fat gbuffers and modern GPUs are great at branching (especially in a tiled setup with coherent tile properties and specialized shader variations) with flags controlling things like special specular so most of this tedious setup is unnecessary. Valuable and still relevant is doing the alpha test and inverse alpha test trick with hair split as opaque vs transparent.

Thanks for you reply. I’m looking for a solution to resolve order problem of translucency hair rending in mobile. And balance efficiency and effectiveness, two passes hair rendering is a good solution.For a forward engine in mobile, do this maybe much sampler than deferred engine. Thanks for reply again.Your blog is valueable.

Thank you so much! Comments like this make my day and encourage me to keep posting. 🙂
---
title: Normalmaps everywhere
url: http://c0de517e.blogspot.com/2012/02/normalmaps-everywhere.html
published: '2012-02-01'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

You are modeling a photorealistic face. Your artists want to be able to have detail, detail detail. Skin pores. Sweat droplets. Thin wrinkles. What do you do?

If your answer is to give them high-res normalmaps and some cool, sharp specular, think twice.

Normalmaps are not about thin, very high frequency detail! Especially NOT when rendered by our current antialiasing techniques.

Let's think about a high fidelity model for example, millions of triangles. It's too expensive to render it in realtime, but we can imagine it looking nice. It will have aliasing issues on regions of high frequency detail, like the lashes on a human face, so it requires many samples to avoid that artifact. We bake normalmaps on a low-poly base mesh, and all our problems disappeared. Right? Now it's fast and it doesn't shimmer. Cool. How? How comes that that aliasing magically disappeared? Isn't it a bit fishy?

**Normalmaps: a few pixels wide detail**

Normalmaps suffer from two main issues.

The first one is that they are not really that good at capturing surface variations. Imagine some thin steps, or square ridges on a flat surface. The normals in tangent space will be all "up" but hey, we had some dramatic discontinuities (steps) where are they? Of course, you lost them in the resolution of your normalmap. Now, steps are not representable no matter what obviously (discontinuity = infinite frequency = no resolution will be enough) but you might think, ok, I create a normalmap with a high resolution, create a bit of bevel around these edges so the normalmap captures it et voilà, problem solved. Right?

This introduces us to the second problem, which puts the nail on the coffin. Normalmaps don't antialias well. They are textures, so on the GPU they are antialiased by some sort of pre-filtering (i.e. mipmaps). We will get always a normal per sample (and MSAA does not give you more shading samples, only depth/geometry ones), in the end (unless we do crazy stuff in the shader that I've never seen done but maybe it would be a cool idea to try...) thus it will take little to zoom out enough to have our normals disappear and become flat again due to the averaging done by filtering. It takes actually _really_ little.

You might want to think about this a bit, and I could make lots of examples, but in the end normalmaps won't cut it, by their nature of being a derivative surface measure they take quite a bit of space to encode details, and can reproduce them faithfully only if there is no minification, so if a feature takes five texels on a normalmap, you might get good results if on-screen that feature still takes five pixels, when you start zooming out it will fade to flat normals again.

Unfortunately some times artists fail to recognize that, and they "cheat" themselves into thinking that certain features are wider than they are, because if they model them realistically they won't show. Thus, we get faces with huge pores and thick lashes or facial hair.

Or models which are covered with detail in the three-five pixel frequency range but that does not exhibit any finer one geometry-wise (other than the geometry edges) and creates a very weird look where the frequencies do not match between colourmaps, normalmaps and geometry, almost like a badly cast plastic toy whose geometry could not hold well the detail.

It also doesn't help that this issue is largely not present in offline rendering, where proper supersampling is able to resolve subpixel detail correctly from normalmaps, thus there is some mismatch in the experience between the same technique used with different rendering algorithms.

![]() |

**So what?**

How can we solve this? By now some ideas should be circulating around your head. Prefiltering versus postfiltering (supersampling). Averaging some quantities and then performing some operations (lighting) versus performing operations on the individual quantities and then averaging? These problems should be familiar, one day I'll write something about it, but always remember than a given rendering technique is not so much useful per se as it is as a part of a "generic" idea that we can apply... For example, a similar-sounding problem could be shadow filtering... and VSM...

But let's step back again a second. The problem with mipmapping basically means that far enough, normalmaps will always suck right? And what we want really is to find a mean to capture the average of the illumination all these bunch of tiny normals that we can't express in a given miplevel would have created. Some sort of "baking"...

Mhm but this averaging illumination... Isn't that what a material, a shader, and a BDRF exactly do? You know, the whole "there is no diffuse material" but really it's just that if you zoom close enough, a lot of tiny fragments in the material are all rough and oriented in different directions and thus scatter light everywhere, in a "diffuse" way... We ignore these geometrical details because they are way too small to capture and we created a statistical around them! Sounds promising. What could we use?

Well, lots of things, but two of them are _really common_ and underused, and you have them already (most probably) so why not...

**Occlusion maps: pixel-sized detail**

One great way to encode geometric detail, maybe surprisingly, is to use occlusion. The sharper, the smaller a depression is, the more occluded it will be.

And occlusion is really easy to encode. And it mipmaps "right", because it's something that we apply _after_ lighting, it's not a measure that we need to compute lighting. Thus the average in a mipmap will still make sense, as we don't need to transform that by a function that we can't distribute over the mipmap averaging...

|

Also, chances are that a lot of your detail will come from the specular, as the specular more high-frequency than diffuse. And chances are that you already have a specular map around... Profit!

Ok but what if we have geometric details which cause sharp lighting discontinuities but not occlusion related. For example, round rivets on a metal tank's body. Or transparent sweat beads on a man's forehead. What could we do then?

**Exponent maps: specular detail to the subpixel**

The two examples I just made are convenient. Round, highly specular shapes. What does that do, lighting wise?

Photographers are known to use the reflection of the lights in the eyes to help them reverse engineering the lighting in a photo. These round shapes will then do something similar, capture the light from any direction.

And as they are highly specular, they will create a strong reflection if there is any strong light anywhere in their field of view, in the field of view of the hemisphere. This strong reflection, even if it's small, will still be significantly visible even if we look at the feature far enough not to be able to resolve, in our samples, the spherical shape itself.

So that is interesting. In a way this surface which has a high phong exponent and creates sharp highlights, when seen from far away acts as a surface with a much lower exponent, that shines if a light is "in view" from the surface and not only at very narrow viewing angle. Is this surprising even though? Really not right? We already know that in reality our materials are made by purely specular, tiny fragments, that average together to create what we model with Phong exponents of whatever other equation.

Sweat on a face though is usually better modeled, for the typical viewing distances found in videogames, as streaks of lower exponents in the material "gloss" map, instead of using normalmaps. This also completes the answer to the original question, at the beginning of the post...

**Conclusion**

So that's it, right? Tricks for artists to express detail, done.

Well, sort-of. Because what we said so far kinda works only at a given scale (the occlusion does not). But what if I need to express a material at all scales. What if I want to zoom close enough to see the sweat droplets, and then pan backwards? I would need a model where up close the sweat layer uses normalmaps and a high specular exponent, but far away the normals get "encoded" in the BRDF by lowering the gloss exponent instead...

Well. Yes. We can do exactly that! Luckily, we have mipmapping which lets us encode different properties of a material at different scales. We don't have to straight average from the top miplevel in order to generate mipmaps... We can get creative!

And indeed, we are getting creative.



Now if you were following, you should also understand why I mentioned VSM and shadows... One idea could be to be able to extract variance from the hardware filtering operation (which is a general idea which is _always_ cool, I'll show that in another post... soon) and use that variance somehow to understand how big is the normal bundle we have to express.



While I was chatting about all this with a coworker, he brought to my attention the work that COD:BlackOps did (I guess I was distracted during Siggraph...), that is exactly along these lines (kudos to them, I love COD rendering)... They directly use this variance to modify the gloss amount, and to bake that in mipmaps, so we don't have to compute anything at runtime, only during mipmap generation we take the variance of the normalmaps in a given mip texel and use that to modify the gloss... Simple implementation, great idea!

[Lean](http://www.csee.umbc.edu/~olano/papers/)and[Clean](http://gaim.umbc.edu/2011/07/24/shiny-and-clean/), and more to the point, Clean translated into[exponent maps](http://advances.realtimerendering.com/s2011/Lazarov-Physically-Based-Lighting-in-Black-Ops%20(Siggraph%202011%20Advances%20in%20Real-Time%20Rendering%20Course).pptx). Or transitioning from a model to an entirely different one, for[oceans](http://onlinelibrary.wiley.com/doi/10.1111/j.1467-8659.2009.01618.x/full)or[trees](http://evasion.inrialpes.fr/~Eric.Bruneton/)...Now if you were following, you should also understand why I mentioned VSM and shadows... One idea could be to be able to extract variance from the hardware filtering operation (which is a general idea which is _always_ cool, I'll show that in another post... soon) and use that variance somehow to understand how big is the normal bundle we have to express.

While I was chatting about all this with a coworker, he brought to my attention the work that COD:BlackOps did (I guess I was distracted during Siggraph...), that is exactly along these lines (kudos to them, I love COD rendering)... They directly use this variance to modify the gloss amount, and to bake that in mipmaps, so we don't have to compute anything at runtime, only during mipmap generation we take the variance of the normalmaps in a given mip texel and use that to modify the gloss... Simple implementation, great idea!

But it's also a matter of educating artists, and I was really happy to see that one of our artists here proposed to drop normalmaps now that our game is rendering from a more open viewpoint, because they were not able to provide good detail (either too noisy if too little filtering or too flat), and resorted to specular maps instead for the purpose.

You might even think that you could take all your maps, and a BRDF, and compute maps and mipmaps for the same BRDF or another BRDF re-fitted to best match the lighting from the original at a given scale... And this is really what I was working on... but this article is already too big and my Mathematica example is too stupid, so I'll probably post that in a follow-up article. Stay tuned...

![]() |

P.S. From twitter people reminded me of these other references, which I admit I knew about but didn't read yet (shame on me!):

Also an addendum, when thinking about aliasing... what about specular aliasing due to geometric detail? I actually started looking into that before thinking about this. Differential operators in the shaders could be used to evaluate curvature for example, but really I found it to be hard to have problems because of geometric normals even for the dense models I was using, you really need very high exponents, so I dropped that and went to analyze normalmaps instead.

[http://www.cs.columbia.edu/cg/normalmap/index.html](http://www.cs.columbia.edu/cg/normalmap/index.html),[http://developer.nvidia.com/content/mipmapping-normal-maps](http://developer.nvidia.com/content/mipmapping-normal-maps),[http://blog.selfshadow.com/2011/07/22/specular-showdown/](http://blog.selfshadow.com/2011/07/22/specular-showdown/)Also an addendum, when thinking about aliasing... what about specular aliasing due to geometric detail? I actually started looking into that before thinking about this. Differential operators in the shaders could be used to evaluate curvature for example, but really I found it to be hard to have problems because of geometric normals even for the dense models I was using, you really need very high exponents, so I dropped that and went to analyze normalmaps instead.

## 10 comments:

Hey, interesting post. I've been working on physical based shading lately, and this is something I'm currently researching, so great timing!

I do have some questions though.

You mention "Occlusion maps", do you mean something like pre-baked ambient occlusion here? Otherwise I'm not entirely sure what occlusion maps are supposed to be ...

Also, did I understood correctly that you dropped normal maps entirely?

What are your thoughts on the work Crytek was doing into making normal mapping better? That included better compression methods and accurate storage in the g-buffer.


Is this not enough or is the MipMapping issue the real killer?

Hi,





Good article. I like you way to see the problem as pre/post filtering!

I have just two remarks:

- You definitely should read this article : http://hal.inria.fr/inria-00589940/en . It sums up the main methods/techniques used for filtering non-linear functions in computer graphics, especially for normal map.

- Just to be right, you said : "We already know that in reality our materials are made by purely specular, tiny fragments, that average together to create what we model ...". Lot of people are confusing about that. It is not the reality. In reality light waves interact with atoms/electrons. What you describe is just a physical model for explaining what is happening :)

Sander: I just mean to mind about occlusions, as a mean to "encode detail" in general. Then yes, you can think about baked AO or multiplying the occlusion in the diffuse and specular or as in the example I made for skin (where diffuse SSS makes occlusion less relevant there) just use specular occlusion (you might also want to have a higher exponent inside the pores, as the normals there are occluded thus restricting the range of the possible specular highlight but it's probably overkill)

Daniel: mipmapping is the core issue yes

Charles: Thanks for the link. And I acknowledge that saying "in reality" is an abuse, but you made the same mistake. In reality we don't have microfacets nor atoms, they are _all_ physical models of reality and I just choose the one that fits better the domain I was working in :)

I'm not a programmer, could I make a shader in UDK's material nodes that just increases the gloss and fades the normal map as the pixel depth increases? would this give roughly the same effect?

Just curious.. have you had a chance to form an opinion about Toksvig's Normal mipmapping approach?

Anon1: You could widen a bit of gloss as the normalmap mip increases (no need to fade the normalmap as it will "fade" itself automatically, that's the problem), but that will "work" only for normalmaps that are more or less equally rough everywhere (could be a workaround for skin pores fading away with mips, for example). A normalmap that has flat areas, and rough ones, won't work correctly with just a constant change everywhere

Anon2: Toksvig is in general a very nice idea. Honestly I don't know how much better a custom fit like the one I sketch in mathematica would work over Toksvig, mine was just an exercise. In general though, the point is to understand Toksvig and Lean and Clean and know that following the same principles you can/should formulate your own based on whatever shading model you're employing.

Post a Comment
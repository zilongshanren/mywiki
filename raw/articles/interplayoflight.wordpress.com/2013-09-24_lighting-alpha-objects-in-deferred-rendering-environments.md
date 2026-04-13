---
title: Lighting alpha objects in deferred rendering environments
url: https://interplayoflight.wordpress.com/2013/09/24/lighting-alpha-objects-in-deferred-rendering-contexts/
author: Kostas Anagnostou
published: '2013-09-24'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

For one of my lunchtime projects some time ago I did a bit of research on how can objects with transparent materials be lit using a deferred renderer. Turns out there are a few of ways to do it:

1) The most obvious solution is to create a [Deep GBuffer](http://www.humus.name/index.php?page=3D&ID=75) with as many extra layers as the number of alpha surfaces we expect to blend. Memory-wise this can easily get out of hand though. An alternative to that (supported by DX11-class APIs) would be to store a number of lit alpha fragments in a linked list per pixel and combining them in a final pass.

2) Another way to achieve this is in a multipass fashion using the stencil buffer, as explained in this [article](http://www.john-chapman.net/content.php?id=13). In short for all transparent objects we : A) render objects to G-buffer and mark affected pixels in stencil buffer, B) accumulate lighting into a separate buffer using the stencil buffer as a mask, C) blend result into final buffer. The main drawback of this method is that requires many iterations to account for all lights and all transparent objects.

3) Use some sort of screen door transparency like the one implemented by [Inferred rendering](http://mynameismjp.wordpress.com/2010/01/10/inferred-rendering/). This is basically opaque rendering in which the “alpha” object is rendered on top of the opaque surfaces with a stippled pattern so that it allows some of their colour through. Also [stochastic transparency](http://www.nvidia.com/docs/IO/88888/StochasticTransparency_I3D2010.pdf) is an interesting variation of screen door transparency which uses a randomised sub-pixel stipple pattern.

4) An alternative way [was presented at Develop 2012](http://www.creative-assembly.com/develop-2012-the-light-fantastic/), by some Creative Assembly guys. Briefly the way this works is by unwrapping and rendering all alpha objects into a separate texture (one texture can accommodate many objects) storing world positions in each texel. Then this texture is fed to the Lighting pass and a lightmap for the alpha objects is created on the fly. At the end, the alpha objects are rendered with forward rendering using this lightmap for correct lighting.

This technique sounded interesting so I did a quick implementation using Hieroglyph’s light prepass renderer to see how it works.

We assume an environment with many coloured lights and a transparent bubble. This is how the bubble looks using forward rendering and no lighting (adding a bit of rim light). None of the scene lights affects the bubble.:

Next we unwrap the bubble and render viewspace positions to a texture. Unwrapping the mesh requires a uv set with no overlaps or mirroring:

Obviously positions can’t be rendered as colours but let’s move on. This texture is fed to the Lighting pass, which uses the positions to calculate how much each light affects a specific surface point (mainly through attenuation since we don’t store normals). The Lighting pass can take into consideration all the lights in the scene to create an alpha pass lightmap:

Finally, the bubble is rendered last using the above lightmap:

Now the bubble is correctly lit by the scene lights.

A disadvantage of this method is that if we only store positions in the “unwrapped mesh” texture, and not normals, it is impossible to do any specular using the Lighting Pass (adding a second texture to store the normals might solve this.

Another potential problem is that you can only fit so many “unwrapped” alpha objects in a texture, so this technique might be unsuitable for many alpha objects in the scene.

Finally, although large parts of the Lighting Pass can be reused, some reworking might be needed to account for the fact that we are not lighting screen space pixels any more but positions (light culling/projection will be affected).

All in all it looks like an interesting technique to render correctly lit alpha objects.

Fixed images.

Challenge: find five differences between your post and this one: http://miss-cache.blogspot.com/2012/08/lighting-transparent-surfaces-with.html :)

Also check out the follow-up: http://miss-cache.blogspot.com/2012/08/lighting-transparent-surfaces-with_26.html

Nice pair of links! I don’t know, implementation? :-)

Or lack thereof. :)
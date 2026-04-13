---
title: Yet Another This-Is-Our-GBuffer-Format Post
url: http://hacksoflife.blogspot.com/2010/12/yet-another-this-is-our-gbuffer-format.html
author: Benjamin Supnik
published: '2010-12-05'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The good news with X-Plane is that we don't have a complex legacy material system to support. If a game is well-batched, the forward renderer can associate separate shaders with batches by material, and each 'material' can thus be radically different in how it handles/transfers light. With a G-Buffer, the lighting equation must be unified and thus everything we need to know to support some common lighting format must go into the G-Buffer. (One thing you can do is pack a material index into the G-Buffer.) Fortuantely, since X-Plane doesn't have such a multi-shader beast we only had one property to save: a shininess ratio (0-1, about 8 bits of precision needed).

What we did have to support was both a full albedo and a full RGB emissive texture; additive emissive textures have been in the sim for over a decade, and authors use them heavily. (They can be modulated by datarefs within the sim, which makes them useful for animating and modulating baked lighting effects.) X-Plane 10 also has a static shadow/baked ambient occlusion type term on some of the new scenery assets that needs to be preserved, also with 8 bits of precision.

The other challenge is that X-Plane authors use alpha translucency fairly heavily; deferred renderers don't do this very well. One solution we have for airplanes is to pull out some translucent surfaces and render them post-deferred-renderer as a forward over-draw pass. But for surfaces that can't be pulled out, we need to do the least-bad thing.

The Format

Thus we pack our G-Buffer into 16 bytes:

- RGBA8 albedo (with alpha)
- RG16F normal (Z vector is reconstructed)
- RG16F depth + shadow-merged-with-shininess
- RGBA8 emissive (with alpha)

(As a side note, if we had a different layout, we could blend the shininess ratio, for example, when we keep a physical position fragment, to try to limit shininess on translucent elements.)

Note that on OS X 10.5 red-green textures are not available, so we have to fall back to four RGBA_16F textures, doubling VRAM. This costs us at least 20% fill-rate on an 8800, but the quick sanity test I did wasn't very abusive; heavier cases are probably a bit worse.

So far we seem to be surviving with a 16-bit floating point eye-space depth coordinate. It does not hold up very well in a planet-wide render though, for rendering techniques where reconstructing the position is important (e.g.

[O'Neil-style atmospheric scattering](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter16.html)). A simple workaround would be to calculate the intersection of the fragment ray with the planet directly by doing a transform of the planet sphere from model-view space. (E.g. if we know that our fragment came from a sphere, why not just work with the original mathematical sphere.)

16F depth does give us reasonably accurate shadows, at least up close, and far away the shadows are going to be limited in quality anyway. I tried logarithmic depth, but it made shadows worse.

Packing Shadowing and Shine

For the static shadow/AO ("shadow") term and the level of specularity ("shine") we have two parameters that need about 8 bits of precision, and we have a 16-bit channel. Perfect, right? Well, not so much.

- NVidia cards won't render to 16-bit integer channels on some platforms.
- ATI cards don't export a bit-cast from integer to floating point, making it hard to pack a real 16-bit int (or two 8-bit ints) into a float.
- If we change the channel to RGBA8 (and combine RG into a virtual 16F) we can't actually use the fourth byte (alpha) because the GL insists on dumping our alpha values. Extended blend would fix this but it's not supported on OS X and even on Windows you can't use it with multiple render targets.

So we simply encode 256.0 * shadow + shine. The resulting quantity gives shininess over 8 bits of precision without shadow, and reduces shininess to around 2 bits in full shadow. If you view the decoded channels separately you can see banding artifacts come in on the shine channel as the shadows kick in. But when you view the two together in the final shader, the artifacts aren't visible at all because the shadow masks out the banded shininess.

(What this trick has done is effectively recycle the exponent as a 'mixer', allocating bits between the two channels.)

Future Formats

A future extension would be to add a fifth 4-byte target. This would give us room to extend to full 32-bit floating point depth (should that prove to be useful), with shadow and shine in 8 bit channels with one new 8-bit channel left. Or alternatively we could:

- Keep Z at 16F and keep an extra channel.
- Technically if we can accept this 'lossy' packing we can get four components into an RG16F, while we can only get 3 pure 8-bit components. (This is due to how the GL manages alpha.)
- If we target hardware that provides float-to-int bit casts, we could have four 8-bit components in the new channel.

Are you storing the sign of Z for your normals somewhere in your G-Buffer?

ReplyDeleteSign of Z - nope, no need. The Z axis here is in eye space..if the normal isn't facing us, how can we see it? :-)



ReplyDeleteThis does assume that when we use back-face culling we do not rely on having the wrong-direction normal be available. This assumption is true for X-Plane.

If you did need sign-of-Z you could stash it in the depth component..there we are really assured we don't need both positive and negative values.

Interesting! :)



ReplyDelete@Benjamin there is some cases where you can see back faces due to the perspective projection (there is a Crytek presentation about normals compression to get precision where it matters showing this case). But I guess that not taking into account the sign of normal.z does not make such a huge difference in most cases.

May be it was not fitting well your rendering pipeline but: did you have a look at the "best fit normal" method?

Hi SebH,












ReplyDeleteYeah - you're right, my bad...side angled face + normal map = back-facing normal :-) But it hasn't proven to be an issue so far...generally that case means that you have some combo of:

- Your normal map is on edge, so the fact that it is flat and not really extruded is perhaps more of an issue, particularly if it is 'heavily extruded'.

- You may have some anisotropic filtering, but the as you approach 90 degrees the quality of the texture sampling is going to get a bit fugly anyway.

So...we'll eat the marginal light cost...I'll try to follow up if we find a case that forces us to stash Z somewhere.

We haven't played with Crytek's normal map optimization schemes yet, although I did read the paper a few weeks ago.

I'm not sure how much it would matter to us...there are basically two cases:

- Gbuffer - we're sending more than 8 bits on dx and dy. :-)

- RGBA8 normal map from an art asset...since we use tangent space normal maps, we don't need to represent every direction, and in practice monstrous amounts of deflection may not be super useful (because the art asset isn't actually extruded in 3-d).

(Side note -- I should probably verify that our art guys aren't actually pushing the normal maps farther than I think they are. :-)

The alternative to best-fit in RGB is to recycle that B channel for something else, and that's really, really tempting...we have several candidate effects we could use it for.

Another option would be to apply a non-linear scale to the dx and dy. Specular hilites tend to be really sensitive to very slight changes from perfect on-axis viewing, and thus the difference between a truly 'flat' normal (dx=dy=0) and a slightly offset one is a big deal.

Consider the relationship between the specular hilite level and the dx component of a normal (assume 2-d for easy math). It's roughly:

(sqrt(1-dx^2))^128^2.2

If you graph that, nearly all of the light falloff hapens in the first 25% of your normal space...that is to say, all of the information is crammed into 1/4 of the bits.

So (this is theoretical, I haven't tried it, and I'm sure I am not the first to think of this) it seems like it might be useful to 'compress' dx and dy of a tangent space normal map using 2-part piece-wise linear curve or some other (hopefully) cheap encoding that would use the first 50% of the channel range for the first few % of normal deflection.

If emmissive is strictly additive, why does it need alpha? Can you just premultiply RGB by A and discard A (and use the full 8 bit alpha for your shininess?)

ReplyDeleteHi Cam,






ReplyDeleteYou are right that emmissive could be pre-multiplied...it's a case where we don't have a good way to recycle the last channel. The problem is that we need alpha blending in the channel to be on so that we can do "replace" operations.

Consider if a non-lit box is drawn in front of a self-emmissive box. Where the over-draw occurs, the forward renderer would end up fully replacing the previous bright pixels with new dark ones.

With the g-buffer, the equivalent op has to happen for us per-channel. So we need to write to the emmissive channel with alpha = 1 and RGB = 0 to tell the GPU to _nuke_ what's already there and replace it with our new (non-emmissive) texels.

You are right that the _resulting_ alpha is useless, so if we could find a 3-channel renderable format, we could win. But the GL doesn't have this, it only has 1,2, or 4. And we can't reuse the alpha channel without turning blending off (so we could write something sane there instead of using our alpha out in our fragment as the 'control'). So we end up wasting it. :-( It's a cost of supporting some proximate form of blending.

(If we had only alpha _testing_ we'd turn off blending and simply kill the fragment when we didn't want to write it out.)
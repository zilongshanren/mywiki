---
title: Derivative Maps in xNormal
url: http://mmikkelsen3d.blogspot.com/2011/11/derivative-maps-in-xnormal.html
author: Morten S Mikkelsen
published: '2011-11-29'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Since I wrote this post I've written a new technical paper called "Surface Gradient Based Bump Mapping Framework" which provides important context to grasp the following and provides more insight.**

**All my papers can be found at**

[https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html](https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html)Version 3.17.8 of

[xNormal](http://www.xnormal.net/)has just been released with a new map type called a Derivative map.

The primary goal with this new map type is to provide a map that can be used with a new method for bump mapping that

**does not use tangent spaces**. There are many advantages to using this method.

1. Reduces foot-print

2. Is much better suited for synthesized surfaces/tessellation

3. Does not distinguish between regular geometry and tessellation.

4. Works with per pixel generated texture coordinates such as

[Tri-Planar Texturing](http://www.slideshare.net/icastano/cascades-demo-secrets).

5. No issues regarding multiple standards for implementation of tangent space generation.

6. Mirroring trivially works.

7. No need to recalculate tangent spaces on meshes with complex geometric deformations.

So how do you do this? It's actually fairly simple to throw into your own shader.

First I'd like to point out that the method is much more closely related to Blinn's bump mapping than it is to normal mapping. This implies that there is a bump scale, however, I'll explain in a moment how this can be auto-generated to work with derivative maps generated using xNormal.

So the shader code you use for derivative maps is still, essentially, listing 1 in my paper

["Bump Mapping Unparametrized Surfaces on the GPU"](https://www.dropbox.com/s/l1yl164jb3rhomq/mm_sfgrad_bump.pdf?dl=0). The variables dBs and dBt are the derivatives of the height value with respect to screen-space. Now the screen-space derivative of the height map can be evaluated from a derivative map using the chain rule which I explained in my previous

[blog post](http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html). You don't have to understand

the math behind it. Using it is trivial since all you do is copy the shader code from the blog post and use it to replace the dBs and dBt in listing 1 (in the paper).

The one thing I forgot to mention in my previous blog post is that you need a bump scale that you apply to dBs and dBt. This can either be a user-defined one or an auto-generated one. Auto-generating the bump scale will make the work-flow more like what artists are used to with normal maps. To do this get the xNormal sdk and open the file

**examples\mikktspace\CMIKK_TangentBasisCalculator.cpp**and grab the small function SuggestInitialScaleBumpDerivative() which returns fUseAsRenderBumpScale. Then you adapt this function to your own tools pipeline.

As for the dependency on texture resolution you can postpone the divide by

*sqrt(width*height)*until the shader which will allow you to use the same mesh specific bump_scale as a constant for many different textures should you want to mix derivatives in the pixel shader. In fact height maps and derivative maps are much better suited for mixing than normal maps. Another option you have is keeping some maps as derivative maps and others as height maps. The screen space derivative of a height map is determined using a different approach such as listing 2 in the paper. But all of the final screen-space derivatives can be mixed together whether they came from one map type or the other.

Also note that if width and height are the same then the dependency on width and height is canceled since we also scale by these to obtain dBs and dBt as was shown in the shader code from my previous

[post](http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html).

Another thing I'd like to point out is that if you make your own implementation that auto-generates the bump scale and it's not the exact same method that is entirely ok. It will not result in any disasters unlike tangent space generation mismatch in normal mapping which results in unwanted hard edges in the lighting.

Finally, for those curious about the distinction between a derivative map and a normal map the derivative map represents the derivatives of the height map

*(dBdu, dBdv)*while the normal map represents the normal of the height map

*normalize( (-dBdu, -dBdv, 1) )*. However, in the context of baking from a hi-res model the distinction is more interesting. Unlike the conventional approach where the derivatives of the surface position (tangent and bitangent) are perceived to be normalized and perpendicular to each other we don't make this approximation for baking a derivative map. The reason is that using the more accurate non orthonormal basis is significantly more compliant with the synthesized basis used to perturb the normal in the pixel shader.

Hello,




ReplyDeleteGood work!

Can you clarify some point about which transform space to use ?

For your listing 1 in you paper, I suppose you must provide position and normal in the same space to the function. Do you provide them in object space or world space or both are possible ?

As the tangent space is no more available, do you have any advice to be compatible with feature like directional lightmap of Half life 2 ? Maybe the way of generating lightmap should be rethink to not more rely on tangent space ?

Thank you

Thank you! :)





ReplyDelete> Can you clarify some point about which transform space to use ?

You can use any consistent space such as object/world/view space and yes surface position and normal have to be in the same space.

Regarding tangent space directional light maps I can see how that would be an issue though tangent space can also be recreated in a pixel shader. However, I'd probably only do this for special cases like parallax mapping. At least for bump mapping w.r.t. screen-space is cheaper and allows you to mix height derivatives acquired relative to different texture spaces which is why this method can do triplanar bump.

Additionally the derivatives can be obtained through different methods like: derivative map, height map, procedurals (w.r.t. different domains even) and all get mixed up into one height derivative w.r.t. screen-space. Much more freedom this way.

> the derivative map represents the derivatives of the height map (dBdu, dBdv) while the normal map represents the normal of the height map normalize( (-dBdu, -dBdv, 1) )


ReplyDeleteDo I read in this correctly that you can reverse this calculation by taking the normal map and dividing it by -(1/n.z) to get the derivative in the x/y direction?

Yes but using the signed values of your normal map. Mind you, however, this is technically only 100% correct when applied to normal maps that were created by converting a height map into a normal map. But in practice, for the most part, it works fine with baked normal maps too. The reason it's technically wrong for baked normal maps is because they were generated under the assumption that the tangent and bitangent are unit length and perpendicular to each other.

ReplyDelete
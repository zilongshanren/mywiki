---
title: Know your Z
url: https://c0de517e.blogspot.com/2010/08/know-your-z.html
published: '2010-08-13'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

What will the following two commented functions do? Will they break things? Could they be useful?

float4 VS(float3 pos: POSITION) : POSITION

{

float4 hPos = mul(worldViewProj,float4(pos, 1.0));


{

float4 hPos = mul(worldViewProj,float4(pos, 1.0));

// OPTION A:

//hPos /= hPos.w;

//hPos /= hPos.w;

// OPTION B:

//hPos.z *= hPos.w / farPlaneViewZ;

//hPos.z *= hPos.w / farPlaneViewZ;

return hPos;

}Answer: They will screw with your perspective interpolation in different ways.

Option A just gives the non-homogeneous space coordinates to the pipeline. It will effectively disable perspective interpolation on your texcoords, and I can't find much use for such a thing :)

Option B is more tricky. If you do the math, you'll find out that it will force the Z-buffer to contain a linear depth value, as the Z-buffer stores z/w, and z ranges from 0 to far after the projection, so by multiplying by w and dividing by far, we get the resulting z/w to be z/far.

Interestingly, it won't screw with texture coordinates as it does not touch w, so it could be really useful.

There is a problem though, that at first I overlooked untill I received a detailed mail from one of my coworkers explaining my naivete. Now z is not linear anymore when interpolated in screenspace. and that could cause all sorts of artifacts where the z on your triangles does not lie on a plane anymore... But in some cases can indeed work fine, if your objects are tassellated enough and you don't get parallel walls close to each other... Shadowmaps for your characters for example...

**: some interesting documents that I've found around...**

*Update*This is basically the same idea as the trick "B" but going into yet another space. The article fails to account for the errors the system introduces, but in the comments you can read basically the same conclusions that I wrote here:


This is an analysis that suggest to invert the z with floating point buffers, that is a very common practice. It does make sense in terms of precision but it's really required by hi-z, because of the way it works.

And last but not least, this article shows the effects of triangle orientation on the z-fighting:


## 10 comments:

A: Makes XYZ a valid screen-space position, so it can be used as a float3 once again.

B: Haven't used this one myself, but looks like it would put Z into a 0-1 range, which is useful for writing out, for a depth pre-pass or deferred shading/lighting.

If you do this in the VS and pass the result as POSITION to the rasterizer I'd say you'll get some strange results. I think option B will just compress z further and maybe bring some stuff that would have been (far-) clipped otherwise back in. So maybe this doesn't look too wrong in the end.


But I can't think of a scenario where this would be useful (in a VS -- in a PS it's another story). So? What's the solution?

As I recall, "A" will effectively disable perspective-correct interpolation.

A. IMHO NULL_PTR is right.

B. Outputs linear z values (w-buffer). Useful if You need same precision over all range (shadow mapping of smth).

Right! The first option is really a gimmick with no useful application, anyway you already have non perspectively correct intepolators if you need them (the COLOR ones) and I can't think of a reason why you should need them anyways. The second trick is actually useful. It records a linear Z from near to far. It makes eye-space position reconstruction from the depth buffer easier, it gives you a nicer distribution of your precision and so on. Someone told me that at least on some cards it screws with the near-clipping even if I could no reproduce the problem, handle with care.

I wouldn't rely on COLOR outputs to be non perspective correct.



DXSDK has this to say: "Color values input to the pixel shader are assumed to be perspective correct, but this is not guaranteed (for all hardware).".

On ATI HD5870 they are perspective correct.

>and I can't think of a reason why you should need them anyways.

Well, NVidia found a use for them here:

http://developer.download.nvidia.com/SDK/10/direct3d/Source/SolidWireframe/Doc/SolidWireframe.pdf

But I agree, it is hard to find yourself in a position where you need them.

If your z is linear, it can also royally screw up coarse-grained z-cull and z compression due to z not being linear in screen space. Have a look at this: http://www.humus.name/index.php?page=News&ID=255

MJP: Yes, I know that article and it's very neat.





I don't think it's 100% accurate, but I agree that floating point depth is in general better (and that's why indeed W buffering is not really supported nowadays).

For example when it says: "Given that the gradient is constant across the primitive it's also relatively easy to compute the exact depth range within a tile for Hi-Z culling" - I don't think this is true at all, Hi-Z gets quads as inputs as everything really past the rasterizer, quads do know all their interpolated attributes, the gradients are indeed computed by finite differences on the quads values, so I don't think the linearity of Z/W in screenspace comes into play.

"Assume for instance that you want to do edge detection on the depth buffer, perhaps for antialiasing by blurring edges. This is easily done by comparing a pixel's depth with its neighbors' depths. With Z values you have constant pixel-to-pixel deltas, except for across edges of course. This is easy to detect by comparing the delta to the left and to the right, and if they don't match (with some epsilon) you crossed an edge. And then of course the same with up-down and diagonally as well" - This sounds like a lot of processing, and it does not sound like a smart idea. The gradient will be constant across a primitive, but in such algorithms you're not interested at all at primitive to primitive edges (i.e. wireframe) but you want object to object ones, so you'll have to use a fairly large threshold anyways and you gain nothing from the linearity. Actually you loose something, because you have to be sure you either scale your threshold with your projection, or convert to view space everything, or yes, do the gradient thing that is expensive.

So in the end? Is this "trick" useful? Most of the times no, and it has some pretty nasty problems too. But in some situations you can be handy indeed, and could let you express your algorithms in clip-space without having to transform from the z-buffer values to some other space.

Nice article! How about this?


hPos.xy /= hPos.w;

hPos.w = 1;

Why don't you try? I don't predict anything good, but who knows :)


FxComposer is your friend

Post a Comment
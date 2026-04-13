---
title: Derivative Maps
url: http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html
author: Morten S Mikkelsen
published: '2011-07-27'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Since I wrote this post I've written a new technical paper called "Surface Gradient Based Bump Mapping Framework" which does a better and more complete job describing the following.**

**All my papers can be found at**

[https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html](https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html)For those interested in the paper

[Bump Mapping Unparametrized Surfaces on the GPU](https://www.dropbox.com/s/l1yl164jb3rhomq/mm_sfgrad_bump.pdf?dl=0)

which discusses an alternative method to normal mapping. I thought I'd comment on a few additional variants/use-cases.

For instance listing 2 computes the screen-space derivative of the height value. This can also be achieved using precomputed derivative maps. These texture space derivatives can be transformed to screen-space using the chain rule.

// set bFlipVertDeriv to true when texST has flipped t coordinate

int2 dim; dbmap.GetDimensions(dim.x, dim.y);

const float2 dBdUV = dim*(2*dbmap.Sample(sampler, In.texST).xy-1);

// chain rule

const float2 TexDx = ddx(In.texST);

const float2 TexDy = ddy(In.texST);

const float fS = bFlipVertDeriv ? -1 : 1; // resolved compile time

float dBs = dBdUV.x * TexDx.x + fS*dBdUV.y * TexDx.y;

float dBt = dBdUV.x * TexDy.x + fS*dBdUV.y * TexDy.y;

A demo incl. source is available for

[download](http://mmikkelsen3d.blogspot.com/2011/12/so-finally-no-tangents-bump-demo-is-up.html)and a method for achieving parallax occ./POM mapping, without tangent space, is described in this

[post](http://mmikkelsen3d.blogspot.com/2012/02/parallaxpoc-mapping-and-no-tangent.html).

The advantage to using derivative maps is a better looking visual during texture magnification especially.

The downside is of course using two channels instead of one. Advantages to either method over conventional normal mapping is of course no precomputed tangent space is needed. There are no tangent space splits in the visible region and the method works whether the surface is tessellated or just a standard triangular model.

I also want to point out that one of the significant observations made in the paper is that the underlying parametrization is irrelevant. What determines Blinn's perturbed normal is the distribution of heights and the shape of the surface. Not how the distribution of heights or the surface are parametrized. This can also be exploited in a domain shader to calculate the new normal when displacement mapping.

To do this the derivative is, again, sampled from a precomputed derivative map. It is then transformed to the corresponding domain space derivative using the chain rule. Finally, the domain space derivatives are used as dBs and dBt in listing 1 where vSigmaS and vSigmaT are replaced with the domain space surface derivatives.

Morten Mikkelsen.

Interesting modification on an old idea. You've piqued my curiosity.




ReplyDeleteAny chance you could post some an image/video/demo of your results? Also, now that there are two channels of data, have you looked at compression of said data? Will it suffer artifacts if used with DXT5 compression like standard normal maps?

Thanks for the intriguing post. ;)

PS. The last two lines could be dot products.

I must admit most of my focus has been on D3D11 compliant hardware among other reasons because of requirements on filtering standards having been raized going from d3d10 to d3d11.



ReplyDeleteMy experiments using derivative maps were done using BC5 and BC6 (and not DXT5) but in my experience there is no loss in quality over normal mapping.

Whether you're using listing 2 or derivative maps or even supporting both the sweet thing is of course that this works on all types of geometry (incl. tessellation) and there are no pregenerated spaces and no visible tangent space splits.

I thought I would just make it clear that the derivative maps I recommend here are not acquired using the (-nx/nz, -ny/nz) trick though that is of course possible. Instead I would bake out single channel 32 bit height maps and then calculate the derivative numerically as a 2D filter (off-line). This way we do not get unwanted hard edges in the lighting between faces which are adjacent at the surface but not in the unwrap (which gives tangent space splits). The reason we do not get unwanted hard edges as you often do with normal mapping is because no transformation was involved in obtaining the derivatives which is why I don't recommend (-nx/nz, -ny/nz).

ReplyDeleteThe technique also trivially works with mirrored models since the parameter domain is the screen.

Reminds me of my favorite alternate derivation for bump mapping, which I originally heard from Brian Cabral. Given some point Q on the surface, Construct a local implicit representation of the surface f(P)=0 for P in a local 3D neighborhood of Q such that grad(f)=N and |grad(f)| = |N| = 1. Also, construct a local volumetric representation for the height field h(P) such that dot(grad(h),grad(f))=0, basically the height field extended perpendicular to the surface. Then a surface displaced by h in the normal direction is f(P)-h(P)=0. The normal to that surface is normalize(grad(f)-grad(h)). You can approximate it by evaluating at Q, in which case you get normalize(N-grad(h)). Since dot(N,grad(h)) was defined to be zero, you can deconstruct grad(h) into directional derivatives in the tangent directions, which works out to regular bump mapping. But the step just before that looks a lot like your listing 3.


ReplyDeleteI wonder then if you could construct a tangent-space independent vGrad for any surface height field. You only need to know it on the surface, so could store it in a texture. Sort of the derivative map analog of a normal map. Also, if you did that, would it work out to essentially an object-space normal map, or would it have other advantages?

You probably realize this already but just in case I thought I'd point out that in the paper I show that Ken's perturbation normalize(N - grad(h)) is actually not entirely correct. You can see the visual difference in figure 2. The correct equation which is 100% identical to Blinn's perturbed normal is using the surface gradient





ReplyDeletenormalize(N - surfgrad(h)). This formulation is entirely general. It does not matter if the height h is defined on a volume or a domain.

If h is defined over a volume then the surfgrad(h) is given by eq. 2 and if defined over a 2D domain (parametrized) then by eq. 3

A super cool thing about eq. 3 is that it doesn't matter which parametrization you use. Any handy one you have will lead to the same surface gradient (since there is only one).

So assuming this was all clear let me try and understand what you mean by tangent space independent. The surface gradient is obviously confined to the tangent plane (a 3 component vector). And it does not depend on the underlying parametrization that is used. So I am not 100% sure what you mean. Perhaps you could clarify?

Cheers though :)

Morten.

Just caught this part in your post "Since dot(N,grad(h)) was defined to be zero".


ReplyDeleteSo yes you are definitely aware of the distinction I was pointing out :)

I think I am beginning to understand your question. Here is how I like to think of the surface gradient of a scalar field over a surface.




ReplyDeleteI think of it as, locally, using an arbitrary rotation that transforms the surface such that the tangent plane ends up in the XY-plane. Here we evaluate the derivatives of the height function in the x and y direction (dH/dx, dH/dy, 0). This 3 component vector is then rotated back out.

Of course another way to think of it is simply as given in eq. 2 where it's the regular gradient projected into the tangent plane.

Anyway, not sure if this brings us much closer to answering your question :) Imo this route just leads us to what we already know which is we can use any parametrization that we like.

Yeah, Brian's construction essentially projects the surface functions and surface gradients into new 3D functions defined in the local 3D neighborhood of the surface. I'd expect the math to work out the same.

ReplyDeleteWhat you'll see here though is that it does not matter what kind of local extension you have of the heights function to the 3D neighborhood. Any extension to a local open volume will work with equations 2 and 4. Perhaps not much of a surprise. And as I explained the other take-away is that any parametrization that leads to the same surface and the same distribution of heights can be used to produce the surface gradient (eq. 3) and thus Blinn's perturbed normal in eq. 4.




ReplyDeleteThe surface gradient is also useful for other things. For instance if you have some scalar function across your surface s(p) and you need ddx(s) then if you can produce the surface gradient of s then you can get ddx(s) by doing:

ddx(s) = dot(ddx(surf_pos), surf_grad(s))

and similar for ddy. Another nice thing is that ddx(surf_pos) and ddy(surf_pos) can be computed analytically so these properties could come in handy in some fancy compute shader that needs to determine ddx(s) and ddx(t) and so on to sample with filtering/mip mapping enabled.

Hey Josh,







ReplyDeleteYou were asking for some pictures/demo.

I uploaded a screen shot of this working in blender --> http://jbit.net/~sparky/makedudv/blender_support/scr_shot.png

The one on the left is using listing 2 (ie. a height map) and the one on the right is using a derivative map (the code here in the blog).

I made a patch for blender that people can try if they want which is available here -->

http://jbit.net/~sparky/makedudv/blender_support/deriv_mm.patch

Finally, I made a free tool "makedudv" which can convert height maps into derivative maps incl. support for exr and hdr.

http://jbit.net/~sparky/makedudv/

With jbit.net down, is makedudv available at another location?

DeleteMore comparisons which show differences during texture magnification.





ReplyDeletehttp://jbit.net/~sparky/blender_deriv/compare/

These test shots were a kind donation by Sean Olson of the Blender community.

At moderate scales such as shown in deriv_moddist_glsl.png you can't really tell the diff between height mapped and derivative mapped but during texture magnification you start to see the difference. The rend_*.png files were made using Blender's renderer but the glsl_*.png files were made using rendering on the gpu.

As you see the faceted appearance is gone when using derivative maps.

Great job. I really appreciate your work. It is very helpful for 3d graphic. Keep it up.

ReplyDeleteThis comment has been removed by a blog administrator.

ReplyDeleteThis comment has been removed by a blog administrator.

ReplyDelete
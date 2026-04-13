---
title: Derivative Maps
url: https://www.rorydriscoll.com/2012/01/11/derivative-maps/
author: Rory
published: '2012-01-11'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

I recently came across an interesting paper, [Bump Mapping Unparametrized Surfaces on the GPU](http://jbit.net/~sparky/sfgrad_bump/mm_sfgrad_bump.pdf) by [Morten Mikkelsen](http://mmikkelsen3d.blogspot.com/) of Naughty Dog. This paper describes an alternative method to normal mapping, closely related to bump mapping. The alluring prospect of this technique is that it doesnâ€™t require that a tangent space be defined.

Mikkelsen is apparently well-versed in academic obfuscation (tsk!), so the paper itself can be a little hard to read. If you’re interested in reading it, then I would recommend first reading Jim Blinnâ€™s [original bump mapping paper](http://research.microsoft.com/pubs/73939/p286-blinn.pdf) to understand some of the derivations.

## But Wait! Whatâ€™s Wrong with Normal Maps?

Nothing really. But if something comes along that can improve quality, performance or memory consumption then it’s worth taking a a look.

## A Quick Detour into Gradients

Given a scalar height field (i.e. a two-dimensional array of scalar values), the gradient of that field is a 2D vector field where each vector points in the direction of greatest change. The length of the vectors corresponds to the rate of change.

The contour map below represents the scalar field generated from the function ![Rendered by QuickLaTeX.com f(x,y) = 1 - (x^2 + y^2)](../../assets/1a573f47db28d7c1.png)


## Derivative Maps

The main premise of the paper is that we can project the gradient of the height field onto an underlying surface and use it to skew the surface normal to approximate the normal of the height-map surface. We can do all of this without requiring tangent vectors.

As with the original bump-mapping technique, itâ€™s not exact due to some terms being dropped due to their relatively small influence, but itâ€™s close.

There are really only two important formulae to consider from the paper. The first shows how to perturb the surface normal using the *surface gradient*. Don’t confuse the surface gradient with the gradient of the height field mentioned above! As you’ll see shortly, they’re different.

![Rendered by QuickLaTeX.com \begin{align*} {\bar{n}}'=\bar{n}-\nabla_s\beta \end{align*}](../../assets/1877ab19f9501f75.png)


Here, ![Rendered by QuickLaTeX.com {\bar{n}}'](../../assets/7687502ab1c7688d.png)

![Rendered by QuickLaTeX.com \bar{n}](../../assets/8f9107a1f252485c.png)

![Rendered by QuickLaTeX.com \nabla_s\beta](../../assets/c57cf3f03e9ecf42.png)


So how do we calculate the surface gradient from the height field gradient? Well, there’s some fun math in there which I don’t want to repeat, but if you’re interested, I would recommend reading Blinn’s paper first, then Mikkelsen’s paper. You eventually arrive at:

![Rendered by QuickLaTeX.com \begin{align*} \nabla_s\beta=\dfrac{(\sigma_t \times \bar{n} )\beta_s + (\bar{n} \times \sigma_s)\beta_t}{\bar{n} \cdot (\sigma_s \times \sigma_t)} \end{align*}](../../assets/c79001768683ff52.png)


In addition to the symbols defined previously, ![Rendered by QuickLaTeX.com \sigma_s](../../assets/9614a4924dae34e0.png)

![Rendered by QuickLaTeX.com \sigma_t](../../assets/2962581981529b20.png)

![Rendered by QuickLaTeX.com \beta_s](../../assets/6076472201830658.png)

![Rendered by QuickLaTeX.com \beta_t](../../assets/716dc675ff4477e3.png)

![Rendered by QuickLaTeX.com s](../../assets/67b3bb6cb34cfa5e.png)

![Rendered by QuickLaTeX.com t](../../assets/20ef7bb1a25431b4.png)


It’s easiest to think of this as the projection of the 2D gradient onto a 3D surface along the normal. Intuitively, this says that the surface gradient direction is pushed out on orthogonal vectors to the s/n and t/n planes by however much the gradient specifies. The denominator term is there to scale up the result when the ![Rendered by QuickLaTeX.com s](../../assets/67b3bb6cb34cfa5e.png)

![Rendered by QuickLaTeX.com t](../../assets/20ef7bb1a25431b4.png)


## Implementation

Implementing this technique is fairly straightforward once you realise the meaning of some of the variables. Since we’re free to choose the partial derivative directions ![Rendered by QuickLaTeX.com s](../../assets/67b3bb6cb34cfa5e.png)

![Rendered by QuickLaTeX.com t](../../assets/20ef7bb1a25431b4.png)

![Rendered by QuickLaTeX.com \sigma](../../assets/dc233c8d6dc11081.png)

![Rendered by QuickLaTeX.com \beta](../../assets/e768004c5cb5f97f.png)


// Project the surface gradient (dhdx, dhdy) onto the surface (n, dpdx, dpdy) float3 CalculateSurfaceGradient(float3 n, float3 dpdx, float3 dpdy, float dhdx, float dhdy) { float3 r1 = cross(dpdy, n); float3 r2 = cross(n, dpdx); return (r1 * dhdx + r2 * dhdy) / dot(dpdx, r1); } // Move the normal away from the surface normal in the opposite surface gradient direction float3 PerturbNormal(float3 n, float3 dpdx, float3 dpdy, float dhdx, float dhdy) { return normalize(normal - CalculateSurfaceGradient(normal, dpdx, dpdy, dhdx, dhdy)); }

So far, so good. Next we need to work out how to calculate the partial derivatives. The reason why we chose screen-space x and y to be our partial derivative directions is so that we can use the ddx and ddy shader instructions to generate the partial derivatives of both the position and the height.

Given a position and normal in the same coordinate-space, and a height map sample, calculating the final normal is straighforward:

// Calculate the surface normal using screen-space partial derivatives of the height field float3 CalculateSurfaceNormal(float3 position, float3 normal, float height) { float3 dpdx = ddx(position); float3 dpdy = ddy(position); float dhdx = ddx(height); float dhdy = ddy(height); return PerturbNormal(normal, dpdx, dpdy, dhdx, dhdy); }

Note that in shader model 5.0, you can use ddx_fine/ddy_fine instead of ddx/ddy to get high-precision partial derivatives.

So how does this look? At a medium distance, I would say that it looks pretty good:

But what about up close?

Uh oh! Whatâ€™s happening here? Well, there are a couple of problems…

The main problem is that the height texture is using bilinear filtering, so the gradient between any two texels is constant. This causes large blocks to become very obvious when up close. There are a couple of options for alleviating this somewhat.

One option is to use bicubic filtering. I haven’t tried it, but I would expect this to make a good difference. The problem is that it will incur an extra cost. Another option, suggested in the paper, is to add a detail bump texture on top. This helps quite a lot, but again it adds more cost.

In the image below I’ve just tiled the same texture at 10x frequency over the top. It would be better to apply some kind of noise function as in the original paper.

The second problem is more subtle. We’re getting some small block artifacts because of the way that the ddx and ddy shader instructions work. They take pairs of pixels in a pixel quad and subtract the relevant values to get the derivative. In the case of the height derivatives, we can alleviate this by performing the differencing ourselves with extra texture samples.

The first problem is pretty much a killer for me. I would rather not have to cover up a fundamental implementation issue with extra fudges and more cost.

## What Now?

It’s unfortunate that this didn’t make it into the original paper, but Mikkelsen mentions in a [blog post](http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html) that you can increase the quality by using precomputed height derivatives. This method requires double the texture storage (or half the resolution) of the ddx/ddy method, but produces much better results.

You’re probably wondering how you can possibly precompute screen-space derivatives. We don’t actually have to. Instead we can use the chain rule to transform a partial derivative from one space to another. In our case we can transform our derivatives from uv-space to screen-space if we have the partial derivatives of the uvs in screen-space.

To calculate dhdx you need dhdu, dhdv, dudx and dvdx:

![Rendered by QuickLaTeX.com \begin{align*} \dfrac{\delta h}{\delta x} = \dfrac{\delta h}{\delta u} \cdot \dfrac{\delta u}{\delta x} + \dfrac{\delta h}{\delta v} \cdot \dfrac{\delta v}{\delta x} \end{align*}](../../assets/006be7c75228cfd5.png)


To calculate dhdy you need dhdu, dhdv, dudy and dvdy:

![Rendered by QuickLaTeX.com \begin{align*} \dfrac{\delta h}{\delta y} = \dfrac{\delta h}{\delta u} \cdot \dfrac{\delta u}{\delta y} + \dfrac{\delta h}{\delta v} \cdot \dfrac{\delta v}{\delta y} \end{align*}](../../assets/7820255dd98c6e48.png)


The hlsl for this is very simple:

float ApplyChainRule(float dhdu, float dhdv, float dud_, float dvd_) { return dhdu * dud_ + dhdv * dvd_; }

Assuming that we have a texture that stores the *texel-space* height derivatives, we can scale this up in the shader to uv-space by simply multiplying by the texture dimensions. We can then use the screen space uv derivatives and the chain rule to transform from dhdu/dhdv to dhdx/dhdy.

// Calculate the surface normal using the uv-space gradient (dhdu, dhdv) float3 CalculateSurfaceNormal(float3 position, float3 normal, float2 gradient) { float3 dpdx = ddx(position); float3 dpdy = ddy(position); float dhdx = ApplyChainRule(gradient.x, gradient.y, ddx(uv.x), ddx(uv.y)); float dhdy = ApplyChainRule(gradient.x, gradient.y, ddy(uv.x), ddy(uv.y)); return PerturbNormal(normal, dpdx, dpdy, dhdx, dhdy); }

So how does this look? Well, it’s pretty much the same at medium distance.

But it’s way better up close, since we’re now interpolating the derivatives.

## Conclusions

In order to really draw any conclusions about this technique, I’m going to need to compare the quality, performance and memory consumption to that of normal mapping. That’s a whole other blog post waiting to happen…

But in theory, the pros are:

**Less mesh memory:**We don’t need to store a tangent vector, so this should translate into some pretty significant mesh memory savings.**Fewer interpolators:**We don’t need to pass the tangent vector from the vertex shader to the pixel shader, so this should be a performance gain.**Possible less texture memory:**At worst this method requires two channels in a texture. At best, a normal map takes up two channels.As Stephen Hill points out in the comments below, this is a pretty weak argument, so I’m removing it.**Easy scaling:**It’s easy to change the height scale on the fly by scaling the height derivatives. This isn’t quite so easy to get right when using normal maps. See[here](http://www.j3l7h.de/talks/2008-02-18_Care_and_Feeding_of_Normal_Vectors.pdf).

And the cons are:

**More ALU:**It’s going to be interesting to see the actual numbers, but this is probably the only thing that could put the nail in the coffin for derivative maps. The extra cost for ALU might be compensated partially by the fewer interpolators, but we’ll have to see.**Less flexible:**A normal map can represent any derivative map, but the reverse is not true. I’m not sure that this is a significant problem in practice though.**Worse quality?**I’m not sure about this one, but it’ll be interesting to see if the quality holds up.

“Easy scaling”: for a 3-channel normal map, it should just be a matter of scaling x and y (or z) and then renormalising; for a 2-channel map, you can again just scale, then reconstruct z as normal. Blending PD maps together is certainly a little less work though.

Morten was saying that he didn’t see a quality difference between PD and normal maps for BC5, but I’m wondering if that’s always the case (e.g. steep slopes, where you’d need to scale things down to stay in range).

Fair point about the scaling if you’re already doing the normalize in your shader. I suppose the nice thing about the PD scaling is that it is simply a mul. Though it’s hard to quibble about ALU instructions when PD maps already require several more! Thinking about it, I probably should have written ‘cheaper’ rather than ‘easy’.

At worst you can only get a partial derivative value of 1 unit/texel, so I don’t think that the quality should be worse than normal maps under very steep slopes. I’ll definitely try that out when I do the comparisons though.

Right, you have to normalise for PD anyway, so I don’t really see the difference when it comes to simple scaling! 🙂

Talking of performance, you might want to consider converting the images to png, since it actually takes a while to load them all here. Quick test: HeightMapFar: .bmp (786KB) -> .png (94KB).

Thanks for the feedback. I thought I actually saved them out as png, but I see that I didn’t.

I need to redo the detail texture one anyway, since I just tiled the same texture at a higher frequency, and that texture has stretching at the poles.

All of the images are now pngs. I also updated the detail texture image, and deleted the argument for easy scaling since it’s pretty weak as you suggest.

No problem! Also, sorry if my comments came across a bit negatively before; nitpicks aside, I really appreciated the post, since I haven’t had the chance to take a critical look at all of this.

[…] post is a quick follow up to my previous post on derivative maps. This time I’m going to compare the quality and performance of derivative […]

[…] post is a quick follow up to my previous post on derivative maps. This time Iâ€™m going to compare the quality and performance of derivative maps […]

First of all, Thanks for great post~

I think there is a little error.

the code

return (r1 * dhdx – r2 * dhdy) / dot(dpdx, r1);

has to be changed to

return (r1 * dhdx + r2 * dhdy) / dot(dpdx, r1);

2 Changmin:

The code is correct. ‘-‘ sign is there to account for the fact that in D3D the v texture coordinate is flipped. See this blog post by Morten Mikkelsen: http://mmikkelsen3d.blogspot.com/2011/07/derivative-maps.html

I took a look at the sign of that calculation, and Changmin is correct – it should be a plus.

Rory, this is a great blog post. Thanks !

We’ve discussed this at work, although I haven’t tried it yet (I am about to give it a go). Another advantage of the derivative maps is that blending them is much simpler, and would give better results than blending normal maps (which has been proven to, while ok, be incorrect).

This post is still very useful, thanks! And the technique works great for procedurally created stuff that never had UVs, or even polygons let alone tangents. I”m still somewhat mystified as to how the derivatives maps (2nd) version manages to look good despite all the ddx/ddy used, but it does!
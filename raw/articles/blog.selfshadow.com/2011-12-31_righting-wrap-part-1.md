---
title: Righting Wrap (Part 1)
url: https://blog.selfshadow.com/2011/12/31/righting-wrap-part-1/
author: Stephen Hill
published: '2011-12-31'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

A while back, [Steve McAuley](http://blog.stevemcauley.com/) and I were discussing physically based rendering miscellanea over a quiet pint – hardly a stretch of the imagination, since we’re English 3D programmers after all! Anyway, it turned out that we both had plans to write up a few thoughts in relation to *wrap shading*, and, following some gentle arm-twisting, Steve has [posted](http://blog.stevemcauley.com/2011/12/03/energy-conserving-wrapped-diffuse/) his. I suggest that you go and read that first if you haven’t already, then return here for a continuation of the subject.

## Bad Wrap

Wrap shading has its uses when more accurate techniques are too expensive, or simply to achieve a certain aesthetic, but common models [1][2] have some deficiencies out of the box. Neither of these is energy conserving and they don’t really play well with shadows either. On top of that, Valve’s *Half Lambert* model [2] has a fixed amount of wrap, so it can’t be tuned to suit different materials (or, perhaps, to limit shadow oddities). I’ll come back to the point about flexibility in [part 2](https://blog.selfshadow.com/2012/01/07/righting-wrap-part-2/), but first I’d like to discuss another factor that’s easily overlooked: *environmental lighting*.

If you’re set on using some form of wrap shading, then it’s not just a matter of applying it to your standard direct sources – directional, point and spot lights, for instance – it ought to be carried through to environmental lighting as well! Naturally, the importance of this depends on how strong and directional your secondary lighting is; obviously if you’re only using constant ambient then there’s no problem, but these days it’s fairly common to encode indirect lighting in *Spherical Harmonics* (SH) [3] and perhaps some additional lights as well. Fortunately, wrap shading in the context of SH lighting is easy, and much like energy conservation it’s a relatively cheap or free addition, so it’s worth considering even if the results prove to be subtle.

## Looking After the Environment

So, how do we accomplish this? Well, that’s best explained with a quick recap. If you recall, for diffuse SH lighting, we first project the lighting environment, $f$, into SH:

$$f_{l}^{m} = \int f(s)\,y_{l}^{m}(s)\,\mathrm{d}s.$$(Of course, in practice, this is commonly performed offline as a numerical integration over a cube map.)

We then convolve this with the SH-projected cosine lobe, $h$, like so:

$$c_{l}^{m} = \sqrt{\frac{4\pi}{2l+1}}h_{l}^{0}f_{l}^{m},\quad \text{where } h_{l}^{0} = \int \mathrm{cos}(s)\,y_{l}^{0}(s)\,\mathrm{d}s.$$Next, we can evaluate the lighting (more specifically, *irradiance*) for a given surface direction, $s$:

Finally, a division by $\pi$ gives us *outgoing* (or *exit*) *radiance*. Personally, I find it convenient to roll these extra terms into $h$ itself. The nice thing about this is that the convolution kernel then boils down (via analytical integration) to easy to remember values for the first three SH bands:

For further details, you can find a complete and approachable account in [4].

Now, back to wrap: adjusting things for our shading model of choice is simply a matter of replacing $\hat{h}$. Let’s try this for the simple wrap model from Green [1] that Steve already discussed:

$$\frac{1}{\pi}\int_{0}^{2\pi} \int_{0}^{\alpha} \frac{\mathrm{cos}(\theta)+w}{1+w}\mathrm{sin}(\theta)\,\mathrm{d}\theta\mathrm{d}\phi, \quad \text{where }\alpha=\mathrm{cos}^{-1}(-w).$$From Steve’s post, we know that we need an additional normalisation factor of $1 + w$ for energy conservation, so the full formula for our new convolution, which I’ll call $\hat{g}$, is:

$$ \hat{g}_{l}^{0} = \frac{1}{1 + w}\sqrt{\frac{4\pi}{2l+1}}\frac{1}{\pi}\int_{0}^{2\pi} \int_{0}^{\alpha} \frac{\mathrm{cos}(\theta)+w}{1+w}y_{l}^{0}(s)\,\mathrm{sin}(\theta)\,\mathrm{d}\theta\mathrm{d}\phi.$$You can go through a similar process of analytical integration as Steve did, only now with the additional SH basis terms $y_{l}^{0}$, or if you’re lazy like me, you can throw the formula at a package like Mathematica. Either way, once you’re done, you’ll arrive at the following (or something equivalent):

$$\hat{g} = \left[ 1, \frac{1}{3}(2 - w), \frac{1}{4}(1 - w)^2, \cdots \right].$$

We can clearly see that this reduces to the cosine convolution kernel, $\hat{h}$, when $w = 0$. In visual terms, the effect of changing $w$ is evident with a single directional light, as you would expect:

![Figure 1: Variable wrap shading (0, 0.5, 1) with a single directional light in SH.](../../assets/75b1c3ed291a3036.png)

*Figure 1: Variable wrap shading (0, 0.5, 1) with a single directional light in SH.*

On the other hand, the difference is a lot subtler with a more uniform lighting environment:

![Figure 2: Variable wrap shading (0, 0.5, 1) with a general SH environment (Grace Cathedral).](../../assets/49f9130c23c69d15.png)

*Figure 2: Variable wrap shading (0, 0.5, 1) with a general SH environment (Grace Cathedral).*

## It’s a Wrap?

Okay, confession time: this post wasn’t *just* about wrap shading, since it also serves as a foundation for future posts. For instance, [part 2](https://blog.selfshadow.com/2012/01/07/righting-wrap-part-2/) will conveniently segue into shader optimisations, which is a topic I’ve been planning to write – or, perhaps more accurately, *rant* – about in general, and I’ll also be returning to Spherical Harmonics down the line.

## References

[1] Green, S., [“Real-Time Approximations to Subsurface Scattering”](http://http.developer.nvidia.com/GPUGems/gpugems_ch16.html), GPU Gems, 2004.

[2] Mitchell, J., McTaggart, G., Green, C., [“Shading in Valve’s Source Engine”](http://www.valvesoftware.com/publications.html), Advanced Real-Time Rendering in 3D Graphics and Games, SIGGRAPH Course, 2006.

[3] Green, R., [“Spherical Harmonic Lighting: The Gritty Details”](http://www.research.scea.com/gdc2003/spherical-harmonic-lighting.pdf), GDC 2003.

[4] Sloan, P.-P, “Efficient Evaluation of Irradiance Environment Maps”, [ShaderX^2: Shader Programming Tips and Tricks with DirectX 9.0](http://tog.acm.org/resources/shaderx/), 2003.
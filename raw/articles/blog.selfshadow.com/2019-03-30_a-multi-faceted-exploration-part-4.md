---
title: A Multi-Faceted Exploration (Part 4)
url: https://blog.selfshadow.com/2019/03/30/multi-faceted-part-4/
author: Stephen Hill
published: '2019-03-30'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/34ca5fe0489ebd19.jpg)

## Bouncing Back

[Last time around](https://blog.selfshadow.com/2018/08/05/multi-faceted-part-3/), I showed that we could improve upon Imageworks’ multiple-scattering approximation by precalculating a new term, $\Ems$, from the *Heitz* model itself. This is, of course, a well-trodden path in rendering: if you can’t use something directly then try to tabulate or fit it instead!

To make this more practical, I also outlined a multiple-scattering variant of the *split integral* trick already in common use in real-time rendering, which allows the specular colour, $\Fr$, to be factored out.

I’ll now go into the details of this precomputation process, and also show how, with further crunching, we can reduce the storage and run-time cost even more.

## Walking the Walk

A practical approach for precomputing the directional albedo of a single-scattering BRDF is via Monte Carlo integration with BRDF importance sampling. 1 We can calculate $\Ems$ from the

*Heitz*model in a similar way via its random-walk sampling process.

Conceptually, each random walk starts with a ray coming from the camera, which bounces one or more times on the microsurface before finally escaping it:

Figure 1: An illustration of the random-walk sampling process. (Courtesy of Eric Heitz.)

At each bounce, some energy is lost due to absorption and the rest is reflected. 2 In the case of our copper conductor test subject, the final energy (or

*energy throughput*) is simply the product of Fresnel reflection at each bounce.

If we perform this process many times and average the final energy of every multi-bounce walk – i.e., treating single-scattering walks as having zero energy – then we obtain $\Ems$, as shown in the last post:

*Figure 2: $\Ems$ for copper GGX material.*

## Doing the Splits

As I previously discussed, we don’t want to precompute $\Ems$ directly, since it bakes in $\Fr$. Instead, we’ll precalculate factors, $\wa \ldots \wnm$, which can be used to reconstruct $\Ems$ at run time for *any* $\Fr$:

To achieve this, we’re going to make two very simple modifications to the random walk process:

-
The walk will now keep track of a

*vector*of energy throughputs, $\ea \ldots \enm$, rather than a single value. At the beginning of the walk, $\ea$, is initialised to 1 and $\eb \ldots \enm$ to 0. -
At each scattering event, the energy throughput was previously multiplied by a Fresnel factor, $F(\omega_h, \omega_r)$, where $\omega_h$ is a sampled normal and $\omega_r$ is the outgoing ray direction. If we use the Schlick Fresnel approximation for $F$, this is


$\quad$ We will now use $\ei$ to track the fraction of energy scaled by $\Fr^i$.

From Equation $\ref{eq:fres}$, we can see that that after the first bounce, a factor $\sia$ of the energy is multipled by $\Fr$ and the rest, $\ssa$, is left untinted, so we set $\ea = \ssa$ and $\eb = \sia$. On the next bounce, with a new Fresnel factor $\ssb$, we will have $\ea = \ssa \ssb$, $\eb = \sia \ssb + \ssa \sib$ and $\ec = \sia \sib$. More energy has moved from order 0 to order 1, and some from order 1 to order 2.

Working things though, the update to our energy throughput vector at each bounce can be written as

$$ \begin{align} \color{teal}{e'_0} &= \ss \, \ea \\ %\color{teal}{e'_1} &= \ss \, \eb + \si \, \ea \\ %\ldots \\ \color{teal}{e'_i} &= \ss \, \ei + \si \, \eim \ . \end{align} $$Or in code:

```
1for (int i = N - 1; i > 0; i--)
2 e[i] = mix(e[i - 1], e[i], s);
3e[0] *= s;
```


The final $\wa \ldots \wnm$ factors that we’re after are simply the averages of $\ea \ldots \enm$ over multiple runs of the random walk process (again, ignoring single scattering):

*Figure 3: Multiple-scattering Fresnel factors for GGX.*

You can see the whole process in action in this [WebGL demo](https://blog.selfshadow.com/sandbox/multi_fresnel.html), which reproduces Figure 2 as well as the decomposition shown in Figure 3.

*Note: there’s quite a bit going on in this demo, but I didn’t want to get into the weeds in this post, so I’ll write up some separate notes at a later date.*

## Losing Weights

Although it may be hard to tell from Figure 3, there is some residual energy in the bottom right corner 3 of $\wc$, and this is true for a few higher orders as well. This implies that we’d need two or three textures to store all of the factors for fully accurate results, as well as a fair amount of maths in the shader. It would be nice to slim this down!

Fortunately, since most of the energy is in the lower orders, the source polynomials for $\Ems$ can be accurately refitted to lower-order cubic curves. For instance, here’s a plot of $\Ems$ for the bottom right corner, together with the refit:

This means that, in practice, we only need a single four-channel texture and three `MAD`

instructions (when Equation $\ref{eq:ms_sum}$ is written in Horner form) to reconstruct $\Ems$ in the shader:

```
1vec3 EFms(vec3 F0, float mu, float rough)
2{
3 vec4 w = EFmsFactors(mu, rough);
4 return w.x + F0*(w.y + F0*(w.z + w.w*F0));
5}
```


I did this refitting in Mathematica using [ MiniMaxApproximation](https://reference.wolfram.com/language/FunctionApproximations/ref/MiniMaxApproximation.html) to minimise relative error, which proved important for accurately reproducing the lower end of the curves.

You can see the end result for yourself in this second [WebGL demo](https://blog.selfshadow.com/sandbox/multi_compare_1.html), which compares *Imageworks* along with the improvements discussed so far (left half), against the *Heitz* reference (right half).

*Note: I realise that not everyone has ready access to Mathematica, so I’m planning to rewrite the refitting step in either Python or C++ before publishing the complete end-to-end process on GitHub.*

## Bonus (Reading) Exercise

Up until now, I’ve been probing Imageworks’ energy-preservation solution, which approximates microfacet multiple scattering with a diffuse-like lobe. However, there are other potentially valid options here. For instance, concurrent to Imageworks’ investigations, [Emmanuel Turquin](https://twitter.com/eturquin) developed a different solution while at Industrial Light & Magic, which instead approximates the multiple scattering via a rescaled single scattering lobe. This approach has since been adopted within Unity’s High Definition Render Pipeline 4 as well Google’s

[Filament](https://google.github.io/filament/Filament.html#materialsystem/improvingthebrdfs/energylossinspecularreflectance).

With permission, I have the privilege of hosting a [technical report](https://blog.selfshadow.com/publications/turquin/ms_comp_final.pdf) from Manu that goes into all of the details of his approach and various shortcuts, along with some comparisons to *Imageworks* and *Heitz*. That said, in conclusion he also states:

“Comparisons in this report have been largely of a qualitative nature. A more thorough and quantitative analysis of the differences between the three main methods is left for future work.”


*In the next post, I hope to go some way towards providing this more detailed analysis. In the meantime, you should read Manu’s TR!*

-
For an example of this, see the

*Image-Based Lighting*section of [[Karis 2013](https://blog.selfshadow.com/publications/s2013-shading-course/)].[↩︎](https://blog.selfshadow.com#fnref:1) -
Since the focus is still on conductors, I’m ignoring refraction and transmission for now.

[↩︎](https://blog.selfshadow.com#fnref:2) -
Corresponding to low view angles and high roughness values.

[↩︎](https://blog.selfshadow.com#fnref:3) -
See the

*Multiple Scattering GGX*section of [[Lagarde and Golubev 2018](http://advances.realtimerendering.com/s2018/index.htm)].[↩︎](https://blog.selfshadow.com#fnref:4)
---
title: Specular BRDF Reference
url: http://graphicrants.blogspot.com/2013/08/specular-brdf-reference.html
author: Brian Karis
published: '2013-08-03'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[new shading model for UE4](http://blog.selfshadow.com/publications/s2013-shading-course/)I tried many different options for our specular BRDF. Specifically, I tried many different terms for to Cook-Torrance microfacet specular BRDF: $$ f(\lv, \vv) = \frac{D(\hv) F(\vv, \hv) G(\lv, \vv, \hv)}{4(\ndotl)(\ndotv)} $$ Directly comparing different terms requires being able to swap them while still using the same input parameters. I thought it might be a useful reference to put these all in one place using the same symbols and same inputs. I will use the same form as Naty [1], so please look there for background and theory. I'd like to keep this as a living reference so if you have useful additions or suggestions let me know.

First let me define alpha that will be used for all following equations using UE4's roughness: $$ \alpha = roughness^2 $$

## Normal Distribution Function (NDF)

The NDF, also known as the specular distribution, describes the distribution of microfacets for the surface. It is normalized [12] such that: $$ \int_\Omega D(\mv) (\ndotm) d\omega_i = 1 $$ It is interesting to notice all models have $\frac{1}{\pi \alpha^2}$ for the normalization factor in the isotropic case.**Blinn-Phong [2]:**$$ D_{Blinn}(\mv) = \frac{1}{ \pi \alpha^2 } (\ndotm)^{ \left( \frac{2}{ \alpha^2 } - 2 \right) } $$ This is not the common form but follows when $power = \frac{2}{ \alpha^2 } - 2$.

**Beckmann [3]:**$$ D_{Beckmann}(\mv) = \frac{1}{ \pi \alpha^2 (\ndotm)^4 } \exp{ \left( \frac{(\ndotm)^2 - 1}{\alpha^2 (\ndotm)^2} \right) } $$

**GGX (Trowbridge-Reitz) [4]:**$$ D_{GGX}(\mv) = \frac{\alpha^2}{\pi((\ndotm)^2 (\alpha^2 - 1) + 1)^2} $$

**GGX Anisotropic [5]:**$$ D_{GGXaniso}(\mv) = \frac{1}{\pi \alpha_x \alpha_y} \frac{1}{ \left( \frac{(\mathbf{x} \cdot \mv)^2}{\alpha_x^2} + \frac{(\mathbf{y} \cdot \mv)^2}{\alpha_y^2} + (\ndotm)^2 \right)^2 } $$

## Geometric Shadowing

The geometric shadowing term describes the shadowing from the microfacets. This means ideally it should depend on roughness and the microfacet distribution.**Implicit [1]:**$$ G_{Implicit}(\lv,\vv,\hv) = (\ndotl)(\ndotv) $$

**Neumann [6]:**$$ G_{Neumann}(\lv,\vv,\hv) = \frac{ (\ndotl)(\ndotv) }{ \mathrm{max}( \ndotl, \ndotv ) } $$

**Cook-Torrance [11]:**$$ G_{Cook-Torrance}(\lv,\vv,\hv) = \mathrm{min}\left( 1, \frac{ 2(\ndoth)(\ndotv) }{\vdoth}, \frac{ 2(\ndoth)(\ndotl) }{\vdoth} \right) $$

**Kelemen [7]:**$$ G_{Kelemen}(\lv,\vv,\hv) = \frac{ (\ndotl)(\ndotv) }{ (\vdoth)^2 } $$

### Smith

The following geometric shadowing models use Smith's method[8] for their respective NDF. Smith breaks $G$ into two components: light and view, and uses the same equation for both: $$ G(\lv, \vv, \hv) = G_{1}(\lv) G_{1}(\vv) $$ I will define $G_1$ below for each model and skip duplicating the above equation.**Beckmann [4]:**$$ c = \frac{\ndotv}{ \alpha \sqrt{1 - (\ndotv)^2} } $$ $$ G_{Beckmann}(\vv) = \left\{ \begin{array}{l l} \frac{ 3.535 c + 2.181 c^2 }{ 1 + 2.276 c + 2.577 c^2 } & \quad \text{if $c < 1.6$}\\ 1 & \quad \text{if $c \geq 1.6$} \end{array} \right. $$

**Blinn-Phong:**

The Smith integral has no closed form solution for Blinn-Phong. Walter [4] suggests using the same equation as Beckmann.

**GGX [4]:**$$ G_{GGX}(\vv) = \frac{ 2 (\ndotv) }{ (\ndotv) + \sqrt{ \alpha^2 + (1 - \alpha^2)(\ndotv)^2 } } $$ This is not the common form but is a simple refactor by multiplying by $\frac{\ndotv}{\ndotv}$.

**Schlick-Beckmann:**

Schlick [9] approximated the Smith equation for Beckmann. Naty [1] warns that Schlick approximated the wrong version of Smith, so be sure to compare to the Smith version before using. $$ k = \alpha \sqrt{ \frac{2}{\pi} } $$ $$ G_{Schlick}(\vv) = \frac{\ndotv}{(\ndotv)(1 - k) + k } $$

**Schlick-GGX:**

For UE4, I used the Schlick approximation and matched it to the GGX Smith formulation by remapping $k$ [10]: $$ k = \frac{\alpha}{2} $$

## Fresnel

The Fresnel function describes the amount of light that reflects from a mirror surface given its index of refraction. Instead of using IOR we instead use the parameter or $F_0$ which is the reflectance at normal incidence.**None:**$$ F_{None}(\mathbf{v}, \mathbf{h}) = F_0 $$

**Schlick [9]:**$$ F_{Schlick}(\mathbf{v}, \mathbf{h}) = F_0 + (1 - F_0) ( 1 - (\vdoth) )^5 $$

**Cook-Torrance [11]:**$$ \eta = \frac{ 1 + \sqrt{F_0} }{ 1 - \sqrt{F_0} } $$ $$ c = \vdoth $$ $$ g = \sqrt{ \eta^2 + c^2 - 1 } $$ $$ F_{Cook-Torrance}(\mathbf{v}, \mathbf{h}) = \frac{1}{2} \left( \frac{g - c}{g + c} \right)^2 \left( 1 + \left( \frac{ (g + c)c - 1 }{ (g - c)c+ 1 } \right)^2 \right) $$

## Optimize

Be sure to optimize the BRDF shader code as a whole. I choose these forms of the equations to either match the literature or to demonstrate some property. They are not in the optimal form to compute in a pixel shader. For example, grouping Smith GGX with the BRDF denominator we have this: $$ \frac{ G_{GGX}(\lv) G_{GGX}(\vv) }{4(\ndotl)(\ndotv)} $$ In optimized HLSL it looks like this:float a2 = a*a;

float G_V = NoV + sqrt( (NoV - NoV * a2) * NoV + a2 );

float G_L = NoL + sqrt( (NoL - NoL * a2) * NoL + a2 );

return rcp( G_V * G_L );

If you are using this on an older non-scalar GPU you could vectorize it as well.

### References

[1] Hoffman 2013,["Background: Physics and Math of Shading"](http://blog.selfshadow.com/publications/s2013-shading-course/)

[2] Blinn 1977, "Models of light reflection for computer synthesized pictures"

[3] Beckmann 1963, "The scattering of electromagnetic waves from rough surfaces"

[4] Walter et al. 2007,

["Microfacet models for refraction through rough surfaces"](http://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf)

[5] Burley 2012,

["Physically-Based Shading at Disney"](http://blog.selfshadow.com/publications/s2012-shading-course/)

[6] Neumann et al. 1999,

["Compact metallic reflectance models"](http://sirkan.iit.bme.hu/~szirmay/brdf6.pdf)

[7] Kelemen 2001,

["A microfacet based coupled specular-matte brdf model with importance sampling"](http://sirkan.iit.bme.hu/~szirmay/scook.pdf)

[8] Smith 1967, "Geometrical shadowing of a random rough surface"

[9] Schlick 1994,

["An Inexpensive BRDF Model for Physically-Based Rendering"](http://www.cs.virginia.edu/~jdl/bib/appearance/analytic%20models/schlick94b.pdf)

[10] Karis 2013,

["Real Shading in Unreal Engine 4"](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_notes.pdf)

[11] Cook and Torrance 1982,

["A Reflectance Model for Computer Graphics"](http://graphics.pixar.com/library/ReflectanceModel/)

[12] Reed 2013,

["How Is the NDF Really Defined?"](http://www.reedbeta.com/blog/2013/07/31/hows-the-ndf-really-defined/)

## 14 comments:

Hi,

Thanks to post all these explanations about the physical based lighting.I have tried to implement it and I got a result but I'm not sure if the calcule is really correct.Maybe could you tell me, my pixel shader code is here : http://pastebin.com/yhkL5KmC.

Thanks for the help

Thanks for posting all these, and for the great Siggraph presentation.

Thanks for the blog and video, it makes very interesting reading.

Can you add the max(0, ...) calls? E.g., in Blinn-Phong, the central factor should be: max(0, n . m)

Thanks for the posting. :)


I think that "m" in NDF may be half vector. Is it right?

Yes m stands for the microfacet normal. The NDF discribes the distribution of these microfacets. For the microfacet to reflect to the view the vector needs to be half way between the light and the view vector. So, the NDF is then telling you the amount of microfacets that line up to reflect towards that view. This is a long way to say that yes in practice you input the half vector for m.

I could understand it easily. Thanks to your lucid explanation!!

For the Beckmann/Phong G1, the definition of c is missing. It is:


c = \frac{|m \cdot n|}{\alpha \sqrt{1 - (m \cdot n)^2}}.

Great reference, thanks for writing this up! Blinn's paper is available online here http://research.microsoft.com/pubs/73852/p192-blinn.pdf if you'd like to add it to the references.

Morgan,


These functions are only defined within the hemisphere. max(0,x) or saturating are ways to make undefined parameters do something sensible. Translating these into shader code will require it as well as preventing divide by zero. I changed the Kelemen function to make it clearer. That was the only one that was ambiguous.

Replaced the Kelemen function.



Equivalent but this one uses terms more similar to the others. Uses double angle cosine identity.

dot(V,L) = 2 * dot(V,H)^2 - 1

Hi Brian, thanks for posting this.



I realize in your course notes you mention that you decided to follow disney's model of re-mapping roughness using (Roughness+1)/2.

In the UE4 source it appears that the mapping has gone away even for analytic light sources, did it not make a difference?

It does make a difference but I removed it a while ago because I felt it is less accurate.



Disney has recently done the same, mentioned in an addendum to their course notes.

Those that implement this should note the singularity that occurs when n.v is approximately 0 (diverging fresnel reflectance and complete geometric attenuation competing with each other). When computing the final result, n.v should be floored to some epsilon to prevent artifacts. In any case, viewing a surface at a completely orthogonal angle is non-physical and should not be modeled.

Post a Comment
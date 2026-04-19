---
title: Derivation of pure Specular Reflection BRDF
url: https://agraphicsguynotes.com/posts/derivation_of_pure_specular_reflection_brdf/
author: Jiayin Cao
published: '2015-10-22'
source_blog: A Graphics Guy's Note
source_site: https://agraphicsguynotes.com/
category: graphics
fetched: '2026-04-19'
---

The book “Physically Based Rendering” already explains it, however I found it a little bit confusing the first time I read the chapters, which are chapters 8.2.2/8.2.3. And I also saw that there is one error of this chapter mentioned by Jérémy Riviere in the [errata page](https://www.pbrt.org/errata-2ed.html). Although he provides a correct change on the equation however it is not clearly connected with the following context.

This is a memo for me recording the derivation of specular reflection in a more clear way.

# Questions after Reading the two Chapters

A couple of questions occurred to me last time I read these two chapters.

There is an equation at the page of 439 describing the relationship between brdf, fresnel and incident/existence radiance.

$$ L_{o}(\omega_o) = f_r( \omega_o , \omega_i ) L_i(\omega_i) = F_r(\omega_i) L_i(\omega_i)$$Looking at the first part of this equation, it says:

$$ L_{o}(\omega_o) = f_r( \omega_o , \omega_i ) L_i(\omega_i) $$Little transformation shows something really weird:

$$ f_r( \omega_o , \omega_i ) = \dfrac{L_{o}(\omega_o)}{L_i(\omega_i)} $$I was quite confused by this equation at first. Where are the missing solid angle and cosine part? It looks like a mistake to me, so I tried to look for it in the errata page and found Jérémy Riviere’s correction about this line. It says “In the first displayed equation, the middle term should be an integral over directions \omega, along the lines of the standard reflection equation.”, the equation should be the following way according to him:

$$ {L_{o}(\omega_{o}) = \int L_{i}(\omega_{i}) f( \omega_{i}, \omega_{o} ) |cos(\theta_{i})| d\omega_{i}} $$This equation itself is a correct one, it is the basic form of LTE without the emission component. However it doesn’t explain anything in the following context in a clear way. And things get more and more blurry if the integral is extended to the last part of the first equation. Actually you can’t just extend the integral to the third part at all, because Fresnel is not delta function, they are not equal at all. If the integral doesn’t goes to the third one, we have another confusion that is why we can replace the integral of brdf and others with a single Fresnel directly?

I’d say that everything is right so far except the very first one. However it is jut not clear to me how it comes with the conclusion. I spend two hours on it before I figured out a better explanation of everything above and drawing the same conclusion with pbrt’s.

# Reflection BRDF

## Relationship between Fresnel and Radiance

Let’s first see the relationship between Fresnel and incident/existence radiance. Here is the definition from wiki “When light moves from a medium of a given [refractive index](https://en.wikipedia.org/wiki/Refractive_index) n1 into a second medium with refractive index n2, both [reflection](https://en.wikipedia.org/wiki/Reflection_(physics)) and [refraction](https://en.wikipedia.org/wiki/Refraction) of the light may occur. The Fresnel equations describe what fraction of the light is reflected and what fraction is refracted (i.e., transmitted).”

To be honest I didn’t quite understand the whole theory of Fresnel, the most important part of this line is “what fraction of light”. To be more precise, I think it should be “what fraction of flux” and that’s exactly how the book uses it at the page of 442. Let’s use it the same way here:

$$ d\Phi_o = F_r(\omega_i) d\Phi_i $$Extend it in the following way:

$$ L_o(\omega_o) cos( \theta_o) sin(\theta_o) dA d\phi_o d\theta_o = F_r(\omega_i) L_i(\omega_i) cos(\theta_i) sin(\theta_i) dA d\phi_i d\theta_i$$And we have the following condition for pure reflection surface.

$$ \theta_i = \theta_o $$ $$ \phi_i = \phi_o + \pi $$That said a number of factors are cancelled out. Dropping those components, we have the new equation which is much simpler than before:

$$ L_o(\omega_o) = F_r(R(\omega_o)) L_i(R(\omega_o)) $$R is the reflection vector of its input vector around normal.

That is exactly the equation mentioned first, although without the middle part. Now let’s find the middle part.

## Relationship between BRDF and Radiance

Let’s start from the rendering equation without emission component, which is exactly how Jérémy Riviere suggested to change it.

$$ {L_{o}(\omega_{o}) = \int L_{i}(\omega_{i}) f( \omega_{i}, \omega_{o} ) |cos(\theta_{i})| d\omega_{i}}$$What we want is the exact form of BRDF, however the only thing we have so far is that it is a delta function for pure reflection surfaces, so let’s go with it first, defining the brdf this way:

$$ f( \omega_{i}, \omega_{o} ) = f_{other}(\omega_{i}, \omega_{o} ) \delta( \omega_i - R(\omega_o) ) $$$ f_{other} $ is our new target now. Drop it into the LTE mentioned above, we have this:

$$ \begin{array} {lcl} L_{o}(\omega_{o}) & = & \int L_{i}(\omega_{i}) f_{other}(\omega_{i}, \omega_{o} ) \delta( \omega_i - R(\omega_o) ) |cos(\theta_{i})| d\omega_{i} \\ & = & L_{i}(R(\omega_{o})) f_{other}(R(\omega_{o}), \omega_{o} ) |cos(R(\theta_{o}))| \end{array} $$## Connect them together

Now we can connect them together reaching the following equation:

$$ L_{o}(\omega_{o}) =L_{i}(R(\omega_{o})) f_{other}(R(\omega_{o}), \omega_{o} ) |cos(R(\theta_{o}))| =F_r(R(\omega_o)) L_i(R(\omega_o)) $$Please be noted that this is quite similar to the one mentioned first except that we have an extra cosine term here. And a big difference between this one and the suggestion from Jérémy Riviere is that there is no complex integral at all. The first part of this equation is not that important any more, focusing on the following two parts and dropping the radiance value, we have the exact form of the missing part of our brdf.

$$ f_{other}(R(\omega_{o}), \omega_{o} ) = \dfrac{F_r(R(\omega_o))}{|cos(R(\theta_{o}))|} $$Putting them together, we have the final BRDF equation:

$$ f(\omega_{i}, \omega_{o} ) = \dfrac{F_r(\omega_i) \delta( \omega_i - R(\omega_o) )}{|cos(\theta_{i})|} $$# Refraction BTDF

Relationship between Fresnel and radiance won’t be mentioned here because it is well explained in the book at the pages of 442 and 443. Here it is:

$$ L_o(\omega_o) = ( 1 - F_r(\omega_i) ) \dfrac{{\eta_o}^2}{{\eta_i}^2} L_i(\omega_i) $$Derivation of the relationship between radiance and btdf is also similar to the one mentioned above, except the fact that R is replaced with T representing the transmittance direction, T can be calculated through Snell’s law. Refraction depending on different wavelength is also ignored here. Here is the final conclusion drawn by PBRT:

$$ f(\omega_i , \omega_o) = ( 1 - F_r(\omega_i) ) \dfrac{{\eta_o}^2}{{\eta_i}^2}\dfrac{\delta( \omega_i - T(\omega_o) )}{|cos(\theta_{i})|} $$